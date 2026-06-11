# New UX — Apps, Pages, Boards & Worksheets

> **Level:** L1 · **Area:** UX · **PLANS:** Logical, Sustainable · **DISCO:** Inputs, Outputs

The **New UX** is how you build interfaces in Anaplan today. You assemble screens from
**cards**, group screens into **pages**, and group pages into an **app** that planners open
to do their work. This page lays out the vocabulary and the one distinction that shapes
every screen you'll design: **input pages vs report pages**.

## The hierarchy of containers

```
App                     a named workspace for an audience ("FP&A Planning")
 └─ Page                a single screen
     ├─ Board           a flexible, card-based layout
     └─ Worksheet       a focused grid + supporting cards
         └─ Card        the building blocks placed on a page
```

| Container | What it is |
| --- | --- |
| **App** | A collection of pages built for a group of users — e.g. one app for budget owners. Users open the app, not the model. |
| **Page** | One screen inside an app. Two flavours: **Board** and **Worksheet**. |
| **Board** | A free-form layout of multiple cards — grids, charts, KPIs, text, images, actions. Good for **overview / report** screens and landing pages. |
| **Worksheet** | A page centred on **one main grid** with supporting cards alongside. Good for **focused data entry** and detail work. |
| **Card** | The unit you place on a page: a grid card, chart card, KPI card, field/text card, image, or action button — each usually driven by a module view. |

> A **card** is a view of a module or list, dressed for display. You don't re-enter data in a
> card — you point it at a module view and choose how it looks.

## Context selectors

A **context selector** sits at the top of a page and sets the *context* for the cards below
it — e.g. which **Version**, which **Region**, which **Time** period. Change the selector and
every card respecting that context updates together.

- Context selectors keep a page **uncluttered**: one selector drives many cards instead of
  each card carrying its own filter.
- They make pages **reusable**: the same page serves every region because the user picks
  theirs from the selector. *(Sustainable — no page-per-region duplication.)*
- Set sensible **defaults** (e.g. current period, working version) so the page is useful the
  instant it opens.

## Input pages vs report pages

This is the most important design decision in the New UX — and it mirrors **DISCO's** split
between **Inputs** and **Outputs**:

| | **Input page** | **Report page** |
| --- | --- | --- |
| Purpose | Planners **type** numbers / make decisions | Users **read** results |
| Reads/writes | Writes to **Inputs (I)** modules | Reads from **Outputs (O)** modules |
| Best page type | Often a **Worksheet** (one focused entry grid) | Often a **Board** (KPIs, charts, summary grids) |
| Editing | Cells editable (subject to [DCA](../06-security-alm/dynamic-cell-access.md) / [access](../06-security-alm/roles-and-selective-access.md)) | Read-only |
| Cues | Clear "enter here" framing, validation, submit action | Headline numbers, variances, trends |

Why separate them:

- **Clarity.** A planner who lands on an entry page knows exactly what to do; a reader of a
  report isn't tempted to type into a number they shouldn't.
- **Safety.** Report pages point at read-only **Output** modules, so there's nothing to
  break by clicking.
- **Performance.** Entry pages stay small and snappy; heavy aggregated visuals live on
  report pages built from purpose-shaped output views. *(Performance.)*

> A common pattern: a **Worksheet** for entry ("Enter your headcount plan") plus a **Board**
> for review ("Plan vs Budget by department"), linked so a planner enters, then jumps to see
> the impact.

## Building a card — the workflow

1. Build the **module view** you want to show (the right line items, dimensions on rows/
   columns, filters) and save it as a named view — ideally an **Output** view for reports.
2. Add a **card** to a page and point it at that saved view.
3. Choose the **card type** (grid, chart, KPI…) and tidy formatting.
4. Wire up **context selectors** so the card responds to the page context.
5. Add **action buttons** (run a [process](../04-integration/actions-and-processes.md),
   submit, navigate) where the workflow needs them.

> Shape the **view in the model**, then display it. Don't try to do calculation work in the
> UX — the page only presents what the modules already compute. *(Logical, Auditable.)*

**Related:** [App Design Principles](app-design-principles.md) ·
[Classic Dashboards](classic-dashboards.md) ·
[DISCO — Inputs & Outputs](../03-methodology/disco.md) ·
[Dynamic Cell Access](../06-security-alm/dynamic-cell-access.md) ·
[Actions & Processes](../04-integration/actions-and-processes.md)

> Source: Anaplan New UX docs (`help.anaplan.com`, UX / Pages & apps section). See
> [`SOURCES.md`](../../SOURCES.md).
