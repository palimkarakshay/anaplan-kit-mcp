# FP&A P&L Planning — Lists

> **Level:** L2 · **Area:** Blueprint (FP&A) · **DISCO:** System (structure)

This model is built almost entirely on the **shared `_common` backbone** — that is the point of a
master plan. It adds only a couple of small domain lists of its own.

---

## Reused from `_common` (do not redefine)

| List | Type | From | Role in this model |
| --- | --- | --- | --- |
| **Time** (native) | — | [`time-and-versions`](../_common/time-and-versions.md) | monthly grain on every plan module |
| **Versions** (native) | — | [`time-and-versions`](../_common/time-and-versions.md) | Actual / Budget / Forecast |
| **L1 Region › L2 Country › L3 Cost Centre/Entity** | hierarchy | [`organization-hierarchy`](../_common/organization-hierarchy.md) | the entity each line belongs to |
| **Currency** | flat | [`common-lists`](../_common/common-lists.md) | local & group (USD) currencies |
| **L1 P&L Statement › L2 P&L Group › L3 P&L Account** | hierarchy | [`common-lists`](../_common/common-lists.md) | the chart of accounts — the P&L spine |
| **L1 Product Family › L2 Product** | hierarchy | [`common-lists`](../_common/common-lists.md) | revenue planning grain |

---

## Lists added by this domain

| List name | Type | Parent | Sample members | Notes |
| --- | --- | --- | --- | --- |
| **Revenue Driver** | flat | — | `Volume`, `Price` | Tags the two revenue assumptions; lets one input module hold both with a clean layout. (Same idea as `_common` *P&L Line Type*.) |
| **Opex Category** | flat | — | `Salaries`, `Travel`, `Marketing`, `IT`, `Other` | The opex lines planners type into; each maps 1:1 to an `L3 P&L Account` via a SYS mapping. |

> Both are **small, stable, human-meaningful** sets → standard (named) lists, not numbered lists.
> *(See [tutorial Step 1](../../tutorials/01-set-up-model-and-lists.md) on list-type choice.)*

---

## Mapping note (why no new hierarchy)

This model does **not** create its own region/account/product lists — doing so would duplicate the
backbone and break consolidation. Instead it **dimensions modules** by the shared leaf lists
(`L3 Cost Centre/Entity`, `L2 Product`, `L3 P&L Account`) and reads attributes from the shared
`SYS02 / SYS03 / SYS04` modules. *(Necessary, Sustainable — add a member once in `_common`,
it appears here automatically.)*

---

**Related:** [`modules.md`](modules.md) · [`formulas.md`](formulas.md) ·
[`_common/common-lists.md`](../_common/common-lists.md) ·
[`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md)
