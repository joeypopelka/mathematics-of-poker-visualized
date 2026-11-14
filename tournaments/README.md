# Chen ch. 26–28: Tournaments — *A Tournament Chip Is Not a Dollar*

An exact reproduction of the three tournament chapters of Chen & Ankenman's
*The Mathematics of Poker* (26 · Doubling Up, 27 · Chips Aren't Cash, 28 ·
Poker's Still Poker), then a continuous chart of the structure the book only
samples at a few worked examples. In the spirit of the adjacent ch. 12 / ch. 15
/ ch. 17 projects — but, unlike those, this one is **pure closed-form
arithmetic**: no enumeration, no large data, every script runs sub-second.

**Full writeup and findings: [REPORT.md](REPORT.md)**

**Live interactive explorer: https://joeypopelka.github.io/mathematics-of-poker-visualized/tournaments/**
(`tourney_explorer.html` — self-contained single page)

Highlights:

- **46 / 46 of the chapters' worked numbers reproduced** — from the doubling-up
  fold decision that flips a +137-chip call into a fold, to the four ICM
  formulas, to the 61.33%-vs-42% bubble calling threshold.
- **Two book inconsistencies found.** Landrum-Burns P3 of the running example
  prints as $1,066.67 but must be **$1,166.67** to sum to the prize pool (a
  typo); and the evening tournament's printed payout percentages give a variance
  multiple of **53.263**, not the book's stated **53.6456**.
- **The chip-value curve `E = Sᵝ`, charted across skill.** Skilled players sit
  *above* the linear line (a skill premium) yet on a *concave* curve (marginal
  chips still worth less) — both facts at once.
- **Rebuy strategy on the doubling-up engine** (as requested): discounted add-ons
  clear their cost at essentially every stack; at-par rebuys break even near an
  8,325 stack. Reproduces `E(6000) = $953`, `E(7500) = $1,162`.
- **The four ICM models bracketed**, with Proportional Chip Count and
  Landrum-Burns as the lower/upper bounds a final-table deal negotiates between.
- **The "bubble factor"** — the ICM risk premium recast as a multiplier on the
  ch. 12 jam/fold ranges — peaks near 1.29× for a middling stack and drops below
  1 for a dominant chip leader.

## Reproduce

```sh
python3 doubling_up.py --mc   # ch.26 + rebuy; --mc runs the E=C^N sim check
python3 icm.py                # ch.27 four equity formulas
python3 strategy.py           # ch.28 chicken, bubble, ICM overlay
python3 analyze.py            # all 46 reproduction checks in one tally
python3 make_artifact.py      # rebuild the self-contained explorer
```

Requires only Python 3 (standard library; no numpy/scipy needed). Each script
prints its reproduction table and writes a small JSON the explorer embeds.

## Method in one paragraph

Every model in these chapters is closed-form — the Theory of Doubling Up
(`E = Cᴺ`), the Proportional-Chip / Landrum-Burns / Malmuth-Harville /
Malmuth-Weitzman equity formulas, and the tournament variance multiple
`k = n·Σvᵢ² − 1` — or a small permutation sum. Malmuth-Harville and
Malmuth-Weitzman share a single subset dynamic program over finishing orders
(`O(2ⁿ·n)`), capped at final-table / sit-and-go sizes; larger fields use
Weitzman's closed-form `p(bust next) ∝ 1/chips`. A short Monte-Carlo validates
`E = Cᴺ` against a simulated doubling bracket. Two constants that the book prints
inconsistently are asserted at their internally-consistent values and flagged.
