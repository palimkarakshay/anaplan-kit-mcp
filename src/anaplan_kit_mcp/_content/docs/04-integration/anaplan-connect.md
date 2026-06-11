# Anaplan Connect

> **Level:** L3 · **Area:** Integration · **PLANS:** Sustainable

**Anaplan Connect** is Anaplan's free **command-line integration client**. It is a small Java
program you run on your own machine or server. You give it credentials and a list of
operations — "upload this file, run this import, run this export, download this file" — and
it talks to the [Anaplan REST API](rest-api.md) for you so you don't have to write that code
yourself.

Think of it as a thin, supported wrapper around the API, packaged for people who live in
**scripts and schedulers** rather than in Python.

## What it's good at

- **Scripted file loads and extracts.** Upload a CSV, run an import action (or a
  [process](actions-and-processes.md)), and check the result — all from one shell script.
- **Scheduled, unattended runs.** Drop the script into **cron** (Linux/macOS) or **Windows
  Task Scheduler** and Anaplan Connect runs the nightly load with no human present.
- **File-based integration on a server you control.** The classic pattern: an ETL job drops
  a file on a server, a cron job runs Anaplan Connect to load it.

## What a script looks like (conceptually)

You don't write API calls — you write a few command-line options. A load script reads,
roughly:

```bash
# Illustrative — flags and exact syntax vary by Anaplan Connect version.
./AnaplanConnect.sh \
  -workspace   "<workspaceId>" \
  -model       "<modelId>" \
  -file        "Actuals.csv"       -put ./Actuals.csv \
  -import      "IMP Load Actuals"  -execute \
  -output      ./load_result.txt
```

That single invocation does what would otherwise be several REST calls: upload the file in
chunks, trigger the named import, poll the task to completion, and write back the result.
Authentication is supplied via username/password or, preferably, a **certificate** (see
[REST API auth](rest-api.md#authentication)).

> ⚠️ **Never hard-code a password in a checked-in script.** Use certificate auth or read
> credentials from a protected environment variable / secrets store. *(Sustainable, and
> basic security hygiene.)*

## Where it fits vs CloudWorks vs the REST API

These three are *alternative runners* for the same model-side [actions](actions-and-processes.md).
Pick by where the work should live:

| You want… | Use | Why |
| --- | --- | --- |
| A scheduled load driven from **a server / file share you manage** | **Anaplan Connect** | Runs anywhere Java runs; pairs with cron / Task Scheduler |
| A **cloud-native** schedule with **no server to maintain**, pulling from S3 / GCS / Azure | **[CloudWorks](cloudworks.md)** | Managed by Anaplan; connects to cloud storage |
| **Custom orchestration** embedded in your own application or data pipeline | **[REST API](rest-api.md)** | Full control; this kit's [`tooling/`](../../tooling/) implements it in Python |

Rule of thumb: **CloudWorks if it can do the job** (least to maintain), **Anaplan Connect**
when the data lives on your own infrastructure and you already have a scheduler, and the
**REST API** when you need logic neither of the above gives you.

## Practical notes

- It's **file-and-action oriented** — it moves files and runs actions; it does not design
  your imports. Build and test the import/process in the model first, then point Anaplan
  Connect at it by name.
- Keep the **action names stable**; the script references them by name, so renaming an
  action in the model breaks the script. *(Sustainable)*
- Capture the **output/log file** every run and alert on failures — an unattended load that
  silently fails is worse than no load.

**Related:** [Actions & Processes](actions-and-processes.md) ·
[CloudWorks](cloudworks.md) · [REST API](rest-api.md) ·
[Python tooling](../../tooling/) · [Integration overview](README.md)

> Source: Anaplan Connect docs (`help.anaplan.com`, Anaplan Connect section). See
> [`SOURCES.md`](../../SOURCES.md).
