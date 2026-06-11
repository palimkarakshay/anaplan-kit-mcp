# Shrink a model with subsets & time ranges

> **Level:** L2 · **Area:** Performance · **PLANS:** Performance, Necessary · **DISCO:** any

## The ask

"The workspace is nearly full and the model is slow. Half the modules are dimensioned by every product and every month back to 2015, but most cells are empty. How do I cut it down without losing anything we use?"

## When you'll see this

- Workspace size / cell-count pressure.
- Modules dimensioned by more list members or more periods than they actually need.
- Sparse modules (mostly blank cells) bloating memory.

## Approach

Cell count = product of every dimension's size × number of line items. Two precise scalpels:

- **Subsets** — dimension a module by a *subset* of a list (only the members it needs) instead of the whole list.
- **Time Ranges** — give a module its own shorter time scope (e.g. 3 years) instead of the model's full calendar.

Both cut cells without deleting data elsewhere. The Planual: only dimension by what you truly need (**Necessary**), and use Time Ranges to bound time (**Performance**).

Why idiomatic:

- **Performance (PLANS):** fewer cells = less memory and faster recalc — the biggest lever in the model.
- **Necessary:** you store exactly what's used, nothing speculative.

## Blueprint

**Before** — over-dimensioned:

| Module | Applies To | Issue |
| --- | --- | --- |
| `CAL Margin` | All Products (5,000) × Full Time (2015–2030, 192 mo) | most products inactive; only 3 forecast years used |

**After** — trimmed:

| Module | Applies To | Fix |
| --- | --- | --- |
| `CAL Margin` | `Active Products` subset (400) × Time Range `Plan Horizon` (36 mo) | subset + time range |

**`SYS Product Subset Driver`** — Boolean defining the subset membership:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Active? | Boolean | None | Product | `SYS Product Details.Status = Status.Active` |

## Formula(s)

This is mostly **structure** — create a subset and a time range, then re-point modules at them. The only formula is the Boolean that drives subset membership (you can build a subset from a Boolean line item):

```
// SYS Product Subset Driver -> Active?
SYS Product Details.Status = Status.Active
```

Then: create a **subset** of `Product` based on `Active?`, create a **Time Range** (`Plan Horizon`, e.g. FY24–FY26 monthly), and set the module's **Applies To** to the subset and its **Time** to the Time Range.

There's no formula to "make it smaller" — sizing is a **dimensioning** choice, which is the point.

## Pitfalls / gotchas

- **Time Range mismatch breaks time formulas.** `LAG`/`CUMULATE`/`PREVIOUS` operate within the line item's time range — if a source has a wider range than the target, references can return blanks at the edges. Confirm ranges line up.
- **Subset membership must be maintained** — if it's driven by an `Active?` flag, make sure the flag updates (import/formula), or the subset goes stale.
- **Aggregation across a subset** only sums subset members — a roll-up may differ from the full-list total. Be deliberate.
- Don't subset away members you still need for **history or audit**; subset the *working* modules, keep the full landing data.
- Removing a dimension a module doesn't need (e.g. it didn't need Time at all) is an even bigger win than subsetting — check dimensionality first.

## Performance & PLANS notes

- The order of impact: (1) remove unnecessary **dimensions**, (2) **subset** the ones you keep, (3) **Time Range** the time scope, (4) reduce line items.
- Subsets + Time Ranges are the canonical **Performance** + **Necessary** tools — reach for them before anything exotic.
- Sparsity is the enemy: a module that's 95% blank is mostly wasted cells — subset/range it down.
- After trimming, check the model's cell-count / size indicators to confirm the saving — measure, don't guess.

## Related

- [`docs/07-performance/time-ranges.md`](../../docs/07-performance/time-ranges.md)
- [`docs/01-fundamentals/numbered-lists-and-subsets.md`](../../docs/01-fundamentals/numbered-lists-and-subsets.md)
- Recipes: [replace-if-with-boolean](replace-if-with-boolean.md) · [sum-vs-nested-lookup](sum-vs-nested-lookup.md) · [build-a-data-hub](../data-and-imports/build-a-data-hub.md)
