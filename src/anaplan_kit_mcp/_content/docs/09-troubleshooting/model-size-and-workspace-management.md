# Model Size & Workspace Management

> **Level:** L2 · **Area:** Troubleshooting · **PLANS:** Performance, Necessary

Anaplan holds your whole model **in memory**, so size isn't a billing detail — it's the thing that
decides whether the model opens in two seconds or thirty, calculates instantly or crawls. Running
out of **workspace** is one of the most common walls a growing model hits. This page is how size
works, what drives it, how to find and shrink the culprits, and why managing size is never "done".

It is **Performance** and **Necessary** made concrete: the smallest model that meets the
requirement is the best model.

---

## Workspace vs model size

- A **workspace** is a memory allocation (in **GB**) that holds one or more models.
- A **model** has its own size; the **workspace size used = the sum of all non-archived models**
  in it.
- **Archived** models do **not** count toward the workspace size (more below).

Anaplan workspaces come in tiers — a standard workspace allocation has an upper bound, and larger
**HyperModel** workspaces go considerably higher. At the time of writing the commonly cited limits
are roughly **130 GB for standard** workspaces and up to **~720 GB for HyperModel**, with the
allocation changed only by Anaplan Support. **Confirm current limits in Anapedia** — they change.

> As an admin you watch the **workspace usage** indicator. When a workspace approaches its
> allocation, you either **shrink models** (preferred) or request more space (costs money and only
> defers the problem). Shrinking is the model builder's job.

---

## What actually drives size: cell count

Model size is overwhelmingly **cell count**, not formulas or formatting. Cell count is the product
of a module's dimension sizes × its line items — every dimension *multiplies*, every line item
*adds*, so a few dimensions reach tens of millions of cells fast (see the formula and the worked
72M-cell example in [sparsity & cell count](../07-performance/sparsity-and-engine.md)).

> The biggest size win is almost always **removing a dimension or a line item you didn't need** —
> not optimising a formula. Necessity *is* performance.

---

## Finding the big modules

Don't guess — Anaplan tells you:

1. Open **Settings → Models** (or the **model's General Info / size** view) to see overall size.
2. Use the **module/grid size** indicators in the model to find which modules dominate.
3. For admins, the **performance / model size diagnostics** rank the heaviest modules.

Sort by size and attack the top of the list — a handful of modules usually account for most of the
model. The rest aren't worth your time.

---

## How to shrink a big module

Work down this list — the items near the top give the biggest cuts:

| Lever | What it does | See |
| --- | --- | --- |
| **Remove an unneeded dimension** | Divides cell count by that dimension's size — the biggest single win | [common errors — over-dimensionalised](common-errors-and-fixes.md#accidentally-huge-modules-over-dimensionalised) |
| **Apply a Time Range** | Module spans only the periods it needs, not the whole calendar | [time-ranges.md](../07-performance/time-ranges.md) |
| **Use subsets** | Dimension by a *portion* of a big list, not all of it | [line-item-subsets.md](../07-performance/line-item-subsets.md) |
| **Fewer line items** | Remove dead/experimental items; merge steps that don't need separating | [PLANS — Necessary](../03-methodology/plans-standard.md#n--necessary) |
| **Numbered lists** | A numbered list with properties is leaner than a deep named hierarchy for transactional/combination data | [numbered lists](../01-fundamentals/numbered-lists-and-subsets.md) |
| **Split odd-dimensioned line items out** | Removes hidden **subsidiary views** that bloat a module | [optimization checklist §7](../07-performance/optimization-checklist.md) |

> **Hiding ≠ removing.** Filtering a list or period off a view does **not** shrink the module —
> the cells still exist. Only a Time Range, a subset, or removing a dimension actually reduces
> size. *(Performance.)*

### Numbered lists as a sizing tool

When you'd otherwise dimension by several lists at once (e.g. every Product × Customer × Channel
combination, most of which never occur), a **numbered list** holds only the combinations that
*actually exist*, with the attributes as properties. That can turn a mostly-empty multi-dimension
module into a compact one. *(Performance, Necessary.)*

---

## Model history & archiving

- **Model history** records data changes. You can view the **latest ~1,000 changes** in the
  History dialog and **export the full history** as plain text for audit. History is retained for
  the **lifespan of the model**.
- **Archiving** a model takes it offline and **frees its space in the workspace** — archived
  models don't count toward the allocation, and **archiving does not delete its history**.
- **Copying** a model is the backup pattern before risky changes — note a **copy does *not*
  carry the source model's history**.
- Confirm exact behaviour and limits in **Anapedia** ("Copy and archive models", "View model
  history").

> **Practical use:** archive old period-end snapshots and decommissioned models to reclaim
> workspace instead of paying for more. Take a **copy before a big structural change** so you can
> roll back.

---

## Why size management is an ongoing job

A model is never "sized once". It grows because:

- Lists grow (new products, customers, periods every year).
- Builders add line items and modules over time.
- "Just in case" dimensions creep in during fast delivery.

So size management is a **recurring discipline**, not a one-off:

- **At calendar rollover**, widen forward Time Ranges *and* trim history ranges — and re-check size.
- **In every review**, run the [optimization checklist](../07-performance/optimization-checklist.md)
  and ask "does this need every dimension, line item, and period?"
- **Watch the workspace gauge** and act before you hit the wall, not after.
- **Archive** what's no longer live.

**Related:** [common-errors-and-fixes.md](common-errors-and-fixes.md) ·
[reconciliation-and-control-totals.md](reconciliation-and-control-totals.md) ·
[Performance overview](../07-performance/README.md) ·
[Time Ranges](../07-performance/time-ranges.md) ·
[Line item subsets](../07-performance/line-item-subsets.md) ·
[Optimization checklist](../07-performance/optimization-checklist.md) ·
[PLANS — Performance](../03-methodology/plans-standard.md#p--performance) ·
[ALM](../06-security-alm/alm.md)

> Source: Anaplan workspace/model size & history docs — `help.anaplan.com` & Anaplan Community
> (workspace limits, copy/archive models, view model history). Confirm current GB limits in
> Anapedia. See [`SOURCES.md`](../../SOURCES.md).
