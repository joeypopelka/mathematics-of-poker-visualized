#!/usr/bin/env python3
"""Phase-2 analysis run: exact LP results for games #11 and #12.

Produces:
  game11_exact_grid.json  -- monotone-selection thresholds + exact values
                             across the artifact's P grid, plus the x1 band
                             analysis and N-convergence evidence at P=2.
  game12_value.json       -- the finite-pot game #12 value (the number the
                             book declined to compute) across P, with raise-cap
                             convergence evidence and cascade validation.
  values_fp.json          -- exact G(Y) curves for #9/#10/#11/#12 on a dense
                             pot grid (for the family hub page).
"""
import json
import time
import numpy as np
from seqlp import (solve_game, solve_ladder, monotone_selection,
                   monotone_selection_ladder, solve_seq_lp, crossing,
                   band_test_x1, NX, NY, validate)


def thresholds_11(P, N):
    """Exact value + Y-side + monotone-selection X-side for game #11."""
    s = solve_game(P, N, allowCR=True)
    v = s["v"]
    Xm = monotone_selection(s, "X")
    Ym = monotone_selection(s, "Y")
    out = dict(P=P, N=N, GY=s["GY"])
    # Y-side (exact closed forms exist; cross-check)
    a, a2 = 1 / (P + 1), 1 / (P + 3)
    R = (1 - a2) / 2
    y1c = (1 - a) / (1 + a + (1 - a2) * R)
    out["y1_closed"] = y1c
    out["y1"] = crossing(Ym[:, 4], v)
    out["y2"] = crossing(Ym[:, 1], v)
    # Y give-up thresholds: y1* = top edge of flat-call region facing a bet;
    # y2# = where fold begins (raise-bluffs occupy [y1*, y2#])
    call = Ym[:, 2]
    idx = np.where(call > 0.5)[0]
    out["y1s"] = float(v[idx[-1]] + 0.5 / N) if len(idx) else None
    fold = Ym[:, 3]
    idx = np.where(fold > 0.5)[0]
    out["y2h"] = float(v[idx[0]] - 0.5 / N) if len(idx) else None
    # X-side monotone selection
    out["x1"] = crossing(Xm[:, 1] + Xm[:, 5], v)         # value continue ends
    out["x1_bet"] = crossing(Xm[:, 1], v)                 # pure bet cutoff
    cr = np.where(Xm[:, 5] > 0.5)[0]
    out["cr_span"] = ([float(v[cr[0]] - 0.5 / N), float(v[cr[-1]] + 0.5 / N)]
                      if len(cr) else None)                # check-raise region
    out["x2s"] = crossing(Xm[:, 3], v)                    # bet-call cutoff
    out["x1s"] = crossing(Xm[:, 7], v, up=True)           # first check-fold
    # x0: bottom of X's bluff region (bet or check-raise bluffs resume at bottom)
    aggr = Xm[:, 1] + Xm[:, 5]
    x0 = None
    for i in range(N - 1, 0, -1):
        if aggr[i] > 0.5 and aggr[i - 1] < 0.5:
            x0 = float(v[i] - 0.5 / N)
            break
    out["x0"] = x0
    # check-raise usage
    out["cr_mass"] = float(Xm[:, 5].sum() / N)
    out["cr_bluff"] = bool((Xm[int(N * 0.75):, 5] > 0.5).any())
    return out


def run_game11(grid_P, N=240):
    rows = []
    for P in grid_P:
        t0 = time.time()
        r = thresholds_11(P, N)
        rows.append(r)
        print(f"#11 P={P}: GY={r['GY']:.5f} x1={r['x1']} x1s={r['x1s']} "
              f"y1s={r['y1s']} y2h={r['y2h']}  ({time.time()-t0:.1f}s)",
              flush=True)
    return rows


def run_band(P=2.0, N=160):
    """The x1 line-vs-band verdict at pot P."""
    print(f"--- band analysis P={P} N={N} ---", flush=True)
    s = solve_game(P, N, allowCR=True)
    bt = band_test_x1(s)
    # aggregate continue mass (bet + check-raise): pinned?
    G = s["value"]
    floor = G - 1e-8 * max(1, abs(G))
    L = np.zeros(NX * N)
    L[1::NX] = 1.0
    L[5::NX] = 1.0
    _, _, hi = solve_seq_lp(s["A"], s["E"], s["e"], s["F"], s["f"],
                            s["ub"], s["vb"] > 0, L, floor)
    _, _, lo = solve_seq_lp(s["A"], s["E"], s["e"], s["F"], s["f"],
                            s["ub"], s["vb"] > 0, -L, floor)
    v = s["v"]
    pb = [dict(v=float(v[i]), lo=round(float(l), 4), hi=round(float(h), 4))
          for i, l, h in bt["per_bucket"]]
    # Y-side: per-bucket fold-probability band in the give-up window (settles
    # whether y1*/y2# are pinned)
    AY = (-s["A"].T).tocsr()
    floorY = -G - 1e-8 * max(1, abs(G))
    ybands = []
    for j in range(N):
        if not (0.55 <= v[j] <= 0.85):
            continue
        Lj = np.zeros(NY * N)
        Lj[j * NY + 3] = 1.0
        _, _, hi_f = solve_seq_lp(AY, s["F"], s["f"], s["E"], s["e"],
                                  s["vb"], s["ub"] > 0, Lj, floorY)
        _, _, lo_f = solve_seq_lp(AY, s["F"], s["f"], s["E"], s["e"],
                                  s["vb"], s["ub"] > 0, -Lj, floorY)
        ybands.append(dict(v=float(v[j]), lo=round(float(-lo_f), 4),
                           hi=round(float(hi_f), 4)))
    out = dict(P=P, N=N, GY=s["GY"],
               bet_mass_min=round(bt["bet_mass_min"], 5),
               bet_mass_max=round(bt["bet_mass_max"], 5),
               continue_mass_min=round(-lo / N, 5),
               continue_mass_max=round(hi / N, 5),
               n_band_buckets=len(pb), per_bucket=pb, y_fold_band=ybands)
    print(f"bet mass in [{out['bet_mass_min']},{out['bet_mass_max']}] | "
          f"bet+cr mass in [{out['continue_mass_min']},"
          f"{out['continue_mass_max']}] | free buckets: {len(pb)}", flush=True)
    return out


def run_nconv(P=2.0, Ns=(100, 200, 400)):
    rows = []
    for N in Ns:
        t0 = time.time()
        r = thresholds_11(P, N)
        r["dt"] = round(time.time() - t0, 1)
        rows.append(r)
        print(f"N={N}: GY={r['GY']:.6f} x1={r['x1']} x1s={r['x1s']}",
              flush=True)
    return rows


def run_game12(grid_P, N=200, Bs=(2, 4, 6, 8, 10, 12)):
    """G12(P) with raise-cap convergence; cascade validation at P=2."""
    rows = []
    for P in grid_P:
        conv = []
        for B in Bs:
            s = solve_ladder(P, N, B)
            conv.append(round(s["GY"], 8))
        # geometric tail estimate: d_k = conv[k]-conv[k-1]
        d1, d2 = conv[-2] - conv[-3], conv[-1] - conv[-2]
        if abs(d1) > 1e-14 and abs(d2 / d1) < 1:
            extra = d2 * (d2 / d1) / (1 - d2 / d1)
        else:
            extra = 0.0
        GY = conv[-1] + extra
        rows.append(dict(P=P, conv=conv, GY=round(GY, 7),
                         tail=round(extra, 9)))
        print(f"#12 P={P}: GY(B)={conv} -> {GY:.6f}", flush=True)
    return rows


def cascade_check(P=2.0, N=400, B=8):
    """Validate the value cascade x1 -> y2 -> x3 -> y4 at P=2 vs the notes."""
    s = solve_ladder(P, N, B)
    Xm = monotone_selection_ladder(s, "X")
    Ym = monotone_selection_ladder(s, "Y")
    v = s["v"]
    xk, yk = s["xk"], s["yk"]
    out = dict(P=P, N=N, B=B, GY=s["GY"])
    out["x1"] = crossing(Xm[:, xk["made1"]], v)
    out["y2"] = crossing(Ym[:, yk["yr1"]], v)
    out["x3"] = crossing(Xm[:, xk["xr2"]], v)
    out["y4"] = crossing(Ym[:, yk["yr3"]], v)
    out["y1"] = crossing(Ym[:, yk["bet"]], v)
    out["x1s"] = crossing(Xm[:, xk["chk_fold"]], v, up=True)
    print(f"cascade P=2: x1={out['x1']} (0.248) y2={out['y2']} (0.086) "
          f"x3={out['x3']} (0.031) y4={out['y4']} (0.012) "
          f"y1={out['y1']} (0.449) x1s={out['x1s']} (0.650)", flush=True)
    return out


def run_values(grid_P, N=150):
    """Exact G(Y) curves for #9/#10/#11 (LP) on a dense grid."""
    out = {"P": list(grid_P), "g9": [], "g10": [], "g11": []}
    for P in grid_P:
        s9 = solve_game(P, N, allowCR=False, allowRaise=False)
        s10 = solve_game(P, N, allowCR=False)
        s11 = solve_game(P, N, allowCR=True)
        out["g9"].append(round(s9["GY"], 6))
        out["g10"].append(round(s10["GY"], 6))
        out["g11"].append(round(s11["GY"], 6))
        print(f"values P={P}: {out['g9'][-1]} {out['g10'][-1]} "
              f"{out['g11'][-1]}", flush=True)
    return out


def main():
    t0 = time.time()
    assert validate(150), "validation gates failed"

    artifact_P = [0.4, 0.7, 1, 1.5, 2, 3, 4, 6, 9, 14, 25, 60, 150]
    g11 = dict(grid=run_game11(artifact_P, N=240),
               band=run_band(2.0, 160),
               band_P9=run_band(9.0, 160),
               nconv=run_nconv(2.0, (100, 200, 400)))
    json.dump(g11, open("game11_exact_grid.json", "w"), indent=1)
    print(f"[game11_exact_grid.json] {time.time()-t0:.0f}s", flush=True)

    value_P = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10,
               13, 17, 22, 30, 45, 70, 120, 200]
    g12 = dict(curve=run_game12(value_P, N=200),
               cascade=cascade_check(2.0, 400, 8),
               limit_check=run_game12([1000.0], N=200)[0])
    json.dump(g12, open("game12_value.json", "w"), indent=1)
    print(f"[game12_value.json] {time.time()-t0:.0f}s", flush=True)

    vals = run_values(value_P, N=150)
    # splice #12 curve in for the hub
    vals["g12"] = [r["GY"] for r in g12["curve"]]
    json.dump(vals, open("values_fp.json", "w"), indent=1)
    print(f"[values_fp.json] done {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
