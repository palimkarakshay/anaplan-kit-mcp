# Formulas & Function Reference

> **Level:** L1 · **Area:** Formulas

This is the function-by-function reference for the kit. It is written for a **brand-new model
builder** — every function has a consistent layout (Syntax → What it does → Example → Watch out
for → Source) so you can scan it like a dictionary while you build.

> ⚠️ Anaplan is a browser-based SaaS platform — there is no offline "compile". These pages
> *describe and illustrate* syntax verified against [Anapedia](https://help.anaplan.com/). Always
> confirm against the live page for your platform version. See [`../../SOURCES.md`](../../SOURCES.md)
> for how each function was validated and the per-function source URLs.

---

## How formulas work in Anaplan

If you come from spreadsheets, unlearn one thing first: **in Anaplan you do not write a formula in
a cell.** You write **one formula per line item**, and that single formula applies to **every cell**
of that line item at once.

### A formula applies across all cells (dimensionality)

A line item lives inside a module, and the module is dimensioned by lists and/or Time (its
**Applies To**). When you type a formula in the **formula bar**, Anaplan evaluates it for every
combination of those dimensions simultaneously, in memory.

So if a module is dimensioned by `Product × Month`, the formula `Volume * Price` is computed for
every product in every month — you write it once.

This is why **dimensionality is everything**:

- The result line item only has the dimensions of its **Applies To**. If you reference a line item
  that has a dimension yours does not, Anaplan must **aggregate** it (e.g. with `SUM`) or you must
  pick a single item (e.g. with `LOOKUP`/`SELECT`).
- If the source has *fewer* dimensions than the target, the value is simply repeated across the
  extra dimensions.
- Matching dimensions line up automatically — you never write a join. This is the superpower and
  the trap: a mismatch silently changes the result instead of erroring.

### Data types & format matching

Every line item has a **Format** (Number, Boolean, Text, Date, Time Period, List, No Data). A
formula's result **must match the line item's format**:

| Line item format | Formula must return | Typical functions |
| --- | --- | --- |
| Number | a number | `SUM`, `+ - * /`, `RANK` |
| Boolean | TRUE/FALSE | comparisons, `AND`/`OR`/`NOT`, `ISBLANK` |
| Text | text | `TEXT`, `NAME`, `LEFT`, `&` (concatenate) |
| Date | a date | `DATE`, `CURRENTPERIODSTART` |
| List (e.g. `Region`) | an item *of that list* | `ITEM`, `PARENT`, `FINDITEM` |

You cannot mix types: `"Q" & 1` fails until you convert the number with `TEXT(1)`. A formula that
returns a `Region` item cannot feed a line item formatted as `Product`.

### Operators

| Group | Operators | Notes |
| --- | --- | --- |
| Arithmetic | `+  -  *  /  ^` | `^` is power |
| Comparison | `=  <>  <  >  <=  >=` | return a Boolean |
| Logical | `AND  OR  NOT` | combine Booleans |
| Text | `&` | concatenate text |

> A bare comparison **is** a Boolean — `Revenue > 0` already returns TRUE/FALSE. You rarely need
> `IF Revenue > 0 THEN TRUE ELSE FALSE`. See [logical-functions.md](logical-functions.md).

### The one-step-per-line-item principle

The single most important habit in Anaplan: **calculate one logical step per line item, then
reference it.** Don't cram a five-stage calculation into one giant nested formula.

```
Gross Revenue   = Volume * Price          -- step 1
Discount Amount = Gross Revenue * Disc %  -- step 2 references step 1
Net Revenue     = Gross Revenue - Discount Amount
```

This is faster to recalculate, trivial to audit, and reusable. It directly serves **PLANS**:
Auditable and Performance. See [plans-standard.md](../03-methodology/plans-standard.md) and
[planual.md](../03-methodology/planual.md).

---

## Reference pages (by category)

| Page | Covers |
| --- | --- |
| [aggregation-functions.md](aggregation-functions.md) | `SUM`, `AVERAGE`, `MIN`, `MAX`, `COUNT`, `ANY`, `ALL`, plus numeric helpers `ROUND`, `ABS` |
| [lookup-and-mapping.md](lookup-and-mapping.md) | `LOOKUP`, `SELECT`, `SUM` as a mapper, `FINDITEM` — the mapping patterns |
| [time-functions.md](time-functions.md) | `CUMULATE`, `DECUMULATE`, `LAG`, `LEAD`, `OFFSET`, `POST`, `PREVIOUS`, `NEXT`, `MOVINGSUM`, `TIMESUM`, `START`/`END`, `PROFILE`, `*VALUE` |
| [text-functions.md](text-functions.md) | `TEXT`, `NAME`, `LEFT`/`RIGHT`/`MID`, `LENGTH`, `FIND`, `SUBSTITUTE`, `TRIM`, `LOWER`/`UPPER`, `CODE`, `MAKELINK`, `MAILTO` |
| [logical-functions.md](logical-functions.md) | `IF THEN ELSE`, `AND`/`OR`/`NOT`, `ISBLANK`/`ISNOTBLANK`/`BLANK`, Boolean line items |
| [date-functions.md](date-functions.md) | `DATE`, `YEAR`/`MONTH`/`DAY`, `WEEKDAY`, `DAYS`, `MONTHTODATE`, `CURRENTPERIODSTART` |
| [financial-functions.md](financial-functions.md) | `NPV`, `IRR`, `PMT`, `CUMIPMT` |
| [ranking-functions.md](ranking-functions.md) | `RANK`, `RANKCUMULATE` (Top-N) |
| [hierarchy-functions.md](hierarchy-functions.md) | `ITEM`, `PARENT`, `ISANCESTOR`, `ITEMLEVEL`, `FIRSTNONBLANK` (no `ANCESTOR`/`CHILDREN` — see page) |
| [cheatsheet.md](cheatsheet.md) | every function, one line each — the quick reference |

**Related:** [The PLANS standard](../03-methodology/plans-standard.md) ·
[The Planual](../03-methodology/planual.md) · [Sources & validation](../../SOURCES.md) ·
[All-functions index (Anapedia)](https://help.anaplan.com/all-functions-160769b0-de37-4f08-87a0-cc3aa55525a3)
