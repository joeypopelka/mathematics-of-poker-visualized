# Chen ch. 26–28: Tournaments — Plan

An exploration of the three tournament chapters of Chen & Ankenman's *The
Mathematics of Poker*, in the same spirit as the adjacent ch. 12 / ch. 15 /
ch. 17 projects: **reproduce the book's numbers exactly, then chart the
continuous structure the book only samples at a few points.**

**Thesis of the repo:** the three tournament chapters are one idea developed in
stages — *a tournament chip is not a dollar*. Skill decouples chips from equity
in the early game (ch. 26); the payout structure decouples them near the money
(ch. 27); and both together reshape correct strategy (ch. 28). One engine makes
that decoupling measurable.

> **Compute note.** Unlike ch. 12 (a multi-million-board equity enumeration in
> C), this block is **closed-form arithmetic plus tiny combinatorics**. Chen's
> own methods are analytic (`E = Cᴺ`), not simulated. Every script runs
> sub-second; the only Monte-Carlo is a small validation of `E = Cᴺ`. The one
> combinatorial risk — Malmuth-Harville's O(n!) permutation sum — is capped at
> final-table / SNG sizes (n ≤ 9), with the closed-form Malmuth-Weitzman used
> for larger fields.

---

## Module 1 — The Theory of Doubling Up + Rebuy  (ch. 26; rebuy from ch. 28)

Engine: the closed-form Theory of Doubling Up.

- `E = Cᴺ`  (26.1), `N = log₂X`
- `E = Sᵝ`, `β = −log₂C`  (26.2), S = fraction of total chips
- Effective tournament size `k` for structured payouts (26.3) and the simplified
  `N − D` form.

**Reproduce (to printed digits):**

| Book anchor | Target |
|---|---|
| 100-player, 2 buy-ins gross | `C = 0.5550`; stack-2 equity `0.0360` |
| NLHE fold decision (250 players, ¾-buyin edge) | `C = 0.5364`; call `0.008857` **<** fold `0.009269` → fold, though chip-EV says "+137 chips, call" |
| Coinflip indifference | `W = C` |
| Decline QQ vs AK (57-43) | implies `0.57⁸ = 0.01114` ≈ 2.85 buy-ins |
| Three-way "third man in", C = 0.55 | needs `30.25%` vs `25%` chipwise |
| Effective size, f = 154/256 | `k = 147.68` (C=0.52); `147.35` (N−D form) |

**Rebuy / add-on (ch. 28, computed on this engine — the requested piece):**
reproduce Case 2 — 6000 chips, 300 players, C = 0.54, $90k pool, 1M chips →
`E(6000) = $953`, `E(7500) = $1,162`; add-on (>$200 value, $100 cost) is a take;
value stays positive to **half the chips in play**; at-par rebuy breakeven near
stack `8,325` at C = 0.51. Case 1 (rebuy on first-hand bustout) → yes.

**Extension the book never charts:** the continuous family of chip-value curves
`E = Sᵝ` sweeping skill C from losing (concave — encourage variance) through
C = 0.5 (linear) to skilled (convex — protect chips), with rebuy/add-on value
overlaid vs stack and C.

## Module 2 — Chips Aren't Cash: four equity formulas  (ch. 27)

Implement all four chip→prize-equity models and reproduce every printed table:

- **Proportional Chip Count** (27.1) — `<Xᵢ> = vₙ + sᵢWₙ`
- **Landrum-Burns** (27.2)
- **Malmuth-Harville** (27.3) — Harville horse-racing analogue
- **Malmuth-Weitzman** (27.4) — `p(bust next) ∝ 1/chips`; authors' near-money favorite

**Reproduce:** 25000/20000/10000/5000 @ 2000/1400/900/700 under all four
(Prop-chip `1616.67…`, Landrum-Burns `1416.67…`); flaw cases `48000/4000×3`
(Prop-chip pays leader `$2,460` > first place; Landrum-Burns `$1,800`).
Variance multiple `k` (27.5) + Player T (`k = 16.105` / `53.6456`, `σ = 0.296`).

**Extension the book never charts:** the four-model *disagreement* across the
stack-distribution simplex — where model choice actually moves money in a
final-table deal. Chen states Prop-chip and Landrum-Burns bound the truth but
never plots the spread.

## Module 3 — Poker's Still Poker: strategy consequences  (ch. 28)

- Game of chicken (Example 28.1) — payoff matrix, three equilibria, "first in" edge.
- Bubble required-equity, reproduced exactly: SNG 5-3-2 four 2500 stacks → **61.33%**
  to call vs **42%** chip-EV; four-handed cases `62.5%`, `65.8%` ("even AKo folds");
  supersatellite fold-AA.

**Extension + repo tie-in:** overlay the ICM risk premium (Module 2) on the
existing **ch. 12 jam/fold** solve — how the money bubble tightens optimal
shove/call ranges vs the chip-EV baseline.

---

## Deliverables (house style)

```
doubling_up.py   # E=C^N engine + rebuy/add-on
icm.py           # four equity formulas + variance multiple
strategy.py      # chicken, bubble required-equity, ch12 ICM overlay
analyze.py       # reproduce-Chen assertions (all numbers above)
make_artifact.py # build self-contained multi-tab index.html
*.json           # small, checked in
index.html       # interactive explorer (3 tabs)
README.md, REPORT.md
```

Pure Python + numpy (sympy for the effective-size / `k` algebra). Sub-second
throughout; no large data blobs.
