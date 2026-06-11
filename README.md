# anaplan-kit-mcp

**MCP server for Anaplan model builders — formula reference, cookbook recipes and blueprint
linting offline; live Anaplan API tools optional.** Python, stdio, MIT.

The knowledge tools work with **zero credentials and zero network**: the package bundles a
content snapshot of [anaplan-kit](https://github.com/palimkarakshay/anaplan-kit) (an
Anapedia-validated formula reference, real-world cookbook recipes, worked model blueprints and
a DISCO/naming conventions linter), so `pip install anaplan-kit-mcp` is fully self-contained.
Live tenant access is an opt-in extra built on
[anaplan-sdk](https://github.com/VinzenzKlass/anaplan-sdk).

## Why this exists

AI agents helping with Anaplan work mostly need *model-building knowledge* — what's the syntax
for `TIMESUM`? how do I structure a data hub? does this blueprint follow DISCO? — long before
they need tenant access. This server gives agents that layer offline, and (when you choose to
configure credentials) a small, honest set of live API tools for discovery and running
imports/exports/processes.

## Quickstart

```bash
# Claude Code
claude mcp add anaplan -- uvx anaplan-kit-mcp

# or run it directly (uv / pipx)
uvx anaplan-kit-mcp
pipx run anaplan-kit-mcp
```

Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "anaplan": {
      "command": "uvx",
      "args": ["anaplan-kit-mcp"]
    }
  }
}
```

Then ask your agent things like *"what's the syntax for TIMESUM?"*, *"find me a recipe for a
rolling forecast"*, or *"lint this module blueprint against DISCO conventions"*.

With live credentials (optional — see below):

```bash
pip install 'anaplan-kit-mcp[live]'
```

## Tools

### Offline knowledge (always available, no credentials, no network)

| Tool | What it does |
| --- | --- |
| `search_kit` | Ranked keyword search over the kit's docs, cookbook and blueprints. Optional `area` filter (e.g. `formulas`, `cookbook`, `time-and-forecasting`). |
| `read_kit_doc` | Read one kit document by repo-relative path (Markdown only, path-escape safe, truncation flagged). |
| `formula_reference` | Look up an Anaplan function (`CUMULATE`, `LOOKUP`, `TIMESUM`, …) in the Anapedia-validated reference → syntax + usage notes; unknown names return closest matches. |
| `list_recipes` | Index of the cookbook's real-world recipes: title, one-line description, area, level. |
| `lint_blueprint` | Lint blueprint Markdown tables against the kit's modeling conventions (DISCO prefixes, deliberate Summaries, banned functions, formula hygiene) → structured ERROR/WARN/INFO findings with stable codes. |

### Live Anaplan API (requires the `[live]` extra + env credentials)

| Tool | What it does |
| --- | --- |
| `anaplan_connection_status` | Report whether credentials/SDK are configured — never reveals values. |
| `anaplan_list_workspaces` | List workspaces the configured account can access. |
| `anaplan_list_models` | List models (tenant-wide, or narrowed to one workspace). |
| `anaplan_model_metadata` | One discovery call: a model's modules, lists, files, imports, exports, actions and processes (as anaplan-sdk exposes them). |
| `anaplan_run_action` | Run a generic action and wait for completion. |
| `anaplan_run_import` | Run an import action and wait for completion. |
| `anaplan_run_export` | Run an export action and wait for completion. |
| `anaplan_run_process` | Run a process (ordered group of actions) and wait for completion. |

## The honesty invariant (load-bearing)

**With no credentials configured, every live tool returns**

```json
{"mode": "offline", "error": "no Anaplan credentials configured"}
```

**without raising and without attempting any network I/O** — the SDK is not even imported on
that path. If `anaplan-sdk` isn't installed (you skipped the `[live]` extra), the same
structured offline response points at the extra. The server starts and serves all offline
tools with zero credentials and zero network; it never pretends it touched a tenant.

## Environment variables

| Variable | Purpose |
| --- | --- |
| `ANAPLAN_KIT_ROOT` | Optional path to an anaplan-kit checkout (or synced content snapshot). Without it the server discovers a nearby checkout, else uses the bundled snapshot. |
| `ANAPLAN_EMAIL` / `ANAPLAN_PASSWORD` | Basic auth for the live tools. |
| `ANAPLAN_CERT_PATH` / `ANAPLAN_PRIVATE_KEY_PATH` | Certificate auth (S/MIME cert + private key file paths; takes precedence over basic auth). |
| `ANAPLAN_PRIVATE_KEY_PASSWORD` | Optional passphrase for the private key. |
| `ANAPLAN_WORKSPACE_ID` / `ANAPLAN_MODEL_ID` | Default IDs so the run/metadata tools can omit them per call. |

Credentials are read from the environment only — never hardcoded, never logged, never echoed
back by any tool.

## Bundled content & syncing

The wheel ships a Markdown snapshot of anaplan-kit's `docs/`, `cookbook/` and `blueprints/`
under `anaplan_kit_mcp/_content/`, stamped with the source commit in `_content/KIT_COMMIT`.
To refresh it from a checkout (maintainers, before a release):

```bash
python tools/sync_kit_content.py --source /path/to/anaplan-kit
```

If you keep your own anaplan-kit checkout, point `ANAPLAN_KIT_ROOT` at it (or run the server
from inside/next to it) and the live checkout is used instead of the snapshot.

## Develop

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,live]"
ruff check . && ruff format --check .
pytest -q                      # all offline; anaplan-sdk is mocked at the client interface
python -m build                # wheel + sdist
```

## MCP registry metadata

This repo carries [`server.json`](server.json) (MCP registry schema, PyPI package
`anaplan-kit-mcp`, stdio transport) and [`smithery.yaml`](smithery.yaml)
(`uvx anaplan-kit-mcp`). The same metadata applies for Glama and similar catalogs:
stdio server, Python ≥ 3.10, package `anaplan-kit-mcp`, command `uvx anaplan-kit-mcp`.

## Relationship to other projects

- **[anaplan-kit](https://github.com/palimkarakshay/anaplan-kit)** (MIT, same author) — the
  content source. The docs/cookbook/blueprints this server searches, the formula reference it
  serves and the conventions linter it runs are anaplan-kit's; this repo packages them for any
  MCP client without needing the kit checkout. The kit also embeds its own copy of this server
  for in-repo use.
- **[anaplan-sdk](https://github.com/VinzenzKlass/anaplan-sdk)** by Vinzenz Klass (Apache-2.0)
  — the actively maintained Python SDK the live tools are built on (the `[live]` extra).
- **[larasrinath/anaplan-mcp](https://github.com/larasrinath/anaplan-mcp)** — a TypeScript MCP
  server focused on the live Anaplan API. If you only want tenant operations and prefer a
  Node stack, that's a good alternative; this server's differentiator is the offline
  model-building knowledge layer.

MIT © Akshay Palimkar. Not affiliated with or endorsed by Anaplan, Inc. "Anaplan" is a
trademark of Anaplan, Inc.; this is an independent open-source tool for people working with it.
