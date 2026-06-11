# The Planual — Anaplan's Model-Building Rulebook

> **Level:** L2 · **Area:** Methodology · The Planual is to Anaplan what a style guide is to code.

## What it is

The **Planual** ("Planning manual") is Anaplan's official book of model-building **rules** —
several hundred numbered rules written by Anaplan's own master model builders. It takes the five
**PLANS** principles and turns them into concrete, checkable instructions. Rules are numbered like
`x.yy-zz` and grouped into chapters that map to the PLANS letters and to model components (Time,
Lists, Modules, Line Items, Data Hubs, Imports, Dashboards, etc.).

> ⚠️ **On rule numbers:** the Planual is versioned and Anaplan updates it. This kit cites rule
> *themes* and, where confirmable, numbers. If you need to quote an exact rule number to a client,
> confirm it in the current Planual. Where we can't confirm a number, we state the rule by its
> **PLANS principle** instead of inventing a number. See [`SOURCES.md`](../../SOURCES.md).

## How the chapters map to PLANS

| Chapter theme | PLANS letter | Example rules (paraphrased) |
| --- | --- | --- |
| Performance | **P** | Don't over-dimensionalise a module; use Time Ranges; avoid `IF` on large cell counts; calculate once and reference. |
| Logical | **L** | One-directional data flow; module per DISCO type; no circular logic. |
| Auditable | **A** | Break complex formulas into stepped line items; keep formulas short; no "magic numbers". |
| Necessary | **N** | No duplicate calculations; remove unused line items; don't store what's cheaply derived. |
| Sustainable | **S** | No hard-coded dates/items; drive logic from System modules & mappings, not `SELECT`; design for new members/periods without formula edits. |

## The rules a beginner breaks most often

These are the ones worth memorising on day one:

1. **No hard-coded list items or dates in formulas.** Use a System module flag or a Time setting
   instead. *(Sustainable)*
2. **Don't `IF` your way through everything.** A Boolean line item or a `LOOKUP`/`SUM` mapping is
   faster and clearer than nested `IF`s on a big module. *(Performance, Auditable)*
3. **One logical step per line item.** Big nested formulas are slow to recalc and impossible to
   audit. *(Auditable, Performance)*
4. **Avoid `SELECT` on specific items** (e.g. `SELECT: Products.Widget`). It breaks when the list
   changes — map instead. *(Sustainable)*
5. **Right-size dimensionality.** Only dimension a module by the lists it truly needs; every extra
   dimension multiplies cell count. *(Performance, Necessary)*
6. **Use System modules for mappings and attributes.** Don't scatter the same lookup logic across
   many calc modules. *(Necessary, Sustainable)*
7. **Set summary methods deliberately.** A line item summing when it should average (or vice
   versa) is a classic silent bug. *(Logical)*
8. **Use a Data Hub** as the single source of truth for shared data, rather than importing the
   same file into many models. *(Sustainable, Necessary)*

## How to use the Planual

- Treat it as the **tie-breaker**. When two approaches both "work", the one that satisfies more
  Planual rules wins.
- In code review, cite the principle: "this nested `IF` breaks Performance/Auditable — let's split
  it into stepped line items."
- The [cookbook](../../cookbook/) recipes and [blueprints](../../blueprints/) flag the Planual
  themes they follow.

**Related:** [PLANS](plans-standard.md) · [DISCO](disco.md) · [Performance](../07-performance/) ·
[model-build-checklist.md](model-build-checklist.md)

> Source: The Planual (Anaplan, Inc.). Confirm current rules at https://help.anaplan.com/ and the Anaplan Community. See [`SOURCES.md`](../../SOURCES.md).
