# Concatenated key for imports

> **Level:** L2 · **Area:** Data & Imports · **PLANS:** Logical, Sustainable · **DISCO:** Data / System

## The ask

"The GL file has one row per Entity + Account + Month, but there's no single ID column. How do I get this to land on the right cell in Anaplan without duplicates?"

## When you'll see this

- Transactional data is unique only on a **combination** of columns, not one ID.
- You load into a **numbered list** that needs a stable, unique code per row.
- You're matching a flat file back to items you created on a previous load.

## Approach

Build a **concatenated key** — a single text field that joins the columns that together make a row unique, e.g. `Entity#Account#YYYYMM`. You use it two ways:

1. As the **code** of a numbered-list item (so an import upserts the same row instead of duplicating it).
2. As the **match key** on the import action, so a delta load lands on the right existing row.

Put a separator (`#`, `|`) between parts so `12` + `34` can't collide with `1` + `234`.

Why idiomatic:

- **Logical (PLANS):** the key encodes exactly the dimensionality that makes a row unique.
- **Sustainable:** a stable key makes imports idempotent — re-running a load updates rather than duplicates. This is what makes [incremental delta imports](incremental-delta-import.md) safe.

Best practice: build the key **once** in a System module (or in the source extract) and reference it — don't re-concatenate in five places.

## Blueprint

**`DAT01 GL Transactions`** — dimensioned by numbered list `G3 Transactions`:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Entity Code | Text | None | G3 Transactions | *(import target)* |
| Account Code | Text | None | G3 Transactions | *(import target)* |
| Period (YYYYMM) | Text | None | G3 Transactions | *(import target)* |
| Match Key | Text | None | G3 Transactions | `Entity Code & "#" & Account Code & "#" & Period (YYYYMM)` |
| Amount | Number | Sum | G3 Transactions | *(import target)* |

The **numbered list code** is set to `Match Key` on import, making each Entity#Account#Month combination a single, reusable item.

## Formula(s)

Concatenate with `&` and a separator. Pad/normalise parts so they're stable:

```
// DAT01 GL Transactions -> Match Key
Entity Code & "#" & Account Code & "#" & Period (YYYYMM)
```

Anaplan has **no generic `TEXT(number)`** function, so you can't naively cast `YEAR()`/`MONTH()` (which return numbers) to text. Two correct ways to get a `YYYYMM` text part:

```
// 1) The period part is a Time line item -> use NAME() to get its label text
NAME(Posting Period)     // e.g. "Mar 24" or "Mar 2024" depending on the calendar's display
```

`NAME(item)` returns the text name of a **list item** (including a Time period), so a Time-formatted line item gives clean period text without numeric casting. The catch: `NAME` returns the period's *display label*, not a guaranteed `YYYYMM`. To get a strict, zero-padded `YYYYMM` (`2024-01`, not `2024-1`):

```
// 2) Map a SYS01 Time Settings text attribute per period (built once, correctly padded)
SYS01 Time Settings.Period YYYYMM[LOOKUP: <period mapping>]
```

where `SYS01 Time Settings.Period YYYYMM` is a **Text** line item holding the pre-padded `YYYYMM` for each period (maintained once, by import or a manual one-off). For a date-driven period, the cleanest option is still to produce the padded key in the **source extract**, where `01`..`12` padding is trivial — Anaplan can't zero-pad a number into text on its own.

## Pitfalls / gotchas

- **Always use a separator.** `Entity & Account` makes `1`+`23` indistinguishable from `12`+`3`. `1#23` vs `12#3` is safe.
- **Codes, not names.** Concatenate stable codes; names change and aren't unique.
- **Normalise case and padding.** `ABC` ≠ `abc` and `2024-1` ≠ `2024-01`. Decide a canonical form and produce it consistently on both the file and the model side.
- A number can't be `&`-joined to text directly, and Anaplan has **no generic `TEXT(number)`**. Use `NAME(item)` for a list/Time item, build the text part from a SYS text attribute, or pad it in the source extract.
- If the key isn't truly unique, the upsert overwrites silently — you lose rows and won't see an error. Confirm uniqueness in the source.

## Performance & PLANS notes

- Build the key in **one** line item (or the extract) and reference it everywhere — satisfies **Necessary** (no duplicated concatenation logic).
- A stable text key on a numbered list is the foundation for delta loads, dump-file reconciliation, and clearing transactional data — see the Related recipes.
- Keep the key as **Text**; don't try to make it a list-formatted lookup unless you genuinely need `FINDITEM` resolution.

## Related

- [`docs/04-integration/imports-exports.md`](../../docs/04-integration/imports-exports.md)
- [`docs/01-fundamentals/numbered-lists-and-subsets.md`](../../docs/01-fundamentals/numbered-lists-and-subsets.md)
- Recipes: [incremental-delta-import](incremental-delta-import.md) · [numbered-list-transactions](../hierarchies-and-lists/numbered-list-transactions.md) · [finditem-text-key](../hierarchies-and-lists/finditem-text-key.md) · [handle-import-errors-and-dump-files](handle-import-errors-and-dump-files.md)
