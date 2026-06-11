# `_common` — Shared Reference Lists

> **Level:** L2 · **Area:** Blueprint (shared backbone) · **DISCO:** System

The remaining shared lists every domain leans on: **Currency** (+ an exchange-rate module),
the **P&L Account** hierarchy (the chart of accounts the FP&A P&L is built on), the **Product**
hierarchy, and a couple of small reference lists. Defined once; referenced everywhere.

---

## Currency

| List name | Type | Parent | Sample members | Notes |
| --- | --- | --- | --- | --- |
| **Currency** | flat | — | `GBP`, `EUR`, `USD`, `INR` | Group/reporting currency = **USD**. Each Country carries its local one (see [org hierarchy](organization-hierarchy.md)). |

### `SYS04 Exchange Rates` — the FX module shape

A **System** module holding the rate from each currency to the group currency, by **month and
version** (rates differ Actual vs Budget vs Forecast). Conversions read this — never a hard-coded rate.

**Module:** `SYS04 Exchange Rates` · **DISCO: System** · **Applies To:** Currency × Time × Versions

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Rate to Group | Number (4 dp) | — | Currency × Time × Versions | input — units of group currency per 1 unit local |
| Is Group Currency? | Boolean | — | Currency | `ITEM(Currency) = Currency.USD` |
| Rate (filled) | Number (4 dp) | — | Currency × Time × Versions | `IF Is Group Currency? THEN 1 ELSE Rate to Group` |

> Pattern: a local amount × `Rate (filled)` (looked up by the entity's `Local Currency`) gives the
> group-currency amount. Used by FP&A, Sales and Workforce. See
> [FP&A formulas](../fpa-pl-planning/formulas.md).

---

## P&L Account hierarchy

The chart of accounts the FP&A P&L rolls up to. Sales feeds the Revenue branch; Workforce and Supply
Chain feed the cost branches.

| List name | Type | Parent | Sample members | Notes |
| --- | --- | --- | --- | --- |
| **L1 P&L Statement** | hierarchy (top) | — | `Net Profit` | The statement total. |
| **L2 P&L Group** | hierarchy | L1 P&L Statement | `Revenue`, `COGS`, `Gross Profit`, `Opex`, `EBITDA` | Subtotal groups. |
| **L3 P&L Account** | hierarchy (leaf) | L2 P&L Group | `Product Revenue`, `Services Revenue`, `Direct Materials`, `Direct Labour`, `Salaries`, `Travel`, `Marketing`, `IT` | Where postings/plan lines land. |

### `SYS03 Account Details` — account classification

**Module:** `SYS03 Account Details` · **DISCO: System** · **Applies To:** L3 P&L Account

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Account Group | List: L2 P&L Group | — | L3 P&L Account | `PARENT(ITEM(L3 P&L Account))` |
| Sign | Number | — | L3 P&L Account | input — `+1` revenue, `-1` cost (for clean P&L math) |
| Is Revenue? | Boolean | — | L3 P&L Account | `Account Group = L2 P&L Group.Revenue` |
| Is Cost? | Boolean | — | L3 P&L Account | `NOT Is Revenue?` |

---

## Product hierarchy

The shared planning grain for FP&A (revenue), Sales (targets) and Supply Chain (demand).

| List name | Type | Parent | Sample members | Notes |
| --- | --- | --- | --- | --- |
| **L1 Product Family** | hierarchy (top) | — | `Hardware`, `Software`, `Services` | Reporting roll-up. |
| **L2 Product** | hierarchy (leaf) | L1 Product Family | `Sensor A`, `Sensor B`, `Platform License`, `Support Plan` | Planning grain for revenue & demand. Supply Chain plans at SKU (a child) — see [supply-chain](../supply-chain/lists.md). |

---

## Small reference lists

| List name | Type | Parent | Sample members | Notes |
| --- | --- | --- | --- | --- |
| **Entity Type** | flat | — | `Sales`, `Ops`, `R&D`, `Shared` | Used by `SYS02 Organization Details`. |
| **P&L Line Type** | flat | — | `Volume`, `Price`, `Amount` | Optional driver tag for revenue modules. |

---

## How domains reuse these lists

| List | FP&A | Sales | Supply Chain | Workforce |
| --- | --- | --- | --- | --- |
| Currency + `SYS04` | ✅ convert P&L | ✅ convert targets | — (units, not $) | ✅ convert salary |
| P&L Account + `SYS03` | ✅ owns it | feeds Revenue | feeds COGS | feeds Salaries |
| Product | ✅ revenue grain | ✅ target grain | ✅ demand grain | — |

---

**Related:** [`organization-hierarchy.md`](organization-hierarchy.md) ·
[`time-and-versions.md`](time-and-versions.md) ·
[FP&A blueprint](../fpa-pl-planning/README.md) ·
[Lists & hierarchies](../../docs/01-fundamentals/lists-and-hierarchies.md)
