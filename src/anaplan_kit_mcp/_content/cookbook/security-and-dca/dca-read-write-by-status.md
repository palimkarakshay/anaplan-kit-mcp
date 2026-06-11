# DCA: read/write by status (lock after submit)

> **Level:** L3 · **Area:** Security & DCA · **PLANS:** Logical, Sustainable · **DISCO:** System

## The ask

"Once a cost-centre owner submits their budget, they shouldn't be able to change it. Before submit it's editable; after submit it's read-only — driven by the approval status, not by me locking it manually."

## When you'll see this

- Lock cells after a submit/approve step in a workflow.
- Make a module editable only in certain states (open period, draft status).
- Any "soft lock" that depends on data rather than role.

## Approach

**Dynamic Cell Access (DCA)** lets a **Boolean driver line item** control, per cell, whether users can **write** (and optionally **read**). You point a target module's *Read Access* and/or *Write Access* at a Boolean in a driver module. Drive that Boolean from the **status** (see [approval-status-workflow](../ux-and-workflow/approval-status-workflow.md)): writable while Draft/Rejected, locked once Submitted/Approved.

```
Write Access driver = NOT (Submitted OR Approved)
```

The driver module must have **matching (or compatible) dimensionality** with the target so each target cell finds its access flag.

Why idiomatic:

- **Sustainable (PLANS):** locking follows the data (status), so it's automatic and consistent — no manual cell protection.
- **Logical:** access logic lives in one System driver module, referenced by the target.

## Blueprint

**`INP80 Approval`** — status per cost centre (from the workflow recipe):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Status | List: Status | None | Cost Centre | *(set by action)* |

**`SYS80 DCA Drivers`** — the access Booleans, dimensioned to match the target (Cost Centre × Time):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Writable? | Boolean | None | Cost Centre, Time | `INP80 Approval.Status = Status.Draft OR INP80 Approval.Status = Status.Rejected` |
| Readable? | Boolean | None | Cost Centre, Time | `TRUE` |

**Target module `INP Budget`** (Cost Centre × Time): set **Write Access** → `SYS80 DCA Drivers.Writable?`, **Read Access** → `SYS80 DCA Drivers.Readable?`.

## Formula(s)

Writable only in editable states:

```
// SYS80 DCA Drivers -> Writable?
INP80 Approval.Status = Status.Draft OR INP80 Approval.Status = Status.Rejected
```

Combine status with an "open period" rule so closed months also lock (reuse `Is Actual?` from [actual-forecast-switchover](../time-and-forecasting/actual-forecast-switchover.md)):

```
// SYS80 DCA Drivers -> Writable?  (status AND period open)
(Status = Status.Draft OR Status = Status.Rejected)
AND NOT SYS01 Time Settings.Is Actual?
```

Then in the **target module's** Blueprint, assign the driver line items to Read Access / Write Access. DCA is configured in the UI — the *logic* is the Boolean, the *wiring* is the access assignment.

## Pitfalls / gotchas

- **Driver dimensionality must align with the target.** If the target is Cost Centre × Time, the driver Boolean should be (at least) Cost Centre × Time, or access won't resolve per cell as expected.
- **DCA write-lock is per-line-item-assignment.** You assign Read/Write Access on the *target* line items; forgetting one leaves a hole.
- **DCA vs roles vs selective access:** DCA is data-driven cell access on top of role/selective access. It can only *restrict* further — it can't grant access a user's role doesn't already have. See [hide-or-lock-by-role](hide-or-lock-by-role.md).
- A read-locked cell shows blank to the user — make sure that's intended (often you lock **write**, keep **read**).
- Status set by free typing can be changed back to Draft to unlock — set status via **actions** and gate by role so the lock can't be trivially bypassed.

## Performance & PLANS notes

- One System driver module feeds DCA for many target modules — **Necessary** + **Sustainable**.
- Boolean drivers are cheap; DCA itself doesn't add heavy calculation.
- Keeping access logic in data (status, period flags) means the model self-locks as the cycle progresses — no manual intervention at close.

## Related

- [`docs/06-security-alm/dynamic-cell-access.md`](../../docs/06-security-alm/dynamic-cell-access.md)
- Recipes: [approval-status-workflow](../ux-and-workflow/approval-status-workflow.md) · [hide-or-lock-by-role](hide-or-lock-by-role.md) · [cascading-selective-access](cascading-selective-access.md) · [actual-forecast-switchover](../time-and-forecasting/actual-forecast-switchover.md)
