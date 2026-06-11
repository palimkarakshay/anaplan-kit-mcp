# Dimensions

> **Level:** L1 · **Area:** Fundamentals · **PLANS:** Performance, Necessary

**Dimensionality** is the single most important thing to understand for building models that are both
*correct* and *fast*. A module's **dimensions** define the shape of its grid — and the shape decides
how many cells it holds, which decides how much memory it uses and how quickly it recalculates.

---

## What a dimension is

A **dimension** is any axis a [module](modules.md) is built across. It can be:

- A **[list](lists-and-hierarchies.md)** — Product, Cost Centre, Region, Employee.
- **[Time](time.md)** — the built-in calendar dimension.
- **[Versions](versions.md)** — the built-in scenario dimension (Actual, Budget, Forecast).

A module can have several dimensions at once, giving it a multi-dimensional cube shape: *for every
Product, for every Month, for every Version, hold these line items*.

---

## Applies To

**Applies To** is where you set a module's (or a line item's) dimensions. It's the list of dimensions
that, together, define which cells exist.

- Set at the **module** level, every line item inherits those dimensions by default.
- Set at the **line item** level (overriding the module) you get a
  [**subsidiary view**](modules.md#subsidiary-views) — that line item has its own, usually smaller, shape.

Reading "Applies To: Product, Time" tells you instantly: this is a grid of *every product × every
period*. That's why every blueprint table in this kit includes an **Applies To** column.

```
Applies To:  Product (500)  ×  Time/Month (36)  ×  Version (3)
             └──────────────── one cell per combination ────────┘
```

---

## Why cell count = product of dimensions × line items

This is the formula to tattoo on your brain:

```
cells in a module = (size of dim 1) × (size of dim 2) × … × (number of line items)
```

Every dimension you add **multiplies** the cell count; it doesn't add to it. A module with:

- 500 Products
- 36 Months
- 3 Versions
- 10 line items

holds **500 × 36 × 3 × 10 = 5,400,000 cells.** Add one more dimension of 50 members and you don't get
+50 — you get **×50 = 270 million cells.** That is how models silently explode.

> ⚠️ The model lives entirely in memory (see [Platform architecture](../00-getting-started/platform-architecture.md)),
> so cells are RAM. Controlling cell count *is* controlling performance and cost. This is the **P** in
> [PLANS](../03-methodology/plans-standard.md), covered in depth under
> [Performance / PLANS-Performance](../07-performance/).

### Worked comparison

| Module | Dimensions | Line items | Cells |
| --- | --- | --- | --- |
| Over-dimensioned | Product (500) × Cost Centre (250) × Month (36) × Version (3) | 10 | 13.5 **billion** |
| Right-sized | Product (500) × Month (36) | 10 | 180,000 |

Same business question, two designs. The first will be slow or won't open; the second is trivial. The
difference is asking *"does this line item really vary by Cost Centre **and** Version?"* before adding
the dimension.

---

## Choosing the right dimensions

Ask these questions for **each** candidate dimension before adding it:

| Ask… | If "no"… |
| --- | --- |
| Does this measure genuinely **vary** by this list? | Don't add the dimension — you'd store identical numbers many times. |
| Do users **input or report** at this granularity? | Aggregate it away; report from a roll-up instead. |
| Could a **[subset](numbered-lists-and-subsets.md)** cover only the members that matter? | Dimension by the subset, not the full list. |
| Could **[Time Ranges](../07-performance/time-ranges.md)** limit the periods? | Apply a time range so you only store needed periods. |
| Is this a **rate/price** that's flat over Time? | Make it a [subsidiary view](modules.md#subsidiary-views) without Time. |

Rules of thumb (all PLANS-driven):

- **Only dimension by lists you truly need.** Every extra dimension multiplies size. *(Necessary, Performance)*
- **Push detail into Data modules, keep Calculations lean.** Don't carry transaction-level Product ×
  Customer detail through your whole calculation chain — aggregate early.
- **Match input granularity to how planners actually plan.** If they budget by Region, don't force them
  (and the model) down to Cost Centre.
- **Prefer subsets and time ranges** over full lists and full timescales when only a slice is relevant.

---

## Sparsity (a quick note)

A module can be *dimensionally* huge but *actually* mostly empty — only some Product × Customer
combinations ever have data. This is **sparsity**, and it's a major performance topic in its own right:
the way you arrange and order dimensions affects how efficiently Anaplan stores those gaps. When you're
ready to tune large models, see [Performance](../07-performance/).

---

**Related:** [Modules](modules.md) · [Lists & hierarchies](lists-and-hierarchies.md) ·
[Numbered lists & subsets](numbered-lists-and-subsets.md) · [Time](time.md) · [Versions](versions.md) ·
[PLANS → Performance](../03-methodology/plans-standard.md) · [Performance](../07-performance/) ·
[Glossary](../00-getting-started/glossary.md)

> Source: Anaplan platform documentation (Anapedia, `help.anaplan.com`). Confirm current behaviour for your platform version. See [`SOURCES.md`](../../SOURCES.md).
