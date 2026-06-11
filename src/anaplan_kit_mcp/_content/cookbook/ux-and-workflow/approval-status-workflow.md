# Approval status workflow

> **Level:** L2 · **Area:** UX & Workflow · **PLANS:** Logical, Sustainable · **DISCO:** Inputs / System

## The ask

"Cost-centre owners submit their budget, then their manager approves or rejects it. I need a simple status — Draft / Submitted / Approved / Rejected — that drives what people can edit and shows where everything stands."

## When you'll see this

- Submit-and-approve cycles (budgets, forecasts, headcount plans).
- A status that gates editability and triggers downstream behaviour.
- A dashboard showing approval progress across many cost centres.

## Approach

Model the status as a **list-formatted line item** over a small `Status` list, driven by buttons that run **imports/actions** to set it. The status then powers everything else: [DCA](../security-and-dca/dca-read-write-by-status.md) locks cells after submit, filters show "what's outstanding", and roll-ups count approvals.

The clean version separates: a `Status` **list** (the allowed states), a status **line item** per cost centre (the current state), and **actions** that move the status (Submit, Approve, Reject) — usually small imports from a one-cell source.

Why idiomatic:

- **Logical (PLANS):** status is data, states are a list — auditable and filterable.
- **Sustainable:** add a state or change the flow without rewriting formulas.

## Blueprint

**List `Status`:** `Draft`, `Submitted`, `Approved`, `Rejected` (ordered).

**`INP80 Approval`** — `Applies To` Cost Centre:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Status | List: Status | None | Cost Centre | *(set by action; default Draft)* |
| Submitted? | Boolean | None | Cost Centre | `Status = Status.Submitted OR Status = Status.Approved` |
| Locked for Edit? | Boolean | None | Cost Centre | `Status = Status.Submitted OR Status = Status.Approved` |
| Approver Comment | Text | None | Cost Centre | *(input)* |

**`OUT20 Approval Tracker`** — counts for a dashboard:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Count Approved | Number | Sum | Cost Centre | `IF Status = Status.Approved THEN 1 ELSE 0` |
| Count Outstanding | Number | Sum | Cost Centre | `IF Status = Status.Draft OR Status = Status.Rejected THEN 1 ELSE 0` |

## Formula(s)

Derive convenience Booleans from the status (used by DCA and filters):

```
// INP80 Approval -> Locked for Edit?
Status = Status.Submitted OR Status = Status.Approved
```

Count for the tracker:

```
// OUT20 Approval Tracker -> Count Approved
IF Status = Status.Approved THEN 1 ELSE 0
```

The status *transitions* are **actions**, not formulas. A "Submit" button runs a small import that writes `Status.Submitted` into the selected cost centre's `Status` line item. Restrict who can press which button via roles/page access.

## Pitfalls / gotchas

- **Use a `Status` list, not free text or a Boolean.** Text invites typos; one Boolean can't express four states. A list keeps states valid and orderable.
- **Comparing to list items** (`Status = Status.Approved`) is fine — it's a small fixed list (not a *Sustainable* violation like `SELECT` on a big data list).
- **Don't let the same person submit and approve** unless intended — gate the Approve action by role/selective access.
- A rejected item should return to an **editable** state (Draft/Rejected) — make sure `Locked for Edit?` reflects that.
- Setting status via action means you can **audit** who changed it and when; avoid letting users free-type the status field directly if you need control.

## Performance & PLANS notes

- One small status line item drives DCA, filters and counts — calculate-once, reuse (**Necessary**).
- The status list is tiny; the convenience Booleans are cheap and keep downstream logic simple/Auditable.
- Pair with DCA so the status doesn't just *display* lock state but actually **enforces** it.

## Related

- [`docs/05-ux/`](../../docs/05-ux/)
- [`docs/06-security-alm/dynamic-cell-access.md`](../../docs/06-security-alm/dynamic-cell-access.md)
- Recipes: [dca-read-write-by-status](../security-and-dca/dca-read-write-by-status.md) · [input-vs-report-pages](input-vs-report-pages.md) · [context-selector-dashboard](context-selector-dashboard.md)
