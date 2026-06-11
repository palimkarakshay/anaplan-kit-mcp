"""Offline indexing and search over the Anaplan kit's Markdown content.

Ported from anaplan-kit (``tooling/anaplan_kit/kitindex.py``, MIT, same author)
and adapted for standalone distribution: the kit content can come from an
explicit checkout *or* from the content snapshot bundled inside this package,
so ``pip install anaplan-kit-mcp`` is fully self-contained.

Everything is **pure stdlib and fully offline**: the index is built by reading
Markdown files (``docs/``, ``cookbook/``, ``blueprints/``, ``tutorials/``,
``exercises/``), scoring is simple term-frequency with heading/title/filename
boosts — no embeddings, no network, no external deps.

Content root resolution order (see :func:`find_kit_root`):

1. The ``ANAPLAN_KIT_ROOT`` environment variable (validated).
2. A discoverable anaplan-kit checkout (walking up from the working directory
   and this package, also checking each ancestor's ``anaplan-kit/`` child).
3. The content snapshot bundled in this package (``_content/``, stamped with
   the source commit in ``_content/KIT_COMMIT``).
"""

from __future__ import annotations

import difflib
import os
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ENV_ROOT = "ANAPLAN_KIT_ROOT"

#: Top-level directories whose Markdown is indexed for search.
CONTENT_DIRS = ("docs", "cookbook", "blueprints", "tutorials", "exercises")

#: Where the function-by-function formula reference lives.
FORMULA_DIR = "docs/02-formulas"

# Files that, together with a cookbook/ directory, identify an anaplan-kit checkout root.
_CHECKOUT_MARKERS = ("SOURCES.md", "LEARNING-PATH.md")

#: The stamp file that identifies a bundled/synced content snapshot root.
KIT_COMMIT_FILE = "KIT_COMMIT"

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
_TOKEN_RE = re.compile(r"[a-z0-9]+")

_SNIPPET_CHARS = 240
_MAX_TF = 5  # cap per-term frequency so one spammy section can't dominate


class KitRootNotFoundError(RuntimeError):
    """Raised when no usable kit content root can be located."""


def _is_checkout_root(path: Path) -> bool:
    """True if ``path`` is an anaplan-kit checkout root."""
    return (path / "cookbook").is_dir() and any((path / m).is_file() for m in _CHECKOUT_MARKERS)


def _is_snapshot_root(path: Path) -> bool:
    """True if ``path`` is a synced content snapshot (bundled or external)."""
    return (path / "cookbook").is_dir() and (path / KIT_COMMIT_FILE).is_file()


def _is_kit_root(path: Path) -> bool:
    return _is_checkout_root(path) or _is_snapshot_root(path)


def bundled_root() -> Path | None:
    """The content snapshot shipped inside this package, if present."""
    candidate = Path(__file__).resolve().parent / "_content"
    return candidate if _is_snapshot_root(candidate) else None


def _discover_checkout() -> Path | None:
    """Find an anaplan-kit checkout near the process or this package.

    Walks up from the current working directory and from this package's
    location; at every ancestor it also checks an ``anaplan-kit/`` child, so a
    sibling checkout (e.g. ``~/projects/anaplan-kit`` next to this repo) is
    found too.
    """
    for start in (Path.cwd().resolve(), Path(__file__).resolve().parent):
        current = start
        for _ in range(12):
            if _is_checkout_root(current):
                return current
            sibling = current / "anaplan-kit"
            if sibling != start and _is_checkout_root(sibling):
                return sibling
            if current.parent == current:
                break
            current = current.parent
    return None


def find_kit_root() -> Path:
    """Locate the kit content root (checkout or bundled snapshot).

    Resolution order:

    1. The ``ANAPLAN_KIT_ROOT`` environment variable (validated; may point at
       a checkout or at a synced content snapshot).
    2. A discoverable anaplan-kit checkout (see :func:`_discover_checkout`).
    3. The bundled content snapshot shipped inside this package.

    Raises:
        KitRootNotFoundError: If none of the above yields content (which only
            happens for broken installs — the snapshot ships in the wheel).
    """
    env = os.environ.get(ENV_ROOT)
    if env:
        candidate = Path(env).expanduser().resolve()
        if _is_kit_root(candidate):
            return candidate
        raise KitRootNotFoundError(
            f"{ENV_ROOT}={env!r} does not point at anaplan-kit content "
            "(expected a directory containing cookbook/ plus SOURCES.md, "
            f"LEARNING-PATH.md or {KIT_COMMIT_FILE})."
        )
    checkout = _discover_checkout()
    if checkout is not None:
        return checkout
    bundled = bundled_root()
    if bundled is not None:
        return bundled
    raise KitRootNotFoundError(
        "Could not locate any anaplan-kit content (no checkout found and the "
        f"bundled snapshot is missing). Set {ENV_ROOT} to an anaplan-kit checkout."
    )


def kit_commit(root: Path) -> str | None:
    """The anaplan-kit source commit a content snapshot was synced from.

    Returns ``None`` for live checkouts (which carry their own git history).
    """
    stamp = root / KIT_COMMIT_FILE
    if not stamp.is_file():
        return None
    first_line = stamp.read_text(encoding="utf-8").strip().splitlines()
    return first_line[0].strip() if first_line else None


# --- Index ----------------------------------------------------------------


@dataclass
class Section:
    """One heading-delimited chunk of a Markdown file, ready for scoring."""

    path: str  # repo-relative POSIX path
    title: str  # the document's first H1 (or filename stem)
    heading: str  # the section's own heading
    text: str  # body text of the section
    counts: Counter = field(default_factory=Counter)
    heading_tokens: frozenset = frozenset()
    title_tokens: frozenset = frozenset()
    file_tokens: frozenset = frozenset()


_index_cache: dict[str, list[Section]] = {}


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def iter_markdown_files(root: Path) -> list[Path]:
    """All indexed Markdown files under the content directories, sorted."""
    files: list[Path] = []
    for name in CONTENT_DIRS:
        base = root / name
        if base.is_dir():
            files.extend(sorted(base.rglob("*.md")))
    return files


def _parse_sections(rel_path: str, text: str) -> list[Section]:
    """Split one document into per-heading sections."""
    lines = text.splitlines()
    title = Path(rel_path).stem
    for line in lines:
        m = _HEADING_RE.match(line)
        if m and len(m.group(1)) == 1:
            title = m.group(2)
            break

    file_tokens = frozenset(_tokenize(Path(rel_path).stem.replace("-", " ")))
    title_tokens = frozenset(_tokenize(title))

    sections: list[Section] = []
    heading = title
    body: list[str] = []

    def flush() -> None:
        joined = "\n".join(body).strip()
        if not joined:
            return  # heading-only/empty chunks add noise, not signal
        section = Section(
            path=rel_path,
            title=title,
            heading=heading,
            text=joined,
            counts=Counter(_tokenize(joined)),
            heading_tokens=frozenset(_tokenize(heading)),
            title_tokens=title_tokens,
            file_tokens=file_tokens,
        )
        sections.append(section)

    for line in lines:
        m = _HEADING_RE.match(line)
        if m:
            flush()
            heading = m.group(2)
            body = []
        else:
            body.append(line)
    flush()
    return sections


def _sections(root: Path) -> list[Section]:
    """The (cached) section index for a content root."""
    key = str(root.resolve())
    cached = _index_cache.get(key)
    if cached is not None:
        return cached
    sections: list[Section] = []
    for path in iter_markdown_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        sections.extend(_parse_sections(rel, text))
    _index_cache[key] = sections
    return sections


def _area_match(rel_path: str, area: str) -> bool:
    """True if ``area`` (case-insensitive) matches part of the path."""
    needle = area.strip().lower().replace(" ", "-")
    return bool(needle) and needle in rel_path.lower()


def _snippet(text: str, terms: list[str]) -> str:
    """A short excerpt around the first matching term."""
    lowered = text.lower()
    pos = -1
    for term in terms:
        pos = lowered.find(term)
        if pos >= 0:
            break
    if pos < 0:
        pos = 0
    start = max(0, pos - 60)
    excerpt = " ".join(text[start : start + _SNIPPET_CHARS].split())
    return excerpt


def search(root: Path, query: str, area: str | None = None, limit: int = 8) -> list[dict]:
    """Ranked keyword search over the kit's Markdown.

    Scoring is per-section: capped term frequency in the body, plus boosts
    when a term appears in the section heading (+5), the document title (+3)
    or the filename (+4), scaled by the fraction of query terms matched, with
    a small whole-phrase bonus.

    Args:
        root: Content root (see :func:`find_kit_root`).
        query: Free-text query, e.g. ``"running total reset year"``.
        area: Optional path filter, e.g. ``"formulas"``, ``"cookbook"``,
            ``"time-and-forecasting"``.
        limit: Maximum number of results.

    Returns:
        Result dicts ``{path, title, heading, snippet, score}``, best first.
    """
    terms = _tokenize(query)
    if not terms or limit <= 0:
        return []
    phrase = query.strip().lower()

    scored: list[tuple[float, Section]] = []
    for sec in _sections(root):
        if area and not _area_match(sec.path, area):
            continue
        score = 0.0
        matched = 0
        for term in terms:
            term_score = float(min(sec.counts.get(term, 0), _MAX_TF))
            if term in sec.heading_tokens:
                term_score += 5.0
            if term in sec.title_tokens:
                term_score += 3.0
            if term in sec.file_tokens:
                term_score += 4.0
            if term_score:
                matched += 1
            score += term_score
        if matched == 0:
            continue
        score *= matched / len(terms)
        if len(terms) > 1 and phrase in sec.text.lower():
            score += 4.0
        scored.append((score, sec))

    scored.sort(key=lambda item: (-item[0], item[1].path, item[1].heading))
    return [
        {
            "path": sec.path,
            "title": sec.title,
            "heading": sec.heading,
            "snippet": _snippet(sec.text, terms),
            "score": round(score, 2),
        }
        for score, sec in scored[:limit]
    ]


# --- Single-document reads -------------------------------------------------


def read_doc(root: Path, rel_path: str, max_chars: int = 20000) -> dict:
    """Read one Markdown document by repo-relative path, safely.

    The path must be relative, resolve to a location **inside** the content
    root, and name a ``.md`` file — anything else is rejected.

    Raises:
        ValueError: For absolute paths, path escapes, or non-Markdown files.
        FileNotFoundError: If the file does not exist.
    """
    cleaned = (rel_path or "").strip()
    if not cleaned:
        raise ValueError("path is required (repo-relative, e.g. 'cookbook/README.md')")
    if Path(cleaned).is_absolute() or cleaned.startswith("~"):
        raise ValueError("path must be repo-relative, not absolute")
    resolved_root = root.resolve()
    resolved = (resolved_root / cleaned).resolve()
    if not resolved.is_relative_to(resolved_root):
        raise ValueError("path escapes the kit root — only files inside the kit can be read")
    if resolved.suffix.lower() != ".md":
        raise ValueError("only Markdown (.md) files can be read")
    if not resolved.is_file():
        raise FileNotFoundError(f"no such document: {cleaned}")
    text = resolved.read_text(encoding="utf-8")
    if max_chars <= 0:
        max_chars = 20000
    return {
        "path": resolved.relative_to(resolved_root).as_posix(),
        "content": text[:max_chars],
        "truncated": len(text) > max_chars,
        "total_chars": len(text),
    }


# --- Formula reference -------------------------------------------------------


_SYNTAX_RE = re.compile(r"\*\*Syntax\*\*\s*\n+```[^\n]*\n(.*?)```", re.DOTALL)
_PAREN_RE = re.compile(r"\([^)]*\)")
_FUNC_NAME_RE = re.compile(r"^[A-Z][A-Z0-9.]*$")

_MAX_SECTION_CHARS = 4000


def _heading_function_names(heading: str) -> list[str]:
    """Function names named by a reference heading.

    Handles ``### SUM``, ``### START / END`` and
    ``### SUM (as a mapping aggregator)`` style headings.
    """
    cleaned = _PAREN_RE.sub("", heading).replace("`", "")
    names: list[str] = []
    for part in cleaned.split("/"):
        name = part.strip().upper()
        if name and _FUNC_NAME_RE.match(name):
            names.append(name)
    return names


def _formula_entries(root: Path) -> dict[str, list[dict]]:
    """Map of FUNCTION NAME -> reference entries from ``docs/02-formulas``."""
    entries: dict[str, list[dict]] = {}
    base = root / FORMULA_DIR
    if not base.is_dir():
        return entries
    for path in sorted(base.glob("*.md")):
        if path.name in ("README.md", "cheatsheet.md"):
            continue
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for sec in _parse_sections(rel, text):
            names = _heading_function_names(sec.heading)
            if not names:
                continue
            syntax_match = _SYNTAX_RE.search(sec.text)
            entry = {
                "heading": sec.heading,
                "path": rel,
                "syntax": syntax_match.group(1).strip() if syntax_match else None,
                "content": sec.text[:_MAX_SECTION_CHARS].strip(),
            }
            for name in names:
                entries.setdefault(name, []).append(entry)
    return entries


def formula_lookup(root: Path, function_name: str) -> dict:
    """Look up an Anaplan function in the kit's formula reference.

    Args:
        root: Content root.
        function_name: e.g. ``"CUMULATE"`` (case-insensitive; a trailing
            ``()`` is tolerated).

    Returns:
        ``{"found": True, "function": ..., "matches": [...]}`` where each
        match has ``heading``/``path``/``syntax``/``content`` — or, when the
        function is unknown, ``{"found": False, ..., "closest": [...]}`` with
        the nearest known function names.
    """
    entries = _formula_entries(root)
    query = (function_name or "").strip().upper().rstrip("()").strip()
    if not query:
        return {"found": False, "function": "", "closest": []}
    if query in entries:
        return {"found": True, "function": query, "matches": entries[query]}

    names = sorted(entries)
    close = difflib.get_close_matches(query, names, n=5, cutoff=0.6)
    containing = [n for n in names if query in n and n not in close]
    return {
        "found": False,
        "function": query,
        "closest": (close + containing)[:8],
        "hint": f"see {FORMULA_DIR}/cheatsheet.md for the full one-line function list",
    }


# --- Cookbook recipe index ---------------------------------------------------


_BADGE_LEVEL_RE = re.compile(r"\*\*Level:\*\*\s*(L\d)")
_BADGE_AREA_RE = re.compile(r"\*\*Area:\*\*\s*([^·*]+)")


def list_recipes(root: Path, area: str | None = None) -> list[dict]:
    """Index of every cookbook recipe: title, one-line description, path.

    Args:
        root: Content root.
        area: Optional filter, matched case-insensitively against the recipe's
            category directory (e.g. ``"time-and-forecasting"``) and its badge
            Area (e.g. ``"Time & Forecasting"``).

    Returns:
        Recipe dicts ``{path, title, description, area, level}``, sorted by path.
    """
    cookbook = root / "cookbook"
    recipes: list[dict] = []
    if not cookbook.is_dir():
        return recipes
    for path in sorted(cookbook.rglob("*.md")):
        if path.name == "README.md":
            continue
        rel = path.relative_to(root).as_posix()
        category = path.parent.name if path.parent != cookbook else ""
        text = path.read_text(encoding="utf-8")

        title = Path(rel).stem
        level = None
        badge_area = ""
        for line in text.splitlines():
            m = _HEADING_RE.match(line)
            if m and len(m.group(1)) == 1 and title == Path(rel).stem:
                title = m.group(2)
            if line.lstrip().startswith(">") and "**Level:**" in line:
                level_match = _BADGE_LEVEL_RE.search(line)
                area_match = _BADGE_AREA_RE.search(line)
                level = level_match.group(1) if level_match else None
                badge_area = area_match.group(1).strip() if area_match else ""

        if area:
            needle = area.strip().lower()
            haystack = f"{category} {category.replace('-', ' ')} {badge_area}".lower()
            if needle.replace(" ", "-") not in haystack.replace(" ", "-"):
                continue

        recipes.append(
            {
                "path": rel,
                "title": title,
                "description": _recipe_description(text),
                "area": badge_area or category,
                "level": level,
            }
        )
    return recipes


def _recipe_description(text: str) -> str:
    """One-line description: the stakeholder ask, or the first prose line."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("## the ask"):
            for candidate in lines[i + 1 :]:
                stripped = candidate.strip().lstrip(">").strip()
                if stripped and not stripped.startswith("#"):
                    return stripped.strip('"“”')[:200]
            break
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", ">", "|", "```", "---")):
            continue
        return stripped[:200]
    return ""
