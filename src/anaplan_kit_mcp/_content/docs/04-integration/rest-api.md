# Anaplan REST API v2

> **Level:** L3 · **Area:** Integration · **PLANS:** Sustainable

This page documents the **REST API v2 (Bulk API)** — the *Integration API v2.0*. It is the
programmatic way to do everything the runners do — upload files, run
[actions and processes](actions-and-processes.md), download exports — from **your own code**.
[Anaplan Connect](anaplan-connect.md) and [CloudWorks](cloudworks.md) both call this API under
the hood. This kit's [`tooling/`](../../tooling/) package is a Python client for exactly this
API, so read this page conceptually and see the tooling for runnable code.

> **Bulk vs Transactional.** This is the **Bulk API**: batch file loads and exports, run as
> asynchronous tasks — the right tool for moving *volumes* of data. Anaplan also exposes a
> separate **Transactional API** for **cell-level, real-time reads and writes** (read/update
> a handful of cells in a view, list members, model metadata) without the file-and-task
> machinery. Pick **per use case**: bulk loads → this API; small real-time reads/writes →
> Transactional. See [platform strategy → which API?](../10-field-guide/platform-strategy.md)
> for the decision framing.

> The base URLs you'll see are `https://auth.anaplan.com` (login) and
> `https://api.anaplan.com/2/0/...` (everything else). Confirm current endpoints in the
> Anapedia *Integration API v2.0* reference — they evolve.

## Authentication

Every call needs a short-lived **auth token** (sent as `AnaplanAuthToken`, **not** `Bearer`).
You obtain it one of two ways:

| Method | How | Use when |
| --- | --- | --- |
| **Basic auth → token** | POST username/password to the auth endpoint, receive a token | Quick start, scripts, learning |
| **Certificate** | Authenticate with an Anaplan-registered CA certificate, receive a token | Production — no password to leak or rotate |

The flow is the same afterwards:

1. Authenticate → receive an **auth token** (valid ~30 minutes).
2. Send the token as `Authorization: AnaplanAuthToken <token>` on every API call.
3. **Refresh** the token before it expires for long-running jobs.

A concrete example (basic auth):

```
POST https://auth.anaplan.com/token/authenticate
Authorization: Basic base64(email:password)
→ 200 { "tokenInfo": { "tokenValue": "<token>", "expiresAt": 1700000000000 } }
```

Then on every Bulk API call to `https://api.anaplan.com/2/0/...`:

```
GET https://api.anaplan.com/2/0/workspaces
Authorization: AnaplanAuthToken <token>
```

> **The header scheme is `AnaplanAuthToken`, not `Bearer`** — a common copy-paste mistake.
> This kit's [`tooling/anaplan_kit/auth.py`](../../tooling/anaplan_kit/auth.py) sends exactly
> this header.

> **Prefer certificate auth in production.** *(Sustainable + security.)* See
> [security & ALM](../06-security-alm/README.md) for the wider access model.

## The resource hierarchy

The API mirrors how Anaplan is organised — you drill down by ID at each level:

```
/workspaces/{workspaceId}
  /models/{modelId}
    /files/{fileId}          ← upload/download targets for imports & exports
    /imports/{importId}      ← import actions
    /exports/{exportId}      ← export actions
    /actions/{actionId}      ← other actions (e.g. delete from list)
    /processes/{processId}   ← ordered groups of actions
```

A typical script first **lists** workspaces, then models, then the imports/exports/processes
inside a model, to discover the IDs it needs.

## Uploading a file in chunks

Files are uploaded in **chunks**, not in one piece — this is how Anaplan handles large
loads reliably:

1. Tell Anaplan how many chunks the file has (or set the chunk size).
2. `PUT` each chunk to
   `/workspaces/{workspaceId}/models/{modelId}/files/{fileId}/chunks/{chunkId}`,
   incrementing the chunk ID per part.
3. Mark the upload **complete**.

The file ID corresponds to the source file an [import action](imports-exports.md) expects —
you're replacing the action's source with fresh content of the same layout.

## Running an action and polling the task

Running an action is **asynchronous**: you start a *task*, then poll it until it finishes.

1. `POST` to the action's `/tasks` endpoint to start it — get back a **taskId**.
2. `GET` `/imports/{importId}/tasks/{taskId}` (or the matching path for exports / processes /
   actions) to read **task status**.
3. Repeat the GET on an interval until the state is **complete** (or failed).
4. For imports, the result includes **success / ignored / failed** row counts and, on
   failures, a **dump file** describing the bad rows — always check it.

```
POST   /imports/{importId}/tasks                 → { taskId }
GET    /imports/{importId}/tasks/{taskId}         → { taskState, progress, currentStep, result }
(poll until taskState == COMPLETE; then check result.successful and fetch the failure dump)
```

The task state isn't just `IN_PROGRESS` / `COMPLETE`: while running, the task reports
**`progress`** (often a fraction 0–1) and a **`currentStep`** label you can show or log. When
`taskState` reaches `COMPLETE`, that only means the task *finished* — you must still check the
**`result.successful`** flag, because a task can complete *unsuccessfully* (e.g. all rows
rejected). Treat `successful == false` as a failure and read the dump.

A **process** works the same way via `/processes/{processId}/tasks`, and its result rolls up
each contained action's outcome.

## Downloading an export

Exports are also **chunked**, in reverse:

1. Run the export action (start a task, poll to completion — as above).
2. Read the export **file**'s chunk count from `/files/{fileId}`.
3. `GET` each chunk and concatenate them into the output file.

## How this maps to the rest of the kit

| API concept | Elsewhere in the kit |
| --- | --- |
| imports / exports | [imports-exports.md](imports-exports.md) |
| actions / processes / tasks | [actions-and-processes.md](actions-and-processes.md) |
| the API wrapped in Python | [`tooling/`](../../tooling/) — auth, chunked upload, run-and-poll, export download |
| auth & certificates | [security & ALM](../06-security-alm/README.md) |

**Related:** [Actions & Processes](actions-and-processes.md) ·
[Anaplan Connect](anaplan-connect.md) · [CloudWorks](cloudworks.md) ·
[Imports & Exports](imports-exports.md) · [Python tooling](../../tooling/) ·
[Integration overview](README.md)

> Source: Anaplan Integration API v2.0 reference (`help.anaplan.com`, Data Integrations /
> Integration API v2.0). See [`SOURCES.md`](../../SOURCES.md).
