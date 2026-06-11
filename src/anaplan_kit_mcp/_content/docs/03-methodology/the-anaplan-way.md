# The Anaplan Way (TAW)

> **Level:** L2 · **Area:** Methodology (delivery) · This is about *how a project runs*, not how a formula is written.

Where **PLANS** governs the *model*, **The Anaplan Way** governs the *project*. It's Anaplan's
agile delivery methodology — how a team turns business needs into a deployed, adopted model. As a
new consultant you'll live inside this rhythm, so it helps to know the vocabulary.

## The phases

| Phase | What happens | Your role as a modeler |
| --- | --- | --- |
| **Foundation / Mobilise** | Define the business problem, success metrics, scope, team, environment. | Understand requirements; agree the model architecture at a high level. |
| **Model Build (sprints)** | Build the model iteratively in short sprints, demoing working software each time. | The bulk of your work — build, test, demo, refine. |
| **Deploy / UAT** | User acceptance testing, data loads, training, go-live. | Fix defects, finalise imports, support testers. |
| **Sustain / Iterate** | Hypercare then ongoing enhancement. | Maintain via ALM; add features as new stories. |

## Key concepts you'll hear

- **User stories** — requirements written as *"As a `<role>`, I want `<capability>`, so that
  `<benefit>`."* You'll estimate and build these.
- **Sprints** — short (often 1–2 week) timeboxes ending in a demo of working functionality.
- **Definition of Done** — a story isn't done until it's built, tested, and meets PLANS.
- **Model Builder vs. Solution Architect** — you (builder) implement; the architect owns the
  overall design and data architecture across models.
- **The "Connected Planning" goal** — models don't live alone; they connect (often via a **data
  hub**) so planning is consistent across finance, sales, supply chain, workforce, etc.

## How it connects to the rest of this kit

- During **Model Build**, you apply [DISCO](disco.md) and [PLANS](plans-standard.md) and reach for
  the [cookbook](../../cookbook/) when a story needs a known pattern.
- During **Deploy** and **Sustain**, you rely on [ALM](../06-security-alm/alm.md) to move changes
  from dev → test → prod safely, and on [integration](../04-integration/) to load real data.

**Related:** [PLANS](plans-standard.md) · [ALM](../06-security-alm/alm.md)

> Source: The Anaplan Way delivery methodology (Anaplan published materials / Academy). See [`SOURCES.md`](../../SOURCES.md).
