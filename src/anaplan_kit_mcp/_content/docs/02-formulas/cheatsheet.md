# Formula Cheat Sheet

> **Level:** L1 · **Area:** Formulas

Every function in this reference, one line each — terse "what it does" + minimal syntax. For full
examples, watch-outs and sources, follow the category links. Square brackets `[ ]` mark **optional**
arguments.

> Validation: signatures cross-checked against Anapedia. See [`../../SOURCES.md`](../../SOURCES.md).

---

## Aggregation — [aggregation-functions.md](aggregation-functions.md)

| Function | What it does | Minimal syntax |
| --- | --- | --- |
| `SUM` | Roll values up to a target via a mapping | `Source.LI[SUM: Mapping]` |
| `AVERAGE` | Mean of mapped values | `Source.LI[AVERAGE: Mapping]` |
| `MIN` | Smallest mapped value (or `MIN(a,b)`) | `Source.LI[MIN: Mapping]` |
| `MAX` | Largest mapped value (or `MAX(a,b)`) | `Source.LI[MAX: Mapping]` |
| `COUNT` | Count non-blank mapped items | `Source.LI[COUNT: Mapping]` |
| `ANY` | TRUE if any mapped Boolean is TRUE | `Source.LI[ANY: Mapping]` |
| `ALL` | TRUE only if all mapped Booleans are TRUE | `Source.LI[ALL: Mapping]` |
| `ROUND` | Round a number to N decimals | `ROUND(Number [, Decimals] [, Direction] [, Method])` |
| `ABS` | Absolute value (drop the sign) | `ABS(Number)` |

## Lookup & Mapping — [lookup-and-mapping.md](lookup-and-mapping.md)

| Function | What it does | Minimal syntax |
| --- | --- | --- |
| `LOOKUP` | Pull one value down via a mapping | `Source.LI[LOOKUP: Mapping]` |
| `SELECT` | Pick one named item (⚠️ avoid on specific items) | `Source.LI[SELECT: List.Item]` |
| `SUM` (mapper) | Push many values up via a mapping | `Source.LI[SUM: Mapping]` |
| `FINDITEM` | Convert text into a list item | `FINDITEM(List, Text)` |

## Time series — [time-functions.md](time-functions.md)

| Function | What it does | Minimal syntax |
| --- | --- | --- |
| `CUMULATE` | Running total over time | `CUMULATE(Values [, Bool] [, list])` |
| `DECUMULATE` | Period movement from a cumulative series | `DECUMULATE(Values [, Bool] [, list])` |
| `LAG` | Value N periods earlier | `LAG(Value, Offset, Substitute [, …])` |
| `LEAD` | Value N periods later | `LEAD(Value, Offset, Substitute [, …])` |
| `OFFSET` | Value ±N periods (sign = direction) | `OFFSET(Value, Offset, Substitute [, List])` |
| `POST` | Push a value forward N periods | `POST(Value, Periods [, List])` |
| `PREVIOUS` | Value of the prior period | `PREVIOUS(Value)` |
| `NEXT` | Value of the next period | `NEXT(Value)` |
| `MOVINGSUM` | Rolling-window aggregate (moves with time) | `MOVINGSUM(LI [, Start] [, End] [, Method] [, List])` |
| `TIMESUM` | Aggregate between two fixed periods (single value) | `TIMESUM(LI [, Start] [, End] [, Method])` |
| `START` / `END` | First / last date of a period (or timeline) | `START([Period])` / `END([Period])` |
| `PROFILE` | Spread a value over time by a weight profile | `PROFILE(Numbers, Profile)` |
| `YEARVALUE` | The year's summary value, on each period | `YEARVALUE(LI)` |
| `HALFYEARVALUE` | The half-year's summary value | `HALFYEARVALUE(LI)` |
| `QUARTERVALUE` | The quarter's summary value | `QUARTERVALUE(LI)` |
| `MONTHVALUE` | The month's summary value | `MONTHVALUE(LI)` |

## Text — [text-functions.md](text-functions.md)

| Function | What it does | Minimal syntax |
| --- | --- | --- |
| `TEXT` | Number → text | `TEXT(Number)` |
| `NAME` | List item → its name (text) | `NAME(Item)` |
| `LEFT` | Leftmost N characters | `LEFT(Text, N)` |
| `RIGHT` | Rightmost N characters | `RIGHT(Text, N)` |
| `MID` | Characters from the middle (1-based start) | `MID(Text, Start [, N])` |
| `LENGTH` | Number of characters | `LENGTH(Text)` |
| `FIND` | Position of a substring (0 if not found) | `FIND(Find, Within [, Start])` |
| `SUBSTITUTE` | Replace all occurrences (no Nth-occurrence arg) | `SUBSTITUTE(Text, Find, Replace)` |
| `TRIM` | Strip leading/trailing/extra spaces (Classic only) | `TRIM(Text)` |
| `LOWER` | To lower case | `LOWER(Text)` |
| `UPPER` | To upper case | `UPPER(Text)` |
| `CODE` | List item → its code (text) | `CODE(Item)` |
| `MAKELINK` | Make a clickable URL cell (display text first) | `MAKELINK(Display, URL)` |
| `MAILTO` | Make a click-to-email cell | `MAILTO(Display, To [, CC] [, BCC] [, Subject] [, Body])` |
| `&` | Concatenate text (operator) | `TextA & TextB` |

## Logical — [logical-functions.md](logical-functions.md)

| Function | What it does | Minimal syntax |
| --- | --- | --- |
| `IF THEN ELSE` | Branch on a condition | `IF Cond THEN R1 ELSE R2` |
| `AND` | TRUE if both | `A AND B` |
| `OR` | TRUE if either | `A OR B` |
| `NOT` | Invert a Boolean | `NOT A` |
| `ISBLANK` | TRUE if the value is blank | `ISBLANK(Value)` |
| `ISNOTBLANK` | TRUE if the value is populated | `ISNOTBLANK(Value)` |
| `BLANK` | Return an empty value (keyword) | `IF Cond THEN X ELSE BLANK` |
| (comparison) | Returns a Boolean directly | `Value > 0` |

## Date — [date-functions.md](date-functions.md)

| Function | What it does | Minimal syntax |
| --- | --- | --- |
| `DATE` | Build a date from parts | `DATE(Year, Month, Day)` |
| `YEAR` | Year number from a date | `YEAR(Date)` |
| `MONTH` | Month number (1–12) | `MONTH(Date)` |
| `DAY` | Day-of-month (1–31) | `DAY(Date)` |
| `WEEKDAY` | Day-of-week number | `WEEKDAY(Date [, Start day])` |
| `DAYS` | Days between dates / in a period | `DAYS(End, Start)` or `DAYS(Period)` |
| `MONTHTODATE` | Month-to-date running total | `MONTHTODATE(Values)` |
| `CURRENTPERIODSTART` | Start date of the Current Period | `CURRENTPERIODSTART()` |

## Financial — [financial-functions.md](financial-functions.md)

| Function | What it does | Minimal syntax |
| --- | --- | --- |
| `NPV` | Net present value of cash flows | `NPV(Rate, Cash Flow)` *(also a date/value-pairs form)* |
| `IRR` | Internal rate of return | `IRR(Cash Flow)` *(also a date/value-pairs form = XIRR)* |
| `PMT` | Periodic loan/annuity payment | `PMT(Rate, Periods, PV [, FV] [, Timing])` |
| `CUMIPMT` | Cumulative interest between periods | `CUMIPMT(Rate, Periods, Principal, Start, End [, Timing])` |

## Ranking — [ranking-functions.md](ranking-functions.md)

| Function | What it does | Minimal syntax |
| --- | --- | --- |
| `RANK` | Rank position of each value | `RANK(Values [, Direction] [, Equal behavior] [, Include] [, Groups])` |
| `RANKCUMULATE` | Running total walked in rank order | `RANKCUMULATE(Cumul vals, Rank vals [, Direction] [, Include] [, Groups])` |

## Hierarchy — [hierarchy-functions.md](hierarchy-functions.md)

| Function | What it does | Minimal syntax |
| --- | --- | --- |
| `ITEM` | The current list item of the cell | `ITEM(List)` |
| `PARENT` | Immediate parent item (one level up) | `PARENT(Child)` |
| `ISANCESTOR` | Boolean: is Item1 above Item2? | `ISANCESTOR(Item1, Item2)` |
| `ITEMLEVEL` | Count up to root / down to leaf (Number, Polaris only) | `ITEMLEVEL(Item, ROOT \| LEAF)` |
| `FIRSTNONBLANK` | First non-blank mapped value | `Source.LI[FIRSTNONBLANK: Mapping]` |

> No `ANCESTOR()` or `CHILDREN()` formula function exists. For a higher ancestor, chain
> `PARENT(PARENT(...))` or use a SYS mapping; to aggregate children, use Summary = Sum or
> `SUM` with a mapping. See [hierarchy-functions.md](hierarchy-functions.md).

---

## Beginner's decision guide

| You want to… | Reach for |
| --- | --- |
| Total detail up to a coarser list | `SUM` with a mapping (or set Summary = Sum) |
| Bring a coarser value down to detail | `LOOKUP` with a mapping (not `SELECT`) |
| Prior / next period | `PREVIOUS` / `NEXT` (fixed) or `LAG` / `LEAD` (variable) |
| Running total / YTD | `CUMULATE` (with a reset Boolean) |
| Rolling 3-month sum | `MOVINGSUM(LI, -2, 0)` |
| % of full-year | `LI / YEARVALUE(LI)` |
| Avoid a wall of `IF`s | a Boolean line item, `MIN`/`MAX`, or a `LOOKUP` mapping |
| "Am I this item?" | `ITEM(List) = …` (compare), or a System flag |
| Build a mapping from the hierarchy | `PARENT(ITEM(...))` (chain for higher levels) or a SYS module |
| Turn text into a list item | `FINDITEM(List, Text)` |
| Top-N flag | `RANK(...) <= N` |

**Related:** [Formulas overview](README.md) · [PLANS](../03-methodology/plans-standard.md) ·
[The Planual](../03-methodology/planual.md) · [Sources & validation](../../SOURCES.md) ·
[All-functions index (Anapedia)](https://help.anaplan.com/all-functions-160769b0-de37-4f08-87a0-cc3aa55525a3)
