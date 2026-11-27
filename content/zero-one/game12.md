# zero-one/game12.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

<!-- block: eyebrow -->
Chapter 17 · Example 17.4

<!-- block: 0-1-game-12 -->
[0,1] Game #12
      <span class="sub">folding + an unlimited raising ladder — the last finite-pot [0,1] game</span>

<!-- block: one-full-street-folding -->
One full street, folding allowed, **no check-raise**, but now an
      **arbitrary number of bets and raises**. X acts first; each raise can be re-raised, forever.
      The new character is **Rₚ** — a pot-dependent generalization of the golden ratio r that sets
      the ratio between each threshold and the next, generating an **infinite cascade of value
      thresholds** marching toward the nuts. As P→∞ it becomes the no-fold Game&nbsp;#6.

<!-- block: once-you-pass-the -->
Once you pass the second raise the game is self-similar: every two further
        bets repeat the same ratios into an ever-larger pot. So the value thresholds form a cascade
        x₁ → y₂ → x₃ → y₄ → … each ≈ Rₚ times the last, converging geometrically to the nuts.

<!-- block: model-from-bill-chen -->
Model from Bill Chen &amp; Jerrod Ankenman, <em>The Mathematics of Poker</em>,
    Example 17.4 (“[0,1] Game #12”: full street / folding / unlimited bets / no check-raise). Exact
    core: Rₚ solves Eq. near 17.14; <code>x₁=(1−α)²/[1+α+(2−α)(1−α₂)Rₚ]</code>; cascade
    <code>yₙ=Rₚ·xₙ₋₁</code>; lower thresholds as in Game&nbsp;#10. Verified at P→∞ against Game&nbsp;#6
    (x₁→1/(1+2r), y₂→r·x₁). Finite-pot game value: exact sequence-form LP
    (<code>seqlp.py</code> / <code>game12_value.json</code>). Companion to
    <code>game2/9/10/11.html</code>.

<!-- block: the-raising-ladder-nbsp -->
The raising ladder &nbsp;(value thresholds → the nuts)

<!-- block: rp-nbsp-vs-pot -->
Rₚ &nbsp;vs. pot &nbsp;(→ r = √2−1)

<!-- block: threshold-readout -->
Threshold readout

<!-- block: what-the-endless-ladder -->
What the endless ladder changes

<!-- block: every-equation-from-game -->
Every equation from Game&nbsp;#10 survives <em>except</em> the one at y₂ — because Y can now be
        re-raised. The fix is that the key relation <span class="mono">y₂ = R·x₁</span> keeps its form
        but R is no longer the fixed (1−α₂)/2; it becomes the pot-dependent **Rₚ**.

<!-- block: the-lower-structure-is -->
**The lower structure is unchanged.** Adding more bets moves Rₚ (and hence x₁) but not the
        relationships among the low thresholds, so y₁, x₁\*, y₀, x₀ follow the same formulas as
        Game&nbsp;#10. And since there's no check-raise, <span class="mono">x₁\* = y₁\*</span> again.

<!-- block: as-p-rp-r -->
As <span class="mono">P → ∞</span>, Rₚ → r and x₁ → 1/(1+2r) ≈ 0.547: the exact solution of
        the no-fold Game&nbsp;#6, with its r-geometric threshold ladder.
