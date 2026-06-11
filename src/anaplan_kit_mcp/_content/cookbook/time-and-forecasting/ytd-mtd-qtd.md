# YTD / MTD / QTD running totals

> **Level:** L2 · **Area:** Time & Forecasting · **PLANS:** Performance, Logical · **DISCO:** Calculations

## The ask

"On the dashboard I want revenue this month, but also year-to-date and quarter-to-date next to it — and YTD should reset every January."

## When you'll see this

- Any P&L or KPI report needs a period figure *and* a cumulative figure.
- YTD that resets at year start; QTD that resets each quarter.
- "Number of working days so far this month" style counters.

## Approach

Use **`CUMULATE`** with a **reset Boolean**. `CUMULATE(value, reset)` adds the value across Time from the start, but starts over wherever the reset Boolean is `TRUE`. Build the reset flags **once** in a `SYS01 Time Settings` module (one Boolean per period type) and reference them everywhere — that's the Sustainable, calculate-once pattern.

```
YTD = CUMULATE(period value, Is First Month of Year?)
```

MTD on a monthly model is just the period value itself; on a weekly/daily model, MTD = `CUMULATE(value, Is First Week of Month?)`.

Why idiomatic:

- **Performance/Logical (PLANS):** `CUMULATE` is engine-native and far faster than a chain of `LAG`/`PREVIOUS` adds.
- The reset flags live in System and feed every cumulative line item — no repeated date logic.

## Blueprint

**`SYS01 Time Settings`** — period attributes, `Applies To` Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Is First Month of Year? | Boolean | None | Time | `MONTH(START()) = 1` |
| Is First Month of Quarter? | Boolean | None | Time | `MONTH(START()) IN {1, 4, 7, 10}` |

**`CAL50 Revenue with Cumulatives`** — `Applies To` L3 Cost Centre × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Revenue | Number | Sum | L3 Cost Centre, Time | *(from source)* |
| Revenue YTD | Number | Sum | L3 Cost Centre, Time | `CUMULATE(Revenue, SYS01 Time Settings.Is First Month of Year?)` |
| Revenue QTD | Number | Sum | L3 Cost Centre, Time | `CUMULATE(Revenue, SYS01 Time Settings.Is First Month of Quarter?)` |

## Formula(s)

Year-to-date that resets every January:

```
// CAL50 -> Revenue YTD
CUMULATE(Revenue, SYS01 Time Settings.Is First Month of Year?)
```

Quarter-to-date:

```
// CAL50 -> Revenue QTD
CUMULATE(Revenue, SYS01 Time Settings.Is First Month of Quarter?)
```

Define the reset flags in `SYS01` (the `START()` of each period gives its first day, so `MONTH(START()) = 1` is January):

```
// SYS01 -> Is First Month of Year?
MONTH(START()) = 1
```

Plain `CUMULATE(Revenue)` with no Boolean cumulates across the **whole** timescale (no reset) — useful for an inception-to-date balance.

## Pitfalls / gotchas

- **Reset Boolean is "reset *to* this period"**: the period where the flag is `TRUE` becomes the new starting point of the running total. Confirm Jan shows just-January, not Dec+Jan.
- Don't fake YTD with the **Time Summary** (the row total) — that's the full-year total, not "to date". `CUMULATE` is the right tool.
- Set the cumulative line item's **summary to `Sum`** so it rolls correctly across the hierarchy; the time behaviour comes from `CUMULATE`, not the summary.
- A fiscal year not starting in January? Drive the reset flag off your **fiscal** calendar in `SYS01`, not the literal calendar month.
- `CUMULATE` works along the model's Time dimension; it won't cumulate across a list unless you give it the list argument deliberately.

## Performance & PLANS notes

- `CUMULATE` is one engine pass — cheaper than `LAG`-based running sums and far cheaper than nested `IF` on dates.
- Build reset Booleans **once** in `SYS01` and reuse — satisfies **Necessary** and keeps fiscal logic in one place.
- Keep cumulatives in a **Calculations/Outputs** module, not the input module, so typing actuals doesn't drag a wide cumulative grid.

## Related

- [`docs/02-formulas/time-functions.md`](../../docs/02-formulas/time-functions.md)
- Recipes: [rolling-forecast](rolling-forecast.md) · [prior-year-comparison](prior-year-comparison.md) · [dynamic-time-filter](../ux-and-workflow/dynamic-time-filter.md)
