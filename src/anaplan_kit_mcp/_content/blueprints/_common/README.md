# `_common` — The Shared Dimensional Backbone

> **Level:** L2 · **Area:** Blueprint (shared backbone) · **DISCO:** System

This folder defines, **once**, the structures that every domain model reuses: Time, Versions, the
Organization hierarchy, Currency, the P&L Account hierarchy and Product. Think of it as the shared
**data hub of dimensions** — the "common ground" beneath FP&A, Sales, Supply Chain and Workforce.

In a real tenant these typically live in a small set of **System (`SYS`) modules** in a data hub or a
foundation model, then flow into spoke models via imports. In these blueprints we keep them in one
place and have each domain *reference* them rather than redefine them.

---

## Why share a backbone? (PLANS link)

| PLANS principle | How the shared backbone serves it |
| --- | --- |
| **Sustainable** | New month / country / product / account is added in **one** place; all four domains inherit it with no formula change. |
| **Logical** | Every domain speaks the same dimensional language — `CC-1100` means the same Cost Centre everywhere. |
| **Necessary** | Time, org and accounts are defined once, not four times. No duplication. |
| **Auditable** | Mappings and flags live in named `SYS` modules, so a reader can trace any roll-up. |

> Golden rule (*Sustainable*): never hard-code a date, a member or a rate in a formula. Drive
> everything from these `SYS` modules and Time. See [PLANS](../../docs/03-methodology/plans-standard.md).

---

## What's in here

| Page | Defines | Key `SYS` module |
| --- | --- | --- |
| [`time-and-versions.md`](time-and-versions.md) | Monthly Time on a fiscal year; Versions Actual / Budget / Forecast | `SYS01 Time Settings`, `SYS90 Model Settings` |
| [`organization-hierarchy.md`](organization-hierarchy.md) | `Region › Country › Cost Centre/Entity` composite list | `SYS02 Organization Details` |
| [`common-lists.md`](common-lists.md) | Currency, P&L Account hierarchy, Product, and reference lists | `SYS04 Exchange Rates`, `SYS03 Account Details` |

---

## How a domain reuses the backbone

A domain page never re-declares Time or rebuilds the org chart. It simply:

1. **Dimensions its modules** by the shared lists (e.g. `Applies To: Cost Centre × Product × Time`).
2. **References shared `SYS` modules** in formulas (e.g. `SYS04 Exchange Rates.Rate to Group`).
3. **Adds only domain-specific lists** (e.g. Sales Rep, SKU, Employee) layered on top.

```
_common (SYS) ──────────────► domain modules (CAL/INP/OUT)
  Time                          dimension every time-phased module
  Versions                      Actual vs Budget vs Forecast everywhere
  Organization + SYS02          roll cost centres up to Region/Group
  Currency  + SYS04             convert local → group currency
  P&L Account + SYS03           classify lines as Revenue / COGS / Opex
  Product                       shared planning grain for FP&A/Sales/SC
```

---

**Related:** [Blueprints overview](../README.md) ·
[`time-and-versions.md`](time-and-versions.md) · [`organization-hierarchy.md`](organization-hierarchy.md) ·
[`common-lists.md`](common-lists.md) · [DISCO](../../docs/03-methodology/disco.md)
