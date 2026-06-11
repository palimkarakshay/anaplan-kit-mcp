# Imports & Exports

> **Level:** L1 · **Area:** Integration · **PLANS:** Sustainable, Necessary · **DISCO:** Data

An **import** loads data from a source (a file or another Anaplan view) into a target in
your model. An **export** writes data out of a view to a file. You build them once in the
browser, Anaplan saves the **mapping**, and from then on the import is a reusable
**action** you (or a script) can re-run against a fresh source of the same shape.

## The two kinds of import

This is the distinction that trips up every beginner. Imports do *two different jobs*:

| Import type | What it changes | Example |
| --- | --- | --- |
| **Data import** | The numbers/values inside a **module** | Load this month's actuals into `DAT01 Actuals` |
| **Structural (list) import** | The **members** of a **list** | Add new products/cost centres to a list; update their properties |

A data import never adds list members on its own *unless you ask it to* (see
[auto-create](#auto-create-list-members)). A list import never fills a module with numbers
— it builds the dimension first. A typical "new product launch" load is therefore **two
actions**: first import the product into the **list**, then import its numbers into the
**module**. Grouping them is exactly what a [process](actions-and-processes.md) is for.

> **Rule of thumb:** lists first, data second. You cannot load a number against a product
> that doesn't exist yet.

## Sources you can import from

- **A flat file** — CSV, TXT or a fixed-width text file you upload. Anaplan stores the
  uploaded file so the action can be re-run by replacing the file with one of the same
  layout.
- **A saved view of another module** — the basis of **model-to-model** imports and the
  heart of a [Data Hub](README.md). The "file" is really a live view in another model.

A **saved view** is just a module view (rows/columns/filters/selected line items) that you
named and saved. It can be the **source** of an import *and* the thing you point an
**export** at. Shaping a clean `OUT`-type output view for export is far better than
exporting a raw calc module.

> The two source types map to the two main **import data source** kinds: an uploaded **file
> source** (the action remembers the file and you replace its content each run) versus a
> **model-to-model** source (a saved view in another model — the Data Hub pattern, no file
> involved). [Connectors / CloudWorks](README.md) add managed sources (e.g. cloud storage,
> databases) on top, but conceptually they still land as one of these two.

## File and chunk size (beginner snags)

Anaplan moves files in **chunks**, and the sizes matter:

- **Uploads are chunked.** Large files are split into pieces (a few MB to ~50 MB each) and
  uploaded part by part, then marked complete — this is what makes big, reliable loads
  possible. In the browser this is automatic; via the [REST API](rest-api.md) you control the
  chunk count/size (this kit's tooling defaults to ~10 MB chunks).
- **Exports come back chunked too** — you reassemble the pieces into the output file.
- **Watch the row/cell volume, not just the byte size.** A load that's a small file can still
  be a *large* number of cells to write; size loads to land in a flat `D` module, not to fan
  out across a wide calc module mid-import.
- Keep the **source layout stable** — re-running an action expects the same columns. A changed
  header or column order is a classic silent breakage.

## Export formats: Grid vs Tabular

When you build an export, you choose how the view is laid out in the file — and beginners
often pick the wrong one:

| Format | Shape | Use when |
| --- | --- | --- |
| **Grid** | The view exactly as shown — line items across columns, a pivoted grid | A human will read it, or you need the on-screen layout |
| **Tabular Multiple Column** | **Normalised** rows: dimension keys in columns, one value column per line item — one row per intersection | **Feeding another system or model** — it's the import-friendly shape |

For **integration** (model-to-model, Data Hub, downstream systems) prefer **Tabular Multiple
Column**: a normalised, code-keyed table imports cleanly. Reserve **Grid** for reports a person
opens. Exporting a pivoted Grid into another system's importer is a common first-time mistake.

## Mapping: matching source columns to your model

When you build an import, Anaplan shows a **mapping** screen. You tell it how each source
column lines up with the target's **dimensions** and **line items**:

| Source column | Maps to | Notes |
| --- | --- | --- |
| `Cost Centre Code` | the **Cost Centre** list dimension | match on code or name |
| `Month` | the **Time** dimension | source format must be parseable |
| `Account` | another list dimension | |
| `Amount` | a **line item** | the actual value |

Key mapping ideas for a beginner:

- **Match on code, not name, where you can.** Codes are stable; names get retyped.
- Columns that identify *where* a number sits map to **dimensions**; the column holding the
  *value* maps to a **line item**.
- Anaplan tries to auto-match by header name. Always check it — a silent mis-map is the
  classic "the totals look wrong" bug.
- Map a **Version** explicitly if your module is versioned (e.g. load into `Actual`).

## Updating data vs updating lists

Say it out loud before every import: *am I updating data or updating the list?*

- **Updating data** overwrites/loads values in a module. It does **not** remove list
  members that are missing from the file — it just doesn't update them.
- **Updating a list** changes the dimension itself: adding members, updating their
  properties/parents, or (if configured) removing members not present in the source.

Mixing these up is how people accidentally wipe planning numbers or, worse, delete list
members. Keep them in separate actions and you keep them straight.

## Auto-create list members

A data import can be told to **create list members on the fly**: if the source has a
product code the target list doesn't contain yet, Anaplan adds it. This is convenient but
**use it deliberately** — it's the most common cause of a list quietly bloating with junk
members (typos, blanks, retired codes) that inflate cell count forever.

Preferred pattern: **import the list cleanly first** (its own structural action, often into
a Data Hub), validated, *then* import data with auto-create **off**. Reserve auto-create
for genuinely dynamic transactional lists where the hub is the gatekeeper.

## Common import pitfalls

| Pitfall | Symptom | Fix |
| --- | --- | --- |
| Matching on **name** not **code** | rows silently skipped when a name changed | map on a stable code |
| **Auto-create** left on | list fills with typo'd / blank members | clean list import first, auto-create off |
| Wrong **Version** mapped | numbers land in `Forecast` instead of `Actual` | map the Version column explicitly |
| **Time** format mismatch | dates won't parse, rows ignored | match source date format to the model calendar |
| Importing into a **calc** line item | values won't stick (formula overwrites them) | import into input line items / `DAT` modules only |
| Exporting a raw calc module | messy, fragile file | export a purpose-built `OUT` saved view |
| Ignoring the **import log** | think it worked; half the rows failed | always read the "rows successful / ignored / failed" summary |

> **Always read the import results dialog.** It tells you how many rows succeeded, were
> ignored, or failed, and why. Treat ignored rows as a bug until proven otherwise.

## Where this fits in DISCO and PLANS

- Land raw imports in a flat **D (Data)** module, faithful to the source. Don't calculate
  in it. *(Logical)*
- Don't import the same file into many models — load it once into a **Data Hub** and feed
  spokes from there. *(Necessary, Sustainable)*
- Keep import mappings driven by stable codes and saved views, not ad-hoc layouts, so the
  load survives next month's file. *(Sustainable)*

**Related:** [Actions & Processes](actions-and-processes.md) ·
[Integration overview / Data Hub](README.md) ·
[DISCO](../03-methodology/disco.md) ·
[Lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md) ·
[REST API](rest-api.md)

> Source: Anaplan import/export & data integration docs (`help.anaplan.com`, Data
> Integrations section). See [`SOURCES.md`](../../SOURCES.md).
