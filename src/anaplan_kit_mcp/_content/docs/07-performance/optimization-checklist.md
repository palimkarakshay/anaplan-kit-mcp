# Optimization Checklist

> **Level:** L3 · **Area:** Performance · **PLANS:** Performance, Necessary, Auditable

A concrete **do / don't** list for keeping models fast. Each item is a **PLANS-Performance**
action — most also help Auditability, because fast formulas and clean formulas are usually
the same thing. Keep this page open while you build and use it as a review pass before you
ship.

## 1. Right-size dimensionality first

The biggest win, every time — see [cell count](sparsity-and-engine.md).

- **Do** dimension a module only by the lists it **truly needs**. Every extra dimension
  *multiplies* cell count.
- **Do** use [subsets](line-item-subsets.md) to dimension by a *portion* of a big list.
- **Do** use [Time Ranges](time-ranges.md) so modules span only the periods they need.
- **Don't** add a Version / Region / level "just in case" — that's the most expensive habit
  in Anaplan. *(Performance, Necessary.)*

## 2. Avoid `IF` on large cell counts — use Booleans

- **Do** compute a condition **once** as a **Boolean** line item, then reference it.
- **Do** multiply by a Boolean (`value * Boolean`) or use it as a driver where it reads
  clearly.
- **Don't** scatter `IF … THEN … ELSE` across millions of cells and many formulas — it's
  slow and hard to audit.

```
# Avoid — IF evaluated over the whole big module, repeated everywhere
Bonus = IF Status = "Active" AND Region = "EU" THEN Base * Rate ELSE 0

# Prefer — decide once in a Boolean, then reference it
Eligible? (Boolean) = Status = Statuses.Active AND IsEU?         # computed once
Bonus               = Base * Rate * Eligible?                    # cheap, clear
```

*(Performance, Auditable.)*

## 3. Prefer SUM / LOOKUP mapping over nested LOOKUP

- **Do** map with a single `SUM` (aggregate up a mapping) or a single `LOOKUP` (read across
  a mapping), driven by a **System** mapping module.
- **Don't** chain `LOOKUP` inside `LOOKUP` inside `LOOKUP` — each layer is work and the
  formula becomes unreadable.
- **Don't** use `SELECT: List.SpecificItem` to dodge mapping — it breaks when the list
  changes. Map instead. *(Sustainable, Auditable.)*

## 4. Calculate once, then reference

- **Do** put each logical step in its **own line item** and reference it downstream.
- **Don't** repeat the same sub-expression in five formulas — that's the same maths computed
  five times.
- **Bonus:** stepped line items recalc only the steps that changed and are far easier to
  debug. *(Performance, Auditable, Necessary.)*

## 5. Minimise text formulas

- **Do** keep text in a few **System** line items; store **codes** and look up the text once.
- **Do** prefer numeric / Boolean operations — they're cheaper than string manipulation.
- **Don't** build `TEXT` / concatenation logic across large modules, or recompute the same
  label in many places. *(Performance, Necessary.)*

## 6. Use Time Ranges and subsets deliberately

- **Do** assign the **tightest [Time Range](time-ranges.md)** each module needs.
- **Do** size by **[subsets](line-item-subsets.md)** (list and line item) instead of full
  lists where only a portion is used.
- **Don't** confuse **hiding** with **removing** — a filtered view still has the cells. Only
  a Time Range / subset actually shrinks the module. *(Performance.)*

## 7. Avoid unnecessary subsidiary views

A **subsidiary view** is created when a line item has *different* dimensionality from its
module (e.g. one line item dimensioned by Time when the module isn't). They have their place,
but each is effectively a hidden extra grid.

- **Do** keep a module's line items on the **same dimensionality** where you can.
- **Do** move a line item that genuinely needs different dimensions into its **own module**.
- **Don't** let subsidiary views proliferate unnoticed — they add cells and hide
  dimensionality from anyone reading the blueprint. *(Performance, Auditable.)*

## 8. Shape outputs, don't over-calc in them

- **Do** build lean **Output (O)** views for [UX cards](../05-ux/new-ux-pages-boards.md) and
  [exports](../04-integration/imports-exports.md) — select and arrange, don't recompute.
- **Don't** point a page card at a giant raw calc module. *(Performance.)*

## The 60-second review pass

Before shipping a module, walk this list:

- [ ] Every **dimension** is necessary; none added "just in case". *(P, N)*
- [ ] **Time Range** is the tightest correct span. *(P)*
- [ ] Big-cell conditions are **Booleans**, not nested `IF`. *(P, A)*
- [ ] Mapping uses **single SUM/LOOKUP**, not nested lookups or `SELECT`. *(P, S)*
- [ ] Each step is **calculated once** and referenced. *(P, A, N)*
- [ ] **Text** logic is minimal and centralised. *(P, N)*
- [ ] No stray **subsidiary views**; odd-dimensioned line items live in their own module. *(P, A)*
- [ ] **Subsets** used where only a portion of a list applies. *(P, N)*

**Related:** [Performance overview](README.md) ·
[Sparsity & cell count](sparsity-and-engine.md) · [Time Ranges](time-ranges.md) ·
[Line item subsets](line-item-subsets.md) ·
[PLANS — Performance](../03-methodology/plans-standard.md) ·
[The Planual](../03-methodology/planual.md)

> Source: Anaplan performance best-practice materials & The Planual (`help.anaplan.com` &
> Anaplan Community). See [`SOURCES.md`](../../SOURCES.md).
