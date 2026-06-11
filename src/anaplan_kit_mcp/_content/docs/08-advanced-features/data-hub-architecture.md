# Data Hub Architecture — Hub-and-Spoke

> **Level:** L3 · **Area:** Advanced Features · **PLANS:** Sustainable, Necessary, Logical · **DISCO:** Data / System

A **Data Hub** is a dedicated Anaplan model whose *only* job is to receive, clean, and master shared
data — lists, attributes, actuals, transactions — and then **publish** it to the planning models
that actually do the planning. Those planning models are the **spokes**. One hub, many spokes:
**hub-and-spoke**.

This is the single most important architectural pattern in Anaplan, and it is the thing that most
separates a model that survives contact with a real client estate from one that quietly rots. If
you read one page in this section, read this one.

## Why a central Data Hub at all

Picture three teams — FP&A, Sales, Supply Chain — each with their own planning model. Each one
needs the same things: the GL actuals, the product master, the cost-centre hierarchy, the FX rates.
Without a hub, each team imports the same files into their own model:

```
GL feed ─┬─► FP&A model      (imports + cleans the file)
         ├─► Sales model     (imports + cleans the file, differently)
         └─► Supply model    (imports + cleans the file, differently again)
```

The result is predictable and painful: three import routines to maintain, three slightly different
cleaning rules, three copies of the product list drifting apart, and numbers that **never tie**
across models. Every new source or new spoke multiplies the mess.

A Data Hub collapses all of that into one place:

```
GL feed ──► [ DATA HUB ]  ──► FP&A model
HR feed ──►   masters &   ──► Sales model
Product ──►   landing     ──► Supply model
master       + clean
```

The hub imports each source **once**, cleans it **once**, masters each list **once**, and every
spoke pulls from the hub. This is [PLANS](../03-methodology/plans-standard.md) made architectural:

- **Sustainable** — one import routine, one place each list is mastered. Add a fourth spoke and you
  wire it to the hub, not to the source files all over again.
- **Necessary** — a row of Actuals is stored and validated *once*, not N times.
- **Logical** — data flows in one clear, traceable direction with no circular dependencies.

## The cardinal rule: one-way data flow

> **Data flows hub → spoke. Never spoke → hub.**

The hub is the upstream source of truth. Spokes **read** from it; they never write back to it. A
spoke that writes to the hub creates a two-way flow — a circular dependency between models — which
is an ALM and reconciliation nightmare and breaks the "single source of truth" promise entirely.

If a spoke produces something another model needs (e.g. a finished forecast that Supply Chain wants
to consume), that is a **separate, deliberate** model-to-model flow — and even then you think hard
about whether it belongs in the hub or in a purpose-built "publishing" model. The default and the
discipline is: **hub down to spokes, full stop.**

## What lives in the hub (and what does not)

A Data Hub is almost entirely **D** (Data) and **S** (System) modules — see
[DISCO](../03-methodology/disco.md). It holds **no planning logic**.

| In the hub | Not in the hub |
| --- | --- |
| Master lists & hierarchies (Entity, Account, Product…) | Driver assumptions planners type in |
| Landing modules — raw, faithful copies of source feeds | Revenue = Volume × Price style calculations |
| SYS attribute & mapping modules (account type, sign flip, hierarchy properties) | Output/report modules shaped for dashboards |
| Light "clean once" steps (apply sign convention, standardise codes) | Anything a planner edits |

### SYS lists and master data live in the hub

The lists and their attributes are **mastered** in the hub. The product master, the cost-centre
tree, the account structure — these are created and maintained in the hub, then **imported into the
spokes** as their list members. A spoke does not maintain its own copy of `Product`; it receives
`Product` from the hub. Master each list in **exactly one place**, and that place is the hub. *(This
is the structural heart of Sustainable.)*

The hub's **System** modules carry the attributes every spoke needs — `Account Type`, `Sign Flip?`,
`P&L Group`, hierarchy roll-up properties — so the cleaning and classification logic is built once
and inherited by all.

## Concatenated text keys for matching

Source systems rarely hand you a single tidy ID. A GL row might be identified by *Entity, Account,
Cost Centre and Period* together. To import that row reliably — and to look it up later — you build
a **concatenated text key**: a single text line item that glues the component codes together with a
delimiter.

```
// SYS key in the landing / staging area
Entity Code & "|" & Account Code & "|" & Cost Centre Code
```

Why this matters in a hub:

- **Imports match on the key.** A unique text key per row lets an import map source rows to list
  items deterministically — and lets you build/auto-create numbered-list members for transactional
  data.
- **`FINDITEM` / `LOOKUP` resolve the key back to a list item** so the value lands on the right
  intersection. (See [`docs/02-formulas/lookup-and-mapping.md`](../02-formulas/lookup-and-mapping.md).)
- **Pick a delimiter that can't appear in the data** (a pipe `|` is common) so codes never collide.
- Keep keys **stable** — if a source code changes, the key changes, and matching breaks. This is why
  keys are built in **SYS** modules where you can see and govern them.

> Concatenated keys are how the hub turns messy, multi-column source rows into clean references that
> spokes can trust. They are a workhorse of the pattern — see the cookbook recipe linked below.

## How spokes import from the hub

Spokes pull from the hub by **model-to-model import**, almost always from a **saved view** in the
hub, and usually wrapped in a **process** so the steps run in the right order.

1. **The hub publishes a saved view.** You build an Output/publish view (e.g. `OUT01 Actuals
   (publish view)`) shaped to contain exactly the cells a spoke needs — no more. Saved views are
   the contract between hub and spoke.
2. **The spoke defines an import action** that reads that hub view. Because both models live in the
   same workspace/tenant, Anaplan supports **model-to-model imports** directly — no files, no
   external tooling required.
3. **Order the loads with a process.** List/member updates must run *before* the data import that
   references them, so wrap the actions in a [process](../04-integration/actions-and-processes.md).
4. **Schedule or trigger it.** A user clicks a button, or you automate it via
   [CloudWorks](../04-integration/cloudworks.md), [Anaplan Connect](../04-integration/anaplan-connect.md),
   or the [REST API](../04-integration/rest-api.md) / the [`tooling/`](../../tooling/) package in this kit.

> **Why a saved view, not the raw module?** A saved view is a stable contract. If you add a line
> item to the underlying hub module, the spoke's import doesn't break — it still reads the columns
> the view exposes. Importing straight from a raw module couples the spoke to the hub's internals.

## Governance benefits

The hub-and-spoke pattern is as much about **control** as about tidiness:

- **Single source of truth.** One place to ask "what are the actuals?" — and one place to fix them
  if they're wrong.
- **One audit point.** Validation, error handling, and dump-file checks happen at the hub, once,
  instead of being re-implemented (badly) in every spoke. See
  [`cookbook/data-and-imports/handle-import-errors-and-dump-files.md`](../../cookbook/data-and-imports/handle-import-errors-and-dump-files.md).
- **Smaller, faster spokes.** A spoke holds only what it plans with — not the full transaction
  history — so its cell count stays low. The hub absorbs the bulk and uses
  [Time Ranges](../07-performance/time-ranges.md) to keep even *its* landing modules in check.
- **Clean ALM boundaries.** Each model is deployed and versioned independently. Because data flows
  one way, you can change a spoke without touching the hub. See [ALM](../06-security-alm/alm.md).
- **Security stays simple.** Source-system access and broad data live in the hub; spokes expose only
  the slice each audience plans with.

## DISCO & PLANS at a glance

| Concern | How the hub satisfies it |
| --- | --- |
| **Sustainable (PLANS)** | One import, one master per list; new spokes wire to the hub, not the sources. |
| **Necessary (PLANS)** | Each fact stored and cleaned once, not per model. |
| **Logical (PLANS)** | Strictly one-directional flow; no circular model dependencies. |
| **DISCO** | The hub is Data + System only — no Inputs, no Calculations-with-business-logic, no Outputs-for-planners. |
| **DISCO of the spoke** | The spoke lands hub data in its own **D** modules, then does **I/S/C/O** on top. |

## Related

- Hands-on build: [`cookbook/data-and-imports/build-a-data-hub.md`](../../cookbook/data-and-imports/build-a-data-hub.md)
- [`docs/04-integration/`](../04-integration/) — imports/exports, actions & processes, CloudWorks, REST API (how the hub physically moves data)
- [`docs/04-integration/actions-and-processes.md`](../04-integration/actions-and-processes.md) · [`imports-exports.md`](../04-integration/imports-exports.md)
- [`docs/03-methodology/disco.md`](../03-methodology/disco.md) · [`plans-standard.md`](../03-methodology/plans-standard.md)
- [`docs/07-performance/time-ranges.md`](../07-performance/time-ranges.md) · [`docs/06-security-alm/alm.md`](../06-security-alm/alm.md)
- Related recipes: [incremental-delta-import](../../cookbook/data-and-imports/incremental-delta-import.md) · [auto-create-list-members](../../cookbook/data-and-imports/auto-create-list-members.md)

> Source: Anaplan Data Hub / hub-and-spoke best-practice materials (Anapedia & Anaplan Community, `help.anaplan.com` / `community.anaplan.com`). Confirm current specifics in Anapedia. See [`SOURCES.md`](../../SOURCES.md).
