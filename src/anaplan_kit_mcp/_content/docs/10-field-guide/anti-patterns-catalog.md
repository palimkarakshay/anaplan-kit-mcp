# Anti-patterns Catalog — Symptom → Fix

> **Level:** L2–L3 · **Area:** Field Guide · **PLANS:** all five · Everything here is in your **control**.

These are the modeling anti-patterns you will see (and be tempted by) in real models. Each entry:
**symptom → why it happens → the fix → where to learn it.** None of these require permission, budget,
or a platform feature — they're entirely your choice at the keyboard.

> How to use this page: when a model "feels wrong," scan the symptoms. When you're reviewing your own
> work (or someone else's), this doubles as a review checklist alongside the
> [model-build checklist](../03-methodology/model-build-checklist.md).

---

## A. Keyboard-level (modeling-in-the-small)

### Line items the size of the universe

- **Symptom:** a line item dimensioned with every list "in case we need it later." Cell count explodes.
- **Why:** future-proofing instinct; not trusting that adding a dimension later is cheap.
- **Fix:** dimension a line item by **only what it needs** (`Applies To` minimal). Cell count = product of dimension sizes × line items — every extra dimension multiplies it. On Classic, empty cells still cost memory.
- **Learn:** [dimensions](../01-fundamentals/dimensions.md) · [sparsity & engine](../07-performance/sparsity-and-engine.md) · PLANS **Performance/Necessary**.

### Boolean-as-dimension

- **Symptom:** `Applies To: Customer × Product × Time × Active-Flag`. The inactive half of the cube still exists.
- **Why:** a filter is modeled as a dimension because the builder doesn't trust filtering.
- **Fix:** make the flag a **Boolean line item**, not a list dimension; filter views/DCA with it.
- **Learn:** [line items & formats](../01-fundamentals/line-items-and-formats.md) · [replace IF with Boolean recipe](../../cookbook/performance/replace-if-with-boolean.md).

### SUM where you needed LOOKUP (and vice-versa)

- **Symptom:** a 4-second calc becomes 40 seconds; the engine materialises an intermediate across a dimension that doesn't belong in the path. The Anaplan version of an N+1 query.
- **Why:** source-vs-target dimensionality confusion — `SUM` aggregates *across* a mapping; `LOOKUP` picks *one* item.
- **Fix:** be deliberate. **`SUM`** when collapsing detail up a mapping; **`LOOKUP`** when reading a single mapped value. Put the mapping in a **System** module.
- **Learn:** [lookup & mapping](../02-formulas/lookup-and-mapping.md) · [sum-lookup-remap recipe](../../cookbook/mapping-and-allocation/sum-lookup-remap.md) · [sum-vs-nested-lookup recipe](../../cookbook/performance/sum-vs-nested-lookup.md).

### Nested-IF hell instead of a mapping module

- **Symptom:** 5–6-level `IF`/`ELSE` chains with business rules hardcoded in the expression; changing a threshold means editing 14 line items across 7 modules.
- **Why:** the rule felt small enough to inline. It never is.
- **Fix:** externalise the rule set as a small **mapping/driver module** and resolve it with `LOOKUP`. One place to change the rule.
- **Learn:** [logical functions](../02-formulas/logical-functions.md) · [DISCO 'System'](../03-methodology/disco.md) · [replace-if-with-boolean](../../cookbook/performance/replace-if-with-boolean.md).

### Time functions instead of a pre-aggregated module

- **Symptom:** the same `TIMESUM(...)` / cumulative call re-evaluated all over the model.
- **Why:** convenient to repeat; the cost is invisible until you profile.
- **Fix:** build the summary **once** in a properly-dimensioned module and reference it. Calculate once, reuse.
- **Learn:** [time functions](../02-formulas/time-functions.md) · [YTD/MTD/QTD recipe](../../cookbook/time-and-forecasting/ytd-mtd-qtd.md) · PLANS **Necessary**.

### Hardcoded numbers in formulas

- **Symptom:** tax rates, FX rates, thresholds inline in expressions. When a rate changes you're grepping the model.
- **Why:** speed in the moment.
- **Fix:** drive every assumption from a **System/Inputs** module. No magic numbers, ever.
- **Learn:** [The Planual](../03-methodology/planual.md) (Sustainable) · [DISCO](../03-methodology/disco.md).

### Format & precision sprawl

- **Symptom:** everything is full-precision `Number` when half should be `Integer`/`Boolean`. Storage and compute compound, especially on Classic.
- **Fix:** pick the **tightest format** that's correct. Booleans for flags, integers for counts.
- **Learn:** [line items & formats](../01-fundamentals/line-items-and-formats.md).

### Summary methods left on default

- **Symptom:** `Sum` everywhere; rates and ratios show nonsense at parent levels; users "only trust the leaf."
- **Why:** Sum is the default and nobody changed it.
- **Fix:** set the **summary method deliberately** (Sum / Average / Formula / None / Ratio) on every line item where the parent total matters.
- **Learn:** [line items & formats](../01-fundamentals/line-items-and-formats.md) · this is a silent-bug classic.

### Text fields as pseudo-dimensions

- **Symptom:** category strings stored as text and compared with string functions, blocking the engine's dimensional joins.
- **Why:** "creating a proper list is too heavy."
- **Fix:** make it a **list**. Resolve incoming text to list items with `FINDITEM`, then map.
- **Learn:** [lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md) · [finditem-text-key recipe](../../cookbook/hierarchies-and-lists/finditem-text-key.md).

### FINDITEM as duct tape

- **Symptom:** `FINDITEM` everywhere a proper **data hub** mapping should exist — it's how the hub never gets built.
- **Fix:** `FINDITEM` is fine in narrow doses (resolving a code on import). For shared master data, build the hub.
- **Learn:** [data hub architecture](../08-advanced-features/data-hub-architecture.md) · [build-a-data-hub recipe](../../cookbook/data-and-imports/build-a-data-hub.md).

### Calculated subsets stacked deep

- **Symptom:** subsets of calculated booleans on top of subsets on top of subsets. Each layer is a recompute dependency and an ALM-sync minefield.
- **Fix:** keep subset logic **shallow and explicit**; prefer a clear Boolean driver to layered calculated subsets.
- **Learn:** [line item subsets](../07-performance/line-item-subsets.md) · [numbered lists & subsets](../01-fundamentals/numbered-lists-and-subsets.md).

---

## B. Architecture-level (modeling-in-the-large)

### The single-model trap

- **Symptom:** everything in one model; a structural change anywhere re-evaluates everything; calculation order is opaque.
- **Why:** cross-model integration "feels hard."
- **Fix:** split along natural boundaries with a **data hub** feeding spoke models. One-way flow.
- **Learn:** [data hub architecture](../08-advanced-features/data-hub-architecture.md) · [integration](../04-integration/).

### Model proliferation with no data hub (the opposite trap)

- **Symptom:** 6–8 models each pulling production data directly; customer codes drift; a "Data Hub" model exists in name with no hub discipline.
- **Fix:** one **canonical master-data layer**; spokes import *from the hub*, never re-import the same source.
- **Learn:** [data hub architecture](../08-advanced-features/data-hub-architecture.md) · [build-a-data-hub](../../cookbook/data-and-imports/build-a-data-hub.md).

### Module sprawl with no taxonomy

- **Symptom:** 500+ modules named `Calc_v2`, `New_Calc`, `Final_Calc_USE_THIS_ONE`. "Navigate to module" is the only way to find anything.
- **Fix:** **DISCO discipline + naming convention** from day one (`DAT/INP/SYS/CAL/OUT` + numbering). Maintain a model map.
- **Learn:** [DISCO](../03-methodology/disco.md) · [naming conventions](../../templates/naming-conventions.md).

### Hierarchy built to match the org chart, not the calculation logic

- **Symptom:** the list hierarchy mirrors the reporting structure at kickoff; two reorgs later every parent/child formula is implicitly wrong and moving it is a months-long project.
- **Fix:** design hierarchies around **calculation/aggregation needs**; keep volatile reporting structures as **attributes/mappings** in System modules, not as the spine.
- **Learn:** [lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md) · [item-parent-ancestor recipe](../../cookbook/hierarchies-and-lists/item-parent-ancestor-rollup.md).

### Versions abused

- **Symptom:** native Versions pressed into service for every scenario — or a home-rolled scenario list that then can't use native version features. Switching later is a rebuild.
- **Fix:** decide deliberately: **native Versions** for Actual/Budget/Forecast-style; a **list dimension** for many what-if scenarios. Know the trade-off *before* you commit.
- **Learn:** [versions](../01-fundamentals/versions.md).

### Unbounded production lists

- **Symptom:** a numbered transactional list grows forever; after 3 years it has millions of members and every module dimensioned by it is in trouble. "We'll deal with it next quarter."
- **Fix:** design an **archive/clear strategy up front** — `DELETE` actions, time-boxed retention, summarise-then-purge.
- **Learn:** [numbered lists](../01-fundamentals/numbered-lists-and-subsets.md) · [clear-a-numbered-list recipe](../../cookbook/hierarchies-and-lists/clear-a-numbered-list.md) · [model size](../09-troubleshooting/model-size-and-workspace-management.md).

### Access models layered into untestable behaviour

- **Symptom:** selective access + role-based module access + DCA interact so the visible number depends on *who's looking*; two builders see different dashboards and can't tell bug from design.
- **Fix:** keep access **layered and documented** — one mechanism per concern, a System module that makes "who can see/do what" explicit and inspectable. Test as multiple personas.
- **Learn:** [roles & selective access](../06-security-alm/roles-and-selective-access.md) · [DCA](../06-security-alm/dynamic-cell-access.md) · [cascading-selective-access recipe](../../cookbook/security-and-dca/cascading-selective-access.md).

### Workspace boundaries chosen for licensing, not architecture

- **Symptom:** a model split across workspaces because one hit the size cap — the split runs across a natural calculation boundary and now needs awkward sync.
- **Fix:** push back with data (see [licensing as an architecture force](platform-strategy.md)); if you must split, split on a **clean integration seam**, not mid-calculation.
- **Learn:** [model size & workspace management](../09-troubleshooting/model-size-and-workspace-management.md).

### Dashboards as static printouts

- **Symptom:** one page per stakeholder, no interaction surface; the "self-service" promise never lands.
- **Fix:** build pages as **tools** — context selectors, input vs report separation, drill paths.
- **Learn:** [app design principles](../05-ux/app-design-principles.md) · [context-selector recipe](../../cookbook/ux-and-workflow/context-selector-dashboard.md).

### Classic dashboards + UX pages maintained in parallel forever

- **Symptom:** Classic dashboards still in prod years after "we're moving to Pages"; new joiners must learn two paradigms.
- **Fix:** as a builder, **build new work in the New UX**; flag the maintenance cost of the parallel estate to whoever owns the roadmap.
- **Learn:** [New UX](../05-ux/new-ux-pages-boards.md) · [classic dashboards](../05-ux/classic-dashboards.md).

---

**Related:** [engineering discipline without the tooling](engineering-discipline.md) · [platform strategy & survival](platform-strategy.md) · [model-build checklist](../03-methodology/model-build-checklist.md) · [optimization checklist](../07-performance/optimization-checklist.md)
