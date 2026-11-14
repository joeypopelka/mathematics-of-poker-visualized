# Mathematics of Poker, Visualized

Exact computational companions to Bill Chen & Jerrod Ankenman's *The
Mathematics of Poker* — every game family in the book re-solved from scratch,
every printed number reproduced or flagged as an erratum, and the "exhaustive
analyses" the book alludes to but never prints, actually carried out.

**Live site: https://joeypopelka.github.io/mathematics-of-poker-visualized/**

| Family | Chapters | Folder | Headline |
|---|---|---|---|
| The AKQ game, limit | 13 | [`akq/limit/`](akq/limit/) | α = 1/(P+1) in its purest form; value (P−1)/6(P+1) |
| The AKQ game, no-limit | 15 + app. | [`akq/nl/`](akq/nl/) | position's value freezes at S\* = 0.5254 pots; 3 exact regime laws |
| The [0,1] games | 11, 16–18 | [`zero-one/`](zero-one/) | sequence-form LP: #11's x₁ is a band; #12's unpublished value = 0.06696 at P=2 |
| Jam-or-fold | 12 | [`jam-or-fold/`](jam-or-fold/) | exact equilibrium at 1,379 stacks; ATs at S = 833.93; crossover S\* = 7.797 |
| Multi-street games | 14, 19 | [`multi-street/`](multi-street/) | geometric growth of pot; the $185 case study sign-flip |
| Risk | 22–25 | [`risk/`](risk/) | RoR / RoRU / Kelly / backing-as-options; the $9,647.50 cutoff erratum |
| Tournaments | 26–28 | [`tournaments/`](tournaments/) | 46/46 worked numbers; four ICM models; bubble factors |
| Multiplayer | 29 | [`multiway/`](multiway/) | alliances; the unbeatable fair game; a new equilibrium erratum |

Each folder has its own `README.md` (reproduction instructions) and, for the
larger projects, a `REPORT.md` with findings. Each `index.html` is a
self-contained interactive explorer (vanilla JS + Canvas, no dependencies, no
build step — works offline and on GitHub Pages).

## Errata found in the book

All verified against the book's own equations in the corresponding solvers:

1. **p. 130 (ch. 12)** — A5s vs AA equity is exactly **0.13307**, not 0.13331.
2. **p. 144 (ch. 13)** — bluff ratio at P = 1.1 is **10/21**, not "10/11".
3. **ch. 22** — two imprecise numeric solves: SNG α = **0.000606** (printed
   ≈0.000632 / once "0.00632"); winner-take-all α = **0.016153** (printed
   0.01683); and σ = 14.036 forgot to subtract μ² (exact 14.0).
4. **ch. 24, Ex. 24.2** — the game-selection cutoff is **c = $9,647.50**; the
   book prints its own 2c as c.
5. **ch. 25** — backer's share **$1,546.64**, not $1,547.64.
6. **ch. 27** — Landrum-Burns P3 = **$1,166.67** (printed $1,066.67); variance
   multiple **53.263** (printed 53.6456).
7. **ch. 29, Ex. 29.2** — the dry-side-pot equilibrium is **x = 0.5178,
   y₁ = 0.2589, bluff band 0.7589 ± 0.0242**; the printed x ≈ 0.2848 fails the
   book's own indifference system and a direct no-deviation check.

## Method

Exact over approximate, everywhere: full enumeration for preflop equities
(evaluator verified against the known frequency counts of all 133,784,560
seven-card hands), sequence-form / direct LP with strong-duality assertions
for equilibria, closed forms re-derived and verified by independent numerics,
and strict EV-margin checks so solver degeneracy can't masquerade as a
finding.

Heavy intermediate data (`equity.f32`, `sweep.npz`, …) is checked in, so the
Python analysis steps run without redoing the C enumeration. Per-folder
reproduction commands are in each README; the only requirements are a C
compiler (jam-or-fold only) and Python 3 with numpy/scipy (several projects
are stdlib-only).

Built with the help of Claude (Anthropic).
