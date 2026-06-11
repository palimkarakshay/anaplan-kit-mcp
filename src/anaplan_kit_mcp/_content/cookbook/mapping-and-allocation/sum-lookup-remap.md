# Remap data between dimensions (SUM / LOOKUP)

> **Level:** L2 · **Area:** Mapping & Allocation · **PLANS:** Sustainable, Performance · **DISCO:** System / Calculations

## The ask

"Sales come in by Product, but the P&L is by Product Group. And Finance want everything rolled to the reporting cost-centre, not the source one. Can you move the numbers across without me re-keying them?"

## When you'll see this

- Source data is in one dimension; reporting needs another.
- A many-to-one relationship (many Products → one Product Group) or a one-to-one remap (source CC → reporting CC).
- You're translating between a transactional grain and a planning grain.

## Approach

Use a **System mapping module** that says, for each source item, *which target item it belongs to*. Then move the data with `SUM` (aggregate up: many source → one target) or `LOOKUP` (pull across: one target → one source).

The rule of thumb:

- **`SUM`** when you're collapsing *many* source items into *one* target (Product → Product Group). The mapping line item is `Applies To` the **source**.
- **`LOOKUP`** when you're fetching a value for each target via a pointer (target → its source). The mapping line item is `Applies To` the **target**.

Why idiomatic:

- **Sustainable (PLANS):** the relationship lives in one System module. Re-map a product to a new group by changing one cell — no formula edits, no `SELECT`.
- **Performance:** `SUM`/`LOOKUP` over a mapping is far faster and cleaner than nested `IF`s naming items.

## Blueprint

**`SYS10 Product Mapping`** — the relationship, `Applies To` Product:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Product Group | List: Product Group | None | Product | *(import target — the mapping)* |

**`DAT01 Sales by Product`** — source data:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Revenue | Number | Sum | Product, Time | *(import target)* |

**`CAL10 Sales by Group`** — result, dimensioned by Product **Group**:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Revenue | Number | Sum | Product Group, Time | `DAT01 Sales by Product.Revenue[SUM: SYS10 Product Mapping.Product Group]` |

## Formula(s)

**Aggregate up (many → one)** — result is by Product Group, source is by Product:

```
// CAL10 Sales by Group -> Revenue
DAT01 Sales by Product.Revenue[SUM: SYS10 Product Mapping.Product Group]
```

**Pull across (target points at source)** — e.g. each reporting CC stores its source CC, fetch its value:

```
// CAL11 Reporting CC -> Value
DAT02 Source CC Data.Value[LOOKUP: SYS11 CC Mapping.Source CC]
```

The bracket reads: "give me `Revenue`, summed/looked-up using the mapping line item as the locator." The mapping line item must be formatted as the **target list** (for `SUM`) or the **source list** (for `LOOKUP`).

## Pitfalls / gotchas

- **`SUM` vs `LOOKUP` mixed up** is the classic error. `SUM`: mapping is on the source, result aggregates. `LOOKUP`: mapping is on the target, result is a straight pull. See [sum-vs-nested-lookup](../performance/sum-vs-nested-lookup.md).
- The mapping line item's **format must be the list you're mapping to/from** — a Text code won't work; use a list-formatted line item (resolve text codes first with [FINDITEM](../hierarchies-and-lists/finditem-text-key.md)).
- **Blank mapping = dropped data.** Items with no mapped target vanish from the `SUM`. Flag unmapped items.
- Don't use `SELECT: Product Group.Electronics` to hard-route — that breaks when the list changes (*Sustainable*).
- Watch **summary methods**: the source line item must `Sum` for the aggregation to be meaningful.

## Performance & PLANS notes

- One mapping module, referenced by many calc modules, is the **Necessary** + **Sustainable** ideal.
- `SUM`/`LOOKUP` are engine-optimised; they outperform `IF`-based routing on large modules every time.
- If you remap frequently, keep the mapping importable so admins can change relationships without a builder.

## Related

- [`docs/02-formulas/lookup-and-mapping.md`](../../docs/02-formulas/lookup-and-mapping.md)
- [`docs/03-methodology/disco.md`](../../docs/03-methodology/disco.md)
- Recipes: [allocate-by-driver](allocate-by-driver.md) · [top-down-allocation-by-ratio](top-down-allocation-by-ratio.md) · [sum-vs-nested-lookup](../performance/sum-vs-nested-lookup.md)
