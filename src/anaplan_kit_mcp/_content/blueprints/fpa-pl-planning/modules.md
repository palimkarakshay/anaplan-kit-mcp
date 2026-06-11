# FP&A P&L Planning — Modules

> **Level:** L2 · **Area:** Blueprint (FP&A) · **DISCO:** mixed (one of each type)

Each module below is a **blueprint table** (one row per line item) tagged with its
[DISCO](../../docs/03-methodology/disco.md) type and the [naming convention](../../templates/).
Dimensions in **Applies To** marked *(common)* come from the shared
[`_common` backbone](../_common/README.md).

---

## INP01 Revenue Assumptions — **Inputs**

What planners type. Volume and price by Cost Centre × Product × month × version.

**Applies To:** L3 Cost Centre/Entity *(common)* × L2 Product *(common)* × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Volume | Number | Sum | CC × Product × Time × Versions | input — units sold |
| Price (local) | Number (2 dp) | None | CC × Product × Time × Versions | input — unit price in entity's local currency |

---

## INP02 Opex Plan — **Inputs**

Operating-expense plan by Cost Centre × Opex Category. Most categories (Travel, Marketing, IT, Other) are
typed by planners; the **`Salaries` row is import-fed from the Workforce model**, not typed (see hand-off
below).

**Applies To:** L3 Cost Centre/Entity *(common)* × Opex Category × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Opex (local) | Number | Sum | CC × Opex Category × Time × Versions | input (typed) — **except `Opex Category = "Salaries"`, which is fed by a model-to-model import** (see note) |

> **Salaries hand-off (Workforce → here):** the `Opex Category = "Salaries"` slice of `Opex (local)` is
> populated by a model-to-model import from Workforce `CAL04 Cost in USD.Cost by CC (local)` (grain
> **L3 Cost Centre × Time × Versions**). The import pins the `Opex Category` dimension to the fixed member
> **`"Salaries"`**, so Workforce's grain expands to this module's grain cleanly. The figure arrives in
> **local** currency and is converted to USD once by `CAL03` (`Opex (USD)`). Planners leave the Salaries row
> read-only; all other categories are typed. See [`workforce-planning/formulas.md`](../workforce-planning/formulas.md) §5.

---

## INP03 Cost Drivers — **Inputs**

Cost ratios. Kept separate from `SYS` because planners *do* tune these each cycle.

**Applies To:** L2 Product *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| COGS % | Number (%) | None | L2 Product | input — direct cost as % of revenue (e.g. Hardware 60%, Software 15%) |

---

## INP04 Direct Materials (imported) — **Inputs**

The **receiving line for bottom-up COGS** fed from the Supply Chain model. Same grain as `CAL02` so the
two reconcile. Blank where Supply Chain has no plan for that Cost Centre × Product — `CAL02` then falls
back to the `COGS %` driver. **Import-fed, not typed** (see hand-off below).

**Applies To:** L3 Cost Centre/Entity *(common)* × L2 Product *(common)* × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Direct Materials (local) | Number | Sum | CC × Product × Time × Versions | **import** from Supply Chain `CAL04 Supply Cost.Supply Cost by CC (local)` — blank ⇒ use COGS % fallback |

---

## SYS modules (reused from `_common`)

This model does not build its own System modules — it **references** the shared ones:
[`SYS01 Time Settings`](../_common/time-and-versions.md), [`SYS02 Organization Details`](../_common/organization-hierarchy.md),
[`SYS03 Account Details`](../_common/common-lists.md), [`SYS04 Exchange Rates`](../_common/common-lists.md).
It adds **one** small local mapping:

### SYS05 Opex Account Map — **System**

Maps each Opex Category to its P&L Account so opex lands on the right P&L line. Built once.

**Applies To:** Opex Category

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| P&L Account | List: L3 P&L Account | None | Opex Category | input — e.g. `Salaries → Salaries`, `Travel → Travel` |

---

## CAL01 Revenue Calculation — **Calculations**

Volume × Price, in local currency. One step per line item. *(Auditable)*

**Applies To:** L3 Cost Centre/Entity *(common)* × L2 Product *(common)* × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Gross Revenue (local) | Number | Sum | CC × Product × Time × Versions | `INP01 Revenue Assumptions.Volume * INP01 Revenue Assumptions.Price (local)` |

---

## CAL02 Cost Calculation — **Calculations**

Direct cost (COGS): use the **imported** bottom-up figure from Supply Chain when present, else fall back to
revenue × the product's COGS %.

**Applies To:** L3 Cost Centre/Entity *(common)* × L2 Product *(common)* × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| COGS (local) | Number | Sum | CC × Product × Time × Versions | `IF ISNOTBLANK(INP04 Direct Materials (imported).Direct Materials (local)) THEN INP04 Direct Materials (imported).Direct Materials (local) ELSE CAL01 Revenue Calculation.Gross Revenue (local) * INP03 Cost Drivers.COGS %` |
| Gross Profit (local) | Number | Sum | CC × Product × Time × Versions | `CAL01 Revenue Calculation.Gross Revenue (local) - COGS (local)` |

> **Bottom-up COGS hand-off (Supply Chain → here):** `INP04 Direct Materials (local)` is fed by a
> model-to-model import from Supply Chain `CAL04 Supply Cost.Supply Cost by CC (local)` — both at grain
> **L3 Cost Centre × L2 Product × Time × Versions**, so the dimensions match member-for-member. Where the
> import leaves a cell blank, `COGS (local)` reverts to the `COGS %` driver. The local figure is converted
> to USD once by `CAL03` (`COGS (USD)`). See [`formulas.md`](formulas.md) §2 and
> [`supply-chain/modules.md`](../supply-chain/modules.md) (CAL04).

---

## CAL03 Currency Conversion — **Calculations**

Convert local amounts to **group currency (USD)** using the entity's `Local Currency` and the
shared FX rate. Never hard-code a rate. *(Sustainable)*

**Applies To:** L3 Cost Centre/Entity *(common)* × L2 Product *(common)* × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| FX Rate | Number (4 dp) | None | CC × Time × Versions | `SYS04 Exchange Rates.Rate (filled)[LOOKUP: SYS02 Organization Details.Local Currency]` |
| Revenue (USD) | Number | Sum | CC × Product × Time × Versions | `CAL01 Revenue Calculation.Gross Revenue (local) * FX Rate` |
| COGS (USD) | Number | Sum | CC × Product × Time × Versions | `CAL02 Cost Calculation.COGS (local) * FX Rate` |
| Opex (USD) | Number | Sum | CC × Opex Category × Time × Versions | `INP02 Opex Plan.Opex (local) * FX Rate` |

---

## CAL04 P&L Build — **Calculations**

Map every USD amount onto an `L3 P&L Account` so the natural hierarchy roll-up *is* the P&L.

**Applies To:** L3 Cost Centre/Entity *(common)* × L3 P&L Account *(common)* × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| P&L Amount (USD) | Number | Sum | CC × P&L Account × Time × Versions | revenue/COGS/opex summed onto their account — see [`formulas.md`](formulas.md) |

> Roll-up to `L2 P&L Group` → `L1 P&L Statement` is automatic from the account hierarchy. Subtotals
> like Gross Profit and EBITDA come for free. *(Necessary — never sum them by formula.)*

---

## OUT01 P&L Statement — **Outputs**

Reporting view. No new logic — selects and formats `CAL04` for a dashboard / export.

**Applies To:** L3 P&L Account *(common)* × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Actual | Number | Sum | P&L Account × Time | `CAL04 P&L Build.P&L Amount (USD)[SELECT: Versions.Actual]` |
| Budget | Number | Sum | P&L Account × Time | `CAL04 P&L Build.P&L Amount (USD)[SELECT: Versions.Budget]` |
| Forecast | Number | Sum | P&L Account × Time | rolling blend — see [`formulas.md`](formulas.md) |

---

## OUT02 Variance — **Outputs**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Fcst vs Budget | Number | Sum | P&L Account × Time | `OUT01 P&L Statement.Forecast - OUT01 P&L Statement.Budget` |
| Fcst vs Budget % | Number (%) | None | P&L Account × Time | `IF OUT01 P&L Statement.Budget = 0 THEN 0 ELSE Fcst vs Budget / OUT01 P&L Statement.Budget` |

---

**Related:** [`formulas.md`](formulas.md) · [`lists.md`](lists.md) ·
[`_common/common-lists.md`](../_common/common-lists.md) (FX & accounts) ·
[DISCO](../../docs/03-methodology/disco.md) · [Cookbook: currency conversion](../../cookbook/)
