# DISCO — Module Design Pattern

> **Level:** L2 · **Area:** Methodology · **PLANS:** Logical, Auditable, Sustainable

**DISCO** is how you decide *what kind of module* you're building and *where logic belongs*. Every
module in a well-built model should fall into exactly one of five categories. Mixing categories in
one module is the #1 cause of slow, unauditable models.

| Letter | Module type | Holds | Changes how often? |
| --- | --- | --- | --- |
| **D** | **Data** | Imported transactional/source data, as-is. The landing zone. | Every load |
| **I** | **Inputs** | Numbers humans type in (assumptions, drivers, rates). | When planners plan |
| **S** | **System** | Time/date attributes, mappings, flags, hierarchy properties. | Rarely (structural) |
| **C** | **Calculations** | The engine room — formulas that combine Inputs + Data + System. | Recalculates |
| **O** | **Outputs** | Reporting views formatted for dashboards/exports. | Read-only |

> Order people usually build in: **D → I → S → C → O** (and data flows the same way).

---

## What goes where

### D — Data

- The raw result of an import (e.g. `DAT01 Actuals from GL`).
- Keep it **flat and faithful** to the source. Don't calculate here.
- Often dimensioned by a **numbered list** for transactional rows.

### I — Inputs

- Driver assumptions: growth %, price, headcount plan, FX rates.
- These are the only modules most planners should be able to **edit**.
- Style: clear, dashboard-friendly, minimal dimensionality.

### S — System

- The quiet backbone: `SYS01 Time Settings`, `SYS02 Account Details`, mapping modules that link
  one list to another, Boolean flags (`Is Actual?`, `Include in Plan?`).
- Built **once**, referenced **everywhere**. This is what makes a model *sustainable* — change the
  flag in one place, the whole model follows.

### C — Calculations

- Where Inputs, Data and System meet. Revenue = Volume × Price; allocations; roll-ups.
- **Break logic into steps** (one line item per step) for speed and auditability.
- Usually not shown directly to users.

### O — Outputs

- The presentation layer: a module shaped exactly for a dashboard card or an export file.
- No new business logic — just selecting, formatting, and arranging existing results.

---

## Naming convention (recommended)

Prefix modules so the type is obvious in any list:

```
DAT01 Actuals from GL          (Data)
INP01 Revenue Assumptions      (Inputs)
SYS01 Time Settings            (System)
SYS02 Cost Centre Details      (System)
CAL01 Revenue Calculation      (Calculations)
OUT01 P&L Report               (Outputs)
```

See [`templates/naming-conventions.md`](../../templates/naming-conventions.md).

---

## Why DISCO matters (PLANS link)

- **Logical / Auditable:** anyone opening the model can see where data enters, where humans input,
  and where numbers are computed.
- **Sustainable:** mappings and flags live in **System** modules, so structural change is a
  one-place edit.
- **Performance:** separating a small **Inputs** module from a large **Calculations** module means
  you don't recalculate the whole engine when someone types one number.

**Related:** [PLANS](plans-standard.md) · [The Planual](planual.md) · every model in
[`blueprints/`](../../blueprints/) tags its modules by DISCO type.

> Source: DISCO module-design pattern (Anaplan Academy / Community best-practice materials). See [`SOURCES.md`](../../SOURCES.md).
