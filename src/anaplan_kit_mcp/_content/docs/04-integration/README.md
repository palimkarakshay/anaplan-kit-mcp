# Integration — Getting Data In and Out

> **Level:** L2 · **Area:** Integration · **PLANS:** Sustainable

Anaplan rarely lives alone. Actuals come from a GL or ERP, headcount comes from an HR
system, prices come from a pricing tool — and the plan you build often has to flow *back*
out to a warehouse or a report. This section is about moving data **into** and **out of**
Anaplan reliably, on a schedule, without hand-keying.

## The mental model

There are two completely separate questions, and beginners often confuse them:

1. **What** moves the data — the *action*. Inside Anaplan you define **imports**,
   **exports**, **deletes** and **processes**. These are reusable, named objects that live
   in the model.
2. **Who/what triggers it** — the *runner*. A user can click a button, or an external
   client can call the action: **Anaplan Connect** (a command-line tool),
   **CloudWorks** (cloud scheduling), or the **REST API** (your own code, like the
   [`tooling/`](../../tooling/) package in this kit).

So the pattern is always: *define the action once in the model, then choose how to run it.*

## The role of a Data Hub

The single most important integration pattern in Anaplan is the **Data Hub** — one
dedicated model whose only job is to receive, clean and store shared data, then feed it to
the "spoke" planning models via model-to-model imports.

Why it matters:

- **One load, many consumers.** You import the GL once into the hub; five planning models
  pull from it. You never import the same file into five models. *(Necessary, Sustainable)*
- **One source of truth.** Everyone sees the same actuals, lists and hierarchies.
- **Smaller, safer spokes.** The hub holds the big transactional data; planning models
  stay lean.

A Data Hub is mostly **D (Data)** and **S (System)** modules in [DISCO](../03-methodology/disco.md)
terms. The cookbook has a full build recipe under `cookbook/data-and-imports/`.

## Map of these pages

| Page | What it covers |
| --- | --- |
| [imports-exports.md](imports-exports.md) | The core concepts: data vs structural imports, mapping, saved views, auto-create, pitfalls. |
| [actions-and-processes.md](actions-and-processes.md) | Action types, grouping them into processes, and how they get run. |
| [anaplan-connect.md](anaplan-connect.md) | The command-line integration client for scripted, scheduled loads. |
| [cloudworks.md](cloudworks.md) | Cloud-based scheduling and connections to AWS/Azure/BigQuery. |
| [rest-api.md](rest-api.md) | The REST API v2 — auth, resource hierarchy, chunked upload, running actions. |
| [ecosystem-and-tooling.md](ecosystem-and-tooling.md) | The wider ecosystem: all official APIs, open-source clients, MCP/AI tooling, Classic vs Polaris. |

> **AI agents:** the kit also ships an **MCP server** (`anaplan-kit-mcp`, see
> [`tooling/`](../../tooling/README.md#mcp-server-anaplan-kit-mcp)) exposing the formula
> reference, cookbook, blueprint linter *and* this REST API client as tools for any
> MCP-capable agent — a fourth "runner". Without credentials it answers honestly in offline
> mode; with the `ANAPLAN_*` env vars it drives the same API described in
> [rest-api.md](rest-api.md).

## Where to start

If you are new, read [imports-exports.md](imports-exports.md) and
[actions-and-processes.md](actions-and-processes.md) first — they are Level 1/2 and you'll
use them in every model. The three "runner" pages (Anaplan Connect, CloudWorks, REST API)
are Level 3 architecture topics you reach once loads need to be automated.

**Related:** [Methodology — DISCO](../03-methodology/disco.md) ·
[Performance](../07-performance/) · [Python tooling](../../tooling/) ·
[Learning Path](../../LEARNING-PATH.md)
