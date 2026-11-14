#!/usr/bin/env python3
"""Round 2: (a) cap 1 vs cap 2 on identical grids, (b) short-stack probes,
(c) structure of the full equilibrium at S=10."""
import time
import numpy as np
from solve import solve_S, describe, strategy_lines

def run(tag, **kw):
    t0 = time.time()
    sol = solve_S(**kw)
    print(f"{tag:44s} V_Y = {sol['value']:+.9f}   [{time.time()-t0:5.1f}s]")
    return sol

if __name__ == "__main__":
    print("=== cap 1 vs cap 2, identical grid protocol (S=10) ===")
    for cap in (1, 2):
        run(f"S=10 cap {cap} backbone20/grid55", S=10.0, raise_cap=cap,
            rounds=4, backbone_n=20, grid_cap=55)
    for cap in (1, 2):
        run(f"S=10 cap {cap} backbone16/grid40", S=10.0, raise_cap=cap,
            rounds=4, backbone_n=16, grid_cap=40)

    print("=== cap 2 vs cap 3 at moderate stack (S=1, cheaper tree) ===")
    for cap in (1, 2, 3):
        run(f"S=1 cap {cap} backbone16/grid40", S=1.0, raise_cap=cap,
            rounds=4, backbone_n=16, grid_cap=40)

    print("=== stack-size probes (cap 1, then spot-check cap 2) ===")
    for S in (0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 30.0):
        run(f"S={S} cap 1", S=S, raise_cap=1, rounds=5)
    for S in (0.2, 0.5, 1.5):
        run(f"S={S} cap 2 backbone16/grid40", S=S, raise_cap=2,
            rounds=4, backbone_n=16, grid_cap=40)

    print("=== full equilibrium structure at S=10 (cap 1) ===")
    sol = solve_S(S=10.0, raise_cap=1, rounds=5, verbose=True)
    print("--- X root bet mass by size ---")
    for s, m in sorted(sol["betX"].items()):
        if m > 1e-4: print(f"   bet {s:8.4f}: {m:.4f}")
    print("--- Y bet-after-check mass by size ---")
    for s, m in sorted(sol["betY"].items()):
        if m > 1e-4: print(f"   bet {s:8.4f}: {m:.4f}")
    print("--- Y raise mass by size ---")
    for s, m in sorted(sol["raiseY"].items()):
        if m > 1e-4: print(f"   raise-to {s:8.4f}: {m:.4f}")
    print("--- X raise mass by size ---")
    for s, m in sorted(sol["raiseX"].items()):
        if m > 1e-4: print(f"   raise-to {s:8.4f}: {m:.4f}")
    print("--- per-infoset behavioral detail (realization-weighted) ---")
    describe(sol)
