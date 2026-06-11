# Anaplan Optimizer — Built-in Optimization

> **Level:** L3 · **Area:** Advanced Features · **PLANS:** Necessary

Most of modeling answers the question **"what does this plan produce?"** — you set the drivers,
the formulas calculate the result. **Anaplan Optimizer** answers a harder question:
**"what is the *best* plan?"** — the cheapest, the most profitable, the most balanced — *given a set
of rules you can't break*. It is a mathematical solver built into the platform that searches the
space of possible decisions and returns the optimum.

Optimizer is powered by a linear-programming engine (Anaplan uses a Gurobi solver) and handles both
**linear programming (LP)** and **mixed-integer programming (MIP)** problems. *Confirm the current
engine and licensing details in Anapedia.*

> ⚠️ **Optimizer is a specialized, separately-enabled add-on.** It is not on by default and is not
> part of base model building. You reach for it only when a requirement genuinely needs optimization
> — not for problems a normal formula can solve.

## What it solves

Optimizer shines on problems where many decisions interact and you must pick the best combination:

| Problem type | Example |
| --- | --- |
| **Allocation** | Spread a fixed production budget across products to maximize margin. |
| **Network / supply optimization** | Decide which distribution centre serves which region to minimize total cost. |
| **Blending / mix** | Choose the cheapest mix of inputs that still meets quality/spec constraints. |
| **Scheduling / assignment** | Assign jobs to machines or shifts under capacity limits. |

The common thread: there are **many feasible plans**, and you want the one that is mathematically
best against a single measurable goal.

## The three ingredients

You don't write a "solve" formula. Instead you express the problem as **ordinary modules and line
items**, and tell Optimizer which line items play which role. Every optimization has three parts:

| Ingredient | What it is | How you build it |
| --- | --- | --- |
| **Objective** | The single number to maximize or minimize (e.g. total profit, total cost). | A numeric line item — a **linear** function of the decision variables. |
| **Decision variables** | The things Optimizer is allowed to *choose* (quantities to produce, whether a site is open). | Numeric line items with **Summary = None**. Can be continuous or integer/Boolean (MIP). |
| **Constraints** | The rules the answer must obey (capacity, demand, budget). | **Boolean** line items whose formula compares linear expressions using `>=`, `=`, or `<=`. |

*Confirm exact line-item settings (Summary = None for variables, Boolean constraints, supported
operators) in Anapedia, as configuration requirements are precise and version-specific.*

### A worked sketch — allocate production for max profit

Decide how many units of each product to make to maximize profit, without exceeding machine hours.

| Line item (role) | Format | Formula / meaning |
| --- | --- | --- |
| `Units to Make` *(variable)* | Number, Summary **None** | Optimizer fills this in. |
| `Margin per Unit` *(input)* | Number | Given. |
| `Hours per Unit` *(input)* | Number | Given. |
| `Total Profit` *(objective)* | Number | `Units to Make * Margin per Unit` — **maximize**. |
| `Within Capacity?` *(constraint)* | Boolean | `Units to Make * Hours per Unit <= Available Hours` |

You register `Total Profit` as the objective (maximize), `Units to Make` as the variable, and
`Within Capacity?` as a constraint. Run the action, and Optimizer writes the optimal `Units to Make`
back into the module.

> **Key idea:** the objective and every constraint must be **linear** in the decision variables —
> no multiplying two variables together, no `IF` branching on a variable. That linearity is what
> lets the solver guarantee a true optimum quickly.

## How you run it

1. **Set up the modules** — variables, objective, constraints as above.
2. **Configure an Optimizer action** that names the objective (max/min), the variables, and the
   constraints, plus the time/version scope to solve over.
3. **Run it** — typically from a button on a [board or worksheet](../05-ux/new-ux-pages-boards.md)
   so a planner can change inputs, click *Optimize*, and see the result. It can also run inside a
   [process](../04-integration/actions-and-processes.md).
4. **Read the answer** — Optimizer writes the chosen variable values back into your model, and your
   normal output formulas pick up from there.

## When a beginner would (and wouldn't) use it

**Use Optimizer when** the ask contains words like *best, optimal, minimize, maximize, cheapest,
most profitable* **subject to** hard limits — and there are too many combinations to try by hand.

**Don't use Optimizer when** a plain formula or a top-down [allocation](../../cookbook/mapping-and-allocation/)
already gives the answer. Spreading a budget *pro-rata* is a formula; spreading it to *maximize
margin under a capacity cap* is optimization. Choosing Optimizer when a formula would do violates
**Necessary** — and adds a licensed dependency and solver run-time you didn't need.

> **Watch-outs:** Optimizer is a batch *solve*, not a live recalc — results don't auto-update when
> inputs change; someone re-runs it. Very large variable/constraint counts increase solve time.
> Keep the problem as small and as linear as the business allows.

## Related

- [`docs/08-advanced-features/planiq.md`](planiq.md) — the *other* "produces numbers your formulas can't" add-on (ML forecasting, not optimization)
- [`docs/04-integration/actions-and-processes.md`](../04-integration/actions-and-processes.md) — running Optimizer inside a process
- [`docs/05-ux/new-ux-pages-boards.md`](../05-ux/new-ux-pages-boards.md) — the board/worksheet a planner triggers it from
- [`cookbook/mapping-and-allocation/`](../../cookbook/mapping-and-allocation/) — formula-based allocation (the non-solver alternative)
- [PLANS — Necessary](../03-methodology/plans-standard.md)

> Source: Anaplan Optimizer / linear programming (Anapedia & Anaplan Community —
> [Linear programming and Optimizer](https://help.anaplan.com/linear-programming-and-optimizer-6a6489be-23fc-45f2-8afb-c98fa714508e),
> [Optimizer](https://help.anaplan.com/optimizer-e8eac6ea-bfac-43a1-abbb-3dad60cea523),
> [Enable and use Optimizer](https://help.anaplan.com/enable-and-use-optimizer-b7ad2da1-3cd1-4c6e-b144-61cdba5acaee)).
> Optimizer is a separately-licensed add-on; confirm current specifics in Anapedia. See [`SOURCES.md`](../../SOURCES.md).
