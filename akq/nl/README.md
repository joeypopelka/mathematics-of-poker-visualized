# Chen Chapter 15: The No-Limit AKQ Game, Across Every Stack Size

An exact equilibrium solve of the one-street no-limit AKQ game from Chapter 15
of Chen & Ankenman's *The Mathematics of Poker* ("Player X Strikes Back"),
computed at **300 starting stack sizes** from 0.02 to 100 pots — an extension
the book motivates but never charts: **how stack depth changes the value of
position.**

**Full writeup and findings: [REPORT.md](REPORT.md)**

**Live interactive explorer: https://joeypopelka.github.io/mathematics-of-poker-visualized/akq/nl/**
(`akq_explorer.html` — self-contained single page)

Highlights:

- **Position helps — but only up to ~½ pot deep.** Y's (in-position) edge
  climbs from 0 to **+0.0272 pots** as the stack deepens to S ≈ 0.525, then
  freezes: for S ≥ 3 the value is flat to 10⁻¹⁶. A 1-pot stack and a 100-pot
  stack are worth exactly the same to position.
- **Four regimes, three exact.** Jam-only **V = S²/(6(1+S))** for S ≤ √2−1;
  a polar-bet law **V = (S/(1+S) − (3−2√2))/6** for √2−1 ≤ S ≤ 0.483; the
  King's blocking bet from 0.483; a stack-independent **plateau from
  S\* = 0.5254**. Closed forms verified against the LP to ~10⁻¹⁷.
- **A √2 that appears twice.** The half-street optimal bet √2−1 is *also* the
  exact stack at which the jam-only regime ends — and the two short-stack laws
  meet there with matching value and slope (a C¹-smooth phase boundary).
- **The plateau is self-referential.** Depth stops mattering exactly when the
  stack first covers Y's own largest equilibrium bet (0.5254 pots).
- Reproduces the book's ch. 15 results — the King's blocking bet and the raises
  that punish it — and pins down their exact numbers (0.162-pot blocker, merged
  45/27/6 range, +0.0272-pot deep value).

## Reproduce

```sh
python3 experiments.py     # structure ablations (~1 min)
python3 sweep.py           # 300-stack sweep, 8 cores (~2 min)
python3 analyze.py         # exact laws + regime boundaries (~1 min)
python3 make_artifact.py   # regenerate the interactive explorer
```

Requires Python 3 with numpy, scipy, and sympy. `sweep.npz`,
`strategies.json`, `features.json`, and `landmarks.json` are checked in, so the
explorer rebuilds without redoing the sweep.

## Method in one paragraph

The game tree is solved exactly by sequence-form linear programming (both
players' LPs, strong-duality checked). No-limit bet/raise sizes are discretized
on a grid refined around the equilibrium support until the value converges;
raises are capped at one and validated against deeper caps (correction
< 3×10⁻⁵). Three regimes have hand-derived closed forms verified to machine
precision; the deep regime is numerical and cross-checked against a polar
restriction with a closed-radical value.
