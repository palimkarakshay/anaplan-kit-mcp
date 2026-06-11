# Sales Planning — Key Formulas

> **Level:** L2 · **Area:** Blueprint (Sales) · **DISCO:** Calculations

How a top-down target becomes per-rep quotas, how a numbered pipeline becomes coverage, and how the
result reconciles with FP&A. One line item per step. *(Auditable)*

---

## 1. Top-down → bottom-up: quota allocation

Split each Territory × Product target across its reps in proportion to their weight.

First, the denominator — total weight in the territory (`CAL01.Territory Weight Total`):

```
INP02 Rep Allocation Weight.Weight[SUM: SYS10 Rep Details.Territory]
```

Then the rep quota (`CAL01.Quota (local)`):

```
IF SYS10 Rep Details.Is Active?
   THEN INP01 Top-Down Target.Target (local)[LOOKUP: SYS10 Rep Details.Territory]
        * INP02 Rep Allocation Weight.Weight
        / Territory Weight Total[LOOKUP: SYS10 Rep Details.Territory]
   ELSE 0
```

- `LOOKUP: SYS10.Territory` brings the territory target onto each rep.
- Dividing by `Territory Weight Total` **normalises** the weights, so quotas always sum back to the
  territory target — no leakage. *(Logical, Auditable)*
- The `Is Active?` guard keeps inactive reps at zero without deleting them. *(Sustainable)*

---

## 2. Numbered pipeline → weighted value

Weight each deal by its stage's win probability (`CAL02.Weighted Value (local) per deal`):

```
DAT01 Pipeline Load.Deal Value (local)
  * SYS11 Stage Probability.Win Probability[LOOKUP: DAT01 Pipeline Load.Stage]
```

Then collapse the (large) Opportunity list onto the planning grid with `SUM`
(`CAL02.Weighted Pipeline (local)`):

```
Weighted Value (local) per deal[
   SUM: DAT01 Pipeline Load.Owner (Rep),
   SUM: DAT01 Pipeline Load.Product,
   SUM: DAT01 Pipeline Load.Close Month ]
```

> This is the key performance move: the heavy transactional list (`Opportunity`) is aggregated into
> the small `Rep × Product × Time` grid in **one** calc, so downstream modules stay tiny.
> *(Performance — see [`docs/07-performance/`](../../docs/07-performance/).)*

---

## 3. Coverage and gap

```
Coverage Ratio = IF Quota (local) = 0 THEN 0
                 ELSE Weighted Pipeline (local) / Quota (local)
Gap to Quota   = Quota (local) - Weighted Pipeline (local)
```

`Coverage Ratio < 1` ⇒ the rep's weighted pipeline doesn't cover quota → flag `At Risk?` in
`OUT01`. Guard the divide-by-zero. *(Auditable)*

---

## 4. Currency conversion (nested LOOKUP)

A rep has no currency directly — it inherits its Cost Centre's. Chain the lookups (`CAL04.FX Rate`):

```
SYS04 Exchange Rates.Rate (filled)[
   LOOKUP: SYS02 Organization Details.Local Currency[
      LOOKUP: SYS10 Rep Details.Cost Centre ] ]
```

- Inner `LOOKUP` : rep → its Cost Centre's `Local Currency`.
- Outer `LOOKUP` : that currency → its FX rate.

Then `Target (USD) = Quota (local) * FX Rate`. Same shared FX module as FP&A and Workforce, so the
rate is identical across domains. *(Sustainable, Logical)*

---

## 5. Reconciliation hand-off to FP&A (model-to-model import)

Sales and FP&A are **separate models**. Summing `CAL04.Target (USD)` up to the finance grain gives a
revenue number on the same grain as FP&A's `CAL03 Currency Conversion.Revenue (USD)`:

```
Sales Target (USD)  [SUM: SYS10 Rep Details.Cost Centre]  by L2 Product, Time, Version
   ≈  FP&A CAL03 Currency Conversion.Revenue (USD)  by L3 Cost Centre, L2 Product, Time, Version
```

**The mechanism is a scheduled model-to-model import** (not a live cross-model formula):

| Sales source line item | FP&A target line item | Mapping (matched on shared `_common` lists) |
| --- | --- | --- |
| `CAL04 Target in USD.Target (USD)` aggregated `[SUM: SYS10 Rep Details.Cost Centre]` | the `Revenue (USD) — Sales target` reconciliation line in FP&A's `OUT02`-side check (read against `CAL03.Revenue (USD)`) | `L3 Cost Centre/Entity` → `L3 Cost Centre/Entity`; `L2 Product` → `L2 Product`; `Time` → `Time`; `Versions` → `Versions` |

The two won't be bit-identical (one is bottom-up quota, the other is volume × price), but they
**must reconcile** — the gap is a planning conversation, not a model error. The `Target (USD)`
reconciles against the `Product Revenue` branch of the P&L in [FP&A](../fpa-pl-planning/formulas.md).

---

## Consistency check

```
INP01 Top-Down Target ─► CAL01 Quota Allocation ─► CAL04 Target (USD) ─► OUT01 / FP&A Revenue
DAT01 Pipeline ────────► CAL02 Weighted Pipeline ─► CAL03 Coverage ───► OUT01 At Risk?
```

Every output traces back to either a typed target or a loaded deal.

---

**Related:** [`modules.md`](modules.md) · [`README.md`](README.md) ·
[FP&A formulas](../fpa-pl-planning/formulas.md) ·
[`_common/common-lists.md`](../_common/common-lists.md) (FX) ·
[Formula reference](../../docs/02-formulas/)
