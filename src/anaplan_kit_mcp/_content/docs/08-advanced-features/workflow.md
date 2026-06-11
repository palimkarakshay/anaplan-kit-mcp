# Anaplan Workflow — Orchestrating the Planning Process

> **Level:** L3 · **Area:** Advanced Features · **PLANS:** Sustainable

A model calculates numbers. A **planning *process*** — a budget cycle, a monthly forecast, a
headcount review — is a sequence of *people* doing things in order: regional managers submit, finance
reviews, a director approves, then the cycle closes. **Anaplan Workflow** is the capability that
**orchestrates that human process**: it tells each contributor *which tasks they own, when they're
due, and how to complete them*, tracks status, and routes approvals — so the cycle runs on rails
instead of in someone's spreadsheet and inbox.

> ⚠️ Workflow is a platform capability layered on the New UX; availability and exact features evolve.
> *Confirm current specifics in Anapedia.*

## The building blocks

| Concept | What it is |
| --- | --- |
| **Task** | A unit of work: a title, description, one or more **assignees**, and an optional **due date**. A task may point a user at a specific page to complete. |
| **Owner** | The **Workflow Owner** administers the cycle — builds tasks and templates and launches them as running workflows. |
| **Approval step** | A task can require an **approver** who can *accept, reject, or send back* to the assignee — building review into the flow. |
| **Status** | Each task reports progress (e.g. not started / in progress / complete / approved). The owner can filter and monitor by name, status, due date, or creator. |
| **Template** | A reusable definition of a multi-step process, launched each cycle with fresh assignees and dates. |
| **Audit trail** | Timestamped status changes give a record of who did what, when — useful for governance and reporting. |

A typical budget cycle as a Workflow:

```
[Submit cost centre plan]  →  [Finance review]  →  [Director approval]  →  [Close cycle]
   owner: each manager        owner: FP&A          approver: director
   due: day 5                 due: day 8           accept / reject / send back
```

Each assignee sees only their tasks and due dates; the owner sees the whole board light up as work
completes.

## How Workflow complements DCA

This is the connection a model builder must understand. **Workflow and
[Dynamic Cell Access (DCA)](../06-security-alm/dynamic-cell-access.md) solve two halves of the same
problem** — and they're strongest together.

| | Governs… | Mechanism |
| --- | --- | --- |
| **DCA** | *Whether the cells are editable* right now | A **formula** opens/locks cells by status (e.g. editable only while status = *Draft*). |
| **Workflow** | *Who does what, and when, and the approval routing* | Assigned **tasks**, due dates, and approval steps drive people through the process. |

A status-driven cycle uses **both**:

1. A **status** line item (Draft → Submitted → Approved) lives in a [System module](../03-methodology/disco.md).
2. **DCA reads that status** to make a manager's cells editable while *Draft* and read-only once
   *Submitted* — so nobody can change a number that's already been sent up.
3. **Workflow drives the people**: it assigns "submit your plan" to each manager with a due date,
   then routes a "review & approve" task to finance, whose approval can flip the status that DCA
   keys off.

> **In short:** DCA enforces *what can be edited* at each stage; Workflow manages *who acts, in what
> order, by when*. DCA is the lock; Workflow is the checklist and the chaser. The status line item is
> the hinge they both turn on.

## When a beginner meets it

You reach for Workflow when a cycle involves **many people who must act in sequence** and **someone
has to chase them** — i.e. the moment "did everyone submit yet?" becomes a manual headache. For a
single-user or tiny model it's overkill; status flags and DCA alone are plenty.

**Sustainable (PLANS) angle:** encoding the process in Workflow means it's repeatable every cycle
from a template — not re-explained over email each month — and it leaves an audit trail. The process
survives a change of personnel the same way a good model survives a change of builder.

## Build notes

- Workflow lives in the **[New UX](../05-ux/new-ux-pages-boards.md)**; tasks can link contributors
  straight to the page where they do the work.
- Tasks can trigger or be tied to **[actions/processes](../04-integration/actions-and-processes.md)**
  (e.g. run an import when a stage completes), so process orchestration and data orchestration meet.
- Design your **status model first** (the System line item and its allowed values); Workflow and DCA
  both hang off it.

## Related

- [`docs/06-security-alm/dynamic-cell-access.md`](../06-security-alm/dynamic-cell-access.md) — the cell-locking half of status-driven cycles
- [`cookbook/security-and-dca/`](../../cookbook/security-and-dca/) — DCA-driven approval recipes
- [`docs/05-ux/new-ux-pages-boards.md`](../05-ux/new-ux-pages-boards.md) — where Workflow tasks live and link to
- [`docs/04-integration/actions-and-processes.md`](../04-integration/actions-and-processes.md) — processes a task can drive
- [`cookbook/ux-and-workflow/`](../../cookbook/ux-and-workflow/) · [DISCO — System modules](../03-methodology/disco.md) · [PLANS — Sustainable](../03-methodology/plans-standard.md)

> Source: Anaplan Workflow (Anapedia & anaplan.com —
> [Workflow](https://help.anaplan.com/workflow-d3ef84e7-e883-4b38-af79-889ea825df9f),
> [Use Workflow in the User Experience](https://help.anaplan.com/use-workflow-in-the-user-experience-f047b35f-77c2-4312-8f9f-6468599c3456),
> [Workflow owner](https://help.anaplan.com/workflow-owner-e41fa3aa-caf6-4484-a8b2-46675f0d3937),
> [Anaplan Workflow](https://www.anaplan.com/platform/anaplan-workflow/)).
> Confirm current specifics in Anapedia. See [`SOURCES.md`](../../SOURCES.md).
