# Numbered Lists & Subsets

> **Level:** L2 · **Area:** Fundamentals · **PLANS:** Performance, Sustainable

Once you understand ordinary [lists and hierarchies](lists-and-hierarchies.md), two variations let you
handle data that doesn't fit the "neat set of uniquely-named things" mould: **numbered lists** (for
transactional, high-volume data) and **subsets** (a flagged portion of a list). This page also gives a
short intro to **line item subsets**.

---

## Numbered lists

A standard list requires every member to have a **unique name**. That works for products and cost
centres, but it breaks down for transactional rows where there's no natural unique label:

- 50,000 sales transactions (many have the same customer + product + date).
- A list of "opportunities", "tickets", "invoices", "headcount requisitions".
- Any imported detail table where the key is a combination, not a single name.

A **numbered list** solves this. Its members are identified internally by an **automatically assigned
number** rather than by a unique display name, so you can have many members that *look* the same.

| | Standard list | Numbered list |
| --- | --- | --- |
| Member identity | Unique **name** | Internal **number** (name optional / non-unique) |
| Best for | Reference data: products, regions, accounts | Transactional/detail data: transactions, line-level records |
| Typical DISCO home | System / Inputs dimensions | [**Data**](../03-methodology/disco.md) modules |
| Display | Show the name | Show one or more **properties** (e.g. Customer + Date) as the label |

### When and why to use one

Use a numbered list when:

- The data is **transactional** and high-volume.
- There is **no single unique name** — the meaningful key is a *combination* of attributes.
- You'll feed it from an import and identify rows by a **combination of properties** rather than a name.

### Properties and display

Because numbered-list members have no meaningful name, you give them **properties** (Customer,
Product, Date, Amount) and choose which properties form the **display name** so humans can read the
rows. As with standard lists, prefer holding the attributes you *calculate against* in a System
module; use properties mainly for identification and display.

> ⚠️ Numbered lists are an **L2** topic for a reason: they're powerful for detail/transaction data but
> add complexity (you import by a property key, not a name). For a first L1 model, standard named lists
> are usually all you need.

---

## Subsets

A **subset** is a **flagged portion of a list** — a sub-selection of its members that you can use as a
smaller dimension in its own right.

You enable a subset on the list's configuration, then flag which members belong to it (manually, or
driven by a Boolean — best practice is to drive it from a System module so it stays
[sustainable](../03-methodology/plans-standard.md)).

### Why use a subset

| Reason | Example |
| --- | --- |
| **Performance** — dimension a module by *fewer* members | A list of 5,000 SKUs, but a pricing module only needs the 200 "active" ones → a `Active SKUs` subset. |
| **Logical** — a module that only applies to part of a list | A bonus module that only applies to the "Sales" cost-centre subset. |
| **Reuse** — one list, several meaningful slices | One Account list with subsets for `P&L Accounts`, `Balance Sheet Accounts`. |

Because a subset is *part of* its parent list, members keep their identity and any hierarchy — you're
just choosing a smaller set to build across. This makes subsets one of the simplest
[performance](../07-performance/) levers: fewer dimension members means fewer cells.

```
Cost Centre list (250 members)
   └── Subset: "Sales Cost Centres" (30 members)  ← dimension the bonus module by this
```

---

## Line item subsets (brief intro)

A **line item subset** is a more advanced construct: instead of selecting list members, it gathers
selected **line items** (measures) from one or more modules and exposes them **as if they were a
list** — i.e. it lets you treat a set of measures as a *dimension*.

Typical use: build a generic report or driver table where "the thing you pivot by" is a chosen set of
measures (e.g. Revenue, COGS, Margin) rather than a normal list.

> ⚠️ Line item subsets are **performance-sensitive** and easy to misuse — they can quietly inflate
> dimensionality and complicate auditing. Treat them as an L2/L3 tool, reach for them only when a plain
> module won't do, and read the performance notes before committing:
> see [Performance → subsets & line item subsets](../07-performance/).

---

## Quick chooser

| You have… | Use… |
| --- | --- |
| A clean set of uniquely-named things | A **standard list** ([lists & hierarchies](lists-and-hierarchies.md)) |
| High-volume transactional rows, no unique name | A **numbered list** |
| A meaningful slice of an existing list | A **subset** (driven by a System-module Boolean) |
| A need to treat several measures as a dimension | A **line item subset** (sparingly; check performance) |

---

**Related:** [Lists & hierarchies](lists-and-hierarchies.md) · [Modules](modules.md) ·
[Dimensions](dimensions.md) · [DISCO](../03-methodology/disco.md) · [Performance](../07-performance/) ·
[Glossary](../00-getting-started/glossary.md)

> Source: Anaplan platform documentation (Anapedia, `help.anaplan.com`). Confirm current behaviour for your platform version. See [`SOURCES.md`](../../SOURCES.md).
