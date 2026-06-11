# Cookbook — Anaplan "cheat code" recipes

This is the centerpiece of the kit: ready-to-use recipes for the scenarios a new Anaplan model builder actually gets handed at work. Each recipe is **self-contained and copy-pasteable** — it states how a stakeholder phrases the ask, the Anaplan-idiomatic approach and *why* (referenced to [PLANS](../docs/03-methodology/plans-standard.md) and [DISCO](../docs/03-methodology/disco.md)), the **blueprint** (lists/modules/line items as the Line Item / Format / Summary / Applies To / Formula grid you see in Anaplan), the exact **formulas**, the **pitfalls** that bite beginners, and **performance/PLANS notes**.

Anaplan is a SaaS GUI tool — there's no compile-and-run outside a tenant — so recipes *describe and illustrate*, validated against Anaplan's published syntax (see [`SOURCES.md`](../SOURCES.md)). Use them as a starting point and adapt the names to your model.

> New here? Read [`LEARNING-PATH.md`](../LEARNING-PATH.md) first, then come back and solve your task. Most recipes are **Level 2**; security/DCA ones reach **Level 3**. Every recipe carries a `Level · Area · PLANS · DISCO` badge.

How to use: find your task in the table below, open the recipe, copy the blueprint and formulas into your model, then walk the **Pitfalls** section before you call it done.

---

## Data & Imports

Getting source data into Anaplan cleanly — hubs, deltas, list creation, hierarchies, error handling, keys.

| Recipe | Category | Level | What it solves |
| --- | --- | --- | --- |
| [Build a data hub](data-and-imports/build-a-data-hub.md) | Data & Imports | L2 | One centralised source-of-truth model feeding spokes, one-way flow |
| [Incremental / delta import](data-and-imports/incremental-delta-import.md) | Data & Imports | L2 | Load only changed rows instead of full truncate-and-reload |
| [Auto-create list members on import](data-and-imports/auto-create-list-members.md) | Data & Imports | L2 | Let an import safely create new list items, mapped to the right parent |
| [Flat file to composite hierarchy](data-and-imports/flat-file-to-hierarchy.md) | Data & Imports | L2 | Turn a flat file with parent codes into a multi-level hierarchy |
| [Handle import errors & dump files](data-and-imports/handle-import-errors-and-dump-files.md) | Data & Imports | L2 | Failed/ignored rows, dump files, ignore-vs-fail, reconciling counts |
| [Concatenated key for imports](data-and-imports/concatenated-key-for-imports.md) | Data & Imports | L2 | Build a unique text key (e.g. Entity#Account#Month) for matching/upsert |

## Mapping & Allocation

Moving and spreading numbers across dimensions with mappings and ratios.

| Recipe | Category | Level | What it solves |
| --- | --- | --- | --- |
| [Remap data between dimensions (SUM/LOOKUP)](mapping-and-allocation/sum-lookup-remap.md) | Mapping & Allocation | L2 | Move data across dimensions via a SYS mapping module |
| [Top-down allocation by ratio](mapping-and-allocation/top-down-allocation-by-ratio.md) | Mapping & Allocation | L2 | Spread a parent total to children by a driver ratio |
| [Breakback: type a total, disaggregate](mapping-and-allocation/breakback-ratio-input.md) | Mapping & Allocation | L2 | Let users type a total and auto-split it to detail |
| [Allocate cost by a driver](mapping-and-allocation/allocate-by-driver.md) | Mapping & Allocation | L2 | Allocate shared cost by headcount / sqft / revenue driver |

## Time & Forecasting

Cumulatives, rolling windows, actual/forecast blends, phasing, and prior-year comparisons.

| Recipe | Category | Level | What it solves |
| --- | --- | --- | --- |
| [YTD / MTD / QTD running totals](time-and-forecasting/ytd-mtd-qtd.md) | Time & Forecasting | L2 | CUMULATE with reset flags for to-date figures |
| [Rolling forecast (n-month window)](time-and-forecasting/rolling-forecast.md) | Time & Forecasting | L2 | A self-advancing rolling forecast window driven by one setting |
| [Actual / forecast switchover](time-and-forecasting/actual-forecast-switchover.md) | Time & Forecasting | L2 | Actuals up to a cutoff, forecast after — Boolean/version driven |
| [Seasonality / phasing](time-and-forecasting/seasonality-phasing.md) | Time & Forecasting | L2 | Spread an annual figure to months via a seasonality profile |
| [Prior-year comparison (YoY)](time-and-forecasting/prior-year-comparison.md) | Time & Forecasting | L2 | Same-period-last-year and growth % with LAG / OFFSET |

## Financial Calcs

The classic finance building blocks: FX, depreciation, debt, and variance bridges.

| Recipe | Category | Level | What it solves |
| --- | --- | --- | --- |
| [Currency conversion](financial-calcs/currency-conversion.md) | Financial Calcs | L2 | Local → reporting currency via a rate-table lookup |
| [FX restatement (constant currency)](financial-calcs/fx-restatement.md) | Financial Calcs | L2 | Restate at plan/PY rates to isolate the FX effect |
| [Straight-line depreciation](financial-calcs/straight-line-depreciation.md) | Financial Calcs | L2 | Depreciate an asset evenly over its useful life |
| [Loan amortization schedule](financial-calcs/loan-amortization.md) | Financial Calcs | L2 | PMT / CUMIPMT level-payment schedule with interest/principal split |
| [Variance waterfall / bridge](financial-calcs/variance-waterfall-bridge.md) | Financial Calcs | L2 | Decompose a variance into named effects for a waterfall chart |

## Hierarchies & Lists

Working with the tree, carrying values, resolving codes, and transactional numbered lists.

| Recipe | Category | Level | What it solves |
| --- | --- | --- | --- |
| [ITEM / PARENT / ANCESTOR rollups](hierarchies-and-lists/item-parent-ancestor-rollup.md) | Hierarchies & Lists | L2 | Read parents/ancestors and test branch membership |
| [Latest non-blank (carry forward)](hierarchies-and-lists/latest-non-blank.md) | Hierarchies & Lists | L2 | Keep showing the last entered value until it changes |
| [Resolve a text code to a list item](hierarchies-and-lists/finditem-text-key.md) | Hierarchies & Lists | L2 | Turn a text code into a list reference with FINDITEM |
| [Model transactions with a numbered list](hierarchies-and-lists/numbered-list-transactions.md) | Hierarchies & Lists | L2 | Hold line-level transactional data efficiently |
| [Clear a numbered list before reload](hierarchies-and-lists/clear-a-numbered-list.md) | Hierarchies & Lists | L2 | DELETE action to wipe transactional data before a full reload |

## UX & Workflow

Building usable pages and simple workflows for planners and reviewers.

| Recipe | Category | Level | What it solves |
| --- | --- | --- | --- |
| [Approval status workflow](ux-and-workflow/approval-status-workflow.md) | UX & Workflow | L2 | A status line item driving a Draft → Submit → Approve flow |
| [Context selector dashboard](ux-and-workflow/context-selector-dashboard.md) | UX & Workflow | L2 | One reusable page where selectors drive every card |
| [Input pages vs report pages](ux-and-workflow/input-vs-report-pages.md) | UX & Workflow | L2 | Separate editable entry from read-only reporting (DISCO-aligned) |
| [Dynamic time filter](ux-and-workflow/dynamic-time-filter.md) | UX & Workflow | L2 | A SYS Boolean time module controlling which periods a page shows |

## Security & DCA

Controlling who sees and edits what — roles, selective access, and Dynamic Cell Access.

| Recipe | Category | Level | What it solves |
| --- | --- | --- | --- |
| [DCA: read/write by status](security-and-dca/dca-read-write-by-status.md) | Security & DCA | L3 | Lock cells after submit using a status-driven DCA Boolean |
| [Cascading selective access](security-and-dca/cascading-selective-access.md) | Security & DCA | L3 | Managers see only their hierarchy branch, cascaded down |
| [Hide or lock by role](security-and-dca/hide-or-lock-by-role.md) | Security & DCA | L3 | Combine roles + DCA for per-role visibility and editability |

## Performance

Keeping the model fast and small, and proving it still ties.

| Recipe | Category | Level | What it solves |
| --- | --- | --- | --- |
| [Replace nested IF with a Boolean](performance/replace-if-with-boolean.md) | Performance | L2 | Kill heavy nested IF on big modules |
| [Shrink with subsets & time ranges](performance/shrink-with-subsets-and-time-ranges.md) | Performance | L2 | Cut cell count with subsets and time ranges |
| [SUM vs nested LOOKUP](performance/sum-vs-nested-lookup.md) | Performance | L2 | Choose the right aggregation function for the relationship |
| [Reconciliation / control-total check](performance/reconciliation-check-module.md) | Performance | L2 | A check module that flags when calculated ≠ source |

---

**36 recipes** across 8 categories. Methodology behind them: [PLANS](../docs/03-methodology/plans-standard.md) · [DISCO](../docs/03-methodology/disco.md) · [The Planual](../docs/03-methodology/planual.md). Validation sources: [`SOURCES.md`](../SOURCES.md).
