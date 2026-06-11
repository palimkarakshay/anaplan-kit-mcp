# ITEM / PARENT / ANCESTOR rollups

> **Level:** L2 · **Area:** Hierarchies & Lists · **PLANS:** Logical, Sustainable · **DISCO:** System / Calculations

## The ask

"On a flat module I need each cost centre to also know its region and its division — and I want to filter only the rows that sit under a chosen division."

## When you'll see this

- You need an item's parent/ancestor as a value (to map, label, or filter).
- Conditional logic that should apply only within a branch of the hierarchy.
- Building System attribute modules that expose the tree as data.

## Approach

Three workhorse functions:

- **`ITEM(list)`** — the current member of `list` in this cell's context.
- **`PARENT(item)`** — the immediate parent of an item (one level up).
- **`ISANCESTOR(ancestor, descendant)`** — `TRUE` if the first item is anywhere above the second in the hierarchy.

Use `PARENT` to step up one level and chain `PARENT(PARENT(...))` to reach grandparents (Anaplan has no `ANCESTOR()` / `CHILDREN()` function — chain `PARENT`, or use a SYS mapping for a named level), and `ISANCESTOR` for "is this under that branch?" tests. Build these **once** in a `SYS` module and reference them — don't re-derive the tree in every calc.

Why idiomatic:

- **Sustainable (PLANS):** attributes follow the hierarchy automatically; restructure the tree and the values update with no formula change.
- **Logical:** the rollup direction matches the hierarchy direction.

## Blueprint

**`SYS40 Cost Centre Hierarchy`** — `Applies To` Cost Centre:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Region | List: Region | None | Cost Centre | `PARENT(ITEM(Cost Centre))` |
| Region Name | Text | None | Cost Centre | `NAME(PARENT(ITEM(Cost Centre)))` |
| Division | List: Division | None | Cost Centre | `PARENT(PARENT(ITEM(Cost Centre)))` |
| Under Selected Division? | Boolean | None | Cost Centre | `ISANCESTOR(INP.Chosen Division, ITEM(Cost Centre))` |

## Formula(s)

Immediate parent of the current cost centre:

```
// SYS40 -> Region
PARENT(ITEM(Cost Centre))
```

Two levels up (grandparent). `ITEM`/`PARENT` return list items, so you can chain them:

```
// SYS40 -> Division
PARENT(PARENT(ITEM(Cost Centre)))
```

"Is this cost centre anywhere under the chosen division?" — great for branch filters and selective access:

```
// SYS40 -> Under Selected Division?
ISANCESTOR(INP Settings.Chosen Division, ITEM(Cost Centre))
```

Get the text name of an ancestor for a label:

```
NAME(PARENT(ITEM(Cost Centre)))
```

## Pitfalls / gotchas

- **`PARENT` format must be the parent list.** The result line item has to be formatted as `Region` (the parent's list), or it won't compile. Chaining to `Division` means that line item is formatted as `Division`.
- **Top-level items have no parent** — `PARENT` returns blank. Guard downstream logic for blanks.
- **`ISANCESTOR` argument order:** `ISANCESTOR(ancestor, descendant)`. Reversed, it's always false. Read it as "is arg1 an ancestor of arg2?".
- `ITEM(list)` only makes sense in a module **dimensioned by that list**. On a module not dimensioned by Cost Centre, `ITEM(Cost Centre)` has no context.
- Don't hard-code item names to test branches (`IF Division = Division.North`); use `ISANCESTOR` against an input/selection so it survives list changes (*Sustainable*).

## Performance & PLANS notes

- Compute hierarchy attributes **once** in a SYS module and reference everywhere — **Necessary** + **Sustainable**.
- These functions are engine-native and cheap; they're the right tool instead of importing parent codes repeatedly.
- `ISANCESTOR` Booleans feed filters, DCA, and selective access cleanly — see [cascading-selective-access](../security-and-dca/cascading-selective-access.md).

## Related

- [`docs/02-formulas/hierarchy-functions.md`](../../docs/02-formulas/hierarchy-functions.md)
- [`docs/01-fundamentals/lists-and-hierarchies.md`](../../docs/01-fundamentals/lists-and-hierarchies.md)
- Recipes: [flat-file-to-hierarchy](../data-and-imports/flat-file-to-hierarchy.md) · [cascading-selective-access](../security-and-dca/cascading-selective-access.md) · [finditem-text-key](finditem-text-key.md)
