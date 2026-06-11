# Top-down allocation by ratio

> **Level:** L2 · **Area:** Mapping & Allocation · **PLANS:** Logical, Auditable · **DISCO:** Calculations

## The ask

"Marketing have a £5m brand budget at the total-company level. Push it down to each region in proportion to last year's revenue."

## When you'll see this

- A number is planned at a parent level and must land on the children.
- The split follows a **driver ratio** (revenue, headcount, prior spend), not an even share.
- You need each child's slice to sum exactly back to the parent.

## Approach

Compute each child's **share of a driver**, then multiply the parent total by that share. The subtle part — and where half-built versions go wrong — is that both the **numerator** (the child's driver) and the **denominator** (the total driver) must be available **at the child grain**. A `SUM` up to the parent lands the total at the *parent* item; to divide at the child you then have to bring that parent total **back down** to each child with a `LOOKUP` over the child→parent mapping. The parent budget is brought down the same way.

```
child allocation = (parent total brought to child) × (child driver ÷ parent total driver brought to child)
```

Why idiomatic:

- **Auditable (PLANS):** one line item per step — you can see the ratio and the result separately.
- **Logical:** ratios sum to 1, so allocations sum back to the parent automatically — no rounding plug needed (usually).

## Blueprint

**`INP01 Brand Budget`** — total typed at the parent, `Applies To` Company (top of Region hierarchy):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Budget | Number | Sum | Company, Time | *(input)* |

**`SYS Region`** — the child→parent mapping, `Applies To` Region:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Company | List: Company | None | Region | `PARENT(ITEM(Region))` *(the parent each region rolls to)* |

**`CAL20 Parent Totals`** — `Applies To` **Company** × Time (the parent grain):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Total Driver (parent) | Number | Sum | Company, Time | `CAL20 Allocation.Driver (PY Revenue)[SUM: SYS Region.Company]` |

**`CAL20 Allocation`** — `Applies To` Region × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Driver (PY Revenue) | Number | Sum | Region, Time | `OUT_PY.Revenue` |
| Total Driver (at child) | Number | None | Region, Time | `CAL20 Parent Totals.Total Driver (parent)[LOOKUP: SYS Region.Company]` |
| Share | Number | None | Region, Time | `IF Total Driver (at child) = 0 THEN 0 ELSE Driver (PY Revenue) / Total Driver (at child)` |
| Parent Budget | Number | None | Region, Time | `INP01 Brand Budget.Budget[LOOKUP: SYS Region.Company]` |
| Allocated Budget | Number | Sum | Region, Time | `Parent Budget × Share` |

## Formula(s)

Step 1 — sum the child driver **up** to the parent grain (this lands the total on the `Company`, not on the regions):

```
// CAL20 Parent Totals -> Total Driver (parent)   (Applies To Company × Time)
CAL20 Allocation.Driver (PY Revenue)[SUM: SYS Region.Company]
```

Step 2 — bring that parent total **back down** to each child with a `LOOKUP`, so every region now holds its parent's total at the region grain:

```
// CAL20 Allocation -> Total Driver (at child)
CAL20 Parent Totals.Total Driver (parent)[LOOKUP: SYS Region.Company]
```

Step 3 — each child's share (numerator and denominator now both at the child grain), guarding divide-by-zero:

```
// CAL20 Allocation -> Share
IF Total Driver (at child) = 0 THEN 0 ELSE Driver (PY Revenue) / Total Driver (at child)
```

Step 4 — bring the parent budget down the same way, then allocate:

```
// CAL20 Allocation -> Parent Budget
INP01 Brand Budget.Budget[LOOKUP: SYS Region.Company]

// CAL20 Allocation -> Allocated Budget
Parent Budget * Share
```

Because every region divides its own driver by the **same** parent total (brought down via `LOOKUP`), the shares sum to 1 across the children of a parent and `Allocated Budget` re-sums to `Parent Budget`. The `SUM`-up / `LOOKUP`-down round trip is the heart of the pattern — a `SUM` alone leaves the total on the parent, where the child-grain division can't reach it.

## Pitfalls / gotchas

- **Divide-by-zero:** if `Total Driver` is 0 the whole allocation is `1/0`. Always guard with `IF Total Driver = 0 THEN 0`.
- **Ratios must share a common denominator.** Each child must divide by the *parent's* total driver, not its own — get the total to the parent and back down.
- **Rounding:** shares are fractions; allocated amounts may not sum to the penny. If exactness matters, allocate all-but-one child and plug the last (or use a rounding-residual line item).
- Don't hard-code the split percentages — drive them from the live driver so they self-adjust (*Sustainable*).
- Make sure the driver line item has `Sum` summary, or `Total Driver` rolls up wrong.

## Performance & PLANS notes

- Stepped line items (driver → share → allocation) are both **Auditable** and faster to recalc than one nested formula.
- This pattern is reused everywhere — cost allocation, target setting, phasing — so build it cleanly once.
- For driver-based *cost* allocation specifically, see [allocate-by-driver](allocate-by-driver.md); for letting users type the total and auto-split, see [breakback-ratio-input](breakback-ratio-input.md).

## Related

- [`docs/02-formulas/lookup-and-mapping.md`](../../docs/02-formulas/lookup-and-mapping.md)
- Recipes: [allocate-by-driver](allocate-by-driver.md) · [breakback-ratio-input](breakback-ratio-input.md) · [seasonality-phasing](../time-and-forecasting/seasonality-phasing.md) · [item-parent-ancestor-rollup](../hierarchies-and-lists/item-parent-ancestor-rollup.md)
