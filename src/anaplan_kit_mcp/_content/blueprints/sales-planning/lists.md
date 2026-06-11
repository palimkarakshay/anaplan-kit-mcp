# Sales Planning — Lists

> **Level:** L2 · **Area:** Blueprint (Sales) · **DISCO:** System (structure)

Sales layers a **rep / territory / opportunity** set on top of the shared backbone. It reuses the
org, product, currency and time dimensions rather than inventing its own.

---

## Reused from `_common` (do not redefine)

| List | Type | From | Role in this model |
| --- | --- | --- | --- |
| **Time** (native) | — | [`time-and-versions`](../_common/time-and-versions.md) | target & pipeline phasing |
| **Versions** (native) | — | [`time-and-versions`](../_common/time-and-versions.md) | quota (Budget) vs latest call (Forecast) |
| **L3 Cost Centre/Entity** | hierarchy | [`organization-hierarchy`](../_common/organization-hierarchy.md) | each rep's home entity; roll-up axis |
| **Currency** | flat | [`common-lists`](../_common/common-lists.md) | local target currency |
| **L2 Product** | hierarchy | [`common-lists`](../_common/common-lists.md) | product axis of targets & pipeline |
| **L3 P&L Account** | hierarchy | [`common-lists`](../_common/common-lists.md) | `Product Revenue` account the target feeds |

---

## Lists added by this domain

| List name | Type | Parent | Sample members | Notes |
| --- | --- | --- | --- | --- |
| **Territory** | hierarchy (top) | — | `EMEA Enterprise`, `Americas Enterprise`, `APAC Mid-Market` | The top-down target grain; maps to a Region in `_common`. |
| **Sales Rep** | hierarchy (leaf) | Territory | `R-Alice`, `R-Bjorn`, `R-Chen`, `R-Diego` | The bottom-up grain; each rep maps to a `Cost Centre`. |
| **Sales Stage** | flat | — | `Lead`, `Qualified`, `Proposal`, `Negotiation`, `Closed Won`, `Closed Lost` | Pipeline funnel; each carries a win-probability in `SYS11`. |
| **Opportunity** | **numbered** | — | `#100481`, `#100482`, … (transactional) | Large, churning deal list — numbered so it never bloats planning grids. *(Performance)* |

> **Why numbered for Opportunity?** Pipeline rows are many, transactional and short-lived — exactly
> the case for a numbered list (see [tutorial Step 1](../../tutorials/01-set-up-model-and-lists.md)).
> Territory/Rep/Stage are small and stable → standard lists.

---

## Mapping into the org backbone

Each rep belongs to a **Cost Centre** so sales numbers consolidate with FP&A:

```
Sales Rep ──(SYS10 Rep Details.Cost Centre)──► L3 Cost Centre/Entity ──► Country ──► Region
```

The Territory hierarchy is a *sales-view* roll-up; the org hierarchy is the *finance-view* roll-up.
A rep sits in both — that's how a territory target reconciles to a Region P&L. *(Logical)*

---

**Related:** [`modules.md`](modules.md) · [`formulas.md`](formulas.md) ·
[`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md) ·
[`_common/common-lists.md`](../_common/common-lists.md)
