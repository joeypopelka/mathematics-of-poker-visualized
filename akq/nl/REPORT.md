# The No-Limit AKQ Game, Solved Across Every Stack Size

*The Mathematics of Poker*, Chen & Ankenman, Chapter 15 (the no-limit AKQ
game — "Player X Strikes Back"). This is an exact equilibrium solve of that
one-street game at **300 starting stack sizes** from 0.02 to 100 pots, built to
answer one question the book poses but does not chart: **how does stack depth
change the value of position?**

**Interactive explorer:** `akq_explorer.html` (self-contained; open in a browser)

## The game

A three-card deck {A > K > Q}. Each player antes 0.5 (pot = 1) and keeps a
stack of *S* pots behind. Each is dealt one card; six equally likely deals.
X acts first (out of position): check, or bet any amount up to *S*. Facing a
check, Y may check (showdown) or bet; facing a bet, Y may fold, call, or raise.
One street, then showdown. Value is stated as **Y's expected profit in pots**,
so V = 0 would mean position is worthless and V > 0 measures what the
in-position player earns per hand at equilibrium.

Because the deck has three cards, A always wins at showdown and Q always loses;
the King is the only card whose showdown result depends on the opponent. All
the game's texture comes from how each player handles the King and from the
bluff/bluff-catch tension on the Queen.

## Method

The tree is solved exactly by **sequence-form linear programming** — both
players' LPs, with a strong-duality check (values agree to < 10⁻⁷) at every
stack. No-limit bet and raise sizes are discretized on a grid that is refined
around the equilibrium's support until the value stops moving (tolerance
10⁻¹⁰). Raises are capped at one re-raise for the sweep; a separate study
(`cap_study.py`) confirms deeper raise wars move the value by at most
~3×10⁻⁵ pots and not at all below S ≈ 0.5, so the curves are accurate. A
tie-breaking LP pass (`clean_plans`) selects, among payoff-equivalent optima,
the one with the least aggressive-action mass, so the reported strategies are
canonical rather than LP artifacts.

Three regimes admit **exact closed forms** (derived by hand, verified against
the LP to machine precision — residuals ~10⁻¹⁷); the deep regime is solved
numerically and cross-checked against a hand-derived "polar" restriction.

## The headline answer

**Position is worth more with a deeper stack — but only up to about half a pot
behind. After that, extra stack is worth exactly nothing.**

| Stack S (pots) | Value to Y (position) | What's happening |
|---|---|---|
| → 0 | → 0 | everyone all-in; pure card-showdown, no skill |
| 0.2 | +0.00556 | tiny jams |
| √2−1 ≈ 0.414 | +0.02036 | jam-only regime ends |
| 0.483 | +0.02660 | King's blocking bet switches on |
| **0.525** | **+0.02724** | **plateau reached** |
| 1, 10, 100 | +0.02724 | identical — flat to 10⁻¹⁶ |

Y's edge climbs from 0 to **≈ +0.0272 pots** (about 2.7% of the pot every
hand) as the stack deepens from nothing to ~0.53 pots, then freezes. For
S ≥ 3 the value is constant to 1.2×10⁻¹⁶ — literally floating-point flat. The
entire dependence of position on stack depth lives **under about half a pot of
stack**; a 1-pot stack and a 100-pot stack are worth precisely the same to the
player in position. This is the opposite of the usual "deeper stacks favor the
skilled/positional player" intuition, and it happens because a one-street game
gives position nothing extra to *do* with chips it will never put in: once the
stack covers Y's largest equilibrium bet (0.525 pots), more chips are dead
weight.

## Four regimes

Reading upward from an all-in-short stack, the equilibrium passes through four
structural phases. The boundaries are exact where marked.

### I. Jam-only (0 < S ≤ √2 − 1)

Bets are so small relative to the pot that the whole game degenerates to
jam-or-call. X jams every Ace and a fraction S/(1+S) of Queens (as bluffs);
the King never jams. Y calls with every Ace and a fraction (1−S)/(1+S) of
Kings. After a check, the roles mirror. The value is

> **V(S) = S² / (6(1 + S))**   — exact.

Verified to |V − law| < 10⁻¹⁶ at S = 0.2, 0.35, and 0.414.

### II. Polar bet (√2 − 1 ≤ S ≤ 0.483)

The stack now covers the classical optimal bet. X unclamps to the half-street
polar size **√2 − 1 of the pot**, betting all Aces plus (1 − 1/√2) of Queens
as bluffs; Y still jams behind after a check. The value is

> **V(S) = ( S/(1+S) − (3 − 2√2) ) / 6**   — exact.

The two laws are not just continuous but **tangent** at S = √2 − 1: regime I
hands off to regime II with matching value *and* slope, a C¹-smooth phase
boundary. (This is why the boundary sits exactly at the half-street bet size
√2 − 1 = 0.41421 — the same constant that solves the half-street AKQ game.)
Verified to < 10⁻¹⁶ at S = 0.425, 0.45, 0.475.

### III. The King strikes back (0.483 ≤ S ≤ 0.525)

At **S ≈ 0.483** a qualitatively new option becomes profitable — and it is
exactly the one the book flags in "Player X Strikes Back": X's **King makes a
small blocking bet.** As stacks deepen through this narrow window, X's bet size
*collapses* from the 0.41-pot polar bet down toward 0.16, because the range is
no longer polar (nut+air) but *merged* — it now contains the King, which wants
a cheap price to deny the Queen's bluffing equity and to fold out Y's own
King. Y answers with a raise, and the raise is what keeps X's blocker honest.
This regime has no clean closed form; it is a rapidly moving mixture.

### IV. Plateau (S ≥ 0.525)

At **S\* = 0.52544** the value reaches its ceiling and every strategy freezes.
The onset is not a coincidence: **S\* equals Y's own equilibrium bet size**
(0.52544 pots after a check). Once the stack covers Y's largest bet, no deeper
stack changes anything, because no equilibrium action ever wants more chips
than that. Beyond S\*, the game is stack-independent.

The frozen deep equilibrium (matching the book's qualitative description of
this game, now with exact frequencies):

- **X, first to act:** bets **0.162 pots** with a merged range — Ace 45%, King
  27%, Queen 6% (bluffs) — and checks the rest.
- **Y facing the bet:** raises to **0.409 pots** with every Ace plus 16% of
  Queens as bluff-raises; calls Kings 72%, folds Kings 28%; folds Queens.
- **X facing the raise:** calls all Aces, calls Kings ~31%, folds Queens.
- **Y after X checks:** bets **0.525 pots** with every Ace and 34% of Queens;
  checks back the rest. (X's King calls this bet 40% of the time; the Queen
  always folds.)

## Fidelity to the book

| Quantity | This solve | Note |
|---|---|---|
| Half-street NL AKQ value | 1/2 − √2/3 = **0.0285955** | exact anchor; bet size √2 − 1 |
| Polar-restricted value (King barred from betting) | **0.0276074** (closed radical) | LP matches to 10⁻⁸ |
| King's blocking bet exists | yes, enters at S ≈ 0.483 | the book's "Player X Strikes Back" point, quantified |
| Raises punish the blocker | yes; forbidding raises flips the game to X-favored (−0.0253) | confirms the book's reasoning |
| Full deep value | **≈ +0.0272 pots to Y** | this extension's headline number |

The blocking bet and the role of raises are **the book's** results (ch. 15);
what's new here is the exact numbers — the 0.162-pot blocker size, the merged
45/27/6 range, the 0.0272-pot deep value — and the **stack-size extension**:
the four-regime structure, the two exact short-stack laws, the tangent C¹
handoff at √2 − 1, and the plateau at S\* = Y's bet size.

## Oddities worth a second look

- **The value curve has a corner but no cliff.** V(S) rises smoothly (C¹) from
  0, then flattens completely. There is no stack size at which position is
  *harmed* by more chips; depth is weakly monotone and then exactly flat.
- **A √2 that shows up twice.** The constant √2 − 1 is both the optimal
  half-street bet size *and* the exact stack at which the jam-only regime ends.
  The game "remembers" the half-street solution as the depth where full-street
  betting first becomes feasible.
- **The plateau is self-referential.** Depth stops mattering exactly when the
  stack first covers the deepest bet the equilibrium ever makes. The game
  defines its own relevant stack ceiling.
- **Grid resolution beats raise depth.** Going from a coarse to a fine bet-size
  grid moves the deep value more (~8×10⁻⁵) than allowing a second re-raise
  (~3×10⁻⁵). No-limit "solutions" are only as exact as their bet-size grid.

## Files

| File | Contents |
|---|---|
| `solve.py` | Game tree, sequence-form LP, refined-grid solver, restricted-variant hooks, clean-plan tie-break |
| `experiments.py` / `experiments2.py` | Structure ablations (half-street, no-K-bet polar, raise-cap, min-bet) |
| `sweep.py` | 300-stack parallel sweep → `sweep.npz`, `strategies.json` |
| `analyze.py` | Exact anchors (sympy), regime-law verification, boundary bisection → `features.json`, `landmarks.json` |
| `cap_study.py` | Raise-cap-1 vs 2 vs 3 convergence → `cap_study.json` |
| `verify.py` | High-precision polar anchor + plateau-onset checks → `verify.json` |
| `make_artifact.py` / `akq_explorer.html` | Interactive explorer generator + output |

## Reproduce

```sh
python3 experiments.py     # structure ablations (~1 min)
python3 sweep.py           # 300-stack sweep, 8 cores (~2 min)
python3 analyze.py         # exact laws + boundaries (~1 min)
python3 verify.py          # precision checks (optional, ~10 min)
python3 cap_study.py       # raise-cap convergence (optional, slow)
python3 make_artifact.py   # regenerate the explorer
```

Requires Python 3 with numpy, scipy, and sympy.
