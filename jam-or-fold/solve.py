#!/usr/bin/env python3
"""
Exhaustive analysis of Chen's Chapter 12 jam-or-fold NLHE game.

Game (Example 12.3, The Mathematics of Poker):
  - Equal stacks of S units. Defender posts blind 1, attacker (button) posts 0.5.
  - Attacker jams (all-in for S) or folds; if jammed, defender calls or folds.

Accounting (consistent, attacker's net):
  fold: -0.5      jam+fold: +1      jam+call: 2*S*eq - S

For fixed S the payoff is bilinear in the behavioral strategies
j in [0,1]^169 (attacker jam probs) and c in [0,1]^169 (defender call probs):

  EV(j,c) = -0.5 + 1.5 * w.j + j^T M c,
  M[A,B]  = w[A] * N[A,B] * (2*S*Q[A,B] - S - 1) / 1225

where w[A] = P(hand class A), N[A,B] = # combos of class B compatible with a
representative combo of A, Q[A,B] = mean equity of A vs those combos.
Suit symmetry makes the 169-class reduction exact.

Equilibrium via two LPs (values must agree by strong duality):
  attacker: max_j 1.5 w.j + sum_B min(0, (M^T j)_B)
  defender: min_c sum_A max(0, 1.5 w_A + (M c)_A)
"""
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, eye as speye, hstack as sphstack

RANKS = "23456789TJQKA"

# ---------------------------------------------------------------- combos/classes
def build_combos():
    combos = []
    for a in range(52):
        for b in range(a + 1, 52):
            combos.append((a, b))
    return combos

def class_of(a, b):
    ra, rb = a >> 2, b >> 2
    sa, sb = a & 3, b & 3
    hi, lo = max(ra, rb), min(ra, rb)
    if hi == lo:
        return (12 - hi) * 13 + (12 - lo)
    if sa == sb:
        return (12 - hi) * 13 + (12 - lo)   # upper triangle = suited
    return (12 - lo) * 13 + (12 - hi)       # lower triangle = offsuit

def class_label(cid):
    r, c = divmod(cid, 13)
    if r == c:
        return RANKS[12 - r] * 2
    if r < c:
        return RANKS[12 - r] + RANKS[12 - c] + "s"
    return RANKS[12 - c] + RANKS[12 - r] + "o"

def aggregate(eqm):
    """169-class N (compat counts) and Q (mean equity), exact by suit symmetry."""
    combos = build_combos()
    ccls = np.array([class_of(a, b) for a, b in combos])
    reps = {}
    for i, cl in enumerate(ccls):
        reps.setdefault(int(cl), []).append(i)
    N = np.zeros((169, 169))
    Q = np.zeros((169, 169))
    for A in range(169):
        ra = reps[A][0]
        row = eqm[ra]
        valid = row >= 0
        cnt = np.bincount(ccls[valid], minlength=169)
        ssum = np.bincount(ccls[valid], weights=row[valid].astype(np.float64), minlength=169)
        N[A] = cnt
        with np.errstate(invalid="ignore"):
            Q[A] = np.where(cnt > 0, ssum / np.maximum(cnt, 1), 0.0)
        # symmetry check against a different representative
        rb = reps[A][len(reps[A]) // 2]
        row2 = eqm[rb]
        valid2 = row2 >= 0
        cnt2 = np.bincount(ccls[valid2], minlength=169)
        ssum2 = np.bincount(ccls[valid2], weights=row2[valid2].astype(np.float64), minlength=169)
        assert np.array_equal(cnt, cnt2), f"count symmetry broken for {class_label(A)}"
        assert np.allclose(ssum, ssum2, atol=2e-4), f"equity symmetry broken for {class_label(A)}"
    w = np.array([len(reps[A]) for A in range(169)]) / 1326.0
    assert np.all(N.sum(axis=1) == 1225)
    return N, Q, w

# ---------------------------------------------------------------- LP equilibrium
class Solver:
    def __init__(self, N, Q, w):
        self.N, self.Q, self.w = N, Q, w
        self.I = speye(169, format="csr")

    def M(self, S):
        return self.w[:, None] * self.N * (2 * S * self.Q - S - 1) / 1225.0

    def solve(self, S):
        """Return (j, c, value, gA, hB). value = attacker EV per hand dealt."""
        M = self.M(S)
        # attacker LP: vars [j, t]; max 1.5 w.j + 1.t
        #   t <= 0 ; t - M^T j <= 0 ; 0 <= j <= 1
        cvec = -np.concatenate([1.5 * self.w, np.ones(169)])
        A_ub = sphstack([csr_matrix(-M.T), self.I], format="csr")
        b_ub = np.zeros(169)
        bounds = [(0, 1)] * 169 + [(None, 0)] * 169
        ra = linprog(cvec, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
        assert ra.status == 0, f"attacker LP failed at S={S}: {ra.message}"
        j = ra.x[:169]
        va = -ra.fun - 0.5

        # defender LP: vars [c, u]; min 1.u  s.t. u >= 0, u >= 1.5w + Mc, 0<=c<=1
        cvec2 = np.concatenate([np.zeros(169), np.ones(169)])
        A_ub2 = sphstack([csr_matrix(M), -self.I], format="csr")
        b_ub2 = -1.5 * self.w
        bounds2 = [(0, 1)] * 169 + [(0, None)] * 169
        rd = linprog(cvec2, A_ub=A_ub2, b_ub=b_ub2, bounds=bounds2, method="highs")
        assert rd.status == 0, f"defender LP failed at S={S}: {rd.message}"
        c = rd.x[:169]
        vd = rd.fun - 0.5
        assert abs(va - vd) < 1e-6, f"duality gap {va - vd} at S={S}"

        # marginals (per unit of hand prob, relative to folding)
        gA = 1.5 * self.w + M @ c          # attacker jam gain, scaled by w
        hB = -(M.T @ j)                    # defender call gain, scaled (>0 => call)
        return j, c, va, gA, hB

# ---------------------------------------------------------------- sweep
def run():
    eqm = np.fromfile("equity.f32", dtype=np.float32).reshape(1326, 1326)
    N, Q, w = aggregate(eqm)
    labels = [class_label(i) for i in range(169)]
    L = {lab: i for i, lab in enumerate(labels)}
    sol = Solver(N, Q, w)

    # ---- validation vs Chen ----
    print("=== validation ===")
    qATs, qA5s = Q[L["ATs"], L["AA"]], Q[L["A5s"], L["AA"]]
    print(f"ATs vs AA equity: {qATs:.5f} (Chen 0.13336)")
    print(f"A5s vs AA equity: {qA5s:.5f} (Chen 0.13331)")
    # threshold vs AA-only caller, consistent accounting and Chen's convention
    for lab in ["ATs", "A5s", "AJs", "A4s", "AQs", "A3s", "AKs", "A2s", "KK"]:
        A = L[lab]
        nAA = N[A, L["AA"]]
        q = Q[A, L["AA"]]
        s_cons = (1.5 * (1225 - nAA) + 0.5 * nAA) / (nAA * (1 - 2 * q))
        s_chen = 1.5 * (1225 - nAA) / (nAA * (1 - 2 * q))
        print(f"  {lab:4s} enters (vs AA-only caller) at S={s_cons:8.2f}"
              f"  [Chen-convention: {s_chen:8.2f}]  n_AA={nAA:.0f} q={q:.5f}")

    j, c, v, _, _ = sol.solve(1500.0)
    print("equilibrium at S=1500 (expect AA only both sides):")
    print("  jam:", [(labels[i], round(j[i], 4)) for i in np.where(j > 1e-6)[0]])
    print("  call:", [(labels[i], round(c[i], 4)) for i in np.where(c > 1e-6)[0]])

    j, c, v, _, _ = sol.solve(833.0)
    print("equilibrium at S=833 (Chen: AA 100%, ATs 87.73%->mix, A5s 100%):")
    print("  jam:", [(labels[i], round(j[i], 4)) for i in np.where(j > 1e-6)[0]])
    print("  call:", [(labels[i], round(c[i], 4)) for i in np.where(c > 1e-6)[0]])

    # ---- stack grid ----
    grid = np.unique(np.concatenate([
        np.round(np.geomspace(1.0, 2500.0, 900), 6),
        np.round(np.arange(1.0, 25.0, 0.05), 6),
    ]))
    print(f"=== sweep: {len(grid)} stack sizes ===")
    JJ = np.zeros((len(grid), 169))
    CC = np.zeros((len(grid), 169))
    VV = np.zeros(len(grid))
    for k, S in enumerate(grid):
        jk, ck, vk, _, _ = sol.solve(float(S))
        JJ[k], CC[k], VV[k] = jk, ck, vk
        if k % 100 == 0:
            print(f"  S={S:9.3f}  value={vk:+.5f}  jam%={np.dot(w, jk)*100:6.2f} "
                  f" call%={np.dot(w, ck)*100:6.2f}")

    np.savez_compressed("sweep.npz", grid=grid, J=JJ, C=CC, V=VV, w=w,
                        labels=np.array(labels))
    print("wrote sweep.npz")

    # ---- threshold refinement by bisection on membership flips ----
    EPS = 1e-6
    thresholds = []
    for side, X in (("jam", JJ), ("call", CC)):
        for h in range(169):
            memb = X[:, h] > EPS
            flips = np.where(memb[:-1] != memb[1:])[0]
            for f in flips:
                lo, hi = float(grid[f]), float(grid[f + 1])
                lo_in = bool(memb[f])
                for _ in range(30):
                    mid = 0.5 * (lo + hi)
                    jm, cm, _, _, _ = sol.solve(mid)
                    x = jm[h] if side == "jam" else cm[h]
                    if (x > EPS) == lo_in:
                        lo = mid
                    else:
                        hi = mid
                    if hi - lo < 1e-4:
                        break
                sc = 0.5 * (lo + hi)
                thresholds.append({
                    "hand": labels[h], "side": side, "S": round(sc, 4),
                    "dir": "exits_as_S_increases" if lo_in else "enters_as_S_increases",
                })
    thresholds.sort(key=lambda t: -t["S"])
    with open("thresholds.json", "w") as fo:
        json.dump(thresholds, fo, indent=1)
    print(f"wrote thresholds.json ({len(thresholds)} transitions)")

    # ---- oddity mining: frequency jumps between adjacent grid points ----
    jumps = []
    for side, X in (("jam", JJ), ("call", CC)):
        d = np.abs(np.diff(X, axis=0))
        for k, h in zip(*np.where(d > 0.25)):
            jumps.append({
                "hand": labels[h], "side": side,
                "S_from": float(grid[k]), "S_to": float(grid[k + 1]),
                "freq_from": round(float(X[k, h]), 4),
                "freq_to": round(float(X[k + 1, h]), 4),
            })
    jumps.sort(key=lambda t: -t["S_from"])
    with open("jumps.json", "w") as fo:
        json.dump(jumps, fo, indent=1)
    print(f"wrote jumps.json ({len(jumps)} discontinuities > 0.25 freq)")

    # non-monotonic range membership (enters, exits, re-enters as S decreases)
    print("=== non-monotonic hands (jam) ===")
    for h in range(169):
        m = (JJ[:, h] > EPS).astype(int)
        nflips = int(np.abs(np.diff(m)).sum())
        if nflips > 1:
            print(f"  {labels[h]}: {nflips} membership flips")

if __name__ == "__main__":
    run()
