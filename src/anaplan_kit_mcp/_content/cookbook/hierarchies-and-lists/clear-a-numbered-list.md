# Clear a numbered list before reload (DELETE action)

> **Level:** L2 · **Area:** Hierarchies & Lists · **PLANS:** Performance, Sustainable · **DISCO:** Data

## The ask

"Every night we do a full reload of the transaction feed. The numbered list keeps growing because old rows never get removed — it's at 8 million items and climbing. How do I wipe it before each load?"

## When you'll see this

- Truncate-and-reload patterns on a transactional numbered list.
- A numbered list bloating because imports add but never remove.
- Housekeeping before a clean full refresh.

## Approach

Add a **"Delete from List using Selection"** action (a DELETE action) and run it **before** the import in a **process**. The action removes list items based on a Boolean selection — typically "everything" for a full truncate, or a flagged subset for a partial clear. Wrapping delete-then-import in one process makes the refresh atomic and repeatable.

The selection is a **Boolean line item** in a module dimensioned by the numbered list: `TRUE` = delete this item.

Why idiomatic:

- **Performance (PLANS):** keeps the list at its true working size instead of accumulating dead rows.
- **Sustainable:** the process runs hands-off each cycle; no manual list pruning.

## Blueprint

**`SYS60 Transaction Housekeeping`** — `Applies To` G3 Transactions (the numbered list):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Delete? (all) | Boolean | None | G3 Transactions | `TRUE` *(full truncate)* |
| Delete? (stale) | Boolean | None | G3 Transactions | `DAT01.Order Date < SYS90 Model Settings.Retain From` *(partial)* |

**Process `Reload Transactions`:**

1. **DELETE action** — "Delete from List using Selection", selection = `SYS60.Delete? (all)`.
2. **Import action** — load the fresh file into `DAT01 Transactions`.

## Formula(s)

There's no formula that deletes — deletion is an **action**. The formula just defines the *selection* the action consumes.

Full truncate (delete every item):

```
// SYS60 Transaction Housekeeping -> Delete? (all)
TRUE
```

Partial clear (only items older than a retention cutoff):

```
// SYS60 Transaction Housekeeping -> Delete? (stale)
DAT01 Transactions.Order Date < SYS90 Model Settings.Retain From
```

Then in the **action setup**: choose "Delete from List using Selection", point it at the numbered list, and set the criteria to the Boolean line item above. Add it as **step 1** of the reload process, with the import as step 2.

## Pitfalls / gotchas

- **Order matters:** delete first, then import. If you import first then delete-all, you wipe the data you just loaded.
- **A full-truncate DELETE is destructive by design.** Guard it: only run inside the controlled process, and make sure the import step is reliable (a failed import after a successful delete leaves you empty). Consider load-then-validate-then-delete-old for safety-critical feeds.
- **DELETE uses a Boolean selection**, not "delete all" magic — the `TRUE` line item *is* "select all". Double-check the selection module is dimensioned by the right list.
- Deleting renumbers nothing you rely on — that's why a **stable code** matters (see [numbered-list-transactions](numbered-list-transactions.md)); never key downstream logic off the internal number.
- In **deployed/ALM** models, confirm the list is a production list and the action is permitted.

## Performance & PLANS notes

- Clearing dead rows is one of the cheapest **Performance** wins on a data hub — cell count is driven by list size.
- An atomic delete+import **process** is **Sustainable**: it runs the same way every cycle with no manual steps.
- For feeds where deletes are rare, prefer **delta upsert** ([incremental-delta-import](../data-and-imports/incremental-delta-import.md)) over truncate-and-reload to save load time.

## Related

- [`docs/04-integration/actions-and-processes.md`](../../docs/04-integration/actions-and-processes.md)
- [`docs/01-fundamentals/numbered-lists-and-subsets.md`](../../docs/01-fundamentals/numbered-lists-and-subsets.md)
- Recipes: [numbered-list-transactions](numbered-list-transactions.md) · [incremental-delta-import](../data-and-imports/incremental-delta-import.md) · [handle-import-errors-and-dump-files](../data-and-imports/handle-import-errors-and-dump-files.md)
