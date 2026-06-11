# Model-Build Checklist

> **Level:** L2 · **Area:** Methodology · Run this before you call a build "done" or review someone else's.

A practical pre-flight / review checklist, phrased as **PLANS + DISCO + Planual** checks. A copyable
version lives in [`templates/model-build-checklist.md`](../../templates/model-build-checklist.md).

## Structure (DISCO)

- [ ] Every module is clearly **one** DISCO type (Data / Inputs / System / Calculations / Outputs).
- [ ] Mappings and attributes live in **System** modules, not scattered in calcs.
- [ ] Data flows one way: D/I → S → C → O. No circular references.
- [ ] Modules follow the naming convention (`DAT/INP/SYS/CAL/OUT` prefixes).

## Performance (P)

- [ ] No module is dimensioned by a list it doesn't need.
- [ ] **Time Ranges** applied where a module doesn't need the full calendar.
- [ ] **Subsets** used where a module only needs part of a list.
- [ ] No `IF`/text formulas running over very large cell counts where a Boolean/lookup would do.
- [ ] Sub-expressions used many times are calculated **once** in their own line item.

## Logical & Auditable (L, A)

- [ ] Complex logic is **split into stepped line items**, each readable.
- [ ] Names describe meaning (`Revenue Gross`, not `R1`).
- [ ] Summary methods are set deliberately (Sum vs Average vs Formula vs None).
- [ ] A reviewer can trace any output number back to its inputs.

## Necessary (N)

- [ ] No duplicate calculations (same logic in two places).
- [ ] No unused / experimental line items or modules left behind.
- [ ] Nothing stored that could be cheaply derived (and vice-versa).

## Sustainable (S)

- [ ] **No hard-coded** dates, periods or list items in any formula.
- [ ] No `SELECT` on specific list items — mapped via System modules instead.
- [ ] Adding a new product / period / entity needs **no formula changes**.
- [ ] Shared source data comes from a **Data Hub**, not re-imported per model.

## Delivery

- [ ] Built to the user story (no scope creep).
- [ ] Tested with realistic data; edge cases checked (blanks, new members, year rollover).
- [ ] Production-bound work is under **ALM** (built in DEV, promotable via revision).
- [ ] Key assumptions documented (notes module / line-item descriptions).

**Related:** [PLANS](plans-standard.md) · [DISCO](disco.md) · [The Planual](planual.md) · [Performance](../07-performance/)
