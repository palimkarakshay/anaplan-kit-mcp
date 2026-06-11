# FP&A P&L Planning — Key Formulas

> **Level:** L2 · **Area:** Blueprint (FP&A) · **DISCO:** Calculations

The formulas that turn assumptions into a P&L, explained step by step. Each lives in its own line
item (see [`modules.md`](modules.md)) so a number can be traced end to end. *(Auditable)*

---

## 1. Revenue = Volume × Price

`CAL01 Revenue Calculation.Gross Revenue (local)`:

```
INP01 Revenue Assumptions.Volume * INP01 Revenue Assumptions.Price (local)
```

Both inputs share the same `CC × Product × Time × Versions` grid, so the multiply is element-wise —
no `LOOKUP` needed. This is the textbook *volume × price* driver.

---

## 2. COGS and Gross Profit (imported value with COGS % fallback)

`CAL02 Cost Calculation.COGS (local)` prefers the **bottom-up** figure imported from Supply Chain and
falls back to the ratio driver where no import exists:

```
IF ISNOTBLANK(INP04 Direct Materials (imported).Direct Materials (local))
   THEN INP04 Direct Materials (imported).Direct Materials (local)
   ELSE CAL01 Revenue Calculation.Gross Revenue (local) * INP03 Cost Drivers.COGS %
```

`COGS %` is dimensioned by Product only, so the fallback **broadcasts** across Cost Centre, Time and
Versions automatically. `Gross Profit (local) = Gross Revenue (local) - COGS (local)`.

> **Hand-off (Supply Chain → here):** `INP04 Direct Materials (local)` is **import-fed** from Supply Chain
> `CAL04 Supply Cost.Supply Cost by CC (local)` via a model-to-model import. Both sit at grain
> **L3 Cost Centre × L2 Product × Time × Versions**, matched on the shared `_common` lists, so the import is
> 1:1 with no remapping. This is what makes COGS *bottom-up* instead of a flat ratio. See
> [supply-chain/formulas.md](../supply-chain/formulas.md) §4 and [`modules.md`](modules.md) (INP04, CAL02).

---

## 3. Currency conversion (local → USD)

The entity's currency comes from `SYS02`, the rate from `SYS04`. `CAL03.FX Rate`:

```
SYS04 Exchange Rates.Rate (filled)[LOOKUP: SYS02 Organization Details.Local Currency]
```

- `LOOKUP` picks the row of `SYS04` whose `Currency` equals the cost centre's `Local Currency`.
- `Rate (filled)` already returns `1` for the group currency (USD), so USD entities pass through
  unchanged.

Then `Revenue (USD) = Gross Revenue (local) * FX Rate` (and likewise COGS, Opex). *(Sustainable — no
rate is ever written into a formula.)*

---

## 4. Building the P&L (map amounts onto accounts)

`CAL04 P&L Build.P&L Amount (USD)` collects each USD measure onto its `L3 P&L Account`. Because
revenue, COGS and opex sit on different grids, sum each onto the account dimension:

```
Revenue (USD)[SUM: revenue → Product Revenue account]
+ COGS (USD)[SUM: cost → Direct Materials account]
+ Opex (USD)[SUM: SYS05 Opex Account Map.P&L Account]
```

In practice you build this as **separate feed line items** (one per source) that each `SUM` onto the
P&L Account dimension, then add them — keeping each step auditable. The account **hierarchy** then
rolls leaves up to Revenue, Gross Profit, EBITDA and Net Profit **for free**.

> Sign handling: `SYS03 Account Details.Sign` (+1 revenue / −1 cost) lets you store everything as a
> positive amount and still get correct subtotals — multiply by `Sign` in the output if you prefer a
> "costs are negative" presentation. *(Auditable)*

---

## 5. The rolling Forecast (blend Actual + Plan)

`OUT01 P&L Statement.Forecast` is the living view: **Actuals where we have them, plan after**. It
keys off the shared time flag — never a named month:

```
IF SYS01 Time Settings.Is Actual?
   THEN CAL04 P&L Build.P&L Amount (USD)[SELECT: Versions.Actual]
   ELSE CAL04 P&L Build.P&L Amount (USD)[SELECT: Versions.Forecast]
```

Roll the model into a new year and the cut-over moves itself, because `Is Actual?` is defined once in
[`SYS01`](../_common/time-and-versions.md). *(Sustainable — this is the kit's signature rolling-forecast pattern.)*

---

## 6. Variance

```
Fcst vs Budget  = OUT01 P&L Statement.Forecast - OUT01 P&L Statement.Budget
Fcst vs Budget % = IF OUT01 P&L Statement.Budget = 0 THEN 0
                   ELSE Fcst vs Budget / OUT01 P&L Statement.Budget
```

Guard the divide-by-zero so empty accounts don't show errors. *(Auditable)*

---

## Consistency check (a number in one module feeds another)

```
INP01 Volume × Price ─► CAL01 Gross Revenue (local)
                         └─► CAL02 COGS (local) ─► Gross Profit (local)
INP04 Direct Materials (imported) ─► CAL02 COGS (local)  [used when present, else COGS %]
CAL01/CAL02 × FX ──────► CAL03 *(USD)  (Revenue (USD), COGS (USD), Opex (USD))
CAL03 + INP02 Opex ────► CAL04 P&L Amount (USD)
CAL04 ─────────────────► OUT01 P&L Statement ─► OUT02 Variance
```

Cross-domain (model-to-model imports, matched on shared `_common` dimensions):

- **Workforce** `Cost by CC (local)` → `INP02 Opex Plan.Opex (local)` at `Opex Category = "Salaries"`.
- **Supply Chain** `Supply Cost by CC (local)` → `INP04 Direct Materials (local)` → `CAL02` COGS.
- **Sales** `Target (USD)` reconciles against `CAL03 Currency Conversion.Revenue (USD)` (same grain).

---

**Related:** [`modules.md`](modules.md) · [`README.md`](README.md) ·
[`_common/time-and-versions.md`](../_common/time-and-versions.md) (`Is Actual?`) ·
[Formula reference](../../docs/02-formulas/) · [Tutorials](../../tutorials/)
