# Build a data hub

> **Level:** L2 · **Area:** Data & Imports · **PLANS:** Sustainable, Necessary · **DISCO:** Data / System

## The ask

"We've got Actuals coming out of the GL, the HR headcount feed, and a product master. Three different planning teams keep importing the same files into their own models and the numbers never tie. Can you give us one clean source everyone pulls from?"

## When you'll see this

- More than one model needs the *same* master data (lists, attributes, actuals).
- The same CSV is being imported into several models, drifting out of sync.
- You're standing up a new Anaplan estate and want it right from day one.

## Approach

Build a **data hub**: a dedicated model whose only job is to receive source data, clean it, and **publish** it to "spoke" models. Data flows **one direction** — source system → hub → spokes. Spokes never import raw files and never write back to the hub.

Why this is the Anaplan-idiomatic way:

- **Sustainable (PLANS):** one import to maintain, one place lists are mastered. Add a new spoke and you wire it to the hub, not to the source files again.
- **Necessary:** the same row of Actuals is stored and validated once, not N times.
- **Logical:** clear, traceable, one-directional flow with no circular dependencies between models.

The hub is almost entirely **D** (Data — landing modules) and **S** (System — attribute/mapping modules). It holds *no* planning logic. Spokes import *from the hub's export views or saved views*, usually via a **process** so the steps run in order.

## Blueprint

**Lists in the hub** (mastered here, exported to spokes):

| List | Type | Notes |
| --- | --- | --- |
| `Entity` | Hierarchy | Legal entity / cost-centre tree |
| `Account` | Hierarchy | GL account structure |
| `Product` | Flat or hierarchy | Product master |
| `G3 Transactions` | Numbered list | Raw GL rows (see [numbered-list-transactions](../hierarchies-and-lists/numbered-list-transactions.md)) |

**`DAT01 Actuals (landing)`** — faithful copy of the GL feed, dimensioned by Entity × Account × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Amount | Number | Sum | Entity, Account, Time | *(import target — no formula)* |
| Source loaded? | Boolean | None | Entity, Account, Time | `Amount <> 0` |

**`SYS03 Account Details`** — attributes used by every spoke (built once):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Account Type | Text | None | Account | *(import target)* |
| Sign Flip? | Boolean | None | Account | *(import target)* |
| P&L Group | List: P&L Groups | None | Account | *(import target)* |

**`OUT01 Actuals (publish view)`** — a saved view shaped exactly for the spoke's import (only the cells a spoke needs).

## Formula(s)

The hub does little calculation. A typical published value applies the sign convention once so every spoke gets clean numbers:

```
// CAL01 Actuals Clean -> Amount Signed
DAT01 Actuals.Amount * IF SYS03 Account Details.Sign Flip? THEN -1 ELSE 1
```

Spokes then import the saved view of `OUT01` / `CAL01`. No formula in the spoke re-derives the sign — it's done once, in the hub.

## Pitfalls / gotchas

- **Never let a spoke write back to the hub.** That creates a two-way flow and an ALM/architecture nightmare. Hub → spoke only.
- **Master each list in exactly one place.** If `Product` lives in the hub, spokes receive it by import — they don't maintain their own copy.
- Don't put planning logic in the hub. It's D + S only; calculations belong in spokes.
- Use **saved views** as import sources so a spoke import doesn't break when you add a hub line item.
- Keep landing modules **flat and faithful** — clean/transform in a separate calc step, not in the landing module.

## Performance & PLANS notes

- A hub keeps spokes *small*: they hold only what they plan with, not the full transaction history.
- Use **Time Ranges** on landing modules so old actuals don't bloat cell count (see [shrink-with-subsets-and-time-ranges](../performance/shrink-with-subsets-and-time-ranges.md)).
- Drive the load order with a **process** so list updates run before the data import that references them.

## Related

- [`docs/04-integration/imports-exports.md`](../../docs/04-integration/imports-exports.md)
- [`docs/04-integration/actions-and-processes.md`](../../docs/04-integration/actions-and-processes.md)
- [`docs/03-methodology/disco.md`](../../docs/03-methodology/disco.md)
- Recipes: [incremental-delta-import](incremental-delta-import.md) · [auto-create-list-members](auto-create-list-members.md) · [concatenated-key-for-imports](concatenated-key-for-imports.md)
