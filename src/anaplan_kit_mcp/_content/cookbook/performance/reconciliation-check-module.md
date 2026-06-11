# Reconciliation / control-total check module

> **Level:** L2 · **Area:** Performance · **PLANS:** Auditable, Necessary · **DISCO:** System / Outputs

## The ask

"After every load and every model change, Finance asks 'do the numbers still tie to source?' I want a single red/green light that screams when the model total doesn't match the GL total."

## When you'll see this

- Proving a loaded total matches the source system.
- Catching when a calc, a remap, or a dropped row breaks a total.
- A standing data-quality control before publishing or signing off.

## Approach

Build a small **check module** that computes the difference between two totals that *must* be equal — model vs source — and exposes a Boolean **`Tie?`**. Surface it on an admin board with conditional formatting (green = 0, red = mismatch). It's tiny, cheap, and the single best **Auditable** habit you can add.

```
Difference = Model Total − Source Total
Tie? = ROUND(Difference, 2) = 0
```

Add checks at each risky boundary: post-import (rows/value), post-remap (sum before = sum after), post-allocation (allocated = pool). Reconcile **value and count**, since offsetting errors can net out.

Why idiomatic:

- **Auditable (PLANS):** a number you can trace, with an explicit pass/fail.
- **Necessary:** one cheap control replaces hours of manual tie-outs.

## Blueprint

**`CHK01 Reconciliation`** — one cell per check (no big dimensions needed):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Model Total | Number | None | *(none)* | `CAL P&L.Revenue[SUM: ...]` (full roll-up) |
| Source Total | Number | None | *(none)* | `DAT Actuals.Amount[SUM: ...]` |
| Difference | Number | None | *(none)* | `Model Total - Source Total` |
| Tie? | Boolean | None | *(none)* | `ROUND(Difference, 2) = 0` |
| Row Count Model | Number | None | *(none)* | `DAT Actuals.Has Value?[SUM: ...]` |
| Row Count Source | Number | None | *(none)* | *(from load control)* |
| Count Tie? | Boolean | None | *(none)* | `Row Count Model = Row Count Source` |
| All Checks Pass? | Boolean | None | *(none)* | `Tie? AND Count Tie?` |

## Formula(s)

The core difference and tolerance-aware tie (use `ROUND` so floating pennies don't false-alarm):

```
// CHK01 Reconciliation -> Difference
Model Total - Source Total

// CHK01 Reconciliation -> Tie?
ROUND(Difference, 2) = 0
```

Reconcile counts too (value can tie while rows don't, and vice versa):

```
// CHK01 Reconciliation -> Count Tie?
Row Count Model = Row Count Source
```

Single roll-up light:

```
// CHK01 Reconciliation -> All Checks Pass?
Tie? AND Count Tie?
```

Surface `All Checks Pass?` on a board with conditional formatting (green/red).

## Pitfalls / gotchas

- **Use a tolerance via `ROUND`** for value ties — exact float equality can fail on rounding. Match the rounding to the reporting precision (2dp for currency).
- **Tie on both value and count.** Two wrong rows can offset to the right total; a count check catches that, and vice versa.
- **Make the check dimensionless where possible** (one cell) so it's cheap and unambiguous; don't dimension a control by lists it doesn't need.
- **A green light is only as good as the totals you chose.** Reconcile the *right* boundary — the one that actually breaks (post-import, post-remap, post-allocation).
- Don't bury the check in a calc module — give it its own `CHK`/`SYS` module so it's findable and auditable.

## Performance & PLANS notes

- A check module is tiny (often single cells) — negligible cost for a large **Auditable** payoff.
- Build it once and reuse the pattern at every risky boundary (**Necessary**).
- Wire load statistics into it (via API/Connect) so the control runs hands-off after each load — see [handle-import-errors-and-dump-files](../data-and-imports/handle-import-errors-and-dump-files.md).

## Related

- [`docs/03-methodology/plans-standard.md`](../../docs/03-methodology/plans-standard.md)
- Recipes: [handle-import-errors-and-dump-files](../data-and-imports/handle-import-errors-and-dump-files.md) · [allocate-by-driver](../mapping-and-allocation/allocate-by-driver.md) · [variance-waterfall-bridge](../financial-calcs/variance-waterfall-bridge.md) · [incremental-delta-import](../data-and-imports/incremental-delta-import.md)
