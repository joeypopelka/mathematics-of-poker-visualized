# An Exhaustive Analysis of Chen's Jam-or-Fold NLHE Game

*The Mathematics of Poker*, Chapter 12, Example 12.3: equal stacks of S units,
defender posts 1, attacker (button) posts 0.5, attacker jams or folds, defender
calls or folds. This is the full equilibrium analysis of that game — the
"exhaustive analysis of this game yields any number of oddities like this"
that the book alludes to on p. 131 — computed exactly for every stack size
from 1 to 2,500 big blinds.

**Interactive explorer:** https://joeypopelka.github.io/mathematics-of-poker-visualized/jam-or-fold/

## Method

1. **Exact equities.** All 812,175 distinct hand-vs-hand preflop matchups,
   reduced by suit isomorphism to 50,258 classes, each enumerated over all
   C(48,5) = 1,712,304 boards with an exact 7-card evaluator (verified against
   the known frequency counts of all 133,784,560 seven-card hands). Output:
   the full 1326×1326 combo equity matrix (`equity.f32`).
2. **Exact 169-class reduction.** By suit symmetry the game has an equilibrium
   constant on the 169 canonical hands; card removal is handled exactly via
   per-class compatibility counts N[A,B] and mean equities Q[A,B]
   (representative-independence asserted).
3. **Exact equilibria.** For fixed S the game's payoff is bilinear in the two
   behavioral strategies j, c ∈ [0,1]^169, so the Nash equilibrium is a linear
   program. Both players' LPs are solved independently at every stack size;
   their values agree to <1e-6 everywhere (strong duality check).
4. **Sweep + bisection.** 1,379 stack sizes (log-spaced 1→2500, plus a dense
   linear grid below 25), with every range-membership transition refined by
   bisection, and every claimed oddity re-verified by strict EV margins so that
   degenerate-LP artifacts cannot masquerade as findings.

Accounting convention (attacker's net, relative to nothing): fold −0.5;
jam+fold +1; jam+call 2S·eq − S. Chen's threshold formula values a called jam
at 2S·eq − S *relative to folding*, which silently drops the attacker's
refunded half-blind; where it matters we report both.

## Fidelity to the book

| Quantity | Book | Exact | Verdict |
|---|---|---|---|
| ATs vs AA equity | 0.13336 | 0.1333627 | ✓ |
| AKs vs AA equity | 0.12141 | 0.1214051 | ✓ |
| AKs vs ATs equity | 0.70473 | 0.7074299 | ✓ |
| AKs vs A5s equity | 0.69817 | 0.6981695 | ✓ |
| **A5s vs AA equity** | **0.13331** | **0.1330692** | **erratum** |
| ATs entry threshold | 833.25 | 833.25 (Chen's convention) / **833.93** (consistent) | ✓ / refined |
| A5s entry threshold | 833.12 | 832.58 (Chen's conv.) / 833.26 (consistent) | shifted by erratum |
| 63s broken strategy | ≤2.3 ∪ 5.1–7.1 | ≤2.39 ∪ 5.1–7.2 | ✓ |
| 53s broken strategy | ≤2.4 ∪ 4.1–12.9 | ≤2.41 ∪ 4.0–12.90 | ✓ |
| 43s broken strategy | ≤2.2 ∪ 4.8–10.0 | ≤2.20 ∪ 4.8–10.0 | ✓ |
| Jam fraction at S=10 | 774/1326 = 58.37% | 58.28% | ✓ |
| Call fraction at S=10 | 494/1326 = 37.25% | 37.38% | ✓ |
| 97s jam threshold | ≈36 | 36.08 | ✓ |

The one substantive correction: **A5s vs AA is exactly 0.13307, not the
0.13331 printed on p. 130.** Consequence: at S = 833 the exact equilibrium is
{AA 100%, ATs 100%, **A5s mixed at 85.5%**} against {AA, AKs at a knife-edge},
rather than the book's {AA 100%, ATs 87.73%, A5s 100%} — with the corrected
equity, the indifference-forced mixing lands on A5s, not ATs.

## The chronology of cooling (selected deep-stack transitions)

Reading from very large stacks downward (all values exact, bisected):

| S | Event |
|---|---|
| ∞ … 834 | Both sides play **AA only** — the frozen phase |
| 833.93 | **ATs** ignites (Chen's 833.25 under his convention) |
| 833.26 | **A5s** joins; defender's **AKs** call arrives at the same knife-edge (833.25) |
| 807.5 | **AKs** joins the jam range |
| 698.8 | **AKo** jams; defender adds **KK** calls at the same point |
| 590.3 | **ATs is expelled** (and the defender's AKs call leaves with it) |
| 477.5 | **KK** finally starts jamming — 356 bb after ATs first did |
| 427.2–589.5 | ATs strictly out (EV margin −0.027 bb at S=500): dominated by the AK/KK calling ecosystem |
| 426.1 | ATs (and AKs calls) return |
| 275.2 / 271.3 | TT jams / QQ jams; JJ + QQ calls reshuffle in a coupled cluster around 270 |
| 269.4–274.1 | Defender's JJ call exists *only* inside this window |
| 157.0–136.6 | ATs's second exile |
| ≤ 135 | ATs is jammed at every smaller stack |

The full catalog (478 transitions) is in `thresholds.json`; the curated
strictly-verified gaps are in `strict_gaps.json`.

## The oddities

- **Card removal beats hand strength.** The first eight hands to enter after
  AA are all suited aces (ATs, A5s, AJs, A4s, AQs, A3s, AKs, A2s — in that
  order, interleaved by the straight-potential pattern T>J>Q>K and 5>4>3>2).
  KK, the second-best hand in poker, waits until S ≈ 477.5.
- **Non-monotonic membership is everywhere.** 21 hands have strictly-verified
  stack windows where they are *out* of the jam range between windows where
  they are in: ATs (twice), A2s–A8s, KTo, Q5s–Q7s, T2s/T3s/T6s, 92s–94s, 84s,
  65s, and Chen's starred trio 63s/53s/43s.
- **Transitions arrive in coupled pairs.** The attacker adding a hand and the
  defender adding/removing its counter happen at the same stack size: ATs's
  jam windows coincide exactly with the defender's AKs call windows; AKo's
  entry coincides with KK's call entry; QQ's jam and call thresholds are the
  same number (269.4).
- **Discontinuous strategy jumps.** At transition points frequencies jump
  discontinuously (e.g., ATs from 100% to 0% at S = 590.3) — Chen's
  phase-transition/temperature metaphor is quantitatively apt: the game value
  is continuous in S while the strategies are not, exactly like a first-order
  phase transition's free energy vs. order parameter.
- **The attacker is favored only in a hot band.** Game value is zero at S = 1
  (everyone all-in, pure coin flips), positive for all 1 < S < **7.797** (peak
  ≈ +0.065 bb around S ≈ 3.6), and negative beyond. At the crossover the
  attacker's EV ledger balances exactly: steal income +0.348 (jam 63.2%,
  defender folds enough to surrender the 1-unit blind 34.8% of hands) against
  fold bleed −0.184 (surrendering the half-blind 36.8% of hands) plus showdown
  deficit −0.164 (46.3% average equity when called, and the cost of that
  deficit scales linearly with S). The analytic anchor is Chen's [0,1] Game #2,
  whose closed-form value −1/2 + 27S/(4(S+3)²) crosses zero at exactly S = 6;
  real hold'em equities are more compressed than that game's fixed 2:1, so
  each showdown moves less money at the same S, stretching the crossover from
  6 to 7.8.

## Files

| File | Contents |
|---|---|
| `equity.c` / `equity` | Exact evaluator + equity enumerator (selftest, `--eq AsKs AcAd` mode) |
| `equity.f32` | 1326×1326 float32 combo equity matrix |
| `solve.py` | 169-class reduction, LP equilibrium, sweep, bisection |
| `analyze.py` | Strict-margin verification, band structure, Chen comparisons |
| `sweep.npz` | Equilibrium strategies and game value at all 1,379 stack sizes |
| `thresholds.json` / `jumps.json` / `strict_gaps.json` | Transition catalogs |
| `make_artifact.py` / `artifact_template.html` | Interactive explorer generator |
| `shove_fold_explorer.html` | The published interactive artifact |
| `solve_run.log` / `equity_run.log` | Run logs |

Reproduce from scratch:
```sh
clang -O3 -march=native -o equity equity.c -lpthread
./equity --selftest && ./equity 8     # ~10 min on 8 cores
python3 solve.py                      # ~1 min
python3 analyze.py
python3 make_artifact.py
```
