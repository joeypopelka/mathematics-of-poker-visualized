# Risk — page text
# Edit this file, then run `python3 build.py` (or just push — the
# GitHub Action rebuilds automatically). Markdown: **bold**, *italic*,
# `math` for mono styling; raw HTML like <sub>/<span class="m"> also works.

<!-- block: eyebrow -->
Chapters 22–25

<!-- block: title -->
Risk

<!-- block: lede -->
Chapters 22–25 of Chen &amp; Ankenman's *The Mathematics of Poker*:
  staying in action. Risk of ruin as an exponential law, what happens when you admit you
  don't know your own win rate, the Kelly criterion for choosing games, and poker as
  finance — swaps, Sharpe ratios, and backing agreements priced as options.

<!-- block: s22-h -->
Risk of ruin is an exponential (ch. 22)

<!-- block: s22-intro -->
From one axiom — <span class="m">R(a+b) = R(a)·R(b)</span>, losing two stacked
  bankrolls means losing each — ruin probability must be
  <span class="m">R(b) = e<sup>−αb</sup></span>. The constant α solves
  <span class="m">⟨e<sup>−αx</sup>⟩ = 1</span> over the game's outcome distribution;
  for (approximately) normal outcomes, <span class="m">α = 2μ/σ²</span>.

<!-- block: s22-note -->
Ruin probability against bankroll (bets). Dots mark successive
    **half-bankrolls** b<sub>½</sub> = ln2/α — each one halves the risk, like half-lives of a
    radioactive sample. Caveats the book is emphatic about: skim profit off the top and your true
    R is 100%; tournament distributions are too skew for the normal formula (their direct α gives
    roughly *half* the normal approximation's ruin probability in the winner-take-all example).

<!-- block: s23-h -->
Risk of ruin when you don't know your win rate (ch. 23)

<!-- block: s23-intro -->
Your observed win rate after N hands is itself a random variable with standard error
  <span class="m">σ<sub>w</sub> = s/√N</span>. Weighting the ruin probability over that
  uncertainty gives the closed form <span class="m">RoRU = R(w,b)·e<sup>2b²σ<sub>w</sub>²/σ⁴</sup>·Φ((w−2bσ<sub>w</sub>²/σ²)/σ<sub>w</sub>) + Φ(−w/σ<sub>w</sub>)</span> —
  the last term is the blunt possibility that you're a losing player and no bankroll saves you.

<!-- block: s23-note -->
RoRU (orange) vs naive RoR (blue) as a function of win rate, at your chosen N
    and bankroll (σ fixed at 18 bets/100 — the book's case study). The gap is the price of
    uncertainty. The book's going-pro example sits at the dots: 40,000 hands, w = 2.5 bets/100,
    300-bet roll → RoR 0.98% but RoRU **3.67%**; deduct 1 bet/100 for living expenses and it's
    6.22% vs **17.25%**. Taking a salary out of a thin edge is how pros go broke. The asymmetry
    is the lesson: overestimating your win rate slightly understates your risk *a lot*.

<!-- block: s24-h -->
Kelly and picking your game (ch. 24)

<!-- block: s24-note -->
Log-utility growth per hour, <span class="m">U ≈ μ/B − (μ²+σ²)/2B²</span>,
    for both games; the crossing is the cutoff <span class="m">2c = μ₁+μ₂+(σ₁²−σ₂²)/(μ₁−μ₂)</span>.
    At the book's own numbers ($35/$400 vs $60/$800) the derivation correctly reaches
    2c = $19,295 — <span class="err">and then prints c = $19,295; the cutoff is c = $9,647.50</span>,
    confirmed here by the utility crossover. Kelly sizing itself: a 3% even-money edge bets 3% of
    bankroll ($150 of $5,000 — Example 24.1, reproduced).

<!-- block: s25-h -->
Poker finance: swaps and backing as options (ch. 25)

<!-- block: s25-note -->
A standard backing deal — backer eats all losses, profits split — is a **call
    option at strike 0**: value of the wins = <span class="m">(σ/√2π)e<sup>−(a−w)²/2σ²</sup> + w·Φ((w−a)/σ)</span>.
    The book's example (w=$4,000, σ=$6,000): wins worth $4,906.72, so the 50/50 player takes
    $2,453.36 — **61.3%** of the whole deal's EV (the book's backer figure, $1,547.64, is a $1
    slip for $1,546.64). Swaps: trading 36% of yourself with an equal-EV player at 9-vs-12-buyin
    variance maximizes your Sharpe ratio (a₁ = σ₂²/(σ₂²+σ₁²) = 0.64). And diversifying across
    game *types* isn't diversification at all — you only ever hold one game at a time.

<!-- block: fid-h -->
Fidelity to the book
