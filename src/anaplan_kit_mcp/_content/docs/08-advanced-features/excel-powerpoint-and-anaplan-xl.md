# Excel, PowerPoint & Anaplan XL — Office Consumption

> **Level:** L3 · **Area:** Advanced Features · **PLANS:** Logical

You build pages and boards in the [New UX](../05-ux/new-ux-pages-boards.md) — but a large share of
business users live in **Microsoft Office** and want Anaplan data *where they already work*. Anaplan
offers **Office add-ins** for exactly this: pull live, governed Anaplan numbers into Excel and
PowerPoint (and, with Excel, write back), so finance analysts and reporting teams don't have to
rebuild everything by hand or export stale CSVs.

There are two related but distinct offerings — **the native Anaplan Office add-ins** and **Anaplan
XL** — and beginners conflate them. Here's the split. *Confirm current product names, packaging, and
licensing in Anapedia, as these evolve.*

## The offerings at a glance

| Tool | What it does | Typical user | Read / write |
| --- | --- | --- | --- |
| **Anaplan for Excel** (Microsoft 365 add-in) | Pull data from Anaplan **saved views** into Excel; with the right access, **write values back** to the model. | Analysts who prefer Excel for ad-hoc analysis and data entry. | Read **and** write |
| **Anaplan for PowerPoint** (add-in) | Retrieve data from Anaplan **saved views** into PowerPoint slides; refresh decks against live model data. | People producing recurring management/board decks. | Read |
| **Anaplan XL** (formerly FluenceXL) | A richer Excel **reporting** add-in: build formatted, refreshable reports from Anaplan and other sources, with read/write back to Anaplan. | Reporting / FP&A teams building structured Excel reports and packs. | Read **and** write |

> **Saved views are the contract** for the native add-ins, just as they are for
> [model-to-model imports](data-hub-architecture.md). The add-in reads a defined view, so what an
> Office user can see/touch is governed by what the view exposes plus their Anaplan security.

## When business users prefer these

- **"Can I just get this in Excel?"** — the single most common request. Analysts are fast in Excel
  and want Anaplan numbers alongside their own working.
- **Bulk / grid-style data entry** that's quicker to key in a spreadsheet than cell-by-cell on a page
  (then written back via the Excel add-in).
- **Formatted recurring reports and board decks** — Anaplan XL for structured Excel packs; the
  PowerPoint add-in for slides that **refresh** instead of being re-pasted each month.
- **Blending Anaplan with other sources** — Anaplan XL can combine Anaplan data with other systems in
  one report. *(Confirm supported connectors in Anapedia.)*

## Governance caveats — read before you hand these out

The add-ins are powerful precisely because data leaves the platform's UI. That's the risk too.

- **Security still applies — don't assume it relaxes.** A user only sees what their roles, selective
  access, and the saved view permit. The add-ins **don't** bypass
  [roles & selective access](../06-security-alm/roles-and-selective-access.md) or
  [DCA](../06-security-alm/dynamic-cell-access.md) — but *verify* this behaves as expected for
  write-back, because a workbook in someone's inbox can outlive its context.
- **Refresh vs. snapshot.** A connected workbook is live only when refreshed; once saved and emailed
  it's a **point-in-time snapshot** that drifts from the model. Make clear which numbers are live.
- **Single source of truth.** The model stays the source of truth (**Logical** in PLANS). Office is a
  *window* onto it, not a parallel copy where new logic should grow. Resist analysts rebuilding
  calculations in Excel that belong in the model.
- **Write-back is real writes.** Excel/XL write-back changes model data — treat it with the same care
  as any input action; rely on the model's DCA/status controls to keep edits valid.
- **Versioning & support.** Add-ins are installed client software with their own versions; keep them
  current and confirm tenant compatibility.

> Rule of thumb: use the add-ins for **consumption and controlled entry**, not as a place to build
> logic. The model computes; Office reads (and, carefully, writes).

## Related

- [`docs/05-ux/`](../05-ux/) — the in-platform alternative: Pages, Boards, Worksheets
- [`docs/05-ux/new-ux-pages-boards.md`](../05-ux/new-ux-pages-boards.md) — build the views these add-ins consume
- [`docs/06-security-alm/roles-and-selective-access.md`](../06-security-alm/roles-and-selective-access.md) · [`dynamic-cell-access.md`](../06-security-alm/dynamic-cell-access.md) — the security the add-ins inherit
- [`docs/04-integration/imports-exports.md`](../04-integration/imports-exports.md) — file-based export, the lower-tech alternative
- [PLANS — Logical](../03-methodology/plans-standard.md) (single source of truth)

> Source: Anaplan Office add-ins & Anaplan XL (Anapedia & anaplan.com —
> [Anaplan for Microsoft 365](https://help.anaplan.com/anaplan-for-microsoft-365-a90600ae-7ae8-42cb-824b-25aea2069c0c),
> [Anaplan XL Reporting](https://help.anaplan.com/anaplan-xl-reporting-4fa3d997-207a-4257-aba7-e73579e4f55c),
> [Extensions](https://help.anaplan.com/extensions--cdd52a14-722b-4300-bbcf-c1638d7ee8a9),
> [Anaplan XL Reporting (anaplan.com)](https://www.anaplan.com/platform/anaplan-xl-reporting/)).
> Product names and licensing evolve; confirm current specifics in Anapedia. See [`SOURCES.md`](../../SOURCES.md).
