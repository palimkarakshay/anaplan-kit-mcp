# Common Errors and Fixes

> **Level:** L2 · **Area:** Troubleshooting · **PLANS:** all five

The errors a new builder actually hits, as a quick **symptom → likely cause → fix** reference.
Almost every one of these is a PLANS principle reasserting itself. The fix is rarely a trick — it's
bringing the build back in line with the standard.

| Symptom | Likely cause | Fix | PLANS |
| --- | --- | --- | --- |
| "Circular reference" — formula won't save | Line item depends on itself, directly or through a chain | Break the loop with `PREVIOUS`, stepped line items, or a one-way data flow (below) | Logical |
| "Formula too complex" / blocking error | One giant nested formula; too many terms/`IF`s | Split into stepped line items; use `LOOKUP`/Boolean instead of long `IF` chains | Auditable, Performance |
| Format-mismatch error | Formula returns a different format than the line item (e.g. Number into Text) | Make formats agree; convert explicitly (`TEXT()`, `VALUE()`) | Logical |
| "Item not found" / `SELECT` breaks | Hard-coded list item that was renamed or removed | Replace `SELECT` with a System-module mapping | Sustainable |
| Import maps nothing / drops rows | Mapping mismatch, code-vs-name, wrong delimiter | Map on **codes**, fix the source, check the import log | Sustainable |
| Page/dashboard opens slowly | Too many objects, large unfiltered grids, on-the-fly calcs in the view | Pre-calculate in a module; trim grids; fewer cards | Performance |
| Module is enormous / model bloated | Over-dimensionalised — dimensioned by lists it doesn't need | Remove unneeded dimensions; apply Time Ranges/subsets | Performance, Necessary |

The rest of the page is the *why* and the *how* for each.

---

## <a name="circular-reference"></a>Circular reference errors

**What it means.** Anaplan recalculates the whole model in dependency order, so it refuses any
formula where a line item depends on itself — directly (`A = A + 1`) or through a chain
(`A → B → C → A`). It will not save a model with a circular dependency.

**Why it happens.** Most often a *running balance* or *rolling* calculation: "this period =
previous period + this period's movement", written so the engine thinks the cell references
itself. Or a genuine logic loop where two modules feed each other.

**How to fix — the stepped / offset approach.** Reference the **prior period**, not the current
cell, so the dependency points one step back in time and never loops:

```
// Running balance — closing this period = opening + movement
Opening Balance = PREVIOUS('Closing Balance')
Closing Balance = Opening Balance + Movement
```

`PREVIOUS` is the simplest tool and never creates a circular reference. When you need a variable
offset, use `LAG(..., n, ...)` with the **`STRICT`** keyword — it tells the engine you will never
refer to the current cell, guaranteeing no loop. For a module-to-module loop, the real fix is to
restore **one-directional data flow** (Inputs → System → Calculations → Outputs): split the
shared logic into a separate stepped line item so the chain goes forward, not in a circle.

> *(Logical — one-way flow; Auditable — stepped line items.)* See
> [PLANS — Logical](../03-methodology/plans-standard.md#l--logical).

---

## "Formula too complex" / blocking errors

**What it means.** Anaplan blocks (won't save) a formula it can't evaluate efficiently — typically
one with too many terms, deeply nested `IF`s, or too many function combinations in a single line
item.

**Why it happens.** The beginner instinct is to write the whole calculation as one heroic nested
formula. The engine has to process the whole thing on every recalc, and you can't audit it.

**How to fix.**

- **Break it into stepped line items**, one logical step each. This is faster to recalc *and*
  readable. If you can't explain a formula in one sentence, it's too long.
- Replace long `IF…THEN…ELSE` chains with a **`LOOKUP`** against a mapping module. Rule of thumb:
  more than ~10 conditions → use a `LOOKUP`, not `IF`.
- Put the **most common condition first** in any `IF`.
- Prefer a **Boolean line item** to a text `IF` flag.

> *(Auditable + Performance — Planual: "break complex formulas into stepped line items".)*

---

## Format-mismatch errors

**What it means.** The formula's result type doesn't match the line item's **Format** (Number,
Text, Boolean, Date, Time Period, List), or you're comparing two incompatible formats.

**Why it happens.** Easy to do: dividing to get a ratio in a Number line item that's set to
Boolean; concatenating text into a Number line item; comparing a Date line item to a number.

**How to fix.** Open the Blueprint, set the line item's **Format** to match what the formula
returns, and convert explicitly where needed: `TEXT(number)`, `VALUE(text)`, `DATE(...)`. Decide
the format *before* you write the formula — it's part of designing the line item.

> *(Logical — the format must mirror the meaning.)* See
> [line items & formats](../01-fundamentals/line-items-and-formats.md).

---

## "Item not found" / `SELECT` breaks when the list changes

**What it means.** A formula uses `SELECT: List.SpecificItem`, and that item was renamed, deleted,
or never existed — so the formula errors or silently returns blank.

**Why it happens.** Hard-coding a list member into a formula. The moment the list changes (and
lists *always* change), the formula breaks. This is one of the most common Sustainable violations.

**How to fix.** Never `SELECT` a specific item. Drive the choice from a **System module** mapping
or a Boolean flag, so the formula keeps working when members come and go:

```
// Instead of:  Revenue = SELECT: Products.Widget -> Sales
// Map it in a System module and use:
Revenue = Sales[LOOKUP: SYS Product Mapping.Target Product]
```

> *(Sustainable — Planual: "avoid `SELECT` on specific items; map instead".)*

---

## Import mapping failures

**What it means.** An import runs but maps zero rows, drops rows, or creates duplicate/blank
members instead of updating existing ones.

**Why it happens.** Common culprits: mapping on **names** instead of **codes**; a header/column
mismatch; wrong delimiter or encoding; the target list isn't a production list; or the source has
trailing spaces/case differences.

**How to fix.**

- Map on **codes**, not display names — codes are stable, names change.
- Read the **import log / dump file** — it lists exactly which rows failed and why.
- Confirm the source column formats match the target line-item formats.
- Reconcile **row counts** afterward (source rows in vs target rows updated). See
  [reconciliation-and-control-totals.md](reconciliation-and-control-totals.md).

> *(Sustainable, Logical.)* See [imports & exports](../04-integration/imports-exports.md).

---

## Slow-opening dashboards / pages

**What it means.** A page or worksheet takes many seconds to open or refresh.

**Why it happens.** Too many cards/objects on one page; large grids showing every list member
unfiltered; calculations happening *in the view* rather than pre-computed; charts over huge ranges.

**How to fix.**

- **Pre-calculate** what the page shows in a dedicated Output module — don't make the page do math.
- Trim grids with filters, subsets and **Time Ranges** so they render a slice, not the universe.
- Fewer objects per page; split a heavy dashboard into focused ones.

> *(Performance.)* See [Performance](../07-performance/).

---

## Accidentally huge modules (over-dimensionalised)

**What it means.** A single module is tens or hundreds of millions of cells and dominates model
size, slowing recalc and opening.

**Why it happens.** The module is dimensioned by a list (or Version, or full Time) it doesn't truly
need. Cell count = product of all dimension sizes × line items, so each extra dimension
*multiplies* the total.

**How to fix.**

- Remove any dimension the module doesn't actually use. **Removing a dimension is the biggest win.**
- Apply a **Time Range** so it covers only the periods it needs.
- Use **subsets** so it spans only the relevant members.
- Move rarely-used line items to their own smaller module.

> *(Performance, Necessary.)* See
> [model-size-and-workspace-management.md](model-size-and-workspace-management.md) and
> [Performance](../07-performance/).

---

**Related:** [README](README.md) ·
[reconciliation-and-control-totals.md](reconciliation-and-control-totals.md) ·
[model-size-and-workspace-management.md](model-size-and-workspace-management.md) ·
[PLANS](../03-methodology/plans-standard.md) · [The Planual](../03-methodology/planual.md)
