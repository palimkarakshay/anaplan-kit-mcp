# 00 · Getting Started

> **Level:** L1 · **Area:** Getting Started · This is your orientation before anything else.

New to Anaplan? Start here. This section gets you from "I've never seen the platform" to "I know
what the pieces are called and where I sit." It's deliberately light on building — the
[fundamentals](../01-fundamentals/) section is where you start designing modules.

| Page | What it covers |
| --- | --- |
| [platform-architecture.md](platform-architecture.md) | Tenant → workspace → model, the in-memory calc engine, and who does what (model builder vs admin). |
| [glossary.md](glossary.md) | A–Z plain-English definitions of every core term, each linked to the page that covers it in depth. |

---

## Anaplan in 10 minutes

**What it is.** Anaplan is a cloud **connected-planning** platform. You build a business model — a
budget, a forecast, a headcount plan, a supply plan — entirely in a web browser. There is nothing
to install, no code to compile, and no "run" button: you change a structure or a formula and the
whole model **recalculates instantly, in memory**.

**The mental model.** Everything is built from a few pieces:

| Piece | Plain meaning | In a spreadsheet, this would be… |
| --- | --- | --- |
| **List** | The things you plan *by* — products, cost centres, months, countries. | The row/column labels you'd repeat on every tab. |
| **Module** | A multi-dimensional grid of numbers and calculations. | A worksheet — but built once and shared across every combination. |
| **Line item** | A single measure or calculation inside a module (`Revenue`, `Growth %`). | A row/formula in that worksheet. |
| **Formula** | The logic on a line item, e.g. `Volume * Price`. | A cell formula — but written once, applied to the whole grid. |
| **Dimension** | A list (or Time, or Versions) that a module is sized by. | The "for every product, for every month" repetition. |

Modules connect to each other through formulas, so a change in one assumption ripples through the
entire plan in real time. That's "connected planning."

**Why people switch to it.** A spreadsheet falls apart at scale — broken links, no audit trail,
one editor at a time, formulas copied a thousand times. Anaplan keeps a single, governed model that
many people edit at once, recalculates the moment anything changes, and lets you trace any number
back to its source.

**The one big rule.** A spreadsheet lets you put any formula in any cell. Anaplan does **not**: a
line item has **one** formula that applies to its whole grid. This feels restrictive at first and is
actually the platform's superpower — it's what makes models fast and auditable. Most of learning
Anaplan is learning to think in whole grids, not individual cells.

---

## How the levels map

This kit follows Anaplan's official **Level 1 → Level 2 → Level 3** model-building progression. Every
page carries a `Level:` badge so you always know where it sits.

| Level | You're learning to… | Lives mostly in |
| --- | --- | --- |
| **L1 — Foundations** | Build a small, correct model: lists, modules, line items, formats, basic formulas. | This section + [01-fundamentals](../01-fundamentals/) |
| **L2 — Real builds** | Build the *sanctioned* way: DISCO structure, numbered lists, subsets, time ranges, data hubs. | [03-methodology](../03-methodology/), [04-integration](../04-integration/) |
| **L3 — Architecture** | Build at scale: performance, ALM, multi-model architecture, advanced patterns. | [07-performance](../07-performance/), [06-security-alm](../06-security-alm/) |

For the full topic-by-topic reading order, see [`../../LEARNING-PATH.md`](../../LEARNING-PATH.md).

---

## Where to go next

1. Read [platform-architecture.md](platform-architecture.md) so the words "tenant", "workspace" and
   "model" mean something.
2. Skim [glossary.md](glossary.md) — don't memorise it, just know it's there.
3. Move into [01-fundamentals](../01-fundamentals/) and start designing.

**Related:** [Learning path](../../LEARNING-PATH.md) · [Fundamentals](../01-fundamentals/) ·
[Methodology](../03-methodology/)
