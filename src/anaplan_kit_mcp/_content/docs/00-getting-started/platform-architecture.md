# Platform Architecture

> **Level:** L1 · **Area:** Getting Started

Before you build anything, you need a map of *where things live* and *who controls what*. Anaplan
is organised as a nested hierarchy of containers, and you build inside the smallest one — the
**model**.

---

## Tenant → Workspace → Model

```
TENANT                         your whole company's Anaplan estate (one per customer)
  └── WORKSPACE                a licensed bucket of memory; holds related models
        └── MODEL              the thing you actually build (lists, modules, formulas)
              └── modules, lists, line items, dashboards, pages…
```

| Container | What it is | Who manages it |
| --- | --- | --- |
| **Tenant** | The top-level account for your organisation. Holds all workspaces, all users, and tenant-wide settings (SSO, security policies). | **Tenant administrator** |
| **Workspace** | A licensed container with a fixed **memory size** (its "allowance"). Several related models live in one workspace and share that memory. | **Workspace administrator** |
| **Model** | A single connected-planning application: its own lists, modules, time, versions, dashboards and security. This is your workbench. | **Model builder** |

> ⚠️ **Workspace memory is the constraint that shapes everything.** A workspace has a finite size,
> and every model in it consumes part of that allowance. This is *why* performance discipline (small
> cell counts, time ranges, subsets) matters from day one — see [PLANS → Performance](../03-methodology/plans-standard.md)
> and [Dimensions](../01-fundamentals/dimensions.md).

A typical setup: one **data hub** model (the shared source of truth) plus several **spoke** models
(FP&A, Sales, Supply Chain), all in the same workspace, exchanging data through imports.

---

## The in-memory calculation engine

This is what makes Anaplan different from a database or a spreadsheet.

- The **entire model lives in memory (RAM)**, not on disk. Every cell of every module is held in
  active memory while the model is open.
- When you change a value or a formula, Anaplan recalculates **only what depends on it**, and does so
  **instantly** — there is no batch job, no overnight refresh, no "recalculate" button.
- Many users can be in the same model at once, all seeing changes ripple through in real time.

**Consequences you'll feel as a builder:**

1. **Size = speed *and* cost.** Memory is finite, so a bloated model is both slow and expensive.
   Cell count (the product of all a module's dimension sizes × its line items) is the number to
   watch. See [Dimensions](../01-fundamentals/dimensions.md).
2. **There is no "run".** You don't compile or execute a model. You change it and the result is
   already there. The docs in this kit therefore *describe and illustrate* — they're validated
   against Anaplan's published syntax, not executed (see [`SOURCES.md`](../../SOURCES.md)).
3. **Order doesn't matter, dependencies do.** You don't sequence calculations top-to-bottom like a
   script; Anaplan figures out the dependency graph. Your job is to keep that graph clean and
   one-directional (see [PLANS → Logical](../03-methodology/plans-standard.md)).

---

## What makes Anaplan different: Connected Planning

The phrase Anaplan uses for itself is **Connected Planning**. Three ideas sit behind it:

| Idea | What it means in practice |
| --- | --- |
| **One connected model** | Modules link through formulas, so an assumption changed in one place updates every dependent number — across functions (finance, sales, ops) that used to live in separate spreadsheets. |
| **Real-time recalculation** | No waiting. Type a new growth rate and the forecast, the P&L, and the dashboard all update at once. |
| **A single source of truth** | Shared reference data (the org hierarchy, the product list, actuals) lives in a **data hub** and flows out to every model, so everyone plans off the same numbers. |

Contrast with spreadsheets: linked workbooks break, can't be edited by many people safely, have no
audit trail, and force you to copy the same formula into thousands of cells. Anaplan replaces that
with one governed, recalculating, multi-user model.

---

## Who does what — the three roles

You will hear these three roles constantly. They're about *permissions and scope*, not job titles.

| Role | Scope | Typical responsibilities |
| --- | --- | --- |
| **Model builder** | Inside one or more **models** they're granted access to. | Build lists, modules, line items, formulas, dashboards/pages; design the model; set up actions and imports. **This is you.** |
| **Workspace administrator** | A whole **workspace**. | Create/delete models, manage the workspace's memory allowance, control who can build in which model, run ALM (dev/test/prod). |
| **Tenant administrator** | The whole **tenant**. | Manage users and SSO at the organisation level, create workspaces, set security policies, oversee licensing. |

These layer up: a tenant admin can do workspace-admin things; a workspace admin can grant
model-builder access. A single person often wears several hats in a small organisation, but the
*scopes* are distinct — and security best practice is to grant the **least** scope needed (see
[Security & ALM](../06-security-alm/)).

> End users (planners, reviewers) aren't on this list — they don't build, they *use* the model
> through dashboards/pages, with what they can see and edit governed by
> [selective access and DCA](../06-security-alm/).

---

**Related:** [Getting started index](README.md) · [Glossary](glossary.md) ·
[Dimensions](../01-fundamentals/dimensions.md) · [PLANS](../03-methodology/plans-standard.md) ·
[Security & ALM](../06-security-alm/)

> Source: Anaplan platform documentation (Anapedia, `help.anaplan.com`). Confirm current behaviour for your platform version. See [`SOURCES.md`](../../SOURCES.md).
