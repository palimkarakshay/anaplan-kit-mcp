# Actual / forecast switchover

> **Level:** L2 · **Area:** Time & Forecasting · **PLANS:** Sustainable, Logical · **DISCO:** System / Calculations

## The ask

"The current view should show Actuals for closed months and Forecast for everything after. When April closes, April should flip from forecast to actual automatically."

## When you'll see this

- A "Current View" / "Latest Estimate" line that blends actuals-to-date with forecast-to-go.
- The actual/forecast boundary moves each month at close.
- Reporting that must never double-count or show a forecast where an actual exists.

## Approach

Drive the split from a single **cutoff** (the last actual month) held in a settings module, and a per-period Boolean **`Is Actual?`** in `SYS01 Time Settings`. The blended line is one `IF` on that flag — actuals up to and including the cutoff, forecast after.

```
Current View = IF Is Actual? THEN Actuals ELSE Forecast
```

Hold actuals and forecast in **separate** line items/versions and combine in a calc line — don't overwrite forecast cells with actuals (you'd lose the forecast and break auditability).

Why idiomatic:

- **Sustainable (PLANS):** moving the boundary is a one-cell change (`Last Actual Month`); no formula edits at close.
- **Logical:** actuals and forecast stay separate and traceable; the blend is explicit.

## Blueprint

**`SYS90 Model Settings`** — the boundary, one cell:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Last Actual Month | Time period | None | *(none)* | *(input each close)* |

**`SYS01 Time Settings`** — per-period flag, `Applies To` Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Is Actual? | Boolean | None | Time | `START() <= START(SYS90 Model Settings.Last Actual Month)` |

**`CAL70 Current View`** — `Applies To` L3 Cost Centre × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Actuals | Number | Sum | L3 Cost Centre, Time | `DAT01 Actuals.Amount` |
| Forecast | Number | Sum | L3 Cost Centre, Time | `INP Forecast.Amount` |
| Current View | Number | Sum | L3 Cost Centre, Time | `IF SYS01 Time Settings.Is Actual? THEN Actuals ELSE Forecast` |

## Formula(s)

Per-period actual flag (everything up to and including the cutoff is actual):

```
// SYS01 Time Settings -> Is Actual?
START() <= START(SYS90 Model Settings.Last Actual Month)
```

The blended current view:

```
// CAL70 Current View -> Current View
IF SYS01 Time Settings.Is Actual? THEN Actuals ELSE Forecast
```

If you use **Versions** (Actual vs Forecast), the same idea applies with the version switch, but a Boolean-driven blend in a calc module is the most transparent and auditable approach.

## Pitfalls / gotchas

- **Don't import actuals on top of forecast cells.** Keep them separate; blend in a calc line. Otherwise the forecast is destroyed and you can't compare A vs F.
- Off-by-one at the boundary: be deliberate about `<=` vs `<`. The cutoff month should be **actual**, the next month forecast.
- The flag must be one **System** line item reused by the blend, any variance, and DCA (lock actuals) — don't re-derive the boundary in each module.
- If the forecast is supposed to *start from* the latest actual, seed it; a forecast that ignores actuals-to-date will look wrong at the join.
- A frozen prior forecast (for comparison) should be its own version/line — don't let the moving boundary rewrite history.

## Performance & PLANS notes

- One Boolean (`Is Actual?`) drives the blend, variance bridges, and cell locking — calculate once, reuse (**Necessary**, **Sustainable**).
- The blend is a single `IF` on a Boolean — cheap and Auditable; avoid date-comparison `IF`s scattered across modules.
- Pair with [DCA read/write by status](../security-and-dca/dca-read-write-by-status.md) to **lock actual months** so planners can't type over closed periods.

## Related

- [`docs/01-fundamentals/versions.md`](../../docs/01-fundamentals/versions.md)
- [`docs/02-formulas/time-functions.md`](../../docs/02-formulas/time-functions.md)
- Recipes: [rolling-forecast](rolling-forecast.md) · [variance-waterfall-bridge](../financial-calcs/variance-waterfall-bridge.md) · [dca-read-write-by-status](../security-and-dca/dca-read-write-by-status.md)
