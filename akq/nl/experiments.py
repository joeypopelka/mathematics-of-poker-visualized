#!/usr/bin/env python3
"""
Structure ablations for the full-street NL AKQ game at a deep stack (S=10).

Questions these answer:
  1. Does the solver reproduce the closed-form half-street game?  (validation:
     X forced to check, no raises -> V = (3-2*sqrt(2))/6 = 0.0285955..., with
     Y betting sqrt(2)-1 of pot.)
  2. Is the King's small "blocker bet" load-bearing, or is the classical
     polar structure (only A and Q ever bet) optimal?  (no_K_bet ablation;
     hand-derived polar-game prediction: V = 0.0276064, X bets sqrt(2)-1.)
  3. Does raise depth matter?  (cap 0 / 1 / 2 comparison.)
  4. Does the value converge as the minimum bet size -> 0?  (lo sweep.)
"""
import time
import numpy as np
from solve import solve_S, describe, allow_all

S = 10.0

def no_root_bet_X(player, card, hist, action):
    return not (player == 0 and hist == ())

def no_raises(player, card, hist, action):
    return action[0] != "r"

def half_street(player, card, hist, action):
    return no_root_bet_X(player, card, hist, action) and \
           no_raises(player, card, hist, action)

def no_K_bet(player, card, hist, action):
    return not (player == 0 and card == 1 and hist == () and action[0] == "b")

def run(tag, expect=None, **kw):
    t0 = time.time()
    sol = solve_S(S, **kw)
    dt = time.time() - t0
    exp = f"  (expected {expect:+.7f})" if expect is not None else ""
    print(f"{tag:34s} V_Y = {sol['value']:+.9f}{exp}   [{dt:5.1f}s]")
    return sol

if __name__ == "__main__":
    print(f"=== ablations at S={S} ===")
    v_half = (3 - 2 * np.sqrt(2)) / 6
    sol_h = run("half-street (X checks, no raises)", expect=v_half,
                allowed=half_street, raise_cap=0, rounds=6)
    print("   half-street Y bet sizes:",
          sorted((round(s, 5), round(m, 4)) for s, m in sol_h["betY"].items()
                 if m > 1e-4), " expect sqrt(2)-1 =", round(np.sqrt(2) - 1, 5))

    sol_polar = run("no K bets, cap 1 (polar X range)", expect=0.0276064,
                    allowed=no_K_bet, raise_cap=1, rounds=6)
    print("   polar X bet sizes:",
          sorted((round(s, 5), round(m, 4)) for s, m in sol_polar["betX"].items()
                 if m > 1e-4))
    print("   polar Y bet sizes:",
          sorted((round(s, 5), round(m, 4)) for s, m in sol_polar["betY"].items()
                 if m > 1e-4))

    sol_cap0 = run("full, no raises (cap 0)", raise_cap=0, rounds=6)
    sol_cap1 = run("full, cap 1 (baseline)", raise_cap=1, rounds=6)
    sol_cap2 = run("full, cap 2", raise_cap=2, rounds=4,
                   backbone_n=16, grid_cap=40)
    sol_cap2b = run("full, cap 2 (finer)", raise_cap=2, rounds=4,
                    backbone_n=20, grid_cap=55)

    print("=== minimum-bet-size sweep (cap 1) ===")
    for lo in (0.08, 0.04, 0.02, 0.01, 0.005, 0.0025):
        run(f"cap 1, lo={lo}", raise_cap=1, rounds=5, lo=lo)
