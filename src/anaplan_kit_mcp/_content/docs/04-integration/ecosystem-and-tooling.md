# The Anaplan Tooling Ecosystem

> **Level:** L3 · **Area:** Integration · **PLANS:** Sustainable, Performance

The other pages in this section teach you *one* runner at a time —
[Anaplan Connect](anaplan-connect.md), [CloudWorks](cloudworks.md), the
[REST API](rest-api.md). This page zooms out: a map of **every official Anaplan API**, the
**official tooling**, the **open-source client landscape**, and the emerging **MCP / AI
tooling** — so that when someone says "integrate with Anaplan," you know which lane to pick
and which wheel *not* to reinvent. Verified June 2026; the ecosystem moves, so confirm
versions and endpoints against the linked sources.

## Official Anaplan APIs — the full matrix

All of these share the same front door: you authenticate against
`https://auth.anaplan.com/token/authenticate` and receive a short-lived token (sent as
`AnaplanAuthToken`, not `Bearer` — see [REST API → Authentication](rest-api.md)). Three auth
modes exist across the platform:

| Auth mode | How | Notes |
| --- | --- | --- |
| **Basic** | Email + password | Simplest; fine for learning, weakest for production. |
| **Certificate** | S/MIME certificate (PEM) | Service-account style; no password rotation pain. |
| **OAuth 2.0** | Registered OAuth client | **Preferred** for production; *required* by CloudWorks. |

With auth out of the way, the APIs themselves:

| API | What it does | Base URL | Notes |
| --- | --- | --- | --- |
| **Integration API v2 — Bulk** | Imports, exports, processes; chunked file upload/download. The workhorse covered in [rest-api.md](rest-api.md). | `https://api.anaplan.com/2/0` | What Anaplan Connect and CloudWorks call under the hood. |
| **Integration API v2 — Transactional** | Cell-level read/write and model metadata: dimensions, line items, lists. | `https://api.anaplan.com/2/0` (same base) | Real-time, no file-and-task machinery; for *small* volumes. |
| **CloudWorks API** | Drive the Anaplan-native iPaaS scheduler programmatically: manage connections and integrations. | `https://api.cloudworks.anaplan.com` | **OAuth 2.0 required.** See [cloudworks.md](cloudworks.md). |
| **SCIM API** | User/group provisioning from an identity provider (standard SCIM 2.0). | `https://api.anaplan.com/scim/1/0/v2` | Uses a dedicated API key, not the normal token flow. |
| **Audit API** | Stream audit events (logins, model changes) into a SIEM. | `https://audit.anaplan.com/audit/api/1/` | Security/compliance teams' lane. |
| **ALM API** | Promote model revisions dev → test → prod programmatically. | (under the Integration API base) | **Professional/Enterprise editions only.** |

Where to read the official word:

- Anapedia API index — https://help.anaplan.com/anaplan-api-844c6d40-a21c-423d-8435-ebaaa0372b76
- Apiary interactive reference — https://anaplan.docs.apiary.io

## Official tooling

- **Anaplan Connect** — the supported Java CLI for scripted imports/exports, covered in
  [anaplan-connect.md](anaplan-connect.md). It derives from Anaplan's open-source Java
  client, https://github.com/anaplaninc/anaplan-java-client — useful to know if you ever
  need to debug what Connect actually sends.
- **anaplan-mulesoft** (https://github.com/anaplaninc/anaplan-mulesoft) — the MuleSoft
  connector is **deprecated**. Do not start new builds on it.

## Open-source Python clients — honest comparison

If you are writing your own integration code in Python, you almost certainly should *not*
hand-roll HTTP calls. The landscape, as of June 2026:

| Client | Repo | Status (Jun 2026) | API coverage | Auth modes | Verdict |
| --- | --- | --- | --- | --- | --- |
| **anaplan-sdk** (VinzenzKlass) | https://github.com/VinzenzKlass/anaplan-sdk | **Actively maintained** — v0.5.16, May 2026 | Bulk + Transactional + ALM + CloudWorks + Audit; sync **and** async | Basic, Certificate, OAuth 2.0 | **Recommended for production.** |
| **apapi** (DLZaan) | https://github.com/DLZaan/apapi | Beta — v0.6.0, Jul 2025 | Broad but beta | Basic, Certificate | Watch, don't bet on. |
| **anaplan-api** (jeswils-ap) | https://github.com/jeswils-ap/anaplan-api | v0.3.4, Oct 2024; less active | Bulk only | Basic, Certificate | Superseded by anaplan-sdk. |
| **This kit's [`tooling/`](../../tooling/)** | (this repo) | Maintained with the course | Bulk basics (auth, files, actions, metadata) | Basic | **Learning-grade.** Built so the exercises have a small, readable client to study — for production integrations, use anaplan-sdk. |

There is **no dedicated JavaScript/TypeScript client library** — JS/TS integrations call
the REST API over raw HTTP.

## MCP / AI tooling

The Model Context Protocol (MCP) lets AI assistants call tools — and Anaplan now has a
small but real MCP corner:

- **larasrinath/anaplan-mcp** — https://github.com/larasrinath/anaplan-mcp — a TypeScript
  MCP server exposing roughly **70 tools** over the Integration API v2 (Bulk +
  Transactional), with OAuth device-grant, certificate and basic auth. v1.2.0, Feb 2026. As
  of June 2026 it is the **only live-API Anaplan MCP server**.
- **This kit's own MCP server** — offline *knowledge* tools (no Anaplan tenant needed),
  built from this kit's reference content; see the kit's [`tooling/`](../../tooling/) docs.

The two are complementary: one drives a real tenant, the other answers model-building
questions offline.

## Calculation engines: Classic (Hyperblock) vs Polaris

Not an API, but an ecosystem fact that shapes every integration and model-design decision
*(PLANS: Performance)*:

- **Classic (Hyperblock)** — the original engine. **Dense**: every cell in every
  dimensional intersection is materialised, so model size grows multiplicatively with
  dimensionality. This is why the [performance section](../07-performance/) drills sparsity
  so hard — in Classic, *you* engineer the sparsity out (subsets, smaller modules, DISCO
  separation).
- **Polaris** — generally available since ~2022. **Natively sparse**: only populated
  intersections cost space, so very high-dimensional, very sparse use cases (think
  SKU × customer × channel) that are impossible in Classic become feasible. Same formula
  syntax, with **minor behavioural differences** — formulas are not blindly portable.
- The choice is **workspace-exclusive** (a workspace is one engine or the other), and
  **migration is not self-serve** — moving a model between engines is a project run with
  Anaplan, not a toggle.

Design implication: on Classic you optimise *against* density (the habits this kit
teaches); on Polaris you trade that for new cost rules where calculation complexity, not
cell count, dominates. Official docs:

- Polaris calculation engine — https://help.anaplan.com/polaris-calculation-engine-8b466778-42b2-4e35-b318-e5e4128b63b7
- Anaplan calculation engines — https://help.anaplan.com/anaplan-calculation-engines-06c06ade-2807-4f3d-9a6e-d69ae0e257e5

## Best-practice grounding

Everything in this kit traces back to two public wells:

- **The Planual** — Anaplan's official model-building rulebook (the PLANS framework, with
  numbered rules) — https://support.anaplan.com/planual-5731dc37-317a-49fa-a5ff-7fc3926972de
- **Anaplan Community** — best-practice articles, OEG posts, forums — https://community.anaplan.com

When this kit and the Planual disagree, the Planual wins — file an issue here.

**Related:** [REST API](rest-api.md) · [Anaplan Connect](anaplan-connect.md) ·
[CloudWorks](cloudworks.md) ·
[Platform strategy](../10-field-guide/platform-strategy.md) ·
[Performance](../07-performance/) · [Sources](../../SOURCES.md)
