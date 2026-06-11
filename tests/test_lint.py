"""Tests for the ported blueprint parser and conventions linter (pure offline logic)."""

from __future__ import annotations

from anaplan_kit_mcp.modeling import (
    Disco,
    LineItem,
    Module,
    check_formula,
    has_errors,
    lint_module,
    parse_blueprint,
    render_module,
)


def _codes(findings) -> set[str]:
    return {f.code for f in findings}


# --- blueprint parsing -------------------------------------------------------


def test_parse_blueprint_extracts_module_and_line_items() -> None:
    md = (
        "## CAL01 Revenue\n"
        "\n"
        "| Line Item | Format | Summary | Applies To | Formula |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| Gross Revenue | Number | Sum | CC × Time | `Volume * Price` |\n"
        "| Volume | Number | Sum | CC × Time | — |\n"
    )
    modules = parse_blueprint(md)
    assert len(modules) == 1
    m = modules[0]
    assert m.name == "CAL01 Revenue"
    assert m.disco is Disco.CALC
    assert [li.name for li in m.line_items] == ["Gross Revenue", "Volume"]
    assert m.line_items[0].formula == "Volume * Price"
    assert m.line_items[0].applies_to == ["CC", "Time"]
    assert m.line_items[1].formula is None


def test_parse_blueprint_render_round_trip() -> None:
    module = Module(
        name="SYS01 Time Settings",
        disco=Disco.SYSTEM,
        line_items=[LineItem(name="Is Actual?", format="Boolean", summary=None)],
    )
    parsed = parse_blueprint(render_module(module))
    assert len(parsed) == 1
    assert parsed[0].name == "SYS01 Time Settings"
    assert parsed[0].line_items[0].name == "Is Actual?"


def test_parse_blueprint_table_without_heading_is_unnamed() -> None:
    md = (
        "| Line Item | Format | Summary | Applies To | Formula |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| Thing | Number | Sum | Time | — |\n"
    )
    modules = parse_blueprint(md)
    assert len(modules) == 1
    assert modules[0].name == ""


# --- module lint rules ---------------------------------------------------------


def test_bad_prefix_is_error() -> None:
    m = Module(name="XYZ01 Bad", disco=Disco.CALC, line_items=[])
    findings = lint_module(m)
    assert "BAD_PREFIX" in _codes(findings)
    assert has_errors(findings)


def test_sys00_time_is_warned() -> None:
    m = Module(name="SYS00 Time Settings", disco=Disco.SYSTEM, line_items=[])
    assert "SYS00_TIME" in _codes(lint_module(m))


def test_is_actual_month_naming_is_warned() -> None:
    m = Module(
        name="SYS01 Time Settings",
        disco=Disco.SYSTEM,
        line_items=[LineItem(name="Is Actual Month?", format="Boolean", summary=None)],
    )
    assert "IS_ACTUAL_NAME" in _codes(lint_module(m))


def test_missing_summary_on_numeric_line_item() -> None:
    m = Module(
        name="CAL01 Revenue",
        disco=Disco.CALC,
        line_items=[LineItem(name="Gross Revenue", format="Number", summary=None)],
    )
    assert "MISSING_SUMMARY" in _codes(lint_module(m))


def test_deliberate_summary_is_clean() -> None:
    m = Module(
        name="CAL01 Revenue",
        disco=Disco.CALC,
        line_items=[LineItem(name="Gross Revenue", format="Number", summary="Sum")],
    )
    assert lint_module(m) == []


def test_empty_line_item_name_is_error() -> None:
    m = Module(
        name="CAL01 Revenue",
        disco=Disco.CALC,
        line_items=[LineItem(name="", format="Number", summary="Sum")],
    )
    assert "EMPTY_NAME" in _codes(lint_module(m))


def test_unnamed_module_is_info_not_error() -> None:
    m = Module(name="", disco=Disco.CALC, line_items=[])
    findings = lint_module(m)
    assert "UNNAMED_MODULE" in _codes(findings)
    assert not has_errors(findings)


# --- formula checks --------------------------------------------------------------


def test_empty_formula_has_no_findings() -> None:
    assert check_formula("") == []
    assert check_formula("   ") == []


def test_unbalanced_delimiters() -> None:
    assert "UNBALANCED" in {f.code for f in check_formula("SUM(Revenue")}
    assert "UNBALANCED" in {f.code for f in check_formula("Revenue[SUM: Map")}


def test_banned_functions_ancestor_children() -> None:
    assert "BANNED_FUNCTION" in {f.code for f in check_formula("ANCESTOR(Item(Region))")}
    assert "BANNED_FUNCTION" in {f.code for f in check_formula("CHILDREN(Region)")}
    # ISANCESTOR is real and allowed.
    assert "BANNED_FUNCTION" not in {f.code for f in check_formula("ISANCESTOR(a, b)")}


def test_bracket_offset_is_error() -> None:
    assert "BRACKET_OFFSET" in {f.code for f in check_formula("Revenue[NEXT: 1]")}


def test_multi_mapping_missing_keyword() -> None:
    bad = "Source.Data[SUM: SYS02.Region, SYS02.Product]"
    good = "Source.Data[SUM: SYS02.Region, SUM: SYS02.Product]"
    assert "MULTI_MAPPING" in {f.code for f in check_formula(bad)}
    assert "MULTI_MAPPING" not in {f.code for f in check_formula(good)}


def test_hardcoded_item_select_and_member_reference() -> None:
    assert "HARDCODED_ITEM" in {f.code for f in check_formula("Revenue[SELECT: Region.North]")}
    assert "HARDCODED_ITEM" in {f.code for f in check_formula("Revenue * Versions.'Actual'")}


def test_nested_if_depth_warning() -> None:
    deep = "IF a THEN IF b THEN IF c THEN IF d THEN 1 ELSE 0 ELSE 0 ELSE 0 ELSE 0"
    assert "NESTED_IF" in {f.code for f in check_formula(deep)}
    flat = "IF a THEN 1 ELSE IF b THEN 2 ELSE 3"
    assert "NESTED_IF" not in {f.code for f in check_formula(flat)}


def test_unknown_function_is_info_only() -> None:
    findings = check_formula("FROBNICATE(x)")
    assert {f.code for f in findings} == {"UNKNOWN_FUNCTION"}
    assert all(f.severity == "INFO" for f in findings)


def test_known_function_not_flagged() -> None:
    assert check_formula("TIMESUM(Revenue, Start, End)") == []
