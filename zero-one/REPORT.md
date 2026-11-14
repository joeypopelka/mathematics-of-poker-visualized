# The [0,1] Games: Exact Solutions, and What "the" Solution Even Means

*The Mathematics of Poker*, chapters 11 and 16–18: the finite-pot [0,1] games.
Hands uniform on [0,1] with 0 the nuts; pot P; limit bets of 1; ex-showdown
accounting, value stated to Y (the in-position player). This project carries
the family from von Neumann's half-street game (Ex. 11.3) through the exact
resolution of the two games the book leaves open-ended: #11 (check-raise) and
#12 (unlimited raises).

**Interactive pages:** [hub](index.html) · game2 · game9 · game10 · game11 · game12

## Method

1. **Closed forms** for games #2, #9, #10 and the Y-side of #11 (book
   equations, re-derived in `Q&A_notes.md`).
2. **Sequence-form LP** (Koller–Megiddo–von Stengel) for everything else
   (`seqlp.py`): hands bucketed N ≤ 400 ways, realization-weight variables,
   flow constraints, the saddle point as a single LP per player (duality gap
   < 1e-6 asserted everywhere). Validation gates before any new claim:
   reproduce #9's and #10's closed forms, #11's Y-side (Eq. 17.13), the
   no-fold #7 limit at P = 200, and game #10 exactly from the #12 ladder at a
   2-bet cap (value match to 1e-7).
3. **Optimal-face analysis**: secondary LPs over the set of optimal strategies
   (value held at the game value) to measure what the equilibrium actually
   pins — aggregates vs. per-hand assignments — and a lexicographic
   **monotone selection** (aggression pushed toward stronger hands) to extract
   the canonical threshold representative.

## Finding 1 — "x₁" in game #11 is a band, and so is most of everything

The book stops publishing full solutions at #11, and an earlier CFR solve here
could never pin X's value/check boundary x₁ (independent runs disagreed,
0.16 vs 0.26). The LP shows why — **the question was ill-posed**:

- At P = 2 the optimal face pins X's **total bet mass to 0.28763 ± 1e-5** and
  **total aggressive mass (bet + check-raise) to 0.37533 ± 1e-5**, but
  per-bucket max/min LPs show *every individual hand's* bet probability free
  to range over [0, 1]. The equilibrium constrains how much X does everything,
  not which hand does what. (Same at P = 9: masses 0.42253/0.52633 ± 1e-5.)
- Y's give-up zone facing a bet (≈[0.55, 0.85] at P = 2) has the same per-hand
  freedom — the old CFR's y₂# ≈ 0.709 and the canonical 0.667 are both inside.
- This is not a #11 quirk: the same indifference structure exists in #9/#10
  (verified analytically: vs. optimal Y, bet and check-call have identical EV
  for every X hand below y₁). The book's crisp thresholds are a *selection*
  from the optimal face — the monotone one.

**The monotone selection formalizes that choice**, and passes the decisive
test: it reproduces the book's #9 and #10 X-side closed forms exactly
(x₁ = 5/21, x₂* = 4/21, x₁* = 68/105 at P = 2). Applied to #11 (P = 2,
N-converged):

| Threshold | Value | Note |
|---|---|---|
| x₁ (value continue ends) | ≈ 0.2925 | mix of bet and check-raise above it |
| x₁* (check-call ends) | 0.650 | **≠ y₁* — the book's predicted split, confirmed** |
| x₀ (bluffs resume) | 0.867 | |
| y₁* = y₂# | 0.6675 ≈ 1 − α | a no-raise-bluff representative is optimal |
| G(Y) | **0.062142** | exact; confirms the region-sum formula's 0.062 |

Full P-grid in `game11_exact_grid.json`; the artifact `game11.html` now draws
these exact values and explains the band structure.

## Finding 2 — game #12's value, which the book declines to compute

G₁₂(P) is now exact (`game12_value.json`): the raise ladder capped at B bets
converges completely by **B = 6** (the Rₚ cascade's geometric decay), swept
over 22 pots:

| P | 0.5 | 1 | 2 | 4 | 10 | 30 | 200 | ∞ |
|---|---|---|---|---|---|---|---|---|
| G₁₂(Y) | 0.0226 | 0.0444 | **0.06696** | 0.0837 | 0.0978 | 0.1070 | 0.1121 | 1/16 + r/8 ≈ 0.1143 |

Cascade check at P = 2 (N = 400): x₁ = 0.2475, y₂ = 0.085, x₃ = 0.030,
y₄ = 0.0125 — matching the closed-form chain (0.248 / 0.086 / 0.031 / 0.012).

**The surprise:** G₁₂ < G₁₀ at *every* finite pot (0.06696 < 0.06824 at
P = 2). Unlimited raising *hurts* the in-position player relative to the
two-bet game: bet 3 is X's option (strategic options have non-negative value —
for X), and Y's bet-4 option recovers less than it costs. The old notes had
this arrow backwards for the no-fold analogue (#5 → #6 is also a decrease,
1/8 → 0.1143); fixed.

## Value curves

`values_fp.json`: exact G(Y) for #9/#10/#11/#12 on a 22-pot grid. Each curve
climbs from 0 at P → 0 to its no-fold limit: #9 → 0 (humped, peak ≈ 0.057
near P ≈ 2.6), #10 → 1/8, #11 → 1/9, #12 → 1/16 + r/8. At every pot
G₉ < G₁₁ < G₁₂ < G₁₀ among the raise games — each player's added option
ratchets the value in his own favor.

## Files

| File | Contents |
|---|---|
| `game2/9/10/11/12.html` | interactive artifacts, one per game |
| `index.html` | family hub + value curves |
| `seqlp.py` | sequence-form LP, monotone selection, band tests, gates |
| `exact_run.py` | the analysis run (grids, bands, values) |
| `game11_exact_grid.json` | #11 exact thresholds + band analysis + N-convergence |
| `game12_value.json` | #12 value curve + cap convergence + cascade check |
| `values_fp.json` | #9–#12 exact value curves |
| `Q&A_notes.md` | study notes: threshold tables, α catalog, Q1–Q17 |
| `PLAN_sequence_form_LP.md` | the design doc this implements |
| `game11_cfr_solver.py`, `game11_grid.json` | the superseded CFR solve (kept for the record) |

Reproduce: `python3 seqlp.py --validate 200 && python3 exact_run.py` (~9 min).
