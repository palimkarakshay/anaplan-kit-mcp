# Platform-Aware Decisions

> **Level:** L2–L3 · **Area:** Field Guide · **PLANS:** Performance, Sustainable

The Anaplan platform has moving parts — multiple engines, multiple APIs, two UX generations, hard
size limits, scattered docs. You can't change any of that. But each one **changes a decision you or
your team actually make**, and that decision *is* in your scope. This page is only those decisions —
no vendor-roadmap or market commentary you can't act on.

---

## Which calculation engine? (Classic vs Polaris)

**Fact you can't change:** a workspace is provisioned as **Classic** *or* **Polaris**, and **cannot
be converted** afterwards. Classic stores data **densely** (every cell costs memory, empty or not);
Polaris is **natively sparse** (well-suited to sparse data). ([Anaplan calculation engines](https://help.anaplan.com/anaplan-calculation-engines-06c06ade-2807-4f3d-9a6e-d69ae0e257e5), [Polaris engine](https://help.anaplan.com/polaris-calculation-engine-8b466778-42b2-4e35-b318-e5e4128b63b7), [sparsity & density](https://help.anaplan.com/understand-sparsity-and-density-616ee341-8a5f-4718-8c90-c82e34eca86c))

**The decision you own:**

- **Find out which engine your workspace uses** before you design. It changes how hard you fight cell count.
- On **Classic**, sparsity is your enemy — the [anti-patterns](anti-patterns-catalog.md) about
  dimensionality, boolean-as-dimension, and right-sized formats matter *enormously*.
- On **Polaris**, the sparse design is forgiven somewhat — but good dimensionality discipline is still
  correct, not optional.
- **At project kickoff, ask which engine and why** — a sparse, high-dimensional model may be a strong
  Polaris case. This is a legitimate architecture question to raise; raise it early, because there's
  no in-place switch later.

## Which integration tool / API?

**Fact you can't change:** several integration generations coexist — **Anaplan Connect** (CLI),
**CloudWorks** (managed scheduling/connections), the **REST API v2 (Bulk)**, and the
**Transactional API**. (See [integration](../04-integration/) and [REST API](../04-integration/rest-api.md).)

**The decision you own:**

- **Pick per use case, not per habit:** bulk data loads → Bulk/Connect/CloudWorks; small real-time
  reads/writes → Transactional API; scheduled chained flows → CloudWorks.
- **Don't pin to the oldest API just because it works.** Document *which* API each integration uses,
  so the team isn't surprised when one is deprecated.
- **One named owner per integration** (see [engineering discipline](engineering-discipline.md) → security hygiene).

## Which UX?

**Fact you can't change:** the **New UX (Pages/Boards/Worksheets)** and **Classic dashboards** both
exist; many tenants still run Classic in production.

**The decision you own:** **build new work in the New UX.** Don't add to the Classic estate. If you
inherit Classic dashboards, flag the dual-maintenance cost to whoever owns the roadmap — and design
new pages as tools, not printouts ([app design](../05-ux/app-design-principles.md)).

## How big can the model get?

**Fact you can't change:** workspace size (GB) is a hard, licensed constraint; cell count is what
drives it.

**The decision you own — this is mostly *control*:**

- Reduce size through **good modeling**, not fidelity-destroying hacks: right-sized dimensionality,
  [Time Ranges](../07-performance/time-ranges.md), [subsets](../07-performance/line-item-subsets.md),
  tight formats, archive strategies for unbounded lists.
- When a real business requirement genuinely needs more size, **make the trade-off explicit** to the
  owner (more dimension = more cells = more cost) rather than silently flattening the model into
  something unmaintainable. Surfacing the trade-off is the *influence* you have.
- Monitor size routinely with the [Calculation Effort column / Model Open Analysis](../09-troubleshooting/model-size-and-workspace-management.md).

## Where to find answers (the documentation map)

**Fact you can't change:** docs are spread across properties with uneven cross-linking and weak search.

**The decision you own — your daily research habit:**

| Source | Best for |
| --- | --- |
| **Anapedia** (help.anaplan.com) | Canonical reference: function syntax, feature behaviour, limits. Start here. |
| **Anaplan Community** (community.anaplan.com) | Real-world problems; often more current than Anapedia for new features. The **OEG (Operational Excellence Group) Best Practice** articles are high-signal. |
| **Anaplan Academy / Learning Center** | Structured L1/L2/L3 training (the [learning path](../../LEARNING-PATH.md)). |
| **Master Anaplanner blogs** | Often the highest signal-to-noise for hard problems — but not vendor-maintained; verify against Anapedia. |

Practical habit: **confirm syntax in Anapedia, find patterns in Community/OEG, verify currency** —
because pages get renamed and links rot. (This kit's own function pages cite their Anapedia source for exactly this reason — see [`SOURCES.md`](../../SOURCES.md).)

## Protect your own effectiveness (individual scope)

A few habits that are *actionable for you*:

- **Document your logic** so it isn't trapped as tribal knowledge — it keeps the model maintainable.
- **Keep the transferable concepts sharp** — dimensional modeling, data-flow design, reconciliation,
  performance reasoning. These outlast any one platform feature or rebrand.
- **Think like an engineer even though the toolchain doesn't.** Models built with
  [PLANS](../03-methodology/plans-standard.md) and the [engineering disciplines](engineering-discipline.md)
  survive the next reorg and the next builder who inherits them.

---

**Related:** [anti-patterns catalog](anti-patterns-catalog.md) · [engineering discipline](engineering-discipline.md) · [performance](../07-performance/) · [model size & workspace management](../09-troubleshooting/model-size-and-workspace-management.md) · [ALM](../06-security-alm/alm.md)

> Sources: Anaplan calculation-engine, sparsity, ALM and integration docs (Anapedia) plus Anaplan Community OEG best practices. See [`SOURCES.md`](../../SOURCES.md).
