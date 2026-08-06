#!/usr/bin/env python3
"""Post-sweep analysis: strict-margin verification, band structure, Chen comparisons."""
import json
import numpy as np
from solve import aggregate, class_label, Solver

def main():
    eqm = np.fromfile("equity.f32", dtype=np.float32).reshape(1326, 1326)
    N, Q, w = aggregate(eqm)
    labels = [class_label(i) for i in range(169)]
    L = {lab: i for i, lab in enumerate(labels)}
    sol = Solver(N, Q, w)

    d = np.load("sweep.npz", allow_pickle=True)
    grid, J, C, V = d["grid"], d["J"], d["C"], d["V"]
    n = len(grid)

    # per-hand normalized jam margin (bb per hand instance, relative to fold)
    # gA/w = 1.5 + (N/1225 * (2SQ - S - 1)) . c ; same for defender call margin
    TOL = 1e-7
    statusJ = np.zeros((n, 169), dtype=int)  # 0 out, 1 mixed/indiff, 2 in
    statusC = np.zeros((n, 169), dtype=int)
    for k, S in enumerate(grid):
        pay = N * (2 * S * Q - S - 1) / 1225.0     # attacker's called payoff coeffs
        gj = 1.5 + pay @ C[k]                       # jam margin per class
        # defender: margin of calling vs folding, conditional on jam; unnormalized
        # call gain = sum_A N[B,A] j_A * -(2SQ[B,A]-S-1)/1225 ... relative to fold (-1)*P(jam|B)
        pj = (N * J[k][None, :]).sum(axis=1)        # P(jam | defender B) * 1225
        gc = (N * J[k][None, :] * (-(2 * S * Q - S - 1))).sum(axis=1) / 1225.0 \
             + (pj / 1225.0) * 1.0                  # + fold loss avoided
        scale = max(1.0, 0.001 * S)
        statusJ[k] = np.where(gj > TOL * scale, 2, np.where(gj < -TOL * scale, 0, 1))
        statusC[k] = np.where(gc > TOL * scale, 2, np.where(gc < -TOL * scale, 0, 1))
        # strict-in must be jammed at freq 1; strict-out at 0 (consistency)
        assert np.all(J[k][statusJ[k] == 2] > 1 - 1e-6), f"S={S} strict-in not jammed"
        assert np.all(J[k][statusJ[k] == 0] < 1e-6), f"S={S} strict-out jammed"

    def bands(X, h, eps=1e-6):
        """[(S_lo, S_hi, mean_freq)] intervals where hand h is in range."""
        memb = X[:, h] > eps
        out = []
        k = 0
        while k < n:
            if memb[k]:
                k0 = k
                while k < n and memb[k]:
                    k += 1
                out.append((float(grid[k0]), float(grid[k - 1]),
                            float(X[k0:k, h].mean())))
            else:
                k += 1
        return out

    print("=== Chen's 'broken strategy' hands (his table: 63s 2.3, 5.1-7.1 | "
          "53s 2.4, 4.1-12.9 | 43s 2.2, 4.8-10.0) ===")
    for lab in ["63s", "53s", "43s"]:
        bs = bands(J, L[lab])
        pretty = ", ".join(f"[{a:.2f}..{b:.2f}] f~{f:.2f}" for a, b, f in bs)
        print(f"  {lab}: {pretty}")

    print("=== S=10 comparison (Chen: jam 774/1326=58.37%, call 494/1326=37.25%) ===")
    k10 = int(np.argmin(np.abs(grid - 10.0)))
    print(f"  S={grid[k10]}: jam {np.dot(w, J[k10])*100:.2f}%  "
          f"({np.dot(w, J[k10])*1326:.1f}/1326 combos), "
          f"call {np.dot(w, C[k10])*100:.2f}%  ({np.dot(w, C[k10])*1326:.1f}/1326)")
    print("  97s jam bands (Chen: jam up to ~36):", bands(J, L["97s"]))

    print("=== ATs full band structure (jam) ===")
    for lab in ["ATs", "AKs", "A5s", "KK", "AKo", "QQ", "JJ", "TT"]:
        for side, X in (("jam", J), ("call", C)):
            bs = bands(X, L[lab])
            if len(bs) > 4:
                bs = bs[:2] + [("...", "...", 0)] + bs[-2:]
            pretty = ", ".join(
                f"[{a if isinstance(a,str) else round(a,2)}..{b if isinstance(b,str) else round(b,2)}]"
                for a, b, f in bs)
            print(f"  {lab:4s} {side}: {pretty}")

    # strict verification of non-monotonic windows: margins in gap interiors
    print("=== strict-margin verification of ATs gaps ===")
    for S in [500.0, 145.0, 700.0, 300.0]:
        j, c, v, gA, hB = sol.solve(S)
        gn = gA[L["ATs"]] / w[L["ATs"]]
        print(f"  S={S}: ATs jam freq={j[L['ATs']]:.4f}, "
              f"normalized jam margin={gn:+.2e} bb")

    # count truly strict non-monotonic hands (ignore mixed chatter)
    print("=== hands with strict OUT window between strict IN regions (jam) ===")
    curated = {}
    for h in range(169):
        s = statusJ[:, h]
        # compress to runs of pure states, mixed (1) treated as its neighbor-bridge
        runs = []
        for k in range(n):
            st = s[k]
            if st == 1:
                continue
            if not runs or runs[-1][0] != st:
                runs.append([st, k, k])
            else:
                runs[-1][2] = k
        pat = [r[0] for r in runs]
        flips = sum(1 for a, b in zip(pat, pat[1:]) if a != b)
        if flips >= 3:  # in-out-in at least (reading upward)
            wins = []
            for st, k0, k1 in runs:
                if st == 0 and k0 > 0 and k1 < n - 1:
                    wins.append((round(float(grid[k0]), 2), round(float(grid[k1]), 2)))
            if wins:
                curated[labels[h]] = wins
                print(f"  {labels[h]}: strictly OUT on {wins}")
    with open("strict_gaps.json", "w") as f:
        json.dump(curated, f, indent=1)
    print(f"wrote strict_gaps.json ({len(curated)} hands with strict gaps)")

if __name__ == "__main__":
    main()
