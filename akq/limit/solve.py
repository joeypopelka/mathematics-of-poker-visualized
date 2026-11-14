#!/usr/bin/env python3
"""The limit AKQ game (ch. 13, Examples 13.1-13.2) — closed forms verified
against a direct equilibrium solve of the full game matrix.

Three-card deck {A, K, Q}; each player one card; pot P; limit bet of 1;
one half street (Y may bet, X may call/fold). Ex-showdown payoffs to Y.

Book closed forms (P >= 1):
  b* = 1/(P+1) = alpha   (Y's bluff frequency with a queen)
  c* = (P-1)/(P+1)        (X's call frequency with a king)
  G(Y) = (P-1)/(6(P+1));  P -> inf limit 1/6.
For P < 1 bluffing is unprofitable even vs. always-fold (aces outnumber
kings in X's conditional range), so b* = c* = 0 and G(Y) = 0.

Undominated strategy space: Y bets all aces + b of queens; X calls all aces
+ c of kings. V(b, c) is bilinear -> solve the 2-variable saddle point by
grid + verification of the indifference conditions.
"""
import json


def value(P, b, c):
    """Ex-showdown EV to Y; each of the 6 deals has probability 1/6.

    (Y hand, X hand): contributions
      (A,K): Y bets; X calls c: +1, folds: 0 (ex-showdown: pot was Y's anyway
             -> folding yields 0 extra, calling pays a bet)
      (A,Q): Y bets; X folds always (dominated otherwise): 0
      (K,*): Y checks kings (dominated to bet): 0
      (Q,A): Y bluffs b; X calls (always with ace): -b
      (Q,K): Y bluffs b; X calls c: -bc, folds (1-c): +bP
    """
    return (c * 1 + b * (-1) + b * (c * (-1) + (1 - c) * P)) / 6.0


def closed(P):
    if P <= 1:
        return 0.0, 0.0, 0.0
    b = 1.0 / (P + 1)
    c = (P - 1.0) / (P + 1)
    g = (P - 1.0) / (6 * (P + 1))
    return b, c, g


def saddle(P, n=2001):
    """max_b min_c V on a fine grid (V bilinear -> exact at grid resolution)."""
    import numpy as np
    bs = np.linspace(0, 1, n)
    cs = np.linspace(0, 1, n)
    # V(b,c) = [c - b + b(-c + (1-c)P)] / 6 ; vectorized min over c for each b
    B, C = np.meshgrid(bs, cs, indexing="ij")
    V = (C - B + B * (-C + (1 - C) * P)) / 6.0
    lower = V.min(axis=1)                 # Y guarantees
    bstar = bs[lower.argmax()]
    gY = lower.max()
    upper = V.max(axis=0)                 # X concedes
    cstar = cs[upper.argmin()]
    gX = upper.min()
    return bstar, cstar, gY, gX


def main():
    print("P      b*(book)  b*(solve)  c*(book)  c*(solve)  G(book)   G(solve)")
    rows = []
    ok = True
    for P in (0.5, 0.8, 1.0, 1.1, 1.5, 2.0, 3.0, 5.0, 9.0, 20.0, 100.0):
        b0, c0, g0 = closed(P)
        bs, cs, gY, gX = saddle(P)
        assert abs(gY - gX) < 1e-3, (P, gY, gX)       # saddle point exists
        ok &= abs(gY - g0) < 1e-3 and abs(bs - b0) < 1e-3 and abs(cs - c0) < 2e-3
        print(f"{P:<6} {b0:.4f}    {bs:.4f}     {c0:.4f}    {cs:.4f}     "
              f"{g0:.5f}   {gY:.5f}")
        rows.append(dict(P=P, b=round(b0, 6), c=round(c0, 6), G=round(g0, 6)))
    # Book spot checks (p. 141-144)
    b, c, g = closed(2.0)
    assert abs(b - 1 / 3) < 1e-12 and abs(c - 1 / 3) < 1e-12
    assert abs(g - 1 / 18) < 1e-12
    assert abs(closed(1.5)[0] - 2 / 5) < 1e-12
    # p. 144 prints the bluff ratio at P=1.1 as "10/11"; 1/(P+1) = 10/21.
    assert abs(closed(1.1)[0] - 10 / 21) < 1e-12
    print("\nGame #1 (P=2): b=1/3, c=1/3, G(Y)=1/18  -- book reproduced")
    print("P->inf limit: G ->", (1e9 - 1) / (6 * (1e9 + 1)), "(-> 1/6)")
    print("ALL CHECKS PASS" if ok else "*** CHECK FAILURE ***")
    json.dump(rows, open("akq_limit.json", "w"), indent=1)


if __name__ == "__main__":
    main()
