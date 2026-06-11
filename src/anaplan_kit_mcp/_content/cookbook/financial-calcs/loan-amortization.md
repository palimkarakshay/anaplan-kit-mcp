# Loan amortization schedule (PMT / CUMIPMT)

> **Level:** L2 · **Area:** Financial Calcs · **PLANS:** Logical, Auditable · **DISCO:** Calculations

## The ask

"We're modelling a £1m term loan, 5% annual rate, 60 monthly payments. I need the level payment, and a schedule splitting each payment into interest and principal with the running balance."

## When you'll see this

- Debt schedules, lease liabilities, financing plans.
- Any "equal-instalment repayment" calculation.
- Cash-flow planning that needs interest vs principal split.

## Approach

Use Anaplan's built-in financial functions. **`PMT`** gives the level periodic payment; **`IPMT`/`PPMT`** split a single period into interest/principal; **`CUMIPMT`/`CUMPRINC`** give cumulative interest/principal between two periods. Keep loan terms in an Inputs module and the schedule in a Calc module dimensioned by the loan × Time.

Confirmed syntax (Anapedia):

- `PMT(Interest rate, Number of periods, Present value [, Future value] [, Timing])`
- `CUMIPMT(Interest rate, Number of periods, Principal, Start period, End period [, Timing])`

Use a **per-period** rate with a **per-period** count (monthly rate = annual / 12, periods = years × 12) — both must use the same time scale.

Why idiomatic:

- **Auditable (PLANS):** payment, interest, principal, balance are separate line items.
- Native financial functions beat a hand-rolled recursive balance formula for clarity and correctness.

## Blueprint

**`INP60 Loan Terms`** — `Applies To` Loan:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Principal | Number | None | Loan | *(input, e.g. 1,000,000)* |
| Annual Rate | Number (%) | None | Loan | *(input, e.g. 5%)* |
| Term (months) | Number | None | Loan | *(input, e.g. 60)* |
| Monthly Rate | Number | None | Loan | `Annual Rate / 12` |
| Level Payment | Number | None | Loan | `PMT(Monthly Rate, Term (months), -Principal)` |

**`CAL130 Amortization`** — `Applies To` Loan × Time (monthly):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Period Number | Number | None | Loan, Time | months since drawdown (1..Term) |
| Active? | Boolean | None | Loan, Time | `Period Number >= 1 AND Period Number <= INP60.Term (months)` |
| Opening Balance | Number | None | Loan, Time | `LAG(Closing Balance, 1, INP60.Principal)` |
| Interest | Number | Sum | Loan, Time | `IF Active? THEN Opening Balance × INP60.Monthly Rate ELSE 0` |
| Payment | Number | Sum | Loan, Time | `IF Active? THEN INP60.Level Payment ELSE 0` |
| Principal Repaid | Number | Sum | Loan, Time | `Payment - Interest` |
| Closing Balance | Number | None | Loan, Time | `Opening Balance - Principal Repaid` |

## Formula(s)

Level payment (PV negative so the payment comes out positive; same time scale on rate and periods):

```
// INP60 Loan Terms -> Level Payment
PMT(Monthly Rate, Term (months), -Principal)
```

Per-period interest and principal — either via the balance roll-forward (shown in the blueprint) or directly with `IPMT`/`PPMT`. The roll-forward is the most auditable:

```
// CAL130 -> Opening Balance
LAG(Closing Balance, 1, INP60 Loan Terms.Principal)

// CAL130 -> Interest
IF Active? THEN Opening Balance * INP60 Loan Terms.Monthly Rate ELSE 0

// CAL130 -> Principal Repaid
Payment - Interest

// CAL130 -> Closing Balance
Opening Balance - Principal Repaid
```

Cumulative interest paid across the whole life (cross-check):

```
CUMIPMT(Monthly Rate, Term (months), Principal, 1, Term (months))
```

## Pitfalls / gotchas

- **Rate / period scale must match.** Monthly payments → monthly rate (`Annual / 12`) and term in months. Mixing annual rate with monthly periods is the #1 error.
- **Sign convention.** Anaplan financial functions treat money-in as positive and money-out as negative. Negate `Principal` (or `PMT`'s result) so the schedule reads naturally; check the cross-cast.
- **The roll-forward needs a previous-period reference** (`LAG(..., 1, Principal)`) so the first month opens at the full principal.
- **Closing balance should hit ~0** at the final payment; rounding can leave pennies — plug the final principal repayment if exactness is required.
- Keep payments **only within `Active?`** months, or interest accrues forever on a zero balance.

## Performance & PLANS notes

- Native `PMT`/`IPMT`/`CUMIPMT` are exact and **Auditable** — don't hand-build the geometric-series formula.
- The balance roll-forward uses `LAG(...,1,...)`, a cheap one-period shift; stepped line items keep it readable.
- Dimension by a small `Loan` list × Time only — don't over-dimension (**Performance**).

## Related

- [`docs/02-formulas/financial-functions.md`](../../docs/02-formulas/financial-functions.md)
- Recipes: [straight-line-depreciation](straight-line-depreciation.md) · [prior-year-comparison](../time-and-forecasting/prior-year-comparison.md)
