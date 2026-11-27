# multiway/index.html — page text
# Edit here, then run `python3 build.py` (or push — the GitHub Action
# rebuilds). **bold**, *italic*, `math`; raw HTML passes through; \* = literal *.

<!-- block: eyebrow -->
Chapter 29

<!-- block: multiplayer-games -->
Multiplayer Games

<!-- block: chapter-29-of-chen -->
Chapter 29 of Chen &amp; Ankenman's *The Mathematics of Poker*: why
  "optimal" stops meaning anything when a third player sits down. A light treatment by
  design — the chapter's own message is that these games have equilibria but no solutions.

<!-- block: the-rock-and-the -->
The rock and the maniac form an **implicit alliance without exchanging a
    bit of information**: the maniac charges you $30 to see a showdown, and the rock only
    ever puts money in when he has you beat. The book conjectures real three-handed analogues
    exist — two players whose pre-announced strategies make the third's EV negative.

<!-- block: erratum-the-book-reports -->
<span class="err">Erratum:</span> the book reports x ≈ 0.2848, y₁ ≈ 0.1424,
    bluff band 0.6424 ± 0.0095 — values that don't satisfy its own three equations (they give
    w = 0.019 on one side and 0.620 on the other), and against which Y could profitably bluff
    hand 0.5 for +0.68. The true simultaneous root is **x = 0.5178, y₁ = 0.2589, band
    0.7589 ± 0.0242**. The chapter's qualitative points survive: X calls far less than the
    9/10 he would without Z, and the bluff-to-value ratio (0.187) runs above the two-player
    α = 1/10. And the destabilizing lesson stands: if Y *overbluffs*, he transfers X's
    equity to Z — allying with the all-in player — and X's best recourse hands some equity
    back to Y.

<!-- block: z-s-ev-per -->
Z's EV per value bet is **discontinuous** in his announced bluff ratio.
    Bluff a little too much (β just over 1/10) and X snaps off every bluff: Z bleeds. But bluff
    *three times* the equilibrium rate and Y — who could never overcall at equilibrium —
    finally has odds to overcall behind X: Z collects two bets on every value hand,
    **17/10 per value bet instead of 9/10**. Over-bluffing only works if the victims know
    about it: the equilibrium is disturbed into an alliance of Z with whichever opponent his β
    recruits. This is the chapter's closing idea — and why the book refuses to say "optimal"
    about multiplayer poker at all.

<!-- block: the-chapter-opens-with -->
The chapter opens with tournament-adjacent material continued from ch. 28
  (backing agreements under tournament skew — see the <a href="../tournaments/">tournaments
  project</a>), a face-up three-way collision (set vs. nut flush draw vs. straight flush draw)
  where *who should do what is genuinely undefined* because every pair of players prefers
  a different alliance, and a pointer toward cooperative game theory (Shapley values) for
  readers who want the deep end. Verified numbers: <code>verify.py</code>.

<!-- block: why-three-is-different -->
Why three is different

<!-- block: 1-the-rock-amp -->
1 · The rock &amp; the maniac: a fair game you cannot win

<!-- block: 2-the-dry-side -->
2 · The dry side pot: bluffing changes meaning

<!-- block: 3-the-clairvoyant-maniac -->
3 · The clairvoyant maniac: announce your sins

<!-- block: also-in-these-pages -->
Also in these pages

<!-- block: nash-proved-every-finite -->
Nash proved every finite game has an equilibrium — a strategy set no one can profit
  by *unilaterally* leaving. But in multiplayer games equilibria multiply (chicken has
  three, with utterly different characters), and nothing stops two players from jointly
  drifting into an **alliance** that farms the third. "Hard" collusion breaks the rules;
  "soft" collusion — implicit, no information shared — is just… poker. The three toy games
  below (verified in <code>verify.py</code>) each isolate one facet.

<!-- block: three-players-ante-10 -->
Three players ante $10, one card each; aces and kings win. The player on your left
    announces: *"check always, call only with a winner."* The one on your right:
    *"bet $30 always, call always."* Both exploitable-looking, both fully disclosed, and
    the game is symmetric. Your best response (call with everything — folding a loser gives 0,
    calling nets +$1.87) still loses:

<!-- block: x-and-y-with -->
X and Y with chips, Z all-in; pot 9; hands uniform on [0,1]; one half street. A
    successful "bluff" no longer wins the pot — Z can't fold — so it's really a semi-bluff
    that evicts X and then must beat Z. The equilibrium (book's own indifference system:
    <span class="m">y₁ = x/2</span>, <span class="m">w = x/(20−18x)</span>,
    <span class="m">w = √((1+x)² − 40x/9)</span>, solved correctly and confirmed by a
    2000-point no-deviation check):

<!-- block: z-is-clairvoyant-into -->
Z is clairvoyant into a pot of 9 against X and Y, who hold identical hands and can
    only check/call. In equilibrium Z bluffs α = 1/10 per value bet and gets called 9/10 of
    the time in total. Now let Z **announce** a bluff ratio β and let X and Y respond
    greedily:
