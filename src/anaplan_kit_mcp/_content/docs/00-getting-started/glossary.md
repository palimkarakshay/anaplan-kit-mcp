# Glossary

> **Level:** L1 · **Area:** Getting Started

Plain-English definitions of the core terms you'll meet everywhere in Anaplan and in this kit. Don't
memorise it — skim it now, then come back when a word stops making sense. The **Covered in** column
links to the page that explains the term in depth.

| Term | One-sentence definition | Covered in |
| --- | --- | --- |
| **Action** | A saved, repeatable operation — an import, export, delete, or open-dashboard — that a user or process can run with one click. | [Integration](../04-integration/) |
| **ALM** | *Application Lifecycle Management* — Anaplan's process for promoting structural changes safely from a development model to test and production. | [ALM](../06-security-alm/alm.md) |
| **Applies To** | The set of dimensions a line item (or whole module) is built across; it defines the grid each cell sits in. | [Dimensions](../01-fundamentals/dimensions.md) |
| **Blueprint** | The design/edit view of a module showing each line item's Format, Summary, Applies To and Formula — the grid this kit uses to describe modules. | [Modules](../01-fundamentals/modules.md) |
| **Cell count** | The number of cells a module holds — the product of its dimension sizes × its line items — and the master number that drives model size and performance. | [Sparsity & cell count](../07-performance/sparsity-and-engine.md) |
| **Composite list** | A multi-level list whose members have parent/child relationships, forming a hierarchy (e.g. Region › Country › Cost Centre). | [Lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md) |
| **Current period** | The single time period Anaplan treats as "now", used by time functions and often driven from a system module. | [Time](../01-fundamentals/time.md) |
| **Dashboard / Page** | The user-facing screen built from grids, charts and inputs; "dashboards" are the classic UX, "pages"/"boards"/"worksheets" the New UX. | [UX](../05-ux/) |
| **Data hub** | A dedicated model that holds shared, governed source data and feeds it to spoke models — a single source of truth. | [Integration](../04-integration/) |
| **DCA** | *Dynamic Cell Access* — driver-based control of whether each cell is read-only, writable or hidden, set by Boolean line items rather than fixed roles. | [Dynamic cell access](../06-security-alm/dynamic-cell-access.md) |
| **Dimension** | A list, Time, or Versions used to size a module; the number of cells is the product of all dimensions × line items. | [Dimensions](../01-fundamentals/dimensions.md) |
| **Format** | The data type of a line item — Number, Boolean, Text, List, Date, Time Period, or No Data — which determines what it can hold and how it calculates. | [Line items & formats](../01-fundamentals/line-items-and-formats.md) |
| **Hierarchy** | The parent/child structure of a composite list, enabling roll-ups (a Country totals its Cost Centres). | [Lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md) |
| **Line item** | A single measure or calculation inside a module (e.g. `Revenue`, `Growth %`), with its own format, summary and formula. | [Line items & formats](../01-fundamentals/line-items-and-formats.md) |
| **Line item subset** | A special list made from selected line items across modules, letting you treat measures as a dimension (use sparingly — performance-sensitive). | [Numbered lists & subsets](../01-fundamentals/numbered-lists-and-subsets.md) |
| **List** | The set of things you plan by — products, cost centres, regions, employees; the building block of every dimension. | [Lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md) |
| **List member** | A single entry in a list (e.g. "France" in a Country list); also called a list item. | [Lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md) |
| **Mapping** | A System-module relationship that links one list to another (e.g. Cost Centre → Region), used by `SUM`/`LOOKUP` instead of hard-coding. | [Modules](../01-fundamentals/modules.md), [DISCO](../03-methodology/disco.md) |
| **Model** | A single connected-planning application with its own lists, modules, time, versions, security and UX — your workbench. | [Platform architecture](platform-architecture.md) |
| **Module** | A multi-dimensional grid of line items built across one or more dimensions; the place all numbers and calculations live. | [Modules](../01-fundamentals/modules.md) |
| **Numbered list** | A list whose members are identified by an internal number rather than a unique name, used for transactional/high-volume data with no natural unique key. | [Numbered lists & subsets](../01-fundamentals/numbered-lists-and-subsets.md) |
| **Process** | An ordered bundle of actions run as one unit (e.g. import → calculate → export). | [Integration](../04-integration/) |
| **Property** | An attribute attached to list members (e.g. a Cost Centre's owner or code); often migrated into System modules for flexibility. | [Lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md) |
| **Saved view** | A stored arrangement of a module (filtered, pivoted, hidden line items) used as a source for imports/exports or as a dashboard grid. | [Modules](../01-fundamentals/modules.md), [Integration](../04-integration/) |
| **Selective access** | List-level security that restricts which list members a user can see and edit, applied per role. | [Security & ALM](../06-security-alm/) |
| **Subset** | A flagged portion of a list (a sub-selection of its members) you can use as a smaller dimension. | [Numbered lists & subsets](../01-fundamentals/numbered-lists-and-subsets.md) |
| **Subsidiary view** | A line item dimensioned differently from its parent module, so it isn't sized by every module dimension. | [Modules](../01-fundamentals/modules.md), [Dimensions](../01-fundamentals/dimensions.md) |
| **Summary method** | The rule for how a line item rolls up across hierarchy/time (Sum, Average, Min, Max, Formula, Ratio, None, or a Boolean option). | [Line items & formats](../01-fundamentals/line-items-and-formats.md) |
| **Switchover** | A version setting that marks the period where a version stops using Actuals and starts using planned (Forecast) values — the boundary between actual and forecast data. | [Versions](../01-fundamentals/versions.md) |
| **Time** | Anaplan's built-in calendar dimension (years down to days), configured once per model in Time Settings. | [Time](../01-fundamentals/time.md) |
| **Time range** | A named, custom span of periods you apply to a module so it stores only the periods it needs (a key performance lever). | [Time ranges](../07-performance/time-ranges.md) |
| **Top-level item** | The single roll-up member of a list that totals every member, used for grand totals and as a default LHS in formulas. | [Lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md) |
| **Version** | A built-in dimension for planning scenarios — Actual, Budget, Forecast — with features like switchover and formula scope. | [Versions](../01-fundamentals/versions.md) |
| **Workspace** | A licensed container with a fixed memory allowance that holds related models. | [Platform architecture](platform-architecture.md) |

---

**Related:** [Getting started index](README.md) · [Platform architecture](platform-architecture.md) ·
[Fundamentals](../01-fundamentals/)

> Source: Anaplan platform documentation (Anapedia, `help.anaplan.com`). See [`SOURCES.md`](../../SOURCES.md).
