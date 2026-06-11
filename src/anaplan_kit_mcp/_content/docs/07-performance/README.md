# Performance

> **Level:** L2 · **Area:** Performance · **PLANS:** Performance, Necessary

Anaplan keeps your whole model **in memory** and recalculates instantly. That speed is the
product's superpower — and the thing you can squander. A bloated model is slow to open, slow
to calculate, and expensive in workspace memory. This section is about keeping models fast,
and it all comes back to one number: **cell count**.

## Cell count is the master lever

A module's cell count is the **product of its dimension sizes × its line items** — every dimension
*multiplies*, every line item *adds*, so a handful of dimensions reaches tens of millions of cells
fast. See the formula and the worked 72M-cell example in
[sparsity-and-engine.md](sparsity-and-engine.md).

> **The biggest performance win is almost always *removing* a dimension or a line item you
> didn't need** — not optimising a formula. Necessity *is* performance. *(Performance,
> Necessary.)*

## The other levers

Once dimensionality is right, the rest of this section is the toolkit for trimming further
and calculating efficiently:

| Page | Lever |
| --- | --- |
| [sparsity-and-engine.md](sparsity-and-engine.md) | Understand the in-memory engine, sparsity, what cell count is, and what triggers recalculation. |
| [time-ranges.md](time-ranges.md) | **Time Ranges** — scope a module to a slice of the calendar to cut cells. |
| [line-item-subsets.md](line-item-subsets.md) | **Line item subsets** and subsets generally as a sizing tool. |
| [optimization-checklist.md](optimization-checklist.md) | A concrete do/don't checklist, phrased as PLANS-Performance actions. |

## Reading the signals

Anaplan exposes model and module **size / memory** indicators (and, for admins, performance
diagnostics). You don't need exact numbers as a beginner — you need the habit of asking, for
every module: *do I need every dimension and every line item here, and only for the periods
that matter?* The pages here turn that habit into specific techniques.

## Where to start

Read [sparsity-and-engine.md](sparsity-and-engine.md) to understand *why* cell count rules
everything, then work through [time-ranges.md](time-ranges.md) and
[line-item-subsets.md](line-item-subsets.md) as your two main shrinking tools. Keep
[optimization-checklist.md](optimization-checklist.md) open while you build.

**Related:** [PLANS — Performance](../03-methodology/plans-standard.md) ·
[The Planual](../03-methodology/planual.md) · [DISCO](../03-methodology/disco.md) ·
[Subsets — fundamentals](../01-fundamentals/numbered-lists-and-subsets.md) ·
[Learning Path](../../LEARNING-PATH.md)
