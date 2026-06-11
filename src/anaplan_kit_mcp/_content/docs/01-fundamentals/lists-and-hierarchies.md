# Lists & Hierarchies

> **Level:** L1 · **Area:** Fundamentals · **PLANS:** Logical, Sustainable

A **list** is the most basic building block in Anaplan: it's the set of *things you plan by*.
Products, cost centres, regions, employees, accounts, scenarios — each is a list. Lists become the
**dimensions** of your modules (see [Dimensions](dimensions.md)), so getting them right is the
foundation everything else sits on.

---

## What a list is

Think of a list as the labels you'd otherwise repeat down the side of every spreadsheet tab. Instead
of typing "France, Germany, Spain…" on a dozen tabs, you build a **Country** list *once* and every
module can be dimensioned by it.

| A list is… | A list is **not**… |
| --- | --- |
| A set of named members (the things you plan by). | A place to store numbers — that's a [module](modules.md). |
| Reusable as a dimension across many modules. | A single column of data. |
| Structural — it changes rarely, by load or admin. | Edited by planners during planning. |

### List members

A **list member** (or list item) is a single entry — "France" in a Country list, "CC-100 Marketing"
in a Cost Centre list. Each member needs a **unique name** within the list (this is true for standard
lists; [numbered lists](numbered-lists-and-subsets.md) relax this for transactional data).

### Properties

A **property** is an attribute attached to every member of a list — a Cost Centre's owner, a
Product's launch date, an Account's GL code.

> ⚠️ **Beginner guidance:** you *can* store attributes as list properties, but Anaplan best practice
> is usually to hold them in a **System module** instead (see [DISCO → System](../03-methodology/disco.md)).
> System modules are easier to reference in formulas, can be time-phased, and are more flexible than
> list properties. Use list properties sparingly; reach for a `SYS` module first. *(Sustainable)*

---

## Composite (parent/child) hierarchies

Most real lists aren't flat — they roll up. A **composite list** stacks several lists into a
parent/child **hierarchy**, so totals aggregate automatically: a Country totals its Cost Centres, a
Region totals its Countries.

In Anaplan a composite hierarchy is built from **one list per level**, linked by a **parent**
relationship:

```
Region        (top level — parents)
  └── Country     (each Country's parent is a Region)
        └── Cost Centre   (each Cost Centre's parent is a Country)
```

Each lower list has a **Parent** setting pointing at the list above it. When you dimension a module by
the bottom list (Cost Centre), Anaplan automatically gives you the roll-up totals at Country and
Region — no formula required. The roll-up behaviour follows each line item's
[**summary method**](line-items-and-formats.md) (Sum, Average, etc.).

### Top-level item

A list can have a single **top-level item** — one member that sits above everything and totals the
*entire* list (e.g. "Total Organisation"). It's optional but very useful:

- It gives you a grand-total cell to report against.
- It's a safe default left-hand side when a formula needs "the whole list".
- It avoids the trap of a member accidentally named "Total".

---

## Worked example — an Organisation hierarchy

Goal: plan by individual **Cost Centre**, but report totals by **Country** and **Region**.

Build three lists, each pointing at its parent:

| List | Parent list | Top-level item | Example members |
| --- | --- | --- | --- |
| **Region** | (none — top) | Total Org | EMEA, Americas |
| **Country** | Region | — | France, Germany (→ EMEA); USA (→ Americas) |
| **Cost Centre** | Country | — | CC-100 Marketing (→ France), CC-200 Sales (→ Germany) |

The resulting structure:

```
Total Org
├── EMEA
│   ├── France
│   │   └── CC-100 Marketing
│   └── Germany
│       └── CC-200 Sales
└── Americas
    └── USA
        └── CC-300 Support
```

Now dimension an expenses module by **Cost Centre**. If `Expense` has summary **Sum**, Anaplan shows:

| Member | Level | Expense (rolled up) |
| --- | --- | --- |
| Total Org | Region top | 1,000 |
| EMEA | Region | 700 |
| France | Country | 400 |
| CC-100 Marketing | Cost Centre (input) | 400 |
| Americas | Region | 300 |

You only ever *type* at the Cost Centre level; every total above it is computed automatically.

---

## When to use a hierarchy (and when not)

| Use a hierarchy when… | Keep it flat / separate when… |
| --- | --- |
| The business naturally rolls up (org, product family → product, geography). | The relationship is many-to-many (a product sold in many regions). |
| You want automatic subtotals at each level. | The "parent" is really just an attribute → use a mapping in a System module. |
| The reporting structure is stable. | Items belong to several groupings at once → model each grouping as its own list + mapping. |

> A composite hierarchy can only express **one** roll-up path. If a Cost Centre needs to roll up by
> *both* Region *and* Function, don't force a second level into the hierarchy — create a separate
> Function list and map to it in a System module, then aggregate with `SUM`. *(Logical, Sustainable)*

---

**Related:** [Numbered lists & subsets](numbered-lists-and-subsets.md) · [Modules](modules.md) ·
[Dimensions](dimensions.md) · [DISCO](../03-methodology/disco.md) · [Glossary](../00-getting-started/glossary.md)

> Source: Anaplan platform documentation (Anapedia, `help.anaplan.com`). Confirm current behaviour for your platform version. See [`SOURCES.md`](../../SOURCES.md).
