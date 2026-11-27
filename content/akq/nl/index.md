# akq/nl/index.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

<!-- block: chapter-15-middot-no -->
Chapter 15 &middot; No-Limit AKQ

<!-- block: what-position-is-worth -->
What position is worth &mdash; <em>and how deep it stops mattering</em>

<!-- block: the-one-street-no -->
The one-street no-limit AKQ game, solved exactly at 300 stack
  sizes. The player in position profits at every depth &mdash; but the edge
  **climbs only until the stack is about half a pot**, then freezes at
  **+0.0272 pots** and never moves again. Drag the stack to watch the
  equilibrium reorganize.

<!-- block: each-stack-size-is -->
Each stack size is solved exactly by **sequence-form linear
  programming** &mdash; both players&rsquo; LPs, with a strong-duality check.
  No-limit bet and raise sizes are discretized on a grid refined around the
  equilibrium support until the value stops moving; raises are capped at one and
  validated against deeper caps (correction &lt; 3&times;10&#8315;&#8309;). The
  three short-stack regime laws are hand-derived and verified against the LP to
  ~10&#8315;&sup1;&#8311;. The King&rsquo;s blocking bet and the raises that
  punish it are Chen &amp; Ankenman&rsquo;s results from ch.&nbsp;15
  (&ldquo;Player X Strikes Back&rdquo;); the exact bet sizes, ranges, the
  four-regime structure, and the plateau are this project&rsquo;s extension.
  Full writeup in <code>REPORT.md</code>.

<!-- block: the-value-of-position -->
The value of position vs. stack depth
    <span class="sub">Y&rsquo;s equilibrium profit, in pots &mdash; the whole story lives under one pot</span>

<!-- block: how-often-each-line -->
How often each line gets played
    <span class="sub">Betting-line frequencies across stack depth</span>

<!-- block: the-four-regimesreading-upward -->
The four regimes<span class="sub">Reading upward from an all-in short stack</span>

<!-- block: methodhow-the-numbers-are -->
Method<span class="sub">How the numbers are made</span>

<!-- block: bets-are-tiny-next -->
Bets are tiny next to the pot, so everything collapses to jam-or-call.
      X jams every **Ace** and some **Queens**; the King never jams.

<!-- block: the-stack-covers-the -->
The stack covers the optimal bet. X bets **&radic;2&minus;1** of pot
      with a polar range (nut Aces + Queen bluffs); Y jams behind. Hands off
      from regime&nbsp;I with matching value <em>and</em> slope.

<!-- block: the-book-rsquo-s -->
The book&rsquo;s move switches on: X&rsquo;s **King makes a small
      blocking bet**. The bet size <em>collapses</em> from 0.41 toward 0.16 as
      the range merges. Y&rsquo;s raise keeps it honest.

<!-- block: value-freezes-at-0 -->
Value freezes at **+0.0272 pots** and every strategy locks. Onset =
      Y&rsquo;s largest bet size: once chips cover that, more stack is dead
      weight. Flat to 10&#8315;&sup1;&#8310;.
