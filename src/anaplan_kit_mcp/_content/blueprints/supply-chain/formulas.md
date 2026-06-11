# Supply Chain — Key Formulas

> **Level:** L2 · **Area:** Blueprint (Supply Chain) · **DISCO:** Calculations

The time-phased inventory balance is the centrepiece. It shows the canonical Anaplan
`PREVIOUS()` carry-forward pattern. One line item per step. *(Auditable)*

---

## 1. Net demand (override or baseline)

`CAL01.Net Demand (units)`:

```
IF INP01 Demand Adjustment.Use Override?
   THEN INP01 Demand Adjustment.Demand Override (units)
   ELSE DAT01 Statistical Demand.Stat Demand (units)
```

A Boolean switch keeps the planner overlay auditable — you can always see whether a number is system
or human. *(Auditable; Boolean beats burying it in a nested `IF`.)*

---

## 2. The inventory projection (PREVIOUS carry-forward)

This is the pattern to learn. Three line items in `CAL02`, computed in order.

**Opening Inventory** — last month's closing, seeded by the loaded on-hand in the first period:

```
IF SYS01 Time Settings.Is First Month of Year? AND ISBLANK(PREVIOUS(Closing Inventory (units)))
   THEN DAT02 Opening On-Hand.On-Hand at Start (units)
   ELSE PREVIOUS(Closing Inventory (units))
```

In practice the simpler, robust idiom is:

```
Opening Inventory (units) = PREVIOUS(Closing Inventory (units)) + (seed in first model month)
```

where the seed (`DAT02`) is added only in the very first period of the model span. The point: the
opening balance is **never typed per month** — it flows from the prior month. *(Sustainable)*

**Required Supply** — bring closing up to demand + safety stock, then respect the minimum order qty:

```
Demand Plus Safety = CAL01 Net Demand.Net Demand (units)
                     + INP02 Inventory Policy.Safety Stock (units)
                     - Opening Inventory (units)

Required Supply (units) =
   IF Demand Plus Safety <= 0 THEN 0
   ELSE CEILING( Demand Plus Safety / INP02 Inventory Policy.Min Order Qty )
        * INP02 Inventory Policy.Min Order Qty
```

`CEILING(x / MOQ) * MOQ` rounds the order **up** to a whole multiple of the minimum order quantity.

**Closing Inventory** — the balance identity:

```
Opening Inventory (units) + Required Supply (units) - CAL01 Net Demand.Net Demand (units)
```

> Why no circular reference? `PREVIOUS()` reads a **prior period** value, so the dependency runs
> forward through time, not back on itself. Anaplan computes period by period. *(Logical)*

---

## 3. Days of supply (uses shared `Days in Period`)

`CAL03.Days of Supply`:

```
IF CAL01 Net Demand.Net Demand (units) = 0 THEN 0
ELSE CAL02 Inventory Projection.Closing Inventory (units)
     / CAL01 Net Demand.Net Demand (units)
     * SYS01 Time Settings.Days in Period
```

`Days in Period` comes from the shared [`SYS01`](../_common/time-and-versions.md) — so a 28-day
February and a 31-day March give correct coverage automatically. *(Sustainable — calendar lives in
`_common`.)*

`Stock-Out Risk? = Closing Inventory (units) < Safety Stock (units)`.

---

## 4. Supply cost and the FP&A hand-off

Cost the planned supply (`CAL04.Supply Cost (local)`):

```
CAL02 Inventory Projection.Required Supply (units) * INP03 Standard Unit Cost.Unit Cost (local)
```

Then aggregate units of cost onto the **finance** grain (`CAL04.Supply Cost by CC (local)`):

```
Supply Cost (local)[
   SUM: SYS21 Location Details.Cost Centre,
   SUM: SYS20 SKU Details.Product ]
```

This collapses SKU × Location down to **L3 Cost Centre × L2 Product × Time × Versions** — exactly the grain
of FP&A's COGS receiving line. FP&A applies FX once on its side (avoiding double conversion), so Supply
Chain stays in units + local cost.

### The FP&A COGS hand-off (model-to-model import)

Supply Chain and FP&A are **separate models**, so the feed is a scheduled **model-to-model import**.
`Supply Cost by CC (local)` lands in FP&A's `INP04 Direct Materials (imported).Direct Materials (local)`;
FP&A's `CAL02 COGS (local)` then uses it where present and falls back to `Revenue × COGS %` otherwise.

| Supply Chain source line item | FP&A target line item | Mapping (matched on shared `_common` lists) |
| --- | --- | --- |
| `CAL04 Supply Cost.Supply Cost by CC (local)` (L3 Cost Centre × L2 Product × Time × Versions) | `INP04 Direct Materials (imported).Direct Materials (local)` (same grain) | `L3 Cost Centre/Entity` → `L3 Cost Centre/Entity`; `L2 Product` → `L2 Product`; `Time` → `Time`; `Versions` → `Versions` — all 1:1, no remapping |

See [fpa-pl-planning/modules.md](../fpa-pl-planning/modules.md) (INP04, CAL02) and
[fpa-pl-planning/formulas.md](../fpa-pl-planning/formulas.md) §2.

---

## Consistency check

```
DAT01 / INP01 ─► CAL01 Net Demand ─┐
DAT02 ─────────► CAL02 Opening ─────┴► CAL02 Required Supply ─► CAL02 Closing
                                                │                      │
                                                ▼                      ▼
                            CAL04 Supply Cost (local)         CAL03 Days of Supply
                                                │
            CAL04 Supply Cost by CC (local) ─► import ─► FP&A INP04 Direct Materials ─► CAL02 COGS
```

Every output traces back to loaded demand/on-hand or a typed policy/cost.

---

**Related:** [`modules.md`](modules.md) · [`README.md`](README.md) ·
[`_common/time-and-versions.md`](../_common/time-and-versions.md) (`Days in Period`) ·
[FP&A formulas](../fpa-pl-planning/formulas.md) ·
[Formula reference](../../docs/02-formulas/) (`PREVIOUS`, `CEILING`)
