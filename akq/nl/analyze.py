#!/usr/bin/env python3
"""
Analysis of the full-street NL AKQ sweep.

  1. Exact closed forms (sympy) for the three solvable anchors:
       - half-street game: bet sqrt(2)-1, V = (3-2*sqrt(2))/6
       - polar-restricted full street (King barred from betting)
       - short-stack jam-only regime: V(S) = S^2 / (6*(1+S))
     each checked against the LP sweep.
  2. Regime boundaries: S_A (jam-only regime ends), S_B (plateau begins),
     plateau value and flatness.
  3. Strategy feature curves vs S (bet sizes, frequencies, line frequencies)
     -> features.json for the interactive explorer.
  4. Landmark table -> landmarks.json.
"""
import json
import numpy as np
import sympy as sp
from solve import solve_S

# ---------------------------------------------------------------- exact anchors
def exact_constants():
    out = {}
    s2 = sp.sqrt(2)

    # half-street: V(s) = s(1-s)/(6(1+s)) maximized at s* = sqrt(2)-1
    s = sp.symbols("s", positive=True)
    Vh = s * (1 - s) / (6 * (1 + s))
    s_half = sp.solve(sp.diff(Vh, s), s)
    s_half = [r for r in s_half if r.is_positive][0]
    out["half_bet"] = sp.simplify(s_half)                 # sqrt(2) - 1
    out["half_V"] = sp.simplify(Vh.subs(s, s_half))       # (3-2*sqrt(2))/6
    out["half_V_constrained"] = Vh                        # V(S) for S < s*

    # polar full street (K barred from betting):
    #   t* = sqrt(2)-1 (X's bet), a = t(1-t)/(1+t) = 3-2*sqrt(2)
    #   s* solves s^2 = a(1+s)   (Y's bet after check)
    #   beta_A = 1 - k,  k = 1/(s^2+2s);  V = (gamma*s - beta_A*alpha*s)/6
    a = 3 - 2 * s2
    s_pol = sp.solve(sp.Eq(s**2, a * (1 + s)), s)
    s_pol = [sp.simplify(r) for r in s_pol if r.is_positive][0]
    k = 1 / (s_pol**2 + 2 * s_pol)
    beta_A = 1 - k
    alpha = s_pol / (1 + s_pol)
    gamma = (1 - k * s_pol) / (1 + s_pol)
    V_pol = sp.simplify((gamma * s_pol - beta_A * alpha * s_pol) / 6)
    out["polar_t"] = s2 - 1
    out["polar_s"] = s_pol
    out["polar_betaA"] = sp.simplify(beta_A)
    out["polar_V"] = V_pol

    # short-stack jam-only regime: V(S) = S^2/(6(1+S)), derived from
    #   X jams {A, Q: S/(1+S)}, Y calls {A, K: (1-S)/(1+S)},
    #   check line: Y jams {A, Q: S/(1+S)}, X's K calls 1/(1+S).
    S = sp.symbols("S", positive=True)
    out["short_V"] = S**2 / (6 * (1 + S))
    return out

def short_V(S):
    return S * S / (6.0 * (1.0 + S))

def law_II(S):
    """Regime II exact value: X bets sqrt(2)-1 with {all A, (1-1/sqrt(2)) of
    Q}; Y jams S after a check. Tangent to the jam-only law at S=sqrt(2)-1."""
    return (S / (1.0 + S) - (3.0 - 2.0 * np.sqrt(2))) / 6.0

# ---------------------------------------------------------------- features
def feature_row(entry):
    """Flatten one strategies.json entry into plot-ready metrics."""
    S = entry["S"]
    row = {"S": S, "V": entry["value"]}
    agg = {}     # (player, card, stage, action-class) -> [mass, size*mass]
    reach = {}   # (player, card, stage) -> total reach
    for line in entry["strategy"]:
        hist = line["hist"]
        if len(hist) == 0:
            stage = "Xroot"
        elif len(hist) == 1 and hist[0][0] == "k":
            stage = "Ycheck"
        elif len(hist) == 1 and hist[0][0] == "b":
            stage = "YvsBet"
        elif len(hist) == 2 and hist[0][0] == "k" and hist[1][0] == "b":
            stage = "XvsCB"
        elif len(hist) == 2 and hist[0][0] == "b" and hist[1][0] == "r":
            stage = "XvsRaise"
        else:
            stage = "other"
        w = line["reach"]
        rkey = (line["player"], line["card"], stage)
        reach[rkey] = reach.get(rkey, 0.0) + w
        for act, amt, p in line["mix"]:
            key = (line["player"], line["card"], stage, act)
            m = agg.setdefault(key, [0.0, 0.0])
            m[0] += w * p
            m[1] += w * p * (amt if amt is not None else 0.0)
    # normalized frequencies + mass-weighted mean sizes
    for (pl, card, stage, act), (m, ms) in agg.items():
        base = f"{pl}_{card}_{stage}_{act}"
        w = reach[(pl, card, stage)]
        row[base] = m / w if w > 0 else 0.0
        if act in ("b", "r") and m > 1e-9:
            row[base + "_size"] = ms / m
    row["lines"] = entry["lines"]
    return row

# ---------------------------------------------------------------- boundaries
def refine_boundary(f, lo, hi, iters=28):
    """Bisect for the S where predicate f flips (f(lo)=True, f(hi)=False)."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if f(mid):
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-6:
            break
    return 0.5 * (lo + hi)

def main():
    d = np.load("sweep.npz")
    S, V = d["S"], d["V"]
    entries = json.load(open("strategies.json"))
    ex = exact_constants()

    print("=== exact anchors ===")
    for kk in ("half_bet", "half_V", "polar_t", "polar_s", "polar_betaA",
               "polar_V"):
        print(f"  {kk:14s} = {sp.nsimplify(ex[kk])} = {float(ex[kk]):.10f}")

    # plateau
    deep = V[S >= 3.0]
    V_plateau = float(np.median(deep))
    flat_dev = float(np.max(np.abs(deep - V_plateau)))
    print(f"\nplateau V = {V_plateau:.9f}, max |dev| for S>=3: {flat_dev:.2e}")

    # regime I & II exact laws, verified with the critical size sqrt(2)-1
    # seeded into the grid (without it the LP blurs the tangent handoff).
    t = float(np.sqrt(2) - 1)
    PREC = dict(raise_cap=1, rounds=10, backbone_n=28, grid_cap=140,
                tol=1e-12, extra_sizes=(t,))
    print("\nregime law verification (anchored high-precision solves):")
    law_checks = []
    for Sx, law, name in ((0.20, short_V, "I"), (0.35, short_V, "I"),
                          (0.4142, short_V, "I"),
                          (0.425, law_II, "II"), (0.45, law_II, "II"),
                          (0.475, law_II, "II")):
        v = solve_S(Sx, **PREC)["value"]
        r = v - law(Sx)
        law_checks.append({"S": Sx, "regime": name, "resid": r})
        print(f"  S={Sx:6.4f} regime {name}: |V - law| = {abs(r):.2e}")
        assert abs(r) < 5e-8, f"law {name} fails at S={Sx}"

    # regime I ends at exactly sqrt(2)-1 (laws tangent there; C1 handoff)
    S_A = t
    print(f"S_A (jam-only ends, exact) = sqrt(2)-1 = {S_A:.6f}")

    # II/III boundary: the King's blocker bet enters
    def k_checks(Sx):
        sol = solve_S(float(Sx), **PREC)
        for (card, hist, a), idx in sol["seqs"][0].items():
            if card == 1 and hist == () and a[0] == "b" \
                    and sol["x"][idx] > 1e-4:
                return False
        return True
    S_K = refine_boundary(k_checks, 0.47, 0.50)
    print(f"S_K (King blocker bet enters) = {S_K:.5f}")

    # plateau onset: value reaches the deep value (which happens when the
    # stack covers Y's deep bet size)
    def below_plateau(Sx):
        v = solve_S(float(Sx), **PREC)["value"]
        return v < V_plateau - 5e-7
    S_star = refine_boundary(below_plateau, 0.50, 0.55)
    print(f"S* (plateau begins) = {S_star:.5f}"
          f"  [Y's deep bet size for comparison]")

    # features
    feats = [feature_row(e) for e in entries]
    with open("features.json", "w") as fo:
        json.dump(feats, fo, indent=0)
    print(f"wrote features.json ({len(feats)} stack sizes)")

    landmarks = {
        "V_plateau_cap1": V_plateau,
        "plateau_flatness": flat_dev,
        "S_A_jam_only_ends": S_A,
        "S_A_exact": "sqrt(2)-1",
        "S_K_blocker_enters": S_K,
        "S_star_plateau_begins": S_star,
        "law_checks": law_checks,
        "law_II_exact": "(S/(1+S) - (3-2*sqrt(2)))/6",
        "half_bet": float(ex["half_bet"]),
        "half_V": float(ex["half_V"]),
        "polar_t": float(ex["polar_t"]),
        "polar_s": float(ex["polar_s"]),
        "polar_betaA": float(ex["polar_betaA"]),
        "polar_V": float(ex["polar_V"]),
        "half_bet_exact": str(sp.nsimplify(ex["half_bet"])),
        "half_V_exact": str(sp.nsimplify(ex["half_V"])),
        "polar_s_exact": str(sp.nsimplify(ex["polar_s"])),
        "polar_V_exact": str(sp.nsimplify(ex["polar_V"])),
        "short_V_exact": "S**2/(6*(1+S))",
    }
    # deep-structure snapshot (largest S entry)
    deep_entry = entries[-1]
    landmarks["deep_structure"] = {
        "X_bet_sizes": deep_entry["betX"],
        "Y_bet_sizes": deep_entry["betY"],
        "cards": deep_entry["cards"],
    }
    with open("landmarks.json", "w") as fo:
        json.dump(landmarks, fo, indent=1)
    print("wrote landmarks.json")

if __name__ == "__main__":
    main()
