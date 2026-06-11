# PLANS — The Anaplan Modeling Standard

> **Level:** L2 · **Area:** Methodology · This is the standard every other page is judged against.

**PLANS** is Anaplan's official standard for *what good model construction looks like*. It is an
acronym — five principles. Whenever you make a modeling choice (a formula, a list, a module
structure), ask: "does this satisfy PLANS?"

| Letter | Principle | Plain meaning |
| --- | --- | --- |
| **P** | **Performance** | The model calculates fast and stays small. Cell count and recalculation are under control. |
| **L** | **Logical** | The structure mirrors the business logic; data flows in a clear, traceable direction. |
| **A** | **Auditable** | Anyone can follow a number back to its source. Formulas are simple and broken into steps. |
| **N** | **Necessary** | Nothing redundant — no duplicate calculations, no line items "just in case". |
| **S** | **Sustainable** | The model survives change: new periods, new list members, new builders, no manual rework. |

---

## P — Performance

- Keep **cell count** down: don't dimension a module by lists it doesn't need (this is *the*
  biggest lever — cell count = product of all dimension sizes × line items).
- Use **Time Ranges** and **subsets** to shrink modules. See [`docs/07-performance/`](../07-performance/).
- Avoid heavy `IF` on large modules — prefer Boolean line items and `LOOKUP`/`SUM` mapping.
- Calculate something **once** in a dedicated line item, then reference it (don't repeat a
  sub-expression in many formulas).

## L — Logical

- Data flows **one direction**: source/import → calculation → output. No circular references.
- Group related logic into the right **DISCO** module type (see [disco.md](disco.md)).
- Name things so the logic reads itself: `Revenue Gross`, not `R1`.

## A — Auditable

- **Break formulas into steps.** A line item per logical step is easier to debug and faster to
  recalc than one giant nested formula. (This is also a Performance win.)
- Keep formulas short enough to read in one line where possible.
- Use **system modules** to hold mappings and flags, so logic is visible, not buried.

## N — Necessary

- Before adding a line item or module, ask "does anything actually need this?"
- Don't store what you can derive cheaply; don't derive what you can store once.
- Remove experiments and dead line items — they still cost memory and confuse readers.

## S — Sustainable

- **Never hard-code** a date, a list member, or a period in a formula. Drive them from system
  modules / Time so the model keeps working next year. (e.g. don't write `IF Time = Jan 25 …`.)
- Use **mappings** (system modules) instead of `SELECT` on specific items.
- Build so that adding a new product / month / entity needs **no formula changes**.

---

## Using PLANS day to day

Every recipe in the [cookbook](../../cookbook/) and every blueprint in this kit calls out which
PLANS principle a choice serves. When you review your own work, walk the five letters in order —
it catches most beginner mistakes before they reach a client model.

**Related:** [The Planual](planual.md) turns these principles into concrete numbered rules ·
[DISCO](disco.md) is how you satisfy *Logical* and *Auditable* structurally ·
[Performance docs](../07-performance/) cover *Performance* in depth.

> Source: Anaplan PLANS modeling standard (Anaplan Academy / Community best-practice materials). See [`SOURCES.md`](../../SOURCES.md).
