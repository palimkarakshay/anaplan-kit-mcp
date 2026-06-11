# Resolve a text code to a list item (FINDITEM)

> **Level:** L2 · **Area:** Hierarchies & Lists · **PLANS:** Logical, Sustainable · **DISCO:** System / Calculations

## The ask

"The imported file has cost-centre *codes* as plain text. I need those to become real Cost Centre list items so I can map and roll up by them."

## When you'll see this

- A landing/Data module holds a text code that needs to point at a list item.
- Building a concatenated key and turning it back into a list reference.
- Any time you have text and need the matching list member for `LOOKUP`/`SUM`.

## Approach

**`FINDITEM`** converts text into a list item. `FINDITEM(List, "text")` returns the member of `List` whose name/code matches the text, or blank if none matches. The result line item **must be formatted as that list**. Once you have a list-formatted line item, you can use it as the locator in `LOOKUP`/`SUM`.

Confirmed syntax (Anapedia): `FINDITEM(List, text)` — set the result line item's format to the same List.

Why idiomatic:

- **Sustainable (PLANS):** new codes resolve automatically as long as the list member exists — no formula edits.
- **Logical:** text-to-item is an explicit, single step that makes downstream mapping clean.

## Blueprint

**`DAT01 Landing`** — text codes from the file, `Applies To` G3 Transactions (numbered list):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| CC Code (text) | Text | None | G3 Transactions | *(import target)* |

**`SYS50 Code Resolution`** — turn text into list items, `Applies To` G3 Transactions:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Cost Centre | List: Cost Centre | None | G3 Transactions | `FINDITEM(Cost Centre, DAT01 Landing.CC Code (text))` |
| Resolved? | Boolean | None | G3 Transactions | `NOT ISBLANK(Cost Centre)` |

## Formula(s)

Resolve the text code to a Cost Centre item (result line item formatted as `Cost Centre`):

```
// SYS50 Code Resolution -> Cost Centre
FINDITEM(Cost Centre, DAT01 Landing.CC Code (text))
```

Flag rows that didn't match so you can review them:

```
// SYS50 Code Resolution -> Resolved?
NOT ISBLANK(Cost Centre)
```

Then map data using the resolved item — e.g. aggregate landing rows up to the Cost Centre list:

```
// CAL -> Amount by Cost Centre
DAT01 Landing.Amount[SUM: SYS50 Code Resolution.Cost Centre]
```

## Pitfalls / gotchas

- **Result format must be the list.** A `FINDITEM` result line item formatted as Text won't compile — format it as the target List.
- **`FINDITEM` matches on the item's name/code** as stored. Case and exact spelling matter; `"ABC "` with a trailing space won't match `"ABC"`. Trim/normalise upstream.
- **No match → blank.** Always pair with a `Resolved?` Boolean so unmatched codes are visible, not silently dropped.
- For **numbered lists**, behaviour depends on the display name/code setup — confirm what you're matching against (see the Anapedia note on numbered-list FINDITEM).
- In **Polaris**, `FINDITEM` can't be used on the Time dimension or on Formula/Ratio summary line items — confirm engine constraints.
- Prefer resolving **once** in a SYS module over calling `FINDITEM` repeatedly across calcs (**Necessary**).

## Performance & PLANS notes

- Resolve text→item **once** and reference the list-formatted line item everywhere downstream.
- A list-formatted result is what makes `SUM`/`LOOKUP` mapping possible — text alone can't be a mapping locator.
- Keep resolution in **System/Data**; the resolved item then drives Calc modules.

## Related

- [`docs/02-formulas/hierarchy-functions.md`](../../docs/02-formulas/hierarchy-functions.md)
- Recipes: [concatenated-key-for-imports](../data-and-imports/concatenated-key-for-imports.md) · [sum-lookup-remap](../mapping-and-allocation/sum-lookup-remap.md) · [numbered-list-transactions](numbered-list-transactions.md)
