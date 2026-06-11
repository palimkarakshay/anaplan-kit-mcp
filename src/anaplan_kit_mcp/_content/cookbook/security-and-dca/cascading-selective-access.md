# Cascading selective access (managers see only their branch)

> **Level:** L3 · **Area:** Security & DCA · **PLANS:** Logical, Sustainable · **DISCO:** System

## The ask

"A regional manager should see and edit only the cost centres under their region — not the whole company. And it should cascade: give them the region and they automatically get everything beneath it."

## When you'll see this

- Each user should only see their slice of a hierarchy.
- Access that should follow the tree (grant a parent, get the descendants).
- Multi-entity models where data is sensitive across branches.

## Approach

Use **Selective Access** on the hierarchy list. When you enable selective access on a list, you grant each user access to specific items; because Anaplan understands the hierarchy, granting a **parent** cascades read/write to its **descendants**. Combined with role-based module access, a manager opening a shared page sees only their branch.

For logic that must respect the same boundary (filters, allocations limited to a branch), pair selective access with an `ISANCESTOR`-based Boolean (see [item-parent-ancestor-rollup](../hierarchies-and-lists/item-parent-ancestor-rollup.md)).

Why idiomatic:

- **Sustainable (PLANS):** access follows the hierarchy; add a cost centre under a region and the region's manager gets it automatically.
- **Logical:** the security model mirrors the org structure.

## Blueprint

**Selective access setup (on the `Cost Centre` / `Region` hierarchy):**

| User | Granted item | Effect (cascade) |
| --- | --- | --- |
| Region Mgr North | `Region.North` | sees/edits all cost centres under North |
| Region Mgr South | `Region.South` | sees/edits all cost centres under South |
| CFO | `Company` (top) | sees everything |

**`SYS40 Cost Centre Hierarchy`** — branch test for logic that must match access:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Region | List: Region | None | Cost Centre | `PARENT(ITEM(Cost Centre))` |
| In My Branch? | Boolean | None | Cost Centre | `ISANCESTOR(USERS.selected region, ITEM(Cost Centre))` *(via a user-context module)* |

## Formula(s)

Selective access itself is **configuration** (granting items to users), not a formula — set it on the list and assign access per user/role.

For *logic* that must respect the same branch (e.g. a calc or filter limited to the user's region), use `ISANCESTOR` against the granted region:

```
// SYS40 Cost Centre Hierarchy -> In My Branch?
ISANCESTOR(SYS User Context.Region, ITEM(Cost Centre))
```

where `SYS User Context` is a module dimensioned by `Users` holding each user's region (often itself set by selective access / an admin import). Read it as "is the user's region an ancestor of this cost centre?".

## Pitfalls / gotchas

- **Cascade direction:** granting a parent gives the descendants. Granting a leaf gives only that leaf. Grant at the level you want the user's *root* to be.
- **Selective access vs DCA:** selective access controls *which list items* a user sees at all; DCA controls *which cells* within visible items are editable. They stack — use both for "see your branch, but it's locked after submit".
- **Performance:** selective access on a very large list with many users has overhead — design the hierarchy so grants are at sensible roll-up levels, not thousands of individual leaf grants.
- **Totals can leak or look wrong:** a user with partial access sees roll-ups computed only over what they can see. Be clear with stakeholders about what a parent total means under selective access.
- Don't rebuild security in formulas — selective access is the platform feature; `ISANCESTOR` is only for *logic* that must align with it, not a replacement.

## Performance & PLANS notes

- Hierarchy-driven access is **Sustainable**: org changes flow through automatically, no per-user re-grant for every new cost centre.
- Granting at roll-up levels (region, not leaf) keeps the access configuration small and fast.
- Pairs naturally with a [context-selector dashboard](../ux-and-workflow/context-selector-dashboard.md) — the selector only offers items the user can see.

## Related

- [`docs/06-security-alm/`](../../docs/06-security-alm/)
- Recipes: [dca-read-write-by-status](dca-read-write-by-status.md) · [hide-or-lock-by-role](hide-or-lock-by-role.md) · [item-parent-ancestor-rollup](../hierarchies-and-lists/item-parent-ancestor-rollup.md) · [context-selector-dashboard](../ux-and-workflow/context-selector-dashboard.md)
