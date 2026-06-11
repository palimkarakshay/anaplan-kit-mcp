# Variance waterfall / bridge

> **Level:** L2 · **Area:** Financial Calcs · **PLANS:** Logical, Auditable · **DISCO:** Calculations / Outputs

## The ask

"Build me the bridge from Budget revenue to Actual revenue — show how much of the gap is volume, how much is price, and how much is FX, as a waterfall."

## When you'll see this

- Budget-to-actual or PY-to-CY variance explained as a waterfall.
- Decomposing a total movement into named effects (volume, price, mix, FX).
- The classic "bridge" chart: start bar, +/- step bars, end bar.

## Approach

A bridge is two things: (1) the **named effect amounts** that decompose the total variance, and (2) a small **Outputs** module shaped so a waterfall chart can render the steps (a category list of bridge steps with one value per step). Compute the effects in a Calc module, then arrange them against a `Bridge Steps` list for the chart.

```
Budget  +  Volume effect  +  Price effect  +  FX effect  =  Actual
```

Decompose with the standard sequential method (hold others at base while flexing one driver):

- **Volume effect** = (Act Volume − Bud Volume) × Bud Price
- **Price effect**  = (Act Price − Bud Price) × Act Volume
- **FX effect**     = constant-currency vs reported difference (see [fx-restatement](fx-restatement.md))

Why idiomatic:

- **Auditable (PLANS):** each effect is its own line item; the effects must sum to the total variance — a built-in check.
- **Logical:** the Outputs module just *arranges* numbers for the chart; no business logic there.

## Blueprint

**List `Bridge Steps`:** `Budget`, `Volume`, `Price`, `FX`, `Actual` (ordered for the chart).

**`CAL140 Variance Effects`** — `Applies To` Entity × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Volume Effect | Number | Sum | Entity, Time | `(Act Vol - Bud Vol) × Bud Price` |
| Price Effect | Number | Sum | Entity, Time | `(Act Price - Bud Price) × Act Vol` |
| FX Effect | Number | Sum | Entity, Time | from [fx-restatement](fx-restatement.md) |
| Total Variance | Number | Sum | Entity, Time | `Actual Revenue - Budget Revenue` |
| Unexplained | Number | Sum | Entity, Time | `Total Variance - Volume Effect - Price Effect - FX Effect` |

**`OUT10 Bridge`** — `Applies To` Bridge Steps × Entity × Time (the chart source):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Step Value | Number | Sum | Bridge Steps, Entity, Time | one value per step (see formula) |

## Formula(s)

The effect calculations (sequential decomposition):

```
// CAL140 -> Volume Effect
(Act Volume - Bud Volume) * Bud Price

// CAL140 -> Price Effect
(Act Price - Bud Price) * Act Volume
```

Shape the Outputs module per bridge step (map each step item to the right number):

```
// OUT10 Bridge -> Step Value
IF ITEM(Bridge Steps) = Bridge Steps.Budget THEN CAL140.Budget Revenue
ELSE IF ITEM(Bridge Steps) = Bridge Steps.Volume THEN CAL140.Volume Effect
ELSE IF ITEM(Bridge Steps) = Bridge Steps.Price  THEN CAL140.Price Effect
ELSE IF ITEM(Bridge Steps) = Bridge Steps.FX     THEN CAL140.FX Effect
ELSE CAL140.Actual Revenue
```

The audit check that must hold:

```
// CAL140 -> Unexplained   (should be 0)
Total Variance - Volume Effect - Price Effect - FX Effect
```

## Pitfalls / gotchas

- **Effects must reconcile to the total variance.** Keep an `Unexplained` line — if it isn't ~0, your decomposition is wrong or incomplete. This is non-negotiable on a bridge.
- **Decomposition order matters.** Volume-then-price vs price-then-volume puts the mix interaction in different buckets. Pick the convention Finance uses and state it.
- The `IF ITEM(...)` chain in `OUT10` is over the **small** `Bridge Steps` list — fine. Don't do this over a large list.
- A waterfall chart needs the steps **in order** — set the `Bridge Steps` list order deliberately (it drives the chart).
- Don't compute effects in the Outputs module; keep logic in `CAL140`, arrangement in `OUT10` (DISCO).

## Performance & PLANS notes

- Separating effects (Calc) from chart shaping (Output) is textbook **DISCO** and keeps logic Auditable.
- The reconciliation line (`Unexplained = 0`) is a free correctness test — see [reconciliation-check-module](../performance/reconciliation-check-module.md).
- Reuse `FX Effect` straight from [fx-restatement](fx-restatement.md) (**Necessary**).

## Related

- [`docs/03-methodology/disco.md`](../../docs/03-methodology/disco.md)
- Recipes: [fx-restatement](fx-restatement.md) · [prior-year-comparison](../time-and-forecasting/prior-year-comparison.md) · [reconciliation-check-module](../performance/reconciliation-check-module.md)
