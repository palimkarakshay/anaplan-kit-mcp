# Replace nested IF with a Boolean

> **Level:** L2 · **Area:** Performance · **PLANS:** Performance, Auditable · **DISCO:** System / Calculations

## The ask

"This module recalcs for ages and the formula is a wall of nested `IF`s. The model builder before me wrote one 12-line formula per cell. Can we make it fast?"

## When you'll see this

- A big module (high cell count) with heavy nested `IF` formulas.
- Conditions re-evaluated in many line items.
- Recalc that drags whenever any input changes.

## Approach

Move the condition into a **Boolean line item** computed once, then reference the Boolean instead of repeating the `IF` test. Even better, replace `IF`-based routing with **`SUM`/`LOOKUP` over a mapping** where you're really selecting by category. The Planual is explicit: avoid heavy `IF` on large cell counts; prefer Booleans and mapping.

```
// instead of repeating a condition in five formulas:
Eligible? (Boolean, computed once)  ->  referenced by the five formulas
```

Why idiomatic:

- **Performance (PLANS):** the engine evaluates the Boolean once and reuses it; nested `IF`s re-test every time, on every cell.
- **Auditable:** a named Boolean (`Is Active?`, `In Window?`) reads better than a buried condition.

## Blueprint

**Before** — one bloated calc line item:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Net Revenue | Number | Sum | Product, Time | `IF Active AND NOT Discontinued AND Price > 0 AND In Window THEN Volume * Price * (1 - Disc%) ELSE 0` |

**After** — Booleans computed once, then a clean calc:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Eligible? | Boolean | None | Product, Time | `Active AND NOT Discontinued AND Price > 0 AND In Window` |
| Gross | Number | Sum | Product, Time | `Volume * Price` |
| Net Revenue | Number | Sum | Product, Time | `IF Eligible? THEN Gross * (1 - Disc%) ELSE 0` |

## Formula(s)

Compute the condition once:

```
// CAL -> Eligible?
Active? AND NOT Discontinued? AND Price > 0 AND SYS01 Time Settings.In Window?
```

Reference it (one cheap test instead of re-deriving the whole condition):

```
// CAL -> Net Revenue
IF Eligible? THEN Gross * (1 - Disc%) ELSE 0
```

Where you're routing by **category**, drop the `IF` chain entirely and map (see [sum-vs-nested-lookup](sum-vs-nested-lookup.md)):

```
// instead of IF Type = A THEN ... ELSE IF Type = B THEN ...
Driver.Value[LOOKUP: SYS Mapping.Target]
```

## Pitfalls / gotchas

- **A single small `IF` is fine.** The problem is *nested/repeated* `IF` on *large* modules. Don't over-engineer a 3-item module.
- **Compute the Boolean in the smallest module that makes sense** (often a SYS module), then reference it — don't recompute it in every calc.
- **Booleans don't aggregate like numbers** — set summary to `None` (or use it deliberately); a Boolean summed across a hierarchy behaves differently than you might expect.
- Splitting into steps adds line items — that's the right trade: a few extra cheap line items beat one giant per-cell formula (still **Necessary**, because each step is used).
- Watch for conditions that belong in a mapping, not a Boolean — if you're testing "which item is this", map instead of `IF`.

## Performance & PLANS notes

- The win scales with cell count: on millions of cells, evaluating a condition once vs many times is dramatic.
- Stepped Booleans + simple calcs are simultaneously a **Performance** and **Auditable** win — the Planual's recurring theme.
- Reuse the Boolean across modules (DCA, filters, calcs) — calculate once, reference everywhere.

## Related

- [`docs/07-performance/`](../../docs/07-performance/)
- [`docs/03-methodology/planual.md`](../../docs/03-methodology/planual.md)
- Recipes: [sum-vs-nested-lookup](sum-vs-nested-lookup.md) · [shrink-with-subsets-and-time-ranges](shrink-with-subsets-and-time-ranges.md) · [allocate-by-driver](../mapping-and-allocation/allocate-by-driver.md)
