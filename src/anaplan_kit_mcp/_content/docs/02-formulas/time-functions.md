# Time Series Functions

> **Level:** L2 · **Area:** Formulas

These are the **time series functions** — the family that works *along the Time dimension*: shift a
value forward/back, accumulate it, sum a rolling window, or read a higher time-summary value. They
are what make rolling forecasts, opening/closing balances, lead-time logistics and YTD figures
possible.

The core family is: `CUMULATE`, `DECUMULATE`, `LAG`, `LEAD`, `MOVINGSUM`, `OFFSET`, `POST`,
`PREVIOUS`, `NEXT`, `PROFILE`, `START`/`END`, plus `TIMESUM` and the period-summary functions
`YEARVALUE`/`HALFYEARVALUE`/`QUARTERVALUE`/`MONTHVALUE`.

> Your module must have **Time** as a dimension for most of these to do anything. The exact set of
> time periods comes from the model's Time settings / Time Ranges.

---

### CUMULATE

**Syntax**

```
CUMULATE(Values to cumulate [, Boolean to include] [, list to cumulate over])
```

**What it does**
Running total: each period gets the sum of itself and all earlier periods.

**Example**

```
YTD Revenue = CUMULATE(Revenue)
```

A cumulative running total of `Revenue` across the timeline. Add a Boolean to restart the
accumulation (e.g. reset each year).

**Watch out for**

- The optional Boolean **includes/excludes** periods — a common pattern is to feed it
  `Time Settings.Year To Date?` to get a clean YTD that resets annually.
- It cumulates across the module's Time by default; the third argument lets it cumulate over a list
  instead.

**Source:** https://help.anaplan.com/cumulate-1173a903-81bb-4838-a4d0-1c9f9c739aa3

---

### DECUMULATE

**Syntax**

```
DECUMULATE(Values to decumulate [, Boolean to include] [, list to decumulate over])
```

**What it does**
The inverse of `CUMULATE`: subtracts the previous period's value from the current. Turns a
cumulative/balance series back into period movements. The first period returns its input value.

**Example**

```
Monthly Movement = DECUMULATE(Cumulative Balance)
```

Recovers each month's change from a running balance.

**Watch out for**

- First period has no prior, so it returns the raw input — check that's the behaviour you want.
- The optional Boolean restarts the de-cumulation; the optional list de-cumulates over that list
  instead of Time, mirroring `CUMULATE`.

**Source:** https://help.anaplan.com/decumulate-eab1f7ce-5c1d-46b6-8361-69086d4876e7

---

### LAG

**Syntax**

```
LAG(Value to offset, Offset amount, Substitute value [, Non-positive behavior, List])
```

**What it does**
Returns the value from **N periods earlier**. The bread-and-butter "prior period" function.

**Example**

```
Prior Month Sales = LAG(Sales, 1, 0)
```

Last month's sales; for the very first period (no prior) it returns the substitute `0`.

**Watch out for**

- The **substitute value** fills periods where the offset falls off the start of time — don't omit
  it or you'll get blanks where you expected zeros.
- `Offset amount` can itself be a line item (a *variable* lag), enabling driver-based shifts.
- For a *fixed* one-period look-back, `PREVIOUS` is simpler; `LAG` wins when the offset varies.

**Source:** https://help.anaplan.com/lag-3064919f-964e-4b84-be56-15f0e127e371

---

### LEAD

**Syntax**

```
LEAD(Value to offset, Offset amount, Substitute value [, Non-positive behavior, List])
```

**What it does**
The forward-looking twin of `LAG`: returns the value from **N periods later**.

**Example**

```
Next Quarter Demand = LEAD(Demand, 1, 0)
```

Reads next period's demand; substitutes `0` past the end of time.

**Watch out for**

- Same substitute-value rule as `LAG`, but at the **end** of the timeline.
- Like `LAG`, the offset can be a line item for variable look-ahead.

**Source:** https://help.anaplan.com/lead-e3f4969b-65b1-4726-b41c-d028c9c71c14

---

### OFFSET

**Syntax**

```
OFFSET(Value to offset, Offset amount, Substitute value [, List])
```

**What it does**
Returns the value a given number of periods away — **positive** offset looks forward, **negative**
looks back. Think of it as `LAG`/`LEAD` combined, with the direction set by the sign.

**Example**

```
Three Months Ago = OFFSET(Headcount, -3, 0)
```

Headcount three periods earlier; `0` before the timeline begins.

**Watch out for**

- Sign convention catches everyone out: **negative = earlier**, positive = later.
- Don't forget the substitute value for edge periods.

**Source:** https://help.anaplan.com/offset-4f5a095c-0e7a-4f1a-b6ea-0ef8f88d6c3f

---

### POST

**Syntax**

```
POST(Value to post, Number of periods [, List])
```

**What it does**
"Posts" a value **forward** by N periods — the value *leaves* the current period and *arrives*
later. Classic use: stock ordered now arrives after a lead time. (Conceptually the reverse-read of
`OFFSET`: instead of *reading* from another period, it *places* a value into a future one.)

**Example**

```
Stock Arrivals = POST(Orders Placed, Lead Time Months)
```

Each order placed shows up as an arrival `Lead Time Months` later.

**Watch out for**

- Values posted past the end of the timeline are lost.
- If several source values land on the **same** target period, `POST` **adds them together**.
- The time range of the argument must match the result line item's time range.

**Source:** https://help.anaplan.com/post-082cb491-879c-4711-b5c6-9ed162391bb1

---

### PREVIOUS

**Syntax**

```
PREVIOUS(Value)
```

**What it does**
Returns the value from the **immediately preceding** period (or list item). A simpler, fixed
one-step `LAG`.

**Example**

```
Opening Balance = PREVIOUS(Closing Balance)
```

This period opens where the last one closed — the canonical balance-roll pattern.

**Watch out for**

- First period returns blank (no prior) — handle it, e.g. `IF ISBLANK(PREVIOUS(...)) THEN Opening
  Input ELSE PREVIOUS(...)`.
- Beware accidental **circularity** in balance formulas; Anaplan resolves period-to-period chains
  but flags true cycles.

**Source:** https://help.anaplan.com/previous-e5806da3-1ae6-4b45-9e02-68ac764cb97d

---

### NEXT

**Syntax**

```
NEXT(Value)
```

**What it does**
Returns the value from the **immediately following** period (or list item) — the forward twin of
`PREVIOUS`.

**Example**

```
Next Period Plan = NEXT(Plan)
```

**Watch out for**

- Last period returns blank (no successor).
- For a *variable* look-ahead, use `LEAD`/`OFFSET` instead.

**Source:** https://help.anaplan.com/next-ce38460d-e931-403a-837c-d650d0ddaf64

---

### MOVINGSUM

**Syntax**

```
MOVINGSUM(Line item to aggregate [, Start offset] [, End offset] [, Aggregation method] [, List])
```

**What it does**
Aggregates a **rolling window** of periods that moves with time — e.g. a trailing 3-month sum.
Default method is `SUM` for numbers (`ANY` for Boolean, `FIRSTNONBLANK` for text/date/list).

**Example**

```
Rolling 3M Sales = MOVINGSUM(Sales, -2, 0)
```

Sum of this month plus the two before it (a trailing-3 window).

**Watch out for**

- Offsets are **relative to the current period**: `-2, 0` = last 3 months; `0, 2` = next 3.
- Override the aggregation method to get a moving average etc.; otherwise it sums.

**Source:** https://help.anaplan.com/movingsum-37394929-ea62-4e55-9655-b8c8c2732679

---

### TIMESUM

**Syntax**

```
TIMESUM(Line item to aggregate [, Start period] [, End period] [, Aggregation method])
```

**What it does**
Aggregates between **two fixed time periods** and returns **a single value** repeated across time —
unlike `MOVINGSUM`, the window does *not* move with the current period.

**Example**

```
FY Total = TIMESUM(Revenue, START(), END())
```

Total revenue across the whole timeline, shown identically in every period.

**Watch out for**

- Returns the **same** total in every period — useful as a denominator (e.g. % of full-year).
- Default method by data type, same as `MOVINGSUM`.

**Source:** https://help.anaplan.com/timesum-45c3bc48-4d80-490d-9b18-76af505c6907

---

### START / END

**Syntax**

```
START()            -- first date of the source module's Time dimension
END()              -- last date of the source module's Time dimension
START(Time Period) -- first date of a given time period
END(Time Period)   -- last date of a given time period
```

**What it does**
`START` returns the **first date** of a time period (or of the whole timeline when called with no
argument); `END` returns the **last date**. They are the bridge from a Time period to a `Date`
value — handy for maturity/due dates and as the bounds for `TIMESUM`.

**Example**

```
Period Start Date = START()                  -- the start date of each period on the timeline
Period End Date   = END()                    -- the last date of each period
FY Total          = TIMESUM(Revenue, START(), END())
```

**Watch out for**

- Both return a **Date**, not a Time period — put the result in a Date-formatted line item.
- With an argument, the source must be **time-period-formatted**; a blank period gives a blank date.
- The displayed date format follows the viewer's browser/OS locale.

**Source:** START https://help.anaplan.com/start-bc44fa0b-7af8-4a8f-ad8f-cbeaccf22003 ·
END https://help.anaplan.com/end-3d41a077-b391-45ca-a6e2-0c6dfaaeb85f

---

### PROFILE

**Syntax**

```
PROFILE(Numbers to change, Profile)
```

**What it does**
Multiplies a value across time according to a **profile** — a sequence of weights dimensioned by a
list *other than* Time. Each number is multiplied by the first profile weight in the first period,
the second weight in the next period, and so on — the natural way to phase an annual figure over
months by a seasonality curve.

**Example**

```
Phased Spend = PROFILE(Annual Budget, Seasonality %)
```

Allocates the annual budget over periods using the seasonality weights.

**Watch out for**

- The profile defines the *shape*; make sure its weights sum to what you intend (often 1 / 100%).
- The `Profile` argument is dimensioned by a **non-Time** list; the function walks its values across
  successive time periods.

**Source:** https://help.anaplan.com/41b5fb84-395b-489f-80be-521add72c581

---

### YEARVALUE / HALFYEARVALUE / QUARTERVALUE / MONTHVALUE

**Syntax**

```
YEARVALUE(Line item)
HALFYEARVALUE(Line item)
QUARTERVALUE(Line item)
MONTHVALUE(Line item)
```

**What it does**
Each returns the **time-summary value of the enclosing period** and writes it down to the finer
periods inside it. `YEARVALUE` puts the year's total (per the line item's Summary method) onto
every month of that year; `QUARTERVALUE` does the same at quarter level, and so on.

**Example**

```
Pct of Year = Revenue / YEARVALUE(Revenue)
```

Each month's share of its full-year revenue — `YEARVALUE` supplies the annual total in every month.

**Watch out for**

- The value returned respects the line item's **Summary** setting (Sum/Average/…). A line item set
  to Average will give the *average*, not the total — a frequent surprise.
- These need the corresponding period to exist in your Time settings (a model with no
  half-years can't use `HALFYEARVALUE`).

**Source:** YEARVALUE https://help.anaplan.com/yearvalue-5df8cf5a-6609-4e14-832f-ddff9b29326b ·
HALFYEARVALUE https://help.anaplan.com/halfyearvalue-d78dd47b-5f5c-4e06-9788-7b1de7446b29 ·
QUARTERVALUE https://help.anaplan.com/quartervalue-496d28ac-cf36-43bf-bc0e-06d4cc52c40e ·
MONTHVALUE https://help.anaplan.com/monthvalue-0f2e55c3-8808-4b37-9017-7ea57e6f0d37

---

**Related:** [date-functions.md](date-functions.md) (dates vs time periods) ·
[aggregation-functions.md](aggregation-functions.md) ·
[Performance — time calculation](../07-performance/) ·
[cheatsheet.md](cheatsheet.md)
