# 01 · Fundamentals

> **Level:** L1 · **Area:** Fundamentals · This is where you start *building*.

These are the building blocks of every Anaplan model. Master this section and you can construct a
small, correct model end-to-end; everything later in the kit (methodology, formulas, performance)
refines how you use these same pieces.

If [00-getting-started](../00-getting-started/) was the map, this is the toolkit.

---

## Recommended reading order

Read these in order — each builds on the last.

| # | Page | What you'll be able to do after it |
| --- | --- | --- |
| 1 | [lists-and-hierarchies.md](lists-and-hierarchies.md) | Create lists and build a parent/child hierarchy that rolls up. |
| 2 | [numbered-lists-and-subsets.md](numbered-lists-and-subsets.md) | Pick the right list type and carve out subsets of a list. |
| 3 | [modules.md](modules.md) | Understand a module as a multi-dimensional grid and read its blueprint. |
| 4 | [line-items-and-formats.md](line-items-and-formats.md) | Choose the correct format and summary for every line item. |
| 5 | [dimensions.md](dimensions.md) | Size a module deliberately and keep cell count under control. |
| 6 | [time.md](time.md) | Configure Time and use it as a dimension. |
| 7 | [versions.md](versions.md) | Model Actual/Budget/Forecast scenarios correctly. |

---

## How the pieces fit

```
LISTS  (the things you plan by)        TIME  +  VERSIONS  (built-in dimensions)
   │                                          │
   └──────────────┬───────────────────────────┘
                  ▼
            DIMENSIONS  (a module's "Applies To")
                  │
                  ▼
              MODULE  =  a grid of  LINE ITEMS
                              │
                  each line item has a  FORMAT + SUMMARY + FORMULA
```

A **list** is a set of things (products, months, cost centres). One or more lists — plus optionally
**Time** and **Versions** — become the **dimensions** of a **module**. Inside the module, each
**line item** holds a measure or calculation, with a **format** (its data type), a **summary method**
(how it rolls up), and a **formula**.

That single chain — lists → dimensions → module → line items — is 90% of Anaplan. The methodology
section then teaches you to arrange those modules *well* (see [DISCO](../03-methodology/disco.md) and
[PLANS](../03-methodology/plans-standard.md)).

---

**Related:** [Getting started](../00-getting-started/) · [Methodology](../03-methodology/) ·
[Formulas](../02-formulas/) · [Performance](../07-performance/) · [Learning path](../../LEARNING-PATH.md)
