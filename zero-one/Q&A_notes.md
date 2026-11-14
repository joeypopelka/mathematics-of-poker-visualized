# Chapter 17 — Q&A Study Notes

Companion notes for *The Mathematics of Poker* (Chen & Ankenman), **Chapter 17: Mixing in Bluffs — Finite Pot [0,1] Games**. Built up from a working session; kept updated as we go.

**Convention throughout:** hands are uniform on **[0, 1]** with **0 = the nuts** and **1 = the worst hand**; lower number wins at showdown. Bet size = 1 unit; pot = P.

**Interactive artifacts in this folder**
- `game2.html` — Example 11.3 (half-street, folding). **von Neumann's poker model.** Strategy structure **+ game value G(Y)** vs. pot.
- `game9.html` — Example 17.1 / Figure 17.1 (one bet). Live strategy structure vs. pot size.
- `game10.html` — Example 17.2 / Figure 17.2 (two bets, no check-raise). Adds the raise.
- `game11.html` — Example 17.3 (two bets, **check-raise**). Y-side exact + X-side CFR-solved.
- `game11_cfr_solver.py`, `game11_grid.json` — the numerical solver + precomputed grid behind #11.
- `game12.html` — Example 17.4 (folding + **unlimited raises**, no check-raise). Rₚ + the infinite value cascade. Game value unresolved at finite P.
- `PLAN_sequence_form_LP.md` — design doc for the exact LP solve that would settle x₁ (line vs band). Not yet implemented.

---

## Reference solutions

### Game #2 (Example 11.3) — half-street, one bet, folding — *von Neumann's poker model*
The precursor to #9–#11, and one of the first games ever solved by game theory (von Neumann & Morgenstern, *Theory of Games and Economic Behavior*, 1944). Half-street: **X must check in the dark**; Y bets or checks; if Y bets, X calls or folds. α = 1/(P+1).

| Threshold | Meaning | Formula |
|---|---|---|
| y₁ | Y: value-bet ↔ check | (1−α)/[(2−α)(1+α)] |
| x₁\* | X: call ↔ fold | 2·y₁ |
| y₀ | Y: check ↔ bluff | 1 − α·y₁ |

Region order (0→1): `y₁ < x₁* < y₀`. Y value-bets [0,y₁], checks [y₁,y₀], bluffs [y₀,1]; X calls [0,x₁*], folds [x₁*,1].
Key relations (all exact): `1−y₀ = α·y₁` (bluff:value ratio = α), `x₁* = 2y₁` (**Y value-bets half the hands X will call**), and X folds α of hands that beat a bluff.

**Game value to Y** (Chapter 18, Eq. 18.1) — the first game value we've recorded:
- G = (1−α)·y₁ − (2−α)(1+α)·y₁²/2  = **y₁(1−α)/2 = (1−α)²/[2(2−α)(1+α)]**.
- Ex-showdown expectation to Y (the bettor). Runs from **0** (P→0, no betting) to **¼** (P→∞) — the ¼ being exactly the no-fold Game #1 value, i.e. the pure worth of the betting lead once folding is irrelevant.
- Spot values: P=1 → 1/18≈0.056; P=2 → 0.100; P=4 → 4/27≈0.148; P→∞ → 0.25.

*(Done: game values G(Y) are now shown — readout + curve — in all four artifacts (#2, #9, #10, #11). Formulas per game recorded below.)*

**Game values to Y, at a glance** (ex-showdown; each finite-pot game → its no-fold counterpart as P→∞):

| Game | G(Y) formula / method | P→∞ limit (= no-fold game) |
|---|---|---|
| #2 (half-street) | (1−α)²/[2(2−α)(1+α)] | ¼ (Game #1) |
| #9 (full, 1 bet) | α(1−α)²/[2(1+α)] — *humped*, peaks ≈0.057 near P≈2.6 | 0 (Game #4) |
| #10 (2 bets, no c-r) | region sum ΣGₙ (below) | ⅛ (Game #5) |
| #11 (2 bets, c-r) | *same* region sum with #11's y's — **exact** (Y-side only) | 1/9 (Game #7) |

Region-sum method for #10 & #11 (hold Y optimal, X best-responds; regions of X's hand): with
G₀=y₁(1−α)/2, G₁=(1−α)y₁, G₂=y₂−α·y₁, G₃=(1−α₂)y₂−(1−α),
`<Y> = y₂·G₃ + (y₁−y₂)·G₂ + (y₀−y₁)·G₁ + (1−y₀)·G₀`.
Spot values (P=2): #9 = 0.056, #10 = 0.068, #11 = 0.062 — and at every pot **G₉ < G₁₁ < G₁₀** (adding the raise helps Y; adding X's check-raise takes some back). Note **#11's game value is exact** even though its x-side thresholds aren't — it depends only on the exact Y-side (y₁,y₂,y₀).

### Game #9 (Example 17.1) — one full street, one bet
α = 1/(P+1).

| Threshold | Meaning | Formula |
|---|---|---|
| x₁ | X: value-bet ↔ check-call | (1−α)²/(1+α) |
| y₁ | Y: value-bet ↔ check (checked to) | (1−α)/(1+α) |
| x₁\* = y₁\* | X check-call cutoff / Y call cutoff | 1−α |
| y₀ | Y: check ↔ bluff | (1+α²)/(1+α) |
| x₀ | X: check-fold ↔ bluff | 1 − α·x₁ |

Region order (0→1): `x₁ < y₁ < x₁*=y₁* < y₀ < x₀`.
Handy relations: `x₁ = (1−α)·y₁`, `1−x₀ = α·x₁`, `1−y₀ = α·y₁`.
Sanity check at **P=4** (α=1/5): x₁=8/15, y₁=2/3, x₁\*=y₁\*=4/5, y₀=13/15, x₀=67/75.

### Game #10 (Example 17.2) — one street, two bets, **no check-raise**
α = α₁ = 1/(P+1), **α₂ = 1/(P+3)**, **R = (1−α₂)/2**. General ratio: **αₙ = 1/(P + (2n−1))**.

Solve x₁ first, then the rest:
`x₁ = (1−α)² / [ 1 + α + (2−α)(1−α₂)R ]` (Eq. 17.12 — holds for *all* no-check-raise games; only R changes with more bets).

| Threshold | Meaning | Formula |
|---|---|---|
| y₂ | Y: value-raise ↔ call | R·x₁ |
| x₂\* | X: bet+call-raise ↔ bet+fold-raise | (1−α₂)·x₁ = 2y₂ |
| x₁ | X: value-bet ↔ check-call | (see 17.12) |
| y₁ | Y: value-bet ↔ check (checked to) | (x₁\*+x₁)/2 |
| x₁\* = y₁\* | X check-call cutoff / Y flat-call cutoff | 2y₁ − x₁ = y₂# − α₂·y₂ |
| y₂# | Y: raise-bluff ↔ fold | 1−α |
| y₀ | Y: check ↔ bluff (checked to) | 1 − α·y₁ |
| x₀ | X: check-fold ↔ bluff | 1 − α·x₁ |

Region order (0→1): `y₂ < x₂* < x₁ < y₁ < x₁*=y₁* < y₂# < y₀ < x₀`.
Sanity check at **P=2** (α=1/3, α₂=1/5, R=0.4): x₁=5/21, y₂=2/21, x₂\*=4/21, y₁=279/630, x₁\*=y₁\*=68/105, y₂#=2/3, y₀≈0.8524, x₀≈0.9206.

### Game #11 (Example 17.3) — one street, two bets, **check-raise allowed**
α = 1/(P+1), α₂ = 1/(P+3), R = (1−α₂)/2. **The book stops giving full closed forms here** — it solves the Y-side and describes the structural changes; there is no threshold table.

**Y-side (exact, book):**
- y₁ = (1−α)/[1 + α + (1−α₂)R]   (Eq. 17.13)
- y₂ = R·y₁     (the R ratio now links two *Y* thresholds, not X→Y as in #10)
- y₂\* = (1−α₂)y₁   (Y bet-calls [0,y₂\*], bet-folds [y₂\*,y₁] — folds α₂ of value bets to a check-raise)
- y₀ = 1 − α·y₁

**X-side + Y give-up (y₁\*, y₂#): solved numerically (CFR).** A counterfactual-regret solve of the full two-bet check-raise game, validated against exact Game #10 (no check-raise) and the no-fold Game #7 limit as P→∞ (x₁→5/9, y₁→2/3, y₂→1/3). Near-indifferent boundaries (check-call/check-fold) and thin bluff bands are approximate — CFR mixes exactly where the equilibrium is itself indifferent.

Structural changes vs #10:
- **X check-raises his strongest hands** (indifferent between check-raise and bet-call on his best region) and adds **check-raise bluffs** among his give-up hands.
- **Y bets tighter, raises looser** (fearing the check-raise); value bets split into bet-call / bet-fold.
- **x₁\* = y₁\* breaks** (they coincided in #9 and #10). Confirmed numerically: at P=2, x₁\*≈0.645 ≠ y₁\*≈0.666. See Q13/Q15.

Verified numeric spot-checks (P=2): y₁=0.403, y₂=0.161, y₂\*=0.323, y₀=0.866 (exact); x₁≈0.26, x₁\*≈0.65, x₀≈0.90, y₁\*≈0.68, y₂#≈0.71 (CFR).

---

### Game #12 (Example 17.4) — full street, folding, **unlimited bets/raises**, no check-raise
The last finite-pot [0,1] game. Every Game #10 equation survives except the one at y₂ (Y can now be re-raised). The fix: `y₂ = R·x₁` keeps its form but **R becomes pot-dependent, Rₚ**, satisfying the backward recursion
`Rₚ = [(P+2)/(P+3)] / [2 + Rₚ₊₂·(P+4)/(P+5)]`, with Rₚ → r = √2−1 as P→∞ (compute by iterating backward from a large pot where Rₚ≈r).

- x₁ = (1−α)²/[1+α+(2−α)(1−α₂)**Rₚ**]  (Eq. 17.12 with R=Rₚ).
- **Value cascade** (converges geometrically to the nuts): x₁ → y₂=Rₚx₁ → x₃=Rₚ₊₂y₂ → y₄=Rₚ₊₄x₃ → … These are the "put in the nth bet for value" thresholds.
- **Lower thresholds unchanged** from #10 (more bets move Rₚ/x₁ but not the low-threshold relationships): y₁=((1−α)+(1+α)x₁)/(2+α−α²), y₀=1−αy₁, x₁\*=2y₁−x₁, x₀=1−αx₁, y₂#=1−α, y₁\*=y₂#−α₂y₂. And **x₁\* = y₁\*** again (no check-raise).
- **P→∞ = Game #6:** Rₚ→r, x₁→1/(1+2r)≈0.547, y₂→r·x₁ — the r-geometric ladder of the no-fold infinite game. Verified.
- **Game value: unresolved at finite P.** Limit is Game #6's 1/16+r/8≈0.1143. The finite value needs summing the whole infinite ladder (book declines it). A quick CFR ladder solver **failed validation** (B=2 gave 0.084 vs #10's 0.068; blew up at large P) — not shipped. Would need a correct sequence-form/self-similar solve.

Spot values (P=2): Rₚ=0.346, x₁=0.248, cascade y₂=0.086, x₃=0.031, y₄=0.012, …; lower y₁=0.449, x₁\*=0.650, y₀=0.850, x₀=0.917.

## Finite-pot → no-fold mapping (P → ∞)

As P→∞, α=1/(P+1)→0, so all α-driven structure (bluffs ∝ α·value, fold regions, call/fold ratios) vanishes and each finite game becomes its **no-fold counterpart**. No-fold games are pot-independent (folding is what made P matter), so each is a single fixed value = the finite game's limit. Equivalently (book's framing): no-fold game + folding option = finite game; "strategic options have non-negative value."

| Finite (fold) | → No-fold (P→∞) | option folding adds | G(Y) limit |
|---|---|---|---|
| #2 half-street (Ex 11.3) [von Neumann] | #1 half-street no-fold (Ex 11.2) | X can fold | ¼ |
| #9 full, 1 bet (Ex 17.1) | #4 full, 1 bet, no-fold (Ex 15.1) | X can fold | 0 |
| #10 full, 2 bets, no c-r (Ex 17.2) | #5 full, 1 raise, no c-r (Ex 16.2) | both fold | ⅛ |
| #11 full, 2 bets, c-r (Ex 17.3) | #7 full, 1 raise, c-r (Ex 16.4) | both fold | 1/9 |
| #12 full, ∞ bets, no c-r (Ex 17.4) | #6 full, ∞ raises, no c-r (Ex 16.3) | both fold | 1/16 + r/8 ≈ 0.114 |

Option-transitions among the no-fold games: #1→#4 (X gains bet), #4→#5 (Y gains raise), #5→#7 (X gains check-raise, value ↓ ⅛→1/9), #5→#6 (X gains re-raise, value ↑ ⅛→0.114). r = √2−1. **All five finite games (#2, #9, #10, #11, #12) now have artifacts.**

## The role(s) of α

- **α = 1/(P+1)** — the "golden ratio of poker." It is simultaneously the **bluff-to-value ratio** (bluff region = α × value region), and the **fold frequency** of a caller facing one bet (call 1−α, fold α).
- **αₙ = 1/(P + (2n−1))** — generalization for the nth bet (bigger pot + more committed bets). α₂ = 1/(P+3) governs the raise. Unmarked α means α₁. Identity: α/α₂ = 1 + 2α.
- **Special value:** α = √2 − 1 ≈ 0.414 (the root of x²+2x−1=0, "golden mean of poker"), occurring at **P = √2**.

---

## Q&A log

### Q1. "The relationship between y₁\* and x₁\* is irrelevant — we only consider one or the other." (Game #9)
Because the two thresholds govern decisions in **mutually exclusive branches** of the game tree. x₁\* only matters when **X checks and Y bets**; y₁\* only when **X bets**. No single indifference equation ever contains both, so their relative ordering can't affect the solution — the book just has to pick an order to draw them.

### Q2. Why are x₁\* and y₁\* equal in Game #9 (both = 1−α)?
- y₁\* = 1−α directly: Y defends over his **whole** range [0,1], calling the top 1−α.
- x₁\* is an *interpolation*: X calls 1−α of the way from x₁ to **y₀** (only his bluff-catchers count) → x₁\* = (1−α)(y₀−x₁)+x₁.
- These land on the same point because of two sub-relations, `x₁ = (1−α)y₁` and `1−y₀ = αy₁`: both sides of the required identity reduce to α(1−α)y₁.
- It is *special that they coincide*; the book flags it precisely because it isn't forced by the parameterization.

### Q3. Why is Y's checked-to bluffing frequency maximized at pot ≈ 1.4?
Y's bluff freq = 1−y₀ = α·y₁ = α(1−α)/(1+α) — a product of a falling factor (α, the bluff ratio) and a rising one (y₁, the value base). Maximizing gives **α²+2α−1=0 → α = √2−1**, i.e. **P = √2 ≈ 1.414**. Peak value = (√2−1)² = **3 − 2√2 ≈ 17.16%**. This is the "golden mean of poker."

### Q4. Why does X's bluffing frequency peak at ≈ 11.3%, and at a *different* pot than Y's?
X's bluff freq = 1−x₀ = α·x₁ = α(1−α)²/(1+α) — the same shape as Y's but with an **extra (1−α)** (because X value-bets a factor (1−α) fewer hands: x₁ = (1−α)y₁). Maximizing gives **2α²+3α−1=0 → α = (√17−3)/4 ≈ 0.281**, i.e. **P = (√17+1)/2 ≈ 2.56** (not 2.9 — the curve is flat on top so 2.1–3.1 all round to 11.3%). Peak ≈ **11.34%**. The extra (1−α) both lowers the peak and pushes it to a larger pot.

### Q5. What is the "value base"?
Each player's bluffs are tethered to his value bets by α: `bluff freq = α × value-bet freq`. The value base is that value-bet region — y₁ for Y, x₁ for X. Since x₁ = (1−α)y₁, X's value base carries an extra (1−α); comparing the numerators (shared 1/(1+α) drops out), Y's ∝ (1−α), X's ∝ (1−α)². That single extra factor is the whole reason their bluff-frequency peaks differ.

### Q6. Book says "x₁\* is 1−α of the way from x₁ to x₀," but at P=2 I compute 60%, not 1−α = 66.7%. What's wrong?
Nothing — your arithmetic is right; the book's **summary sentence is loose**. The precise rule (and Eq. 17.6) anchors to **y₀, not x₀**: `x₁* = x₁ + (1−α)(y₀ − x₁)`. Only X's hands better than y₀ are bluff-catchers, so the defensible region is [x₁, y₀], and x₁\* is 1−α of *that*. The book's own precise passage says exactly this; the later summary compresses [x₁, y₀] back to [x₁, x₀] and drops the caveat.

### Q7. Of X's whole checking range [x₁, x₀], what fraction does he defend (check-call)?
**Not 1−α.** It's (x₁\* − x₁)/(x₀ − x₁) = **2(1−α) / [(1+α)(2−α)]** — 60% at P=2 (rises to 100% as P→∞, 0 as P→0). The 1−α call rate applies only to the bluff-catching slice [x₁, y₀]; the tail [y₀, x₀] auto-folds, diluting the overall defense frequency.

### Q8. Are the non-catcher hands [y₀, x₀] "worse than Y's weakest bluff"? (correction)
**No — that was my error.** Y's weakest bluff is the hand at 1; a hand at x₀−ε beats it easily, and in fact [y₀, x₀] beats *most* of Y's bluffs. The real reason X folds them is **pot odds**: calling needs equity ≥ 1/(P+2), and these hands beat **zero value bets** (they only beat part of the bluffs), so their equity falls below the price. Even the break-even hand x₁\* beats *all* bluffs and no value bets — exactly 1/(P+2) equity. "Beat a bluff" should be read as "beat the **marginal** bluff at y₀."

### Q9. "Using the strongest hands in the (fold, raise-bluff) region dominates." (Game #10 raise-bluffs)
Y's raise-bluffs come from the **top** of his give-up range [y₁\*, y₂#], not the bottom. Contrast with one-bet bluffing (bluff your *worst*), which works because give-up hands get **checked** and can win a showdown, so you preserve the medium ones. Here the give-up hands get **folded** — they never show down — so there's no showdown value to preserve. A called raise-bluff always loses ("no hope of a showdown"), so hand rank doesn't affect bluff EV → co-optimal. Bluffing the strongest of the give-ups then **weakly dominates**: fold your very worst (they'd never win a showdown), and keep the best give-ups in as bluffs, since they retain equity if a showdown ever does occur. Rule: **never fold a hand stronger than one you're bluffing.**

### Q10. In Game #10, does Y ever gain by bluff-raising the *top* of the give-up range vs. the bottom?
**No — exact tie in equilibrium**, for two reasons: a called raise-bluff always loses (X's raise-calling range dominates every give-up hand), and there's no later street to win on. X responds to bluff *frequency*, not composition, so top vs. bottom yields identical value. This holds across the whole [0,1] chapter — the "strongest dominates" rule is only a **weak** (non-dominated) tie-break. It becomes strictly more valuable only with real-poker features the model strips out: **equity when called / draws, a future street, blockers, or a suboptimal opponent**.

### Q11. Is bluffing the *top* of your check-through range (one-bet game) dominated?
**Yes — strictly** (real EV loss vs. optimal opponent), unlike the raise case. Here give-up hands are **checked** and reach a showdown, so there's a genuine showdown-value gradient. The indifference at y₀ makes it monotone: hands better than y₀ strictly prefer checking (showdown value), hands worse strictly prefer bluffing (fold equity, ~0 showdown value). Bluffing a medium hand while checking a trash hand loses on **both**. Unifying idea: **if the give-up hand ever shows down, bluff the trash (strict); if it never shows down (folded), bluff the strongest give-ups (weak tie-break).**

### Q12. What is R in Game #10?
R = (1−α₂)/2 is the ratio of Y's value raises to X's value bets: **y₂ = R·x₁**. It bundles two factors — Y raises with **half** the hands X will continue with (X can't re-raise → clean ½), times the **(1−α₂)** fraction of value bets X keeps in to face a raise (he folds α₂ to defend vs. raise-bluffs). As P→∞, α₂→0 and **R→1/2**, matching the no-fold Game #6; the (1−α₂) is the finite-pot correction for X folding to the raise.

### Q13. Why does x₁\* = y₁\* *again* in Game #10 (and I was told they'd split)?
They **don't split** — that earlier claim was wrong. They're exactly equal (68/105 at P=2), just no longer equal to 1−α. Both are the **worst hand a player flat-calls a single (first) bet with to bluff-catch**, and both decisions have identical **pot odds** (call 1 into pot P → need 1/(P+2) equity) against a range polarized at the **same α₁** (1−x₀=αx₁ and 1−y₀=αy₁). The raise machinery (α₂, R) only touches the *upper* thresholds; per Eq. 17.12 the "fundamental relationships among the lower thresholds" are unchanged by adding bets. So x₁\*=y₁\* holds across **all no-check-raise games** — it slides below 1−α as R changes, but both move together. What *would* split them is **allowing check-raising**, which stops X's post-check decision from being a clean call/fold.

### Q14. Why are x₁\* and y₁\* no longer 1−α in Game #10, and why is y₂# now 1−α?
The "1−α" didn't disappear — it **relocated**. The invariant is **"Y folds α of his hands to a bet"** (book's own reframing): the 1−α line is always the total *continue-vs-give-up* boundary, pinned by making X's bluff (at x₀) indifferent — X's bluff wins the pot only when Y gives up entirely, so Y must fold α. Which threshold that boundary sits on depends on Y's available actions. In **Game #9** Y facing a bet can only call/fold, so "not folding" = calling and the boundary is the call cutoff → y₁\* = 1−α. In **Game #10** Y gains a non-folding action *above* his flat-call cutoff — the **raise-bluff** — so "not folding" = raise + call + raise-bluff = [0, y₂#]; the give-up line moves out to **y₂# = 1−α**, and the flat-call cutoff **y₁\* retreats inside it** (raise-bluffs [y₁\*, y₂#] fill the gap). Since x₁\* is locked to y₁\*, it drops too. At P=2: y₂# = 2/3 = 1−α (Y folds [2/3, 1]); raise-bluffs occupy [0.648, 0.667]; x₁\*=y₁\*=68/105 ≈ 0.648 < 2/3.

### Q16. Why couldn't the X-side of #11 be solved with indifference equations (like the Y-side / like #9, #10)? — the check-raise roadblock
It *can* be set up, but it doesn't unwind into clean closed forms, and this is the same wall the book hits (it stops publishing full solutions at #11). The reason is a **strategic degeneracy introduced by check-raise**:

- Deriving Y's indifference at y₁ (which is what pins X's value cutoff x₁) gives, in net bets:
  `b − x₂ + x₁ + 2·x₁* − 2·y₁ − x_crb = 0`.
- Two *extra* unknowns appear that don't exist in #9/#10: **`b`** (the point where X's strongest hands split between **bet-calling** and **check-raising** — the book notes X is *indifferent* between these, i.e. a genuinely **mixed strategy**), and **`x_crb`** (how far X's **check-raise bluffs** extend vs. bet-bluffs).
- In #9 (one bet) and #10 (no check-raise) no such split exists, so each value threshold gets its own standalone equation and they unwind one-at-a-time into closed forms. With check-raise, X's value **and** his bluffs each split across two branches (bet vs. check-raise), and those split-weights appear *inside* the equation for x₁ — so the thresholds couple into one big simultaneous system whose solution is messy and un-illuminating. The book: "we will generally omit listing off the whole solution," and even #10's full solution is "not particularly useful."

**Consequence / how we handle it:** the Y-side stays exact (closed forms, Eq. 17.13). The X-side (x₁, x₁*, x₀) + Y's give-up thresholds (y₁*, y₂#) are obtained by **numerically solving the equilibrium** — a validated CFR+ solve, cross-checked against exact Game #10 (no check-raise) and the no-fold Game #7 limit (P→∞). CFR is actually the *right* tool here because it represents the mixed strategy natively. There is no tidy `x₁ = (…)/(…)` for this game; that object effectively doesn't exist in usable form. (This also explains **why the book stops giving full solutions exactly at the check-raise game.**)

**Lesson for me (feedback):** don't promise #9/#10-style closed forms for a game before checking whether a mixed-strategy/branch-split degeneracy is present — if it is, the clean-threshold method breaks and a numerical equilibrium solve is the honest tool.

**Follow-up (attempt to "sharpen to exact-numeric"):** even a *numerical* exact answer for x₁ turned out to be out of reach with the CFR solver. Validating the threshold extraction against exact Game #10 (x₁ should = 0.238): every extraction method returned ≈0.13–0.15, and two independent high-precision runs disagreed on #11 (x₁ ≈ 0.16 vs 0.26). By contrast **x₁\*** (≈0.66 vs exact 0.648) and **x₀** (0.921 ✓) *do* validate. Root cause: X's **bet-fold** hands and his **check-call** hands are near-indifferent, so the equilibrium genuinely blurs across x₁ and CFR's average strategy mixes there — there is no crisp threshold to read. A reliable x₁ would require a **sequence-form LP / support-enumeration** solve (bigger separate build), and the true object may be a mixed *band* rather than a single line. Status: Y-side exact; x₀ and x₁\* reliable-numeric; **x₁ is only approximate** and is labeled as such in `game11.html`.

### Q17. What is a sequence-form linear program (the exact-solve method for x₁)?
The standard exact method for a **two-player zero-sum extensive game with imperfect information** — exactly our poker tree (private hands from chance, then bet/check → raise/call/fold …).

- **Why the obvious routes fail.** *Normal form* (one matrix) needs a pure strategy = an action at every infoset → ~aᵏ strategies, **exponential**; can't even write it down. *Behavioral* strategies (a prob per action per infoset) are compact, but reaching a leaf multiplies probabilities along the path, so when both players optimize the payoff is **bilinear / non-convex** — not an LP.
- **The trick (Koller–Megiddo–von Stengel).** Change variables to **realization weights of *sequences***. A *sequence* = the string of a player's *own* actions from root to a point (e.g. for X: `∅, bet, bet·call, bet·fold, check, check·raise, check·call, check·fold`). Its weight = product of action probs along it. In these variables everything is **linear**:
  - #sequences ≈ #tree edges (linear, a *sum* not a *product*);
  - constraints are linear **flow** equations (root weight = 1; each sequence's weight = sum of its immediate extensions' weights);
  - expected payoff is **bilinear**, xᵀA y, with A a sparse matrix indexed by sequence pairs (chance + leaf payoffs baked in).
- **One LP.** Fix x; Y's best response `min_y xᵀAy` s.t. Y's flow constraints is an LP → replace by its **dual** → the whole saddle-point collapses to a single LP in x + dual vars, of size **linear in the game tree**. Solve once, read both realization plans, normalize back to behavioral strategies/thresholds.
- **Why it beats CFR for x₁.** CFR is iterative and you read the **time-average**, which smears across indifferent regions (what blurred x₁). An LP returns an **exact optimal vertex** (rational solution for rational data, no averaging): if a crisp x₁ exists it returns it exactly; if the bet-fold/check-call zone is a genuine **mixed band**, the LP shows that definitively instead of guessing.
- **Why it's a real build (not done yet).** For our Bayesian game: discretize hands into N buckets, construct the sequence sets, the two flow-constraint matrices, and the sparse payoff matrix A (each entry an integral over leaf payoffs weighted by 1/N² chance), then hand to `scipy.linprog`. ~few hundred lines + its own validation pass (must re-derive exact #10). Offered as optional follow-up to get the definitive x₁ verdict (exact threshold, or proof it's a band).

### Q15. Build Game #11 (check-raise). [confirms the x₁\*=y₁\* prediction]
Built `game11.html`. Because the book doesn't give full closed forms, the X-side was **solved numerically by CFR** (validated on #10 and the #7 limit). This numerically **confirmed the Q13 prediction**: allowing check-raise *does* break x₁\* = y₁\* (P=2: x₁\*≈0.645 ≠ y₁\*≈0.666), because X's post-check decision is no longer a clean call/fold — he can check-raise. So the x₁\*=y₁\* equality is a property of *no-check-raise* games specifically, holding across #9 and all of #10's bet-count family but ending the moment check-raise enters.

---

## Threshold quick-reference (selected pots)

**Game #9** (α = 1/(P+1)):

| P | α | x₁ | y₁ | x₁\*=y₁\* | y₀ | x₀ |
|---|---|---|---|---|---|---|
| 1 | 0.500 | 0.167 | 0.333 | 0.500 | 0.833 | 0.917 |
| 2 | 0.333 | 0.333 | 0.500 | 0.667 | 0.867(≈) | 0.889 |
| 4 | 0.200 | 0.533 | 0.667 | 0.800 | 0.867 | 0.893 |
| √2≈1.41 | 0.414 | — | — | — | max bluff 1−y₀ = 17.16% | — |

**Game #10** (α₂ = 1/(P+3), R = (1−α₂)/2):

| P | α | α₂ | R | x₁ | y₁ | x₁\*=y₁\* |
|---|---|---|---|---|---|---|
| 1 | 0.500 | 0.250 | 0.375 | 0.130 | 0.309 | 0.488 |
| 2 | 0.333 | 0.200 | 0.400 | 0.238 | 0.443 | 0.648 |
| 9 | 0.100 | 0.083 | 0.458 | 0.427 | 0.655 | 0.884 |
| ∞ | 0 | 0 | 0.500 | 0.500 | 0.750 | 1.000 |

*(For exact values at any pot, use the sliders in `game9.html` / `game10.html`.)*
