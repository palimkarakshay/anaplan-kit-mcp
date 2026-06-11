# Straight-line depreciation

> **Level:** L2 · **Area:** Financial Calcs · **PLANS:** Logical, Auditable · **DISCO:** Calculations

## The ask

"We capitalise assets and depreciate them straight-line over their useful life. From the in-service date, spread the cost evenly across the months of its life and stop when it's fully depreciated."

## When you'll see this

- CapEx / fixed-asset planning, depreciation schedules.
- Spreading a one-off cost evenly over a number of periods from a start date.
- Any "amortise X over N months starting on date D" pattern.

## Approach

Per asset: monthly depreciation = cost ÷ useful-life months, charged only in the **months within the asset's life window** (on/after the in-service month, before life ends). Drive the window with period flags so nothing is hard-coded.

```
monthly dep = IF (in life window) THEN Cost / Useful Life Months ELSE 0
```

Hold asset attributes (cost, life, in-service date) in an Inputs/Data module; compute the schedule in a Calc module dimensioned by Asset × Time.

Why idiomatic:

- **Auditable (PLANS):** the period charge, the cumulative, and the NBV are separate, inspectable steps.
- **Sustainable:** the window is date-driven — add an asset and the schedule builds itself.

## Blueprint

**`INP50 Asset Register`** — `Applies To` Asset:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Cost | Number | Sum | Asset | *(input)* |
| In-Service Date | Date | None | Asset | *(input)* |
| Useful Life (months) | Number | None | Asset | *(input)* |

**`CAL120 Depreciation`** — `Applies To` Asset × Time (monthly):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Months Since Start | Number | None | Asset, Time | see formula |
| In Life Window? | Boolean | None | Asset, Time | `Months Since Start >= 0 AND Months Since Start < INP50.Useful Life (months)` |
| Monthly Depreciation | Number | Sum | Asset, Time | `IF In Life Window? THEN INP50.Cost / INP50.Useful Life (months) ELSE 0` |
| Accumulated Depreciation | Number | Sum | Asset, Time | `CUMULATE(Monthly Depreciation)` |
| Net Book Value | Number | Sum | Asset, Time | `INP50.Cost - Accumulated Depreciation` |

## Formula(s)

Months elapsed since the in-service month (0 in the start month). Use a period index from `SYS01`:

```
// CAL120 -> Months Since Start
SYS01 Time Settings.Period Index
  - LOOKUP index of the period containing INP50 Asset Register.In-Service Date
```

A cleaner alternative if you map the in-service month to a Time period: compare with `START()`. Then the life window:

```
// CAL120 -> In Life Window?
Months Since Start >= 0 AND Months Since Start < INP50 Asset Register.Useful Life (months)
```

Even monthly charge inside the window:

```
// CAL120 -> Monthly Depreciation
IF In Life Window? AND INP50 Asset Register.Useful Life (months) > 0
THEN INP50 Asset Register.Cost / INP50 Asset Register.Useful Life (months)
ELSE 0
```

Accumulated depreciation and NBV:

```
// CAL120 -> Accumulated Depreciation
CUMULATE(Monthly Depreciation)

// CAL120 -> Net Book Value
INP50 Asset Register.Cost - Accumulated Depreciation
```

## Pitfalls / gotchas

- **Divide-by-zero / blank life.** Guard `Useful Life > 0`.
- **Off-by-one on the window.** `< Useful Life` (not `<=`) so a 12-month life charges exactly 12 months. Verify the total depreciation equals cost.
- **Rounding residual:** `Cost / N` may not sum back to `Cost` to the penny over N months. If exactness matters, plug the final month with `Cost - prior accumulated`.
- **Mid-month conventions** (half-month in first month) need an explicit rule — don't assume; ask Finance.
- Don't hard-code the start period — derive `Months Since Start` from the asset's date so reusing the model next year just works (*Sustainable*).

## Performance & PLANS notes

- Stepped line items (window → charge → accumulated → NBV) are **Auditable** and let `CUMULATE` do the running total in one pass.
- A single Boolean window drives the charge — cheaper and clearer than nested date `IF`s.
- For reducing-balance or interest-based schedules, see [loan-amortization](loan-amortization.md).

## Related

- [`docs/02-formulas/time-functions.md`](../../docs/02-formulas/time-functions.md)
- Recipes: [loan-amortization](loan-amortization.md) · [seasonality-phasing](../time-and-forecasting/seasonality-phasing.md) · [latest-non-blank](../hierarchies-and-lists/latest-non-blank.md)
