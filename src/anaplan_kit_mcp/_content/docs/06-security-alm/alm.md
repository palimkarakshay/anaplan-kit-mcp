# ALM — Application Lifecycle Management

> **Level:** L3 · **Area:** ALM · **PLANS:** Sustainable, Auditable

**Application Lifecycle Management (ALM)** is how you change a *live* Anaplan model safely.
The problem it solves: planners are typing real numbers into PROD every day, but you still
need to add line items, fix formulas and ship new modules — **without overwriting their
data**. ALM lets you make structural changes in a separate **development** model and
**synchronize** just the structure into production.

## Development mode vs deployed mode

A model is in one of two modes:

| Mode | What it allows | Where it's used |
| --- | --- | --- |
| **Standard (development)** | Full structural editing — add/change lists, modules, line items, views | The **DEV** model where builders work |
| **Deployed** | Structural editing **blocked**; only data changes | **PROD** (and usually TEST) — protects the live model |

**Deployed mode** is the lock that makes ALM safe: nobody can accidentally alter PROD's
structure, so the only way structure changes is a controlled **synchronization** from
development. Production data is recommended to live only in deployed-mode models.

> ⚠️ **The golden rule: never take a production model out of deployed mode.** Doing so breaks
> ALM compatibility and you may lose the ability to synchronize future changes cleanly. If
> you need a structural change, make it in DEV and sync it in.

## The promotion path: DEV → TEST → PROD

```
   DEV  (Standard mode)        TEST (Deployed)            PROD (Deployed)
   build & change structure  →  validate the sync       →  live planning
        |  revision tag             |  data here is test       |  real planner data
        +------ synchronize --------+------ synchronize --------+
                 (structure only flows DEV → downstream)
```

- **DEV** — you build. Standard mode, structural changes allowed.
- **TEST** — a deployed copy where you apply the change and **verify** it before it reaches
  planners.
- **PROD** — deployed; planners work here. Structure only ever arrives via synchronization.

Structure flows **one way**, DEV → TEST → PROD. Data does **not** flow with it.

## Revisions and revision tags

You don't sync "the model" — you sync to a **revision**:

- A **revision tag** is a named **snapshot of a model's structure** at a point in time,
  created by a workspace admin in the **development** model.
- To promote, you **synchronize** a target model up to a chosen revision tag of the source.
- Tag at meaningful milestones ("Sprint 7 — added Workforce module") so you have clean,
  comparable points to promote and roll forward.

> Add revision tags **only to development models**. You can't tag a deployed model, and
> tagging production risks incompatibility. Keep DEV slightly ahead and tag there.

## Synchronization — and what it does / doesn't move

**Synchronize** compares the target to a source revision and applies the **structural**
differences. The crucial split:

| Category | Examples | Moves on sync? |
| --- | --- | --- |
| **Structural** | Lists' *structure*, modules, line items, formulas, views, actions, roles, page layouts | **Yes** — this is what ALM promotes |
| **Production data** | Numbers planners typed, imported actuals, list *members* of production lists | **No** — stays in the target; not overwritten |

So ALM **moves the model's design** and **leaves the planners' data alone**. That's the whole
point: ship a new calculation to PROD without wiping this quarter's forecast.

> **Production lists / production data** are flagged so their *contents* are treated as data
> (owned by the target), even though the list's *existence* is structure. This lets you add a
> list in DEV and let PROD keep its own members.

> ⚠️ **ALM moves *structure*, not *people*.** A **role's definition** (what the role can do) is
> structure and syncs — but the **users themselves and their role assignments do *not* sync**.
> Add a planner to PROD, or change who is in which role, **in the production model directly**;
> don't expect a sync to carry it across. This catches almost every beginner. See
> [Roles & Selective Access](roles-and-selective-access.md).

## Why use ALM from the start

- **You can't bolt it on cleanly later.** Set up the DEV/PROD split and deploy PROD *before*
  go-live; retrofitting once planners are entering data is painful.
- **Safe iteration.** Build and break things in DEV without touching live plans.
- **Auditable releases.** Revision tags give you a history of what shipped, when.
- **Sustainable.** Structural change becomes a routine, repeatable promotion — not a risky
  hand-edit in the live model. *(Sustainable, Auditable.)*

## Good practice

- Decide the **DEV → TEST → PROD** topology on day one; put PROD in **deployed mode**.
- **Tag in DEV** at each release; keep tags meaningful.
- **Test the sync in TEST** before PROD.
- **Never** take PROD out of deployed mode.
- Keep DEV and PROD **compatible** — sync regularly rather than letting them drift far apart.

**Related:** [Security & ALM overview](README.md) ·
[Roles & Selective Access](roles-and-selective-access.md) ·
[Integration / Data Hubs](../04-integration/README.md) ·
[PLANS — Sustainable](../03-methodology/plans-standard.md) ·
[Learning Path — Level 3](../../LEARNING-PATH.md)

> Source: Anaplan ALM docs (`help.anaplan.com`, Application Lifecycle Management). See
> [`SOURCES.md`](../../SOURCES.md).
