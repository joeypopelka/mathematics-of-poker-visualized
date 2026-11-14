# Chips Aren't Cash: The Tournament Chapters, Reproduced

Chen & Ankenman devote three chapters (26–28) of *The Mathematics of Poker* to
tournaments. Unlike the earlier toy-game chapters, these are light on equations
and heavy on worked examples — which makes them perfect to *reproduce
exactly*. Every model in the three chapters is closed-form or small combinatorics,
so this project is arithmetic, not enumeration: all of it runs sub-second.

**Result: 46 of 46 of the chapters' worked numbers reproduce**, and along the way
the reproduction turns up **two internal inconsistencies in the printed text**.

The three chapters are one argument in three acts — *a tournament chip is not a
dollar*:

- **ch. 26 — skill** decouples chips from equity in the early and middle game.
- **ch. 27 — the payout structure** decouples them near the money.
- **ch. 28 — both** reshape correct strategy.

---

## Act I — The Theory of Doubling Up (ch. 26)

The chapter's whole apparatus is one relation. With `C` the (assumed constant)
chance of doubling your stack before busting and `N = log₂X` the number of
doubles needed to win a winner-take-all field of `X`,

```
E = C**N            E = S**β ,  β = −log₂C   (S = your fraction of all chips)
```

Setting a player's starting equity to `1/X` forces `C = 0.5` and chips become
*exactly linear* — the sanity check the model must pass. A skilled player inverts
the relation from a known edge: a 2-buy-in expectation in a 100-player field
gives **C = 0.5550**; a ¾-buy-in edge in a 250-player field gives **C = 0.5364**.

**The chip-value curve.** Charting `E = Sᵝ` continuously (tab 1) shows the whole
story the book only samples. Skilled curves sit *above* the linear line (a skill
premium — your chips are worth more than their share) but are *concave* (each
marginal chip is worth less than the last). Losing players sit below and convex —
the model's blunt advice that **losing players should court variance**, since
every additional double hands the field another chance to out-skill them.

**The decision the theory flips.** The headline reproduction: a 250-player NLHE
spot where calling a river shove is **+137 chips** by chip-EV, yet the doubling-up
equities are `E(call & win) = 0.024603`, `E(fold) = 0.009269`, so

```
EV(call) = 0.36 × 0.024603 = 0.008857  <  0.009269 = EV(fold)   →  fold.
```

**Corollaries**, all reproduced: you are indifferent to a coinflip exactly when
your win chance equals `C`; declining a 57-43 flip implies you believe you are
worth `0.57⁸ = 0.01114` of the tournament (the book rounds this to "about 2.85
buy-ins," though its own figure is 2.785); the third player into a three-way
all-in needs `C² = 30.25%` rather than the chip-linear 25%. The **effective
tournament size** for a match-play field split 154/102 comes out to **k = 147.35**
— a 256-player field with the skill latitude of a 147-player one.

**Rebuy strategy** (ch. 28, but computed on exactly this engine — as requested).
Reproducing Case 2: at 6000 chips `E = $953`, at 7500 chips `E = $1,162`, so a
$100 add-on worth ≈ $209 is automatic. Charting add-on value vs. stack (tab 1)
confirms the book's conclusions: the **discounted add-on clears its cost at
essentially every stack**, while an **at-par rebuy** (C = 0.51) breaks even near
an 8,325 stack — rebuy at par with care, take discounted add-ons always.

---

## Act II — Chips Aren't Cash (ch. 27)

Four models map a chip stack to a cash equity; each is biased, and knowing the
biases is the point. All four are implemented and every printed number matches.

| Model | Rule | Bias |
|---|---|---|
| Proportional Chip Count (27.1) | `vₙ + sᵢWₙ` | over-pays big stacks — **lower bound** flips: can pay the leader *more than first* |
| Landrum-Burns (27.2) | 1st ∝ chips, rest split evenly | over-pays small stacks — **upper bound** |
| Malmuth-Harville (27.3) | Harville horse-racing analogue | accurate |
| Malmuth-Weitzman (27.4) | P(bust next) ∝ 1/chips | accurate; authors' near-money favorite |

On the running example (25k/20k/10k/5k, $2000/1400/900/700) the models bracket
cleanly for the leader: prop-chip $1616.67 ≥ MW $1529 ≥ MH $1511 ≥ Landrum-Burns
$1416.67. The prop-chip flaw is stark on 48k/4k/4k/4k, where it awards the leader
**$2,460 — more than first-place money**.

**The disagreement, charted.** Sliding the leader's stack from even to dominating
(tab 2) draws the band between the two bounds — the space a final-table deal
negotiates inside — and shows prop-chip crossing above the $2,000 first-place
line, which no valid model may do.

**Book inconsistency #1.** Landrum-Burns for P3 of the running example prints as
**$1,066.67**. But the four Landrum-Burns equities must sum to the $5,000 pool,
and they only do so with **P3 = $1,166.67**; $1,066.67 is a typo. (This project
asserts the sum-to-pool value.)

**Book inconsistency #2.** The tournament variance multiple `k = n·Σvᵢ² − 1`
(27.5) reproduces the morning example exactly (**16.105**). But the evening
example's printed payout percentages sum to 100% and give **53.263** by the same
formula, while the book reports **53.6456** — its own table does not reproduce
its own number.

---

## Act III — Poker's Still Poker (ch. 28)

Two structural facts reshape play. First, confrontations are **not constant-sum**
— every uninvolved player gains equity when two others collide — so tournaments
embed a **game of chicken** (Example 28.1) in which being *first* all-in claims
the favorable equilibrium (its mixed equilibrium drives on exactly 10% of the
time). Second, a step in the money imposes a **risk premium**: the equity to call
off your stack exceeds the chip-EV break-even.

Reproduced to the digit: the 5-3-2 sit-and-go where the big blind needs **61.33%**
to call versus a **42%** chip-EV break-even (Example 28.2); the four-handed bubble
cases needing **62.5%** and **65.8%** ("even AKo is a fold"); and the
supersatellite where folding pocket aces is correct — the big stack's fold equity
(0.978 of a seat) beats calling an 81%-favorite AA (`0.81 × ~1.0`), because he is
wagering a seat, not chips.

**The bubble factor.** Casting the ICM premium as **required-equity ÷ chip-EV
threshold** turns it into a single multiplier on the chip-EV jam/fold ranges
solved in the companion **ch. 12** project. Swept across a 5-3-2 SNG (tab 3), the
factor **peaks near 1.29× for a middling stack** and **drops below 1 for a
dominant leader**, who can correctly call *lighter* than chip-EV because he cannot
bust and profits from every elimination. That is the quantitative bridge from the
chip-EV shove/fold charts to their money-bubble corrections.

---

## Method

Everything is closed-form (`E = Cᴺ`, the four equity formulas, the variance
multiple) or a small permutation sum. Malmuth-Harville and Malmuth-Weitzman share
one subset-DP over finishing orders (`O(2ⁿ·n)`), capped at final-table / SNG
sizes; the closed-form Weitzman weight `p ∝ 1/chips` handles larger fields. A
tiny Monte-Carlo (`doubling_up.py --mc`) confirms `E = Cᴺ` against a simulated
doubling bracket. `python3 analyze.py` runs all 46 reproduction checks.
