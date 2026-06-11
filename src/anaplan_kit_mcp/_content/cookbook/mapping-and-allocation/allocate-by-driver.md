# Allocate cost by a driver (headcount / sqft / revenue)

> **Level:** L2 · **Area:** Mapping & Allocation · **PLANS:** Logical, Auditable, Sustainable · **DISCO:** Calculations

## The ask

"Facilities costs sit in one shared cost centre. Allocate them out to the business units by floor space. Oh, and IT cost should go by headcount, and corporate overhead by revenue."

## When you'll see this

- Shared/indirect costs must be pushed to consuming units for full-cost reporting.
- Different cost pools use **different drivers** (headcount, sqft, revenue, transaction count).
- Management reporting / transfer pricing / activity-based costing.

## Approach

This is top-down allocation with a twist: the **driver is selectable per cost pool**. Model each driver as a line item, pick the right one per pool, compute each unit's share of that driver, and multiply the pool cost by the share.

```
allocated cost = pool cost × (unit's driver ÷ total driver for that pool)
```

Keep drivers in a System/Inputs module and the **pool → driver** choice in a small mapping, so adding a pool or switching its driver is data, not a formula edit.

Why idiomatic:

- **Sustainable (PLANS):** the driver choice is data (a mapping cell), not hard-coded logic.
- **Auditable:** stepped line items show the driver, the share, and the allocated amount separately.

## Blueprint

**`SYS20 Driver by Pool`** — which driver each cost pool uses:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Driver Type | List: Driver Types | None | Cost Pool | *(input/mapping)* |

**`INP20 Drivers`** — the driver values, `Applies To` Business Unit:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Headcount | Number | Sum | Business Unit, Time | *(input)* |
| Floor Space (sqft) | Number | Sum | Business Unit, Time | *(input)* |
| Revenue | Number | Sum | Business Unit, Time | `OUT.Revenue` |

**`CAL40 Pool Totals`** — `Applies To` **Cost Pool** × Time (the denominator grain, one row per pool):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Total Driver (pool) | Number | Sum | Cost Pool, Time | `CAL40 Cost Allocation.Selected Driver` *(BU dimension drops, so it sums across BUs per pool)* |

**`CAL40 Cost Allocation`** — `Applies To` Cost Pool × Business Unit × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Selected Driver | Number | Sum | Cost Pool, Business Unit, Time | see formula |
| Total Driver (at BU) | Number | None | Cost Pool, Business Unit, Time | `CAL40 Pool Totals.Total Driver (pool)` *(broadcast back to each BU)* |
| Share | Number | None | Cost Pool, Business Unit, Time | `IF Total Driver (at BU) = 0 THEN 0 ELSE Selected Driver / Total Driver (at BU)` |
| Pool Cost | Number | Sum | Cost Pool, Business Unit, Time | `INP_Pool.Cost` (broadcast to each BU) |
| Allocated Cost | Number | Sum | Cost Pool, Business Unit, Time | `Pool Cost × Share` |

## Formula(s)

Pick the driver per pool (small, readable `IF`/`LOOKUP` on the **driver type**, not on item names):

```
// CAL40 Cost Allocation -> Selected Driver
IF SYS20 Driver by Pool.Driver Type = Driver Types.Headcount THEN INP20 Drivers.Headcount
ELSE IF SYS20 Driver by Pool.Driver Type = Driver Types.Sqft THEN INP20 Drivers.Floor Space (sqft)
ELSE INP20 Drivers.Revenue
```

Sum the driver to the pool grain, then broadcast it back so each BU divides by the **same** pool total. Because `CAL40 Pool Totals` has no BU dimension, referencing `Selected Driver` into it sums across BUs (the dimension simply drops); referencing the pool total back into the BU-level module repeats it across every BU:

```
// CAL40 Pool Totals -> Total Driver (pool)   (Applies To Cost Pool × Time)
CAL40 Cost Allocation.Selected Driver

// CAL40 Cost Allocation -> Total Driver (at BU)   (pool total, repeated across BUs)
CAL40 Pool Totals.Total Driver (pool)
```

That gives each BU the denominator it needs, at the BU grain. Share and allocation (guarded):

```
// CAL40 Cost Allocation -> Share
IF Total Driver (at BU) = 0 THEN 0 ELSE Selected Driver / Total Driver (at BU)

// CAL40 Cost Allocation -> Allocated Cost
Pool Cost * Share
```

## Pitfalls / gotchas

- **Divide-by-zero** when a pool's total driver is 0 (e.g. a BU with no headcount month) — guard it.
- Choosing the driver by **list item, not item name** keeps it Sustainable. Selecting on `Driver Types` (a small fixed list) is fine; `SELECT: BusinessUnit.Acme` is not.
- **Allocated cost should reconcile to the pool total.** Sum `Allocated Cost` across BUs per pool and check it equals `Pool Cost` — see [reconciliation-check-module](../performance/reconciliation-check-module.md).
- **Circular driver:** allocating overhead by revenue is fine; allocating by *fully-loaded cost that includes the allocation* is circular. Use a pre-allocation driver.
- Time alignment: if drivers are monthly, allocate monthly; mixing an annual driver with monthly cost skews results.

## Performance & PLANS notes

- The `Selected Driver` `IF` is small (over the Driver Types list, a handful of items) — acceptable. Avoid `IF` chains over large lists; map instead.
- Stepped line items make the allocation **Auditable** and let the engine cache `Total Driver` once.
- Keep drivers in **Inputs**, the pool→driver choice in **System** — change a driver without touching the calc engine.

## Related

- [`docs/02-formulas/lookup-and-mapping.md`](../../docs/02-formulas/lookup-and-mapping.md)
- Recipes: [top-down-allocation-by-ratio](top-down-allocation-by-ratio.md) · [sum-lookup-remap](sum-lookup-remap.md) · [reconciliation-check-module](../performance/reconciliation-check-module.md) · [replace-if-with-boolean](../performance/replace-if-with-boolean.md)
