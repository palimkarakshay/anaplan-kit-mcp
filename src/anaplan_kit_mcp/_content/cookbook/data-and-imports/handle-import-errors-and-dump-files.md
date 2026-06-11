# Handle import errors & dump files

> **Level:** L2 · **Area:** Data & Imports · **PLANS:** Auditable, Sustainable · **DISCO:** Data

## The ask

"The nightly load 'succeeded' but the totals are short by £2m. The integration team says Anaplan accepted the file. Where did the missing rows go?"

## When you'll see this

- An import reports success but the numbers don't tie to the source.
- Rows reference list items or periods that don't exist yet, so they silently drop.
- You need to prove to Finance that every source row was either loaded or accounted for.

## Approach

Every Anaplan import produces an **import result**: how many rows succeeded, how many were **ignored**, and how many **failed** — plus a downloadable **dump file** containing the rejected rows and the reason each was rejected. The fix is never "hope it works"; it's **reconcile counts every run** and **read the dump file** when they don't match.

Key behaviours to internalise:

- **Ignored** rows are usually *unmatched mappings* (a code or period not in the target list/time). They don't error — they just don't load. This is the silent £2m.
- **Failed** rows break a hard rule (wrong format, duplicate key where uniqueness is required).
- The import option **"Ignore" vs "Fail" on errors** decides whether a bad row is skipped or the whole import aborts.

Why idiomatic:

- **Auditable (PLANS):** rows in = rows loaded + rows ignored + rows failed. If that equation doesn't balance, you have an unexplained gap.
- **Sustainable:** a reconciliation step catches new unmapped codes the day they appear, not at month-end close.

## Blueprint

**`DAT90 Load Control`** — one-cell (unmoduled) control totals, set by the import / a follow-on import of the result:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Rows in Source | Number | None | *(none)* | *(from extract row count)* |
| Rows Loaded | Number | None | *(none)* | *(from import result)* |
| Rows Ignored | Number | None | *(none)* | *(from import result)* |
| Rows Failed | Number | None | *(none)* | *(from import result)* |
| Source Total | Number | None | *(none)* | *(source file value total, for the value tie)* |
| Reconciled? | Boolean | None | *(none)* | `Rows in Source = Rows Loaded + Rows Ignored + Rows Failed` |
| Clean Load? | Boolean | None | *(none)* | `Reconciled? AND Rows Ignored = 0 AND Rows Failed = 0` |

**`DAT01 Actuals (landing)`** plus an `Amount` control total to tie value, not just count (see [reconciliation-check-module](../performance/reconciliation-check-module.md)).

## Formula(s)

The reconciliation equation is the whole point — put it in a Boolean so a dashboard can show red/green:

```
// DAT90 Load Control -> Reconciled?
Rows in Source = Rows Loaded + Rows Ignored + Rows Failed
```

```
// DAT90 Load Control -> Clean Load?
Reconciled? AND Rows Ignored = 0 AND Rows Failed = 0
```

Tie on **value** as well as count, because two offsetting wrong rows can net to a right count:

```
// CAL01 Load Check -> Value Tie?
ROUND(DAT01 Actuals.Amount[SUM: ...], 2) = DAT90 Load Control.Source Total
```

## Pitfalls / gotchas

- **"Success" is not "complete".** An import that ignores 10,000 unmatched rows still reports success. Always read the *ignored* count.
- **The dump file is your friend** — download it from the import result. It lists each rejected row and the reason ("invalid list item", "no matching time period").
- Most ignored rows = a **missing list member or period**. Run the list/time imports *before* the data import in your process, or turn on create-on-import (see [auto-create-list-members](auto-create-list-members.md)).
- "Ignore errors" hides problems if you never check the result; "Fail on errors" stops the whole load on one bad row. Pick deliberately and **always reconcile after**.
- Counts can tie while values don't (sign flips, duplicates). Reconcile **both**.

## Performance & PLANS notes

- A reconciliation/control module is cheap (one cell) and is the single best **Auditable** habit on a data hub.
- Capture the result automatically by importing the import-run statistics back into `DAT90 Load Control` via the API/Anaplan Connect, so the check is hands-off.
- Surface `Clean Load?` on an admin board; a red flag should block the downstream publish to spokes.

## Related

- [`docs/04-integration/imports-exports.md`](../../docs/04-integration/imports-exports.md)
- [`docs/04-integration/actions-and-processes.md`](../../docs/04-integration/actions-and-processes.md)
- Recipes: [incremental-delta-import](incremental-delta-import.md) · [reconciliation-check-module](../performance/reconciliation-check-module.md) · [concatenated-key-for-imports](concatenated-key-for-imports.md)
