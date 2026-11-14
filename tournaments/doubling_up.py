"""Module 1 - The Theory of Doubling Up  (Chen & Ankenman ch. 26; rebuy from ch. 28).

The whole chapter is closed-form.  The one governing relation is

    E = C**N          (26.1)     N = log2(X)          (doubles to win)
    E = S**beta       (26.2)     beta = -log2(C)      (S = fraction of chips)

where
    E  = a player's probability of winning a winner-take-all (WTA) tournament,
    C  = his (assumed constant) chance of doubling his stack before busting,
    N  = the number of doubles needed to go from his stack to all the chips,
    X  = field size,
    S  = his stack as a fraction of all chips in play.

Everything below is arithmetic on those two equations.  `python3 doubling_up.py`
reproduces every worked number in the chapter and writes doubling_up.json for the
explorer.  `--mc` runs a small Monte-Carlo check that E = C**N.
"""
from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass


# --------------------------------------------------------------------------- #
# Core relations
# --------------------------------------------------------------------------- #
def doubles_needed(total_chips: float, stack: float) -> float:
    """N = log2(total / stack): how many doubles from `stack` to all the chips."""
    return math.log2(total_chips / stack)


def C_from_equity(equity: float, doubles: float) -> float:
    """Invert E = C**N for C given a known equity and N.  C = E**(1/N)."""
    return equity ** (1.0 / doubles)


def winprob(C: float, doubles: float) -> float:
    """E = C**N: probability of winning a WTA tournament needing `doubles` doubles."""
    return C ** doubles


def equity_at_stack(C: float, total_chips: float, stack: float) -> float:
    """Win probability from an arbitrary stack: E = C**log2(total/stack)."""
    return winprob(C, doubles_needed(total_chips, stack))


def beta(C: float) -> float:
    """beta = -log2(C), so that E = S**beta with S the chip fraction (26.2)."""
    return -math.log2(C)


# --------------------------------------------------------------------------- #
# Effective tournament size k  (structured payouts, 26.3 and the N-D form)
# --------------------------------------------------------------------------- #
def effective_size(field: int, payouts_buyins: list[float]) -> dict:
    """Effective (winner-take-all) field size k for a structured payout.

    Uses the book's simplified form.  With w_i = v_i - v_{i+1} (w_last = v_last)
    the incremental prize for finishing i-th instead of (i+1)-th, and
    P = sum_i i*w_i = total prize pool, the "missing doubles" are

        N - D = sum_i (i * w_i * log2 i) / P            k = field / 2**(N-D)

    `payouts_buyins` is [v1, v2, ...] denominated in buy-ins.
    """
    v = list(payouts_buyins)
    w = [v[i] - (v[i + 1] if i + 1 < len(v) else 0.0) for i in range(len(v))]
    P = sum((i + 1) * w[i] for i in range(len(w)))          # 1-indexed place
    num = sum((i + 1) * w[i] * math.log2(i + 1) for i in range(len(w)))
    n_minus_d = num / P
    k = field / (2.0 ** n_minus_d)
    return {"pool": P, "N_minus_D": n_minus_d, "k": k}


# --------------------------------------------------------------------------- #
# Rebuy / add-on indifference  (ch. 28, evaluated on the doubling-up engine)
# --------------------------------------------------------------------------- #
def addon_value(C: float, total_chips: float, pool: float, stack: float,
                addon_chips: float) -> float:
    """Cash value of buying `addon_chips` more, at a given stack (dollars)."""
    e0 = equity_at_stack(C, total_chips, stack)
    e1 = equity_at_stack(C, total_chips, stack + addon_chips)
    return pool * (e1 - e0)


def addon_breakeven_stack(C: float, total_chips: float, pool: float,
                          addon_chips: float, cost: float) -> float | None:
    """Largest stack at which the add-on/rebuy is still worth its `cost`.

    value(stack) = pool*(E(stack+addon) - E(stack)) is decreasing in stack;
    return the stack where it crosses `cost` (or None if it never does).
    """
    lo, hi = 1.0, total_chips / 2.0            # search up to half the chips
    if addon_value(C, total_chips, pool, lo, addon_chips) < cost:
        return None                            # never worth it, even short
    if addon_value(C, total_chips, pool, hi, addon_chips) >= cost:
        return hi                              # still worth it at half the chips
    for _ in range(200):                       # bisection
        mid = 0.5 * (lo + hi)
        if addon_value(C, total_chips, pool, mid, addon_chips) >= cost:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# --------------------------------------------------------------------------- #
# Reproduce the chapter's worked numbers
# --------------------------------------------------------------------------- #
@dataclass
class Check:
    name: str
    got: float
    want: float
    tol: float

    @property
    def ok(self) -> bool:
        return abs(self.got - self.want) <= self.tol


def reproductions() -> list[Check]:
    ck: list[Check] = []

    # -- Equal-skill WTA forces C = 0.5 (chips exactly linear) ---------------
    #    1/X = C**log2(X)  =>  C = 0.5 for any X.
    ck.append(Check("equal-skill C", C_from_equity(1 / 128, doubles_needed(128, 1)),
                    0.5, 1e-12))

    # -- 100-player example: 2 buy-ins gross => win prob 0.02 ----------------
    C100 = C_from_equity(2 / 100, doubles_needed(100, 1))
    ck.append(Check("100p: C", C100, 0.5550, 5e-4))
    ck.append(Check("100p: E(stack=2)", equity_at_stack(C100, 100, 2), 0.0360, 5e-4))

    # -- NLHE fold decision: 250 players, 3/4-buyin edge ---------------------
    #    Starting stack 1500; gross equity 1.75 buy-ins => E(1 stack)=1.75/250.
    Cb = C_from_equity(1.75 / 250, doubles_needed(250, 1))
    ck.append(Check("NLHE: C", Cb, 0.5364, 5e-4))
    e_call_win = equity_at_stack(Cb, 250 * 1500, 6075)     # 6075 chips
    e_fold = equity_at_stack(Cb, 250 * 1500, 2050)         # 2050 chips
    ck.append(Check("NLHE: E(call&win)", e_call_win, 0.024603, 5e-5))
    ck.append(Check("NLHE: E(fold)", e_fold, 0.009269, 5e-5))
    ck.append(Check("NLHE: EV(call)", 0.36 * e_call_win, 0.008857, 5e-5))
    # calling (0.008857) < folding (0.009269) although chip-EV says call (+137).

    # -- Coinflip indifference W = C, and "decline QQvAK => you think you win"-
    #    Declining a 57-43 flip implies C = 0.57; the book's E = 0.57**8 = 0.01114
    #    (which is 2.785 buy-ins; its prose rounds this loosely to "about 2.85").
    ck.append(Check("decline 57-43: E", 0.57 ** 8, 0.01114, 5e-5))

    # -- Third man in: needs C**2 (=30.25% at C=0.55) vs 25% chipwise ---------
    ck.append(Check("third-man-in req eq", 0.55 ** 2, 0.3025, 1e-9))

    # -- Effective tournament size k (154/102 match-play split) --------------
    eff = effective_size(256, [154.0, 102.0])
    ck.append(Check("effective size k", eff["k"], 147.35, 0.1))

    # -- Rebuy Case 2: 6000 chips, 1M total, C=0.54, $90k pool ---------------
    e6000 = equity_at_stack(0.54, 1_000_000, 6000)
    e7500 = equity_at_stack(0.54, 1_000_000, 7500)
    ck.append(Check("rebuy: E(6000)*pool", 90_000 * e6000, 953, 6))
    ck.append(Check("rebuy: E(7500)*pool", 90_000 * e7500, 1162, 6))
    # at-par add-on (1500 chips for $150) breakeven near stack 8325 at C=0.51
    be = addon_breakeven_stack(0.51, 1_000_000, 90_000, 1500, 150)
    ck.append(Check("rebuy: par breakeven stack", be, 8325, 60))

    return ck


# --------------------------------------------------------------------------- #
# Small Monte-Carlo validation that E = C**N (a clean doubling bracket)
# --------------------------------------------------------------------------- #
def monte_carlo_check(C: float, doubles: int, trials: int = 400_000,
                      seed: int = 12345) -> dict:
    """In a bracket, the skilled player must win `doubles` independent doubles,
    each with probability C.  Empirical P(win) should match C**doubles."""
    import random
    rng = random.Random(seed)
    wins = 0
    for _ in range(trials):
        for _ in range(doubles):
            if rng.random() >= C:
                break
        else:
            wins += 1
    emp = wins / trials
    theory = C ** doubles
    se = math.sqrt(theory * (1 - theory) / trials)
    return {"C": C, "doubles": doubles, "empirical": emp, "theory": theory,
            "abs_err": abs(emp - theory), "std_err": se}


# --------------------------------------------------------------------------- #
# Data for the explorer
# --------------------------------------------------------------------------- #
def build_artifact_data() -> dict:
    # Family of chip-value curves E = S**beta for a sweep of skill C.
    S = [i / 200 for i in range(1, 201)]                # chip fraction 0.005..1
    skills = [0.44, 0.47, 0.50, 0.53, 0.56]
    curves = []
    for C in skills:
        b = beta(C)
        curves.append({"C": C, "beta": b, "E": [round(s ** b, 6) for s in S]})

    # Rebuy: add-on value vs current stack, for a few skill levels (Case 2 setup).
    stacks = [1000 * i for i in range(1, 251)]          # up to 250k (=quarter)
    rebuy = []
    for C in (0.51, 0.54, 0.57):
        disc = [round(addon_value(C, 1_000_000, 90_000, s, 1500), 2) for s in stacks]
        rebuy.append({"C": C, "stack": stacks, "addon_value": disc})

    return {
        "chip_value_curves": {"S": S, "curves": curves},
        "rebuy": {"note": "Case 2: 1M chips, $90k pool, add-on = 1500 chips",
                  "series": rebuy,
                  "discount_cost": 100, "par_cost": 150},
        "effective_size_example": effective_size(256, [154.0, 102.0]),
    }


def main() -> None:
    checks = reproductions()
    width = max(len(c.name) for c in checks)
    print("Reproducing Chen ch. 26 / 28 (Theory of Doubling Up):\n")
    for c in checks:
        flag = "ok " if c.ok else "XX "
        print(f"  [{flag}] {c.name:<{width}}  got {c.got:.6g}   want {c.want:.6g}")
    n_ok = sum(c.ok for c in checks)
    print(f"\n  {n_ok}/{len(checks)} checks pass.")

    if "--mc" in sys.argv:
        print("\nMonte-Carlo check of E = C**N:")
        for C, d in ((0.50, 7), (0.5364, 8), (0.56, 6)):
            r = monte_carlo_check(C, d)
            print(f"  C={r['C']:.4f} N={r['doubles']}: "
                  f"empirical {r['empirical']:.5f}  theory {r['theory']:.5f}  "
                  f"(|err| {r['abs_err']:.5f}, se {r['std_err']:.5f})")

    with open("doubling_up.json", "w") as f:
        json.dump(build_artifact_data(), f)
    print("\nWrote doubling_up.json")

    if not all(c.ok for c in checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
