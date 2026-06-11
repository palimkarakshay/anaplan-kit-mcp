# Incremental / delta import (load only changed rows)

> **Level:** L2 · **Area:** Data & Imports · **PLANS:** Performance, Sustainable · **DISCO:** Data

## The ask

"The full Actuals extract is 40 million rows and takes 50 minutes to load every night. We only ever change last month — can't we just load what's new?"

## When you'll see this

- A source table is huge but day-to-day changes are tiny.
- Nightly load windows are tight and a full reload doesn't fit.
- The source system can give you a "modified since" or change-flag column.

## Approach

Load a **delta**: only the rows that changed since the last successful load, instead of truncate-and-reload. The cleanest delta is driven by the *source*, not by Anaplan guessing — ask for a `Last Modified` timestamp or a `Change Flag` in the extract.

Two patterns, in order of preference:

1. **Source-filtered file** — the source system exports only changed rows (e.g. `WHERE modified_date >= :lastRun`). Anaplan just imports that small file. Best for performance.
2. **Anaplan-side delta** — you import the full file but the source includes a change flag/timestamp; you only act on flagged rows.

Why this is idiomatic: it serves **Performance** (small loads recalc fast) and **Sustainable** (the import keeps working as volumes grow). Crucially, an import in Anaplan is an **upsert** — matched keys update in place, unmatched keys are added — so loading only changed rows leaves everything else untouched.

## Blueprint

**`DAT01 Actuals (landing)`** — numbered list `G3 Transactions` keyed by a concatenated key (see [concatenated-key-for-imports](concatenated-key-for-imports.md)):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Amount | Number | Sum | G3 Transactions | *(import target)* |
| Last Modified | Date | None | G3 Transactions | *(import target)* |
| Match Key | Text | None | G3 Transactions | *(import target — unique key)* |

**`DAT90 Load Control`** — a one-cell module (no dimension) that records watermark + counts:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Last Successful Load | Date | None | *(none)* | *(set by import / manual)* |
| Rows in Last Delta | Number | None | *(none)* | *(set by import)* |

## Formula(s)

The delta logic mostly lives in the **import action** mapping and the source query, not in a formula. The key Anaplan-side choices:

- In the import action, map on the **unique key** so updates land on the right row:

```
Map "Match Key" (file) -> "Match Key" (list code)
```

- Use **"Update existing items"** and **"Add new items"** on the action; leave **"Delete omitted items" OFF** — otherwise an incremental file would delete every row not in the delta.

If you must compute a change flag inside Anaplan after a full load:

```
// CAL01 Delta -> Changed?
DAT01 Actuals.Last Modified > DAT90 Load Control.Last Successful Load
```

## Pitfalls / gotchas

- **Never tick "Delete omitted items" on a delta import** — it will wipe everything not in today's small file. This is the classic data-loss mistake.
- Deletes are the hard part: an incremental file *adds and updates* but won't remove rows the source deleted. Handle deletes with a separate flagged file or a periodic full reconcile.
- The match key must be **truly unique and stable**. If the key changes, the upsert creates duplicates instead of updating.
- Watermark drift: if a load half-fails, your "last successful load" date may be wrong. Only advance the watermark on confirmed success.
- Reconcile counts periodically against a full row count — see [reconciliation-check-module](../performance/reconciliation-check-module.md).

## Performance & PLANS notes

- Smaller imports = shorter recalc and shorter load windows. This is one of the biggest **Performance** wins available on a data hub.
- A numbered list with a stable key is what makes the upsert reliable and keeps the list from ballooning with duplicates.
- Schedule a full reconcile (weekly/monthly) so small drift never becomes large drift.

## Related

- [`docs/04-integration/imports-exports.md`](../../docs/04-integration/imports-exports.md)
- [`docs/04-integration/actions-and-processes.md`](../../docs/04-integration/actions-and-processes.md)
- Recipes: [build-a-data-hub](build-a-data-hub.md) · [concatenated-key-for-imports](concatenated-key-for-imports.md) · [handle-import-errors-and-dump-files](handle-import-errors-and-dump-files.md) · [reconciliation-check-module](../performance/reconciliation-check-module.md)
