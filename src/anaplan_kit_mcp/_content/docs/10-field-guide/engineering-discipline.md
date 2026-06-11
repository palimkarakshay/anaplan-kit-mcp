# Engineering Discipline Without the Tooling

> **Level:** L3 · **Area:** Field Guide · **PLANS:** Auditable, Sustainable

Anaplan ships almost none of the engineering primitives a software team takes for granted: no
branching, no pull requests, no unit-test framework, no CI/CD, no APM. That is a platform fact you
can't change. What you *can* change is whether your team brings the **disciplines** anyway, using
in-platform mechanisms and a little process. None of this needs a vendor feature — only agreement.

Each section below: **what's missing → the workaround a team can actually run.**

---

## Version control & change tracking

**Missing:** Git-style branching, merge, history, and `git blame` on a formula. ALM is *linear* —
revision tags on a dev model synced to deployed models; you can clone a model but the clone is a
fork that can't rejoin the trunk. (See [ALM](../06-security-alm/alm.md).)

**Run instead:**

- **Treat ALM revision tags as your commits.** Tag at every meaningful, working checkpoint — not
  once a sprint. Name them consistently (`YYYY-MM-DD_sprintN_short-desc`). Keep them small and
  frequent so a "revert" means syncing the previous tag, not unpicking weeks of work.
- **Keep a change log** *inside the model* — a tiny `SYS Change Log` module (or list) with date,
  author, revision tag, what changed and why. This is the `git blame` the platform won't give you.
- **Export the blueprint to version it externally.** A model's blueprint exports as metadata
  (modules, line items, formulas as text). Commit those exports to a real Git repo on each release —
  now you have a textual, diffable history of formula changes that survives outside the tenant.
- **Coordinate the shared dev model.** Multiple builders in one dev model overwrite each other's
  structural changes. Agree a lightweight protocol: a "who's building what" board, time-boxed
  structural windows, and a rule that big structural changes are announced before they land.
- **Backups are your real rollback.** Because ALM rollback is brittle, take a dated model copy
  before any risky structural change. (Copies are workspace-quota-billable — budget for one rollback
  slot.) Restore-from-history covers data.

## Code review

**Missing:** pull requests and a reviewable formula-by-formula diff.

**Run instead:**

- **Blueprint-diff review.** Export the blueprint before and after a change and diff the text (in
  your Git repo, or any diff tool). Review *that*. It's the closest thing to a PR diff Anaplan allows.
- **Walkthrough review.** A second builder opens the module in blueprint view and walks the changed
  line items against the [model-build checklist](../03-methodology/model-build-checklist.md) and the
  [anti-patterns catalog](anti-patterns-catalog.md). Make it a standing habit, not a favour.
- **Definition of Done includes review.** No revision tag promoted to TEST without a second pair of
  eyes. Cheap, and it catches the silent-summary and nested-`IF` classes of bug.

## Testing & regression

**Missing:** xUnit, mocking (every module is statically wired), automated regression.

**Run instead:**

- **Reconciliation / control-total ("check") modules.** A `CHK` module compares calculated totals
  to source totals and raises a Boolean `Out of Balance?`. This is your assertion library — keep
  them permanently in the model, not just at build time. See
  [reconciliation & control totals](../09-troubleshooting/reconciliation-and-control-totals.md) and
  the [reconciliation-check-module recipe](../../cookbook/performance/reconciliation-check-module.md).
- **Expected-value test modules.** For critical calcs, store known inputs and the known-correct
  output in a small test module; a `Pass/Fail` line item compares live calc to expected. Run it after
  every structural change — your manual regression suite.
- **Edge-case discipline.** Blanks, divide-by-zero, brand-new list members, year/fiscal rollover,
  53-week years, sign flips. See [testing & UAT](../09-troubleshooting/testing-and-uat.md).
- **UAT is a layer, not the whole program.** "Finance ties the numbers to last month" is necessary
  but not sufficient. Pair it with the check/test modules above so a regression is caught *before* a
  board pack disagrees with itself.

## "CI" and deployment gates

**Missing:** a pipeline that validates a candidate model and refuses to promote on failure.
CloudWorks is a *scheduler*, not CI — it runs what you point it at.

**Run instead:**

- **A health-check dashboard.** A single page that surfaces every `Out of Balance?` and `Fail` flag
  across the model. Green-before-promote is your manual quality gate.
- **Scheduled validation.** Use a CloudWorks/Process chain to run import + reconciliation actions on
  a schedule and alert on failures — not true CI, but it catches broken loads early.
- **A written promotion checklist** (dev → test → prod) that a human runs every time: tag created,
  blueprint diff reviewed, check modules green, smoke test passed, backup taken.

## Observability

**Missing:** APM, distributed tracing, cross-model observability.

**Run instead:**

- **Use the in-model diagnostics that *do* exist:** the **Calculation Effort column** (shows each
  line item's % of calc effort, right in the blueprint) and **Model Open Analysis** (calc time in ms
  per module/line item). These are your profiler — learn them early. See
  [sparsity & engine](../07-performance/sparsity-and-engine.md) and
  [model size & workspace management](../09-troubleshooting/model-size-and-workspace-management.md).
- **Monitor model size deliberately** as part of routine maintenance, not after planners complain.
- **Keep a model map.** A maintained schema diagram + module index is the cross-model "trace" the
  platform won't give you. Treat the [OEG Performance Triangle](https://community.anaplan.com/discussion/140709/oeg-best-practice-anaplan-performance-triangle) framing as your mental model.

## Decisions & knowledge (beating tribal knowledge)

**Missing:** ADRs, service catalogs, and a culture that writes things down.

**Run instead:**

- **Architecture Decision Records.** Keep a short decisions log (in this repo, or a model notes
  module): *versions vs scenario list, single model vs hub-and-spoke, why this hierarchy.* The "why"
  is what the next builder — or future-you after a reorg — needs.
- **Document logic where it lives.** Line-item descriptions and a `SYS Notes` module beat a Word doc
  nobody opens. Compliance/SOX binders serve the auditor, not the next engineer — write engineer-facing notes too.
- **Don't be the single point of failure.** Tribal knowledge makes the model un-maintainable when
  you're away. Share it.

## Security hygiene a team controls

- **Least privilege, not "make them an admin."** The admin shortcut becomes next year's audit
  finding. Model roles deliberately; test the model as each persona.
- **Named service accounts + token rotation.** Don't let one human's account own half the
  integrations (they leave; everything breaks). Assign integration ownership and actually rotate API
  tokens — the platform supports it; operationalise it.
- **Make the access matrix explicit.** A System module documenting "who can see/do what" turns the
  untestable selective-access × role × DCA interaction into something inspectable. See
  [roles & selective access](../06-security-alm/roles-and-selective-access.md) and [DCA](../06-security-alm/dynamic-cell-access.md).

---

**Related:** [anti-patterns catalog](anti-patterns-catalog.md) · [platform-aware decisions](platform-strategy.md) · [ALM](../06-security-alm/alm.md) · [reconciliation & control totals](../09-troubleshooting/reconciliation-and-control-totals.md) · [testing & UAT](../09-troubleshooting/testing-and-uat.md)

> Sources: Anaplan ALM & deployed-mode docs, Calculation Effort / Model Open Analysis, and Anaplan Community OEG best practices. See [`SOURCES.md`](../../SOURCES.md).
