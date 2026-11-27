<!-- block: page-title -->
Jam-or-Fold: The Phase Diagram

<!-- block: eyebrow -->
Chapter 12 &middot; Example 12.3

<!-- block: jam-or-fold-at -->
Jam-or-Fold <span class="thin">at every temperature</span>

<!-- block: an-exhaustive-equilibrium-analysis -->
An exhaustive equilibrium analysis of Chen &amp; Ankenman's shove/fold no-limit
  hold'em game, from **1 big blind** to the frozen depths of **2,500**. Exact enumerated
  equities (1,712,304 boards per matchup), exact card removal, and a linear-program equilibrium
  at every stack size &mdash; the &ldquo;exhaustive analysis of this game&rdquo; that the book
  alludes to but never prints.

<!-- block: equities-are-exact-every -->
Equities are exact: every one of the 812,175 distinct hand-vs-hand matchups was
  reduced by suit isomorphism to 50,258 classes and enumerated over all
  <code>C(48,5)&nbsp;=&nbsp;1,712,304</code> boards (the 7-card evaluator was verified against the
  known frequency counts of all 133,784,560 seven-card hands). Equilibria are exact linear
  programs over behavioral strategies with full card-removal accounting, solved independently for
  both players at every stack size; the two LP values agree to &lt;10<sup>-6</sup> at every point.

<!-- block: range-explorer-drag-the -->
Range explorer
    <span class="sub">drag the stack size &mdash; watch the system melt</span>

<!-- block: the-phase-diagram-169 -->
The phase diagram
    <span class="sub">169 hands &times; stack size &mdash; every band edge is a phase transition</span>

<!-- block: temperature-curves-what-the -->
Temperature curves
    <span class="sub">what the whole system is doing as it cools</span>

<!-- block: catalog-of-oddities-selected -->
Catalog of oddities
    <span class="sub">selected phase transitions, auto-mined from the sweep</span>

<!-- block: method-amp-fidelity-to -->
Method &amp; fidelity to the book <span class="sub">how this was computed</span>

<!-- block: caption -->
Each row is one starting hand, ordered by the stack size at which it first
  enters the range; brightness is its equilibrium frequency. Reading right to left is cooling:
  ranges freeze out hand by hand until only **AA** survives. Broken or re-ignited bands are
  Chen's &ldquo;oddities&rdquo; &mdash; hands that are jammed at one stack size, abandoned at
  another, and sometimes recalled later. Hover for details.

<!-- block: caption-2 -->
All range-membership transitions with S &gt; <span id="thCut"></span> bb,
  refined by bisection. The full list continues to shallow stacks inside the data payload.
