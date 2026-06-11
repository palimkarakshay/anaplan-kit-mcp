# Workforce Planning — Lists

> **Level:** L2 · **Area:** Blueprint (Workforce) · **DISCO:** System (structure)

Workforce adds a **position / employee** list and a **job grade** reference, layered on the shared
org, currency and time backbone.

---

## Reused from `_common` (do not redefine)

| List | Type | From | Role in this model |
| --- | --- | --- | --- |
| **Time** (native) | — | [`time-and-versions`](../_common/time-and-versions.md) | monthly cost phasing; dates drive proration |
| **Versions** (native) | — | [`time-and-versions`](../_common/time-and-versions.md) | Budget headcount vs Forecast |
| **L3 Cost Centre/Entity** | hierarchy | [`organization-hierarchy`](../_common/organization-hierarchy.md) | where each position sits; roll-up axis |
| **Currency** | flat | [`common-lists`](../_common/common-lists.md) | local salary currency |
| **L3 P&L Account** | hierarchy | [`common-lists`](../_common/common-lists.md) | `Salaries` account the cost feeds |

---

## Lists added by this domain

| List name | Type | Parent | Sample members | Notes |
| --- | --- | --- | --- | --- |
| **Position** | **numbered** | — | `#P0001` (filled), `#P0002` (filled), `#P0100` (open hire), … | One row per seat — filled *or* planned/open. Numbered because the set is large and churns (hires, leavers, reqs). *(Performance)* |
| **Job Grade** | flat | — | `G1 Analyst`, `G2 Senior`, `G3 Manager`, `G4 Director` | Reference for default salary bands & load %. |

> **Why one Position list for both employees and open reqs?** A planned hire is just a position with
> a future start date and no name yet. Modelling both on one list means the proration math is
> identical for everyone — no parallel logic. *(Necessary, Sustainable)*

---

## Mapping into the org backbone

Each position carries its Cost Centre as an attribute in `SYS30`, so labour cost consolidates with
FP&A and every other domain:

```
Position ──(SYS30 Position Details.Cost Centre)──► L3 Cost Centre/Entity ──► Country ──► Region
Position ──(SYS30 Position Details.Job Grade)────► Job Grade  (default comp)
```

---

**Related:** [`modules.md`](modules.md) · [`formulas.md`](formulas.md) ·
[`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md) ·
[`_common/common-lists.md`](../_common/common-lists.md)
