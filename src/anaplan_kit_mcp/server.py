"""MCP server exposing Anaplan model-building knowledge and (optional) live API tools.

Runs over **stdio** via the ``anaplan-kit-mcp`` console script. Two tool families:

* **Offline knowledge tools** — search/read the anaplan-kit Markdown (docs,
  cookbook, blueprints), look up the formula reference, list cookbook recipes,
  and lint blueprint tables with the kit's real conventions linter. Pure local
  logic over the bundled content snapshot (or a checkout); always available.
* **Live Anaplan API tools** — built on `anaplan-sdk
  <https://github.com/VinzenzKlass/anaplan-sdk>`_ (the ``[live]`` extra).
  Credentials come from environment variables only: ``ANAPLAN_EMAIL`` /
  ``ANAPLAN_PASSWORD`` (basic) or ``ANAPLAN_CERT_PATH`` /
  ``ANAPLAN_PRIVATE_KEY_PATH`` (certificate), plus optional
  ``ANAPLAN_WORKSPACE_ID`` / ``ANAPLAN_MODEL_ID`` defaults.

**Offline honesty invariant (load-bearing, inherited from anaplan-kit):** when
credentials are not configured, every live tool returns
``{"mode": "offline", "error": "no Anaplan credentials configured"}`` —
without raising and without attempting any network I/O. The same structured
response (mentioning the ``[live]`` extra) is returned when anaplan-sdk is not
installed. Nothing in this module performs network access at import time.

The tool surface is ported from anaplan-kit's embedded MCP server
(``tooling/anaplan_kit/mcp_server.py``, MIT, same author).
"""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from . import kitindex, live
from .kitindex import KitRootNotFoundError
from .modeling.blueprint import parse_blueprint
from .modeling.lint import lint_module

mcp = FastMCP("anaplan-kit-mcp")


# --- helpers -----------------------------------------------------------------


def _kit_root_error(exc: KitRootNotFoundError) -> dict[str, Any]:
    return {"error": str(exc), "hint": f"set {kitindex.ENV_ROOT} to an anaplan-kit checkout"}


# --- offline knowledge tools ---------------------------------------------------


@mcp.tool()
def search_kit(query: str, area: str | None = None, limit: int = 8) -> dict[str, Any]:
    """Search the Anaplan kit's docs, cookbook and blueprints.

    Ranked keyword search (offline, no embeddings). Use `area` to narrow by
    path, e.g. "formulas", "cookbook", "methodology", "time-and-forecasting".
    Returns {path, title, heading, snippet, score} per hit — follow up with
    read_kit_doc(path) for the full document.
    """
    try:
        root = kitindex.find_kit_root()
    except KitRootNotFoundError as exc:
        return _kit_root_error(exc)
    results = kitindex.search(root, query, area=area, limit=limit)
    return {"query": query, "area": area, "results": results}


@mcp.tool()
def read_kit_doc(path: str, max_chars: int = 20000) -> dict[str, Any]:
    """Read one kit document by repo-relative path (e.g. "cookbook/README.md").

    Only Markdown files inside the kit content can be read; long documents are
    truncated at max_chars (the response says so via "truncated": true).
    """
    try:
        root = kitindex.find_kit_root()
    except KitRootNotFoundError as exc:
        return _kit_root_error(exc)
    try:
        return kitindex.read_doc(root, path, max_chars=max_chars)
    except (ValueError, FileNotFoundError) as exc:
        return {"error": str(exc), "path": path}


@mcp.tool()
def formula_reference(function_name: str) -> dict[str, Any]:
    """Look up an Anaplan function (e.g. CUMULATE, LOOKUP, TIMESUM) in the kit's
    Anapedia-validated formula reference.

    Returns syntax, usage notes and the source doc path. If the function is
    unknown, returns the closest-matching function names instead.
    """
    try:
        root = kitindex.find_kit_root()
    except KitRootNotFoundError as exc:
        return _kit_root_error(exc)
    return kitindex.formula_lookup(root, function_name)


@mcp.tool()
def list_recipes(area: str | None = None) -> dict[str, Any]:
    """List the kit's cookbook recipes: title, one-line description, path, level.

    Optionally filter by area (e.g. "time-and-forecasting", "Data & Imports",
    "security"). Recipes are ready-to-use blueprints for real modeling tasks.
    """
    try:
        root = kitindex.find_kit_root()
    except KitRootNotFoundError as exc:
        return _kit_root_error(exc)
    recipes = kitindex.list_recipes(root, area=area)
    return {"area": area, "count": len(recipes), "recipes": recipes}


@mcp.tool()
def lint_blueprint(content: str) -> dict[str, Any]:
    """Lint Anaplan blueprint Markdown against the kit's modeling conventions.

    Parses every canonical "| Line Item | Format | Summary | Applies To |
    Formula |" table in the text and runs the kit's real linter (DISCO naming,
    summaries, banned functions, formula hygiene). Returns structured findings
    with severity ERROR/WARN/INFO and stable codes.
    """
    modules = parse_blueprint(content or "")
    findings: list[dict[str, Any]] = []
    counts = {"ERROR": 0, "WARN": 0, "INFO": 0}
    for module in modules:
        for finding in lint_module(module):
            counts[finding.severity] += 1
            findings.append(
                {
                    "severity": finding.severity,
                    "code": finding.code,
                    "message": finding.message,
                    "location": finding.location,
                }
            )
    return {
        "modules_parsed": len(modules),
        "module_names": [m.name or "<unnamed>" for m in modules],
        "findings": findings,
        "counts": counts,
        "ok": counts["ERROR"] == 0,
    }


# --- live Anaplan API tools ----------------------------------------------------


@mcp.tool()
def anaplan_connection_status() -> dict[str, Any]:
    """Report whether live Anaplan credentials are configured (never reveals values).

    mode "live" means credentials (basic or certificate) are set AND
    anaplan-sdk is installed; "offline" means live tools will refuse to run.
    Also reports which ANAPLAN_* environment variables are configured.
    """
    return live.connection_status()


@mcp.tool()
def anaplan_list_workspaces() -> dict[str, Any]:
    """List Anaplan workspaces the configured account can access (live API)."""
    client, err = live.make_client()
    if err is not None:
        return err
    try:
        return {"mode": "live", "workspaces": live.dump(client.get_workspaces())}
    except Exception as exc:
        return live.live_error(exc)


@mcp.tool()
def anaplan_list_models(workspace_id: str | None = None) -> dict[str, Any]:
    """List Anaplan models the configured account can access (live API).

    workspace_id (defaulting to ANAPLAN_WORKSPACE_ID) narrows the listing to
    one workspace; without it, every model the account can see is returned.
    """
    workspace_id, _ = live.resolved_ids(workspace_id)
    client, err = live.make_client(workspace_id=workspace_id)
    if err is not None:
        return err
    try:
        if workspace_id:
            models = client.get_models(only_in_workspace=workspace_id)
        else:
            models = client.get_models()
        return {"mode": "live", "workspace_id": workspace_id, "models": live.dump(models)}
    except Exception as exc:
        return live.live_error(exc)


@mcp.tool()
def anaplan_model_metadata(
    model_id: str | None = None, workspace_id: str | None = None
) -> dict[str, Any]:
    """List a model's modules, lists, files, imports, exports, actions and processes (live API).

    IDs default to ANAPLAN_WORKSPACE_ID / ANAPLAN_MODEL_ID. This is the
    discovery call to find the IDs that anaplan_run_* tools need.
    """
    workspace_id, model_id = live.resolved_ids(workspace_id, model_id)
    client, err = live.make_client(workspace_id=workspace_id, model_id=model_id)
    if err is not None:
        return err
    if not workspace_id:
        return live.missing_id_error("workspace_id", live.ENV_WORKSPACE)
    if not model_id:
        return live.missing_id_error("model_id", live.ENV_MODEL)
    result: dict[str, Any] = {"mode": "live", "workspace_id": workspace_id, "model_id": model_id}
    try:
        result["files"] = live.dump(client.get_files())
        result["imports"] = live.dump(client.get_imports())
        result["exports"] = live.dump(client.get_exports())
        result["actions"] = live.dump(client.get_actions())
        result["processes"] = live.dump(client.get_processes())
    except Exception as exc:
        return live.live_error(exc)
    try:
        transactional = client.tr
        result["modules"] = live.dump(transactional.get_modules())
        result["lists"] = live.dump(transactional.get_lists())
    except Exception as exc:  # transactional API may be unavailable for this model/role
        result["modules"] = None
        result["lists"] = None
        result["transactional_error"] = f"{type(exc).__name__}: {exc}"
    return result


def _run_live_task(
    resource: str,
    resource_id: str,
    workspace_id: str | None,
    model_id: str | None,
) -> dict[str, Any]:
    """Shared run-and-wait path for actions/imports/exports/processes."""
    workspace_id, model_id = live.resolved_ids(workspace_id, model_id)
    client, err = live.make_client(workspace_id=workspace_id, model_id=model_id)
    if err is not None:
        return err
    if not workspace_id:
        return live.missing_id_error("workspace_id", live.ENV_WORKSPACE)
    if not model_id:
        return live.missing_id_error("model_id", live.ENV_MODEL)
    try:
        action_id = int(str(resource_id).strip())
    except ValueError:
        return {
            "mode": "live",
            "error": f"{resource} id must be the numeric Anaplan ID, got {resource_id!r}",
        }
    try:
        task = client.run_action(action_id)
    except Exception as exc:
        return live.live_error(exc)
    return {
        "mode": "live",
        "workspace_id": workspace_id,
        "model_id": model_id,
        "resource": resource,
        "resource_id": str(resource_id),
        "task": live.dump_one(task),
    }


@mcp.tool()
def anaplan_run_action(
    action_id: str, workspace_id: str | None = None, model_id: str | None = None
) -> dict[str, Any]:
    """Run a generic Anaplan action (e.g. delete-from-list) and wait for it (live API).

    IDs default to ANAPLAN_WORKSPACE_ID / ANAPLAN_MODEL_ID.
    """
    return _run_live_task("action", action_id, workspace_id, model_id)


@mcp.tool()
def anaplan_run_import(
    import_id: str, workspace_id: str | None = None, model_id: str | None = None
) -> dict[str, Any]:
    """Run an Anaplan import action and wait for completion (live API).

    The import's source file must already hold the data to load.
    """
    return _run_live_task("import", import_id, workspace_id, model_id)


@mcp.tool()
def anaplan_run_export(
    export_id: str, workspace_id: str | None = None, model_id: str | None = None
) -> dict[str, Any]:
    """Run an Anaplan export action and wait for completion (live API).

    Produces the export file inside Anaplan; downloading it is a separate
    (file-transfer) step not exposed by this server.
    """
    return _run_live_task("export", export_id, workspace_id, model_id)


@mcp.tool()
def anaplan_run_process(
    process_id: str, workspace_id: str | None = None, model_id: str | None = None
) -> dict[str, Any]:
    """Run an Anaplan process (ordered group of actions) and wait for it (live API)."""
    return _run_live_task("process", process_id, workspace_id, model_id)


def main() -> None:
    """Entry point for the ``anaplan-kit-mcp`` console script (stdio transport)."""
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
