# Academy & Community Best Practices

> **Level:** L2 · **Area:** Methodology · Field-tested advice from Anaplan's training and practitioner community.

[PLANS](plans-standard.md), [DISCO](disco.md) and [The Planual](planual.md) give you the *rules*.
The **Anaplan Academy** (official training) and the **Anaplan Community** (practitioner forums,
best-practice articles, the Center of Excellence) are where you pick up the *habits* and learn to
apply those rules. This page is the habit-and-where-to-learn layer — it points at the standards
rather than restating them.

## The rules already covered elsewhere

The day-to-day construction rules an Academy course or Community thread will drill into you are the
ones this kit already documents in full. Rather than repeat them, treat these as the canonical pages:

- **Structure and data flow (D→I→S→C→O), System modules, naming** → [DISCO](disco.md) and
  [`templates/naming-conventions.md`](../../templates/naming-conventions.md).
- **A single Data Hub feeding spokes** → [`docs/04-integration/`](../04-integration/).
- **Stepped line items, Booleans over `IF`, map don't `SELECT`, calculate once at the right level**
  → [The Planual](planual.md) and the [model-build checklist](model-build-checklist.md).
- **Cell count, Time Ranges, subsets, avoiding text/`IF` on huge modules** →
  [PLANS — Performance](plans-standard.md#p--performance) and [`docs/07-performance/`](../07-performance/).

## The habits training and community actually add

These are the working habits the standards assume but don't spell out:

- **Design before you build.** Sketch the modules and the data flow on paper first.
  Re-architecting a live model is far more expensive than a whiteboard rethink.
- **Build to the user story, not beyond it.** Necessary (the N in PLANS) applies to *features* too,
  not just cells.
- **Demo early and often** (The Anaplan Way) — feedback on a working module beats a perfect spec.
- **Use ALM from the start** for anything heading to production: build in DEV, promote to PROD via
  revisions. *(See [`docs/06-security-alm/alm.md`](../06-security-alm/alm.md).)*
- **Document assumptions** in the model (a notes module or line-item descriptions), so the next
  builder — often future-you — understands intent.

## Where to keep learning

- **Anapedia** — the reference docs: https://help.anaplan.com/
- **Anaplan Community** — best-practice articles, the model-builder forums, and the Planual:
  https://community.anaplan.com/
- **Anaplan Academy** — the official Level 1/2/3 courses behind [`LEARNING-PATH.md`](../../LEARNING-PATH.md).

**Related:** [PLANS](plans-standard.md) · [DISCO](disco.md) · [The Planual](planual.md) · [model-build-checklist.md](model-build-checklist.md)

> Source: Anaplan Academy & Anaplan Community best-practice materials. See [`SOURCES.md`](../../SOURCES.md).
