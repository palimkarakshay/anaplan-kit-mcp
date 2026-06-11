# Currency conversion (local → reporting)

> **Level:** L2 · **Area:** Financial Calcs · **PLANS:** Sustainable, Logical · **DISCO:** System / Calculations

## The ask

"Each entity reports in its own currency. Consolidate everything to USD using the month's exchange rate."

## When you'll see this

- Multi-entity models where entities transact in different currencies.
- Group consolidation that reports in one currency.
- Any model with an FX rate table.

## Approach

Keep three things separate: the **local amount**, a **rate table** (System), and the **converted amount** (calc). Each entity has a local currency (an attribute), and you look up the right rate per currency × month. Don't bury currency in formulas — drive it from a `SYS` mapping so adding an entity/currency needs no formula change.

```
reporting amount = local amount × rate(entity's currency, this month)
```

Use the correct rate type per line: **average** rate for P&L flows, **closing** rate for balance-sheet positions.

Why idiomatic:

- **Sustainable (PLANS):** rates and currency assignments are data; new currency = new rows, not new formulas.
- **Logical:** local, rate, and reporting are distinct, traceable line items.

## Blueprint

**`SYS02 Organization Details`** — each cost centre's local currency, `Applies To` L3 Cost Centre:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Local Currency | List: Currency | None | L3 Cost Centre | *(mapping/input)* |

**`INP40 FX Rates`** — `Applies To` Currency × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Average Rate | Number | None | Currency, Time | *(input/import — to USD)* |
| Closing Rate | Number | None | Currency, Time | *(input/import — to USD)* |

**`CAL100 Reporting Values`** — `Applies To` L3 Cost Centre × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Local Amount | Number | Sum | L3 Cost Centre, Time | *(from source, in local ccy)* |
| FX Rate | Number | None | L3 Cost Centre, Time | `INP40 FX Rates.Average Rate[LOOKUP: SYS02 Organization Details.Local Currency]` |
| Reporting Amount (USD) | Number | Sum | L3 Cost Centre, Time | `Local Amount × FX Rate` |

## Formula(s)

Pull each entity's rate via its currency (rate table is by Currency × Time; entity maps to a currency):

```
// CAL100 -> FX Rate
INP40 FX Rates.Average Rate[LOOKUP: SYS02 Organization Details.Local Currency]
```

Convert:

```
// CAL100 -> Reporting Amount (USD)
Local Amount * FX Rate
```

Balance-sheet items use the closing rate instead:

```
INP40 FX Rates.Closing Rate[LOOKUP: SYS02 Organization Details.Local Currency]
```

## Pitfalls / gotchas

- **Rate direction.** Be explicit whether rates are "1 local = X USD" or "1 USD = X local". Multiply vs divide accordingly, and document it on the rate line item.
- **Average vs closing.** P&L flows use the period average; balance-sheet positions use the closing rate. Mixing them is a classic restatement error.
- **Missing rate = blank/zero conversion.** A currency with no rate row silently zeros out. Flag missing rates (`ISBLANK(FX Rate)`).
- Don't hard-code currency with `SELECT: Currency.USD` — map via `SYS02 Organization Details` (*Sustainable*).
- Aggregating converted amounts up the org hierarchy is fine **after** conversion; never sum local amounts of different currencies before converting.

## Performance & PLANS notes

- One rate table + one currency mapping feed the whole model (**Necessary**, **Sustainable**).
- `LOOKUP` against the rate table is engine-native and cheap.
- For constant-currency / plan-rate restatement (strip out FX movement), see [fx-restatement](fx-restatement.md).

## Related

- [`docs/02-formulas/lookup-and-mapping.md`](../../docs/02-formulas/lookup-and-mapping.md)
- Recipes: [fx-restatement](fx-restatement.md) · [sum-lookup-remap](../mapping-and-allocation/sum-lookup-remap.md) · [variance-waterfall-bridge](variance-waterfall-bridge.md)
