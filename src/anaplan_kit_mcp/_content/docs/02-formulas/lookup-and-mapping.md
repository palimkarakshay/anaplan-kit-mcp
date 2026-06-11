# Lookup & Mapping

> **Level:** L2 · **Area:** Formulas · **PLANS:** Sustainable, Logical

This is one of the most important pages in the kit. Mapping data between lists — pulling a value
*down* to a finer dimension, or pushing it *up* to a coarser one — is the daily bread of Anaplan
modeling, and doing it the *right* way (mappings, not hard-coded item picks) is what makes a model
sustainable.

Two directions, two functions:

| You want to… | Direction | Use |
| --- | --- | --- |
| Bring **one** value from a coarser list to a finer one (e.g. each cost centre reads its region's FX rate) | pull **down** | **`LOOKUP`** |
| Roll **many** values up to a coarser list (e.g. sum all cost centres into their region) | push **up** | **`SUM`** (or `AVERAGE`/`MIN`/`MAX`/`ANY`/`ALL`) |

Both rely on a **mapping line item**: a line item (usually in a **System** module) that is
*formatted as the target list* and says, for each source item, which target it belongs to.

---

### LOOKUP

**Syntax**

```
Source.Line Item[LOOKUP: MappingLineItem]
```

**What it does**
Reads a value *from* the `Source` line item by following a mapping. The mapping line item is
formatted as the **source's** dimension and tells Anaplan which source item to fetch for each cell
of the result. In plain terms: "for this row, go look up the value belonging to *that* item."

**Example**

```
-- SYS Cost Centre.Region is formatted as the Region list (one region per cost centre)
-- FX01 Rates.Rate is dimensioned by Region
CC FX Rate = FX01 Rates.Rate[LOOKUP: SYS Cost Centre.Region]
```

Each cost centre picks up the FX rate of the region it maps to. The result is dimensioned by
**Cost Centre**; the rate lived on **Region**; the mapping bridged them.

**Watch out for**

- The mapping line item's **format must match the dimension of the source** you are looking into
  (here `Region`, because the rate is *by region*).
- A blank mapping returns blank for that cell — incomplete mappings = silent gaps.
- Anapedia advises: if a formula needs **10+ `IF THEN ELSE`s**, replace them with a `LOOKUP` and a
  mapping module. *(Performance, Auditable.)*

**Source:** https://help.anaplan.com/lookup-f8baa402-606d-4764-a349-d8003fa383be ·
examples: https://help.anaplan.com/lookup-examples-18ec86e1-8e21-4d7b-a207-cf378a001d1d

---

### SELECT

**Syntax**

```
Source.Line Item[SELECT: List.Item]
```

**What it does**
Picks **one specific, named item** from a dimension — e.g. always read the `USD` rate, or the
`Total Company` total. It hard-codes the choice into the formula.

**Example**

```
USD Rate = FX01 Rates.Rate[SELECT: Currency.USD]
```

Always returns the USD row of the rate module.

**Watch out for**
> ⚠️ **Use sparingly.** `SELECT` on a *specific list item* (e.g. `Currency.USD`,
> `Products.Widget`) is **discouraged** — it breaks the moment that item is renamed or removed, and
> it hides a business assumption inside a formula. The Planual flags this under **Sustainable**:
> drive the choice from a **mapping/System module** and use `LOOKUP` instead. `SELECT` on a
> **generic** Time member (like `SELECT: TIME.'All Periods'`) is the accepted exception.

**Source:** https://help.anaplan.com/select-2ca3148d-466e-44bd-830e-7e5cf3ac8d08

---

### SUM (as a mapping aggregator)

**Syntax**

```
Source.Line Item[SUM: MappingLineItem]
```

**What it does**
The mirror image of `LOOKUP`. Where `LOOKUP` pulls one value down, `SUM` rolls many values **up**:
it adds every source item whose mapping points at the target. See also `AVERAGE`/`MIN`/`MAX`/`ANY`/
`ALL` in [aggregation-functions.md](aggregation-functions.md).

**Example**

```
Region Cost = COST01 Cost by CC.Amount[SUM: SYS Cost Centre.Region]
```

For each region, total the `Amount` of every cost centre mapped to that region.

**Watch out for**

- The result line item **must be dimensioned by the mapping's target** (`Region`).
- The mapping line item must be **formatted as that target list** (`Region`).
- This is the direction-up partner to `LOOKUP`'s direction-down. Get the two confused and you'll
  reference a dimension you don't have.

**Source:** https://help.anaplan.com/sum-fa7ab44f-c31c-4928-88b3-9fe28ca8a774

---

### FINDITEM

**Syntax**

```
FINDITEM(List, Text)
```

**What it does**
Converts **text** into the matching **list item** (matching by the item's name, or its code for
some lists). Essential when imported data arrives as text and you need a real list reference to map
on.

**Example**

```
Country Item = FINDITEM(Countries, "US")     -- returns the Countries item named/coded "US"
Mapped Country = FINDITEM(Countries, DAT01.Country Text)
```

Turn a text country code on imported rows into an actual `Countries` list item you can `LOOKUP`/
`SUM` against.

**Watch out for**

- Returns **blank** if no item matches — no error. Pair with `ISBLANK` to catch bad data.
- The result line item must be **formatted as that list** (`Countries`).
- Match is on the item's name/code; trailing spaces or case can cause misses (clean with
  `TRIM`/`UPPER` first — see [text-functions.md](text-functions.md)).

**Source:** https://help.anaplan.com/finditem-0668e215-a0d2-4ad1-b93f-3c2a56a9f5c2

---

## Worked example: cost-centre data up to region (the SUM vs LOOKUP pattern)

A textbook setup. You import actuals **by cost centre**, but report **by region**, and each region
has a single budget you want every cost centre to see.

**1. Build a System mapping module** `SYS Cost Centre` dimensioned by `Cost Centre`:

| Line Item | Format | Formula | Purpose |
| --- | --- | --- | --- |
| `Region` | Region (list) | *(imported / typed once)* | Which region each cost centre belongs to |

**2. The Data module** `COST01 Cost by CC` dimensioned by `Cost Centre × Month`:

| Line Item | Format | Formula |
| --- | --- | --- |
| `Amount` | Number | *(imported actuals)* |

**3. The Region budget input** `BUD01 Region Budget` dimensioned by `Region × Month`:

| Line Item | Format | Formula |
| --- | --- | --- |
| `Budget` | Number | *(planner input)* |

**4. The Calculations** — now both directions in one place:

```
-- Push UP: total cost-centre actuals into each region (result dimensioned by Region × Month)
Region Actual = COST01 Cost by CC.Amount[SUM: SYS Cost Centre.Region]

-- Pull DOWN: let every cost centre see its region's budget (result dimensioned by Cost Centre × Month)
CC Region Budget = BUD01 Region Budget.Budget[LOOKUP: SYS Cost Centre.Region]
```

The mapping line item `SYS Cost Centre.Region` is used **both** ways — `SUM` rolls the cost-centre
detail up, `LOOKUP` pulls the region figure down. Add a new cost centre tomorrow, set its `Region`
once, and **no formula changes** are needed. That is the Sustainable principle in action.

> Why not `SELECT: Region.North`? Because the moment regions are renamed or a new one appears, the
> formula is wrong and someone has to hand-edit it. The mapping module absorbs that change for free.

**Related:** [aggregation-functions.md](aggregation-functions.md) ·
[hierarchy-functions.md](hierarchy-functions.md) (PARENT/ITEM for building mappings) ·
[DISCO — System modules](../03-methodology/disco.md) ·
[The Planual — avoid SELECT, use mappings](../03-methodology/planual.md)
