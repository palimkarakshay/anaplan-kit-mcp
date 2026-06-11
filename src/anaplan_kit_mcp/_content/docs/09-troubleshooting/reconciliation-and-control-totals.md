# Reconciliation & Control Totals

> **Level:** L2 · **Area:** Troubleshooting · **PLANS:** Auditable, Sustainable · **DISCO:** Calculations

The habit that separates a trusted builder from a hopeful one is **proving the numbers tie out** —
not assuming they do. A model can calculate, save, and look fine while quietly being wrong (a
dropped import row, a mis-set summary, a sign flip). The defence is cheap and permanent: a small
**check / control-total module** that compares *calculated* against *source*, and flips a Boolean
red when they disagree.

This is pure **Auditable**: anyone can glance at one cell and know whether to trust the model
today. And it's **Sustainable**: the check keeps watching every period, every load, with no manual
effort.

---

## The core pattern: a "control total" check module

The idea is always the same three pieces:

1. A **source total** you trust (a number from the GL, the extract, a known-good figure).
2. The **model's own total** of the same thing, calculated independently.
3. A **variance** and a Boolean **"Out of balance?"** that flags any difference.

Put it in its own tiny **System/Calculation** module so it's visible, not buried inside a calc.

**`CHK01 Control Totals`** — a reconciliation module (often one cell per metric, or dimensioned by
the lowest level you reconcile at, e.g. Entity):

| Line Item | Format | Summary | Formula |
| --- | --- | --- | --- |
| Source Total | Number | Sum | *(imported from GL/extract, or hard total of source)* |
| Model Total | Number | Sum | `CAL30 P&L.Net Revenue[SUM: ...]` |
| Variance | Number | Sum | `Model Total - Source Total` |
| Variance % | Number | None | `IF Source Total = 0 THEN 0 ELSE Variance / Source Total` |
| Within Tolerance? | Boolean | None | `ABS(Variance) <= Tolerance` |
| **Out of Balance?** | Boolean | None | `NOT Within Tolerance?` |
| Tolerance | Number | None | *(input, e.g. `0.01` for rounding noise)* |

> **Why a tolerance, not `=`?** Floating-point and rounding mean two "equal" totals can differ by
> a fraction of a cent. Compare with `ABS(Variance) <= Tolerance` (or `ROUND(...,2)` on both
> sides), never raw `=` on calculated money. *(Auditable.)*

Surface **Out of Balance?** on an admin board with conditional formatting (red/green). A red cell
is your signal to investigate *before* a user finds the wrong number.

---

## Reconciling import row counts

An import can report "success" while silently **ignoring** thousands of unmatched rows (a missing
list member or period). The count never errors — it just doesn't load. Catch it with the
**rows-balance equation**:

```
// CHK02 Load Control -> Reconciled?
Rows in Source = Rows Loaded + Rows Ignored + Rows Failed
```

| Line Item | Format | Summary | Formula |
| --- | --- | --- | --- |
| Rows in Source | Number | None | *(extract row count)* |
| Rows Loaded | Number | None | *(from import result)* |
| Rows Ignored | Number | None | *(from import result)* |
| Rows Failed | Number | None | *(from import result)* |
| Reconciled? | Boolean | None | `Rows in Source = Rows Loaded + Rows Ignored + Rows Failed` |
| Clean Load? | Boolean | None | `Reconciled? AND Rows Ignored = 0 AND Rows Failed = 0` |

> **Count *and* value.** Two offsetting wrong rows can net to a right count. Always reconcile the
> **value** as well (`Model Total = Source Total`), not just the row count.

See [common-errors-and-fixes.md — import mapping failures](common-errors-and-fixes.md#import-mapping-failures)
and [handle import errors & dump files](../../cookbook/data-and-imports/handle-import-errors-and-dump-files.md).

---

## Tying model output back to the GL / source

Month-end reconciliation against the General Ledger is the classic real-world demand. The pattern
scales the control-total idea to a dimension (usually **Account** or **Entity × Account**):

```
// CHK03 GL Reconciliation -> Out of Balance?
ABS( OUT10 Reported P&L.Amount - DAT01 GL Actuals.Amount ) > Tolerance
```

Build it so a single Boolean at the **Total** level answers "does the whole P&L tie?", and the
detail rows let you drill straight to the account that doesn't. A reviewer should be able to:

1. Look at the **top-level Out of Balance?** — green means done.
2. If red, **sort the detail by ABS(Variance)** to find the offending account in seconds.

That two-step drill is the whole point: the check doesn't just say *something's* wrong, it points
at *what*.

---

## When the check goes red — how to read it

| Variance pattern | Likely cause | Where to look |
| --- | --- | --- |
| Off by a round, large amount | A whole entity/account didn't load (ignored rows) | Import dump file; missing list member |
| Off by a small fraction | Rounding / floating point — not a real error | Widen tolerance or `ROUND` both sides |
| Sign is reversed | Debit/credit or import sign convention | Check the import's sign handling / a `* -1` |
| Doubled | Import ran twice, or double-counted in a `SUM` mapping | Check process run log; check mapping dimensionality |
| Drifts over time | A hard-coded date or a too-tight Time Range | Search formulas for hard-coded periods *(Sustainable)* |

---

## Good practice

- **Build the check first, alongside the calc** — not as an afterthought when numbers are
  questioned. *(Auditable.)*
- Keep control modules **tiny and named clearly** (`CHK*`). They cost almost nothing in cell
  count and earn their keep on day one.
- Make the import process **write its result statistics back** into the load-control module (via
  the API / Anaplan Connect) so the check is hands-off. *(Sustainable.)*
- A red **Out of Balance?** should **block the downstream publish** to spoke models, not just warn.
- Reconcile **both count and value**, and **both totals and a meaningful breakdown**.

**Related:** [common-errors-and-fixes.md](common-errors-and-fixes.md) ·
[testing-and-uat.md](testing-and-uat.md) ·
[Reconciliation check module recipe](../../cookbook/performance/reconciliation-check-module.md) ·
[Handle import errors & dump files](../../cookbook/data-and-imports/handle-import-errors-and-dump-files.md) ·
[PLANS — Auditable](../03-methodology/plans-standard.md#a--auditable) ·
[The Planual](../03-methodology/planual.md)

> Source: Anaplan best-practice (control totals / reconciliation) — `help.anaplan.com` & Anaplan
> Community. See [`SOURCES.md`](../../SOURCES.md).
