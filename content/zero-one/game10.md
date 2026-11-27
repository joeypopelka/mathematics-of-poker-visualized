# zero-one/game10.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

<!-- block: eyebrow -->
Chapter 17 · Example 17.2

<!-- block: 0-1-game-10 -->
[0,1] Game #10
      <span class="sub">introducing the raise — the strategy structure of Figure 17.2, made live</span>

<!-- block: one-full-street-two -->
One full street, **two bets left**, no check-raising. Hands are uniform on
      **[0, 1]** with **0 the nuts** and **1 the worst hand**. X acts first; Y responds and
      may now **raise**. That single addition forces two new ideas: X must decide, when he value
      bets, whether he'll **call or fold a raise**, and Y builds a **raise-bluffing** range. As
      before, everything is driven by the **pot size&nbsp;P**.

<!-- block: ex-showdown-expectation-to -->
Ex-showdown expectation to Y (Chapter 18), summed over X's best-response
      regions. It rises with the pot toward **⅛** as P→∞ — exactly the no-fold two-bet
      Game&nbsp;#5 value. Adding the raise makes it larger than one-bet Game&nbsp;#9 at every pot.
      The dot marks the current pot.

<!-- block: r-1-2-2 -->
R = (1−α₂)/2 is the ratio of Y's value raises to X's value bets:
        <span class="mono">y₂ = R·x₁</span>. It bundles two things — Y raises with <em>half</em> the
        hands X will continue with (X can't re-raise, so it's the clean one-half), times the
        <em>(1−α₂)</em> fraction of value bets X actually keeps in to face a raise. As the pot grows
        α₂ → 0 and R → 1/2: Y raises with half of what X bets, exactly as in the no-fold
        Game&nbsp;#6. The (1−α₂) is the finite-pot correction for X folding to the raise.

<!-- block: model-amp-closed-form -->
Model &amp; closed-form thresholds from Bill Chen &amp; Jerrod Ankenman,
    <em>The Mathematics of Poker</em>, Example 17.2 (“[0,1] Game #10”, one street / two bets /
    no check-raise). Solver uses the reduced relation <code>x₁=(1−α)²/[1+α+(2−α)(1−α₂)R]</code>
    with R=(1−α₂)/2, then Eqs. 17.2–17.11. Verified against the book's table at P = 1, 2, 9, ∞
    (e.g. P=2 → x₁=5/21, y₁=279/630, x₁\*=68/105, y₂=2/21, x₂\*=4/21). Companion to
    <code>game9.html</code> (Example 17.1).

<!-- block: value-of-the-game -->
Value of the game to Y &nbsp;vs. pot

<!-- block: threshold-readout -->
Threshold readout

<!-- block: what-the-raise-changes -->
What the raise changes

<!-- block: a-second-bet-introduces -->
A second bet introduces a second ratio. The general rule is
        **αₙ = 1/(P + (2n−1))**: the one-bet α₁ = 1/(P+1) still governs betting and bluffing,
        while **α₂ = 1/(P+3)** now governs the raise, since a raise puts two more bets into a
        bigger pot.

<!-- block: x-now-splits-his -->
**X now splits his value bets.** With his strongest hands [0, x₂\*] he bets and
        <em>calls</em> a raise; with the next slice [x₂\*, x₁] he bets and <em>folds</em> to a raise.
        He folds α₂ of his value bets, because he must make Y indifferent to raise-bluffing:
        <span class="mono">x₂\* = (1−α₂)x₁</span>.

<!-- block: y-raise-bluffs-from -->
**Y raise-bluffs from the top of his give-up range,** [y₁\*, y₂#] — the strongest of the
        hands he'd otherwise fold — and folds the rest, [y₂#, 1]. Those give-up hands never reach a
        showdown, so there's no showdown value to protect; bluffing the strongest of them is the
        non-dominated choice. In total Y folds α of his hands to a bet:
        <span class="mono">y₂# = 1−α</span>.

<!-- block: as-before-x1-y1 -->
As before <span class="mono">x₁\* = y₁\*</span> coincide, and as
        <span class="mono">P → ∞</span> every threshold marches to 1 and the game collapses to the
        no-fold Chapter&nbsp;16 games; as <span class="mono">P → 0</span>, all action vanishes.
