# anaplan-kit-mcp

**Public MIT** standalone Python MCP server (stdio, FastMCP) for Anaplan model builders:
5 offline knowledge tools over bundled anaplan-kit content (search, doc read, formula
reference, recipes, blueprint lint) + 8 live Anaplan API tools on `anaplan-sdk` (`[live]`
extra). Lumivara product line: **Learn**. GitHub `palimkarakshay/anaplan-kit-mcp`;
PyPI `anaplan-kit-mcp`. The Anaplan analog of `abap-mcp`.

## Package manager: pip + venv (NOT uv) — Python 3.10+ (CI 3.11), hatchling build

## Commands (authoritative)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,live]"
ruff check . && ruff format --check .   # lint gates
pytest -q                               # all OFFLINE; anaplan-sdk mocked at client interface
python -m build                         # wheel + sdist (publish is owner-run via twine/uv)
python tools/sync_kit_content.py        # refresh bundled snapshot from ../anaplan-kit
.venv/bin/anaplan-kit-mcp               # run the stdio server
```

## Layout

- `src/anaplan_kit_mcp/` — `server.py` (13 tools + main), `kitindex.py` (search/read/formula/
  recipes + root resolution), `live.py` (anaplan-sdk gate/wrappers), `modeling/` (ported
  blueprint parser + DISCO/formula linter), `_content/` (bundled docs/cookbook/blueprints
  snapshot + `KIT_COMMIT` stamp).
- `tests/` — offline suite; conftest pins content to the bundled snapshot + scrubs ANAPLAN_* env.
- `tools/sync_kit_content.py` — dev-only content sync; `server.json` + `smithery.yaml` registry manifests.

## Gotchas / invariants

- **Offline honesty (load-bearing):** no credentials → every live tool returns
  `{"mode": "offline", "error": "no Anaplan credentials configured"}` — no raise, no network,
  no SDK import. SDK missing → same shape mentioning the `[live]` extra. Never fake tenant access.
- Source of truth for tool logic is anaplan-kit's embedded server (`tooling/anaplan_kit/
  mcp_server.py`) — this repo is the standalone port; do NOT edit anaplan-kit from here.
- Content root resolution: `ANAPLAN_KIT_ROOT` → discovered checkout → bundled `_content/`.
  Re-run the sync script (and commit) before any release so the snapshot stays current.
- Creds via env only (`ANAPLAN_EMAIL/PASSWORD` or `ANAPLAN_CERT_PATH/ANAPLAN_PRIVATE_KEY_PATH`);
  never hardcode, never log, never echo values (connection_status returns booleans only).
- stdout is the JSON-RPC channel — anything human-facing goes to stderr.
- No deploy target — ships as a PyPI package (owner publishes; no token on this box).
