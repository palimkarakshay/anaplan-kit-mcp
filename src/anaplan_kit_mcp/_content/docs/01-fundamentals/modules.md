# Modules

> **Level:** L1 · **Area:** Fundamentals · **PLANS:** Logical · **DISCO:** all five module types

A **module** is the heart of Anaplan: a **multi-dimensional grid** of [line items](line-items-and-formats.md)
built across one or more [dimensions](dimensions.md). Every number, every calculation, every input in
a model lives in a module. If a [list](lists-and-hierarchies.md) is "the things you plan by", a module
is "where you plan".

---

## A module is a grid

In a spreadsheet you have one flat sheet of rows and columns. A module is the same idea, but it can
have **many** dimensions at once. Picture this expense module:

- **Line items** down one axis: `Expense`, `Budget`, `Variance`.
- **Time** across the top: Jan, Feb, Mar…
- A **list** (Cost Centre) giving you a separate grid *for every member*.
- **Versions** (Actual, Budget) giving you another whole copy.

So a single module can be a 4-dimensional cube: *for every Cost Centre, for every Version, for every
Month, hold these three line items*. You build the logic **once** and it applies across the whole cube.

```
                  Time →   Jan   Feb   Mar
Cost Centre: CC-100
  Expense                  100   110   120
  Budget                   105   105   105
  Variance                  -5     5    15
(…and the same grid repeats for every Cost Centre, every Version)
```

---

## How lists, Time and Versions form the dimensions

A module's dimensions — its **[Applies To](dimensions.md)** — can be any mix of:

| Dimension source | Example | Notes |
| --- | --- | --- |
| **Lists** | Cost Centre, Product, Region | The things you plan by. Any number of them. |
| **[Time](time.md)** | Months / Quarters / Years | Built-in; added by ticking "Applies to Time". |
| **[Versions](versions.md)** | Actual, Budget, Forecast | Built-in; added by ticking "Applies to Versions". |

**Line items are not a dimension** in the same sense — they're the *measures* inside the module. The
total cell count is the **product of all dimension sizes × the number of line items** — which is why
choosing dimensions carefully is the #1 performance decision (see [Dimensions](dimensions.md)).

---

## Subsidiary views

By default every line item in a module shares the module's full dimensionality. Sometimes that's
wasteful — one line item genuinely needs *fewer* dimensions than the rest.

A **subsidiary view** is a line item given its **own, smaller Applies To**, different from its parent
module. Example: in a module dimensioned by `Product × Time`, a `Standard Price` line item might apply
to `Product` only (price doesn't change by month). That line item then stores far fewer cells.

```
Module "CAL Pricing"  — Applies To: Product × Time
  Volume          (Product × Time)        full grid
  Standard Price  (Product only)          ← subsidiary view: no Time dimension
  Revenue         (Product × Time)        = Volume * Standard Price
```

> ⚠️ Subsidiary views save memory but can make a module harder to read (different line items have
> different shapes). Best practice often prefers splitting genuinely different-shaped data into
> **separate modules** for clarity. Use subsidiary views deliberately, not by accident. *(Auditable)*

---

## The Blueprint view

Every module has two views:

- **Grid view** — the data: cells of numbers you and planners see.
- **Blueprint view** — the *design*: a row per line item showing its configuration.

The **Blueprint** is where you, the builder, live. This kit describes every module as a **blueprint
table** with these columns:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Volume | Number | Sum | Product, Time | (input) |
| Standard Price | Number | None | Product | (input) |
| Revenue | Number | Sum | Product, Time | `Volume * Standard Price` |

Read a blueprint top to bottom and you can audit the whole module without opening a single cell —
which is exactly the point. (See [Line items & formats](line-items-and-formats.md) for what goes in
each column.)

---

## Saved views

A **saved view** is a stored *arrangement* of a module — pivoted, filtered, with line items hidden or
reordered, optionally showing only a [subset](numbered-lists-and-subsets.md). Saved views are used to:

- Feed a dashboard/page grid showing exactly the right slice.
- Act as the **source or target of an import/export** (see [Integration](../04-integration/)).

A saved view doesn't copy data — it's a lens onto the same module.

---

## Modules and DISCO

A model isn't one giant module — it's many small ones, each with a clear job. **[DISCO](../03-methodology/disco.md)**
is the pattern for deciding *what kind* of module you're building:

| DISCO | Module's job | Example |
| --- | --- | --- |
| **D**ata | Hold imported source data as-is | `DAT01 Actuals from GL` |
| **I**nputs | Numbers humans type | `INP01 Revenue Assumptions` |
| **S**ystem | Mappings, flags, attributes | `SYS01 Time Settings` |
| **C**alculations | The formula engine | `CAL01 Revenue Calculation` |
| **O**utputs | Reporting/export views | `OUT01 P&L Report` |

Keeping one job per module is what makes a model fast and auditable — read [DISCO](../03-methodology/disco.md)
next.

---

**Related:** [Line items & formats](line-items-and-formats.md) · [Dimensions](dimensions.md) ·
[Lists & hierarchies](lists-and-hierarchies.md) · [DISCO](../03-methodology/disco.md) ·
[Integration](../04-integration/) · [Glossary](../00-getting-started/glossary.md)

> Source: Anaplan platform documentation (Anapedia, `help.anaplan.com`). Confirm current behaviour for your platform version. See [`SOURCES.md`](../../SOURCES.md).
