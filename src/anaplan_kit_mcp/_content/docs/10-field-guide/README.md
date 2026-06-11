# 10 · Field Guide — Anti-patterns & Surviving the Real World

> **Level:** L2–L3 · **Area:** Field Guide · **PLANS:** all five

The rest of this kit teaches you how to build *well*. This section is about what actually goes
**wrong** on real projects — and, most importantly, **what you (a new model builder) or your team can
actually do about it.**

> **Scope of this guide.** It deliberately covers *only* problems that are **in scope for an
> individual builder or a team** — things you can fix at the keyboard or institute as team habits.
> Wider ecosystem realities that no developer can action (vendor product strategy, ownership/PE,
> licensing pricing, the services market, acquisition timing) are **out of scope** — being annoyed
> at them is wasted energy. Where a platform reality *does* change a decision you make, we cover the
> decision, not the politics.

This is deliberately unsentimental. Anaplan is a capable platform (Hyperblock and Polaris are both
strong calc engines). But there's a wide gap between how Anaplan teams work and how a mature
software-engineering team works. Knowing that gap early makes you a better builder than peers who
learn it by accident over years.

## Two buckets you can act on: control and influence

When you hit a problem, sort it honestly — and only spend energy on the first two:

| Bucket | What it means | Your move |
| --- | --- | --- |
| **Control** | Your own modeling choices. | Fix it. This is the [anti-patterns catalog](anti-patterns-catalog.md). |
| **Influence** | Team/process habits the platform doesn't give you for free (review, testing, change tracking, observability). | Bring the discipline yourself — see [engineering discipline without the tooling](engineering-discipline.md). |
| *Accept (not covered here)* | Vendor/ownership/licensing/market realities. | Out of your hands. The only in-scope slice is *"a platform fact changed my technical decision"* — that's in [platform-aware decisions](platform-strategy.md). |

Most new builders waste energy being frustrated by the "accept" bucket and neglect the "control"
bucket — where all their actual leverage is.

## Pages

- **[anti-patterns-catalog.md](anti-patterns-catalog.md)** — the keyboard- and architecture-level
  anti-patterns, each with *symptom → why it happens → the fix → where in this kit to learn it.*
  Start here; this is the part you control completely.
- **[engineering-discipline.md](engineering-discipline.md)** — how to get version-control habits,
  code review, testing, "CI", and observability on a platform that ships none of them as primitives.
  This is the **team-level (influence)** playbook.
- **[platform-strategy.md](platform-strategy.md)** — *platform-aware decisions*: the handful of
  platform realities (which calc engine, which API/integration tool, which UX, how big the model can
  get, where to find answers) that should change a **decision you actually make**. In-scope only —
  no vendor/market commentary you can't action.

## The one idea to take away

**Most anti-patterns are a corner cut under delivery pressure.** When the incentive is to ship fast
and small, the quick path is tempting — but recognise that incentive and choose the
[PLANS](../03-methodology/plans-standard.md)-compliant path anyway, because you'll be the one
maintaining it (or explaining it to the next builder) long after the deadline is forgotten.

**Related:** [PLANS](../03-methodology/plans-standard.md) · [DISCO](../03-methodology/disco.md) · [The Planual](../03-methodology/planual.md) · [Performance](../07-performance/) · [Troubleshooting](../09-troubleshooting/)
