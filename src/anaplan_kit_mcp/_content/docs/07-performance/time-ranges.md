# Time Ranges

> **Level:** L2 · **Area:** Performance · **PLANS:** Performance, Necessary

A **Time Range** lets a module or line item span **only part** of the model calendar instead
of the full timeline. Because [cell count](sparsity-and-engine.md) multiplies by the size of
the Time dimension, shrinking how many periods a module covers is one of the easiest, safest
ways to cut a model down.

## The problem they solve

Your **model calendar** might run, say, 2020–2030 monthly — 132 months — so every module can
reach any period. But most modules don't *need* all of it:

- A **detailed driver** module is only planned for the **current + next year** (24 months).
- A **historical actuals** module only needs the **past 3 years**.
- A **long-range output** might need years, but at **yearly**, not monthly, granularity.

Without Time Ranges, each of those modules is sized for the **full 132 months** anyway —
paying for periods it never uses.

## How a Time Range works

A **Time Range** is a named, reusable definition of a span of the calendar — a start period,
an end period, and a granularity (e.g. months/quarters/years). You define it once at the model
level, then assign it to a module (or to individual line items).

```
Model calendar:        Jan 2020 ────────────────────────── Dec 2030   (132 months)

Time Range "Plan 2yr": Jan 2026 ──── Dec 2027   (24 months)  ← assign to driver modules
Time Range "Hist 3yr": Jan 2023 ──── Dec 2025   (36 months)  ← assign to actuals modules
```

A module on `Plan 2yr` has cells for **24** months, not 132 — an ~82% cut on the Time
dimension before you touch anything else. The reduction multiplies through every other
dimension in the module.

## When to use them

- **Driver / input modules** that only plan a near horizon → a short forward range.
- **Actuals / history** modules → a backward range covering only loaded history.
- **Detailed monthly calc** that feeds a **summary yearly output** → monthly range on the
  detail, yearly range on the summary.
- Anywhere a module clearly **doesn't span the whole calendar** — which is most modules.

> Right-sizing time is as important as right-sizing lists. *"Does this module need every
> period?"* belongs next to *"does it need every dimension?"* *(Necessary, Performance.)*

## Pitfalls

| Pitfall | What happens | Avoid by |
| --- | --- | --- |
| Formula references **outside** the range | A `LOOKUP`/`LAG` reaching a period not in the module's range returns blank/zero | Ensure source and target ranges overlap where the formula needs them |
| **Mismatched ranges** across linked modules | Values "disappear" at the edges when one module's range is narrower | Plan ranges as a set; keep linked modules' overlaps deliberate |
| **Granularity mismatch** | A monthly module feeding a yearly one (or vice-versa) needs the right time aggregation/`YEARVALUE` etc. | Match granularity intentionally; use time functions to bridge |
| Range **too tight** | Next year arrives and the module has no cells for it | Use ranges that roll, or widen before period rollover |
| Treating it as **cosmetic** | Hiding periods on a view isn't the same as a Time Range — hidden periods still exist as cells | Use a real Time Range to actually remove the cells |

> **Hiding ≠ removing.** Filtering periods off a view doesn't shrink the module. Only a Time
> Range removes the underlying cells.

## Good practice

- Create a **small set of named Time Ranges** ("Plan 2yr", "Hist 3yr", "LRP yearly") and
  reuse them — don't invent a one-off per module. *(Sustainable.)*
- Assign the **tightest range each module genuinely needs**.
- Check **cross-module formulas** still line up after assigning ranges.
- Revisit ranges at **calendar rollover** so forward-looking modules keep enough periods.

**Related:** [Performance overview](README.md) ·
[Sparsity & cell count](sparsity-and-engine.md) ·
[Line item subsets](line-item-subsets.md) ·
[Optimization checklist](optimization-checklist.md) ·
[Time — fundamentals](../01-fundamentals/time.md)

> Source: Anaplan Time Ranges docs (`help.anaplan.com`, Time / performance sections). See
> [`SOURCES.md`](../../SOURCES.md).
