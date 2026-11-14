#!/usr/bin/env python3
"""
Precision verifications:
  1. Polar-restricted game *with raises disallowed* must match the sympy
     radical V_polar = 0.0276074093 (analyze.py's exact anchor).
  2. Plateau onset: fixed grid protocol (hi=3 for all S) so values are
     comparable across S; find where V(S) first equals the deep value.
  3. Deep flatness at high precision.
"""
import json
import numpy as np
from solve import solve_S

def no_K_bet_no_raise(player, card, hist, action):
    if action[0] == "r":
        return False
    if player == 0 and card == 1 and hist == () and action[0] == "b":
        return False
    return True

PREC = dict(raise_cap=1, rounds=10, backbone_n=28, grid_cap=130, tol=1e-12)

def main():
    out = {}
    print("=== polar anchor, raises disallowed ===")
    sol = solve_S(10.0, rounds=10, backbone_n=28, grid_cap=130, tol=1e-12,
                  raise_cap=0, allowed=no_K_bet_no_raise)
    print(f"  V = {sol['value']:.10f}  (sympy radical 0.0276074093)")
    print(f"  X bet sizes: {sorted((round(s,5), round(m,3)) for s, m in sol['betX'].items() if m > 1e-4)}")
    print(f"  Y bet sizes: {sorted((round(s,5), round(m,3)) for s, m in sol['betY'].items() if m > 1e-4)}")
    out["polar_noraise_V"] = sol["value"]

    print("=== plateau onset, fixed-grid protocol ===")
    vals = {}
    for S in (0.45, 0.5, 0.53, 0.55, 0.6, 0.65, 0.7, 0.8, 1.0, 1.5, 2.0,
              3.0, 10.0):
        v = solve_S(float(S), **PREC)["value"]
        vals[S] = v
        print(f"  S={S:6.2f}  V={v:.10f}", flush=True)
    v_deep = vals[10.0]
    out["plateau_V_cap1"] = v_deep
    out["plateau_vals"] = vals
    onset = min(S for S, v in vals.items() if abs(v - v_deep) < 1e-8)
    print(f"  deep V = {v_deep:.10f}; |V-Vdeep|<1e-8 from S = {onset}")
    dev = max(abs(vals[S] - v_deep) for S in (1.0, 1.5, 2.0, 3.0))
    print(f"  flatness S in [1,3]: max dev {dev:.2e}")
    out["onset_1e8"] = onset

    with open("verify.json", "w") as fo:
        json.dump(out, fo, indent=1)
    print("wrote verify.json")

if __name__ == "__main__":
    main()
