# SUM vs nested LOOKUP (choose the right aggregation)

> **Level:** L2 · **Area:** Performance · **PLANS:** Performance, Logical · **DISCO:** Calculations

## The ask

"I need sales rolled from Product to Product Group. One colleague says use `SUM`, another says `LOOKUP`. They give different answers and one of them is slow. Which is right?"

## When you'll see this

- Moving data between dimensions and unsure which mapping function fits.
- A formula that's correct but slow, or fast but wrong.
- Choosing between aggregating up vs pulling across.

## Approach

Pick by **direction of the relationship**:

- **`SUM`** — *many source → one target*. You're **aggregating** (Products into a Group). The mapping line item lives on the **source** and is formatted as the **target** list. Result is dimensioned by the target.
- **`LOOKUP`** — *one target → its source*. You're **fetching** a single value via a pointer (each reporting CC stores its source CC). The mapping lives on the **target** and is formatted as the **source** list. No aggregation.

If you find yourself chaining several `LOOKUP`s to fake an aggregation, that's the wrong tool — use `SUM`. If you `SUM` when you only need one value, you may aggregate cells you didn't mean to.

```
Aggregate up:   Source.Value[SUM: Mapping.TargetItem]
Pull across:    Source.Value[LOOKUP: Mapping.SourceItem]
```

Why idiomatic:

- **Performance (PLANS):** the right native function is engine-optimised; nested `LOOKUP`s or `IF`-routing aren't.
- **Logical:** the function matches the cardinality of the relationship.

## Blueprint

**`SYS10 Product Mapping`** — for `SUM`, mapping on the source (Product), formatted as target (Group):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Product Group | List: Product Group | None | Product | *(mapping)* |

**Results:**

| Module | Applies To | Formula |
| --- | --- | --- |
| `CAL Sales by Group` (aggregate) | Product Group, Time | `DAT Sales.Revenue[SUM: SYS10 Product Mapping.Product Group]` |
| `CAL Reporting CC` (pull) | Reporting CC, Time | `DAT Source.Value[LOOKUP: SYS11 CC Map.Source CC]` |

## Formula(s)

Aggregate many products into a group (the common case):

```
// CAL Sales by Group -> Revenue
DAT Sales.Revenue[SUM: SYS10 Product Mapping.Product Group]
```

Pull a single value across via a pointer (no aggregation):

```
// CAL Reporting CC -> Value
DAT Source.Value[LOOKUP: SYS11 CC Map.Source CC]
```

You can combine: `SUM` to aggregate **and** `LOOKUP` to relocate in the same bracket when the relationship needs both — but only when each genuinely applies.

## Pitfalls / gotchas

- **`SUM` aggregates; `LOOKUP` doesn't.** Using `LOOKUP` where you needed `SUM` returns *one* arbitrary source value, not the total — a silent wrong number.
- **Mapping format and placement:** `SUM` mapping is on the source, formatted as the target list; `LOOKUP` mapping is on the target, formatted as the source list. Getting this backwards won't compile or will misroute.
- **Nested/chained `LOOKUP` to emulate a roll-up is slow and wrong** — that's `SUM`'s job.
- **Blank mappings drop data from a `SUM`** and return blank from a `LOOKUP` — flag unmapped items.
- Don't replace either with `IF Type = ...` chains — mapping is both faster and Sustainable (see [replace-if-with-boolean](replace-if-with-boolean.md)).

## Performance & PLANS notes

- Native `SUM`/`LOOKUP` over a mapping are the engine's optimised aggregation paths — far faster than `IF` routing on large modules.
- One mapping module reused by many calcs is **Necessary** + **Sustainable**.
- Right function = right answer *and* good performance — this choice is both correctness and speed.

## Related

- [`docs/02-formulas/lookup-and-mapping.md`](../../docs/02-formulas/lookup-and-mapping.md)
- Recipes: [sum-lookup-remap](../mapping-and-allocation/sum-lookup-remap.md) · [replace-if-with-boolean](replace-if-with-boolean.md) · [shrink-with-subsets-and-time-ranges](shrink-with-subsets-and-time-ranges.md)
