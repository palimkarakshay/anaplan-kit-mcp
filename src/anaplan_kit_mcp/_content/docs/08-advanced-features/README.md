# Advanced Features — Platform Capabilities Beyond Modeling

> **Level:** L3 · **Area:** Advanced Features

Everything in the rest of this kit teaches you to **build a model** — lists, modules, line items,
formulas, imports, UX. That is the core craft, and most of your job. But Anaplan is a *platform*,
and a working consultant keeps bumping into capabilities that sit **around** the model: a
multi-model **architecture** that keeps data clean, **solvers** and **ML** that produce numbers
your formulas can't, **process orchestration** that tells people what to do, and **Office add-ins**
that let business users consume the model from where they already live.

This section is your map to those capabilities. You don't need any of them on day one — but you
*will* meet each on a real project, and knowing what each one is (and is not) for stops you from
either reinventing it by hand or reaching for it when a plain module would do.

## What lives here

| Page | What it is | When a beginner first meets it |
| --- | --- | --- |
| [data-hub-architecture.md](data-hub-architecture.md) | The **hub-and-spoke** pattern: one central Data Hub model feeding many planning "spoke" models. **The most important page in this section.** | The moment a second model needs the same master data or actuals — usually your first real client estate. |
| [optimizer.md](optimizer.md) | **Anaplan Optimizer** — a linear / mixed-integer programming engine built into the platform. Solves allocation, network/supply, and blending problems. | When a requirement says "find the *best* plan" (cheapest, most profitable) under constraints, not just "calculate this plan". |
| [planiq.md](planiq.md) | **PlanIQ** — Anaplan's AI/ML forecasting. Trains forecast models on history and writes predictions back into your modules. | When demand/revenue forecasting needs statistical accuracy beyond a growth-rate formula. |
| [workflow.md](workflow.md) | **Anaplan Workflow** — orchestrating a planning *process*: tasks, owners, due dates, status, approvals across contributors. | When a cycle involves many people who must do things in order and someone has to chase them. |
| [excel-powerpoint-and-anaplan-xl.md](excel-powerpoint-and-anaplan-xl.md) | The **Office add-ins**: Anaplan for Excel & PowerPoint, and **Anaplan XL** reporting. Read/write Anaplan data from Office. | When business consumers say "can I just get this in Excel?" |

## How to read this section

Start with **[data-hub-architecture.md](data-hub-architecture.md)** — it's foundational, it's
pure modeling discipline (no add-on licence), and it ties straight into [PLANS](../03-methodology/plans-standard.md)
and [DISCO](../03-methodology/disco.md). The other four pages are **specialized capabilities**:
read them when a project actually calls for them. Optimizer and PlanIQ are **licensed add-ons** /
separately-enabled features; Workflow and the Office add-ins are about how people *drive* and
*consume* the model rather than how you build it.

> ⚠️ Several of these are commercial add-ons or separately licensed, and Anaplan ships changes
> often. Treat the pages here as conceptual orientation and **confirm the current specifics in
> Anapedia** ([help.anaplan.com](https://help.anaplan.com/)) for your tenant.

**Related:** [Integration](../04-integration/) (how a Data Hub physically moves data) ·
[Security & ALM](../06-security-alm/) (DCA, the static cousin of Workflow) ·
[Methodology](../03-methodology/) (PLANS & DISCO, which the Data Hub embodies) ·
[Cookbook](../../cookbook/) · [Learning Path](../../LEARNING-PATH.md)
