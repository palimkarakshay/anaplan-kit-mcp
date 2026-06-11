"""Render and parse module *blueprints* — the kit's canonical Markdown table.

Ported from anaplan-kit (``tooling/anaplan_kit/modeling/blueprint.py``, MIT, same author).

A blueprint is the table format the kit uses throughout ``blueprints/`` and
``templates/``::

    > **Level:** L2 · **Area:** Blueprint · **DISCO:** Calculations

    ## CAL01 Revenue Calculation

    | Line Item | Format | Summary | Applies To | Formula |
    | --- | --- | --- | --- | --- |
    | Gross Revenue | Number | Sum | CC × Time | `Volume * Price` |

:func:`render_module` produces that text from a :class:`~.model.Module`;
:func:`parse_blueprint` tolerantly recovers modules from real-world Markdown
(extra prose, multiple tables per file, optional heading) so that
``parse_blueprint(render_module(m))`` round-trips the line items.
"""

from __future__ import annotations

import re

from .model import Disco, LineItem, Module

# The canonical column header, matched case-insensitively with flexible spacing.
_HEADER_COLUMNS = ("line item", "format", "summary", "applies to", "formula")

# A heading line that names a module: "## CAL01 Revenue" or "**CAL01 Revenue**".
_HEADING_RE = re.compile(r"^\s*#{1,6}\s+(.*\S)\s*$")
_BOLD_HEADING_RE = re.compile(r"^\s*\*\*(.+?)\*\*\s*$")


def _badge_line(m: Module) -> str:
    """A one-line context badge above the heading."""
    return f"> **Level:** L2 · **Area:** Blueprint · **DISCO:** {m.disco.name.title()}"


def _cell(value: str | None) -> str:
    """Escape a value for a Markdown table cell (pipes break columns)."""
    text = (value or "").replace("|", "\\|").strip()
    return text or "—"


def _format_applies_to(applies_to: list[str]) -> str:
    return " × ".join(applies_to) if applies_to else "—"


def render_module(m: Module) -> str:
    """Render ``m`` as a Markdown blueprint (badge + heading + canonical table)."""
    lines: list[str] = []
    lines.append(_badge_line(m))
    lines.append("")
    lines.append(f"## {m.name}")
    lines.append("")
    lines.append("| Line Item | Format | Summary | Applies To | Formula |")
    lines.append("| --- | --- | --- | --- | --- |")
    for li in m.line_items:
        formula = li.formula
        # Wrap a non-empty formula in backticks for readability; render() strips
        # them on parse so the round-trip is clean.
        formula_cell = f"`{formula}`" if formula and formula.strip() else "—"
        row = (
            f"| {_cell(li.name)} "
            f"| {_cell(li.format)} "
            f"| {_cell(li.summary)} "
            f"| {_format_applies_to(li.applies_to)} "
            f"| {_cell_formula(formula_cell)} |"
        )
        lines.append(row)
    return "\n".join(lines) + "\n"


def _cell_formula(text: str) -> str:
    """A formula cell is already prepared; only escape stray pipes."""
    return text.replace("|", "\\|").strip()


# --- Parsing -------------------------------------------------------------


def _split_row(line: str) -> list[str]:
    """Split a Markdown table row into trimmed cell strings.

    Handles escaped pipes (``\\|``) so they don't split a cell.
    """
    # Temporarily protect escaped pipes.
    placeholder = "\x00"
    protected = line.replace("\\|", placeholder)
    # Drop the leading/trailing pipe, then split.
    protected = protected.strip()
    if protected.startswith("|"):
        protected = protected[1:]
    if protected.endswith("|"):
        protected = protected[:-1]
    cells = [c.replace(placeholder, "|").strip() for c in protected.split("|")]
    return cells


def _is_separator_row(cells: list[str]) -> bool:
    """A separator row is all dashes/colons (``| --- | :--: |``)."""
    return all(
        re.fullmatch(r":?-{1,}:?", c.strip()) is not None for c in cells if c.strip() != ""
    ) and any(cells)


def _is_header_row(cells: list[str]) -> bool:
    """True if the cells match the canonical blueprint header."""
    normalized = [c.strip().lower() for c in cells]
    return normalized[: len(_HEADER_COLUMNS)] == list(_HEADER_COLUMNS)


def _clean_formula(text: str) -> str | None:
    """Strip surrounding backticks / em-dash placeholder from a formula cell."""
    text = (text or "").strip()
    if text in ("", "—", "-"):
        return None
    # Strip a single wrapping pair of backticks.
    if text.startswith("`") and text.endswith("`") and len(text) >= 2:
        text = text[1:-1].strip()
    return text or None


def _clean_value(text: str) -> str:
    text = (text or "").strip()
    return "" if text in ("—", "-") else text


def _parse_applies_to(text: str) -> list[str]:
    text = _clean_value(text)
    if not text:
        return []
    # Tables use "×" (or "x"/"X" surrounded by spaces) to join dimensions.
    parts = re.split(r"\s*[×]\s*|\s+[xX]\s+", text)
    return [p.strip() for p in parts if p.strip()]


def _module_name_from_heading(heading: str) -> str:
    """Pull a module *code* name out of a heading line.

    Handles the kit's real headings, e.g. ``## CAL01 Revenue``,
    ``**INP01 Assumptions**`` and ``` ## `SYS04 Exchange Rates` — the FX module
    shape ``` — by stripping markdown markers and any trailing descriptive
    suffix ("— ...", "– ...", "- ...", "(...").

    Returns ``""`` for headings that are *not* module codes (prose section
    headings like "How to read a blueprint"), so a table under them parses as an
    un-named module (an INFO, not a naming error).
    """
    name = heading.strip().replace("`", "").replace("**", "")
    # Drop a trailing descriptive annotation after a dash or an opening paren.
    name = re.split(r"\s+[—–-]\s+|\s+\(", name, maxsplit=1)[0]
    name = name.strip().strip("*").strip()
    # Only accept it as a module name if it looks like a module code: three
    # letters followed by a digit (SYS01, CAL02, DAT90, OUT01, …).
    if not re.match(r"^[A-Za-z]{3}\d", name):
        return ""
    return name


def _disco_from_name(name: str) -> Disco | None:
    m = re.match(r"^\s*([A-Za-z]{3})", name)
    if not m:
        return None
    return Disco.from_prefix(m.group(1))


def parse_blueprint(md: str) -> list[Module]:
    """Parse all canonical blueprint tables found in ``md`` into modules.

    Tolerant of real kit files: prose between tables, multiple tables, optional
    ``## NAME`` / ``**NAME**`` headings preceding a table (used to name the
    module and infer its DISCO from the prefix). A table with no preceding
    heading still parses into an (un-named) module.
    """
    lines = md.splitlines()
    modules: list[Module] = []

    # Track the most recent heading so we can attach it to the next table.
    last_heading: str | None = None

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # Remember the latest heading-ish line (resets are fine; the closest
        # heading before a table wins).
        h = _HEADING_RE.match(line)
        if h:
            last_heading = h.group(1)
            i += 1
            continue
        b = _BOLD_HEADING_RE.match(line)
        if b:
            last_heading = b.group(1)
            i += 1
            continue

        # A potential table row?
        if line.lstrip().startswith("|"):
            cells = _split_row(line)
            if _is_header_row(cells):
                # The next non-blank line should be a separator; then rows.
                module, consumed = _consume_table(lines, i, last_heading)
                if module is not None:
                    modules.append(module)
                last_heading = None  # consumed
                i += consumed
                continue
        i += 1

    return modules


def _consume_table(
    lines: list[str], header_idx: int, heading: str | None
) -> tuple[Module | None, int]:
    """Parse a table starting at ``header_idx``; return (module, lines_consumed)."""
    i = header_idx + 1
    n = len(lines)

    # Skip an optional separator row.
    if i < n and lines[i].lstrip().startswith("|"):
        sep_cells = _split_row(lines[i])
        if _is_separator_row(sep_cells):
            i += 1

    line_items: list[LineItem] = []
    while i < n and lines[i].lstrip().startswith("|"):
        cells = _split_row(lines[i])
        # Stop if we hit another header row.
        if _is_header_row(cells):
            break
        if _is_separator_row(cells):
            i += 1
            continue
        # Pad/truncate to 5 columns.
        cells = (cells + ["", "", "", "", ""])[:5]
        name, fmt, summary, applies, formula = cells
        line_items.append(
            LineItem(
                name=_clean_value(name),
                format=_clean_value(fmt),
                summary=_clean_value(summary) or None,
                applies_to=_parse_applies_to(applies),
                formula=_clean_formula(formula),
            )
        )
        i += 1

    consumed = i - header_idx

    if heading:
        name = _module_name_from_heading(heading)
    else:
        name = ""
    disco = _disco_from_name(name) or Disco.CALC
    module = Module(name=name, disco=disco, line_items=line_items)
    return module, consumed
