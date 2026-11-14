# Implementation Plan — Sequence-Form LP for [0,1] Game #11

**Status:** design only — *not yet implemented.*
**Goal:** compute the *exact* equilibrium of the two-bet check-raise game to settle the one open question the CFR solve couldn't: **is X's value/check-call boundary x₁ a crisp threshold, or a genuine mixed band?** — and, if crisp, its exact value across pot sizes.

See `Q&A_notes.md` Q16 (why closed forms fail here) and Q17 (what sequence form is) for background. Terminal payoffs are already validated in `game11_cfr_solver.py`.

---

## 1. Success criteria

1. Reproduces the **exact Game #10** thresholds when check-raise is disabled (x₂*=0.190, x₁=0.238, x₁*=0.648, x₀=0.921 at P=2) to within discretization error.
2. Reproduces the **no-fold Game #7** solution when folding is disabled (x₁=5/9, y₁=2/3, x₂=1/9, y₂=1/3).
3. Returns, for Game #11 at each pot P, either (a) a crisp x₁, or (b) a rigorously-measured **band** [x₁⁻, x₁⁺] with its width — via the secondary-LP test in §7.
4. Y-side comes out matching the exact closed forms (Eq. 17.13) — an independent check that the model is right.

---

## 2. Why an LP (one line)

CFR converges to equilibrium but you read the *time-average*, which smears indifferent regions (this is what blurred x₁). An LP returns an **exact optimal vertex** of the strategy polytope — crisp where the equilibrium is crisp, and *detectably* non-unique where it is a band.

---

## 3. Game model (the tree)

Hands i (X), j (Y) drawn uniform on N buckets, value v=(k+0.5)/N, **lower = better**. Pot P dead; bet = 1. Showdown: lower hand wins. Two bets max; check-raise allowed.

**Infosets** (one copy per hand bucket):

| Player | Infoset | Reached when | Actions |
|---|---|---|---|
| X | `IX0(i)` | root | bet, check |
| X | `IXbr(i)` | X bet, Y raised | call, fold |
| X | `IXcb(i)` | X checked, Y bet | **raise (check-raise)**, call, fold |
| Y | `IYb(j)` | X bet | raise, call, fold |
| Y | `IYc(j)` | X checked | bet, check |
| Y | `IYcr(j)` | X checked, Y bet, X raised | call, fold |

(For **#10** validation: drop the `raise` action from `IXcb`. For **#7**: drop all `fold` actions.)

**Terminal payoffs uₓ(i,j)** — copy from the validated solver (`S = 1[i<j]`, constant-sum P):

| Leaf | line | betsX,betsY | uₓ |
|---|---|---|---|
| CC | check,check | 0,0 | P·S |
| Cbf | check,bet,X-fold | 0,1 | 0 |
| Cbc | check,bet,X-call | 1,1 | S·(P+2)−1 |
| CbrF | check,bet,X-raise,Y-fold | 2,1 | P+1 |
| CbrC | check,bet,X-raise,Y-call | 2,2 | S·(P+4)−2 |
| Bf | bet,Y-fold | 1,0 | P |
| Bc | bet,Y-call | 1,1 | S·(P+2)−1 |
| BrF | bet,Y-raise,X-fold | 1,2 | −1 |
| BrC | bet,Y-raise,X-call | 2,2 | S·(P+4)−2 |

---

## 4. Sequences & leaf map

**X sequences (per bucket i):** `∅, bet, bet·call, bet·fold, check, check·raise, check·call, check·fold` → ≤ 8N.
**Y sequences (per bucket j):** `∅, raise, call, fold, bet, chk, bet·crcall, bet·crfold` → ≤ 8N.

**Leaf → (Xseq, Yseq)** (this is the sparse structure of A):

| Leaf | Xseq | Yseq |
|---|---|---|
| CC   | check       | chk |
| Cbf  | check·fold  | bet |
| Cbc  | check·call  | bet |
| CbrF | check·raise | bet·crfold |
| CbrC | check·raise | bet·crcall |
| Bf   | bet         | fold |
| Bc   | bet         | call |
| BrF  | bet·fold    | raise |
| BrC  | bet·call    | raise |

---

## 5. Flow constraints

For each player, realization weight r(·) ≥ 0 with, per hand bucket:

- **X:** r(∅ᵢ)=1; r(bet)+r(check)=r(∅); r(bet·call)+r(bet·fold)=r(bet); r(check·raise)+r(check·call)+r(check·fold)=r(check).
- **Y:** r(∅ⱼ)=1; r(raise)+r(call)+r(fold)=r(∅); r(bet)+r(chk)=r(∅); r(bet·crcall)+r(bet·crfold)=r(bet).

These give the constraint matrices E (X), F (Y) with RHS e, f (root rows = 1, others = 0). Behavioral strategy at any infoset = child weight / parent weight.

**Chance:** fold the 1/N (X) and 1/N (Y) deal probabilities into the payoff matrix A (see §6), and keep each type's root weight = 1 (conditional realization plans).

---

## 6. Payoff matrix A

A is indexed (Xseq over all i) × (Yseq over all j). For each of the 9 leaves and each (i,j):

```
A[ (i, Xseq_leaf), (j, Yseq_leaf) ] += (1/N²) · uX(leaf, i, j)
```

Sparse: only the 9 seq-pair patterns above are nonzero, each over the N×N bucket grid. Size ≈ 8N × 8N but with ~9N² nonzeros.

---

## 7. The LP

X maximizes, Y minimizes, value = xᵀA y. Using LP duality on the inner min (dual vars q, one per Y flow row):

```
maximize_{x, q}   fᵀ q
subject to        E x = e,      x ≥ 0
                  Fᵀ q ≤ Aᵀ x   (i.e. Aᵀx − Fᵀq ≥ 0)
                  q free
```

- Solve with `scipy.optimize.linprog` (method="highs"): variables z=(x,q); objective −fᵀq (minimized); `A_eq=[E|0], b_eq=e`; `A_ub=[−Aᵀ | Fᵀ], b_ub=0`; bounds x≥0, q free.
- **x** → X's equilibrium realization plan. Recover **y** either from the mirror LP (swap roles) or from `linprog`'s dual marginals; solving the mirror LP is the low-risk choice.

**Band-vs-line test for x₁ (the key deliverable).** After obtaining the optimal game value G\*:
1. Add the constraint that X stays optimal (fix value = G\* via the equilibrium constraints for both plans).
2. Define a linear functional L(x) = total realization mass of X's *value-bet* hands (Σᵢ r(bet·call ᵢ)+r(bet·fold ᵢ)+r(check·raise ᵢ) weighted appropriately), i.e. a proxy for "where the value region ends."
3. Solve two secondary LPs: **maximize** and **minimize** L(x) subject to optimality. If max = min → x₁ is **crisp**; if they differ → x₁ is a **band**, and the gap *is* the band width. This is a rigorous, LP-native answer to the open question.

---

## 8. Discretization & exactness

- Start N=100 (fast), scale to 200/400 for precision.
- Ties (i=j) are measure-zero; set S(i,i)=0 (or 0.5) — negligible.
- **Convergence study:** solve at N∈{50,100,200,400}, Richardson-extrapolate each threshold to N→∞, report value ± discretization error. This alone suffices to distinguish a line from a band.
- **Optional true-exact:** at modest N (~40–60) run a *rational* simplex (e.g. via `sympy`/`fractions` or `sage`) for exact rational thresholds. Nice-to-have, not required for the line-vs-band verdict.

---

## 9. Validation protocol (do this BEFORE trusting any #11 number)

1. **#10 (drop check-raise):** must reproduce x₂*=0.190, x₁=0.238, x₁*=0.648, x₀=0.921, y₁=0.443 at P=2 (and match the book table at P=1,9). Gate: all within ~1/N.
2. **#7 (drop folding):** must reproduce x₁=5/9, y₁=2/3, x₂=1/9, y₂=1/3.
3. **Y-side of #11:** solved y₂,y₂*,y₁,y₀ must match Eq. 17.13 closed forms — independent confirmation the model/matrices are correct.
4. Only after 1–3 pass, report #11 X-side + the x₁ band test.

---

## 10. Implementation steps

1. `seqlp.py`: game spec (infosets, actions, terminal `uX`) — **reuse validated payoffs**.
2. Build sequence lists + index maps for X and Y.
3. Build E, e, F, f (sparse).
4. Build A (sparse, scipy.sparse) from the 9-leaf map × N×N grid.
5. Assemble and solve the primal LP for x; mirror LP for y.
6. Recover behavioral strategies; extract thresholds (x₁, x₁*, x₀, x₂, y*'s).
7. Implement the §7 band test for x₁.
8. Validation harness (§9) with pass/fail asserts.
9. Grid over P∈[0.5,20]; save `game11_exact_grid.json`.
10. If crisp: swap the exact x₁ into `game11.html` (remove the ≈/dashed treatment). If band: render x₁ as an explicit shaded band with measured width. Update `Q&A_notes.md` either way.

---

## 11. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Flow-constraint / sequence indexing bugs | Validation gates §9 (#10 exact is unforgiving) |
| Wrong chance weighting or payoff sign | #7 + Y-side closed-form cross-check |
| LP degeneracy / multiple optima misread as noise | The band test §7 is designed for exactly this — it *measures* non-uniqueness instead of hiding it |
| N too small to resolve thin bands | Convergence study §8; refine N near the boundary |
| Performance at large N | scipy HiGHS + sparse matrices; N=400 is ~6k vars, trivial for HiGHS |

---

## 12. Deliverables

- `seqlp.py` — the solver + validation harness.
- `game11_exact_grid.json` — exact thresholds (or band bounds) across P.
- Updated `game11.html` — exact x₁ (crisp) or a measured band.
- `Q&A_notes.md` update — the verdict (line vs band) and final numbers.

## 13. Effort estimate

~½–1 focused session: most of the time is (a) getting the sequence/flow bookkeeping right and (b) passing the #10/#7 validation gates. Once those pass, the #11 solve and band test are quick.

## 14. Open decisions (for when we start)

- Float-HiGHS + convergence study (fast, ~1/N precision) vs. rational simplex (true-exact, slower)? *Recommendation: float first for the line-vs-band verdict; add rational only if a crisp exact value is wanted.*
- Pot grid density and slider range to refresh in the artifact.
