# Logical Functions

> **Level:** L1 · **Area:** Formulas · **PLANS:** Performance, Auditable

Logical functions make decisions: choose between values, test conditions, combine TRUE/FALSE.
They are easy to use and easy to **overuse** — the #1 beginner anti-pattern in Anaplan is a wall of
nested `IF`s on a big module. This page shows the right tool for each job.

---

### IF THEN ELSE

**Syntax**

```
IF Condition THEN Result1 ELSE Result2
```

**What it does**
Returns `Result1` when the Boolean `Condition` is TRUE, otherwise `Result2`. You can nest it
(`… ELSE IF … THEN … ELSE …`) for multiple branches.

**Example**

```
Bonus = IF Revenue > Target THEN Revenue * Bonus % ELSE 0
```

**Watch out for**

- `Result1` and `Result2` must be the **same data type** as the line item (both numbers, both the
  same list, etc.).
- **Don't nest deeply.** Anapedia's own guidance: if you'd need **10+** `IF THEN ELSE`s, switch to
  a `LOOKUP` against a mapping module instead — faster and auditable.
  See [lookup-and-mapping.md](lookup-and-mapping.md).
- Heavy `IF` on a large cell count is a **Performance** red flag. Split logic into stepped line
  items and prefer Booleans/mappings. *(Planual: Performance, Auditable.)*

**Source:** https://help.anaplan.com/if-then-else-9fb6586e-0219-4771-a660-4ebcc317efc0

---

### AND

**Syntax**

```
Condition1 AND Condition2
```

**What it does**
Returns TRUE only when **both** Booleans are TRUE.

**Example**

```
Eligible? = Active? AND Revenue > 0
```

**Watch out for**

- Operands must be **Boolean**. A bare comparison (`Revenue > 0`) already is one — no `IF` needed
  to make it.
- For combining many flags, a dedicated Boolean line item per flag (then `AND` them) reads far
  better than one long expression.

**Source:** https://help.anaplan.com/operators-and-constants-f1c2ec15-34af-4ebe-8114-530cf7c9f3bc

---

### OR

**Syntax**

```
Condition1 OR Condition2
```

**What it does**
Returns TRUE when **at least one** Boolean is TRUE.

**Example**

```
Needs Review? = Over Budget? OR Flagged?
```

**Watch out for**

- To OR a *list item* against several options, compare via `ITEM(...)` =, or better, drive it from
  a System flag. Avoid hard-coding item names. *(Sustainable.)*

**Source:** https://help.anaplan.com/operators-and-constants-f1c2ec15-34af-4ebe-8114-530cf7c9f3bc

---

### NOT

**Syntax**

```
NOT Condition
```

**What it does**
Inverts a Boolean: TRUE becomes FALSE and vice versa.

**Example**

```
Inactive? = NOT Active?
```

**Watch out for**

- Often clearer to store the positive flag once (`Active?`) and use `NOT Active?` where needed than
  to maintain two opposite flags that can drift apart. *(Necessary.)*

**Source:** https://help.anaplan.com/operators-and-constants-f1c2ec15-34af-4ebe-8114-530cf7c9f3bc

---

### ISBLANK

**Syntax**

```
ISBLANK(Value)
```

**What it does**
Returns a **Boolean**: TRUE when the value is blank (empty), FALSE otherwise. The clean way to test
"did this cell get a value?" without comparing to `0` or `""`.

**Example**

```
Missing Region? = ISBLANK(SYS Cost Centre.Region)
```

**Watch out for**

- It is already a Boolean — use it directly, no `IF … THEN TRUE` wrapper.
- A blank number is **not** the same as `0`; `ISBLANK` distinguishes them where `= 0` would not.

**Source:** https://help.anaplan.com/isblank-709bc8d0-f645-4a83-b7d9-7cd2476cee12

---

### ISNOTBLANK

**Syntax**

```
ISNOTBLANK(Value)
```

**What it does**
The inverse of `ISBLANK`: returns TRUE when the value **is** populated. Equivalent to
`NOT ISBLANK(...)`, but reads more clearly.

**Example**

```
Has Email? = ISNOTBLANK(Contact Email)
```

**Watch out for**

- Returns a Boolean directly — no wrapper needed.

**Source:** https://help.anaplan.com/isnotblank-1463efe5-aff5-43fa-abf7-39b7d95a6692

---

### BLANK

**Syntax**

```
BLANK
```

**What it does**
A keyword that returns an **empty value** of the matching format. Use it in `IF THEN ELSE` to leave
a cell empty rather than forcing `0` or `""`. Valid for text, date, time-period and list-formatted
results.

**Example**

```
Display Date = IF Is Confirmed? THEN Order Date ELSE BLANK
```

**Watch out for**

- For **number** line items, returning `0` and returning a blank can behave differently in
  downstream sums and `ISBLANK` tests — pick the one your logic expects.

**Source:** https://help.anaplan.com/operators-and-constants-f1c2ec15-34af-4ebe-8114-530cf7c9f3bc

---

## Nested logic — and when to stop nesting

A multi-branch `IF`:

```
Band = IF Score >= 90 THEN "A" ELSE IF Score >= 75 THEN "B" ELSE IF Score >= 50 THEN "C" ELSE "D"
```

This is fine for a handful of branches. But once branches multiply, or the same condition recurs
across many line items, you are paying for it twice: it recalculates slowly and nobody can audit
it. Two escape hatches:

1. **A `LOOKUP` against a mapping module.** Put the bands/thresholds in a System module keyed by a
   list and look them up. Adding a band later needs **no formula change**.
2. **`MIN`/`MAX` arithmetic.** Many `IF`s are really clamps: `MAX(Value, 0)` floors at zero;
   `MIN(Value, Cap)` caps it — no `IF` at all.

---

## Best practice: a Boolean line item instead of repeating IF

If the **same condition** appears in several formulas, compute it **once** as a Boolean line item,
then reference that flag everywhere. This is the single highest-value logic habit in Anaplan.

```
-- System/Calc module, computed once:
Is Actual?     = START() <= CURRENTPERIODSTART()         -- Boolean line item (Date vs Date)

-- Reused, cleanly, in many places:
Reported Value = IF Is Actual? THEN Actual ELSE Forecast
Variance       = IF Is Actual? THEN 0 ELSE Forecast - Plan
```

Why this wins:

- **Performance** — the test is evaluated once, not re-derived in every formula.
- **Auditable** — the rule lives in one named line item; change it in one place.
- **Sustainable** — no hard-coded period/item scattered across the model.

> Rule of thumb: *if you wrote the same `IF` twice, it should have been a Boolean line item.*

**Related:** [lookup-and-mapping.md](lookup-and-mapping.md) (replace IF chains with mappings) ·
[aggregation-functions.md](aggregation-functions.md) (ANY/ALL roll up Booleans) ·
[The Planual — don't IF your way through everything](../03-methodology/planual.md) ·
[cheatsheet.md](cheatsheet.md)
