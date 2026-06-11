# Time

> **Level:** L1 · **Area:** Fundamentals · **PLANS:** Sustainable, Performance

Almost every plan happens *over time* — by month, by quarter, by year. Anaplan gives you a **built-in
Time dimension** so you don't have to model the calendar as an ordinary list. You configure it **once**
per model in **Time Settings**, and then any module can use it by ticking "Applies to Time".

---

## The Time dimension

Time is special: it's a native dimension that Anaplan understands as a *calendar*, which unlocks
time-intelligence functions (`LAG`, `CUMULATE`, `YEARVALUE`, period-to-date, etc. — see
[Formulas](../02-formulas/)) and automatic roll-ups from days → weeks → months → quarters → years.

> Don't build a "Month" list by hand. Use the Time dimension — it gives you the calendar hierarchy,
> the time functions, and sustainable behaviour as years roll over, for free. *(Sustainable)*

---

## Configuring Time (Time Settings)

You set these once for the whole model:

| Setting | What it controls | Example |
| --- | --- | --- |
| **Calendar type** | The shape of the year (standard months, weeks, or custom) | Calendar Months/Quarters/Years; Weeks (4-4-5 etc.) |
| **Fiscal year start** | Which month the year begins | Jan (calendar) or, say, Apr / Jul / Oct (fiscal) |
| **Model start / number of years** | The overall span of Time available | FY2024 + 3 years |
| **Period types to show** | Which aggregation levels are visible | Months, Quarters, Half-years, Years |

### Calendar types

- **Calendar Months/Quarters/Years** — the standard 12-month structure.
- **Weeks: 4-4-5 / 4-5-4 / 5-4-4 / 13×4** — retail/financial calendars where quarters are built from a
  fixed pattern of weeks.
- **Weeks: general** — define your own week-based structure.

### Fiscal year start

If your fiscal year doesn't begin in January, set the **fiscal year start month**. Then "FY2025" and
year-to-date functions align to *your* fiscal calendar, not the Gregorian one. Set this correctly up
front — changing it later is disruptive.

---

## Period types

Once Time is configured, these aggregation levels become available as needed:

| Period type | Notes |
| --- | --- |
| **Day** | Finest grain; only enable if you genuinely plan daily (it's large). |
| **Week** | For week-based calendars. |
| **Month** | The most common planning grain. |
| **Quarter** | Roll-up of months. |
| **Half-year** | Roll-up of quarters. |
| **Year** | Top roll-up. |

Higher periods aggregate the lower ones automatically, using each line item's
[**summary method**](line-items-and-formats.md) — e.g. `Revenue` (Sum) totals its months into the
quarter, while `Margin %` (Formula/Ratio) is recomputed at the quarter rather than summed.

---

## Timescale and "Applies to Time"

A module gets a Time dimension when you tick **Applies to Time** in its blueprint. You then choose its
**timescale** — the period type the module is *stored at* (e.g. store at Month, with Quarter/Year as
automatic roll-ups). Storing at the coarsest grain you can get away with is a real performance lever.

```
Module "CAL Revenue"  — Applies To: Product × Time (Month)
   Jan-25  Feb-25  Mar-25  …   (Q1-25, FY25 appear automatically as roll-ups)
```

---

## Current period

Anaplan tracks one **current period** — the period it treats as "now". It drives time functions and is
the basis for "is this actual or forecast?" logic.

> Best practice: **don't hard-code "now"** into formulas (e.g. `IF Time = Mar 25`). Instead drive
> current-period logic from the model's current period and a **System module** (e.g. a `SYS Time`
> module with Boolean flags like `Is Actual Period?`). That keeps the model working as time advances —
> the **S** in [PLANS](../03-methodology/plans-standard.md). See [DISCO → System](../03-methodology/disco.md).

---

## Time Ranges (brief intro)

By default a Time-dimensioned line item spans the model's *entire* calendar. Often it doesn't need to:
a 3-year actuals module doesn't need the 10-year planning horizon, and a daily module certainly doesn't
need every day for a decade.

A **Time Range** is a named, custom span of periods (e.g. `FY24-FY26 Months`) you apply to a module so
it stores **only** the periods it actually needs — dramatically cutting cell count. Time Ranges are one
of the most effective [performance](../07-performance/) tools and a core L2 skill.

→ Full treatment: **[Performance → Time Ranges](../07-performance/time-ranges.md).**

---

**Related:** [Versions](versions.md) · [Dimensions](dimensions.md) · [Modules](modules.md) ·
[Line items & formats](line-items-and-formats.md) · [Time Ranges](../07-performance/time-ranges.md) ·
[Formulas](../02-formulas/) · [Glossary](../00-getting-started/glossary.md)

> Source: Anaplan platform documentation (Anapedia, `help.anaplan.com`). Confirm current behaviour for your platform version. See [`SOURCES.md`](../../SOURCES.md).
