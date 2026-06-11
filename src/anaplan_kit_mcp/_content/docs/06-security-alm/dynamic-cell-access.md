# Dynamic Cell Access (DCA)

> **Level:** L3 · **Area:** Security · **PLANS:** Sustainable, Logical · **DISCO:** System

[Roles and selective access](roles-and-selective-access.md) decide what a user can do and on
which list items — but they're **static**. **Dynamic Cell Access (DCA)** controls
editability at the **cell level**, **by formula**, so cells open and lock automatically as
the data changes — for example, "this cell is editable only while the plan status is
*Draft*". Once it's *Submitted*, the same cell goes read-only for everyone, with no manual
intervention.

## How DCA works

DCA is driven by an **access driver module** — a dedicated [System](../03-methodology/disco.md)
module holding **Boolean** line items:

- A **Read access driver** — `TRUE` where the target cells should be **visible**.
- A **Write access driver** — `TRUE` where the target cells should be **editable**.

You then point the target module (or specific line items) at these drivers via its
**Read Access Driver** and **Write Access Driver** settings in Blueprint. The driver
controls whether each cell is **editable** or **read-only**, and whether its value is
**readable** at all.

| Driver value | Read driver | Write driver | Result for the cell |
| --- | --- | --- | --- |
| Editable | TRUE | TRUE | User can see **and** edit |
| Read-only | TRUE | FALSE | User can see, cannot edit |
| Not readable | FALSE | (n/a) | Cell is **blanked / not readable** for the user |

> **A Read driver of `FALSE` doesn't remove the cell from the page.** It makes the cell's
> value **not readable** (it shows blank, and isn't editable), but the row/column still exists
> in the layout. To *hide* something structurally — drop a module, line item or dimension from
> what a user sees — use **roles** (No Access) or the **page/view design**, not DCA. DCA
> governs *readability and editability of cells*, not page layout.

> The driver module must share the **dimensionality** you want to control by. To lock cells
> *by cost centre and time*, the driver is dimensioned by Cost Centre × Time. You can apply a
> driver at **module level** (one row) or per **line item** for fine control. You can even
> include the **Users** list to vary access per person.

## Worked example — status-driven editing

**Requirement:** planners may edit the headcount plan **only while the plan is in Draft**.
Once a cost centre's plan is **Submitted**, its cells lock.

### Step 1 — a status input

A small [Input](../03-methodology/disco.md) module, `INP00 Plan Status`, dimensioned by
**Cost Centre**, holds the current status:

| Line Item | Format | Applies to | Notes |
| --- | --- | --- | --- |
| `Status` | List: `Plan Status` (`Draft`, `Submitted`) | Cost Centre | Set by reviewer / workflow |

### Step 2 — the access driver module (a blueprint)

`SYS09 Headcount DCA` — a **System** module, **Boolean**, dimensioned to match the target
(Cost Centre, here at module level):

| Line Item | Format | Applies to | Summary | Formula |
| --- | --- | --- | --- | --- |
| `Can Read` | Boolean | Cost Centre | None | `TRUE` |
| `Can Write` | Boolean | Cost Centre | None | `INP00 Plan Status.Status = Plan Status.Draft` |

`Can Write` is `TRUE` exactly where the status is `Draft`. (Comparing to the list item via a
mapping/property rather than typing the word keeps it [Sustainable](../03-methodology/plans-standard.md).)

### Step 3 — wire it to the target

On the headcount input module's Blueprint, set:

- **Read Access Driver** → `SYS09 Headcount DCA.Can Read`
- **Write Access Driver** → `SYS09 Headcount DCA.Can Write`

### Result

- While a cost centre is `Draft`: cells are **editable**.
- The moment it's `Submitted`: `Can Write` flips to `FALSE`, and those cells become
  **read-only** on every page and grid — no rebuild, no re-permissioning. *(Sustainable.)*

```
Plan Status.Status = Draft      →  Can Write = TRUE   →  cells editable
Plan Status.Status = Submitted  →  Can Write = FALSE  →  cells read-only
```

## Why DCA, not IF or roles

- **Roles/selective access can't do "while Draft"** — they don't change with the data. DCA
  does. *(Logical.)*
- **Don't fake it with `IF`** inside calc formulas — that controls *values*, not
  *editability*, and bloats your calc logic. A Boolean driver controls editability cleanly
  and is faster. *(Performance, Auditable.)*
- Drivers live in **System** modules, visible and reusable — the same `SYS09` can drive
  several targets. *(Necessary, Sustainable.)*

## Good practice

- Put drivers in a clearly named **System** module (`SYS… DCA`), not scattered in calc
  modules.
- Keep drivers **Boolean and simple** — one expression per driver; reference, don't repeat.
- Match the driver's **dimensionality** to the granularity you need (module-level vs
  line-item-level vs per-user).
- Combine with [selective access](roles-and-selective-access.md): selective access for
  *which items*, DCA for *which cells, when*.

**Related:** [Roles & Selective Access](roles-and-selective-access.md) ·
[Security & ALM overview](README.md) · [DISCO — System modules](../03-methodology/disco.md) ·
[Booleans over IF — optimization](../07-performance/optimization-checklist.md) ·
cookbook security & DCA recipes (`cookbook/security-and-dca/`)

> Source: Anaplan Dynamic Cell Access & access drivers docs (`help.anaplan.com`). See
> [`SOURCES.md`](../../SOURCES.md).
