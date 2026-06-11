"""Offline lint rules for modules and features.

Ported from anaplan-kit (``tooling/anaplan_kit/modeling/lint.py``, MIT, same author).

These enforce the kit's naming + DISCO conventions on the local data model and
fold in the per-formula checks from :mod:`.formula`. Everything is pure logic —
no tenant required.
"""

from __future__ import annotations

import re

from .formula import check_formula
from .model import Feature, Finding, Module

# Formats that should normally carry a deliberate Summary choice.
_NUMERIC_FORMATS = ("number", "number (%)", "number (2 dp)", "number (4 dp)")
# Summary values that mean "not deliberately set".
_EMPTY_SUMMARIES = {"", "default"}


def _is_numeric_format(fmt: str | None) -> bool:
    fmt = (fmt or "").strip().lower()
    return fmt.startswith("number")


def lint_module(m: Module) -> list[Finding]:
    """Lint a single module and its line items. Returns all findings."""
    findings: list[Finding] = []
    name = (m.name or "").strip()
    expected = m.disco.prefix

    if not name:
        # A blueprint table the parser couldn't attribute to a heading is a
        # documentation gap, not a model error — flag as INFO, never fail on it.
        findings.append(
            Finding(
                "INFO",
                "UNNAMED_MODULE",
                "blueprint table has no detectable module name — add a '## NAME' heading "
                "above it so naming/DISCO can be checked",
                "<unnamed module>",
            )
        )
    else:
        # --- Module-name prefix must match the DISCO type. ---
        # Names look like "CAL01 Revenue": three letters + digits + space + title.
        actual_prefix_match = re.match(r"^([A-Za-z]{3})", name)
        actual_prefix = actual_prefix_match.group(1).upper() if actual_prefix_match else ""
        if actual_prefix != expected:
            findings.append(
                Finding(
                    "ERROR",
                    "BAD_PREFIX",
                    f"module name '{name}' should start with '{expected}' for a "
                    f"{m.disco.name.title()} module",
                    name,
                )
            )

        # --- Time-settings module should be SYS01, not SYS00. ---
        if re.match(r"^SYS00\b", name, re.IGNORECASE):
            findings.append(
                Finding(
                    "WARN",
                    "SYS00_TIME",
                    "time-settings module is conventionally 'SYS01 Time Settings', not 'SYS00'",
                    name,
                )
            )

    for li in m.line_items:
        loc = f"{name} → {li.name}" if li.name else f"{name} → <unnamed>"
        li_name = (li.name or "").strip()

        # --- Empty line-item name is an error. ---
        if not li_name:
            findings.append(Finding("ERROR", "EMPTY_NAME", "line item has no name", loc))

        # --- The actual/forecast flag is 'Is Actual?', not 'Is Actual Month?'. ---
        if li_name.lower() == "is actual month?":
            findings.append(
                Finding(
                    "WARN",
                    "IS_ACTUAL_NAME",
                    "the actual/forecast flag is conventionally named "
                    "'Is Actual?', not 'Is Actual Month?'",
                    loc,
                )
            )

        # --- Numeric line item with no deliberate Summary. ---
        summary = li.summary
        if _is_numeric_format(li.format):
            norm = (summary or "").strip().lower()
            if summary is None or norm in _EMPTY_SUMMARIES:
                findings.append(
                    Finding(
                        "WARN",
                        "MISSING_SUMMARY",
                        f"numeric line item '{li_name}' has no deliberate Summary "
                        "— set it (Sum/Average/None) on purpose",
                        loc,
                    )
                )

        # --- Per-formula checks, relocated to this line item. ---
        for f in check_formula(li.formula or "", loc):
            findings.append(f)

    return findings


def lint_feature(f: Feature) -> list[Finding]:
    """Lint every module in a feature; findings are tagged by module location."""
    findings: list[Finding] = []
    for m in f.modules:
        findings.extend(lint_module(m))
    return findings


def has_errors(findings: list[Finding]) -> bool:
    """True if any finding is an ERROR."""
    return any(f.severity == "ERROR" for f in findings)
