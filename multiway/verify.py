#!/usr/bin/env python3
"""Multiplayer games (ch. 29) — the chapter's worked numbers, verified.

Light treatment by design: the chapter's own point is that multiplayer games
have no 'solution', only equilibria that can be disturbed into alliances.
"""
import math


def ex29_1():
    """The rock & the maniac: a symmetric fair game we cannot win.

    3 players ante $10; one card each from a 52-card deck; aces and kings
    (8 cards) win. Rock (left): check, call only with winner. Maniac (right):
    bet $30 always, call always. Us (middle): best response.
    """
    W, D = 8, 52
    # with a losing card: call EV
    p_no_winner = (D - 1 - W) / (D - 1) * (D - 2 - W) / (D - 2)
    assert abs(p_no_winner - 0.708) < 1e-3
    ev_call = p_no_winner * 45 - 30
    assert abs(ev_call - 1.87) < 0.01                  # call beats fold
    # full-game EV table (calling with losers, book's six rows)
    p_w = W / D
    rows = []
    # we hold a winner (7 winners left in 51)
    p_bothw = p_w * (7 / 51) * (6 / 50)
    p_rw_ml = p_w * (7 / 51) * (44 / 50)
    p_rl_mw = p_w * (44 / 51) * (7 / 50)
    p_bothl = p_w * (44 / 51) * (43 / 50)
    rows += [(p_bothw, 0), (p_rw_ml, 20), (p_rl_mw, 5), (p_bothl, 50)]
    # we hold a loser
    p_l = 1 - p_w
    p_l_bothl = p_l * (43 / 51) * (42 / 50)
    p_l_anyw = p_l - p_l_bothl
    rows += [(p_l_bothl, 5), (p_l_anyw, -40)]
    assert abs(sum(p for p, _ in rows) - 1) < 1e-12
    ev = sum(p * v for p, v in rows)
    assert abs(ev - (-0.707)) < 0.005, ev              # book: -$0.707
    return dict(ev_call=ev_call, game_ev=ev,
                probs=[round(p, 4) for p, _ in rows])


def ex29_3():
    """Dry side pot [0,1] game (pot 9, Z all-in): Nash thresholds.

    The book's own system (its Example 29.2 of the second kind):
        y1 = x/2                      (Y's value indifference)
        w  = y1/(10-9x) = x/(20-18x)  (X's call indifference at x)
        w  = sqrt((1+x)^2 - 40x/9)    (width between the two roots of Y's
                                       bluff indifference quadratic)
    The book reports x ~ 0.2848, y1 ~ 0.1424, band 0.6424 +/- 0.0095. But
    x = 0.2848 does not satisfy the system: the two w-expressions give
    0.019 vs 0.620 there. The true simultaneous root is x ~ 0.518 — and the
    no-deviation check below confirms it IS the equilibrium while the book's
    numbers are not (at x=0.2848, Y strictly gains by bluffing hand 0.5).
    """
    def f(x):
        d = (1 + x) ** 2 - 40 * x / 9
        return x / (20 - 18 * x) - (math.sqrt(d) if d > 0 else -1.0)
    # root lies just below the tangency point (disc = 0 at x ~ 0.5195)
    lo, hi = 0.4, 0.5195
    for _ in range(300):
        m = (lo + hi) / 2
        if f(m) < 0:
            lo = m
        else:
            hi = m
    x = (lo + hi) / 2
    y1 = x / 2
    w = x / (20 - 18 * x)
    center = (1 + x) / 2
    a, b = center - w / 2, center + w / 2

    # --- no-deviation (Nash) check on a fine grid ---
    def check(xthr, yv, blo, bhi, require=True):
        """True iff no profitable deviation for either player (grid)."""
        wb = bhi - blo
        ok = True
        n = 2000
        for i in range(n):                      # Y's hands
            y = (i + 0.5) / n
            ev_value = xthr - 2 * y             # bet-for-value minus check
            ev_bluff = -xthr + 9 * max(0.0, (y - xthr)) * (1 - y) \
                if y > xthr else -xthr + 9 * (y - xthr) * (1 - y)
            best = max(0.0, ev_value, ev_bluff)
            if y <= yv:
                take = ev_value
            elif blo <= y <= bhi:
                take = ev_bluff
            else:
                take = 0.0
            if take < best - 1e-3:
                ok = False
                break
        for i in range(n):                      # X's hands
            t = (i + 0.5) / n
            ev_call = -yv + wb * (10 - 9 * t)
            take = ev_call if t <= xthr else 0.0
            if take < max(0.0, ev_call) - 1e-3:
                ok = False
                break
        return ok

    assert check(x, y1, a, b), "corrected solution fails Nash check"
    # the book's printed solution admits profitable deviations:
    bx, by1, bw = 0.2848, 0.1424, 0.0190
    assert not check(bx, by1, 0.6424 - bw / 2, 0.6424 + bw / 2), \
        "book solution unexpectedly passes"
    # e.g. Y bluffing hand 0.5 against x=0.2848 nets:
    gain = -bx + 9 * (0.5 - bx) * 0.5
    assert gain > 0.68                          # strictly profitable
    return dict(x=x, y1=y1, w=w, center=center, band=(a, b),
                book=(bx, by1, bw), book_bluff_gain_at_half=gain)


def ex29_4():
    """Clairvoyant maniac, pot 9: Z's EV per value bet as his announced
    bluff ratio beta varies, with X and Y playing equity-maximizing
    responses. Discontinuous — and overbluffing 3x wins."""
    alpha = 1 / 10

    def z_ev(beta):
        if beta <= alpha:                 # equilibrium: called 9/10 total
            return 9 / 10
        if beta <= 1 / 5:                 # X calls always, Y can't overcall
            return 1 - beta
        return 2 - beta                   # Y overcalls too

    assert abs(z_ev(0.10) - 0.9) < 1e-12
    assert z_ev(1 / 8) < 0.9              # "actually bad for Z"
    assert abs(z_ev(0.30) - 1.7) < 1e-12  # 17/10 per value bet
    return dict(eq=9 / 10, over_18=z_ev(1 / 8), over_3x=z_ev(0.3))


if __name__ == "__main__":
    r1 = ex29_1()
    print(f"29.1 rock & maniac: call EV +$1.87 OK; game EV = "
          f"${r1['game_ev']:.3f} (book -$0.707) — unbeatable  OK")
    r3 = ex29_3()
    print(f"29.3 dry side pot: TRUE equilibrium x={r3['x']:.4f}, "
          f"y1={r3['y1']:.4f}, bluff band {r3['center']:.4f}±{r3['w']/2:.4f} "
          f"(Nash-checked); book's x=0.2848 fails its own system AND the "
          f"deviation check (bluffing 0.5 nets +{r3['book_bluff_gain_at_half']:.2f})")
    r4 = ex29_4()
    print(f"29.4 clairvoyant maniac: eq 0.9; 1/8-bluff {r4['over_18']:.3f} "
          f"(worse); 3x-bluff {r4['over_3x']:.1f} (17/10)  OK")
    print("ALL CHECKS PASS")
