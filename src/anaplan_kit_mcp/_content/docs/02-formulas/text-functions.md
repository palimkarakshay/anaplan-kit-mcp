# Text Functions

> **Level:** L1 · **Area:** Formulas · **PLANS:** Performance

Text functions build, slice and clean strings — labels for dashboards, codes for mapping, email
links for workflows.

> ⚠️ **Performance note.** Text is comparatively **expensive** in Anaplan: text line items cost
> more memory than numbers/Booleans, and text comparisons are slower. Use text for **display and
> keys**, not as a substitute for proper list references or Boolean flags. Where possible, do text
> wrangling **once** in a System module and reference the result — don't recompute strings deep
> inside large calculation modules. *(Planual: Performance / Necessary.)*

To join text, use the `&` operator: `"Q" & TEXT(Quarter Num)`.

---

### TEXT

**Syntax**

```
TEXT(Value)
```

**What it does**
Converts a **number** into a text value, so it can be concatenated with `&` or used by other
functions that expect text. (For turning a *list item* into text, use `NAME` or `CODE` instead —
`TEXT` is the number→text converter.)

**Example**

```
Label = "Year " & TEXT(Year Num)        -- "Year 2026"
```

**Watch out for**

- You **must** convert numbers before joining: `"Q" & 1` errors; `"Q" & TEXT(1)` works.
- `TEXT` of a number may include decimals/formatting you don't want — combine with `ROUND` first.

**Source:** https://help.anaplan.com/text-7c779d7b-c753-43f0-bc10-43e78b9b8572

---

### NAME

**Syntax**

```
NAME(List item)
```

**What it does**
Returns the **name** of a list item as text. The bridge from a list-formatted line item to a
text label.

**Example**

```
Region Label = NAME(ITEM(Region))       -- the current region's name as text
```

**Watch out for**

- `NAME` returns the display name; `CODE` returns the code — pick deliberately when names aren't
  unique.
- Don't store `NAME(...)` if you can just reference the list item; text duplicates cost memory.

**Source:** https://help.anaplan.com/name-bb3d44df-6980-4266-b9f8-42b053e7826d

---

### LEFT

**Syntax**

```
LEFT(Text, Number of characters)
```

**What it does**
Returns the leftmost N characters of a string.

**Example**

```
Country Prefix = LEFT(Product Code, 2)      -- "US-1234" -> "US"
```

**Watch out for**

- If N exceeds the length, you simply get the whole string (no error).

**Source:** https://help.anaplan.com/left-9c2a45d9-5af8-433a-b45c-46b0d6ae8462

---

### RIGHT

**Syntax**

```
RIGHT(Text, Number of characters)
```

**What it does**
Returns the rightmost N characters of a string.

**Example**

```
Last4 = RIGHT(Account No, 4)
```

**Watch out for**

- To grab "everything after a fixed prefix", combine with `LENGTH`/`FIND` rather than guessing N.

**Source:** https://help.anaplan.com/right-f076e4fd-3f63-4b7b-9ed2-3769a0dfd0e7

---

### MID

**Syntax**

```
MID(Text, Start position [, Number of characters])
```

**What it does**
Returns characters from the **middle** of a string, starting at `Start position` (1-based).

**Example**

```
Middle = MID(Product Code, 3, 4)        -- chars 3-6
```

**Watch out for**

- Position is **1-based** (the first character is position 1), unlike many languages.
- Combine with `LENGTH` to extract "from position X to the end".

**Source:** https://help.anaplan.com/mid-5e5cc593-8bb2-4417-8daf-ed57b552e2cc

---

### LENGTH

**Syntax**

```
LENGTH(Text)
```

**What it does**
Returns the number of characters in a string. (Also written `LEN`.)

**Example**

```
Code Length = LENGTH(Product Code)
```

**Watch out for**

- Counts spaces too — trim first if leading/trailing spaces shouldn't count.

**Source:** https://help.anaplan.com/length-49846ba7-7b09-4d11-b203-58ba512e7727

---

### FIND

**Syntax**

```
FIND(Text to find, Within text [, Start])
```

**What it does**
Returns the **position** of the first occurrence of one string inside another (optionally starting
the search at a given position).

**Example**

```
Dash Pos = FIND("-", Product Code)              -- position of the first "-"
Prefix   = LEFT(Product Code, FIND("-", Product Code) - 1)   -- everything before it
```

**Watch out for**

- Returns `0` when the substring is not found — guard with an `IF FIND(...) > 0` test before
  feeding the result into `LEFT`/`MID`.
- Position is 1-based and case-sensitive.

**Source:** https://help.anaplan.com/find-b4571668-130a-4de8-a7b2-57439714f344

---

### SUBSTITUTE

**Syntax**

```
SUBSTITUTE(Text, Text to find, Replacement text)
```

**What it does**
Finds **all** occurrences of a substring and replaces them with another.

**Example**

```
Clean = SUBSTITUTE(Raw Name, "_", " ")      -- "Cost_Centre_01" -> "Cost Centre 01"
```

**Watch out for**

- Replaces **every** match, not just the first. Unlike Excel, Anaplan's `SUBSTITUTE` has **no
  optional fourth (occurrence) argument** — you cannot target only the Nth instance; it always
  replaces all of them, left to right.
- Chain `SUBSTITUTE`s to remove several characters — but if you find yourself chaining many, reconsider
  the upstream data quality.

**Source:** https://help.anaplan.com/substitute-841babeb-4694-4761-91c1-18d920edb879

---

### TRIM

**Syntax**

```
TRIM(Text)
```

**What it does**
Removes **leading and trailing spaces**, and collapses runs of spaces *between* words down to a
single space. The go-to cleaner for text imported from external systems with irregular spacing.

**Example**

```
Code Norm = UPPER(TRIM(Raw Code))           -- "  ab   cd " -> "AB CD"
```

**Watch out for**

- `TRIM` is **not available in Polaris** (Classic Engine only).
- Trim **before** matching (e.g. before `FINDITEM`), since stray spaces silently break exact-text
  lookups.

**Source:** https://help.anaplan.com/trim-351955a5-838c-4f3b-9073-96732fc259a9

---

### LOWER

**Syntax**

```
LOWER(Text)
```

**What it does**
Converts text to lower case.

**Example**

```
Key = LOWER(Email)
```

**Watch out for**

- Use `LOWER`/`UPPER` to **normalise before matching** (e.g. before `FINDITEM`) since text
  comparison is case-sensitive.
- An optional `Locale` argument exists in the **Classic Engine** (not Polaris) for language-aware
  casing.

**Source:** https://help.anaplan.com/lower-610b25eb-611f-412e-ab2d-dc8083dc22d4

---

### UPPER

**Syntax**

```
UPPER(Text)
```

**What it does**
Converts text to upper case.

**Example**

```
Code Norm = UPPER(TRIM(Raw Code))
```

**Watch out for**

- Same matching/normalisation use as `LOWER`. Pick one convention and apply it consistently.

**Source:** https://help.anaplan.com/upper-6b58ff23-ffc1-475e-b96a-421f127f87b4

---

### CODE

**Syntax**

```
CODE(List item)
```

**What it does**
Returns the **code** of a list item as text (the unique code, as opposed to its display name).

**Example**

```
CC Code = CODE(ITEM(Cost Centre))
```

**Watch out for**

- Codes are stable keys; **names** can change. For mapping/joins, prefer `CODE` over `NAME`.
- Returns blank if the item has no code.

**Source:** https://help.anaplan.com/code-0e20099c-af47-4343-9ad9-3a20b580d2de

---

### MAKELINK

**Syntax**

```
MAKELINK(Text to display, URL)
```

**What it does**
Produces a **clickable hyperlink** cell: the first argument is the **display text** shown in the
cell, the second is the **URL** it points to.

**Example**

```
Doc Link = MAKELINK("Open", "https://intranet/cc/" & CODE(ITEM(Cost Centre)))
```

**Watch out for**

- **Display text comes first, URL second** — easy to transpose if you think of it as "make a link
  from a URL".
- Only valid `http://` / `https://` URLs work, and the line item needs the **Text** format
  (link-type).
- Not available in **Polaris** (Classic Engine only).

**Source:** https://help.anaplan.com/makelink-0dbc28e2-da61-4b82-95c7-11fe707a06ab

---

### MAILTO

**Syntax**

```
MAILTO(Display text, To [, CC] [, BCC] [, Subject] [, Body text])
```

**What it does**
Produces a clickable cell that opens a pre-filled email.

**Example**

```
Notify = MAILTO("Email approver", Approver Email, "", "", "Budget ready", "Please review.")
```

**Watch out for**

- Not available in the **Polaris** engine (Classic Engine only).
- The first argument is the **display text**, then recipients — easy to transpose.

**Source:** https://help.anaplan.com/mailto-880af3a5-45c5-4f80-ba27-a55fc8b411d0

---

**Related:** [lookup-and-mapping.md](lookup-and-mapping.md) (FINDITEM turns text into list items) ·
[hierarchy-functions.md](hierarchy-functions.md) (NAME/CODE work on ITEM) ·
[Performance docs](../07-performance/) · [cheatsheet.md](cheatsheet.md)
