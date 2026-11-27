<!-- block: page-title -->
The Limit AKQ Game — Mathematics of Poker, Visualized

<!-- block: eyebrow -->
Chapter 13 · Examples 13.1–13.2

<!-- block: the-limit-akq-game -->
The Limit AKQ Game

<!-- block: chapter-13-of-chen -->
Chapter 13 of Chen &amp; Ankenman's *The Mathematics of Poker*
  (Examples 13.1–13.2) — "perhaps the simplest form of symmetrical, non-trivial poker,"
  and the cleanest place to watch <span class="alpha">α&nbsp;=&nbsp;1/(P+1)</span>,
  the golden ratio of poker, do its work.

<!-- block: never-fold-the-nuts -->
Never fold the nuts, never call with a dead hand, never value-bet
    the middle card (it only gets called by the Ace), never check the nuts. What
    survives is a 2×2 game — Y: bluff queens or not; X: call with kings or not —
    which the book shows is *exactly* Cops &amp; Robbers from ch. 10.

<!-- block: y-s-bluff-frequency -->
Y's bluff frequency <span style="color:var(--heat)">b\* = 1/(P+1)</span> falls as the pot
    grows; X's calling frequency <span style="color:var(--ice)">c\* = (P−1)/(P+1)</span> rises toward always-call;
    the <span style="color:var(--green)">game value (P−1)/(6(P+1))</span> climbs toward its ceiling of 1/6.
    Everything kinks at **P = 1**: below it a bluff loses even when every King folds
    (half of X's remaining deck is Aces), so nobody bluffs, nobody calls, and the game is worth zero.

<!-- block: closed-forms-verified-against -->
Closed forms verified against an independent saddle-point solve of the
    full payoff matrix (<code>solve.py</code>).

<!-- block: the-game -->
The game

<!-- block: dominance-does-most-of -->
Dominance does most of the work

<!-- block: the-equilibrium-live -->
The equilibrium, live

<!-- block: why-is-everywhere -->
Why α is everywhere

<!-- block: fidelity-to-the-book -->
Fidelity to the book

<!-- block: a-three-card-deck -->
A three-card deck: Ace, King, Queen. Each player antes into a pot of
  <span class="m">P</span> and is dealt one card. One half street of limit betting
  (bet size 1): **X checks in the dark**, then Y bets or checks; facing a bet,
  X calls or folds. High card wins the showdown. Holding the King you know the
  opponent has the nuts or nothing — the deck itself creates perfectly polarized
  *card removal*, which the symmetric [0,1] games can't show.

<!-- block: before-any-mixing-pure -->
Before any mixing, pure logic deletes most of the game:

<!-- block: now-remove-the-limit -->
**Now remove the limit.** Chapter 15's appendix asks what happens when the
      bet size is free — and the answer (the King's blocking bet, the plateau of
      position) is charted at 300 stack depths in
      <a href="../nl/">the no-limit AKQ game&nbsp;→</a>

<!-- block: keep-the-limit-lose -->
**Keep the limit, lose the deck.** The same α logic on hands uniform in
      [0,1], through bets, raises and check-raises:
      <a href="../../zero-one/">the [0,1] games&nbsp;→</a>

<!-- block: big -->
Y bets every Ace and <span class="alpha">α</span> of his Queens — bluffs are a fixed
  *fraction of value bets*, chosen so a King gains nothing by calling. X folds
  <span class="alpha">α</span> of the hands that beat a bluff — chosen so a Queen gains nothing by
  bluffing. The same constant prices both sides of the bet, here with a three-card deck,
  in the [0,1] games with a continuum, and in real poker with 1,326 combos.

<!-- block: lbl -->
strategies &amp; value by pot size — the book's Figure 13.1, plus the value curve

<!-- block: fid -->
**10/21** (= 1/(P+1); the printed value contradicts the book's own formula)
