# Versions

> **Level:** L1 · **Area:** Fundamentals · **PLANS:** Logical, Necessary

**Versions** are Anaplan's built-in dimension for **planning scenarios** — typically **Actual**,
**Budget**, and **Forecast**. Like [Time](time.md), Versions is native (you don't build it as an
ordinary list), and it comes with special behaviour — **switchover** and **version formulas** — that a
plain list dimension can't offer.

---

## What Versions are for

A plan almost always compares "what really happened" against "what we planned" against "what we now
expect". Those are versions:

| Version | Meaning | Typically |
| --- | --- | --- |
| **Actual** | What happened | Imported from the GL / source systems (read-only) |
| **Budget** | The approved plan | Locked once signed off |
| **Forecast** | The latest expectation | Editable by planners going forward |

You add Versions to a module by ticking **Applies to Versions** in its blueprint. The module then holds
a separate copy of its grid per version, and you can build a `Variance` line item like
`Forecast - Budget` directly.

---

## Switchover

The signature feature of Versions is **switchover** — having a single reporting line read **Actuals up
to a point in time, then plan/forecast beyond it**.

You set a **switchover period** on a version. Before that period the version shows Actual values; from
that period onward it shows its own (forecast) values. This gives you the classic "actuals + forecast"
view without writing date-comparison formulas yourself.

```
Forecast version, switchover = Apr-25
   Jan  Feb  Mar | Apr  May  Jun …
   ←—  Actuals —→ ←——  Forecast ——→
```

> Switchover is configured on the **Versions** settings, not in a formula. Because it's period-aware, it
> stays correct as the [current period](time.md#current-period) advances — *Sustainable* by design.

---

## Formula scope: "vary by version" vs not

A line item's formula can apply to **all versions the same way**, or it can be told to **vary by
version** so different versions calculate differently:

- **Same for all versions (default):** e.g. `Revenue = Volume * Price` computes identically in Actual,
  Budget and Forecast.
- **Vary by version (version formulas):** lets a line item use a *different* formula per version — for
  instance, Actuals are imported (no formula) while Forecast is calculated from drivers.

Use version-varying formulas deliberately and sparingly; they're powerful but can make a module harder
to audit. Where you can, prefer one clear formula and let switchover handle the Actual/Forecast split.

---

## When to model scenarios as Versions vs as a list dimension

This is a frequent design decision. Versions are perfect for the **Actual / Budget / Forecast** axis,
but they are **not** the right home for an open-ended set of what-if scenarios.

| Use **Versions** when… | Use a **list dimension** when… |
| --- | --- |
| The scenarios are the standard A/B/F set | You need many, growing, user-created scenarios |
| You want **switchover** (actuals→forecast) | Scenarios are just parallel copies, no switchover |
| You want native variance & version formulas | You want users to add/remove scenarios without admin |
| The set is small and stable | The set is large or changes often |

| Decision | Why |
| --- | --- |
| "Actual vs Budget vs Forecast" | **Versions** — exactly what they're for; gives switchover + variance. |
| "10 pricing what-if scenarios planners create themselves" | A **Scenario list** dimension — versions don't scale to many, and only admins manage versions. |
| "Best / Base / Worst case on top of A/B/F" | Often a small **Scenario list** *alongside* Versions. |

> ⚠️ Versions are managed by builders/admins, not end users, and every extra version **multiplies cell
> count** like any other dimension (see [Dimensions](dimensions.md)). Don't reach for a new version when
> a list dimension — or no new dimension at all — would do. *(Necessary, Performance)*

---

## A small blueprint example

A reporting module dimensioned by `Account × Time × Versions`:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Amount | Number | Sum | Account, Time, Versions | (input / imported for Actual) |
| Budget Amount | Number | Sum | Account, Time | `Amount` (Budget version) |
| Variance to Budget | Number | Sum | Account, Time, Versions | `Amount - Budget Amount` |
| Variance % | Number (%) | Formula | Account, Time, Versions | `Variance to Budget / Budget Amount` |

Note `Variance %` uses the **Formula** summary so it recomputes correctly at parents (see
[Line items & formats → ratio trap](line-items-and-formats.md#the-classic-ratio-trap)).

---

**Related:** [Time](time.md) · [Dimensions](dimensions.md) · [Modules](modules.md) ·
[Line items & formats](line-items-and-formats.md) · [PLANS](../03-methodology/plans-standard.md) ·
[Glossary](../00-getting-started/glossary.md)

> Source: Anaplan platform documentation (Anapedia, `help.anaplan.com`). Confirm current behaviour for your platform version. See [`SOURCES.md`](../../SOURCES.md).
