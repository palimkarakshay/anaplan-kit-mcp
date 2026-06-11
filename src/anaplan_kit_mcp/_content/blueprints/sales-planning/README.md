# Sales Planning — Blueprint

> **Level:** L2 · **Area:** Blueprint (Sales) · **DISCO:** mixed

Plans **sales targets by rep and product**, sets **quotas** from a top-down number, and tracks a
**pipeline** to see whether coverage is sufficient. Its product **Target (USD)** is the revenue signal
that reconciles with the FP&A model's `CAL03 Currency Conversion.Revenue (USD)`.

---

## What this model does

1. Reps are organised into **territories**; each rep maps to a **Cost Centre** in the shared org.
2. Leadership sets a **top-down target** per territory × product (Inputs).
3. The engine **allocates** the target down to reps by a weight (e.g. prior attainment), producing a
   per-rep **quota**.
4. A **pipeline** of open opportunities is loaded (Data) and weighted by probability.
5. **Coverage** = weighted pipeline ÷ quota tells each rep how exposed they are.
6. Targets convert to **USD** and roll up the org so Sales reconciles with the FP&A P&L Revenue.

---

## Which `_common` lists it reuses

| Shared structure | From | Used as |
| --- | --- | --- |
| **Time** + `SYS01 Time Settings` | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | monthly target / pipeline phasing; `Is Actual?` for attainment-to-date |
| **Versions** | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | Budget (quota) vs Forecast (latest call) |
| **L3 Cost Centre/Entity** + `SYS02 Organization Details` | [`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md) | each rep's home cost centre → Country/Region roll-up |
| **Currency** + `SYS04 Exchange Rates` | [`_common/common-lists.md`](../_common/common-lists.md) | local targets → USD |
| **L2 Product** | [`_common/common-lists.md`](../_common/common-lists.md) | the product axis of targets & pipeline |
| **L3 P&L Account** | [`_common/common-lists.md`](../_common/common-lists.md) | `Target $` feeds the `Product Revenue` line |

Domain-specific lists (Sales Rep, Territory, Opportunity, Sales Stage) live in [`lists.md`](lists.md).

---

## Architecture sketch (data flow)

```
  Inputs               System                Data            Calculations         Outputs
  ------               ------                ----            ------------         -------
  INP01 Top-Down ┐     SYS01 Time     ┐
  Target          │    SYS02 Org       │     DAT01
  INP02 Rep        ├──► SYS10 Rep       ├──►  Pipeline ──►  CAL01 Quota      ┐
  Weight          │    Details          │    (numbered)    Allocation        ├─► OUT01 Rep
                  ┘    SYS04 FX         ┘                   CAL02 Weighted    │   Scorecard
                       SYS11 Stage Prob                     Pipeline          │
                                                            CAL03 Coverage    ┘
                                                            CAL04 Target USD ──► (feeds FP&A Revenue)
```

- One direction: Inputs/Data + System → Calculations → Outputs. *(Logical)*
- The numbered **Opportunity** list keeps the large, churning pipeline out of the planning grids.
  *(Performance)*

### Hand-off to FP&A (model-to-model import)

Sales and FP&A are **separate models**, so the hand-off is a scheduled **model-to-model import**, not a
live cross-model formula. The source is this model's `CAL04 Target in USD.Target (USD)` aggregated to the
finance grain **L3 Cost Centre × L2 Product × Time × Versions**; the target is FP&A's
`CAL03 Currency Conversion.Revenue (USD)` at the **same grain**.

**Import mapping (Sales → FP&A):**

| Sales source (this model) | FP&A target | Match on |
| --- | --- | --- |
| `CAL04 Target in USD.Target (USD)` `[SUM: SYS10 Rep Details.Cost Centre]` by Product, Time, Version | a `Revenue (USD) — Sales target` reconciliation line read alongside `CAL03 Currency Conversion.Revenue (USD)` | `L3 Cost Centre/Entity` (shared) · `L2 Product` (shared) · `Time` (shared) · `Versions` (shared) |

Because both models dimension on the **shared `_common` lists**, the four dimensions line up member-for-member
— no remapping. Sales is the *bottom-up* revenue view; FP&A's `CAL03.Revenue (USD)` is the *driver-based*
(volume × price) view. They will not be bit-identical — the gap is a planning conversation, not a model error.
See [fpa-pl-planning/formulas.md](../fpa-pl-planning/formulas.md).

---

**Related:** [`lists.md`](lists.md) · [`modules.md`](modules.md) · [`formulas.md`](formulas.md) ·
[`_common` backbone](../_common/README.md) · [FP&A blueprint](../fpa-pl-planning/README.md) ·
[DISCO](../../docs/03-methodology/disco.md)
