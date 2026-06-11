# `_common` — Organization Hierarchy

> **Level:** L2 · **Area:** Blueprint (shared backbone) · **DISCO:** System

The shared "who/where" axis: a composite list hierarchy **Region › Country › Cost Centre / Entity**.
Every domain plans *by* some leaf of this hierarchy and rolls *up* through it — so a Cost Centre cost,
a sales rep's territory and a headcount all aggregate to the same Country and Region totals.

See [Lists & hierarchies](../../docs/01-fundamentals/lists-and-hierarchies.md).

---

## The composite list (hierarchy)

A **composite list** is several lists stacked so each member has a parent in the level above. Build
top-down: Region first, then Country (parent = Region), then Cost Centre/Entity (parent = Country).

| List name | Type | Parent | Sample members | Notes |
| --- | --- | --- | --- | --- |
| **L1 Region** | hierarchy (top) | — | `EMEA`, `Americas`, `APAC` | Top roll-up; reporting regions. |
| **L2 Country** | hierarchy | Region | `UK`, `Germany`, `USA`, `India` | Holds the local **currency** (property). |
| **L3 Cost Centre/Entity** | hierarchy (leaf) | Country | `CC-1100 UK Sales`, `CC-1200 UK Ops`, `CC-3100 US Sales`, `CC-4100 India R&D` | The planning grain — where revenue, cost and headcount land. |

> The **leaf** (`L3 Cost Centre/Entity`) is what modules are usually dimensioned by. Roll-ups to
> Country and Region are automatic once the hierarchy is built — never sum them with formulas.
> *(Necessary, Performance)*

---

## `SYS02 Organization Details` — the org attributes module

A **System** module dimensioned by the **leaf** list, holding each cost centre's attributes and
mappings: its local currency, its entity type, whether it's in the current plan. Other modules read
these instead of hard-coding. *(Sustainable, Auditable)*

**Module:** `SYS02 Organization Details` · **DISCO: System** · **Applies To:** L3 Cost Centre/Entity

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Country | List: L2 Country | — | L3 Cost Centre/Entity | `PARENT(ITEM(L3 Cost Centre/Entity))` |
| Region | List: L1 Region | — | L3 Cost Centre/Entity | `PARENT(Country)` |
| Local Currency | List: Currency | — | L3 Cost Centre/Entity | `Country.Currency` *(property lookup; see [common-lists](common-lists.md))* |
| Entity Type | List: Entity Type | — | L3 Cost Centre/Entity | input *(Sales / Ops / R&D / Shared)* |
| Is Active? | Boolean | — | L3 Cost Centre/Entity | input — include in plan rollups |
| Cost Centre Manager | Text | — | L3 Cost Centre/Entity | input |

---

## How domains reuse the Organization hierarchy

| Domain | Reuses it as | Example |
| --- | --- | --- |
| **FP&A P&L** | the entity each P&L line belongs to | revenue & cost are dimensioned by `L3 Cost Centre/Entity`. |
| **Sales** | each rep's home cost centre / territory roll-up | `SYS Sales Rep Details.Cost Centre` maps a rep into the org. |
| **Workforce** | where each employee / position sits | headcount cost lands on a Cost Centre, then rolls to Country. |
| **Supply Chain** | the entity owning a Location | a DC/plant Location maps to a Cost Centre for cost roll-up. |

Because all four point at the **same leaf list**, their numbers aggregate to identical Country and
Region totals — the FP&A P&L can consolidate them without reconciliation. *(Logical)*

> Currency conversion uses `SYS02 Organization Details.Local Currency` together with
> [`SYS04 Exchange Rates`](common-lists.md) — local amounts convert to the group currency on the way up.

---

**Related:** [`common-lists.md`](common-lists.md) (Currency & accounts) ·
[`time-and-versions.md`](time-and-versions.md) ·
[Lists & hierarchies](../../docs/01-fundamentals/lists-and-hierarchies.md) ·
[FP&A modules](../fpa-pl-planning/modules.md)
