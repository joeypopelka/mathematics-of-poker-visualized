<!-- block: page-title -->
[0,1] Game #11 — Live Figure (check-raise)

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

<!-- block: method -->
**How these numbers are computed — the sequence-form LP, and what it found.** The Y-side
    value thresholds (y₂, y₂\*, y₁, y₀) are the book's **exact closed forms** (Eq. 17.13). The
    rest come from an **exact sequence-form LP** (Koller–Megiddo–von&nbsp;Stengel;
    <code>seqlp.py</code>), gate-validated by reproducing Games&nbsp;#9 and #10's closed forms
    (x₁ = 5/21, x₂\* = 4/21, x₁\* = 68/105 at P=2) and the no-fold #7 limit. The LP settled the
    question CFR could not: **there is no crisp x₁.** At P=2 the optimal set pins X's total bet
    mass to **0.28763&nbsp;±&nbsp;0.00001** and total aggressive mass (bet + check-raise) to
    **0.37533&nbsp;±&nbsp;0.00001**, yet *every individual hand's* action probability can
    range over [0,1] — rigorously measured by maximizing/minimizing each hand's bet frequency over
    the optimal face. The same freedom holds for Y's give-up zone (call/raise-bluff/fold
    assignment on ≈[0.55,&nbsp;0.85]). The thresholds drawn here are the **canonical monotone
    representative** (aggression pushed lexicographically toward stronger hands — the selection
    that reproduces the book's own #9/#10 thresholds exactly). Under it, x₁\* ≈ 0.650 ≠ y₁\* ≈ 0.667
    (the book's predicted split, confirmed), y₁\* = y₂# (a representative with *no raise-bluffs*
    exists in the optimal face), and the old CFR "blur" at x₁ stands revealed as genuine
    equilibrium-set structure, not solver noise. The game value is exact:
    **G(Y) = 0.062142 at P=2** (N→∞ converged), confirming the region-sum formula.
