# zero-one/game9.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

<!-- block: page-title -->
[0,1] Game #9 — Live Figure 17.1

<!-- block: eyebrow -->
Chapter 17 · Example 17.1

<!-- block: 0-1-game-9 -->
[0,1] Game #9
      <span class="sub">mixing in bluffs — the strategy structure of Figure 17.1, made live</span>

<!-- block: one-full-street-one -->
One full street, one bet left. Both players hold a hand drawn uniformly on
      the interval **[0,&nbsp;1]**, where **0 is the nuts** and **1 is the worst hand**.
      X acts first; Y responds. Everything below is driven by a single quantity — the
      **pot size&nbsp;P**. Move it and watch the value-betting, bluffing, calling and folding
      regions breathe.

<!-- block: ex-showdown-expectation-to -->
Ex-showdown expectation to Y: **G = α(1−α)²/[2(1+α)]** (Chapter 18).
      It is <em>humped</em> — rising then falling, peaking near P≈2.6 at ≈0.057 — and → **0** as
      P→∞ (the no-fold Game&nbsp;#4 value: with an infinite pot nobody folds, so the one-bet
      full-street lead is worth nothing). The dot marks the current pot.

<!-- block: value-bets-and-bluffs -->
Value bets and bluffs are balanced so the opponent is exactly
        indifferent to calling — that indifference <em>is</em> the solution.

<!-- block: model-amp-closed-form -->
Model &amp; closed-form thresholds from Bill Chen &amp; Jerrod Ankenman,
    <em>The Mathematics of Poker</em>, Example 17.1 (“[0,1] Game #9”). Solution:
    <code>x₁=(1−α)²/(1+α)</code>, <code>y₁=(1−α)/(1+α)</code>, <code>x₁\*=y₁\*=1−α</code>,
    <code>y₀=(1+α²)/(1+α)</code>, <code>x₀=1−αx₁</code>. Verified against the book’s P=4 worked
    example (α=1/5 → x₁=8/15, y₁=2/3, x₁\*=4/5, y₀=13/15, x₀=67/75).

<!-- block: value-of-the-game -->
Value of the game to Y &nbsp;vs. pot

<!-- block: threshold-readout -->
Threshold readout

<!-- block: how-to-read-it -->
How to read it

<!-- block: the-one-lever-is -->
The one lever is **α = 1/(P+1)**, the “golden ratio of poker.” It is the fraction of
        hands the bettor bluffs relative to his value bets, and the fraction the caller must
        <em>fold</em> to stay unexploitable.

<!-- block: bigger-pot-smaller-more -->
**Bigger pot → smaller α → more action.** With more dead money to win, folding
        gets expensive, so both players bet, call, and bluff a wider slice of hands. As
        <span class="mono">P → ∞</span> every threshold marches to 1: it collapses to the
        no-fold games of Chapter&nbsp;16, where everyone value-bets and calls with everything.

<!-- block: as-p-0-the -->
As <span class="mono">P → 0</span> the pot isn’t worth fighting for, α → 1, and all the
        regions vanish into a single check-down.

<!-- block: notice-the-alignment-of -->
Notice the alignment of the gridlines: <span class="mono">y₁</span> always lands at the
        midpoint of X’s betting and calling thresholds — Y value-bets everything X would have,
        plus half the hands X would merely call with.
