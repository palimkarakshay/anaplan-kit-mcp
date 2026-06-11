# Security & ALM

> **Level:** L2 · **Area:** Security / ALM · **PLANS:** Sustainable, Auditable

Two jobs every real model needs that beginners often leave until last: deciding **who can
see and change what** (security), and **how the model changes safely over time without
losing planners' data** (ALM — Application Lifecycle Management). This section covers both.

## Security — the layers

Anaplan security is layered. Each layer narrows access further than the one above:

| Layer | Controls | Page |
| --- | --- | --- |
| **Workspace / model roles** | What a user can do in a model (view, edit, admin) | [roles-and-selective-access.md](roles-and-selective-access.md) |
| **Selective access** | *Which list items* a user can see/edit within their role | [roles-and-selective-access.md](roles-and-selective-access.md) |
| **Dynamic Cell Access (DCA)** | *Which cells* are editable, read-only or hidden — dynamically, by formula | [dynamic-cell-access.md](dynamic-cell-access.md) |

Read top to bottom: a **role** says what you can do, **selective access** says which slice
of the lists you do it on, and **DCA** says which individual cells are open right now.

## ALM — the layers of change

ALM keeps **structure** (lists, modules, formulas, views) flowing safely from a development
model to the live one **without overwriting planners' data**:

| Concept | What it is | Page |
| --- | --- | --- |
| **Development vs deployed mode** | Where you change structure vs where users plan | [alm.md](alm.md) |
| **DEV → TEST → PROD** | The promotion path for changes | [alm.md](alm.md) |
| **Revisions & revision tags** | Saved snapshots of model structure to synchronize | [alm.md](alm.md) |
| **Synchronization** | Pushing structural changes from source to target | [alm.md](alm.md) |

## Map of these pages

| Page | What it covers |
| --- | --- |
| [roles-and-selective-access.md](roles-and-selective-access.md) | Workspace/model roles, selective access by list item, users & admin basics. |
| [dynamic-cell-access.md](dynamic-cell-access.md) | DCA driver modules — Boolean Read/Write line items, with a worked status-driven example. |
| [alm.md](alm.md) | Dev/deployed mode, DEV→TEST→PROD, revision tags, sync, what ALM moves and what it doesn't. |

## Why start both early

- **Security** is hard to retrofit — design lists so access can be *driven by them* from the
  beginning. *(Sustainable.)*
- **ALM** only works if you turn it on *before* the model is live; once planners are typing
  into PROD you must not break compatibility. Decide your dev/prod split on day one.

**Related:** [DISCO](../03-methodology/disco.md) · [PLANS](../03-methodology/plans-standard.md) ·
[UX](../05-ux/) · [Integration](../04-integration/) · [Learning Path](../../LEARNING-PATH.md)
