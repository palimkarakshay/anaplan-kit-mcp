# Hide or lock by role (roles + DCA together)

> **Level:** L3 · **Area:** Security & DCA · **PLANS:** Logical, Sustainable · **DISCO:** System

## The ask

"Planners can edit the assumptions, reviewers can only look, and admins can see the hidden reconciliation tabs. Same model, different experience per role."

## When you'll see this

- Different user roles need different edit rights and different visible content.
- "Read-only for most, editable for some" on the same module.
- Hiding admin/diagnostic content from regular users.

## Approach

Anaplan layers three controls — use the right one for each job:

1. **Roles** — control which **modules/pages** a user can open and broad read/write at the model level.
2. **Selective access** — which **list items** a user sees (see [cascading-selective-access](cascading-selective-access.md)).
3. **DCA** — which **cells** are editable, driven by a Boolean that can itself depend on role.

To vary editability by role *within* a visible module, drive a DCA Boolean from a **role flag** held in a `SYS Users` module. Pages/modules a role shouldn't see at all are handled by **role access**, not DCA.

```
Write Access driver = user's role is "Planner"
```

Why idiomatic:

- **Logical (PLANS):** each control does one job — roles for visibility, DCA for cell editability.
- **Sustainable:** role flags are data; reassign a user's role and access follows.

## Blueprint

**`SYS Users`** — role attributes, `Applies To` Users:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Is Planner? | Boolean | None | Users | *(import from role / admin input)* |
| Is Reviewer? | Boolean | None | Users | *(import)* |
| Is Admin? | Boolean | None | Users | *(import)* |

**`SYS80 DCA Drivers`** — editability, dimensioned to match the target and including Users:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Writable? | Boolean | None | Users, Cost Centre, Time | `SYS Users.Is Planner?` |

**Target `INP Budget`**: Write Access → `SYS80 DCA Drivers.Writable?`. Admin-only diagnostic modules: restrict via **role access** (don't even publish them to other roles).

## Formula(s)

Editable only for planners (a role-driven DCA Boolean):

```
// SYS80 DCA Drivers -> Writable?
SYS Users.Is Planner?
```

Combine role with status and period for a complete rule:

```
// SYS80 DCA Drivers -> Writable?  (planner AND draft AND open period)
SYS Users.Is Planner?
AND (INP80 Approval.Status = Status.Draft OR INP80 Approval.Status = Status.Rejected)
AND NOT SYS01 Time Settings.Is Actual?
```

Hiding whole tabs from non-admins is **role configuration** (don't grant the page), not a formula — DCA can't hide a module, only restrict its cells.

## Pitfalls / gotchas

- **DCA can't grant beyond the role.** If a role has no write access to a module, DCA can't make a cell writable. DCA only *restricts further* within what the role already allows.
- **To truly hide content, use roles**, not DCA — a DCA read-lock blanks cells but the module/page still exists. Admin-only modules simply shouldn't be in other roles' page access.
- **The DCA driver needs the Users dimension** (or to be evaluated in user context) to vary by who's logged in — a driver without a user dimension can't differ per role.
- Maintaining role Booleans by hand drifts — **import them from the role assignment** so they stay in sync.
- Layer order matters: roles → selective access → DCA. Debug top-down (can they open the page? see the item? edit the cell?).

## Performance & PLANS notes

- One `SYS Users` role module feeds every DCA driver — **Necessary** + **Sustainable**.
- Use the cheapest control that does the job: hide with roles (no calc cost), lock cells with DCA Booleans (cheap).
- Keep diagnostic/reconciliation modules in an **admin-only** role so they don't clutter or worry regular users — they still cost memory, but not confusion.

## Related

- [`docs/06-security-alm/`](../../docs/06-security-alm/)
- [`docs/06-security-alm/dynamic-cell-access.md`](../../docs/06-security-alm/dynamic-cell-access.md)
- Recipes: [dca-read-write-by-status](dca-read-write-by-status.md) · [cascading-selective-access](cascading-selective-access.md) · [input-vs-report-pages](../ux-and-workflow/input-vs-report-pages.md)
