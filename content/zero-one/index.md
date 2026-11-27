# zero-one/index.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

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
