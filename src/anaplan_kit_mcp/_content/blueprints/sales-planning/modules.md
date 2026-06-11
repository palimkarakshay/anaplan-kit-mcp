# Sales Planning — Modules

> **Level:** L2 · **Area:** Blueprint (Sales) · **DISCO:** mixed

Blueprint tables, one row per line item, [DISCO](../../docs/03-methodology/disco.md)-tagged.
Dimensions marked *(common)* come from the [`_common` backbone](../_common/README.md).

---

## DAT01 Pipeline Load — **Data**

The raw CRM export. Flat and faithful — no calculation here. Dimensioned by the **numbered**
Opportunity list. *(Data, kept on a numbered list for performance.)*

**Applies To:** Opportunity

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Owner (Rep) | List: Sales Rep | None | Opportunity | import from CRM |
| Product | List: L2 Product *(common)* | None | Opportunity | import from CRM |
| Stage | List: Sales Stage | None | Opportunity | import from CRM |
| Close Month | List: Time *(common)* | None | Opportunity | import from CRM |
| Deal Value (local) | Number | Sum | Opportunity | import from CRM |

---

## INP01 Top-Down Target — **Inputs**

Leadership's number per Territory × Product × month. The plan starts here.

**Applies To:** Territory × L2 Product *(common)* × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Target (local) | Number | Sum | Territory × Product × Time × Versions | input — top-down revenue target |

---

## INP02 Rep Allocation Weight — **Inputs**

How the territory target splits across its reps (e.g. prior-year attainment share).

**Applies To:** Sales Rep × L2 Product *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Weight | Number | Sum | Sales Rep × Product | input — relative share (need not sum to 1; normalised in CAL01) |

---

## SYS10 Rep Details — **System**

Rep attributes & the mapping into the shared org. Built once.

**Applies To:** Sales Rep

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Territory | List: Territory | None | Sales Rep | `PARENT(ITEM(Sales Rep))` |
| Cost Centre | List: L3 Cost Centre/Entity *(common)* | None | Sales Rep | input — links rep to the finance org |
| Is Active? | Boolean | None | Sales Rep | input |

> `SYS01`, `SYS02`, `SYS04` are reused from `_common`; only Sales-specific SYS modules are shown here.

---

## SYS11 Stage Probability — **System**

Win probability per funnel stage. A flag/attribute table, not a calculation.

**Applies To:** Sales Stage

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Win Probability | Number (%) | None | Sales Stage | input — e.g. Lead 10%, Qualified 30%, Proposal 50%, Negotiation 75%, Closed Won 100%, Closed Lost 0% |

---

## CAL01 Quota Allocation — **Calculations**

Split the top-down target down to reps by normalised weight.

**Applies To:** Sales Rep × L2 Product *(common)* × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Territory Weight Total | Number | Sum | Territory × Product | `INP02 Rep Allocation Weight.Weight[SUM: SYS10 Rep Details.Territory]` |
| Quota (local) | Number | Sum | Sales Rep × Product × Time × Versions | see [`formulas.md`](formulas.md) — target × rep weight ÷ territory weight |

---

## CAL02 Weighted Pipeline — **Calculations**

Collapse the numbered pipeline onto the planning grid and weight by stage probability.

**Applies To:** Sales Rep × L2 Product *(common)* × Time *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Weighted Value (local) per deal | Number | Sum | Opportunity | `DAT01 Pipeline Load.Deal Value (local) * SYS11 Stage Probability.Win Probability[LOOKUP: DAT01 Pipeline Load.Stage]` |
| Weighted Pipeline (local) | Number | Sum | Sales Rep × Product × Time | `Weighted Value (local) per deal[SUM: DAT01.Owner (Rep), SUM: DAT01.Product, SUM: DAT01.Close Month]` |

---

## CAL03 Coverage — **Calculations**

**Applies To:** Sales Rep × L2 Product *(common)* × Time *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Coverage Ratio | Number | None | Sales Rep × Product × Time | `IF CAL01 Quota Allocation.Quota (local) = 0 THEN 0 ELSE CAL02 Weighted Pipeline.Weighted Pipeline (local) / CAL01 Quota Allocation.Quota (local)` |
| Gap to Quota (local) | Number | Sum | Sales Rep × Product × Time | `CAL01 Quota Allocation.Quota (local) - CAL02 Weighted Pipeline.Weighted Pipeline (local)` |

---

## CAL04 Target in USD — **Calculations**

Convert quota to group currency and stage it for the FP&A hand-off.

**Applies To:** Sales Rep × L2 Product *(common)* × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| FX Rate | Number (4 dp) | None | Sales Rep × Time × Versions | `SYS04 Exchange Rates.Rate (filled)[LOOKUP: SYS02 Organization Details.Local Currency[LOOKUP: SYS10 Rep Details.Cost Centre]]` |
| Target (USD) | Number | Sum | Sales Rep × Product × Time × Versions | `CAL01 Quota Allocation.Quota (local) * FX Rate` |

---

## OUT01 Rep Scorecard — **Outputs**

Reporting view per rep. No new logic.

**Applies To:** Sales Rep × Time *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Quota (USD) | Number | Sum | Sales Rep × Time | `CAL04 Target in USD.Target (USD)` |
| Weighted Pipeline (USD) | Number | Sum | Sales Rep × Time | `CAL02 Weighted Pipeline.Weighted Pipeline (local) * CAL04 Target in USD.FX Rate` |
| Coverage % | Number (%) | None | Sales Rep × Time | `CAL03 Coverage.Coverage Ratio` |
| At Risk? | Boolean | None | Sales Rep × Time | `Coverage % < 1` |

---

**Related:** [`formulas.md`](formulas.md) · [`lists.md`](lists.md) ·
[`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md) ·
[FP&A modules](../fpa-pl-planning/modules.md) · [Cookbook: top-down allocation](../../cookbook/)
