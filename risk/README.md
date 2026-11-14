# Risk (ch. 22–25)

Staying in action: risk of ruin, uncertain win rates, the Kelly criterion, and
poker finance (swaps, Sharpe ratios, backing agreements as options). Pure
closed-form / stdlib arithmetic in the spirit of the tournaments project —
every script runs sub-second.

**Live page:** https://joeypopelka.github.io/mathematics-of-poker-visualized/risk/

Covered, with every worked number reproduced (`solve.py`, all asserts):

- ch 22: `R(b) = e^{−αb}` from `R(a+b)=R(a)R(b)`; the die game (α = ln 2);
  Eq. 22.2 solved for the SNG, winner-take-all, limit and NL distributions;
  `α = 2μ/σ²` for normal outcomes **re-derived by numerical integration**;
  half-bankrolls.
- ch 23: the RoRU closed form (Eq. 23.1) re-derived by numerical integration;
  the going-pro case study (0.98% → 3.67% uncertain; 6.22% → 17.25% after
  paying yourself 1 bet/100).
- ch 24: Kelly bet sizing (3% edge → bet 3%); optimal bankroll; the
  game-selection cutoff `2c = μ₁+μ₂+(σ₁²−σ₂²)/(μ₁−μ₂)`.
- ch 25: Sharpe ratio, the 36% tournament swap, and backing agreements priced
  as call options (Eqs. 25.6/25.7), including the 6-tier schedule to the cent.

Book slips found and verified:

1. **Ch 24, Example 24.2 (the substantive one): the printed game-selection
   cutoff "c = $19,295" is actually 2c** — the cutoff is **$9,647.50**,
   confirmed by direct utility crossover.
2. Ch 22: the SNG α ≈ 0.000632 doesn't satisfy the book's own equation
   (g(0.000632) = 1.0009); the exact root is **0.000606** (and one paragraph
   prints "0.00632", dropping a zero).
3. Ch 22: the winner-take-all α ≈ 0.01683 likewise; exact root **0.016153**
   (R(100) = 19.9%, not 18.6%); and its σ = 14.036 = √E[x²] forgot to
   subtract μ² (exact σ = 14.0). The chapter's conclusions are unaffected.
4. Ch 25: the backer's share $1,547.64 is a $1 slip for $1,546.64.

```sh
python3 solve.py     # all verifications + risk.json (stdlib only)
```
