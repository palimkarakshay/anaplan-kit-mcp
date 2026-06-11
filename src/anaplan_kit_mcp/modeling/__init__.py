"""Offline Anaplan modeling conventions linter (no tenant required).

Ported from anaplan-kit (``tooling/anaplan_kit/modeling/``, MIT, same author).
This subpackage carries the parts the MCP server's ``lint_blueprint`` tool
needs: the data model, the formula checks, the blueprint Markdown parser and
the module lint rules. Nothing here makes a network call.

Public API::

    from anaplan_kit_mcp.modeling import (
        Disco, LineItem, Module, Feature, Finding,
        KNOWN_FUNCTIONS, check_formula,
        lint_module, lint_feature, has_errors,
        render_module, parse_blueprint,
    )
"""

from __future__ import annotations

from .blueprint import parse_blueprint, render_module
from .formula import KNOWN_FUNCTIONS, check_formula
from .lint import has_errors, lint_feature, lint_module
from .model import Disco, Feature, Finding, LineItem, Module

__all__ = [
    # model
    "Disco",
    "LineItem",
    "Module",
    "Feature",
    "Finding",
    # formula
    "check_formula",
    "KNOWN_FUNCTIONS",
    # lint
    "lint_module",
    "lint_feature",
    "has_errors",
    # blueprint
    "render_module",
    "parse_blueprint",
]
