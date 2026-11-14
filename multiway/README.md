# Multiplayer Games (ch. 29)

A light single page, by design — the chapter's own message is that multiplayer
games have Nash equilibria but no "solutions": players can disturb an
equilibrium into implicit alliances, so "optimal" stops meaning anything.

**Live page:** https://joeypopelka.github.io/mathematics-of-poker-visualized/multiway/

Covered (`verify.py` checks every number):

- **The rock & the maniac** (Ex. 29.1): a symmetric, fully-disclosed,
  fair-looking game with EV **−$0.707** for the player in the middle — an
  alliance with no information exchange.
- **The dry side pot** [0,1] game (pot 9, one player all-in). **New erratum
  found:** the book's reported equilibrium (x ≈ 0.2848, y₁ ≈ 0.1424, bluff
  band 0.6424 ± 0.0095) does not satisfy the book's own three indifference
  equations and fails a direct no-deviation check (Y profitably bluffs hand
  0.5 for +0.68). The true simultaneous root — confirmed Nash by a fine-grid
  deviation check — is **x = 0.5178, y₁ = 0.2589, bluff band
  0.7589 ± 0.0242**. The chapter's qualitative lessons survive unchanged.
- **The clairvoyant maniac** (Ex. 29.4): Z's EV per value bet is
  *discontinuous* in his announced bluff ratio — 9/10 at equilibrium, worse
  at small over-bluffs (X snaps him off), then 17/10 at triple the
  equilibrium rate (Y gains overcalling odds). Over-bluffing recruits an
  ally, but only if announced.

```sh
python3 verify.py    # stdlib only, instant
```
