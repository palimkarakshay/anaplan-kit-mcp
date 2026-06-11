# FP&A P&L Planning — Blueprint

> **Level:** L2 · **Area:** Blueprint (FP&A) · **DISCO:** mixed

The **canonical** model of the kit — the one the [tutorials](../../tutorials/) build step by step. It
plans **revenue (volume × price)** and **cost**, converts local amounts to the group currency, and
rolls everything up to a **P&L** on the shared chart of accounts. It is the *master plan*: Sales,
Workforce and Supply Chain feed numbers **into** it.

---

## What this model does

1. Planners enter **volume** and **price** assumptions by Cost Centre × Product × Time (Inputs).
2. A calc engine derives **gross revenue**, then **COGS** — using a **bottom-up figure imported from
   Supply Chain** where available, else a **COGS %** driver — and computes **gross profit**.
3. **Opex** (salaries, travel, marketing, IT) is planned per Cost Centre; the **Salaries** category is
   **imported from Workforce** rather than typed.
4. Local amounts convert to **group currency (USD)** via the shared FX rates.
5. Every line maps to a **P&L Account**, so the result is a real Profit & Loss with subtotals
   (Revenue → Gross Profit → EBITDA → Net Profit).
6. A rolling **Forecast** blends Actuals-to-date with the plan using `SYS01.Is Actual?`.

---

## Which `_common` lists it reuses

| Shared structure | From | Used as |
| --- | --- | --- |
| **Time** + `SYS01 Time Settings` | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | every module is monthly; `Is Actual?` drives the rolling forecast |
| **Versions** (Actual / Budget / Forecast) | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | the scenario axis on all plan modules |
| **L3 Cost Centre/Entity** + `SYS02 Organization Details` | [`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md) | the entity each P&L line belongs to; supplies `Local Currency` |
| **Currency** + `SYS04 Exchange Rates` | [`_common/common-lists.md`](../_common/common-lists.md) | local → USD conversion |
| **L3 P&L Account** + `SYS03 Account Details` | [`_common/common-lists.md`](../_common/common-lists.md) | the chart of accounts the P&L rolls up to; this model **owns** it |
| **L2 Product** | [`_common/common-lists.md`](../_common/common-lists.md) | revenue planning grain |

Domain-specific lists added on top live in [`lists.md`](lists.md).

---

## Architecture sketch (data flow)

```
  Inputs                System                 Calculations              Outputs
  ------                ------                 ------------              -------
  INP01 Volume &  ┐     SYS01 Time      ┐
  Price            │    SYS02 Org        │
  INP02 Opex Plan  ├──► SYS03 Account    ├──►  CAL01 Revenue      ┐
  INP03 COGS %     │    SYS04 FX Rates   │     CAL02 Cost / COGS   ├──► OUT01 P&L
  INP04 Direct     ┘                     ┘     CAL03 FX Convert    │    Statement
  Materials (imp)                              CAL04 P&L Build     ┘    OUT02 Variance
        ▲
        │ model-to-model imports (matched on shared _common dimensions)
        ├── Workforce  Cost by CC (local) ───────► INP02 Opex Plan, Opex Category = "Salaries"
        ├── Supply Chain Supply Cost by CC (local) ► INP04 Direct Materials (local) ─► CAL02 COGS
        └── Sales      Target (USD) ──────────────► reconciled vs CAL03 Revenue (USD)
```

- **One direction**: Inputs + System → Calculations → Outputs. No circular references. *(Logical)*
- Each calc step is its **own line item** so a number can be traced from the P&L back to an
  assumption. *(Auditable)*

### How the other domains hand off into this model (model-to-model imports)

These are **separate models**. Each feed is a scheduled **model-to-model import** whose mapping joins on
the **shared `_common` dimensions** (so members line up with no remapping), not a live cross-model formula.

| Source line item (other model) | Target line item (here) | Mapping (matched dimensions) | P&L Account |
| --- | --- | --- | --- |
| Workforce `CAL04 Cost in USD.Cost by CC (local)` | `INP02 Opex Plan.Opex (local)` | `L3 Cost Centre/Entity`, `Time`, `Versions`; **`Opex Category` ← fixed `"Salaries"`** | `Salaries` |
| Supply Chain `CAL04 Supply Cost.Supply Cost by CC (local)` | `INP04 Direct Materials (imported).Direct Materials (local)` | `L3 Cost Centre/Entity`, `L2 Product`, `Time`, `Versions` (1:1) | `Direct Materials` |
| Sales `CAL04 Target in USD.Target (USD)` (`[SUM: Cost Centre]`) | reconciliation check vs `CAL03 Currency Conversion.Revenue (USD)` | `L3 Cost Centre/Entity`, `L2 Product`, `Time`, `Versions` (1:1) | `Product Revenue` |

`INP04` feeds `CAL02` COGS (imported value where present, `COGS %` fallback otherwise); the Salaries import
overwrites only the `Salaries` opex slice. See each domain's `formulas.md` for the exact hand-off line items.

---

**Related:** [`lists.md`](lists.md) · [`modules.md`](modules.md) · [`formulas.md`](formulas.md) ·
[`_common` backbone](../_common/README.md) · [Tutorials](../../tutorials/) ·
[DISCO](../../docs/03-methodology/disco.md)
