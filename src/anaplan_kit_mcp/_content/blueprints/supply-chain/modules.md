# Supply Chain — Modules

> **Level:** L2 · **Area:** Blueprint (Supply Chain) · **DISCO:** mixed

Blueprint tables, [DISCO](../../docs/03-methodology/disco.md)-tagged. Dimensions marked *(common)*
come from the [`_common` backbone](../_common/README.md). The planning grid is **SKU × Location ×
Time** unless noted.

---

## DAT01 Statistical Demand — **Data**

The system-generated baseline forecast, loaded as-is.

**Applies To:** SKU × Location × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Stat Demand (units) | Number | Sum | SKU × Location × Time × Versions | import from forecasting engine |

---

## DAT02 Opening On-Hand — **Data**

Current physical inventory, loaded for the first plan month only.

**Applies To:** SKU × Location

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| On-Hand at Start (units) | Number | Sum | SKU × Location | import from WMS (seeds the projection's first opening balance) |

---

## INP01 Demand Adjustment — **Inputs**

Planner overlay on the statistical baseline (promotions, judgement).

**Applies To:** SKU × Location × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Demand Override (units) | Number | Sum | SKU × Location × Time × Versions | input — blank = use statistical |
| Use Override? | Boolean | None | SKU × Location × Time × Versions | input |

---

## INP02 Inventory Policy — **Inputs**

Replenishment rules per SKU × Location.

**Applies To:** SKU × Location

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Safety Stock (units) | Number | Sum | SKU × Location | input |
| Lead Time (days) | Number | None | SKU × Location | input |
| Min Order Qty | Number | None | SKU × Location | input — supply is rounded up to a multiple of this |

---

## INP03 Standard Unit Cost — **Inputs**

Cost per unit (local currency of the Location's entity). Drives the FP&A COGS hand-off.

**Applies To:** SKU × Location × Time *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Unit Cost (local) | Number (2 dp) | None | SKU × Location × Time | input — standard cost |

---

## SYS20 SKU Details / SYS21 Location Details — **System**

Attributes & mappings. `SYS01`, `SYS02` reused from `_common`.

**SYS20 — Applies To:** SKU

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Product | List: L2 Product *(common)* | None | SKU | `PARENT(ITEM(SKU))` |
| Is Active? | Boolean | None | SKU | input |

**SYS21 — Applies To:** Location

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Cost Centre | List: L3 Cost Centre/Entity *(common)* | None | Location | input — links DC/plant to finance org |

---

## CAL01 Net Demand — **Calculations**

Pick override or statistical demand.

**Applies To:** SKU × Location × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Net Demand (units) | Number | Sum | SKU × Location × Time × Versions | `IF INP01 Demand Adjustment.Use Override? THEN INP01 Demand Adjustment.Demand Override (units) ELSE DAT01 Statistical Demand.Stat Demand (units)` |

---

## CAL02 Inventory Projection — **Calculations**

The time-phased balance — the heart of the model. Uses `PREVIOUS()` to chain months.

**Applies To:** SKU × Location × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Opening Inventory (units) | Number | None | SKU × Location × Time × Versions | see [`formulas.md`](formulas.md) — prior Closing, seeded by `DAT02` |
| Required Supply (units) | Number | Sum | SKU × Location × Time × Versions | see [`formulas.md`](formulas.md) — fill demand + safety stock, respect MOQ |
| Closing Inventory (units) | Number | None | SKU × Location × Time × Versions | `Opening Inventory (units) + Required Supply (units) - CAL01 Net Demand.Net Demand (units)` |

---

## CAL03 Coverage — **Calculations**

**Applies To:** SKU × Location × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Days of Supply | Number | None | SKU × Location × Time × Versions | `IF CAL01 Net Demand.Net Demand (units) = 0 THEN 0 ELSE CAL02 Inventory Projection.Closing Inventory (units) / CAL01 Net Demand.Net Demand (units) * SYS01 Time Settings.Days in Period` |
| Stock-Out Risk? | Boolean | None | SKU × Location × Time × Versions | `CAL02 Inventory Projection.Closing Inventory (units) < INP02 Inventory Policy.Safety Stock (units)` |

---

## CAL04 Supply Cost — **Calculations**

Cost of the planned supply, and the FP&A COGS feed.

**Applies To:** SKU × Location × Time *(common)* × Versions *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Supply Cost (local) | Number | Sum | SKU × Location × Time × Versions | `CAL02 Inventory Projection.Required Supply (units) * INP03 Standard Unit Cost.Unit Cost (local)` |
| Supply Cost by CC (local) | Number | Sum | L3 Cost Centre/Entity × L2 Product × Time × Versions | `Supply Cost (local)[SUM: SYS21 Location Details.Cost Centre, SUM: SYS20 SKU Details.Product]` |

> `Supply Cost by CC (local)` (grain **L3 Cost Centre × L2 Product × Time × Versions**) is the hand-off
> line. It is **imported** (model-to-model) into FP&A's `INP04 Direct Materials (imported).Direct Materials
> (local)` at the **same grain** — matched 1:1 on the shared `_common` lists — where FP&A's `CAL02` uses it
> as bottom-up COGS (with a `COGS %` fallback). FX is applied once, on the FP&A side. *(Necessary — no
> double conversion.)* See [`formulas.md`](formulas.md) §4 and [`fpa-pl-planning/modules.md`](../fpa-pl-planning/modules.md).

---

## OUT01 Supply Plan — **Outputs**

Reporting view; no new logic.

**Applies To:** SKU × Location × Time *(common)*

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Net Demand | Number | Sum | SKU × Location × Time | `CAL01 Net Demand.Net Demand (units)` |
| Required Supply | Number | Sum | SKU × Location × Time | `CAL02 Inventory Projection.Required Supply (units)` |
| Closing Inventory | Number | None | SKU × Location × Time | `CAL02 Inventory Projection.Closing Inventory (units)` |
| Days of Supply | Number | None | SKU × Location × Time | `CAL03 Coverage.Days of Supply` |
| Stock-Out Risk? | Boolean | None | SKU × Location × Time | `CAL03 Coverage.Stock-Out Risk?` |

---

**Related:** [`formulas.md`](formulas.md) · [`lists.md`](lists.md) ·
[`_common/time-and-versions.md`](../_common/time-and-versions.md) (`Days in Period`) ·
[FP&A modules](../fpa-pl-planning/modules.md) · [Time fundamentals](../../docs/01-fundamentals/time.md)
