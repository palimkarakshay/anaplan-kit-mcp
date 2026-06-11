# Latest non-blank (carry forward last value)

> **Level:** L2 · **Area:** Hierarchies & Lists · **PLANS:** Logical, Sustainable · **DISCO:** Calculations

## The ask

"Planners only enter the headcount (or a price, or an FX rate) in the months it changes. For every other month, just keep showing the last value they typed."

## When you'll see this

- Sparse inputs that should persist until changed (prices, rates, run-rates, balances).
- "Last known value" / carry-forward / fill-right behaviour.
- A balance that rolls forward when no transaction occurs.

## Approach

Carry the previous period's *result* forward whenever the current input is blank, using the prior period as the fallback. The clean pattern is a self-referencing line item using **`PREVIOUS`** (the value of this same line item in the prior period):

```
Effective = IF NOT ISBLANK(Input) THEN Input ELSE PREVIOUS(Effective)
```

`PREVIOUS(x)` returns `x` from the immediately prior period. Because `Effective` references its own previous value, the last typed input propagates forward until a new input appears.

Why idiomatic:

- **Logical (PLANS):** one stepped line item expresses "keep the last value".
- **Sustainable:** works for any timescale and survives new periods with no edits.

## Blueprint

**`INP70 Sparse Inputs`** — `Applies To` Item × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Entered Value | Number | Sum | Item, Time | *(input — left blank between changes)* |

**`CAL150 Carry Forward`** — `Applies To` Item × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Effective Value | Number | Sum | Item, Time | `IF NOT ISBLANK(INP70.Entered Value) THEN INP70.Entered Value ELSE PREVIOUS(Effective Value)` |

## Formula(s)

Carry the last entered value forward (self-referencing on the prior period):

```
// CAL150 Carry Forward -> Effective Value
IF NOT ISBLANK(INP70 Sparse Inputs.Entered Value)
THEN INP70 Sparse Inputs.Entered Value
ELSE PREVIOUS(Effective Value)
```

To detect blanks on a **Number** line item, prefer `ISBLANK`. (Note `0` is a real value, not blank — if planners type `0` to mean "reset to zero", that's respected; if they leave it empty, it's blank and carries forward.)

If the source line item is text or you want "first period defaults to a seed":

```
IF NOT ISBLANK(Entered Value) THEN Entered Value ELSE PREVIOUS(Effective Value)
// PREVIOUS at the very first period returns blank/zero — seed it if needed
```

## Pitfalls / gotchas

- **`0` vs blank.** `ISBLANK` is true only for genuinely empty cells. If a planner can legitimately enter `0`, this is what you want. If `0` should *not* reset the carry, you need a different sentinel (e.g. a separate "is set?" Boolean).
- **First period has no previous** — `PREVIOUS` returns blank/zero there. Seed the opening value if the series should start populated.
- **Self-reference is allowed across Time** (the prior period), but a line item cannot reference its own *current* period — keep the recursion strictly on `PREVIOUS`.
- Carry-forward across a **Time Range** boundary can surprise you — confirm the prior period exists in the line item's time range.
- Don't confuse this with `CUMULATE` (a running *sum*); this carries the *last value*, it doesn't add.

## Performance & PLANS notes

- One self-referencing line item is cheaper and clearer than nested `IF`s checking many prior periods.
- `PREVIOUS` is engine-native; the recursion is a single backward pass along Time.
- Keep the carry-forward in a **Calc** module separate from the sparse **Input** so typing doesn't drag extra cells.

## Related

- [`docs/02-formulas/time-functions.md`](../../docs/02-formulas/time-functions.md)
- Recipes: [prior-year-comparison](../time-and-forecasting/prior-year-comparison.md) · [actual-forecast-switchover](../time-and-forecasting/actual-forecast-switchover.md) · [ytd-mtd-qtd](../time-and-forecasting/ytd-mtd-qtd.md)
