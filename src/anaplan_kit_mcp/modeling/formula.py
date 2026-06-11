"""Offline static checks for Anaplan formula text.

Ported from anaplan-kit (``tooling/anaplan_kit/modeling/formula.py``, MIT, same author).

:func:`check_formula` runs a handful of cheap, high-value checks that catch the
formula mistakes the kit's docs call out most often — no tenant, no parser,
just string/regex heuristics. It returns a list of :class:`~.model.Finding`.

The checks intentionally err toward *useful* over *exhaustive*: an unknown
function token is reported as INFO (the known-function list may be incomplete),
while genuinely invalid syntax (banned functions, bracket misuse, single-keyword
multi-mappings, unbalanced delimiters) is reported as ERROR.
"""

from __future__ import annotations

import re

from .model import Finding

# Functions documented in docs/02-formulas/cheatsheet.md. Used only to flag
# *unknown* WORD( tokens as INFO — never to error, since this list may lag the
# platform. Operators/keywords (IF/THEN/ELSE/AND/OR/NOT/BLANK) are not "WORD("
# calls so they don't need to be here.
KNOWN_FUNCTIONS: frozenset[str] = frozenset(
    {
        # Aggregation
        "SUM",
        "AVERAGE",
        "MIN",
        "MAX",
        "COUNT",
        "ANY",
        "ALL",
        "ROUND",
        "ABS",
        # Lookup & mapping
        "LOOKUP",
        "SELECT",
        "FINDITEM",
        "FIRSTNONBLANK",
        # Time series
        "CUMULATE",
        "DECUMULATE",
        "LAG",
        "LEAD",
        "OFFSET",
        "POST",
        "PREVIOUS",
        "NEXT",
        "MOVINGSUM",
        "TIMESUM",
        "START",
        "END",
        "PROFILE",
        "YEARVALUE",
        "HALFYEARVALUE",
        "QUARTERVALUE",
        "MONTHVALUE",
        # Text
        "TEXT",
        "NAME",
        "LEFT",
        "RIGHT",
        "MID",
        "LENGTH",
        "FIND",
        "SUBSTITUTE",
        "TRIM",
        "LOWER",
        "UPPER",
        "CODE",
        "MAKELINK",
        "MAILTO",
        # Logical
        "ISBLANK",
        "ISNOTBLANK",
        # Date
        "DATE",
        "YEAR",
        "MONTH",
        "DAY",
        "WEEKDAY",
        "DAYS",
        "MONTHTODATE",
        "CURRENTPERIODSTART",
        # Financial
        "NPV",
        "IRR",
        "PMT",
        "CUMIPMT",
        # Ranking
        "RANK",
        "RANKCUMULATE",
        # Hierarchy
        "ITEM",
        "PARENT",
        "ISANCESTOR",
        "ITEMLEVEL",
    }
)

# Bracket keywords that are valid aggregation/lookup *mappings* inside [ ].
_MAPPING_KEYWORDS = (
    "SUM",
    "LOOKUP",
    "MIN",
    "MAX",
    "AVERAGE",
    "COUNT",
    "ANY",
    "ALL",
    "SELECT",
    "FIRSTNONBLANK",
)

# Time offsets that some modelers wrongly write in bracket form (e.g. [NEXT: 1]).
# The correct form is the function call NEXT(...)/LAG(...) etc.
_BANNED_BRACKET_OFFSETS = ("NEXT", "LAG", "LEAD", "OFFSET", "PREVIOUS")


def _check_balanced(text: str, location: str) -> list[Finding]:
    """Report unbalanced (), [] or unmatched single quotes."""
    findings: list[Finding] = []
    pairs = {")": "(", "]": "["}
    openers = set(pairs.values())
    stack: list[str] = []
    in_quote = False
    quote_count = 0
    n = len(text)
    for i, ch in enumerate(text):
        if ch == "'":
            # Ignore English contraction/possessive apostrophes (alphanumeric on
            # both sides, e.g. "entity's") — those are prose, not Anaplan string
            # quotes. A real item quote like Versions.'Actual' has a non-alnum
            # char on at least one side, so it is still counted.
            prev = text[i - 1] if i > 0 else ""
            nxt = text[i + 1] if i + 1 < n else ""
            if prev.isalnum() and nxt.isalnum():
                continue
            quote_count += 1
            in_quote = not in_quote
            continue
        if in_quote:
            continue
        if ch in openers:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                findings.append(
                    Finding(
                        "ERROR", "UNBALANCED", f"unbalanced '{ch}' — no matching opener", location
                    )
                )
                # keep scanning but don't pop a bad match
            else:
                stack.pop()
    if stack:
        findings.append(
            Finding(
                "ERROR",
                "UNBALANCED",
                f"unbalanced delimiter(s): {''.join(stack)} left open",
                location,
            )
        )
    if quote_count % 2 != 0:
        findings.append(
            Finding("ERROR", "UNBALANCED", "unbalanced single quote — odd number of '", location)
        )
    return findings


def _check_banned_functions(text: str, location: str) -> list[Finding]:
    """Flag ANCESTOR(/CHILDREN( — neither exists in Anaplan. Allow ISANCESTOR(."""
    findings: list[Finding] = []
    # ANCESTOR( but not ISANCESTOR( : negative lookbehind on the IS.
    if re.search(r"(?<![A-Za-z])ANCESTOR\s*\(", text) or re.search(
        r"(?<=[^A-Za-z])ANCESTOR\s*\(", text
    ):
        # Guard: ensure it's not the tail of ISANCESTOR.
        for m in re.finditer(r"ANCESTOR\s*\(", text):
            before = text[: m.start()]
            if not re.search(r"IS$", before):
                findings.append(
                    Finding(
                        "ERROR",
                        "BANNED_FUNCTION",
                        "ANCESTOR() does not exist in Anaplan — chain "
                        "PARENT(PARENT(...)) or use a SYS mapping",
                        location,
                    )
                )
                break
    if re.search(r"(?<![A-Za-z])CHILDREN\s*\(", text):
        findings.append(
            Finding(
                "ERROR",
                "BANNED_FUNCTION",
                "CHILDREN() does not exist in Anaplan — aggregate children with "
                "Summary = Sum or a SUM mapping",
                location,
            )
        )
    return findings


def _check_bracket_offsets(text: str, location: str) -> list[Finding]:
    """Flag [NEXT: n] / [LAG: n] etc. — time offsets are functions, not brackets."""
    findings: list[Finding] = []
    for kw in _BANNED_BRACKET_OFFSETS:
        if re.search(rf"\[\s*{kw}\s*:", text, re.IGNORECASE):
            findings.append(
                Finding(
                    "ERROR",
                    "BRACKET_OFFSET",
                    f"[{kw}: …] bracket syntax is invalid — use the function form {kw}(...)",
                    location,
                )
            )
    return findings


def _iter_bracket_blocks(text: str):
    """Yield ``(keyword, inner_text)`` for each ``[KEYWORD: …]`` block.

    Handles nested brackets inside the block (e.g. a LOOKUP whose mapping is
    itself a bracketed expression) by depth-tracking the matching ``]``.
    """
    for m in re.finditer(r"\[\s*([A-Za-z]+)\s*:", text):
        kw = m.group(1).upper()
        depth = 1
        i = m.end()
        start = i
        while i < len(text) and depth > 0:
            if text[i] == "[":
                depth += 1
            elif text[i] == "]":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        inner = text[start:i]
        yield kw, inner


def _check_multi_mapping(text: str, location: str) -> list[Finding]:
    """Flag single-keyword multi-mappings, e.g. ``[SUM: a, b]``.

    Under SUM/LOOKUP, every mapping needs its own keyword
    (``[SUM: a, SUM: b]``). A comma inside such a block that is *not* followed
    by another mapping keyword is the classic mistake.
    """
    findings: list[Finding] = []
    keyword_re = re.compile(r"^\s*(?:" + "|".join(_MAPPING_KEYWORDS) + r")\s*:", re.IGNORECASE)
    for kw, inner in _iter_bracket_blocks(text):
        if kw not in {"SUM", "LOOKUP"}:
            continue
        # Split the inner block on top-level commas (ignore commas nested in
        # () or [] which belong to a sub-expression).
        segments = _split_top_level(inner)
        if len(segments) <= 1:
            continue
        # First segment is the mapping for this keyword. Each *subsequent*
        # segment must itself start with a mapping keyword.
        for seg in segments[1:]:
            if not keyword_re.match(seg):
                findings.append(
                    Finding(
                        "ERROR",
                        "MULTI_MAPPING",
                        f"[{kw}: …] has multiple mappings but the extra one(s) "
                        f"lack a keyword — write [{kw}: a, {kw}: b]",
                        location,
                    )
                )
                break
    return findings


def _split_top_level(text: str) -> list[str]:
    """Split ``text`` on commas that are not nested in () or []."""
    parts: list[str] = []
    depth = 0
    cur: list[str] = []
    in_quote = False
    for ch in text:
        if ch == "'":
            in_quote = not in_quote
            cur.append(ch)
            continue
        if in_quote:
            cur.append(ch)
            continue
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def _check_hardcoded_items(text: str, location: str) -> list[Finding]:
    """WARN on hard-coded list-item references (SELECT: or Word.'Something')."""
    findings: list[Finding] = []
    if re.search(r"\[\s*SELECT\s*:", text, re.IGNORECASE):
        findings.append(
            Finding(
                "WARN",
                "HARDCODED_ITEM",
                "SELECT: pins a specific list item — prefer a LOOKUP mapping or "
                "a SYS flag (Sustainable)",
                location,
            )
        )
    # A reference like Versions.'Actual' or List.'Some Item' hard-codes a member.
    if re.search(r"[A-Za-z0-9 )\]]\.'[^']+'", text):
        findings.append(
            Finding(
                "WARN",
                "HARDCODED_ITEM",
                "hard-coded list item reference (X.'Item') — drive selection from "
                "a System flag instead (Sustainable)",
                location,
            )
        )
    return findings


def _check_if_depth(text: str, location: str) -> list[Finding]:
    """WARN when nested IF depth exceeds 3 (Auditable / Performance)."""
    upper = text.upper()
    depth = 0
    max_depth = 0
    # Walk word-boundary tokens for IF / END (THEN/ELSE keep the same IF open;
    # a fresh IF before the ELSE of the prior one increases nesting). We count
    # IF opens and close one on each matching ELSE...end. Simpler robust proxy:
    # depth = max number of IF keywords that are simultaneously "open", tracked
    # by treating each IF as +1 and each ELSE as a soft boundary is unreliable,
    # so we use the count of IF keywords nested via THEN/ELSE structure below.
    tokens = re.findall(r"\bIF\b|\bTHEN\b|\bELSE\b", upper)
    for tok in tokens:
        if tok == "IF":
            depth += 1
            max_depth = max(max_depth, depth)
        elif tok == "ELSE":
            # An ELSE closes the THEN branch of the nearest IF; the IF itself is
            # resolved at the ELSE for nesting-depth purposes once its result is
            # produced. Decrement so a flat IF/ELSE chain stays shallow.
            depth = max(depth - 1, 0)
    if max_depth > 3:
        return [
            Finding(
                "WARN",
                "NESTED_IF",
                f"nested IF depth {max_depth} > 3 — use a Boolean line item, "
                "MIN/MAX, or a LOOKUP mapping (Auditable / Performance)",
                location,
            )
        ]
    return []


def _check_unknown_functions(text: str, location: str) -> list[Finding]:
    """INFO on WORD( tokens that aren't in KNOWN_FUNCTIONS (list may be partial)."""
    findings: list[Finding] = []
    seen: set[str] = set()
    # A function call has the "(" immediately after the name, e.g. "SUM(".
    # A space before "(" (e.g. "Price (local)") is a line-item reference, not a
    # call, so we deliberately don't match it.
    for m in re.finditer(r"\b([A-Za-z][A-Za-z0-9]*)\(", text):
        name = m.group(1)
        up = name.upper()
        if up in seen:
            continue
        seen.add(up)
        if up not in KNOWN_FUNCTIONS:
            findings.append(
                Finding(
                    "INFO",
                    "UNKNOWN_FUNCTION",
                    f"'{name}(' is not in the known-function list (it may be a "
                    "newer/Polaris function, or a typo)",
                    location,
                )
            )
    return findings


def check_formula(text: str, location: str = "") -> list[Finding]:
    """Run all offline formula checks over ``text``; return collected findings.

    An empty/whitespace/``None`` formula yields no findings (a line item may
    legitimately have no formula — e.g. an input).
    """
    if not text or not text.strip():
        return []
    findings: list[Finding] = []
    findings += _check_balanced(text, location)
    findings += _check_banned_functions(text, location)
    findings += _check_bracket_offsets(text, location)
    findings += _check_multi_mapping(text, location)
    findings += _check_hardcoded_items(text, location)
    findings += _check_if_depth(text, location)
    findings += _check_unknown_functions(text, location)
    return findings
