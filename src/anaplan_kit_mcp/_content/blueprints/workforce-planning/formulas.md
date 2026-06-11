# Workforce Planning — Key Formulas

> **Level:** L2 · **Area:** Blueprint (Workforce) · **DISCO:** Calculations

**Hire-date proration** is the formula that makes a workforce model real: a joiner who starts on the
15th costs roughly half that month. It leans entirely on the shared date flags in
[`SYS01`](../_common/time-and-versions.md). One line item per step. *(Auditable)*

---

## 1. Resolve each position (roster vs planned hire)

`SYS30 Position Details.Effective Salary (local)`:

```
IF INP01 Planned Hires.Is Planned Hire?
   THEN IF ISNOTBLANK(INP01 Planned Hires.Planned Salary (local))
           THEN INP01 Planned Hires.Planned Salary (local)
           ELSE INP02 Comp Assumptions.Default Salary (local)[LOOKUP: Job Grade]
   ELSE DAT01 Current Roster.Annual Salary (local)
```

A planned hire with no salary falls back to its **Job Grade** band default — so a req can be created
with just a grade and a start date. The same resolve pattern fills Cost Centre, FTE and start date.
*(Sustainable — open reqs need minimal data to plan.)*

---

## 2. Hire-date proration (the signature calc)

How many days of the month is the position active? Overlap the position's `[Start, End]` window with
the month's `[Period Start Date, Period End Date]` (both from shared `SYS01`).

`CAL01.Active Days`:

```
MAX( 0,
     MIN( SYS01 Time Settings.Period End Date,
          IF ISBLANK(SYS30 Position Details.Effective End Date)
             THEN SYS01 Time Settings.Period End Date
             ELSE SYS30 Position Details.Effective End Date )
   - MAX( SYS01 Time Settings.Period Start Date,
          SYS30 Position Details.Effective Start Date )
   + 1 )
```

- `MAX(period start, hire date)` = first active day in the month.
- `MIN(period end, leave date)` = last active day (open-ended ⇒ month end).
- `+ 1` because both endpoints are inclusive; `MAX(0, …)` zeros out months before hire / after leave.

`CAL01.Proration Factor`:

```
Active Days / SYS01 Time Settings.Days in Period
```

`Days in Period` is the shared calendar value — so Feb (28/29) and 31-day months prorate correctly
with **no hard-coded 30**. *(Sustainable — calendar lives in `_common`.)*

---

## 3. Salary cost

`CAL02.Monthly Salary (local)`:

```
SYS30 Position Details.Effective Salary (local) / 12
  * SYS30 Position Details.Effective FTE
  * CAL01 Active Proration.Proration Factor
```

Annual ÷ 12 = full monthly salary; × FTE (part-time) × proration (part-month). A 0.5-FTE hire
starting mid-March pays `salary/12 × 0.5 × ~0.55`. *(Auditable — each factor is visible.)*

---

## 4. Employer load → fully-loaded cost

```
Load Amount (local) = Monthly Salary (local)
                      * INP02 Comp Assumptions.Load %[LOOKUP: SYS30 Position Details.Job Grade]
Fully-Loaded Cost (local) = Monthly Salary (local) + Load Amount (local)
```

The `Load %` is looked up by the position's Job Grade — change a grade's load once, every position
on that grade follows. *(Sustainable)*

---

## 5. Currency conversion (nested LOOKUP) and the FP&A hand-off

A position inherits its Cost Centre's currency (`CAL04.FX Rate`):

```
SYS04 Exchange Rates.Rate (filled)[
   LOOKUP: SYS02 Organization Details.Local Currency[
      LOOKUP: SYS30 Position Details.Cost Centre ] ]
```

Then `Fully-Loaded Cost (USD) = Fully-Loaded Cost (local) * FX Rate`. For the FP&A hand-off, aggregate the
**local** cost to the finance grain (`CAL04.Cost by CC (local)`):

```
CAL03 Fully-Loaded Cost.Fully-Loaded Cost (local)[SUM: SYS30 Position Details.Cost Centre]
```

This collapses the numbered Position list down to **L3 Cost Centre × Time × Versions**. `Cost by CC (USD)`
is the same roll-up of the USD line for this model's own reporting; the FP&A feed itself is sent in **local**
so FP&A converts once.

### The FP&A `Salaries` hand-off (model-to-model import)

Workforce and FP&A are **separate models**, so the feed is a scheduled **model-to-model import**. Workforce's
`Cost by CC (local)` lands in FP&A's `INP02 Opex Plan.Opex (local)` against the **fixed `Opex Category` member
`"Salaries"`** — Workforce replaces FP&A's typed Salaries opex with a driver-based labour cost.

| Workforce source line item | FP&A target line item | Mapping |
| --- | --- | --- |
| `CAL04 Cost in USD.Cost by CC (local)` (L3 Cost Centre × Time × Versions) | `INP02 Opex Plan.Opex (local)` | `L3 Cost Centre/Entity` → `L3 Cost Centre/Entity` (shared); `Time` → `Time`; `Versions` → `Versions`; **`Opex Category` ← fixed value `"Salaries"`** (constant in the import definition — Workforce has no Opex Category axis, so the import pins every row to the Salaries member) |

Same shared FX (`SYS04`) as Sales and FP&A, so rates match across domains.
See [fpa-pl-planning/modules.md](../fpa-pl-planning/modules.md) (INP02) and
[fpa-pl-planning/formulas.md](../fpa-pl-planning/formulas.md).

---

## 6. Headcount & FTE roll-ups

```
Headcount = Is Active This Month?[SUM: SYS30 Position Details.Cost Centre]
FTE       = (Effective FTE * Proration Factor)[SUM: SYS30 Position Details.Cost Centre]
```

Headcount counts active positions (a Boolean sums as a count); FTE is proration-weighted, so a
mid-month 0.5-FTE hire adds ~0.27 FTE that month. *(Logical)*

---

## Consistency check

```
DAT01 Roster / INP01 Hires ─► SYS30 Position Details (resolve)
SYS30 + SYS01 dates ───────► CAL01 Proration Factor
CAL01 × SYS30 salary ──────► CAL02 Monthly Salary ─► CAL03 Fully-Loaded ─► CAL04 (USD + local)
CAL04 Cost by CC (USD) ────► OUT01 Labour Cost
CAL04 Cost by CC (local) ──► import ─► FP&A INP02 Opex Plan (Opex Category = "Salaries")
```

Every cost traces back to a loaded employee or a typed req plus the shared calendar and FX.

---

**Related:** [`modules.md`](modules.md) · [`README.md`](README.md) ·
[`_common/time-and-versions.md`](../_common/time-and-versions.md) (dates, `Days in Period`) ·
[FP&A formulas](../fpa-pl-planning/formulas.md) ·
[Formula reference](../../docs/02-formulas/) (`MIN`, `MAX`, date math)
