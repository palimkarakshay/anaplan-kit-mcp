# Supply Chain — Lists

> **Level:** L2 · **Area:** Blueprint (Supply Chain) · **DISCO:** System (structure)

Supply Chain plans at a finer grain than the rest of the kit: **SKU** (a child of the shared
Product) × **Location**. It reuses the backbone for Product, Org and Time.

---

## Reused from `_common` (do not redefine)

| List | Type | From | Role in this model |
| --- | --- | --- | --- |
| **Time** (native) | — | [`time-and-versions`](../_common/time-and-versions.md) | monthly buckets; `Days in Period` for coverage |
| **Versions** (native) | — | [`time-and-versions`](../_common/time-and-versions.md) | Budget plan vs Forecast demand |
| **L1 Product Family › L2 Product** | hierarchy | [`common-lists`](../_common/common-lists.md) | SKU rolls up into `L2 Product` (shared revenue grain) |
| **L3 Cost Centre/Entity** | hierarchy | [`organization-hierarchy`](../_common/organization-hierarchy.md) | Location → Cost Centre for cost roll-up |
| **L3 P&L Account** | hierarchy | [`common-lists`](../_common/common-lists.md) | `Direct Materials` account the supply cost feeds |

---

## Lists added by this domain

| List name | Type | Parent | Sample members | Notes |
| --- | --- | --- | --- | --- |
| **SKU** | hierarchy (leaf) | **L2 Product** *(common)* | `SKU-A1`, `SKU-A2` (under Sensor A); `SKU-B1` (under Sensor B) | Extends the shared Product hierarchy **downward** — SKUs roll into the same Products FP&A/Sales plan. |
| **Location** | hierarchy (top) | — | `DC-UK`, `DC-DE`, `DC-US`, `Plant-IN` | Distribution centres / plants. Each maps to a Cost Centre via `SYS21`. |

> **Key design choice:** SKU is parented on the **shared `L2 Product`**, not a brand-new product
> list. So Supply Chain demand at SKU level aggregates straight into the Product totals that FP&A and
> Sales use — one product language across the tenant. *(Logical, Sustainable)*

---

## Mapping into the org backbone

```
SKU ──► L2 Product (common) ──► L1 Product Family (common)
Location ──(SYS21 Location Details.Cost Centre)──► L3 Cost Centre/Entity ──► Country ──► Region
```

The Location → Cost Centre map is what lets a warehouse's supply cost land on the right entity's
P&L. *(Logical)*

---

**Related:** [`modules.md`](modules.md) · [`formulas.md`](formulas.md) ·
[`_common/common-lists.md`](../_common/common-lists.md) (Product) ·
[`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md)
