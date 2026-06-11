# Actions & Processes

> **Level:** L2 · **Area:** Integration · **PLANS:** Sustainable, Auditable · **DISCO:** Data

An **action** is a named, reusable thing the model can *do* — load a file, write out a
file, empty a list. A **process** is an ordered group of actions you run as one unit. You
build both once in the browser; afterwards a user clicks a button or a script calls them.
This page is the bridge between [imports & exports](imports-exports.md) (what an import
*is*) and the runners ([Anaplan Connect](anaplan-connect.md), [CloudWorks](cloudworks.md),
[REST API](rest-api.md)) that fire them on a schedule.

## Action types

When you create an action, Anaplan saves it under the model's **Actions** area. The types a
beginner meets:

| Action type | What it does | Typical use |
| --- | --- | --- |
| **Import** | Loads data or list members from a file / saved view into a target | Load actuals; add new cost centres |
| **Export** | Writes a saved view out to a file (CSV, XLSX, etc.) | Send the plan to a warehouse |
| **Delete from list using selection** | Removes list members flagged by a Boolean selection | Clear last period's transactional rows |
| **Open dashboard / page** | Navigates the user to a named dashboard or UX page | Button on a workflow card |
| **Clear / reset** | (Within imports) clears data in scope before loading | Wipe-and-reload patterns |

> **Delete by selection, not by hand.** A *delete from list using selection* action deletes
> the members where a Boolean line item is `TRUE`. You drive that Boolean from a System
> module, so the delete is repeatable and auditable — never hand-delete transactional rows.

## Processes — ordered groups of actions

A **process** runs a sequence of actions **in order**, top to bottom, as a single
operation. This is how you express a real-world load that takes several steps.

Classic example — a monthly actuals refresh:

```
Process: "Monthly Actuals Load"
  1. Import  →  update Cost Centre list      (structural: lists first)
  2. Import  →  update Account list          (structural)
  3. Import  →  load Actuals into DAT01       (data)
  4. Export  →  reconciliation check view     (optional verification)
```

Why processes matter:

- **Order is guaranteed.** Lists are built before data lands against them — the *lists
  first, data second* rule from [imports-exports.md](imports-exports.md) enforced for you.
- **One thing to run.** Users (and schedulers) trigger one process, not six fiddly
  actions in the right order. *(Sustainable)*
- **One audit trail.** The process result shows each step's success / ignored / failed
  counts together. *(Auditable)*

> Build the individual actions, test each one, *then* assemble them into a process. A
> process is only as reliable as its weakest action.

## How actions get run

The same action object can be triggered four ways — define once, run many ways:

| Runner | Who/what triggers it | When you'd use it |
| --- | --- | --- |
| **A user, in the UX** | A button on a page or dashboard | Planner-initiated loads, "Submit" workflows |
| **[Anaplan Connect](anaplan-connect.md)** | A script on a server, scheduled via cron / Task Scheduler | Nightly file-based loads |
| **[CloudWorks](cloudworks.md)** | Cloud scheduler + cloud storage connection | Cloud-native, no server to maintain |
| **[REST API](rest-api.md)** | Your own code (e.g. the [`tooling/`](../../tooling/) package) | Custom orchestration, embedding in a pipeline |

A button in the UX is just an action (often a process) surfaced as something a planner can
click. The runner doesn't change the action — it changes *who pulls the trigger*.

## Good practice

- **Name actions for what they do**, prefixed so they sort sensibly: `IMP Load Actuals`,
  `EXP P&L to Warehouse`, `DEL Clear Transactions`. *(Auditable, Sustainable)*
- **Keep structural and data imports as separate actions**, then sequence them in a
  process — don't try to do both in one.
- **Test the process end to end** with a representative file before scheduling it.
- **Read the process result** every run; treat ignored rows as a defect.

**Related:** [Imports & Exports](imports-exports.md) ·
[Anaplan Connect](anaplan-connect.md) · [CloudWorks](cloudworks.md) ·
[REST API](rest-api.md) · [Integration overview](README.md) ·
[DISCO](../03-methodology/disco.md)

> Source: Anaplan actions & processes docs (`help.anaplan.com`, Data Integrations /
> Build a model sections). See [`SOURCES.md`](../../SOURCES.md).
