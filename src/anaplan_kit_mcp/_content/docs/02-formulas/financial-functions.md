# Financial Functions

> **Level:** L2 · **Area:** Formulas

Financial functions handle the time-value-of-money maths behind investment cases and loan
schedules: net present value, internal rate of return, and loan payments.

> ⚠️ These functions have **engine-specific behaviour and multiple syntaxes** (for example `NPV`
> and `IRR` each have a *cash-flow-over-Time* form **and** a *date/value-pairs* form, which take
> different arguments). The signatures below are the common forms verified against Anapedia —
> **always confirm the exact arguments on the linked Anapedia page for your engine and use case.**

---

### NPV

**Syntax**

```
-- Cash-flow-over-Time form (module dimensioned by Time):
NPV(Interest rate, Cash flow line item)
-- (A second form takes pairs of dates and cash flows; arguments differ.)
```

**What it does**
Calculates the **net present value** of a series of cash flows (inflows positive, outflows
negative) discounted at a constant interest rate.

**Example**

```
Project NPV = NPV(Discount Rate, Net Cash Flow)
```

Discounts the `Net Cash Flow` series back to a present value at `Discount Rate`.

**Watch out for**

- There are **two syntaxes** (time-series vs. date/value pairs); which one applies is determined by
  whether you pass more or fewer than two arguments.
- The rate must match the cash-flow **period** (a monthly series needs a monthly rate).

**Source:** https://help.anaplan.com/npv-d2331d84-a431-4179-8c82-9846f0c453d0

---

### IRR

**Syntax**

```
IRR(Cash flow line item)              -- cash-flow-over-Time form
-- (A second form takes date/cash-flow pairs and more arguments.)
```

**What it does**
Returns the **internal rate of return** — the discount rate at which the NPV of the cash flows is
zero.

**Example**

```
Project IRR = IRR(Net Cash Flow)
```

**Watch out for**

- Like `NPV`, `IRR` has two forms distinguished by **how many arguments** you pass — more or fewer
  than two arguments selects the form. The date/value-pairs form is the equivalent of Excel's
  `XIRR`.
- IRR needs at least one sign change in the cash flows (an outflow then inflows) to have a solution;
  unusual flows can yield no/odd results.

**Source:** https://help.anaplan.com/irr-3e65abd3-a8d8-4cb7-af34-937232ae79c5

---

### PMT

**Syntax**

```
PMT(Interest rate, Number of periods, Present value [, Future value] [, Timing])
```

**What it does**
Returns the **periodic payment** for a loan or annuity, given a constant rate and number of
periods.

**Example**

```
Monthly Payment = PMT(Annual Rate / 12, Term Months, Loan Amount)
```

The level monthly payment that repays `Loan Amount` over `Term Months`.

**Watch out for**

- The **rate and the number of periods must use the same unit** — a monthly schedule needs a
  monthly rate (annual ÷ 12).
- `Timing` controls payment at start vs. end of period; the optional `Future value` defaults to 0.
- Sign convention: present value and payment typically have opposite signs.

**Source:** https://help.anaplan.com/pmt-07d126f7-dd4d-4510-b15d-add22fc527fd

---

### CUMIPMT

**Syntax**

```
CUMIPMT(Interest rate, Number of periods, Principal, Start period, End period [, Timing])
```

**What it does**
Returns the **cumulative interest** payable on a loan between a start and end period.

**Example**

```
Interest Yr1 = CUMIPMT(Annual Rate / 12, Term Months, Loan Amount, 1, 12)
```

Total interest paid across months 1–12.

**Watch out for**

- Same rate/period unit-matching rule as `PMT`.
- `Start period` / `End period` are **period numbers** within the loan, not dates.

**Source:** https://help.anaplan.com/2f6eca23-c0b6-4b4b-a68c-1def28d2dab6

---

> Related financial functions exist in Anaplan (`PPMT`, `NPER`, …). If you need them, look them up
> in the all-functions index and confirm arguments before use — don't guess.

**Related:** [time-functions.md](time-functions.md) (cash flows live on the Time dimension) ·
[All-functions index (Anapedia)](https://help.anaplan.com/all-functions-160769b0-de37-4f08-87a0-cc3aa55525a3) ·
[cheatsheet.md](cheatsheet.md)
