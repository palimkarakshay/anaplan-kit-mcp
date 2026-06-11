# Blueprints — Worked Anaplan Models

> **Level:** L2 · **Area:** Blueprint (overview) · **DISCO:** all five module types

This folder holds **worked example models** — complete-enough sketches of real Anaplan models so a
brand-new builder can see how [lists](../docs/01-fundamentals/lists-and-hierarchies.md),
[modules](../docs/01-fundamentals/modules.md), [line items](../docs/01-fundamentals/line-items-and-formats.md)
and [formulas](../docs/02-formulas/) fit together. Nothing here runs — Anaplan is built in a browser
(see the [repo README](../README.md)) — these pages *describe and illustrate* a model the way you'd
design it on paper before building it.

---

## How to read a blueprint

Each domain has four files:

| File | What it shows |
| --- | --- |
| `README.md` | Overview, which shared `_common` lists it reuses, a text architecture sketch. |
| `lists.md` | The lists, as a table: **List name · Type (flat/hierarchy/numbered) · Parent · Sample members · Notes**. |
| `modules.md` | The modules, each as a **blueprint table** and tagged with a [DISCO](../docs/03-methodology/disco.md) type. |
| `formulas.md` | The key formulas, in Anaplan syntax, explained step by step. |

**Blueprint table** — the same grid you see in Anaplan's Blueprint view, one row per line item:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Example | Number | Sum | Product × Time | `Volume * Price` |

**Module naming** follows the DISCO prefix convention — `DAT` (Data), `INP` (Inputs), `SYS` (System),
`CAL` (Calculations), `OUT` (Outputs) — so the module type is obvious in any list. See
[DISCO](../docs/03-methodology/disco.md) and [PLANS](../docs/03-methodology/plans-standard.md).

---

## The shared `_common` backbone (the "common ground")

A real connected-planning tenant does **not** redefine Time, the org chart and the chart of accounts
once per model — it defines them **once** and every model reuses them. These blueprints do the same.

[`_common/`](_common/) holds the shared **dimensional backbone**:

| Shared structure | Defined in | Reused by |
| --- | --- | --- |
| **Time** (monthly, fiscal year) + `SYS01 Time Settings` flags | [`_common/time-and-versions.md`](_common/time-and-versions.md) | all four domains |
| **Versions** (Actual / Budget / Forecast) | [`_common/time-and-versions.md`](_common/time-and-versions.md) | all four domains |
| **Organization** `Region › Country › Cost Centre/Entity` + `SYS02 Organization Details` | [`_common/organization-hierarchy.md`](_common/organization-hierarchy.md) | FP&A, Sales, Workforce, Supply Chain |
| **Currency** + `SYS04 Exchange Rates` | [`_common/common-lists.md`](_common/common-lists.md) | FP&A, Sales, Workforce |
| **P&L Account** hierarchy | [`_common/common-lists.md`](_common/common-lists.md) | FP&A (Sales/Workforce feed it) |
| **Product** hierarchy | [`_common/common-lists.md`](_common/common-lists.md) | FP&A, Sales, Supply Chain |

> Why this matters (*Sustainable*): add a new month, a new country, or a new product **once** in
> `_common` and every domain inherits it with **no formula changes**. This is the structural meaning
> of "all domains, properly segregated, with common ground."

---

## Map of the four domains

```
                          _common backbone
        (Time · Versions · Organization · Currency · P&L Account · Product)
                                   │
        ┌──────────────┬───────────┴───────────┬────────────────┐
        ▼              ▼                         ▼                ▼
   FP&A P&L        Sales                   Supply Chain      Workforce
   Planning        Planning                                  Planning
   revenue +       quota / pipeline        demand →          headcount /
   cost → P&L      by rep & product        inventory/supply  FTE / salary
        ▲              │                         │                │
        │   Target(USD)│  Supply Cost by CC      │  Cost by CC    │
        │   reconcile  │  (local) → INP04        │  (local) →     │
        │   vs CAL03   │  Direct Materials       │  INP02 Salaries│
        │   Revenue    │  → CAL02 COGS           │                │
        │   (USD)      ▼                         ▼                ▼
        └──────────── model-to-model imports (matched on shared dimensions) ──┘
                       into the FP&A P&L (the master plan)
```

The cross-domain feeds are **real model-to-model imports**, each with a named source line item, a named
target line item, and a mapping that joins on the **shared `_common` dimensions** (so members line up with
no remapping). They are not live cross-model formulas — see the table below and each domain's `formulas.md`.

| Source (model.line item) | Target (FP&A.line item) | Matched dimensions |
| --- | --- | --- |
| Workforce `CAL04.Cost by CC (local)` | `INP02 Opex Plan.Opex (local)` | L3 Cost Centre · Time · Versions; `Opex Category` fixed to `"Salaries"` |
| Supply Chain `CAL04.Supply Cost by CC (local)` | `INP04 Direct Materials (imported).Direct Materials (local)` → `CAL02 COGS` | L3 Cost Centre · L2 Product · Time · Versions (1:1) |
| Sales `CAL04.Target (USD)` | reconciled vs `CAL03 Currency Conversion.Revenue (USD)` | L3 Cost Centre · L2 Product · Time · Versions (1:1) |

| Domain | What it plans | Folder |
| --- | --- | --- |
| **FP&A P&L Planning** | Revenue (volume × price) + cost planning rolling up to a P&L. The canonical model the [tutorials](../tutorials/) build. | [`fpa-pl-planning/`](fpa-pl-planning/) |
| **Sales Planning** | Territory / quota / pipeline; sales targets by rep & product. | [`sales-planning/`](sales-planning/) |
| **Supply Chain** | Demand forecast → inventory / supply; product × location. | [`supply-chain/`](supply-chain/) |
| **Workforce Planning** | Headcount plan, FTE, salary / cost with hire-date proration. | [`workforce-planning/`](workforce-planning/) |

The domains are **internally consistent**: because all four dimension on the shared `_common` lists, a
number produced in one model imports into another with its dimensions already aligned. Workforce's
`Cost by CC (local)` becomes FP&A's `Salaries` opex; Supply Chain's `Supply Cost by CC (local)` becomes
FP&A's `Direct Materials` COGS via `INP04`; Sales' `Target (USD)` reconciles against FP&A
`CAL03 Revenue (USD)`. Each is a concrete model-to-model import with a named mapping (see the table above
and each domain's `formulas.md`), not an unbacked arrow.

---

**Related:** [`_common/`](_common/) · [DISCO](../docs/03-methodology/disco.md) ·
[PLANS](../docs/03-methodology/plans-standard.md) · [Tutorials](../tutorials/) ·
[Fundamentals](../docs/01-fundamentals/)
