# Date Functions

> **Level:** L1 · **Area:** Formulas

Date functions build and dissect **date values** (a specific calendar day, like `15 Mar 2026`).

> ⚠️ **Date vs. Time Period — know the difference.** This trips up every newcomer.
>
> - A **Date** is a line item *format*: a single calendar day stored in a cell (e.g. an order date).
>   You manipulate it with the functions on this page (`DATE`, `YEAR`, `DAYS`, …).
> - **Time** is a model **dimension** — the columns Jan/Feb/Mar/Q1/FY26 across the top of a module.
>   You manipulate it with the **time series functions** (`LAG`, `CUMULATE`, `YEARVALUE`, …) in
>   [time-functions.md](time-functions.md).
>
> They connect via functions like `CURRENTPERIODSTART` (gives the *date* a time period starts) and
> period-summary functions. But a Date sitting in a cell is **not** the same as the Time dimension —
> you cannot `LAG` a Date line item, and you cannot `YEAR()` a list. Match the tool to the thing.

---

### DATE

**Syntax**

```
DATE(Year, Month, Day)
```

**What it does**
Builds a date value from three numbers. Month is 1–12, Day is 1–31.

**Example**

```
Period End = DATE(Year Num, Month Num, 28)
```

Constructs a date from numeric parts (e.g. assembling dates from imported components).

**Watch out for**

- Out-of-range parts (month 13, day 32) are invalid — validate inputs first.
- To get the day a *time period* starts, use `CURRENTPERIODSTART`, not `DATE`.

**Source:** https://help.anaplan.com/date-68d07b3e-cf86-48fc-9822-ead63c7be153

---

### YEAR

**Syntax**

```
YEAR(Date)
```

**What it does**
Extracts the year from a date as a number (e.g. `2026`).

**Example**

```
Order Year = YEAR(Order Date)
```

**Watch out for**

- Returns a **number**, so put it in a Number-formatted line item.
- Blank date in → blank/0 out; guard if you'll do arithmetic on it.

**Source:** https://help.anaplan.com/year-d5b458d3-b0f7-4b70-a28a-342ea85f8416

---

### MONTH

**Syntax**

```
MONTH(Date)
```

**What it does**
Extracts the month number (1–12) from a date.

**Example**

```
Order Month = MONTH(Order Date)        -- 3 for any date in March
```

**Watch out for**

- Returns the **month number**, not a month name or a Time period. To label it, map the number to
  text/an item.

**Source:** https://help.anaplan.com/month-38d3ce37-2f9e-4a16-8324-f3ba10c11808

---

### DAY

**Syntax**

```
DAY(Date)
```

**What it does**
Extracts the day-of-month (1–31) from a date.

**Example**

```
Day of Month = DAY(Invoice Date)
```

**Watch out for**

- This is the day **number within the month**, not the weekday — for weekday use `WEEKDAY`.

**Source:** https://help.anaplan.com/day-2acab59d-aca5-4c8a-8a79-b98f5846c200

---

### WEEKDAY

**Syntax**

```
WEEKDAY(Date [, Starting day of week])
```

**What it does**
Returns the day of the week as a number. The optional second argument sets which day counts as `1`.

**Example**

```
Is Weekend? = WEEKDAY(D) = 6 OR WEEKDAY(D) = 7
```

Flags Saturday/Sunday (numbering depends on the starting-day argument you choose).

**Watch out for**

- The number-to-day mapping depends on the **starting-day** argument — set it explicitly so the
  meaning of `1` is unambiguous.

**Source:** https://help.anaplan.com/a445eb44-98b7-4abc-8748-92435187e423

---

### DAYS

**Syntax**

```
DAYS(End date, Start date)     -- number of days between two dates
DAYS(Time period)              -- number of days in a time period
```

**What it does**
Returns a **number of days** — either between two dates, or the count of days in a given time
period (the period overload is handy for daily-rate calculations).

**Example**

```
Lead Days  = DAYS(Receipt Date, Order Date)
Days in Mth = DAYS(Period)         -- e.g. 31 for January
```

**Watch out for**

- The argument order is **(End date, Start date)** — getting it backwards flips the sign of the
  result.
- The two-date form and the period form are both called `DAYS`; the engine picks by argument type.

**Source:** https://help.anaplan.com/days-fc064281-7c00-456f-821f-a94aebc35144

---

### MONTHTODATE

**Syntax**

```
MONTHTODATE(Values to cumulate)
```

**What it does**
Cumulates a numeric line item **within each month** — a month-to-date running total that resets at
the start of every month. Most useful on daily/weekly time scales.

**Example**

```
MTD Sales = MONTHTODATE(Daily Sales)
```

**Watch out for**

- **Cannot** be used if the model's calendar type is **Weeks: General**.
- Needs a sub-monthly Time granularity for the "to date" to mean anything.

**Source:** https://help.anaplan.com/monthtodate-a5fb44d0-43cf-418b-ac60-295e09ae295a

---

### CURRENTPERIODSTART

**Syntax**

```
CURRENTPERIODSTART()
```

**What it does**
Returns the **start date of the model's Current Period** (set in Time settings). Takes no
arguments. The bridge from the Time dimension to a Date value — and the *sustainable* way to ask
"are we in the past?" without hard-coding a date.

**Example**

```
Is Actual? = Period Start Date < CURRENTPERIODSTART()
```

A Boolean that flips actual/forecast automatically as the Current Period rolls forward — no formula
edit ever needed. *(Sustainable.)*

**Watch out for**

- Returns a **Date**, not a Time period.
- It tracks the **Current Period** setting, so changing that setting re-drives every formula that
  uses it — which is exactly the point.

**Source:** https://help.anaplan.com/currentperiodstart-a7af7113-e1dc-478d-bbbe-ecb597092991

---

**Related:** [time-functions.md](time-functions.md) (the Time dimension family) ·
[logical-functions.md](logical-functions.md) (CURRENTPERIODSTART feeds Is Actual? flags) ·
[The Planual — no hard-coded dates](../03-methodology/planual.md) · [cheatsheet.md](cheatsheet.md)
