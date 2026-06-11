# The Calc Engine, Sparsity & Cell Count

> **Level:** L2 · **Area:** Performance · **PLANS:** Performance, Necessary

To build fast models you need a working mental model of *how Anaplan calculates*. This page
covers the in-memory engine, why **cell count** is the number that matters, what **sparsity**
is (and why it still costs you), and **what triggers a recalculation**.

## The in-memory calculation engine

Anaplan holds the **entire model in RAM** and recalculates **immediately** when an input
changes. There is no "run" button and no waiting for an overnight batch — change a price,
and revenue, margin and the P&L update in front of you. That's why it feels instant.

The cost of that magic: **every cell you define occupies memory**, whether or not it holds an
interesting number. Performance is therefore mostly a question of *how many cells exist* and
*how much recalculation a change sets off*.

## Cell count — the master number

A module is a multi-dimensional grid. Its cell count is the **product of its dimension sizes
× its line items**:

```
cells = dim₁ × dim₂ × … × dimₙ × (number of line items)
```

Worked example:

| Dimension | Size |
| --- | --- |
| Product | 500 |
| Cost Centre | 200 |
| Month | 36 |
| Line items | 20 |

```
500 × 200 × 36 × 20 = 72,000,000 cells   in one module
```

The lesson: each **dimension multiplies**, each **line item adds**. Adding one more
dimension (say Version × 4) takes this to **288 million**. This is why
[right-sizing dimensionality](optimization-checklist.md) is the single biggest lever, and why
[Time Ranges](time-ranges.md) and [subsets](line-item-subsets.md) — which *reduce* a
dimension's effective size — matter so much.

## Sparsity — empty cells still cost

A module is **sparse** when most of its cells are blank — e.g. most products aren't sold in
most cost centres, but a Product × Cost Centre module reserves a cell for **every**
combination anyway.

- Anaplan still **accounts for** that grid; a sparse module dimensioned by two big lists can
  be enormous even if 95% is empty.
- The fix is **structural, not cosmetic**: don't dimension a module by lists whose
  combinations are mostly meaningless. Where a real relationship is sparse, model it on a
  **numbered list** of the *actual* combinations (transactions), not the full cross-product.

> **Sparsity is a design smell, not a free lunch.** Blank cells you'll never use are cell
> count you're still paying for. *(Necessary, Performance.)*

## What triggers recalculation

Understanding recalc helps you keep models snappy:

- **Editing an input** recalculates everything **downstream** of it (the dependency chain),
  not the whole model.
- **Large modules in the chain cost more** to recompute — a change feeding a 72M-cell module
  is heavier than one feeding a 10k-cell module.
- **Formula shape matters.** A single giant nested formula recalculates as one big lump;
  **stepped line items** let the engine recompute only the steps affected and are easier to
  audit. *(Auditable + Performance — the same advice from two directions.)*
- **`IF` on huge cell counts** is expensive; a **Boolean** line item evaluated once, then
  referenced, is cheaper (see [the checklist](optimization-checklist.md)).

So two things drive recalc cost: **how many cells** are downstream, and **how the formulas are
shaped**. You control the first with dimensionality/Time Ranges/subsets, and the second with
the patterns in the [optimization checklist](optimization-checklist.md).

## Reading the model's size indicators (conceptually)

Anaplan shows **size / memory** information at the model and module level, and admins have
access to performance diagnostics. As a beginner, you don't need to interpret exact byte
counts — build the instinct to check, per module: *which dimensions am I using, how big are
they, how many line items, and could any of this be smaller?* That question, asked every
time, prevents most performance problems before they start.

**Related:** [Performance overview](README.md) · [Time Ranges](time-ranges.md) ·
[Line item subsets](line-item-subsets.md) ·
[Optimization checklist](optimization-checklist.md) ·
[PLANS — Performance](../03-methodology/plans-standard.md)

> Source: Anaplan engine & performance best-practice materials (`help.anaplan.com` &
> Anaplan Community). See [`SOURCES.md`](../../SOURCES.md).
