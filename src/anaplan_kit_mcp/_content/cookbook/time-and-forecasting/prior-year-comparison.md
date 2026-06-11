# Prior-year comparison (YoY with LAG / OFFSET)

> **Level:** L2 · **Area:** Time & Forecasting · **PLANS:** Logical, Auditable · **DISCO:** Calculations

## The ask

"On every P&L line show this month vs the same month last year, and the % growth."

## When you'll see this

- Year-on-year, month-on-month, or same-period-last-year comparisons.
- Growth %, variance vs prior year, indexed trends.
- Any report with a "PY" or "vs LY" column.

## Approach

Shift a value back along Time with **`LAG`** (or `OFFSET`). On a monthly model, same-month-last-year is 12 periods back; prior month is 1 back. `LAG(value, n, default)` pulls the value from `n` periods earlier, returning `default` when it runs off the start of the timescale.

```
PY value = LAG(value, 12, 0)        // monthly model
YoY %     = (this − PY) / PY
```

`LAG` and `OFFSET` are similar; `LAG(value, n, default)` looks **back** n periods. `OFFSET(value, n, default)` shifts by n (negative looks back) and can take an optional dimension. For straightforward "same month last year", `LAG` reads cleanest.

Why idiomatic:

- **Auditable/Logical (PLANS):** the comparison is an explicit, single-step line item.
- No hard-coded periods — it shifts relative to "now", so it keeps working next year (*Sustainable*).

## Blueprint

**`CAL90 YoY`** — `Applies To` L3 Cost Centre × Time (monthly):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Revenue | Number | Sum | L3 Cost Centre, Time | *(from source)* |
| Revenue PY | Number | Sum | L3 Cost Centre, Time | `LAG(Revenue, 12, 0)` |
| YoY Variance | Number | Sum | L3 Cost Centre, Time | `Revenue - Revenue PY` |
| YoY % | Number (%) | None | L3 Cost Centre, Time | `IF Revenue PY = 0 THEN 0 ELSE YoY Variance / Revenue PY` |

## Formula(s)

Same month, prior year (12 periods back on a monthly scale):

```
// CAL90 YoY -> Revenue PY
LAG(Revenue, 12, 0)
```

Variance and growth %, guarded against divide-by-zero:

```
// CAL90 YoY -> YoY Variance
Revenue - Revenue PY

// CAL90 YoY -> YoY %
IF Revenue PY = 0 THEN 0 ELSE YoY Variance / Revenue PY
```

`OFFSET` alternative (negative shift looks backward; third arg is the substitute when off-range):

```
OFFSET(Revenue, -12, 0)
```

## Pitfalls / gotchas

- **The lag count must match your time grain.** Monthly = 12 for a year; quarterly = 4; weekly ≈ 52 (and 53-week years bite). Don't assume 12.
- **First year has no PY** — `LAG` returns the default (use `0`, or `BLANK` if you want the cell empty). Decide which, and make the % handle it.
- **Divide-by-zero** in growth % when PY is 0 — always guard.
- `LAG`/`OFFSET` shift along the **model's Time dimension**; they don't understand "fiscal year" on their own. For SPLY across an irregular calendar, drive the offset from a `SYS01` mapping instead.
- Don't build PY by hard-coding `IF Time = ...` — that breaks every January (*Sustainable* violation).

## Performance & PLANS notes

- `LAG`/`OFFSET` are engine-native time shifts — cheap and one-step **Auditable**.
- Keep PY, variance and % as **separate** line items rather than one nested formula — easier to read and recalc.
- If many modules need PY, consider a single comparison module and reference it (**Necessary**).

## Related

- [`docs/02-formulas/time-functions.md`](../../docs/02-formulas/time-functions.md)
- Recipes: [variance-waterfall-bridge](../financial-calcs/variance-waterfall-bridge.md) · [ytd-mtd-qtd](ytd-mtd-qtd.md) · [latest-non-blank](../hierarchies-and-lists/latest-non-blank.md)
