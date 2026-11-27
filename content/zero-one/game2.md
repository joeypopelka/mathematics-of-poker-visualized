# zero-one/game2.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

<!-- block: eyebrow -->
Chapter 11 · Example 11.3

<!-- block: 0-1-game-2 -->
[0,1] Game #2
      <span class="sub">the half-street game with folding — von Neumann's poker model, made live</span>

<!-- block: half-a-street-one -->
Half a street, one bet. **X must check in the dark**; then **Y** may bet or
      check, and if Y bets, X may **call or fold**. Hands are uniform on **[0, 1]** (0 = the
      nuts). Because X can now fold, Y starts to **bluff** — and the whole betting/bluffing/calling
      balance is governed by one number, the pot size **P**. This is the ancestor of Games
      #9–#11.

<!-- block: ex-showdown-expectation-to -->
Ex-showdown expectation to Y: **G = (1−α)² / [2(2−α)(1+α)]**.
        It rises from 0 (tiny pot, no betting) toward **¼** as P→∞ — exactly the no-fold
        Game&nbsp;#1 value. The dot marks the current pot.

<!-- block: bluffs-and-value-bets -->
Bluffs and value bets balance at ratio α (<span class="mono">1−y₀ = α·y₁</span>),
      and X folds α of the hands that could beat a bluff — each side making the other exactly
      indifferent. This is the α that runs through every later game.

<!-- block: model-amp-solution-from -->
Model &amp; solution from Bill Chen &amp; Jerrod Ankenman, <em>The Mathematics of
    Poker</em>, Example 11.3 (“[0,1] Game #2”), with the game value from Chapter 18 (Eq. 18.1). Exact
    closed forms: <code>α=1/(P+1)</code>, <code>y₁=(1−α)/[(2−α)(1+α)]</code>, <code>x₁\*=2y₁</code>,
    <code>y₀=1−αy₁</code>, <code>G=y₁(1−α)/2</code>. Originally von Neumann &amp; Morgenstern (1944).
    Companion to <code>game9.html</code>, <code>game10.html</code>, <code>game11.html</code>.

<!-- block: threshold-readout -->
Threshold readout

<!-- block: value-of-the-game -->
Value of the game to Y &nbsp;vs. pot

<!-- block: how-to-read-it -->
How to read it

<!-- block: y-bets-his-best -->
Y bets his best hands for **value** [0, y₁], **checks** the middle [y₁, y₀], and
      **bluffs** his worst [y₀, 1]. X **calls** his best [0, x₁\*] and **folds** the rest.
      The one lever is **α = 1/(P+1)**.

<!-- block: bet-half-of-what -->
**Bet half of what gets called.** The calling cutoff is <span class="mono">x₁\* = 2y₁</span> —
      Y value-bets exactly half the hands X will call with. And there'd be <em>no</em> bluffing without
      folding: if Y only value-bet, X would fold everything weak and Y couldn't get paid, so Y must
      bluff to drag X's calls down to [y₁, x₁\*].

<!-- block: the-value-of-position -->
**The value of position.** Being the player who gets to bet is worth
      <span class="mono">G</span> per hand — from 0 in a vanishing pot up to **¼ of a bet** in an
      enormous one. That ¼ is the pure value of the betting lead when folding no longer matters.
