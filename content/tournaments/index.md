# tournaments/index.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

<!-- block: page-title -->
Chen ch. 26–28 · Tournaments

<!-- block: eyebrow -->
Chapters 26–28

<!-- block: tournaments-a-tournament-chip -->
Tournaments <span class="sub">a tournament chip is not a dollar</span>

<!-- block: reproducing-the-tournament-chapters -->
Reproducing the tournament chapters of Chen &amp; Ankenman's
    *The Mathematics of Poker*, then charting the continuous structure the
    book only samples. Skill decouples chips from equity early (ch. 26); the
    payout structure decouples them near the money (ch. 27); both reshape correct
    play (ch. 28). **46/46** of the book's worked numbers reproduced.

<!-- block: the-chip-value-curve -->
The chip-value curve <span class="mono">E = S<sup>β</sup></span>,
        β = −log₂C

<!-- block: the-decision-the-theory -->
The decision the theory flips

<!-- block: rebuy-add-on-value -->
Rebuy / add-on value <span class="k">(ch. 28, on the doubling-up engine)</span>

<!-- block: four-equity-formulas-one -->
Four equity formulas, one final table

<!-- block: where-the-models-disagree -->
Where the models disagree — the leader's equity

<!-- block: the-game-of-chicken -->
The game of chicken (Example 28.1)

<!-- block: required-equity-to-call -->
Required equity to call, on the bubble

<!-- block: the-bubble-factor-icm -->
The bubble factor <span class="k">— ICM premium as a multiplier on
        ch. 12 jam/fold ranges</span>

<!-- block: a-player-s-equity -->
A player's equity as a function of his stack fraction **S**, for a
        chance-of-doubling **C**. C = 0.5 is exactly linear (chips = equity).
        Skilled players (C &gt; 0.5) sit *above* the line — a skill premium —
        yet the curve is concave, so each marginal chip is still worth less than
        the last. Losing players (C &lt; 0.5) sit below and should court variance.

<!-- block: 250-player-nlhe-3 -->
250-player NLHE, ¾-buy-in edge ⇒ C = 0.5364. A river check-raise all-in:
        call 2050 to win 4025, 36% equity. Chip-EV says call (+137 chips). The
        Theory of Doubling Up says fold.

<!-- block: case-2-1-000 -->
Case 2: 1,000,000 chips in play, $90,000 pool, a 1500-chip add-on. Its
        cash value as your stack grows, for three skill levels. The discounted
        add-on ($100) clears its cost all the way to a huge stack; the at-par
        rebuy ($150) has a much earlier break-even.

<!-- block: stacks-25k-20k-10k -->
Stacks 25k / 20k / 10k / 5k, payouts $2000 / 1400 / 900 / 700. Proportional
        Chip Count (lower bound) and Landrum-Burns (upper bound) sandwich the two
        accurate models. Every number here matches the book.

<!-- block: slide-the-chip-leader -->
Slide the chip leader from an even 15k up to a dominating 48k (the other
        three share the rest). The gap between Proportional Chip Count and
        Landrum-Burns is the band of plausible fair value; a final-table deal
        lives inside it. Prop-chip crosses *above first-place money* — its
        fatal flaw — where the dashed line marks $2,000.

<!-- block: confrontations-aren-t-constant -->
Confrontations aren't constant-sum — every other player gains when two
          collide — so being *first* all-in is an edge. Three equilibria; the
          sequential first-mover claims the favorable one.

<!-- block: the-step-into-the -->
The step into the money forces a risk premium: the equity you need to
          call off your stack far exceeds the chip-EV break-even.

<!-- block: a-5-3-2 -->
A 5-3-2 sit-and-go, hero facing a jam as his own stack varies (others
        share the rest). The required calling equity ÷ the chip-EV threshold is
        the factor by which your ch. 12 shove/call ranges must tighten. It peaks
        for a middling stack and drops below 1 for a dominant leader, who can
        call *lighter* than chip-EV.

# -- recovered in audit pass --

<!-- block: note -->
Folding (0.009269) beats calling (0.008857): passing up a
        thin edge protects the skill you'll deploy over many future doubles.

<!-- block: note-2 -->
Reproduces the book: at 6000 chips E = $953, at 7500
        chips E = $1,162, so the $100 add-on (worth ≈ $209) is automatic; at-par
        break-even (C = 0.51) sits near a 8,325 stack.

<!-- block: note-erratum -->
Book erratum flagged: Landrum-Burns P3 prints as
        $1,066.67, but the sum-to-pool identity forces $1,166.67 (a typo).
