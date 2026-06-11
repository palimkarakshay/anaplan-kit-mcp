# Troubleshooting

> **Level:** L2 · **Area:** Troubleshooting · **PLANS:** Auditable, Logical, Sustainable

Every model builder hits the same walls: a formula won't save, an import drops rows, a page
takes forever to open, or the numbers just don't tie out. This section is the "things go wrong /
how do I prove this is right" knowledge — symptom, cause, fix — that you reach for *while you
build*, not after.

It pairs two habits that separate a junior builder from a trusted one:

1. **Diagnose fast.** Recognise the common errors and know the standard fix for each.
2. **Prove it's right.** Build reconciliation/control checks, test edge cases, and keep the
   model small enough to stay fast — so you *catch* problems before a user does.

Almost every problem here traces back to a broken **PLANS** principle. The fix is usually not a
clever trick; it's bringing the build back in line with the standard (one-way data flow, stepped
line items, no hard-coding, right-sized dimensions).

---

## Pages in this section

| Page | When you need it |
| --- | --- |
| [common-errors-and-fixes.md](common-errors-and-fixes.md) | A formula won't save, an import fails, a page is slow, a module is huge — the errors beginners actually hit, as a symptom/cause/fix reference. |
| [reconciliation-and-control-totals.md](reconciliation-and-control-totals.md) | Proving your numbers tie out: build a check module that flags "out of balance", reconcile import row counts, tie output back to the GL. |
| [testing-and-uat.md](testing-and-uat.md) | How to actually test a build — test data, edge cases, regression, UAT with the business, a Definition of Done. |
| [model-size-and-workspace-management.md](model-size-and-workspace-management.md) | Workspace and model size, what drives it, how to find and shrink bloated modules, and why size is an ongoing job. |

---

## First things to check

When something breaks, walk this list **before** you start rewriting formulas. Most beginner
problems are on it:

1. **Read the actual error text.** Anaplan tells you the line item and often the cause. Don't
   guess — open the Blueprint and look at the line item flagged in red.
2. **Check the formats match.** A formula returning Number into a Text line item (or comparing a
   Date to a Number) is the single most common "why won't this save" cause.
3. **Look for a circular reference.** Does your line item depend on itself, directly or through a
   chain? Anaplan blocks this. See the [circular reference fix](common-errors-and-fixes.md#circular-reference).
4. **Check the data flow direction.** Inputs → System → Calculations → Outputs, one way. A loop in
   the flow is usually the root cause of a circular or "complex" error. *(Logical.)*
5. **Verify the dimensionality.** Is the module dimensioned by exactly the lists it needs — no
   more (bloat, slowness) and no fewer (wrong totals)?
6. **For imports:** check the mapping and the source format. Most "item not found" / dropped-row
   failures are a mapping or a code-vs-name mismatch.
7. **For wrong numbers:** check the **Summary** method on each line item (Sum vs Average vs Formula
   vs None) — a silent mis-set summary is a classic invisible bug.
8. **Ask "did this used to work?"** If a change broke it, diff against the last good state and
   check what you touched (this is where [regression testing](testing-and-uat.md) earns its keep).

> **Golden rule:** if you can't explain a formula in one sentence, it's too long. Break it into
> stepped line items — it gets faster *and* easier to debug. *(Auditable, Performance.)*

**Related:** [PLANS](../03-methodology/plans-standard.md) ·
[The Planual](../03-methodology/planual.md) ·
[Model-Build Checklist](../03-methodology/model-build-checklist.md) ·
[Performance](../07-performance/) · [Cookbook](../../cookbook/README.md)
