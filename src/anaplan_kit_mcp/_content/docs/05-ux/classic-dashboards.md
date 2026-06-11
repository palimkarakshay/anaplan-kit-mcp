# Classic Dashboards (Legacy)

> **Level:** L1 · **Area:** UX · **PLANS:** Sustainable

**Classic dashboards** are Anaplan's original way of building user screens, predating the
[New UX](new-ux-pages-boards.md). You won't build new ones if you can help it, but you *will*
open older models that are full of them — so you need to read and maintain them.

## What a classic dashboard is

A **classic dashboard** is a single screen you assemble inside the classic model interface
by **publishing** elements onto it:

| Element | What it is |
| --- | --- |
| **Grid** | A published module view — rows, columns, line items — that users read or edit |
| **Chart** | A bar / line / pie visual built from a grid |
| **Text box** | Headings, instructions, labels |
| **Action button** | Runs an [import / export / process](../04-integration/actions-and-processes.md) |
| **Selector / page control** | Lets the user pick a list item, version, or time — the classic ancestor of a context selector |

You publish a module view "to a dashboard", arrange the elements on a grid-like canvas, and
control which users see it via roles. Conceptually it's the same idea as a New UX **Board**:
cards/grids on a screen driven by selectors — just an older toolset and look.

## How it maps to the New UX

| Classic | New UX equivalent |
| --- | --- |
| Dashboard | **Page** (Board or Worksheet) |
| Published grid | **Grid card** |
| Published chart | **Chart card** |
| Page selector | **Context selector** |
| Action button | **Action card / button** |

The **underlying modules are identical** — both interfaces are presentation layers over the
same line items. Migrating a dashboard to the New UX is largely re-presenting the same views
as cards, not rebuilding the model.

## When you'll still encounter them

- **Legacy models** built before the New UX became standard.
- **Models mid-migration**, where some screens have moved and some haven't.
- **Quick admin/debug grids** an older team left in place.

## Working with them sensibly

- **Don't invest in new classic dashboards.** Build new interfaces in the
  [New UX](new-ux-pages-boards.md). *(Sustainable.)*
- When you touch a legacy model, consider whether the screen is a good candidate to
  **migrate** to a Page — especially high-traffic ones.
- The same design rules apply either way: separate **input** screens from **report**
  screens, keep selectors driving many grids, and point grids at purpose-shaped views — see
  [App Design Principles](app-design-principles.md).
- Editing rights on a classic grid still obey
  [roles, selective access](../06-security-alm/roles-and-selective-access.md) and
  [DCA](../06-security-alm/dynamic-cell-access.md) — security is set on the model, not the
  dashboard.

**Related:** [New UX — Pages & Boards](new-ux-pages-boards.md) ·
[App Design Principles](app-design-principles.md) ·
[Security & ALM](../06-security-alm/) ·
[Actions & Processes](../04-integration/actions-and-processes.md)

> Source: Anaplan classic dashboard docs (`help.anaplan.com`, classic UX section). See
> [`SOURCES.md`](../../SOURCES.md).
