# Auto-create list members on import

> **Level:** L2 · **Area:** Data & Imports · **PLANS:** Sustainable, Logical · **DISCO:** Data / System

## The ask

"New cost centres get opened all the time. I don't want to manually add every one to Anaplan before the load runs — can the import just create them when it sees a new code?"

## When you'll see this

- Source systems mint new entities/products/employees between loads.
- You're loading transactional data keyed to items that may not exist yet.
- You want loads to be hands-off but still safe.

## Approach

Let the **import action create new list members** from the file, while controlling exactly *where* they land. In the import action you tick **"Add new items"**; Anaplan inserts any code not already in the list, and updates the rest. For a hierarchy you also map the **parent** so new members slot into the right branch — never the top level by accident.

Why idiomatic:

- **Sustainable (PLANS):** loads survive new members appearing in the source without a builder touching the model.
- **Logical:** mapping the parent keeps the hierarchy correct and one-directional.

The safe version of "auto-create" pairs creation with a **mapping/parent column** and (ideally) a **staging list** in a data hub, so junk codes don't pollute your real planning hierarchy.

## Blueprint

**List to populate:** `Cost Centre` (hierarchy under parent list `Region`).

Import file columns:

| File column | Maps to | Purpose |
| --- | --- | --- |
| `CC Code` | `Cost Centre` → Code | The unique item identifier |
| `CC Name` | `Cost Centre` → Display Name | Human-readable name |
| `Region Code` | `Cost Centre` → Parent | Slots the new item under the right region |

**`SYS02 Organization Details`** — attributes refreshed on each load:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Active? | Boolean | None | Cost Centre | *(import target)* |
| Opened Date | Date | None | Cost Centre | *(import target)* |

## Formula(s)

List creation happens in the **action settings**, not a formula. Key choices in the import action:

```
List mapping:
  - Item:   map file "CC Code"   -> Code
  - Parent: map file "Region Code" -> Parent   (so new items land in the right branch)
Options:
  - Add new items:            ON
  - Update existing items:    ON
  - Delete omitted items:     OFF   (don't let one file remove members it simply didn't mention)
```

To flag rows whose parent is missing (so you can review them):

```
// CAL01 New Member Check -> Orphan?
ISBLANK(PARENT(ITEM(Cost Centre)))
```

## Pitfalls / gotchas

- **Map the parent**, or new members pile up at the top level (or fail). For a numbered list, also set the display-name/code mapping deliberately.
- **Leave "Delete omitted items" OFF** unless the file is a guaranteed full population — otherwise auto-create on Monday and auto-delete on Tuesday.
- A typo'd code creates a *new* member rather than updating the intended one. Validate codes upstream or stage first.
- Auto-creating into your live planning model can pollute it. Prefer creating in a **data hub staging list**, review, then publish clean members to spokes.
- Watch the **list maximum size** and any "production list" ALM settings — creation can be blocked in deployed models.

## Performance & PLANS notes

- Creating members on import is cheap; the cost is *uncontrolled* growth. Pair with a periodic clean-up/deactivate flag (`Active?`) rather than deleting history.
- Keep auto-create in the **hub** so spokes receive a vetted list, satisfying **Necessary** and **Sustainable**.

## Related

- [`docs/04-integration/imports-exports.md`](../../docs/04-integration/imports-exports.md)
- [`docs/01-fundamentals/lists-and-hierarchies.md`](../../docs/01-fundamentals/lists-and-hierarchies.md)
- Recipes: [flat-file-to-hierarchy](flat-file-to-hierarchy.md) · [build-a-data-hub](build-a-data-hub.md) · [handle-import-errors-and-dump-files](handle-import-errors-and-dump-files.md)
