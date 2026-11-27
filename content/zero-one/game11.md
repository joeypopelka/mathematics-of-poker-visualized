# zero-one/game11.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

<!-- block: eyebrow -->
Chapter 17 · Example 17.3

<!-- block: 0-1-game-11 -->
[0,1] Game #11
      <span class="sub">two bets, with check-raising — the strategy structure, made live</span>

<!-- block: one-full-street-two -->
One full street, **two bets left**, and now **X may check-raise**. Hands are
      uniform on **[0, 1]**, 0 the nuts. This is where the book stops giving a full closed-form
      solution. The **Y-side value thresholds are exact** (Eq. 17.13); everything else is now
      solved **exactly by sequence-form LP** — which settled the old open question: **x₁ is not a
      line.** The equilibrium pins X's *aggregate* frequencies to five decimal places while
      leaving each individual hand's assignment free; the X-side drawn here is the canonical
      (monotone, book-style) representative of that optimal set. Two new ideas appear: X
      check-raises among his strongest hands, and Y's value bets split into **bet-call** vs
      **bet-fold** to a check-raise.

<!-- block: ex-showdown-expectation-to -->
Ex-showdown expectation to Y (Chapter 18) — the <em>same</em> region formula
      as Game&nbsp;#10, and **exact here** because it depends only on the exact Y-side (y₁, y₂, y₀),
      not the approximate x₁. It rises toward **1/9** as P→∞ (the no-fold check-raise
      Game&nbsp;#7 value), and sits below Game&nbsp;#10 at every pot — the price Y pays for X gaining
      the check-raise. The dot marks the current pot.

<!-- block: in-game-10-no -->
In Game #10 (no check-raise) the ratio R = (1−α₂)/2 linked an <em>X</em>
        threshold to a <em>Y</em> threshold (y₂ = R·x₁). With check-raise it links two
        <em>Y</em> thresholds instead: <span class="mono">y₂ = R·y₁</span>. The recurrence shifts
        from X→Y to Y→Y.

<!-- block: model-from-bill-chen -->
Model from Bill Chen &amp; Jerrod Ankenman, <em>The Mathematics of Poker</em>,
    Example 17.3 (“[0,1] Game #11”: one street / two bets / check-raise allowed). The book gives the
    Y-side (Eq. 17.13) and the structural changes but omits full threshold values; the rest is solved
    numerically here. Companion to <code>game9.html</code>, <code>game10.html</code>.

<!-- block: value-of-the-game -->
Value of the game to Y &nbsp;vs. pot

<!-- block: threshold-readout -->
Threshold readout

<!-- block: what-check-raise-changes -->
What check-raise changes

<!-- block: the-value-regions-are -->
The value regions are what move; everything else cascades off them. The book solves the
        Y-side in closed form — the key result is **Eq. 17.13**:

<!-- block: x-check-raises-his -->
**X check-raises his best hands.** On his strongest region he is indifferent between
        check-raising and bet-calling, and he adds a band of **check-raise bluffs** among his
        give-up hands (◆). Betting a little of his strength as a trap lets him punish Y's bets.

<!-- block: y-bets-tighter-raises -->
**Y bets tighter, raises looser.** Fearing the check-raise, Y value-bets a narrower
        range after X checks, and splits it into **bet-call** [0, y₂\*] and **bet-fold**
        [y₂\*, y₁] — folding α₂ of his value bets to a check-raise
        (<span class="mono">y₂\* = (1−α₂)y₁</span>).

<!-- block: the-x1-y1-symmetry -->
**The x₁\* = y₁\* symmetry breaks.** In #9 and #10 those cutoffs coincided; here they
        separate, because X's post-check decision is no longer a clean call/fold — he can
        check-raise. That's the structural signature of this game.
