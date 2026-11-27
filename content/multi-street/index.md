# multi-street/index.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

<!-- block: page-title -->
Multi-Street Games — Mathematics of Poker, Visualized

<!-- block: eyebrow -->
Chapters 14 &amp; 19

<!-- block: multi-street-games -->
Multi-Street Games

<!-- block: chapters-14-amp-19-2 -->
Chapters 14 &amp; 19 of Chen &amp; Ankenman's *The Mathematics of Poker*:
  what size to bet when the bet size is yours to choose — on one street, on many,
  and in the limit of infinitely many. Home of the book's most quoted result,
  the **geometric growth of pot**.

<!-- block: clairvoyance-game-f-s -->
<span style="color:var(--heat)">Clairvoyance game: f(s) = ys/(1+s)</span> rises
    forever — **jam**. <span style="color:var(--ice)">The AKQ game: f(s) = s(1−s)/(6(1+s))</span>
    peaks at **s\* = √2−1 ≈ 0.414** — the "golden mean of poker," r. (A quiet oddity: at s\*, X's
    calling frequency with Kings, (1−r)/(1+r), is *also exactly r*.) In the
    <span style="color:var(--purple)">[0,1] version</span> Y bets a different amount with every hand —
    value function y(s) = 3/(7(1+s)²), call function x(s) = 6/(7(1+s)), bluff mass exactly 1/7.

<!-- block: each-column-is-a -->
Each column is a street: <span style="color:var(--heat)">pot entering</span> with the
    <span style="color:var(--ice)">bet</span> stacked on top — the same shape every street, scaled by G.
    Pot-sized bets (G=3) need stacks of (3<sup>M</sup>−1)/2 pots — **13 pots deep for three streets**;
    half-pot bets (G=2) get stacks in at (2<sup>M</sup>−1)/2 — 3.5 pots over three streets.

<!-- block: the-book-s-figure -->
The book's Figure 19.1, completed: the per-street growth ratio G against stack
    depth for M = 2…5 streets. Dashed lines: pot-sized (G=3) and half-pot (G=2) bets.

<!-- block: the-same-stack-bet -->
The same stack, bet in the same number of streets — and the sizing scheme alone
    swings the game from losing to winning. The small first bet is not timidity: it buys a 46%
    call-through rate at every step of a pot that is growing 3.33× per street.

<!-- block: x-s-1-1 -->
<span style="color:var(--ice)">x(s) = 1/√(1+2s)</span> — the caller's hands committing at
    least s; <span style="color:var(--heat)">y(s) = y·√((1+2S)/(1+2s))</span> (capped at 1) — the clairvoyant's.
    The M-street geometric game converges to these curves as M→∞ (verified to 2×10⁻³ at M=1000 in
    <code>solve.py</code>), and position's value goes to zero — the auction is symmetric.

<!-- block: one-street-first-the -->
One street first: the value of a bet size (ch. 14)

<!-- block: the-geometric-growth-of -->
The geometric growth of pot (ch. 19)

<!-- block: why-it-matters-the -->
Why it matters: the $185 case study (Example 19.3)

<!-- block: infinite-streets-the-auction -->
Infinite streets: the auction game (Examples 19.4–19.6)

<!-- block: fidelity-to-the-book -->
Fidelity to the book

<!-- block: give-the-bettor-a -->
Give the bettor a polarized range (nuts or air) and charge him bet <span class="m">s</span>
  (in pots). His bluffs are priced by <span class="m">α = s/(1+s)</span> and his value function
  <span class="m">f(s)</span> does the rest:

<!-- block: static-hands-clairvoyant-bettor -->
Static hands, clairvoyant bettor, M streets, stacks S pots deep. Each street the
  non-clairvoyant player simply folds α and calls; the bettor stacks bluffs street
  over street. The optimal sizing grows the pot by the *same ratio*
  <span class="m">G = (1+2S)<sup>1/M</sup></span> every street, landing all-in on the river.

<!-- block: stacks-185-antes-5 -->
Stacks $185, antes $5, three streets; Y's card wins a showdown 2/13 of the time
    (clairvoyant). Betting flat $60 per street vs. betting the geometric growth of pot:

<!-- block: let-the-number-of -->
Let the number of streets go to infinity and betting becomes an *auction*: each hand
  silently commits to a total <span class="m">s</span> it is willing to put in. The equilibrium
  commitment curves are square roots:
