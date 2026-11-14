# The Limit AKQ Game (ch. 13)

The gateway game of the AKQ family: three-card deck, pot P, one half street of
limit betting (Examples 13.1–13.2). Closed forms

- Y bluffs a Queen with probability `b* = 1/(P+1) = α`
- X calls with a King with probability `c* = (P−1)/(P+1)`
- game value to Y `G = (P−1)/(6(P+1))` → 1/6 as P → ∞, zero for P ≤ 1

verified in `solve.py` against an independent saddle-point solve of the full
payoff matrix. Reproduces the book's Game #1 numbers (b = c = 1/3, G = 1/18 at
P = 2); one footnote: p. 144 prints the bluff ratio at P = 1.1 as "10/11",
which contradicts the book's own formula — 1/(P+1) = **10/21**.

**Live page:** https://joeypopelka.github.io/mathematics-of-poker-visualized/akq/limit/

```sh
python3 solve.py     # verification + akq_limit.json
```

The no-limit continuation (ch. 15 appendix) lives in [`../nl/`](../nl/).
