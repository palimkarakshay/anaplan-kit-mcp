# Testing & UAT

> **Level:** L2 · **Area:** Troubleshooting · **PLANS:** Auditable, Sustainable

There is no "compile and run" in Anaplan — you build live in a browser, and the only way to know a
model is right is to **test it deliberately**. Beginners skip this and find out at month-end, in
front of the business, that a formula breaks on a blank or a new product. This page is how to test
a build before anyone trusts it: test data, edge cases, regression, and a real **UAT** with users,
tied to The Anaplan Way's **Definition of Done**.

---

## The layers of testing

Test from the inside out — cheap checks first, business sign-off last:

| Layer | What you're proving | Who |
| --- | --- | --- |
| **Formula / unit** | Each calculation gives the right number for known inputs | Builder |
| **Edge cases** | It survives blanks, zeros, new members, rollover | Builder |
| **Reconciliation** | Totals tie to the source / GL | Builder |
| **Regression** | A change didn't break something that worked | Builder |
| **UAT** | The business agrees it does what they asked | Users |

The first three are covered by [reconciliation & control totals](reconciliation-and-control-totals.md).
This page focuses on edge cases, regression, and UAT.

---

## Use realistic test data

Toy data ("100, 200, 300") hides bugs. Test with data that looks like the real thing:

- **Real shape and scale** — a representative slice of the actual list sizes and value ranges.
- **Known-good totals** — a source total you can reconcile against (so you can *prove* right, not
  just *look* right). See [control totals](reconciliation-and-control-totals.md).
- **Deliberately messy rows** — a blank, a zero, a negative, a brand-new code — so you see how the
  model handles them *before* production does.

---

## Edge cases a new builder must check

These are the ones that pass in the demo and fail in the real world:

| Edge case | What breaks | What to verify |
| --- | --- | --- |
| **Blank / empty cells** | `IF` on blank, division returning errors, blanks treated as zero | Formula handles blank explicitly; `IF Driver = 0 THEN 0 ELSE ...` guards divides |
| **Divide by zero** | Ratio line items error or show huge numbers | Every division has a zero-denominator guard |
| **New list member** | New product/entity loads but has no mapping, drops out of totals | Adding a member needs **no formula change**; it appears in every relevant module *(Sustainable)* |
| **Year rollover** | Hard-coded `IF Time = Jan 25` logic, or a too-tight Time Range with no cells next year | No hard-coded dates; Time Ranges roll or are widened before rollover |
| **Fiscal year start ≠ calendar** | Aggregations land in the wrong year; YTD resets on the wrong month | Time settings use the fiscal calendar; YTD/`YEARVALUE` respect it |
| **Leap year / 53-week / short period** | Daily or weekly rates assume 365/52; Feb 29 or week 53 throws counts off | Period-length logic derives from Time, not a constant |
| **Negative / sign-flipped values** | A `SUM` or `ABS` hides a wrong sign | Check a known negative flows through with the right sign |
| **Top-of-list / empty list** | A `FIRSTNONBLANK`/`LOOKUP` with nothing to find | Verify behaviour when the list is empty or the lookup misses |

> **The rollover test is the one beginners forget.** Set your test clock forward (or reason
> through next year) and ask: *does every forward-looking module still have cells, and does any
> formula reference "this year" by a hard-coded date?* If yes, it breaks in January. *(Sustainable.)*

---

## Regression testing after a change

The most dangerous moment is editing a model that already works. A change to one line item can
ripple anywhere the engine recalculates.

**A simple, repeatable approach:**

1. **Capture a baseline.** Before changing anything, export the key output totals (or screenshot a
   reconciliation board). This is your "known good".
2. **Make the change.**
3. **Re-run the same exports / reconciliation.** Diff against the baseline. *Only the numbers you
   intended to change should have changed.*
4. **Walk your control totals** — they should all still be green.
5. If something else moved, you found a regression — trace it before shipping.

> The cheapest regression net is a **reconciliation/check module that's already there**: if a
> change knocks something out of balance, the Boolean flips red the moment you save. That's why
> the [control-total habit](reconciliation-and-control-totals.md) pays off twice.

---

## A simple test-script approach

You don't need a heavy tool — a **table** is enough. Keep it next to the build (a notes module, a
shared sheet, or this repo's templates):

| # | Test | Input / setup | Expected result | Pass? | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Revenue ties to GL | Load May actuals | `Out of Balance? = FALSE` | | |
| 2 | New product appears everywhere | Add `P999` to list | Shows in P&L, allocation, output | | |
| 3 | Blank driver doesn't error | Clear a growth rate | Result = 0, no error | | |
| 4 | Year rollover | Advance to next FY | Forward modules have cells; no hard-coded dates | | |
| 5 | Divide-by-zero guard | Set denominator to 0 | Ratio = 0, not error | | |

Re-run the **same script** after every significant change — that *is* your regression suite.

---

## UAT with business users

User Acceptance Testing is the business confirming the model does what *they* asked — not what you
think they asked.

- **Test against the user stories**, one by one. Each story should have an observable pass/fail.
- **Let users drive** with their own scenarios and data — they'll try things you didn't.
- **Reconcile to a number they already trust** (last month's reported figure). Tying to a known
  result builds confidence faster than any explanation.
- **Log issues** with severity; fix, then **re-test the fix and regression-test around it**.
- Watch for **scope creep** — capture new asks as new stories, don't silently absorb them.

---

## Tie to The Anaplan Way — "Definition of Done"

The Anaplan Way runs delivery in sprints, and a story isn't "done" because the formula saves. A
practical **Definition of Done** for a model builder:

- [ ] Built to the **user story** — no more, no less (no scope creep).
- [ ] **Edge cases** checked: blanks, zeros, new members, year/fiscal rollover.
- [ ] **Reconciles** to source/GL — control totals green.
- [ ] **Regression**-tested — only intended numbers changed.
- [ ] **UAT signed off** by the business owner.
- [ ] Passes the [Model-Build Checklist](../03-methodology/model-build-checklist.md) (PLANS + DISCO).
- [ ] Key assumptions **documented** (line-item descriptions / notes).
- [ ] Production-bound work is under **ALM** and promotable via revision.

If any box is unticked, it isn't done — it's "works on my screen".

**Related:** [reconciliation-and-control-totals.md](reconciliation-and-control-totals.md) ·
[common-errors-and-fixes.md](common-errors-and-fixes.md) ·
[Model-Build Checklist](../03-methodology/model-build-checklist.md) ·
[PLANS](../03-methodology/plans-standard.md) ·
[The Anaplan Way](../03-methodology/the-anaplan-way.md) ·
[ALM](../06-security-alm/alm.md)

> Source: The Anaplan Way & Anaplan testing best-practice — `help.anaplan.com` & Anaplan
> Community. See [`SOURCES.md`](../../SOURCES.md).
