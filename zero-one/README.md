# The [0,1] Games (ch. 11, 16–18)

The book's continuous-hand family: hands uniform on [0,1] (0 = nuts), pot P,
limit bets of 1 — from von Neumann's half-street game through bets, raises,
check-raises, and unlimited raising. Five interactive artifacts, one per game,
plus an exact sequence-form LP solver that settles the two questions the book
(and an earlier CFR attempt) left open.

**Live hub:** https://joeypopelka.github.io/mathematics-of-poker-visualized/zero-one/

| Game | Book | Page | Status |
|---|---|---|---|
| #2 half-street (von Neumann) | Ex. 11.3 | `game2.html` | exact closed forms |
| #9 one bet | Ex. 17.1 | `game9.html` | exact closed forms |
| #10 two bets, no check-raise | Ex. 17.2 | `game10.html` | exact closed forms |
| #11 two bets, check-raise | Ex. 17.3 | `game11.html` | **exact LP** (book stops here) |
| #12 unlimited raises | Ex. 17.4 | `game12.html` | Rₚ cascade + **exact LP value** |

Headline results from the LP (`seqlp.py`, `exact_run.py` — full writeup in
[REPORT.md](REPORT.md)):

- **Game #11's x₁ is not a line.** The equilibrium pins X's aggregate
  frequencies to 1e-5 while leaving every individual hand's assignment free; a
  lexicographic "monotone selection" (which exactly reproduces the book's
  #9/#10 thresholds) supplies the canonical representative, under which
  x₁\* = 0.650 ≠ y₁\* = 0.667 — the book's predicted check-raise split,
  confirmed exactly.
- **Game #12's finite-pot value — which the book declines to compute — is
  G(Y) = 0.06696 at P = 2** (full curve in `game12_value.json`), converged by
  a 6-bet raise cap, and *below* game #10's value at every finite pot: the
  third bet is X's option.
- All four finite-pot value curves (#9/#10/#11/#12) computed exactly
  (`values_fp.json`), each converging to its no-fold limit (0, 1/8, 1/9,
  1/16 + r/8).

Reproduce:

```sh
python3 seqlp.py --validate 200   # gates: #9/#10 closed forms, #7 limit, B=2==#10
python3 exact_run.py              # ~9 min: grids, band analysis, value curves
```

Requires Python 3 with numpy + scipy. `Q&A_notes.md` holds the running study
notes (threshold tables, the α catalog, 17 Q&As).
