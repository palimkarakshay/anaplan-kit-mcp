# App Design Principles — Building for Planners

> **Level:** L2 · **Area:** UX · **PLANS:** Logical, Performance, Sustainable

A model builder's last job is the one users judge you on: the **screens**. A perfect model
behind a confusing page gets abandoned. This page is a short set of principles for designing
[Pages](new-ux-pages-boards.md) (and [classic dashboards](classic-dashboards.md)) that
planners can use without training — each tied back to **PLANS**.

## 1. Separate input from report

The single biggest design rule, straight out of [DISCO](../03-methodology/disco.md):

- **Input pages** let planners type — they read/write **Inputs (I)** modules.
- **Report pages** let users read — they read **Outputs (O)** modules, read-only.

Don't mix "enter your numbers" and "admire the totals" on one cluttered screen. A planner
should always know whether they're *entering* or *reviewing*. *(Logical, Auditable.)*

## 2. Minimise clicks to the task

Open the page → the planner can act. That means:

- Sensible **default context** (current period, working version) so nothing useful is
  hidden behind a selector the user must set first.
- The **entry grid in front**, not three pages deep.
- A **clear action button** for "Submit" / "Recalculate" / "Run load" right where the
  workflow needs it. *(Logical.)*

## 3. Let context selectors do the work

One [context selector](new-ux-pages-boards.md#context-selectors) driving many cards beats a
filter on every card and beats one page per region.

- **One page, many users** — each picks their context. *(Sustainable — no duplication.)*
- Fewer controls on screen = less to misunderstand. *(Clarity.)*

## 4. Design for performance

The page inherits the model's [performance](../07-performance/) — and can make it worse:

| Do | Don't |
| --- | --- |
| Point cards at small, **purpose-shaped Output views** | Publish a giant raw calc module to a card |
| Keep open lists/columns to what's needed | Show every line item and every period at once |
| Use **Time Ranges** so cards only span relevant periods | Render the full calendar when one quarter is meant |
| Split heavy visuals onto a separate report page | Stack a dozen heavy charts on one Board |

A page that opens slowly is a page planners avoid. *(Performance.)*

## 5. Clarity and accessibility

- **Name everything for the planner**, not the builder: "Headcount Plan", not
  `INP03 HC v2`.
- Add **short instructions** (a text card / header) so a first-time user knows what to do.
- Use **conditional formatting** for signal (red variance) — sparingly, with meaning.
- Ensure colour isn't the *only* cue (use labels/values too) so the page is readable for
  everyone.
- Keep a **consistent layout** across pages so users learn the app once.

## 6. Control what's editable — visibly

Pair good layout with the right access:

- Use [Dynamic Cell Access](../06-security-alm/dynamic-cell-access.md) so cells are
  editable only when they should be (e.g. while a plan is in *Draft*).
- Use [roles & selective access](../06-security-alm/roles-and-selective-access.md) so each
  planner sees and edits only their slice.

A cell a user can't edit should *look* locked — uneditable-but-clickable cells generate
support tickets.

## Quick PLANS-UX checklist

- [ ] Input and report screens are **separate** (I vs O). *(Logical)*
- [ ] Page opens **ready to use** with good default context. *(Logical)*
- [ ] **Context selectors** drive cards; no page-per-list-item duplication. *(Sustainable)*
- [ ] Cards point at **lean Output views**, not raw calc modules. *(Performance)*
- [ ] Time Ranges / open lists keep the page **light**. *(Performance)*
- [ ] Names, instructions and formatting are **planner-friendly and accessible**.
- [ ] Editability matches reality via **DCA / selective access**.

**Related:** [New UX — Pages & Boards](new-ux-pages-boards.md) ·
[Classic Dashboards](classic-dashboards.md) ·
[DISCO](../03-methodology/disco.md) · [PLANS](../03-methodology/plans-standard.md) ·
[Performance](../07-performance/) ·
[Dynamic Cell Access](../06-security-alm/dynamic-cell-access.md)

> Source: Anaplan UX best-practice materials (`help.anaplan.com` & Anaplan Community). See
> [`SOURCES.md`](../../SOURCES.md).
