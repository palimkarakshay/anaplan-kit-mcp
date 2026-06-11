# CloudWorks

> **Level:** L3 · **Area:** Integration · **PLANS:** Sustainable

**CloudWorks** is Anaplan's **cloud-based scheduling and integration** service. Instead of
running a script on a server you maintain ([Anaplan Connect](anaplan-connect.md)) or writing
your own code ([REST API](rest-api.md)), you configure integrations in a web UI and Anaplan
runs them in the cloud — no server, no cron job, nothing to patch.

It's managed by **Integration administrators**; you can also grant restricted integration
users the right to run CloudWorks integrations within their assigned workspaces.

## The three building blocks

| Concept | What it is |
| --- | --- |
| **Connection** | A saved, reusable link to a cloud data source — **AWS S3**, **Google Cloud Storage**, or **Azure Blob Storage** (flat files), plus supported cloud data warehouses |
| **Integration** | A single move: a file in the connected storage ↔ an Anaplan [import or export action](actions-and-processes.md) |
| **Integration flow** | An **ordered sequence** of integrations that run one after another — the cloud equivalent of an Anaplan [process](actions-and-processes.md) spanning steps |

You first create a **connection** (credentials to your cloud storage), then build
**integrations** on top of it, then optionally chain them into a **flow**.

## Scheduling

CloudWorks runs integrations and flows on a schedule you set:

- **Frequency:** hourly, daily, weekly, or monthly.
- **Window:** a time zone, a start/end date, and an execution time. Scheduled starts have a
  short tolerance window, so stagger jobs rather than firing many at the exact same minute.
- **Notifications:** alert on success / failure so an unattended load that breaks gets
  noticed.

This is the big draw: a recurring load with **nothing for you to host or keep running**.

## A typical setup

```
Connection:   "Prod S3 - finance-landing"   (AWS S3 bucket)
Integration:  S3 file "actuals.csv"  →  IMP Load Actuals (Data Hub)
Flow:         1. Load Cost Centre list
              2. Load Account list
              3. Load Actuals          (the integration above)
Schedule:     Daily, 02:00 Europe/London, email on failure
```

Your ETL writes `actuals.csv` to the S3 bucket each night; CloudWorks picks it up and runs
the flow into the [Data Hub](README.md). Spoke models then pull from the hub.

## When to use CloudWorks

Reach for CloudWorks when:

- Your source data already lives in (or can be dropped into) **cloud storage** — S3, GCS,
  Azure Blob.
- You want **scheduling without owning infrastructure** — no server, no cron, no Java
  runtime to keep alive.
- You need to **chain steps** (lists then data) reliably in the cloud via an integration
  flow.
- Integration ownership should sit with **administrators in a UI**, not with developers in
  code.

Prefer [Anaplan Connect](anaplan-connect.md) instead when the data lives on **your own
infrastructure** and you already have a scheduler there; prefer the [REST API](rest-api.md)
when you need **custom orchestration** that CloudWorks can't express.

> **One mental model for all three:** they are different *runners* for the same model-side
> [actions and processes](actions-and-processes.md). Build and test the action in the model
> first; choose the runner second.

**Related:** [Actions & Processes](actions-and-processes.md) ·
[Anaplan Connect](anaplan-connect.md) · [REST API](rest-api.md) ·
[Integration overview / Data Hub](README.md)

> Source: Anaplan CloudWorks docs (`help.anaplan.com`, CloudWorks section). See
> [`SOURCES.md`](../../SOURCES.md).
