# Dynamic time filter (SYS boolean time module)

> **Level:** L2 · **Area:** UX & Workflow · **PLANS:** Sustainable, Performance · **DISCO:** System

## The ask

"The forecast page should only show the open forecast months, the actuals review only closed months, and next quarter's board only the next three months — and all of it should advance automatically each month."

## When you'll see this

- Pages that should display a *moving* set of periods (current quarter, next 3 months, YTD).
- Hiding closed/locked periods from a planning view.
- Any filter on Time that must update itself as time moves.

## Approach

Build a `SYS01 Time Filters` module with one **Boolean line item per filter intent** (`Show Forecast Months?`, `Show Current Quarter?`, etc.), each dimensioned by **Time**. Apply the relevant Boolean as the **filter** on a grid/chart. The Booleans derive from a single source-of-truth `SYS90 Model Settings` (the current period and last actual month) and the period index in `SYS01 Time Settings`, so every filtered page advances automatically — no manual re-pointing.

```
Show Forecast Months? = period is after the last actual month
```

Why idiomatic:

- **Sustainable (PLANS):** filters are data-driven off one setting; the roll-forward is automatic.
- **Performance:** filtering to fewer visible periods lightens the page; reusing one Boolean avoids duplicated filter logic.

## Blueprint

**`SYS90 Model Settings`** — the single source of "now" (global cells):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Last Actual Month | Time period | None | *(none)* | *(input each close)* |
| Current Period Index | Number | None | *(none)* | `LOOKUP/derived index of the current month` |

**`SYS01 Time Settings`** — period scaffolding, `Applies To` Time (shared with the time recipes):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Period Index | Number | None | Time | `CUMULATE(1)` |
| Is Actual? | Boolean | None | Time | `START() <= START(SYS90 Model Settings.Last Actual Month)` |

**`SYS01 Time Filters`** — one Boolean per intent, `Applies To` Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Show Forecast Months? | Boolean | None | Time | `NOT SYS01 Time Settings.Is Actual?` |
| Show Current Quarter? | Boolean | None | Time | `QUARTERVALUE-based test` (see formula) |
| Show Next 3 Months? | Boolean | None | Time | `Period Index > Current Period Index AND Period Index <= Current Period Index + 3` |

## Formula(s)

Closed vs open months from one cutoff:

```
// SYS01 Time Filters -> Show Forecast Months?
NOT SYS01 Time Settings.Is Actual?
```

Where `Is Actual?` (in `SYS01 Time Settings`) is:

```
// SYS01 Time Settings -> Is Actual?
START() <= START(SYS90 Model Settings.Last Actual Month)
```

"Next 3 months" using the period index (see [rolling-forecast](../time-and-forecasting/rolling-forecast.md) for `Period Index = CUMULATE(1)`):

```
// SYS01 Time Filters -> Show Next 3 Months?
SYS01 Time Settings.Period Index > SYS90 Model Settings.Current Period Index
AND SYS01 Time Settings.Period Index <= SYS90 Model Settings.Current Period Index + 3
```

Apply the Boolean as the **grid/card filter** on Time — no formula on the displayed module changes.

## Pitfalls / gotchas

- **Filter ≠ Time Range.** A filter hides periods from *view*; a Time Range actually removes them from the *module* (cell count). Use a filter for "what to show", a Time Range for "what to store" (see [shrink-with-subsets-and-time-ranges](../performance/shrink-with-subsets-and-time-ranges.md)).
- **Drive from one setting.** Don't hard-code `Time = Q2 25` in a filter; base every Boolean on `Last Actual Month` / current index so it self-advances (*Sustainable*).
- The filter Boolean must be **dimensioned by Time** (and only Time, usually) to apply cleanly to the Time axis.
- A blank/unset `Last Actual Month` makes every period "forecast" or "actual" — validate the setting on an admin board.
- Multiple intents = multiple Booleans; don't overload one Boolean with `OR` logic that no single page actually wants.

## Performance & PLANS notes

- One System filter module feeds every page's Time filter — **Necessary** + **Sustainable**, and it advances itself.
- Showing fewer periods speeds page render; combine with Time Ranges to cut underlying cell count too.
- These same Booleans can drive forecast logic and DCA (lock actual months) — calculate once, reuse.

## Related

- [`docs/02-formulas/time-functions.md`](../../docs/02-formulas/time-functions.md)
- [`docs/07-performance/time-ranges.md`](../../docs/07-performance/time-ranges.md)
- Recipes: [rolling-forecast](../time-and-forecasting/rolling-forecast.md) · [actual-forecast-switchover](../time-and-forecasting/actual-forecast-switchover.md) · [shrink-with-subsets-and-time-ranges](../performance/shrink-with-subsets-and-time-ranges.md)
