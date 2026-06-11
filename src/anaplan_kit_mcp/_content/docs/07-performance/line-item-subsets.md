# Line Item Subsets (and Subsets as a Sizing Tool)

> **Level:** L2 · **Area:** Performance · **PLANS:** Performance, Necessary, Sustainable

Two related tools let you treat *a chosen slice* of something as a dimension, so you size and
calculate against only what you need: ordinary **subsets** (a flagged portion of a **list**)
and **line item subsets** (treating selected **line items** as if they were a list
dimension). Both are levers on [cell count](sparsity-and-engine.md). For the fundamentals of
list subsets, see [numbered lists & subsets](../01-fundamentals/numbered-lists-and-subsets.md);
this page focuses on their use as a **performance / sizing** tool.

## Subsets as a sizing tool (recap)

A **subset** is a Boolean-flagged portion of a list you can use as a **smaller dimension**.
Instead of dimensioning a module by all 5,000 products, dimension it by the *"Planned
Products"* subset of 300.

```
Products (full list)         5,000 members
  └─ Subset "Planned"          300 members   ← dimension the planning module by THIS
```

The planning module is now sized for **300**, not 5,000 — a ~94% cut on that dimension,
multiplied through everything else in the module. Use subsets wherever a module only ever
operates on a known **portion** of a list. *(Necessary, Performance.)*

## Line item subsets — line items as a dimension

A **line item subset** turns a chosen set of **line items** (from one or more modules) into
something you can use as a **list-style dimension** in another module. Instead of repeating
the same handful of measures as separate line items everywhere, you reference them as members
of a dimension.

### Why this helps

Consider a P&L with measures `Revenue`, `COGS`, `Gross Margin`, `Opex`, `EBIT`. Suppose many
modules need to do the *same thing* to *each* of those measures (variance, % of revenue,
currency conversion). Two ways to model it:

| Approach | Shape | Problem |
| --- | --- | --- |
| Repeat line items | Each module re-declares `Revenue … EBIT` and repeats the formula per measure | Duplicated logic; widening the set means editing every module *(breaks Necessary, Sustainable)* |
| **Line item subset** | The measures become a **dimension**; calc is written **once** across that dimension | One formula handles all measures; add a measure to the subset and it flows everywhere |

### What it looks like

```
Line Item Subset "P&L Measures"  ←  { Revenue, COGS, Gross Margin, Opex, EBIT }

Module "Variance"  dimensioned by:  Cost Centre × Time × [P&L Measures]
  Variance = Actual[P&L Measures] - Budget[P&L Measures]   (one formula, all measures)
```

Now the variance logic is written **once** over the `[P&L Measures]` dimension rather than
five times. Add `Depreciation` to the subset and the variance module picks it up with **no
formula change**. *(Necessary, Sustainable.)*

## Using both to control size

- **List subset** → fewer **rows/members** in a dimension (plan only the products you plan).
- **Line item subset** → fewer **repeated line items / modules**; the measures become one
  reusable dimension instead of duplicated columns.

Both reduce what the engine has to store and recompute, and both keep logic in **one place**.

## Pitfalls

| Pitfall | Note |
| --- | --- |
| Over-using line item subsets | They add a layer of abstraction; use where measures genuinely repeat across modules, not for a one-off |
| Forgetting subset **maintenance** | A list subset is only as right-sized as its Boolean flag — drive the flag from a System module so it stays current *(Sustainable)* |
| Mixing **incompatible formats** in a line item subset | Members should be consistent (e.g. all numeric) so the cross-dimension formula behaves |
| Assuming a subset **copies** data | A subset is a *view of membership*, not a duplicate — it points at the same items |

## Good practice

- Reach for a **list subset** whenever a module operates on a *known portion* of a big list.
- Reach for a **line item subset** when the *same calculation repeats across the same set of
  measures* in several places — write it once over the subset.
- Drive subset membership from **System** modules / Booleans, not by hand. *(Sustainable.)*
- Re-check, per module: *am I sizing by the smallest correct set of items and measures?*

**Related:** [Performance overview](README.md) ·
[Sparsity & cell count](sparsity-and-engine.md) · [Time Ranges](time-ranges.md) ·
[Optimization checklist](optimization-checklist.md) ·
[Numbered lists & subsets — fundamentals](../01-fundamentals/numbered-lists-and-subsets.md)

> Source: Anaplan subsets & line item subsets docs (`help.anaplan.com`, lists & modules /
> performance). See [`SOURCES.md`](../../SOURCES.md).
