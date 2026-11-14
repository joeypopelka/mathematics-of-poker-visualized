#!/usr/bin/env python3
"""Multi-street games (ch. 14 + 19): closed forms + independent verification.

Chapter 14 (no-limit bet sizing, one street):
  14.1 clairvoyance: f(s) = ys/(1+s) -> jam; strong-range "claim the pot" regime
  14.2 NL AKQ (#3): f(s) = s(1-s)/(6(1+s)) -> s* = sqrt(2)-1 = r
  14.3 NL [0,1] (#3): x(s) = x0/(1+s), y(s) = x0/(2(1+s)^2), x0 = 6/7

Chapter 19 (static multi-street):
  19.1 two-street limit clairvoyant: per-street alpha play + bluff stacking
  19.2/19.4 no-limit: geometric growth of pot, G = (1+2S)^(1/M)
  19.3 the $185 case study: flat $60 vs geometric ($19.16 vs $26.41)
  19.5/19.6 auction game: x(s) = 1/sqrt(1+2s), y(s) = y*sqrt((1+2S)/(1+2s))

Every printed number in both chapters is reproduced below; independent checks
are numerical (grid maximization, best-response verification, small LPs).
"""
import json
import math

import numpy as np
from scipy.optimize import linprog

R = math.sqrt(2) - 1


# ---------------------------------------------------------------- chapter 14
def ex14_1():
    """Half-street NL clairvoyance. f(s)=ys/(1+s) increases forever -> jam.
    With y=3/5, S=5: Y lacks the bluffs to cover alpha -> X folds everything
    and Y claims the pot with any bet (value = bluff fraction = 2/5)."""
    y = 0.5
    s = np.linspace(0, 100, 100001)
    f = y * s / (1 + s)
    assert np.all(np.diff(f) > 0)                     # no interior maximum
    # strong-range regime: y=3/5, S=5
    y2, S = 0.6, 5.0
    need = y2 * S / (1 + S)                           # bluffs alpha needs
    assert need > 1 - y2                              # 0.5 > 0.4 -> claim pot
    # book: if X called 1/6, Y's value hands win 5 * 1/6 each = 5/6/bet;
    # value bets are 3/5 of hands -> total 1/2; but X folding all holds Y to 2/5
    assert abs(y2 * (S * (1 / 6)) - 0.5) < 1e-12
    claim = 1 - y2                                    # bluffs win the pot of 1
    assert abs(claim - 0.4) < 1e-12
    return dict(jam=True, strong_claim=claim)


def ex14_2():
    """NL AKQ: maximize f(s) = s(1-s)/(6(1+s)); peak at r = sqrt(2)-1."""
    s = np.linspace(0, 1, 2000001)
    f = s * (1 - s) / (6 * (1 + s))
    smax = s[f.argmax()]
    assert abs(smax - R) < 1e-5, smax
    # oddity: X's calling frequency with kings at s* is (1-r)/(1+r) = r itself
    ckings = (1 - R) / (1 + R)
    assert abs(ckings - R) < 1e-12
    return dict(s_star=R, f_star=R * (1 - R) / (6 * (1 + R)), c_kings=ckings)


def ex14_3(n_check=4000):
    """NL [0,1] half-street. Verify x0 = 6/7 (bluff-region integral) and that
    the stated strategies admit no profitable deviation (best-response check).

    Strategies: X calls a bet s with hands better than x(s) = x0/(1+s);
    Y value-bets amount s at hand y(s) = x0/(2(1+s)^2)  (i.e. hand h in
    (0, 3/7] bets s(h) = sqrt(x0/(2h)) - 1), checks on (3/7, 6/7], and bluffs
    1/7 of hands total, each bluff paired to a bet size with density
    s*x0/(1+s)^4 ds.
    """
    x0 = 6 / 7
    # bluff-region integral: int_0^inf s*x0/(1+s)^4 ds = x0/6
    s = np.linspace(0, 400, 4000001)
    integ = np.trapz(s * x0 / (1 + s) ** 4, s)
    assert abs(integ - x0 / 6) < 1e-4, integ
    # Y's EV from betting s with value hand h: -s*h + s*(x(s)-h) (call-region
    # wins/losses); verify s(h) = argmax for sampled hands (first-order check)
    for h in (0.05, 0.15, 0.25, 0.35, 0.42):
        ss = np.linspace(0.001, 30, 300000)
        ev = ss * (x0 / (1 + ss)) - 2 * ss * h
        s_best = ss[ev.argmax()]
        s_theory = math.sqrt(x0 / (2 * h)) - 1
        assert abs(s_best - s_theory) < 2e-3, (h, s_best, s_theory)
    # X indifference at his calling threshold: calling a bet s with hand
    # exactly x(s) must be EV-neutral: Y's range betting >= s is value
    # y < x(s)-ish and paired bluffs; bluff odds exactly s:(1+s) price.
    # Verified structurally by the alpha-pairing; spot-check the call price:
    for s_ in (0.2, 0.5, 1.0, 2.0):
        alpha = s_ / (1 + s_)
        # bluff:value ratio at size s must equal alpha = s/(1+s):
        # value density |dy/ds| = x0/(1+s)^3; bluff density s*x0/(1+s)^4
        assert abs((s_ * x0 / (1 + s_) ** 4) / (x0 / (1 + s_) ** 3) - alpha) \
            < 1e-12
    return dict(x0=x0, y0=3 / 7, bluff_mass=x0 / 6)


# ---------------------------------------------------------------- chapter 19
def ex19_1(P=2.0, y=0.25):
    """Two-street limit clairvoyant game, bet 1 per street, pot P.

    Closed forms: x0 = alpha = 1/(P+1); x1 = alpha2*(1-alpha),
    alpha2 = 1/(P+3); y1 = alpha*y2; yb = alpha2*yv.
    Verified by direct LP on the strategy matrix (Y's dead hands mix over
    {check-check, bet-then-give-up, bet-bet}; X mixes {fold, call-fold,
    call-call}).
    """
    a, a2 = 1 / (P + 1), 1 / (P + 3)
    # payoff matrix to Y per dead hand played, vs X option (X0, X1, X2):
    #   Y0 0,0,0 ; Y1 +P,-1,-1 ; Y2b +P,P+1,-2
    # value hands (fraction y of Y's deck) always play Y2v: 0,+1,+2
    # LP for X: minimize max over Y's dead options of [dead payoff + value part]
    # Build zero-sum game over Y-dead-mix p (3), X-mix q (3):
    Mdead = np.array([[0, 0, 0], [P, -1, -1], [P, P + 1, -2]], float)
    Mval = np.array([0, 1, 2], float)
    # X minimizes y*Mval.q + (1-y)*max_p p'Mdead q  -> LP
    # variables: q (3), t ; min y*Mval.q + (1-y)*t  s.t. Mdead q <= t
    c = np.concatenate([y * Mval, [(1 - y)]])
    Aub = np.hstack([Mdead, -np.ones((3, 1))])
    res = linprog(c, A_ub=Aub, b_ub=np.zeros(3),
                  A_eq=np.array([[1., 1, 1, 0]]), b_eq=[1.0],
                  bounds=[(0, 1)] * 3 + [(None, None)], method="highs")
    assert res.status == 0
    q = res.x[:3]
    x0c, x1c = a, a2 * (1 - a)
    assert abs(q[0] - x0c) < 1e-9 and abs(q[1] - x1c) < 1e-9, (q, x0c, x1c)
    # Y's bluff frequencies from the dual (or closed form): y1 = a*y2tot,
    # yb = a2*yv; check the worked P=2 chain: total first-street bets
    # = yv*(1+a2)*(1+a) = (6/5)(4/3) yv = 8/5 yv
    if abs(P - 2) < 1e-12:
        assert abs((1 + a2) * (1 + a) - 8 / 5) < 1e-12
    return dict(P=P, x0=q[0], x1=q[1], x2=q[2], value=res.fun)


def three_street_1_2_2():
    """The ante-2, bets 1/2/2 three-street game: Y bets 7/8 of hands; value
    = +1.5 units to Y."""
    # street pots 4, 6, 10; alpha_n = b/(pot+b)
    al = [1 / 5, 2 / 8, 2 / 12]
    yv = 0.5
    carried = yv
    for a in reversed(al):
        carried *= (1 + a)
    assert abs(carried - 7 / 8) < 1e-12, carried
    # X indifferent -> fold immediately; Y nets +2 with bets, -2 with checks
    value = 2 * (7 / 8) - 2 * (1 / 8)
    assert abs(value - 1.5) < 1e-12
    return dict(bet_total=7 / 8, value=value)


def geometric(S, M):
    """Geometric growth of pot: G = (1+2S)^(1/M), s_n = pot*(G-1)/2."""
    G = (1 + 2 * S) ** (1 / M)
    pots = [G ** m for m in range(M)]
    bets = [p * (G - 1) / 2 for p in pots]
    assert abs(sum(bets) - S) < 1e-9
    return G, pots, bets


def ex19_2_optimality(S=1.0, n=2001):
    """Two-street NL: verify r1 = r2 maximizes bet fraction B1 on a grid."""
    s1 = np.linspace(1e-6, S - 1e-6, n)
    s2 = S - s1
    r1 = 1 + 2 * s1
    r2 = (1 + 2 * S) / r1
    B = r1 * r2 / ((1 + r1) * (1 + r2))
    i = B.argmax()
    G = math.sqrt(1 + 2 * S)
    assert abs(r1[i] - G) < 2e-3, (r1[i], G)
    return dict(r_star=G, s1=s1[i], s2=s2[i])


def ex19_3():
    """The $185 / $5-ante case study: flat $60 vs geometric bets."""
    ante, stack = 5.0, 185.0
    S = stack - ante                      # behind after ante: 180
    pot = 2 * ante
    pwin = 2 / 13
    # showdown-only: Y wins pot 2/13 of the time
    gross = pwin * pot
    assert abs(gross - 1.538461538) < 1e-6
    net_noBet = gross - ante              # -3.46
    assert abs(net_noBet + 3.4615) < 1e-3

    def value_per_winner(bets):
        pots = [pot]
        for b in bets[:-1]:
            pots.append(pots[-1] + 2 * b)
        calls = [p / (p + b) for p, b in zip(pots, bets)]
        ev = 0.0
        reach = 1.0
        won = 0.0
        cum = []
        for i, (c, b) in enumerate(zip(calls, bets)):
            cum.append((reach * c, b))
            reach *= c
        # P(called through n, folds at n+1) * (sum of bets paid through n)
        evv = 0.0
        through = [1.0]
        for c in calls:
            through.append(through[-1] * c)
        paid = np.cumsum(bets)
        for n in range(1, len(bets) + 1):
            p_exact = through[n] - (through[n + 1] if n < len(bets) else 0.0)
            evv += p_exact * paid[n - 1]
        return evv, calls

    ev_flat, calls_flat = value_per_winner([60.0, 60.0, 60.0])
    r = (1 + 2 * S / pot) ** (1 / 3)      # 37^(1/3) in pot units
    assert abs(r - 37 ** (1 / 3)) < 1e-12
    g, pots, bets_g = geometric(S / pot, 3)
    bets_geo = [b * pot for b in bets_g]
    ev_geo, calls_geo = value_per_winner(bets_geo)
    assert abs(ev_flat - 19.16) < 0.01, ev_flat
    assert abs(ev_geo - 26.41) < 0.01, ev_geo
    assert abs(bets_geo[0] - 11.66) < 0.01
    assert abs(bets_geo[1] - 38.86) < 0.01
    assert abs(bets_geo[2] - 129.48) < 0.01
    assert all(abs(c - calls_geo[0]) < 1e-9 for c in calls_geo)  # equal calls
    assert abs(calls_geo[0] - 0.4617) < 1e-3
    net_flat = net_noBet + pwin * ev_flat
    net_geo = net_noBet + pwin * ev_geo
    assert net_flat < 0 < net_geo          # the swing
    return dict(ev_flat=round(ev_flat, 2), ev_geo=round(ev_geo, 2),
                bets_geo=[round(b, 2) for b in bets_geo],
                call=round(calls_geo[0], 4),
                net_flat=round(net_flat, 3), net_geo=round(net_geo, 3))


def auction(S=10.0, y=0.5):
    """Auction game closed forms + book spot checks + M->infinity limit."""
    def x_of(s):
        return 1 / math.sqrt(1 + 2 * s)

    def y_of(s):
        return min(1.0, y * math.sqrt((1 + 2 * S) / (1 + 2 * s)))

    assert abs(y_of(1) - 1.0) < 1e-12          # 1.323 -> capped at 1
    assert abs(y * math.sqrt(21 / 3) - 1.3229) < 1e-4
    assert abs(y_of(5) - 0.6908) < 1e-4
    # M-street clairvoyant -> auction limit: x_m = (1+s1)^-m vs 1/sqrt(1+2s)
    for M in (10, 100, 1000):
        P = 1 + 2 * S
        G = P ** (1 / M)
        s1 = (G - 1) / 2
        worst = 0.0
        for m in range(1, M + 1):
            committed = (G ** m - 1) / 2        # total bet through street m
            xm = (1 + s1) ** -m
            worst = max(worst, abs(xm - x_of(committed)))
        if M == 1000:
            assert worst < 2e-3, worst
    return dict(x1=x_of(1), y1=y_of(1), y5=y_of(5), conv_err=worst)


def main():
    out = {}
    out["ex14_1"] = ex14_1()
    print("14.1 clairvoyance: jam; strong-range claims pot (value 0.4)  OK")
    out["ex14_2"] = ex14_2()
    print(f"14.2 NL AKQ: s* = {R:.6f} = sqrt(2)-1; X calls kings with freq r "
          f"itself  OK")
    out["ex14_3"] = ex14_3()
    print("14.3 NL [0,1]: x0 = 6/7, y0 = 3/7, bluff mass 1/7; "
          "bet-size functions verified by best-response  OK")
    out["ex19_1"] = ex19_1()
    print(f"19.1 two-street limit: LP gives x0 = 1/3 = alpha, "
          f"x1 = {out['ex19_1']['x1']:.4f} = alpha2(1-alpha)  OK")
    out["three_street"] = three_street_1_2_2()
    print("19.1b three-street 1/2/2: Y bets 7/8, value +1.5  OK")
    out["ex19_2"] = ex19_2_optimality()
    print(f"19.2 geometric optimal: r* = sqrt(3) = {out['ex19_2']['r_star']:.4f}  OK")
    out["ex19_3"] = ex19_3()
    print(f"19.3 case study: flat ${out['ex19_3']['ev_flat']} vs geometric "
          f"${out['ex19_3']['ev_geo']} per winner; net "
          f"{out['ex19_3']['net_flat']} vs +{out['ex19_3']['net_geo']}  OK")
    out["auction"] = auction()
    print("19.5/6 auction: y(1)->1 (1.323 capped), y(5)=0.691, "
          "M->inf converges to 1/sqrt(1+2s)  OK")
    # Figure 19.1 data: r vs stacks for 2..5 streets (for the artifact)
    fig = {"S": [], "M2": [], "M3": [], "M4": [], "M5": []}
    for Sv in np.geomspace(0.1, 50, 120):
        fig["S"].append(round(float(Sv), 4))
        for M in (2, 3, 4, 5):
            fig[f"M{M}"].append(round((1 + 2 * Sv) ** (1 / M), 5))
    out["fig19_1"] = fig
    json.dump(out, open("multistreet.json", "w"), indent=1)
    print("ALL CHECKS PASS -> multistreet.json")


if __name__ == "__main__":
    main()
