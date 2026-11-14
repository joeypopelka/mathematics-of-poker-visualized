#!/usr/bin/env python3
"""
Sweep the full-street NL AKQ equilibrium across starting stacks S.

For each S: refined-grid sequence-form LP solve (raise cap 1, validated
against cap 2/3 in experiments), then summarize:
  - game value to Y (position),
  - per-card bet frequencies and mass-weighted mean sizes,
  - line frequencies (deal-weighted probability of each betting line),
  - per-deal EV decomposition.

Outputs sweep.npz (arrays) + strategies.json (per-S structure detail).
"""
import json
import sys
import numpy as np
from multiprocessing import Pool
from solve import (solve_S, build_tree, build_sequence_form, onpath_lines,
                   CARDS, DEALS)

def leaf_stats(sol):
    """Deal-weighted line frequencies and per-deal EV using the exact
    equilibrium realization plans."""
    S = sol["S"]
    root, _ = build_tree(S, sol["sizes"], 1)
    seqs = sol["seqs"]
    x, y = sol["x"], sol["y"]
    lines = {}          # line label -> probability
    deal_ev = {}        # (cx, cy) -> Y's conditional EV
    card_line = {}      # (player, card, linetype) -> prob

    def label(hist):
        return "-".join(a for a, _ in hist)

    def walk(node, sx, sy, cx, cy):
        for a, child in zip(node.actions, node.children):
            nsx, nsy = sx, sy
            if node.player == 0:
                sk = (cx, node.hist, a)
                if sk not in seqs[0]: continue
                nsx = seqs[0][sk]
            else:
                sk = (cy, node.hist, a)
                if sk not in seqs[1]: continue
                nsy = seqs[1][sk]
            if child.player is None:
                p = x[nsx] * y[nsy]
                if p <= 0: continue
                if child.kind == "fold":
                    pay = (0.5 + child.bx) if node.player == 0 else -(0.5 + child.by)
                else:
                    pay = (0.5 + child.bx) if cy > cx else -(0.5 + child.by)
                lines[label(child.hist)] = lines.get(label(child.hist), 0.0) + p / 6.0
                deal_ev[(cx, cy)] = deal_ev.get((cx, cy), 0.0) + p * pay
            else:
                walk(child, nsx, nsy, cx, cy)

    for cx, cy in DEALS:
        walk(root, 0, 0, cx, cy)
    return lines, deal_ev

def card_summary(sol):
    """Per-card aggression summary from realization plans."""
    out = {}
    for player, name in ((0, "X"), (1, "Y")):
        plan = sol["x"] if player == 0 else sol["y"]
        for card in range(3):
            bet_m, bet_ws, raise_m, raise_ws = 0.0, 0.0, 0.0, 0.0
            for (c, hist, a), idx in sol["seqs"][player].items():
                if c != card or plan[idx] <= 1e-12: continue
                if a[0] == "b" and len(hist) <= 1:      # first-in bet
                    bet_m += plan[idx]; bet_ws += plan[idx] * a[1]
                elif a[0] == "r":
                    raise_m += plan[idx]; raise_ws += plan[idx] * a[1]
            out[f"{name}_{CARDS[card]}"] = {
                "bet_freq": bet_m,
                "bet_mean_size": bet_ws / bet_m if bet_m > 1e-12 else 0.0,
                "raise_mass": raise_m,
                "raise_mean_to": raise_ws / raise_m if raise_m > 1e-12 else 0.0,
            }
    return out

def solve_one(S):
    sol = solve_S(float(S), raise_cap=1, rounds=6, tol=1e-10, clean=True)
    lines, deal_ev = leaf_stats(sol)
    summ = card_summary(sol)
    root, _ = build_tree(sol["S"], sol["sizes"], 1)
    strat = onpath_lines(sol, root)
    slim = {
        "S": float(S),
        "value": float(sol["value"]),
        "betX": {f"{k:.10g}": float(v) for k, v in sol["betX"].items() if v > 1e-7},
        "betY": {f"{k:.10g}": float(v) for k, v in sol["betY"].items() if v > 1e-7},
        "raiseX": {f"{k:.10g}": float(v) for k, v in sol["raiseX"].items() if v > 1e-7},
        "raiseY": {f"{k:.10g}": float(v) for k, v in sol["raiseY"].items() if v > 1e-7},
        "cards": summ,
        "lines": {k: float(v) for k, v in sorted(lines.items()) if v > 1e-9},
        "deal_ev": {f"{CARDS[cx]}{CARDS[cy]}": float(v)
                    for (cx, cy), v in deal_ev.items()},
        "strategy": strat,
    }
    print(f"  S={S:9.4f}  V={sol['value']:+.8f}", flush=True)
    return slim

def main():
    grid = np.unique(np.round(np.concatenate([
        np.geomspace(0.05, 100.0, 220),
        np.arange(0.02, 1.52, 0.02),
        [np.sqrt(2) - 1, 0.5087902, 1/3, 0.25, 2/3],
    ]), 8))
    print(f"=== sweep: {len(grid)} stack sizes ===")
    with Pool(8) as pool:
        results = pool.map(solve_one, grid.tolist())
    results.sort(key=lambda r: r["S"])
    S = np.array([r["S"] for r in results])
    V = np.array([r["value"] for r in results])
    np.savez_compressed("sweep.npz", S=S, V=V)
    with open("strategies.json", "w") as fo:
        json.dump(results, fo, indent=0)
    print("wrote sweep.npz, strategies.json")
    print(f"V range: min {V.min():+.6f} at S={S[V.argmin()]:.3f}, "
          f"max {V.max():+.6f} at S={S[V.argmax()]:.3f}, "
          f"V(deep)={V[-1]:+.6f}")

if __name__ == "__main__":
    main()
