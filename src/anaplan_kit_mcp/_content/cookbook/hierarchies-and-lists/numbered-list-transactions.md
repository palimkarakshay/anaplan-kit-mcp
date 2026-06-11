# Model transactional data with a numbered list

> **Level:** L2 · **Area:** Hierarchies & Lists · **PLANS:** Performance, Logical · **DISCO:** Data

## The ask

"We get a feed of individual sales orders — thousands a day, each with a customer, product, date and amount. How do I hold these in Anaplan without inventing a unique code for every row?"

## When you'll see this

- Transactional/line-level data: orders, journals, invoices, GL postings.
- Many rows that don't have a natural single-column ID, or where you don't want to manage codes by hand.
- The landing module of a data hub.

## Approach

Use a **numbered list**. Unlike a regular list (where each item needs a unique code/name you manage), a numbered list lets Anaplan key items by an internal number, while you store the real attributes (customer, product, amount) as **properties or line items**. You still give it a **stable text code** (often a [concatenated key](../data-and-imports/concatenated-key-for-imports.md)) so imports upsert instead of duplicating.

Pattern:

- One numbered list = one transactional grain (one item per order line).
- Attributes live as line items in a **Data** module dimensioned by that list.
- Roll the transactions up to planning dimensions with `SUM` over mapping line items.

Why idiomatic:

- **Performance (PLANS):** a numbered list with line-item properties is far leaner than dimensioning a module by Customer × Product × Date (mostly empty cells).
- **Logical:** transactions land flat and faithful, then aggregate to the dimensions you plan by.

## Blueprint

**List `G3 Transactions`** — numbered list, code = concatenated key.

**`DAT01 Transactions`** — `Applies To` G3 Transactions:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Customer | List: Customer | None | G3 Transactions | *(import target)* |
| Product | List: Product | None | G3 Transactions | *(import target)* |
| Order Date | Date | None | G3 Transactions | *(import target)* |
| Amount | Number | Sum | G3 Transactions | *(import target)* |
| Order Month | Time period | None | G3 Transactions | *(derived from Order Date for mapping)* |

**`CAL160 Sales by Customer/Month`** — `Applies To` Customer × Time (the planning grain):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Revenue | Number | Sum | Customer, Time | `DAT01 Transactions.Amount[SUM: DAT01 Transactions.Customer, SUM: DAT01 Transactions.Order Month]` |

## Formula(s)

Aggregate the flat transactions up to the planning dimensions using the line-item attributes as mappings:

```
// CAL160 -> Revenue
DAT01 Transactions.Amount[SUM: DAT01 Transactions.Customer, SUM: DAT01 Transactions.Order Month]
```

The two `SUM` mappings (Customer and Order Month) move the per-transaction `Amount` to the Customer × Time grid. Each mapping line item must be formatted as the target dimension (Customer as a list; Order Month as Time).

## Pitfalls / gotchas

- **Always give a stable code** (concatenated key) so re-importing updates rows rather than appending duplicates. A pure numbered list with no code is hard to reconcile.
- **Don't plan directly on the transaction list.** It's a Data landing zone — aggregate to planning dimensions in Calc, then plan there.
- **Numbered lists grow** — pair with a [clear/DELETE action](clear-a-numbered-list.md) for reload housekeeping and watch the list maximum.
- Mapping line items must be the **right format** (list / Time), not text — resolve text codes with [FINDITEM](finditem-text-key.md) first.
- Be deliberate about **summary methods**: `Amount` must `Sum`; attribute line items use `None`.

## Performance & PLANS notes

- A numbered list avoids the sparsity explosion of dimensioning by every transactional attribute — a major **Performance** win.
- Keep history in the hub on a numbered list; spokes receive only the **aggregated** result, staying small.
- Reload with truncate-and-load (clear then import) or delta (upsert on the key) — see Related.

## Related

- [`docs/01-fundamentals/numbered-lists-and-subsets.md`](../../docs/01-fundamentals/numbered-lists-and-subsets.md)
- Recipes: [concatenated-key-for-imports](../data-and-imports/concatenated-key-for-imports.md) · [clear-a-numbered-list](clear-a-numbered-list.md) · [finditem-text-key](finditem-text-key.md) · [incremental-delta-import](../data-and-imports/incremental-delta-import.md)
