# Supply Chain — Blueprint

> **Level:** L2 · **Area:** Blueprint (Supply Chain) · **DISCO:** mixed

Turns a **demand forecast** into a **supply / inventory plan** at **Product × Location × Time**. It
computes how much to make/buy, projects inventory balances, and produces a unit **supply cost** that
can drive the FP&A model's COGS. This model works in **units**, not currency, until the final cost
step.

---

## What this model does

1. A **statistical / consensus demand** forecast is loaded and adjusted (Data + Inputs).
2. **Inventory policy** (safety stock, lead time, MOQ) is set per SKU × Location (Inputs).
3. The engine projects **opening → demand → required supply → closing inventory** month by month —
   a classic time-phased balance using `PREVIOUS()`.
4. **Coverage (days of supply)** and **stock-out flags** are derived.
5. Required supply × **standard unit cost** gives a **Supply Cost** that feeds FP&A COGS.

---

## Which `_common` lists it reuses

| Shared structure | From | Used as |
| --- | --- | --- |
| **Time** + `SYS01 Time Settings` | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | monthly buckets; `Days in Period` for days-of-supply; `Is Actual?` for actual vs planned demand |
| **Versions** | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | Budget plan vs Forecast demand |
| **L3 Cost Centre/Entity** + `SYS02 Organization Details` | [`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md) | each Location maps to a Cost Centre for cost roll-up |
| **L1 Product Family › L2 Product** | [`_common/common-lists.md`](../_common/common-lists.md) | demand grain (SKU is a child of Product) |
| **L3 P&L Account** | [`_common/common-lists.md`](../_common/common-lists.md) | `Direct Materials` account the Supply Cost feeds |

> **No Currency here.** Supply Chain plans in **units**. Cost becomes currency only at the FP&A
> hand-off, which applies FX once — avoiding double conversion. *(Necessary)*

Domain-specific lists (SKU, Location) live in [`lists.md`](lists.md).

---

## Architecture sketch (data flow)

```
  Data              Inputs              System            Calculations           Outputs
  ----              ------              ------            ------------           -------
  DAT01 Stat ┐      INP01 Demand        SYS01 Time
  Demand      │     Adjust       ┐      SYS20 SKU    ┐
              ├───► INP02 Inv      ├──►  Details      ├──► CAL01 Net Demand  ┐
  DAT02 On-   │     Policy         │     SYS21 Loc     │    CAL02 Inventory    ├─► OUT01 Supply
  Hand        ┘     INP03 Unit     ┘     Details       ┘    Projection         │   Plan
                    Cost                                     CAL03 Coverage     │
                                                             CAL04 Supply Cost ─┘─► (feeds FP&A COGS)
```

- One direction; `CAL02` is the only module with a time-dependency (`PREVIOUS()`), and it's
  acyclic across time. *(Logical, no circular reference.)*
- SKU × Location is the heavy grid — `SYS` flags and time ranges keep it lean. *(Performance)*

### Hand-off to FP&A (model-to-model import)

Supply Chain and FP&A are **separate models**, so the feed is a scheduled **model-to-model import**, not a
live formula. `CAL04 Supply Cost.Supply Cost by CC (local)` (grain **L3 Cost Centre × L2 Product × Time ×
Versions**) imports into FP&A's `INP04 Direct Materials (imported).Direct Materials (local)` at the **same
grain**, matched 1:1 on the shared `_common` lists. FP&A's `CAL02 COGS (local)` then uses the imported figure
where present and falls back to `Revenue × COGS %` otherwise — making COGS **bottom-up** for planned SKUs.
This is the `Direct Materials` branch of the P&L. See [`formulas.md`](formulas.md) §4 and
[fpa-pl-planning/modules.md](../fpa-pl-planning/modules.md).

---

**Related:** [`lists.md`](lists.md) · [`modules.md`](modules.md) · [`formulas.md`](formulas.md) ·
[`_common` backbone](../_common/README.md) · [FP&A blueprint](../fpa-pl-planning/README.md) ·
[DISCO](../../docs/03-methodology/disco.md)
