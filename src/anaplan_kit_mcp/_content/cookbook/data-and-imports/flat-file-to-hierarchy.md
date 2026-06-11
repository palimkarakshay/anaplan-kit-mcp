# Flat file to composite hierarchy

> **Level:** L2 · **Area:** Data & Imports · **PLANS:** Sustainable, Logical · **DISCO:** Data / System

## The ask

"Here's a CSV of every cost centre. Each row has the cost centre code, its name, and the region code it belongs to. Can you build the region → cost centre tree in Anaplan from this?"

## When you'll see this

- The source gives you one flat table with a **parent-code column** rather than a pre-built tree.
- You need a two- or three-level composite hierarchy (Region > Cost Centre, or Company > Region > Cost Centre).
- Master data lives in a data hub and you want the structure rebuilt on each load.

## Approach

A composite hierarchy in Anaplan is **a stack of lists**: a top list, then a child list whose **Parent** is the list above it. A flat file becomes a hierarchy by **importing the parent column into each child list's Parent property**. Build it **top-down** — the parent list must exist before the child can point at it.

Why idiomatic:

- **Sustainable (PLANS):** the tree rebuilds itself from data on every load. Add a new region in the source, run the process, and the structure follows — no manual list editing.
- **Logical:** the parent column maps one child to exactly one parent, giving a clean one-directional rollup.

Build a **process** with the imports in dependency order: load `Region` first, then `Cost Centre` (which references Region as its parent). See [auto-create-list-members](auto-create-list-members.md) for the create-on-import settings.

## Blueprint

**Lists (the hierarchy stack):**

| List | Parent | Populated from |
| --- | --- | --- |
| `Region` | *(top level)* | distinct `Region Code` column |
| `Cost Centre` | `Region` | `CC Code`, parent = `Region Code` |

**Import file (one flat table):**

| File column | Maps to | Notes |
| --- | --- | --- |
| `Region Code` | `Region` → Code (import 1) and `Cost Centre` → Parent (import 2) | used twice |
| `Region Name` | `Region` → Display Name | |
| `CC Code` | `Cost Centre` → Code | the leaf item |
| `CC Name` | `Cost Centre` → Display Name | |

**`SYS02 Organization Details`** — attributes for downstream use:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Parent Region | List: Region | None | Cost Centre | `PARENT(ITEM(Cost Centre))` |
| Region Name | Text | None | Cost Centre | `NAME(PARENT(ITEM(Cost Centre)))` |

## Formula(s)

Most of the work is in **import-action mappings**, not formulas. Order matters:

```
Process step 1 — import Region:
  Item:   file "Region Code" -> Code
  Name:   file "Region Name" -> Display Name
  Add new items: ON

Process step 2 — import Cost Centre:
  Item:   file "CC Code"      -> Code
  Parent: file "Region Code"  -> Parent     <- this builds the tree
  Add new items: ON ; Delete omitted items: OFF
```

To verify the structure after load, derive the parent in a SYS module:

```
// SYS02 Organization Details -> Parent Region
PARENT(ITEM(Cost Centre))
```

## Pitfalls / gotchas

- **Load the parent list first.** Import `Cost Centre` before `Region` exists and every row orphans or fails.
- A blank or unmatched `Region Code` sends the item to the top level or to the dump file — flag orphans (`ISBLANK(PARENT(ITEM(Cost Centre)))`).
- **Codes vs display names:** map on **Code**, not name. Names aren't guaranteed unique and change often.
- Three-level tree = three lists and three import steps, each pointing at the level above. Don't try to cram levels into one list.
- If the same leaf code appears under two parents in the file, the last row wins — the source data is wrong, fix it upstream.

## Performance & PLANS notes

- Building structure from data (not by hand) is the **Sustainable** win — the model absorbs org changes with zero formula edits.
- Keep the hierarchy build in the **data hub** so every spoke receives the same vetted tree.
- A composite hierarchy is cheaper than carrying region as a separate property on a flat list, because rollups come for free.

## Related

- [`docs/01-fundamentals/lists-and-hierarchies.md`](../../docs/01-fundamentals/lists-and-hierarchies.md)
- [`docs/04-integration/imports-exports.md`](../../docs/04-integration/imports-exports.md)
- Recipes: [auto-create-list-members](auto-create-list-members.md) · [item-parent-ancestor-rollup](../hierarchies-and-lists/item-parent-ancestor-rollup.md) · [concatenated-key-for-imports](concatenated-key-for-imports.md)
