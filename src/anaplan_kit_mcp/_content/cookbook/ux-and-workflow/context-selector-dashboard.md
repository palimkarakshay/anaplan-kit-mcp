# Context selector dashboard

> **Level:** L2 · **Area:** UX & Workflow · **PLANS:** Logical, Sustainable · **DISCO:** Outputs

## The ask

"One budget page that every cost-centre owner uses — they pick their cost centre (and the scenario) at the top, and every grid and chart below updates to that selection."

## When you'll see this

- A single page reused by many users, each filtered to their context.
- A "pick a region / product / version" selector that drives the whole page.
- Standard FP&A input and review boards.

## Approach

In the New UX, a **page selector** (synced selectors / context selectors) sets the current item of a list (and Time/Version) for the whole page or board. Every grid and chart that shares that dimension follows the selection automatically — you don't write a formula to "filter by selection"; you publish modules dimensioned by the same list and let the synced selector drive them.

For logic that must react to the selection (e.g. show the selected item's name in a label), read it with **`ITEM`** in a module dimensioned by that list, or use a single-cell module the selector writes to.

Why idiomatic:

- **Sustainable (PLANS):** one page serves all members; add a cost centre and it just appears in the selector.
- **Logical:** selection is a UX concern; the underlying modules stay clean and dimensioned correctly.

## Blueprint

**Page setup (New UX):**

| Element | Bound to | Notes |
| --- | --- | --- |
| Page/context selector | `Cost Centre` | the dimension users pick |
| Page/context selector | `Version` | Actual / Budget / Forecast |
| Synced selector | `Time` | period or range |
| Grid card | `INP Budget` (Cost Centre × Time) | follows the selectors |
| Chart card | `OUT P&L` (Cost Centre × Time) | follows the selectors |

**`SYS70 Page Context`** (optional, for labels/logic) — a one-cell module the page reads:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Selected Cost Centre | List: L3 Cost Centre | None | *(none)* | *(set by the page selector)* |
| Selected CC Name | Text | None | *(none)* | `NAME(Selected Cost Centre)` |

**`SYS01 Time Filters`** (reused from [dynamic-time-filter](dynamic-time-filter.md)) — a Boolean to drive the page's Time selector so the grid only shows the relevant periods:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Show Forecast Months? | Boolean | None | Time | `NOT SYS01 Time Settings.Is Actual?` |

Apply `Show Forecast Months?` as the Time filter on the input grid card so planners only see open periods, while the chart card uses no Time filter to show full history.

## Formula(s)

Most of this is **configuration, not formulas** — publish cards dimensioned by the shared lists and the synced selectors filter them.

Where you genuinely need the selection in a formula, use `ITEM` inside a module dimensioned by that list (e.g. a one-row label module), or compute attributes that the page surfaces:

```
// label of the currently shown cost centre (module dimensioned by Cost Centre)
NAME(ITEM(Cost Centre))
```

Avoid `SELECT: CostCentre.SpecificItem` to "hard-filter" a card — that defeats the reusable selector and breaks when the list changes (*Sustainable*).

## Pitfalls / gotchas

- **Synced vs unsynced selectors.** Cards only move together if their selectors are *synced* on the same dimension. Mismatched sync is the usual "why didn't the chart update?" cause.
- **Don't hard-code the item.** A selector that's reusable beats a page rebuilt per cost centre. Let access/selective access decide *which* members a user can pick.
- Cards must share the **same list/dimension** to respond to one selector — a card dimensioned by a different list won't follow.
- Showing a user only *their* members combines this with **selective access** (see [cascading-selective-access](../security-and-dca/cascading-selective-access.md)) — the selector then only offers what they can see.
- Keep heavy logic out of the page; the page is **Outputs** (DISCO) — it arranges, it doesn't compute.

## Performance & PLANS notes

- One reusable page (not one-per-entity) is the **Sustainable**/**Necessary** ideal — fewer artefacts to maintain.
- Publishing pre-shaped **Output** modules keeps page render fast; avoid putting big calc modules directly on the page.
- Combine with a dynamic time filter so the period selector is itself data-driven — see [dynamic-time-filter](dynamic-time-filter.md).

## Related

- [`docs/05-ux/`](../../docs/05-ux/)
- Recipes: [input-vs-report-pages](input-vs-report-pages.md) · [dynamic-time-filter](dynamic-time-filter.md) · [cascading-selective-access](../security-and-dca/cascading-selective-access.md) · [approval-status-workflow](approval-status-workflow.md)
