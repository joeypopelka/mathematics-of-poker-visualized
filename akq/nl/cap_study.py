#!/usr/bin/env python3
"""
Raise-cap convergence study: the sweep uses raise cap 1; this quantifies the
correction from deeper raise wars (cap 2, cap 3) on identical grid protocols,
across stacks, so the report can state cap-infinity values with error bars.
"""
import json
import time
import numpy as np
from solve import solve_S

PROTO = dict(rounds=4, backbone_n=18, grid_cap=48)
S_LIST = [0.3, 0.5, 0.75, 1.0, 1.5, 2.5, 5.0, 10.0, 25.0, 60.0]
CAP3_LIST = [0.5, 1.0, 2.5, 10.0]

def main():
    rows = []
    for S in S_LIST:
        row = {"S": S}
        for cap in (1, 2):
            t0 = time.time()
            v = solve_S(S, raise_cap=cap, **PROTO)["value"]
            row[f"cap{cap}"] = v
            print(f"S={S:6.2f} cap{cap}: V={v:+.9f}  [{time.time()-t0:5.1f}s]",
                  flush=True)
        if S in CAP3_LIST:
            t0 = time.time()
            v = solve_S(S, raise_cap=3, **PROTO)["value"]
            row["cap3"] = v
            print(f"S={S:6.2f} cap3: V={v:+.9f}  [{time.time()-t0:6.1f}s]",
                  flush=True)
        rows.append(row)
    for r in rows:
        d21 = r["cap2"] - r["cap1"]
        line = f"S={r['S']:6.2f}  cap1={r['cap1']:+.8f}  d(2-1)={d21:+.2e}"
        if "cap3" in r:
            d32 = r["cap3"] - r["cap2"]
            # geometric extrapolation of the alternating tail
            ratio = d32 / d21 if abs(d21) > 1e-12 else 0.0
            vinf = r["cap3"] + (d32 * ratio / (1 - ratio)
                                if abs(ratio) < 0.9 else 0.0)
            line += f"  d(3-2)={d32:+.2e}  ratio={ratio:+.3f}  Vinf~{vinf:+.8f}"
        print(line)
    with open("cap_study.json", "w") as fo:
        json.dump(rows, fo, indent=1)
    print("wrote cap_study.json")

if __name__ == "__main__":
    main()
