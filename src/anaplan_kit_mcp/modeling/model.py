"""Core data model for the offline modeling tools.

Ported from anaplan-kit (``tooling/anaplan_kit/modeling/model.py``, MIT, same author).

These dataclasses describe a *feature* an Anaplan modeler is designing: a set
of modules, each holding line items, tagged by their :class:`Disco` type. They
are deliberately plain — no network, no tenant — so the lint / sizing /
blueprint tools can operate on them as pure local logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Disco(Enum):
    """The five DISCO module types and their canonical name prefixes.

    DISCO is the module-design pattern from the methodology docs: every module
    is exactly one of Data, Inputs, System, Calculations or Outputs, and its
    name is prefixed accordingly (e.g. ``SYS01 Time Settings``).
    """

    DATA = "DAT"
    INPUTS = "INP"
    SYSTEM = "SYS"
    CALC = "CAL"
    OUTPUTS = "OUT"

    @property
    def prefix(self) -> str:
        """The three-letter module-name prefix for this type (e.g. ``CAL``)."""
        return self.value

    @classmethod
    def from_prefix(cls, prefix: str) -> Disco | None:
        """Return the :class:`Disco` whose prefix matches ``prefix`` (case-insensitive).

        Returns ``None`` if no type matches — callers decide whether that is an
        error (lint) or simply "unknown" (tolerant parsing).
        """
        prefix = (prefix or "").strip().upper()
        for member in cls:
            if member.value == prefix:
                return member
        return None


@dataclass
class LineItem:
    """A single line item (a row in Anaplan's Blueprint view)."""

    name: str
    format: str
    summary: str | None
    applies_to: list[str] = field(default_factory=list)
    formula: str | None = None


@dataclass
class Module:
    """A module: a DISCO type, a name, and its line items."""

    name: str
    disco: Disco
    line_items: list[LineItem] = field(default_factory=list)


@dataclass
class Feature:
    """A feature being designed: a related collection of modules."""

    name: str
    modules: list[Module] = field(default_factory=list)


@dataclass
class Finding:
    """A single lint / sizing observation.

    ``severity`` is one of ``"ERROR"``, ``"WARN"`` or ``"INFO"``. ``code`` is a
    short stable identifier (e.g. ``"BAD_PREFIX"``) suitable for testing.
    ``location`` points at where the issue lives (module / line item / path).
    """

    severity: str
    code: str
    message: str
    location: str = ""

    def __post_init__(self) -> None:
        if self.severity not in {"ERROR", "WARN", "INFO"}:
            raise ValueError(f"invalid severity: {self.severity!r}")

    def __str__(self) -> str:
        where = f" [{self.location}]" if self.location else ""
        return f"{self.severity} {self.code}: {self.message}{where}"
