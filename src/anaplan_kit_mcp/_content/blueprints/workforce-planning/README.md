# Workforce Planning — Blueprint

> **Level:** L2 · **Area:** Blueprint (Workforce) · **DISCO:** mixed

Plans **headcount, FTE and fully-loaded labour cost** by Cost Centre and role, including
**hire-date proration** (a new joiner mid-month costs only part of the month). Its
**fully-loaded cost** feeds the FP&A model's `Salaries` opex line.

---

## What this model does

1. **Existing employees** are loaded; **planned hires** (open positions) are entered (Data + Inputs).
2. Each position has a **start date**, **FTE**, **annual salary** and a **load %** (employer taxes,
   benefits).
3. The engine **prorates** salary by the fraction of each month the position is active — the
   signature calculation.
4. Salary + load = **fully-loaded cost**; converted to **USD** and rolled up the org.
5. Headcount and FTE are summed per Cost Centre × month for reporting.

---

## Which `_common` lists it reuses

| Shared structure | From | Used as |
| --- | --- | --- |
| **Time** + `SYS01 Time Settings` | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | monthly cost phasing; `Period Start/End Date` and `Days in Period` drive proration |
| **Versions** | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | Budget headcount vs Forecast |
| **L3 Cost Centre/Entity** + `SYS02 Organization Details` | [`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md) | where each position sits; supplies `Local Currency` |
| **Currency** + `SYS04 Exchange Rates` | [`_common/common-lists.md`](../_common/common-lists.md) | local salary → USD |
| **L3 P&L Account** | [`_common/common-lists.md`](../_common/common-lists.md) | `Salaries` account the cost feeds |

Domain-specific lists (Employee/Position, Job Grade) live in [`lists.md`](lists.md).

---

## Architecture sketch (data flow)

```
  Data            Inputs              System              Calculations          Outputs
  ----            ------              ------              ------------          -------
  DAT01     ┐     INP01 Planned       SYS01 Time   ┐
  Current   │     Hires        ┐      SYS30 Position │     CAL01 Active     ┐
  Roster     ├──► INP02 Comp     ├──►  Details        ├──► Proration         ├─► OUT01 HC
            │     Assumptions    │     SYS04 FX       ┘     CAL02 Salary      │   & Cost
            ┘                    ┘                          Cost              │
                                                            CAL03 Loaded Cost │
                                                            CAL04 Cost USD ───┘─► (feeds FP&A Salaries)
```

- One direction: Data/Inputs + System → Calculations → Outputs. *(Logical)*
- Positions live on a list dimensioned by `L3 Cost Centre/Entity` via `SYS30`, so cost rolls to the
  same Country/Region totals as every other domain. *(Logical)*

### Hand-off to FP&A (model-to-model import)

Workforce and FP&A are **separate models**, so the feed is a scheduled **model-to-model import**, not a
live formula. `CAL04 Cost in USD.Cost by CC (local)` (grain **L3 Cost Centre × Time × Versions**) imports
into FP&A's `INP02 Opex Plan.Opex (local)`, with the import pinning the **`Opex Category` dimension to the
fixed member `"Salaries"`** (Workforce carries no Opex Category, so every row maps to that one member).
This reconciles the grains: Workforce L3 Cost Centre × Time × Versions → INP02 L3 Cost Centre × **Salaries**
× Time × Versions. The feed is sent in **local** currency so FP&A applies FX once. Workforce replaces a typed
Salaries number with a driver-based one. See [`formulas.md`](formulas.md) §5 and
[fpa-pl-planning/modules.md](../fpa-pl-planning/modules.md).

---

**Related:** [`lists.md`](lists.md) · [`modules.md`](modules.md) · [`formulas.md`](formulas.md) ·
[`_common` backbone](../_common/README.md) · [FP&A blueprint](../fpa-pl-planning/README.md) ·
[DISCO](../../docs/03-methodology/disco.md)
