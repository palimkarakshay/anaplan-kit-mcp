"""Tests for the offline kit index: root resolution, search, doc reads, formulas, recipes.

Everything is pure local file reading over the bundled content snapshot — no
network, no tenant, no mocking needed. Ported/adapted from anaplan-kit's
``test_kitindex.py`` (MIT, same author).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from anaplan_kit_mcp import kitindex
from anaplan_kit_mcp.kitindex import KitRootNotFoundError

# --- root discovery ---------------------------------------------------------


def test_find_kit_root_from_env(bundled_root: Path) -> None:
    assert kitindex.find_kit_root() == bundled_root.resolve()


def test_find_kit_root_env_invalid(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv(kitindex.ENV_ROOT, str(tmp_path))
    with pytest.raises(KitRootNotFoundError):
        kitindex.find_kit_root()


def test_find_kit_root_env_accepts_checkout(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / "cookbook").mkdir()
    (tmp_path / "SOURCES.md").write_text("# sources\n")
    monkeypatch.setenv(kitindex.ENV_ROOT, str(tmp_path))
    assert kitindex.find_kit_root() == tmp_path.resolve()


def test_discover_checkout_finds_sibling(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    checkout = tmp_path / "anaplan-kit"
    (checkout / "cookbook").mkdir(parents=True)
    (checkout / "LEARNING-PATH.md").write_text("# path\n")
    workdir = tmp_path / "somewhere" / "deep"
    workdir.mkdir(parents=True)
    monkeypatch.chdir(workdir)
    assert kitindex._discover_checkout() == checkout


def test_find_kit_root_falls_back_to_bundled(
    monkeypatch: pytest.MonkeyPatch, bundled_root: Path
) -> None:
    monkeypatch.delenv(kitindex.ENV_ROOT, raising=False)
    monkeypatch.setattr(kitindex, "_discover_checkout", lambda: None)
    assert kitindex.find_kit_root() == bundled_root.resolve()


def test_find_kit_root_raises_when_nothing_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(kitindex.ENV_ROOT, raising=False)
    monkeypatch.setattr(kitindex, "_discover_checkout", lambda: None)
    monkeypatch.setattr(kitindex, "bundled_root", lambda: None)
    with pytest.raises(KitRootNotFoundError):
        kitindex.find_kit_root()


def test_bundled_snapshot_records_source_commit(bundled_root: Path) -> None:
    commit = kitindex.kit_commit(bundled_root)
    assert commit is not None
    assert re.fullmatch(r"[0-9a-f]{40}", commit)


def test_kit_commit_none_for_checkout(tmp_path: Path) -> None:
    assert kitindex.kit_commit(tmp_path) is None


# --- search -------------------------------------------------------------------


def test_search_finds_cumulate_in_formula_docs() -> None:
    results = kitindex.search(kitindex.find_kit_root(), "CUMULATE running total")
    assert results, "expected at least one hit"
    paths = [r["path"] for r in results]
    assert any("docs/02-formulas" in p for p in paths)
    top = results[0]
    assert set(top) == {"path", "title", "heading", "snippet", "score"}
    assert top["score"] >= results[-1]["score"]  # ranked, best first


def test_search_finds_data_hub_recipe() -> None:
    results = kitindex.search(kitindex.find_kit_root(), "data hub", limit=8)
    assert any("data-hub" in r["path"] or "data_hub" in r["path"] for r in results)


def test_search_area_filter_restricts_paths() -> None:
    results = kitindex.search(kitindex.find_kit_root(), "forecast", area="cookbook")
    assert results
    assert all(r["path"].startswith("cookbook/") for r in results)


def test_search_empty_query_returns_nothing() -> None:
    assert kitindex.search(kitindex.find_kit_root(), "   ") == []


def test_search_respects_limit() -> None:
    results = kitindex.search(kitindex.find_kit_root(), "module", limit=3)
    assert len(results) <= 3


# --- read_doc ------------------------------------------------------------------


def test_read_doc_returns_content() -> None:
    doc = kitindex.read_doc(kitindex.find_kit_root(), "cookbook/README.md")
    assert doc["path"] == "cookbook/README.md"
    assert "Cookbook" in doc["content"]
    assert doc["truncated"] is False


def test_read_doc_truncates() -> None:
    doc = kitindex.read_doc(kitindex.find_kit_root(), "cookbook/README.md", max_chars=50)
    assert len(doc["content"]) == 50
    assert doc["truncated"] is True
    assert doc["total_chars"] > 50


def test_read_doc_rejects_path_escape() -> None:
    root = kitindex.find_kit_root()
    with pytest.raises(ValueError):
        kitindex.read_doc(root, "../../../etc/passwd.md")
    with pytest.raises(ValueError):
        kitindex.read_doc(root, "docs/../../outside.md")


def test_read_doc_rejects_absolute_path() -> None:
    with pytest.raises(ValueError):
        kitindex.read_doc(kitindex.find_kit_root(), "/etc/passwd.md")


def test_read_doc_rejects_non_markdown() -> None:
    with pytest.raises(ValueError):
        kitindex.read_doc(kitindex.find_kit_root(), "KIT_COMMIT")


def test_read_doc_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        kitindex.read_doc(kitindex.find_kit_root(), "docs/does-not-exist.md")


# --- formula reference -----------------------------------------------------------


def test_formula_lookup_finds_cumulate() -> None:
    result = kitindex.formula_lookup(kitindex.find_kit_root(), "CUMULATE")
    assert result["found"] is True
    match = result["matches"][0]
    assert match["path"].startswith("docs/02-formulas/")
    assert "CUMULATE" in (match["syntax"] or "")
    assert match["content"]


def test_formula_lookup_is_case_insensitive_and_tolerates_parens() -> None:
    assert kitindex.formula_lookup(kitindex.find_kit_root(), "cumulate()")["found"] is True


def test_formula_lookup_unknown_returns_closest() -> None:
    result = kitindex.formula_lookup(kitindex.find_kit_root(), "CUMULAT")
    assert result["found"] is False
    assert "CUMULATE" in result["closest"]


def test_formula_lookup_handles_combined_headings() -> None:
    # "### START / END" defines two functions in one heading.
    result = kitindex.formula_lookup(kitindex.find_kit_root(), "END")
    assert result["found"] is True


# --- cookbook recipes -------------------------------------------------------------


def test_list_recipes_returns_every_recipe_with_fields() -> None:
    recipes = kitindex.list_recipes(kitindex.find_kit_root())
    assert len(recipes) > 10
    for recipe in recipes:
        assert recipe["path"].startswith("cookbook/")
        assert recipe["title"]
        assert recipe["description"]


def test_list_recipes_area_filter() -> None:
    recipes = kitindex.list_recipes(kitindex.find_kit_root(), area="time-and-forecasting")
    assert recipes
    assert all(r["path"].startswith("cookbook/time-and-forecasting/") for r in recipes)
