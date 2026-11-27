# zero-one/index.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

<!-- block: page-title -->
The [0,1] Games — Mathematics of Poker, Visualized

<!-- block: eyebrow -->
Chapters 11 &amp; 16–18

<!-- block: the-0-1-games -->
The [0,1] Games

<!-- block: chapters-11-amp-16-2 -->
Chapters 11 &amp; 16–18 of Chen &amp; Ankenman's *The Mathematics of Poker*:
  hands uniform on [0,1] (0 = the nuts), pot P, limit bets of 1 — poker reduced to pure
  betting structure. One interactive page per game, from von Neumann's 1944 half-street
  model to the unlimited-raise ladder, plus an exact sequence-form LP that settles what
  the book leaves open.

<!-- block: exact-game-value-to -->
Exact game value to Y (ex-showdown) by pot size, all four finite-pot games
    (sequence-form LP; <code>values_fp.json</code>). Dashed: the P→∞ no-fold limits. Note the strict
    ordering <span style="color:var(--red)">#9</span> &lt; <span style="color:var(--purple)">#11</span>
    &lt; <span style="color:var(--green)">#12</span> &lt; <span style="color:var(--ice)">#10</span> at
    every pot beyond the tiny ones: Y's raise option (#9→#10) is worth the most; giving X the
    check-raise (#10→#11) or the re-raise war (#10→#12) hands part of it back. #9's curve is the odd
    one — it *humps* near P ≈ 2.6 and falls to zero, because with one bet and no raises, a huge
    pot makes the bettor's edge evaporate (its no-fold limit is Game #4's value: zero).

<!-- block: the-games -->
The games

<!-- block: one-chart-what-each -->
One chart: what each strategic option is worth

<!-- block: the-catalog -->
The α catalog

# -- recovered in audit pass --

<!-- block: card -->
Von Neumann's poker model — the first solved poker game. One bet, X checks dark.
      The birthplace of α = 1/(P+1).

<!-- block: card-2 -->
X may now bet. Thresholds interleave; x₁\* = y₁\* = 1−α — one price for
      bluff-catching on both sides.

<!-- block: card-3 -->
The raise arrives, with raise-bluffs. The 1−α boundary relocates to y₂#; the
      R-ratio links Y's raises to X's bets.

<!-- block: card-4 -->
Where the book stops publishing solutions. The LP shows why: x₁ is a *band* —
      aggregates pinned to 1e-5, assignments free. Canonical selection + exact value inside.

<!-- block: card-5 -->
The Rₚ cascade of value thresholds marching to the nuts — and the finite-pot
      game value the book declined to compute, now exact.

<!-- block: card-6 -->
Methods, validation gates, the band-structure finding, the #12 value curve,
      and the full file map. Study notes in Q&amp;A_notes.md.

<!-- block: fid -->
bluff : value ratio; caller's fold share — "the golden ratio of poker"

<!-- block: fid-2 -->
the same, for the nth bet into the enlarged pot

<!-- block: fid-3 -->
the golden mean of poker: #12's P→∞ ladder, the NL AKQ bet, the α at P=√2
