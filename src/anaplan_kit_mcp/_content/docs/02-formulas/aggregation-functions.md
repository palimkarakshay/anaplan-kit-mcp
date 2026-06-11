# Aggregation Functions

> **Level:** L1 · **Area:** Formulas

Aggregation functions roll detail **up** — many cells into one. They are the workhorses of any
model: turning per-product numbers into per-region totals, finding the largest value, counting
non-blank rows.

There are two shapes you will meet:

1. **Mapping aggregation** — `SUM`, `AVERAGE`, `MIN`, `MAX`, `ANY`, `ALL`, `FIRSTNONBLANK` written
   as `Source.Line Item[SUM: Mapping]`. These move a value from a finer dimension to a coarser one
   using a **mapping line item** (a System-module line item that says which target each source row
   belongs to). This is *the* Anaplan way to aggregate across lists — covered in depth in
   [lookup-and-mapping.md](lookup-and-mapping.md).
2. **Plain aggregation along a list dimension** the line item already shares (Anaplan also
   aggregates automatically up a hierarchy via the line item's **Summary** setting).

> The line item that *contains* a `[SUM: …]` formula must be dimensioned by every dimension used
> in the mapping argument. Get the dimensionality wrong and the number is silently wrong, not an
> error.

---

### SUM

**Syntax**

```
Values to sum[SUM: Mapping]
```

**What it does**
Adds up source values, grouping them onto the target by a mapping line item. The classic "push
cost-centre numbers up to region" tool.

**Example**

```
Region Cost = COST01 Cost by CC.Amount[SUM: SYS Cost Centre.Region]
```

For each region, sum every cost-centre's `Amount` whose mapping `Region` equals that region.

**Watch out for**

- The mapping line item must be **formatted as the target list** (here, `Region`).
- Your result line item must be dimensioned by `Region`; the source by `Cost Centre`.
- Blank mappings drop those source rows from the total — check your mapping is complete.

**Source:** https://help.anaplan.com/sum-fa7ab44f-c31c-4928-88b3-9fe28ca8a774

---

### AVERAGE

**Syntax**

```
Values to average[AVERAGE: Mapping]
```

**What it does**
Returns the mean of the mapped source values on each target item.

**Example**

```
Avg Deal Size = SALES.Deal Value[AVERAGE: SYS Rep.Region]
```

Average deal value per region across that region's sales reps.

**Watch out for**

- `AVERAGE` here averages the **source cells**, not a sum-divided-by-something you define. For a
  weighted average, compute `SUM(numerator) / SUM(denominator)` in separate line items instead.
- Beware blanks: a blank source cell is excluded from the average, which may not be what you want.

**Source:** https://help.anaplan.com/average-574b100e-85cb-42f2-bc3e-91f2c1d0634f

---

### MIN

**Syntax**

```
Values[MIN: Mapping]
```

**What it does**
Returns the smallest mapped value on each target item. (`MIN` is also used as a plain two-argument
comparison: `MIN(a, b)` returns the smaller of two values.)

**Example**

```
Earliest Start = TASKS.Start Date[MIN: SYS Task.Project]
```

The earliest task start date per project.

**Watch out for**

- Works on numbers and dates. For dates, "minimum" means earliest.
- Don't confuse the aggregation form `[MIN: …]` with the inline `MIN(x, y)` comparison form.

**Source:** https://help.anaplan.com/min-7ddb1ccd-5fcd-4af0-aa7a-eadfa2c3a7c8

---

### MAX

**Syntax**

```
Values[MAX: Mapping]
```

**What it does**
Returns the largest mapped value on each target item. Also available inline as `MAX(a, b)`.

**Example**

```
Peak Headcount = HC.Headcount[MAX: SYS Dept.Division]
```

The highest headcount any department reached, rolled up per division.

**Watch out for**

- `MAX(Value, 0)` is a common idiom to floor a number at zero (no negatives) — clearer and faster
  than an `IF`.

**Source:** https://help.anaplan.com/max-aggregation-function-29e3860f-86d6-419d-83f3-9c4af61a59d2

---

### COUNT

**Syntax**

```
Values to count[COUNT: Mapping]
```

**What it does**
Counts the non-blank source items mapped to each target.

**Example**

```
Reps per Region = SYS Rep.Active?[COUNT: SYS Rep.Region]
```

Number of (non-blank/active) reps in each region.

**Watch out for**

- `COUNT` counts **non-blank** cells, not "rows that are TRUE". To count Booleans that are TRUE,
  filter first (e.g. a line item that is blank when FALSE) or use `SUM` over a 1/0 indicator.
- `COUNT` is an aggregation **method** (used as `[COUNT: Mapping]`), not a standalone `COUNT(...)`
  function — Anaplan has no Excel-style `COUNTIF`; build the 1/0 indicator and `SUM` it instead.

**Source:** https://community.anaplan.com/kb/articles/153745-aggregate

---

### ANY

**Syntax**

```
Boolean values[ANY: Mapping]
```

**What it does**
Returns TRUE if **at least one** mapped source cell is TRUE. The Boolean equivalent of an OR
roll-up.

**Example**

```
Region Has Overspend? = COST01.Over Budget?[ANY: SYS Cost Centre.Region]
```

TRUE for a region if any of its cost centres is over budget.

**Watch out for**

- Source and result must be **Boolean**.
- `ANY` is the default aggregation method for Boolean line items in functions like `MOVINGSUM`.

**Source:** https://help.anaplan.com/any-8ad06ef2-8b17-4f21-b2df-990eca953ac4

---

### ALL

**Syntax**

```
Boolean values[ALL: Mapping]
```

**What it does**
Returns TRUE only if **every** mapped source cell is TRUE. The Boolean equivalent of an AND
roll-up.

**Example**

```
Region Fully Approved? = WF.Approved?[ALL: SYS Cost Centre.Region]
```

TRUE for a region only when all its cost centres are approved.

**Watch out for**

- An empty group (no source items mapped) can return TRUE — "all of nothing is true". Guard with a
  `COUNT > 0` check if that matters. (Note the *unmapped-cell* default itself differs by engine:
  TRUE in Classic, FALSE in Polaris.)

**Source:** https://help.anaplan.com/all-c9035c86-1e45-4774-9463-cc5aca76fc7e

---

## Numeric helpers: ROUND and ABS

Not aggregations, but the two number functions every beginner reaches for early — kept here so the
reference has a home for them.

### ROUND

**Syntax**

```
ROUND(Number to round [, Number of decimal places] [, Rounding direction] [, Rounding method])
```

**What it does**
Rounds a number to a given number of decimal places (default 0). Optional arguments control the
rounding **direction** and **method**; if you supply a later optional argument you must supply the
earlier ones too.

**Example**

```
Rounded Rate = ROUND(Raw Rate, 2)        -- 0.12345 -> 0.12
Whole Units  = ROUND(Forecast Units)     -- to the nearest integer
```

**Watch out for**

- Round **for display/output**, not mid-calculation, unless the business rule genuinely rounds at
  that step — repeated intermediate rounding accumulates error.

**Source:** https://help.anaplan.com/round-0d779b88-d366-4849-af05-f57367772598

---

### ABS

**Syntax**

```
ABS(Number)
```

**What it does**
Returns the **absolute value** of a number — drops the sign, so negatives become positive.

**Example**

```
Variance Magnitude = ABS(Actual - Plan)
```

**Watch out for**

- Useful for "how far off, regardless of direction" tests, e.g. `ABS(Variance) > Tolerance`.

**Source:** https://help.anaplan.com/abs-76d009f0-95e2-4233-9b72-026e49264cfd

---

## Don't forget the Summary setting

Before reaching for a `[SUM: …]`, remember that a line item already rolls **up its own list
hierarchy** automatically according to its **Summary** method (Sum / Average / Min / Max / None /
Formula). Setting the wrong summary is a classic silent bug — a line item that *averages* when it
should *sum*. *(PLANS: Logical.)* You only need an explicit aggregation function to move a value to
a **different** list via a mapping.

**Related:** [lookup-and-mapping.md](lookup-and-mapping.md) (the SUM-vs-LOOKUP mapping pattern) ·
[logical-functions.md](logical-functions.md) · [cheatsheet.md](cheatsheet.md) ·
[DISCO — System modules hold mappings](../03-methodology/disco.md)
