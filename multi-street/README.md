# Multi-Street Games (ch. 14 + 19)

No-limit bet sizing on one street (ch. 14) and across many (ch. 19) — the home
of the book's most quoted result, the **geometric growth of pot**: with static
hands, the optimal sizing grows the pot by the same ratio
`G = (1+2S)^(1/M)` on every street, landing all-in on the river.

**Live page:** https://joeypopelka.github.io/mathematics-of-poker-visualized/multi-street/

Covered, with every printed number reproduced (`solve.py`, all asserts):

- 14.1 clairvoyance → jam; the strong-range "claim the pot" regime
- 14.2 NL AKQ → `s* = √2−1` (and the quiet oddity that X's calling frequency
  at s\* is also exactly r)
- 14.3 NL [0,1] half street → `x₀ = 6/7`, bet-size functions verified by
  numerical best-response
- 19.1 two-street limit clairvoyant (verified by independent LP) + the
  three-street 1/2/2 game (Y bets 7/8; value +1.5)
- 19.2/19.4 geometric growth optimality (grid max confirms r₁ = r₂)
- 19.3 the $185 case study: flat $60 ($19.16/winner, net −$0.51) vs geometric
  ($26.41/winner, net +$0.60) — sizing alone flips the game's sign
- 19.5/19.6 the auction game `x(s) = 1/√(1+2s)`, `y(s) = y√((1+2S)/(1+2s))`,
  and its equivalence to the M→∞ geometric game (verified at M=1000)

```sh
python3 solve.py     # all verifications + multistreet.json
```
