# Breakback: type a total, disaggregate to detail

> **Level:** L2 · **Area:** Mapping & Allocation · **PLANS:** Logical, Auditable · **DISCO:** Inputs / Calculations

## The ask

"Planners want to type a single annual revenue number for the region and have it automatically split across the products and months — but they also want to still see (and tweak) the detail."

## When you'll see this

- A user enters a number at a **summary** level and expects it pushed to the detail.
- "Breakback" / "spread" behaviour — the opposite of normal bottom-up rollup.
- Target-setting: set the total, let the model fill the lines by an existing mix.

## Approach

Anaplan rolls **up** by default; breakback pushes a typed total **down** to detail by a **ratio**. The clean, auditable way is *not* to fight the engine with editable summary cells, but to model it explicitly: an **input total**, a **ratio** (the existing or seed mix), and a **calculated detail = total × ratio**.

```
detail = entered total × (detail's share of the mix)
```

Note: Anaplan does have a native **Breakback** toggle on grids that lets a user edit a calculated parent and have it spread by the current child ratios. This recipe gives the **explicit, model-driven** version — it's more auditable and survives in calculation modules where the grid toggle doesn't apply.

Why idiomatic:

- **Auditable (PLANS):** the total, the ratio and the detail are separate line items you can inspect.
- **Logical:** ratio sums to 1, so the detail sums back to the entered total.

## Blueprint

**`INP10 Region Target`** — the single typed number, `Applies To` Region (no Product/Time detail):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Annual Target | Number | Sum | Region | *(input)* |

**`CAL30 Region Totals`** — `Applies To` **Region** (the denominator grain, one row per region):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Total Mix (region) | Number | Sum | Region | `CAL30 Breakback.Seed Mix` *(Product & Month dimensions drop, so it sums to the region total)* |

**`CAL30 Breakback`** — `Applies To` Region × Product × Month:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Seed Mix | Number | Sum | Region, Product, Month | `OUT_PY.Revenue` *(or a typed mix)* |
| Total Mix (at detail) | Number | None | Region, Product, Month | `CAL30 Region Totals.Total Mix (region)` *(broadcast back to each Product × Month)* |
| Ratio | Number | None | Region, Product, Month | `IF Total Mix (at detail) = 0 THEN 0 ELSE Seed Mix / Total Mix (at detail)` |
| Target | Number | None | Region, Product, Month | `INP10 Region Target.Annual Target` *(broadcast from the region grain)* |
| Spread Detail | Number | Sum | Region, Product, Month | `Target × Ratio` |

## Formula(s)

Sum the seed mix to the region grain, then broadcast it back so every detail cell divides by the **same** region denominator. `CAL30 Region Totals` has neither Product nor Month, so referencing `Seed Mix` into it sums those dimensions away; referencing the region total back into the detail module repeats it across every Product × Month:

```
// CAL30 Region Totals -> Total Mix (region)   (Applies To Region)
CAL30 Breakback.Seed Mix

// CAL30 Breakback -> Total Mix (at detail)   (region total, repeated across detail)
CAL30 Region Totals.Total Mix (region)
```

Build the ratio (numerator and denominator now both at the detail grain), guarding the divide:

```
// CAL30 Breakback -> Ratio
IF Total Mix (at detail) = 0 THEN 0 ELSE Seed Mix / Total Mix (at detail)
```

Bring the typed total down to every detail cell (it broadcasts from the region grain), then spread:

```
// CAL30 Breakback -> Target
INP10 Region Target.Annual Target

// CAL30 Breakback -> Spread Detail
Target * Ratio
```

Because every detail divides its own seed mix by the same region total, the ratios sum to 1 within a region and `Spread Detail` re-sums to the typed `Annual Target`.

## Pitfalls / gotchas

- **Don't make a summary cell editable in a calc module and expect spread** — that's the native grid Breakback toggle, only available on input modules/grids and easily confused. For repeatable logic, use this explicit total × ratio model.
- **Zero seed mix = nothing to spread to.** Guard the divide; decide a fallback (even split: `1 / COUNT` of detail, or carry the whole total to a default line).
- **Two-level breakback** (split to Product *and* Month) needs the ratio to cover the full detail grain, or you'll double-allocate. Use one combined ratio across Product × Month.
- Re-entering the total **overwrites** any manual line tweaks, because the detail is calculated. If users must tweak lines, give them an editable override line item and a switch.
- Watch rounding — spread detail may not re-sum to the typed total to the penny.

## Performance & PLANS notes

- Explicit breakback (input + ratio + calc) is **Auditable** and recalcs predictably, unlike chained editable summaries.
- Reuse the same ratio engine as [top-down-allocation-by-ratio](top-down-allocation-by-ratio.md) and [seasonality-phasing](../time-and-forecasting/seasonality-phasing.md) — it's the same shape.
- Keep the **input** total in a small Inputs module so typing it doesn't recalc the big calc module's other cells unnecessarily.

## Related

- [`docs/01-fundamentals/modules.md`](../../docs/01-fundamentals/modules.md)
- Recipes: [top-down-allocation-by-ratio](top-down-allocation-by-ratio.md) · [seasonality-phasing](../time-and-forecasting/seasonality-phasing.md) · [allocate-by-driver](allocate-by-driver.md)
