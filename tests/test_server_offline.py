"""Tests for the MCP server's offline knowledge tools and tool registry.

All offline: the knowledge tools read the bundled content snapshot (pinned by
conftest), no credentials exist, no network is reachable or needed.
"""

from __future__ import annotations

import asyncio

import pytest

from anaplan_kit_mcp import kitindex, server

EXPECTED_TOOLS = {
    # offline knowledge
    "search_kit",
    "read_kit_doc",
    "formula_reference",
    "list_recipes",
    "lint_blueprint",
    # live API
    "anaplan_connection_status",
    "anaplan_list_workspaces",
    "anaplan_list_models",
    "anaplan_model_metadata",
    "anaplan_run_action",
    "anaplan_run_import",
    "anaplan_run_export",
    "anaplan_run_process",
}


# --- server wiring ----------------------------------------------------------


def test_console_entrypoint_exists() -> None:
    assert callable(server.main)
    assert server.mcp.name == "anaplan-kit-mcp"


def test_all_thirteen_tools_registered() -> None:
    tools = asyncio.run(server.mcp.list_tools())
    names = {t.name for t in tools}
    assert names == EXPECTED_TOOLS
    assert len(names) == 13


# --- offline knowledge tools --------------------------------------------------


def test_search_kit_returns_ranked_results() -> None:
    result = server.search_kit("rolling forecast", area="cookbook")
    assert result["results"]
    assert all(r["path"].startswith("cookbook/") for r in result["results"])


def test_search_kit_structured_error_when_no_content(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    monkeypatch.setenv(kitindex.ENV_ROOT, str(tmp_path))
    result = server.search_kit("anything")
    assert "error" in result
    assert "results" not in result
    assert kitindex.ENV_ROOT in result["hint"]


def test_read_kit_doc_reads_a_doc() -> None:
    result = server.read_kit_doc("docs/02-formulas/README.md")
    assert "Formulas" in result["content"]


def test_read_kit_doc_rejects_escape_as_structured_error() -> None:
    result = server.read_kit_doc("../../../etc/passwd.md")
    assert "error" in result
    assert "content" not in result


def test_read_kit_doc_rejects_non_markdown() -> None:
    result = server.read_kit_doc("KIT_COMMIT")
    assert "error" in result


def test_formula_reference_finds_known_function() -> None:
    result = server.formula_reference("LOOKUP")
    assert result["found"] is True
    assert result["matches"][0]["path"].startswith("docs/02-formulas/")


def test_formula_reference_timesum() -> None:
    result = server.formula_reference("TIMESUM")
    assert result["found"] is True
    assert "TIMESUM" in (result["matches"][0]["syntax"] or "")


def test_list_recipes_tool() -> None:
    result = server.list_recipes(area="time-and-forecasting")
    assert result["count"] == len(result["recipes"]) > 0


def test_lint_blueprint_flags_convention_violations() -> None:
    # Deliberate violations: a non-DISCO prefix (BAD_PREFIX) and the
    # 'Is Actual Month?' naming the kit warns about (IS_ACTUAL_NAME).
    content = (
        "## XYZ01 Bad Module\n"
        "\n"
        "| Line Item | Format | Summary | Applies To | Formula |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| Is Actual Month? | Boolean | — | Time | — |\n"
    )
    result = server.lint_blueprint(content)
    assert result["modules_parsed"] == 1
    codes = {f["code"] for f in result["findings"]}
    assert "BAD_PREFIX" in codes
    assert "IS_ACTUAL_NAME" in codes
    assert result["ok"] is False


def test_lint_blueprint_clean_table_is_ok() -> None:
    content = (
        "## CAL01 Revenue\n"
        "\n"
        "| Line Item | Format | Summary | Applies To | Formula |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| Gross Revenue | Number | Sum | Time | `Volume * Price` |\n"
    )
    result = server.lint_blueprint(content)
    assert result["modules_parsed"] == 1
    assert result["ok"] is True


def test_lint_blueprint_empty_content() -> None:
    result = server.lint_blueprint("")
    assert result["modules_parsed"] == 0
    assert result["ok"] is True
