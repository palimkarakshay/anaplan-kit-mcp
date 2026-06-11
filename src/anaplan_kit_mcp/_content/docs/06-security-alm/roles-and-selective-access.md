# Roles & Selective Access

> **Level:** L2 · **Area:** Security · **PLANS:** Sustainable, Auditable · **DISCO:** System

Anaplan security answers two questions in order: **what can this user do?** (their **role**)
and **on which slice of the data?** (**selective access**). Get these two right and you've
covered most access needs before reaching [DCA](dynamic-cell-access.md).

## Users and the workspace admin

- A **user** is a person with an Anaplan login, added to a workspace.
- A **workspace administrator** manages users, models, roles and integrations for a
  workspace. Admins bypass most model-level restrictions, so keep the admin list short.
- Within a model, users are given a **role**; everything else (selective access, DCA) refines
  what that role can touch.

> Treat workspace admin like `root`. Day-to-day planners and even most builders should *not*
> be workspace admins.

## Before any of this: how users get *in* (SSO/SAML & provisioning)

Roles and selective access decide what a user can do **once they have an account** — but real
tenants hit **authentication and provisioning** first:

- **SSO via SAML.** Most enterprises front Anaplan with **single sign-on** using **SAML 2.0**,
  managed by a **tenant security administrator** against the company identity provider (IdP).
  When a workspace is assigned to an SSO connection, its users authenticate through the IdP
  rather than an Anaplan password — so the IdP also enforces password policy, MFA and access
  windows.
- **Exception users.** Keep at least one **exception user** who can still use the standard
  Anaplan login, so an IdP outage or misconfiguration can't lock everyone out.
- **Provisioning.** A person needs an Anaplan account (tenant level) **and** to be added to a
  workspace before any model role applies. Account creation/SSO is **tenant administration**;
  roles and selective access are **model** concerns. They are different layers — don't conflate
  "they can log in" with "they have the right model access".

This kit treats SSO/provisioning conceptually; the model-level controls below are where you
spend most of your day.

## Roles — what a user can do

A **role** is defined per model and bundles permissions for the model's components —
modules, lists, actions, dashboards/pages. For each, a role grants something like:

| Access level | Meaning |
| --- | --- |
| **No Access** | The component is hidden from the user |
| **Read** | Can view, cannot change |
| **Write** | Can view and edit |

You typically create roles by **persona** — e.g. `Cost Centre Manager`, `FP&A Analyst`,
`Reviewer` — and set each role's access to every module/list/action once. Assign users to
roles; never wire permissions to individuals one by one. *(Sustainable.)*

| Role | INP modules | OUT modules | Actions | Pages |
| --- | --- | --- | --- | --- |
| Cost Centre Manager | Write | Read | Run "Submit" | Entry + report |
| FP&A Analyst | Write | Write | Run loads | All |
| Reviewer | Read | Read | None | Report only |

## Selective access — which list items

A role says "this user can write to the Headcount module". **Selective access** narrows that
to "...but only for **their** cost centres". It is access controlled **by list item**.

How it works:

1. Turn on **selective access** for the list (e.g. `Cost Centre`).
2. For each user/role, grant **Read** or **Write** on specific **list items** (or
   parents, which cascade to children in a hierarchy).
3. Now every module dimensioned by that list automatically shows each user only their
   permitted items.

> **Access is driven by lists.** Because selective access attaches to *list members*, the
> list hierarchy *is* your security map. Design the list so the slices people need (by
> region, by department, by manager) fall on clean hierarchy boundaries — then access is a
> property of the structure, not a pile of exceptions. *(Sustainable.)*

### Driving access from a list — the pattern

A scalable approach is to make access a **data-driven** property rather than a manual grid:

- Hold a **mapping** (often in a **System** module or imported list properties) of *user →
  permitted items*.
- Maintain it like any other data — import it, audit it — instead of clicking through
  screens for hundreds of users.

This keeps security **auditable** (you can see who has what in a module) and **sustainable**
(add a new manager → add a mapping row, no model change).

## Where roles/selective access stop, and DCA begins

| Need | Use |
| --- | --- |
| "This persona can't see this module at all" | **Role** (No Access) |
| "This user only sees *their* cost centres" | **Selective access** (by list item) |
| "Cells are editable only while status = Draft" | **[Dynamic Cell Access](dynamic-cell-access.md)** |

Roles and selective access are **static** (set per user/role). When editability must change
**dynamically** based on the data itself — a status, a lock flag, a period — that's DCA's
job.

## Good practice

- **Roles by persona, users into roles.** Never permission individuals directly.
- **Design lists so access falls on hierarchy boundaries.** Security is a list property.
- **Drive bulk access from a mapping** you can import and audit.
- **Keep workspace admins minimal.**
- **Review access** when the org changes — it's part of keeping the model sustainable.

**Related:** [Security & ALM overview](README.md) ·
[Dynamic Cell Access](dynamic-cell-access.md) · [ALM](alm.md) ·
[DISCO — System modules](../03-methodology/disco.md) ·
[Lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md)

> Source: Anaplan security docs (`help.anaplan.com`, model roles & selective access). See
> [`SOURCES.md`](../../SOURCES.md).
