# Seasonality / phasing an annual figure to months

> **Level:** L2 · **Area:** Time & Forecasting · **PLANS:** Logical, Auditable · **DISCO:** Inputs / Calculations

## The ask

"Sales gave me a £12m annual number per product. Spread it across the year by our usual seasonal shape — December is big, January is dead."

## When you'll see this

- A figure is planned annually but the model needs monthly detail.
- A known **seasonal profile** (December heavy, summer light) should shape the spread.
- Budget phasing, demand planning, cash phasing.

## Approach

Hold a **seasonality profile** as monthly weights, normalise them to a ratio that sums to 1 across the year, then `monthly = annual × month ratio`. It's the [breakback](../mapping-and-allocation/breakback-ratio-input.md) pattern applied to Time: the "children" are the months, the "ratio" is the seasonal share.

```
month value = annual total × (month weight ÷ sum of weights in the year)
```

Keep the profile in an **Inputs** module (planners tune the shape) and the annual total in another; the monthly result is a clean calc.

Why idiomatic:

- **Logical (PLANS):** weights → ratio → spread, each a step.
- **Auditable:** the profile is visible and editable; the spread is one multiply.

## Blueprint

**`INP30 Seasonality Profile`** — monthly weights, `Applies To` Product × Month (or a shared profile by Profile list):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Weight | Number | Sum | Product, Month | *(input, e.g. 1.0 flat, 2.5 for Dec)* |
| Year Weight | Number | Sum | Product, Month | `YEARVALUE(Weight)` |
| Month Ratio | Number | None | Product, Month | `IF Year Weight = 0 THEN 0 ELSE Weight / Year Weight` |

**`INP31 Annual Plan`** — `Applies To` Product × Year:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Annual Total | Number | Sum | Product, Year | *(input)* |

**`CAL80 Phased Plan`** — `Applies To` Product × Month:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Monthly Plan | Number | Sum | Product, Month | `Annual (this year) × INP30 Seasonality Profile.Month Ratio` |

## Formula(s)

Normalise the weights to a ratio that sums to 1 within each year. `YEARVALUE(Weight)` gives every month the **total weight of its own year** — the denominator each month needs, at the month grain — so the ratio is correct cell-by-cell:

```
// INP30 Seasonality Profile -> Year Weight
YEARVALUE(Weight)

// INP30 Seasonality Profile -> Month Ratio
IF Year Weight = 0 THEN 0 ELSE Weight / Year Weight
```

Spread the annual figure (bring the year total to each month via `YEARVALUE`, which gives every month of a year the value held at the year):

```
// CAL80 Phased Plan -> Monthly Plan
YEARVALUE(INP31 Annual Plan.Annual Total) * INP30 Seasonality Profile.Month Ratio
```

`YEARVALUE` returns, for each month, the value of the line item at that month's **year** — perfect for broadcasting an annual figure down to its months.

## Pitfalls / gotchas

- **Ratio must sum to 1 per year**, or the months won't re-sum to the annual total. Normalise (`Weight / Year Weight`); don't assume raw weights already sum to 1.
- **Divide-by-zero** if a product has all-zero weights — guard it and decide a fallback (even spread = `1/12`).
- `YEARVALUE` broadcasts the **year** value to months; make sure `Annual Total` is held at the Year level (or use the correct time-summary).
- A flat (even) spread is just weights all = 1 → ratio = `1/12`. Don't hard-code `/12`; let the profile express it so a 53-week or part-year case still works.
- Re-entering the annual total **recomputes** all months — manual month tweaks need a separate override line.

## Performance & PLANS notes

- The profile is small and reusable; reference it from many phased calcs (**Necessary**).
- Time-summary functions like `YEARVALUE` are engine-native — faster and clearer than `IF MONTH(...) = ...` chains.
- Same ratio engine as [breakback](../mapping-and-allocation/breakback-ratio-input.md) and [top-down allocation](../mapping-and-allocation/top-down-allocation-by-ratio.md) — learn it once.

## Related

- [`docs/02-formulas/time-functions.md`](../../docs/02-formulas/time-functions.md)
- Recipes: [breakback-ratio-input](../mapping-and-allocation/breakback-ratio-input.md) · [top-down-allocation-by-ratio](../mapping-and-allocation/top-down-allocation-by-ratio.md) · [rolling-forecast](rolling-forecast.md)
