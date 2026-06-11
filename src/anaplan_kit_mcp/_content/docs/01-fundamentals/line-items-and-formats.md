# Line Items & Formats

> **Level:** L1 · **Area:** Fundamentals · **PLANS:** Logical, Auditable

A **line item** is a single measure or calculation inside a [module](modules.md) — `Revenue`,
`Growth %`, `Is Active?`. Each line item has a **format** (what kind of data it holds), a **summary
method** (how it rolls up), and optionally a **formula**. Getting format and summary right is where a
lot of silent beginner bugs hide, so this page is worth reading carefully.

---

## Line items

In the [Blueprint](modules.md#the-blueprint-view) view, each line item is one row. The columns you set:

| Column | What it controls |
| --- | --- |
| **Format** | The data type — Number, Boolean, Text, List, Date, Time Period, No Data. |
| **Summary** | How values aggregate up hierarchies and Time (Sum, Average, None…). |
| **Applies To** | Its dimensions; can differ from the module ([subsidiary view](modules.md#subsidiary-views)). |
| **Formula** | The logic; blank means it's an input cell. |
| Formatting | Decimal places, units, thousands separator, negative-number style, etc. |

A line item with **no formula** is an **input** (planners type into it). A line item **with** a formula
is calculated and read-only.

---

## Formats (data types)

The **format** decides what a line item can hold and how it behaves in formulas.

| Format | Holds | Typical use | Default summary |
| --- | --- | --- | --- |
| **Number** | Numeric values | Revenue, volume, rates, %, counts | Sum |
| **Boolean** | TRUE / FALSE (a checkbox) | Flags: `Is Active?`, `Include in Plan?`, DCA drivers | None (or Boolean options) |
| **Text** | Free text | Names, comments, codes (display only — can't do maths) | None |
| **List** | A reference to one member of a chosen list | A mapping: "this row's Region", a dropdown selector | None |
| **Date** | A calendar date | Hire date, launch date, contract end | None |
| **Time Period** | A reference to a period of the model's Time | "Effective period", "go-live month" | None |
| **No Data** | Nothing (a spacer/header) | Visual separators, grouping rows on a dashboard | None |

> Some platforms label a "**Mixed**" state — it simply means a line item's format hasn't been set yet,
> or a view shows line items of differing formats together. A real line item always resolves to one of
> the formats above; **No Data** is the deliberate "this row holds nothing" choice.

### Format tips

- **Number vs Text:** if you'll ever add, compare, or aggregate it, it must be **Number**. Storing a
  number as Text is a classic bug — it looks fine but breaks every formula. *(see pitfalls below)*
- **List format = a mapping.** A `List`-formatted line item that points at, say, the Region list is how
  you connect one list to another for `SUM`/`LOOKUP`. This usually lives in a
  [System module](../03-methodology/disco.md).
- **Boolean for flags.** Use a Boolean, not a Number 1/0 or a "Yes"/"No" text — Booleans are smaller,
  faster, and drive `IF`, filters and [DCA](../06-security-alm/dynamic-cell-access.md) cleanly.

---

## Summary methods

The **summary method** decides what shows at the *parent* level of a hierarchy and at higher Time
periods (the quarter total of three months, the Region total of its Countries).

| Summary | Parent shows… | Use for |
| --- | --- | --- |
| **Sum** | The total of the children | Amounts, volumes, counts (anything additive) |
| **Average** | The mean of the children | Average headcount, average price (when averaging is meaningful) |
| **Min** | The smallest child | Floors, earliest, worst-case |
| **Max** | The largest child | Caps, latest, best-case |
| **Formula** | The line item's **own formula re-applied** at the parent | Ratios/% that must be *recomputed*, not summed (see below) |
| **None** | Nothing at the parent (blank) | Inputs you don't want to roll up; text/dates |
| **Ratio** | A numerator ÷ denominator you nominate | A weighted ratio computed from two other line items |
| **Boolean options** | `Any`/`All` true, count of trues | Rolling up flags |

### The classic ratio trap

A percentage or rate must **never** use Sum. If `Margin %` = `Profit / Revenue` and you Sum it, the
parent shows the *sum of the percentages* — nonsense (e.g. 20% + 30% + 25% = 75%).

Fix it with summary **Formula** (recompute `Profit / Revenue` at every level) or **Ratio**
(nominate Profit as numerator, Revenue as denominator):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Profit | Number | Sum | Region, Time | `Revenue - Cost` |
| Revenue | Number | Sum | Region, Time | (input) |
| Margin % | Number (%) | **Formula** | Region, Time | `Profit / Revenue` |

Now the Region total of `Margin %` is correctly *its own* Profit ÷ Revenue, not the sum of the
children's percentages.

---

## Formatting options

Separate from format/summary, each line item has display settings: decimal places, **units** label,
thousands separator, negative-number style (parentheses/red), zoom, and whether to show as a
percentage. These are cosmetic — they don't change the stored value — but they make
[Output modules](../03-methodology/disco.md) readable.

---

## Beginner pitfalls

| Pitfall | Symptom | Fix |
| --- | --- | --- |
| **Number stored as Text** | Can't sum it; formulas error or treat it as 0 | Set format to **Number**; re-import or `VALUE()` it |
| **Wrong summary on a ratio/%** | Parent totals look absurd (e.g. 250%) | Use **Formula** or **Ratio** summary |
| **Summary = Sum on an input that shouldn't roll up** | Phantom totals appear at parents | Set summary to **None** |
| **Boolean modelled as Text "Yes"/"No"** | Filters/`IF`/DCA won't work; bigger model | Use a real **Boolean** line item |
| **Everything left as default Sum** | Averages, prices, flags all roll up wrong | Set the summary **deliberately** on every line item |
| **Free-typed dates as Text** | Date maths impossible | Use **Date** or **Time Period** format |

> Setting the summary method deliberately on **every** line item is one of the Planual themes worth
> internalising on day one — a wrong summary is a silent bug that survives review. *(Logical)* See
> [The Planual](../03-methodology/planual.md).

---

**Related:** [Modules](modules.md) · [Dimensions](dimensions.md) · [Time](time.md) ·
[Versions](versions.md) · [The Planual](../03-methodology/planual.md) ·
[Formulas](../02-formulas/) · [Glossary](../00-getting-started/glossary.md)

> Source: Anaplan platform documentation (Anapedia, `help.anaplan.com`). Confirm current behaviour for your platform version. See [`SOURCES.md`](../../SOURCES.md).
