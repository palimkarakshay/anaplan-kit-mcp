# Workforce Planning — Modules

> **Level:** L2 · **Area:** Blueprint (Workforce) · **DISCO:** mixed

Blueprint tables, [DISCO](../../docs/03-methodology/disco.md)-tagged. Dimensions marked *(common)*
come from the [`_common` backbone](../_common/README.md). Positions are on the **numbered Position
list**.

---

## DAT01 Current Roster — **Data**

The HRIS export of filled positions, loaded as-is.

**Applies To:** Position

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Employee Name | Text | None | Position | import from HRIS |
| Cost Centre | List: L3 Cost Centre/Entity *(common)* | None | Position | import |
| Job Grade | List: Job Grade | None | Position | import |
| Start Date | Date | None | Position | import — hire date |
| End Date | Date | None | Position | import — blank if active (no planned leave) |
| FTE | Number | None | Position | import — 1.0 = full time, 0.5 = half |
| Annual Salary (local) | Number | None | Position | import |

---

## INP01 Planned Hires — **Inputs**

Open requisitions / planned headcount. Same shape as the roster, but typed by planners.

**Applies To:** Position

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Is Planned Hire? | Boolean | None | Position | input — distinguishes a req from a filled seat |
| Planned Start Date | Date | None | Position | input |
| Planned FTE | Number | None | Position | input |
| Planned Salary (local) | Number | None | Position | input — blank ⇒ use Job Grade default |

---

## INP02 Comp Assumptions — **Inputs**

Default bands and the employer load. Tuned each cycle.

**Applies To:** Job Grade

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Default Salary (local) | Number | None | Job Grade | input — band midpoint |
| Load % | Number (%) | None | Job Grade | input — employer taxes + benefits (e.g. 25%) |

---

## SYS30 Position Details — **System**

The single source of truth per position — resolves roster vs planned-hire into one set of
attributes. `SYS01`, `SYS02`, `SYS04` reused from `_common`.

**Applies To:** Position

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Cost Centre | List: L3 Cost Centre/Entity *(common)* | None | Position | `IF INP01 Planned Hires.Is Planned Hire? THEN <planned CC input> ELSE DAT01 Current Roster.Cost Centre` |
| Job Grade | List: Job Grade | None | Position | roster grade, or planned grade for a hire |
| Effective Start Date | Date | None | Position | `IF INP01 Planned Hires.Is Planned Hire? THEN INP01 Planned Hires.Planned Start Date ELSE DAT01 Current Roster.Start Date` |
| Effective End Date | Date | None | Position | `DAT01 Current Roster.End Date` (blank = no end) |
| Effective FTE | Number | None | Position | `IF INP01 Planned Hires.Is Planned Hire? THEN INP01 Planned Hires.Planned FTE ELSE DAT01 Current Roster.FTE` |
| Effective Salary (local) | Number | None | Position | see [`formulas.md`](formulas.md) — chosen salary or Job Grade default |

---

## CAL01 Active Proration — **Calculations**

The signature step: what fraction of each month is this position active? Uses shared date flags.

**Applies To:** Position × Time *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Active Days | Number | Sum | Position × Time | see [`formulas.md`](formulas.md) — overlap of [Start, End] with the month |
| Proration Factor | Number | None | Position × Time | `Active Days / SYS01 Time Settings.Days in Period` |
| Is Active This Month? | Boolean | None | Position × Time | `Active Days > 0` |

---

## CAL02 Salary Cost — **Calculations**

**Applies To:** Position × Time *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Monthly Salary (local) | Number | Sum | Position × Time | `SYS30 Position Details.Effective Salary (local) / 12 * SYS30 Position Details.Effective FTE * CAL01 Active Proration.Proration Factor` |

---

## CAL03 Fully-Loaded Cost — **Calculations**

Add the employer load.

**Applies To:** Position × Time *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Load Amount (local) | Number | Sum | Position × Time | `CAL02 Salary Cost.Monthly Salary (local) * INP02 Comp Assumptions.Load %[LOOKUP: SYS30 Position Details.Job Grade]` |
| Fully-Loaded Cost (local) | Number | Sum | Position × Time | `CAL02 Salary Cost.Monthly Salary (local) + Load Amount (local)` |

---

## CAL04 Cost in USD — **Calculations**

Convert and stage for the FP&A hand-off.

**Applies To:** Position × Time *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| FX Rate | Number (4 dp) | None | Position × Time × Versions | `SYS04 Exchange Rates.Rate (filled)[LOOKUP: SYS02 Organization Details.Local Currency[LOOKUP: SYS30 Position Details.Cost Centre]]` |
| Fully-Loaded Cost (USD) | Number | Sum | Position × Time × Versions | `CAL03 Fully-Loaded Cost.Fully-Loaded Cost (local) * FX Rate` |
| Cost by CC (local) | Number | Sum | L3 Cost Centre/Entity × Time × Versions | `CAL03 Fully-Loaded Cost.Fully-Loaded Cost (local)[SUM: SYS30 Position Details.Cost Centre]` |
| Cost by CC (USD) | Number | Sum | L3 Cost Centre/Entity × Time × Versions | `Fully-Loaded Cost (USD)[SUM: SYS30 Position Details.Cost Centre]` |

> **FP&A `Salaries` feed.** `Cost by CC (local)` (grain **L3 Cost Centre × Time × Versions**) is the line
> that lands in FP&A `INP02 Opex Plan.Opex (local)` against the **fixed member `Opex Category = "Salaries"`**
> via a model-to-model import. It is fed in **local currency** so FP&A applies FX **once** on its side
> (`CAL03 Currency Conversion.Opex (USD)`) — no double conversion. `Cost by CC (USD)` stays for this
> model's own USD reporting (`OUT01`). See the mapping in [`formulas.md`](formulas.md) §5 and the FP&A
> side in [`fpa-pl-planning/modules.md`](../fpa-pl-planning/modules.md) (INP02).

---

## OUT01 Headcount & Cost — **Outputs**

Reporting view; no new logic.

**Applies To:** L3 Cost Centre/Entity *(common)* × Time *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Headcount | Number | Sum | Cost Centre × Time | `CAL01 Active Proration.Is Active This Month?[SUM: SYS30 Position Details.Cost Centre]` *(count of active positions)* |
| FTE | Number | Sum | Cost Centre × Time | `(SYS30 Position Details.Effective FTE * CAL01 Active Proration.Proration Factor)[SUM: SYS30 Position Details.Cost Centre]` |
| Labour Cost (USD) | Number | Sum | Cost Centre × Time | `CAL04 Cost in USD.Cost by CC (USD)` |

---

**Related:** [`formulas.md`](formulas.md) · [`lists.md`](lists.md) ·
[`_common/time-and-versions.md`](../_common/time-and-versions.md) (dates & `Days in Period`) ·
[FP&A modules](../fpa-pl-planning/modules.md) · [Cookbook: hire-date proration](../../cookbook/)
