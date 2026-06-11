# FX restatement (constant currency / plan rate)

> **Level:** L2 · **Area:** Financial Calcs · **PLANS:** Logical, Auditable · **DISCO:** System / Calculations

## The ask

"Revenue is up 8% in USD but half of that is just the euro strengthening. Show me growth at *constant currency* — restate this year at last year's (or the budget) rates so we can see the real movement."

## When you'll see this

- "Constant-currency" / "FX-neutral" growth analysis.
- Restating actuals at **plan/budget rates** to isolate operational vs FX variance.
- Splitting a YoY variance into a **rate effect** and a **volume/price effect**.

## Approach

Convert the **same local amounts** at two different rate sets: the **actual** rate and a **constant** rate (prior-year average, or budget/plan rate). The difference between the two converted figures is the pure **FX effect**; the constant-currency figure is what you compare for "real" growth.

```
reported (USD)        = local × actual rate
constant currency USD = local × constant (plan/PY) rate
FX effect             = reported − constant currency
```

Why idiomatic:

- **Auditable (PLANS):** two clean conversions plus a difference — the FX effect is explicit, not buried.
- **Logical:** reuses the same local amount and the same rate table; only the rate *type* changes.

## Blueprint

**`INP40 FX Rates`** — extended with a constant/plan rate, `Applies To` Currency × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Actual Rate | Number | None | Currency, Time | *(import)* |
| Plan Rate | Number | None | Currency, Time | *(input — locked budget rate)* |

**`CAL110 Constant Currency`** — `Applies To` L3 Cost Centre × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Local Amount | Number | Sum | L3 Cost Centre, Time | *(from source)* |
| Reported (USD) | Number | Sum | L3 Cost Centre, Time | `Local Amount × Actual Rate` |
| Constant Ccy (USD) | Number | Sum | L3 Cost Centre, Time | `Local Amount × Plan Rate` |
| FX Effect | Number | Sum | L3 Cost Centre, Time | `Reported (USD) - Constant Ccy (USD)` |

(Rates pulled via the cost centre's local currency — see [currency-conversion](currency-conversion.md).)

## Formula(s)

Convert the same local amount twice:

```
// CAL110 -> Reported (USD)
Local Amount * INP40 FX Rates.Actual Rate[LOOKUP: SYS02 Organization Details.Local Currency]

// CAL110 -> Constant Ccy (USD)
Local Amount * INP40 FX Rates.Plan Rate[LOOKUP: SYS02 Organization Details.Local Currency]
```

Isolate the FX movement:

```
// CAL110 -> FX Effect
Reported (USD) - Constant Ccy (USD)
```

Constant-currency growth (compare CC this year to reported PY, or CC-on-CC depending on your definition):

```
// CC growth vs PY
IF LAG(Reported (USD), 12, 0) = 0 THEN 0
ELSE (Constant Ccy (USD) - LAG(Reported (USD), 12, 0)) / LAG(Reported (USD), 12, 0)
```

## Pitfalls / gotchas

- **Pin down the definition.** "Constant currency" can mean restate-at-PY-rate or restate-at-budget-rate. Agree which with Finance before building — they give different numbers.
- **Same local base.** Both conversions must start from the *identical* local amount, or the FX effect is contaminated by other changes.
- **Plan rate must be frozen.** If the "constant" rate moves, it isn't constant. Hold it as a locked input, ideally a version or a protected line item.
- Restating a **balance sheet** at constant rate also needs the closing-rate convention; don't apply average rates to positions.
- Keep `FX Effect` as a **separate** line so a variance bridge can pick it up cleanly — see [variance-waterfall-bridge](variance-waterfall-bridge.md).

## Performance & PLANS notes

- Reusing one rate table with multiple rate types (actual, plan, closing) is **Necessary** + **Sustainable**.
- Two `LOOKUP` conversions and a subtraction — cheap and fully **Auditable**.
- Feeds directly into FX-vs-operational variance analysis.

## Related

- [`docs/02-formulas/lookup-and-mapping.md`](../../docs/02-formulas/lookup-and-mapping.md)
- Recipes: [currency-conversion](currency-conversion.md) · [variance-waterfall-bridge](variance-waterfall-bridge.md) · [prior-year-comparison](../time-and-forecasting/prior-year-comparison.md)
