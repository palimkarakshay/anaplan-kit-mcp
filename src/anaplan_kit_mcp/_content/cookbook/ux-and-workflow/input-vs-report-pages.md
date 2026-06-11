# Input pages vs report pages

> **Level:** L2 · **Area:** UX & Workflow · **PLANS:** Logical, Performance · **DISCO:** Inputs / Outputs

## The ask

"Planners keep accidentally typing over calculated numbers, and the review board is cluttered with editable cells nobody should touch. Can we cleanly separate where people enter data from where they read results?"

## When you'll see this

- A page mixes editable assumptions and read-only results and confuses users.
- You want a tidy "enter here" experience separate from a "review here" experience.
- Aligning the UX with DISCO so logic and presentation don't tangle.

## Approach

Separate **Input pages** (built on **Inputs** modules — editable assumptions only) from **Report pages** (built on **Outputs** modules — read-only, formatted views). This mirrors **DISCO**: Inputs are where humans type; Outputs are shaped for reading. Calculations sit behind both and aren't shown directly.

Rule of thumb:

- **Input page** → publish **I** modules; cells editable; minimal, focused.
- **Report page** → publish **O** modules; cells read-only (or hard-locked via DCA); formatted for consumption/export.

Why idiomatic:

- **Logical (PLANS):** the page type matches the module's DISCO role — no editable calc cells.
- **Performance:** Output modules are pre-shaped and light to render; you don't drop a giant calc grid on a page.

## Blueprint

**Input page** — built on `INP01 Revenue Assumptions`:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Growth % | Number (%) | None | Product, Time | *(input)* |
| Price | Number | None | Product, Time | *(input)* |

**Report page** — built on `OUT01 P&L Report` (no new logic, just arranged results):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Revenue | Number | Sum | Product, Time | `CAL Revenue.Revenue` |
| Gross Margin % | Number (%) | None | Product, Time | `CAL Revenue.GM%` |

## Formula(s)

This recipe is mostly **structure and DISCO discipline**, not formulas. The Output module only *references* finished results — it must not introduce business logic:

```
// OUT01 P&L Report -> Revenue   (reference, no new logic)
CAL Revenue.Revenue
```

Make report cells non-editable by building them on calculated/Output line items (a line item with a formula isn't editable), and/or apply read-only **DCA** for hard locks (see [hide-or-lock-by-role](../security-and-dca/hide-or-lock-by-role.md)).

## Pitfalls / gotchas

- **Don't publish Calculation modules directly to users.** They're the engine room, not a UI — show **Inputs** for entry and **Outputs** for reading.
- **Editable vs calculated:** a line item with a formula is read-only by nature. Don't make a calculated value editable to "let users tweak it" — give them a proper input + override pattern instead.
- A report page with stray editable cells invites accidental overwrites — audit every card's editability.
- Keep input pages **focused** (few drivers) so planners aren't lost; keep report pages **formatted** (units, %, conditional formatting).
- Putting logic in the Output module to "fix" a number breaks DISCO and hides the real source — fix it in the Calc module.

## Performance & PLANS notes

- Pre-shaped **Output** modules render faster than live calc grids and keep pages snappy (**Performance**).
- Matching page type to DISCO role is the structural form of **Logical** + **Auditable**.
- Fewer editable surfaces = fewer accidental edits = less reconciliation pain later.

## Related

- [`docs/03-methodology/disco.md`](../../docs/03-methodology/disco.md)
- [`docs/05-ux/`](../../docs/05-ux/)
- Recipes: [context-selector-dashboard](context-selector-dashboard.md) · [approval-status-workflow](approval-status-workflow.md) · [hide-or-lock-by-role](../security-and-dca/hide-or-lock-by-role.md)
