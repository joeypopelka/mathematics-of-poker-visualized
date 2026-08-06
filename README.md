# Chen Chapter 12: Jam-or-Fold NLHE, Exhaustively Analyzed

An exact equilibrium analysis of the shove/fold no-limit hold'em game from
Chapter 12 (Example 12.3) of Chen & Ankenman's *The Mathematics of Poker*,
at every stack size from 1 to 2,500 big blinds — the "exhaustive analysis of
this game" the book alludes to on p. 131 but never prints.

**Full writeup and findings: [REPORT.md](REPORT.md)**

**Live interactive explorer: https://joeypopelka.github.io/Chen-ch12-shove-fold/**

Highlights:

- Exact preflop equities (all 812,175 matchups × 1,712,304 boards), exact
  card removal, and an exact LP equilibrium at 1,379 stack sizes.
- Reproduces Chen's landmark numbers: ATs joining AA at S = 833.25 (his
  convention; 833.93 under fully consistent accounting), his three starred
  "broken strategy" hands (63s/53s/43s), and the S=10 jam/call fractions.
- One book erratum found: A5s vs AA is exactly **0.13307**, not the printed
  0.13331 — which moves the forced mixing at S = 833 from ATs onto A5s.
- 21 hands with strictly-verified "gap" windows where they leave the jam
  range and return (ATs vanishes twice, mirrored exactly by the defender's
  AKs calling windows).
- An interactive phase-diagram explorer (`shove_fold_explorer.html` — a
  single self-contained page; open it in any browser).

## Reproduce

```sh
clang -O3 -march=native -o equity equity.c -lpthread
./equity --selftest        # verify the 7-card evaluator (exact frequencies)
./equity 8                 # ~10 min on 8 cores -> equity.f32 (included in repo)
python3 solve.py           # 169-class reduction, LP sweep, thresholds
python3 analyze.py         # strict-margin verification, band structure
python3 make_artifact.py   # regenerate the interactive explorer
```

Requires clang (or any C11 compiler with pthreads), Python 3 with numpy and
scipy. `equity.f32` and `sweep.npz` are checked in, so the Python steps run
without redoing the C enumeration.
