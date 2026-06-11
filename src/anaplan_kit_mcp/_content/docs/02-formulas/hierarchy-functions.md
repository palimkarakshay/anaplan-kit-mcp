# Hierarchy Functions

> **Level:** L2 · **Area:** Formulas

Hierarchy functions navigate **lists and their structure** — "which item am I?", "what's my
parent?", "is X above Y?", "what level am I at?". They return **list items** or **Booleans/numbers**
and are the backbone of building mappings and roll-up logic.

A mental model: every cell of a list-dimensioned module *knows which list item it sits on*.
`ITEM(List)` hands you that item, and the rest of these functions walk up/down the hierarchy from
there.

---

### ITEM

**Syntax**

```
ITEM(List)
```

**What it does**
Returns the **current list item** for the cell being calculated — the item on that row of the
dimension. The key to "am I this item?" tests and to building self-referential logic.

**Example**

```
Is HQ Cost Centre? = ITEM(Cost Centre) = Cost Centre.'HQ'
Own Name           = NAME(ITEM(Cost Centre))
```

The first asks, for each cost-centre row, "is this row the HQ item?"

**Watch out for**

- `ITEM(List)` only works if the module **is dimensioned by** that list.
- Comparing `ITEM(...)` to a hard-coded item name is acceptable for a one-off, but for recurring
  logic drive it from a System flag instead. *(Sustainable.)*

**Source:** https://help.anaplan.com/item-41298b7a-e877-40e8-8cfa-8d7009d8686f

---

### PARENT

**Syntax**

```
PARENT(Child item)
```

**What it does**
Returns the **immediate parent** of a list item (or time period) — one level up the hierarchy.
Returns a value of the same data type as the child, but at the parent's level.

**Example**

```
CC Region = PARENT(ITEM(Cost Centre))     -- if Region is the parent list of Cost Centre
```

Gives each cost centre its region item — a quick way to build a mapping when the hierarchy already
encodes the relationship.

**Watch out for**

- Result is **formatted as the parent list** — your line item must match that format.
- `PARENT` goes **exactly one** level up. For "two levels up", chain it (`PARENT(PARENT(item))`) or
  build a SYS mapping line item — see *Reaching ancestors and children* below.

**Source:** https://help.anaplan.com/parent-1cdc486d-c4d7-42db-8b1a-d9e12c060999

---

### ISANCESTOR

**Syntax**

```
ISANCESTOR(Item1, Item2)
```

**What it does**
Returns a **Boolean**: TRUE if `Item1` is an ancestor of `Item2` (its parent, grandparent, and so
on). Great for "does this detail row belong under that node?" tests across composite hierarchies.

**Example**

```
Under Selected Node? = ISANCESTOR(Selected Region, ITEM(Cost Centre))
```

TRUE for every cost centre that sits beneath the chosen region.

**Watch out for**

- Returns a **Boolean** — use it directly, no `IF … THEN TRUE` wrapper.
- Order matters: `ISANCESTOR(ancestor, descendant)`. Swapping the arguments inverts the test.

**Source:** https://help.anaplan.com/isancestor-2c35cf1b-9392-4726-8ebb-4291d1b24225

---

### ITEMLEVEL

**Syntax**

```
ITEMLEVEL(Item, ROOT)     -- count of items from the item up to its root, inclusive
ITEMLEVEL(Item, LEAF)     -- count of items from the item down to its furthest descendant, inclusive
```

**What it does**
Returns a **number**: a count of items along a hierarchy from the given item, either up toward the
root (`ROOT`) or down toward its deepest leaf (`LEAF`), counting the item itself. It does **not**
return a Boolean and does not, on its own, give a single "level index" of the classic kind.

**Example**

```
Depth To Root  = ITEMLEVEL(ITEM(Cost Centre), ROOT)   -- 1 at the top, larger further down
Depth To Leaf  = ITEMLEVEL(ITEM(Cost Centre), LEAF)   -- 1 at a leaf, larger higher up
```

A clean leaf test follows from the `LEAF` direction — a leaf has no descendants below it:

```
Is Leaf? = ITEMLEVEL(ITEM(Cost Centre), LEAF) = 1     -- Boolean: true only for bottom-level items
```

Note `Is Leaf?` is the **comparison** `= 1`; `ITEMLEVEL(...)` by itself is a number, so a Boolean
line item cannot take the bare function.

**Watch out for**

- `ITEMLEVEL` is **only available in the Polaris calculation engine** — it is not in Classic. If you
  are on Classic, derive leaf status another way (e.g. flag items that have no children via a SYS
  module).
- The result is a **count (Number)**, not a Boolean or a fixed level label. A blank item returns 0.

**Source:** https://help.anaplan.com/itemlevel-756d1428-5f1d-4d79-8274-d075a1bd312f

---

### FIRSTNONBLANK

**Syntax**

```
Values to search[FIRSTNONBLANK: Mapping]
```

**What it does**
An **aggregation** function: returns the **first non-blank** value found for each target item
(across the mapped source, in list/time order). The natural way to grab "the first value that
exists" — e.g. the first month a product had sales. Returns a value matching the source's type.

**Example**

```
First Active Region = SYS Cost Centre.Region[FIRSTNONBLANK: SYS Cost Centre.Division]
```

For each division, the first non-blank region among its cost centres.

**Watch out for**

- The containing line item must be **dimensioned by all of the mapping's dimensions**.
- "First" follows the **order of the list/time dimension** — make sure that order means what you
  think.
- It is the default aggregation method for text/date/list line items in `MOVINGSUM`/`TIMESUM`.

**Source:** https://help.anaplan.com/firstnonblank-125738aa-c067-4602-b5bb-da6f4dfe940c

---

## Reaching ancestors and children

There is **no `ANCESTOR()` and no `CHILDREN()` formula function** in the Anaplan model formula
language. (Those names exist only in Anaplan XL's MDX, not in module formulas.) To do what they
suggest, use the built-in patterns instead:

- **A higher ancestor (more than one level up).** Chain `PARENT`: `PARENT(PARENT(ITEM(List)))` for
  the grandparent, and so on — or, more sustainably for a fixed target level, build a **SYS mapping
  module** line item (formatted as the target list) that records each item's ancestor once, and
  reference that.
- **Aggregating children.** You rarely need an explicit "children" function: a line item's
  **Summary method = Sum** already rolls children up their own hierarchy **automatically**. When you
  must aggregate across a *different* list, use `SUM` with a **mapping line item**
  (`Source.LI[SUM: Mapping]`) — see [aggregation-functions.md](aggregation-functions.md).

---

## The "am I this item?" pattern (and why ITEM beats SELECT)

A recurring need: do something only for a particular item, or build a mapping from the hierarchy.

```
-- Build a Cost Centre -> Region mapping straight from the hierarchy (no manual table):
CC Region        = PARENT(ITEM(Cost Centre))

-- Treat one item specially, sustainably (compare ITEM, don't SELECT a value):
Apply HQ Overhead? = ITEM(Cost Centre) = Cost Centre.'HQ'
```

Using `ITEM`/`PARENT` (chained where you need a higher level) keeps the logic **driven by
structure**, so adding members or re-parenting the hierarchy needs no formula change — far more
sustainable than `SELECT`ing a specific item (see [lookup-and-mapping.md](lookup-and-mapping.md)).

**Related:** [lookup-and-mapping.md](lookup-and-mapping.md) (hierarchy-built mappings feed
LOOKUP/SUM) · [aggregation-functions.md](aggregation-functions.md) (ANY/ALL/FIRSTNONBLANK) ·
[DISCO — System modules](../03-methodology/disco.md) · [cheatsheet.md](cheatsheet.md)
