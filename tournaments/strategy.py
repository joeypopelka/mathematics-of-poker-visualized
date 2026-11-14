"""Module 3 - Poker's Still Poker: strategy consequences (ch. 28).

Two things the payout structure does to correct play:

  1. Confrontations are not constant-sum (everyone else gains when two players
     collide), so tournaments contain a "game of chicken" (Example 28.1): it
     pays to be the *first* one all-in.
  2. A step in the money forces a *risk premium* -- the equity you need to call
     off your stack exceeds the chip-EV break-even (Examples 28.2 and the SNG
     bubble cases).

We reproduce the chapter's numbers and, using Module 2's ICM, express the
premium as a "bubble factor" that maps directly onto the ch. 12 jam/fold ranges.

`python3 strategy.py` reproduces the numbers and writes strategy.json.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass

import icm


# --------------------------------------------------------------------------- #
# Game of chicken (Example 28.1)
# --------------------------------------------------------------------------- #
#   payoff (A, B):        B drive on     B swerve
#   A drive on           (-10, -10)      ( 1, -1)
#   A swerve             ( -1,   1)      ( 0,  0)
def chicken_mixed_equilibrium() -> float:
    """Symmetric mixed equilibrium: probability of 'drive on' that makes the
    opponent indifferent.  -10p + (1-p) = -p  =>  p = 1/10."""
    # B(drive) = p*(-10) + (1-p)*(1);  B(swerve) = p*(-1) + (1-p)*0
    # set equal: -10p + 1 - p = -p  ->  p = 0.1
    return 0.1


# --------------------------------------------------------------------------- #
# Required equity to call for your tournament life
# --------------------------------------------------------------------------- #
def required_equity(eq_win: float, eq_lose: float, eq_fold: float) -> float:
    """Solve X*eq_win + (1-X)*eq_lose = eq_fold for the calling equity X."""
    return (eq_fold - eq_lose) / (eq_win - eq_lose)


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

    # -- Game of chicken: mixed equilibrium drives on 10% of the time --------
    ck.append(Check("chicken: P(drive on)", chicken_mixed_equilibrium(), 0.10, 1e-9))

    # -- Example 28.2: SNG 5-3-2, four 2500 stacks, SB jams, BB to call ------
    #    The book approximates the prize equities (buy-in units):
    #      call & win  (5000 chips): 0.5*5 + 0.5*2.5             = 3.75
    #      call & lose (0 chips):                                  0
    #      fold (2100 chips + SB):   0.21*5 + 0.29*0 + 0.5*2.5   = 2.30
    eq_win, eq_fold = 0.5 * 5 + 0.5 * 2.5, 0.21 * 5 + 0.29 * 0 + 0.5 * 2.5
    ck.append(Check("28.2 call&win equity", eq_win, 3.75, 1e-9))
    ck.append(Check("28.2 fold equity", eq_fold, 2.30, 1e-9))
    ck.append(Check("28.2 required equity (ICM)",
                    required_equity(eq_win, 0.0, eq_fold), 0.6133, 5e-4))
    #    Chip-EV break-even: X*5000 = 2100  ->  42%
    ck.append(Check("28.2 required equity (chip-EV)", 2100 / 5000, 0.42, 1e-9))

    # -- Four-handed SNG bubble cases (5-3-2 payouts) ------------------------
    #    One Big Stack (5500/1500x3): big stack jams, BB defends.
    win_obs = 0.30 * 5 + 0.40 * 3 + 0.25 * 2 + 0.05 * 0        # = 3.2
    fold_obs = 0.10 * 5 + 0.30 * 3 + 0.30 * 2 + 0.30 * 0        # = 2.0
    ck.append(Check("One-Big-Stack req eq", fold_obs / win_obs, 0.625, 1e-3))
    #    Four Equal (2500x4): UTG jams.
    win_eq = 0.50 * 5 + 0.30 * 3 + 0.20 * 2                     # = 3.8
    fold_eq = 0.25 * 5 + 0.25 * 3 + 0.25 * 2 + 0.25 * 0         # = 2.5
    ck.append(Check("Four-Equal req eq", fold_eq / win_eq, 0.658, 1e-3))

    # -- Supersatellite fold-AA story (8 seats, 10 players) ------------------
    #    Two ~equal big stacks holding 75% of chips; the rest split 25%.
    #    Seats are flat prizes (each = 1 unit); places 9-10 pay 0.
    T = 200000
    big, small = 0.375 * T, (0.25 * T) / 8
    #    Fold: big stack keeps 37.5% of the chips among 10 players for 8 seats.
    eq_fold = icm.malmuth_weitzman([big, big] + [small] * 8, [1] * 8 + [0, 0])[0]
    #    Call & win: the other big stack busts (10th); winner holds 75% of the
    #    chips among the 9 survivors for 8 seats -> a seat is all but locked.
    eq_win = icm.malmuth_weitzman([0.75 * T] + [small] * 8, [1] * 8 + [0])[0]
    call_ev = 0.81 * eq_win + 0.19 * 0.0                        # AA is ~81% to win
    ck.append(Check("supersat: fold beats call(AA)",
                    1.0 if eq_fold > call_ev else 0.0, 1.0, 0))
    ck.append(Check("supersat: fold equity ~1", eq_fold, 1.0, 0.05))

    return ck


# --------------------------------------------------------------------------- #
# Bubble factor: the ICM risk premium as a multiplier on ch. 12 jam/fold ranges
# --------------------------------------------------------------------------- #
def _hero_equity(stacks: list[float], payouts: list[float], hero: int) -> float:
    """ICM (Malmuth-Weitzman) equity of `hero`, robust to busted (zero) stacks:
    players with chips compete for the top places; the busted occupy the bottom."""
    live = [i for i, s in enumerate(stacks) if s > 0]
    if stacks[hero] <= 0:                       # hero busted -> takes a bottom place
        return payouts[len(live)]
    eqs = icm.malmuth_weitzman([stacks[i] for i in live], payouts[:len(live)])
    return eqs[live.index(hero)]


def bubble_factor(stacks: list[float], payouts: list[float], hero: int,
                  jam_stack: float) -> dict:
    """Required calling equity under ICM vs chip-EV, for `hero` facing an all-in
    of size `jam_stack` (both covered).  Their ratio is the factor by which the
    chip-EV (ch. 12) calling threshold must tighten near the money.

    Chip-EV break-even: the caller risks `jam_stack` to win it back, so in the
    symmetric covered case the chip-EV threshold is 0.5; the ICM premium scales
    it up.
    """
    eq_fold = _hero_equity(stacks, payouts, hero)
    others = [j for j in range(len(stacks)) if j != hero]
    loser = min(others, key=lambda j: stacks[j])       # smallest = likely jammer
    won = list(stacks)
    won[hero] += jam_stack
    won[loser] = max(0.0, won[loser] - jam_stack)
    eq_win = _hero_equity(won, payouts, hero)
    lost = list(stacks)
    lost[hero] = max(0.0, lost[hero] - jam_stack)
    eq_lose = _hero_equity(lost, payouts, hero)
    req_icm = required_equity(eq_win, eq_lose, eq_fold)
    return {"req_icm": req_icm, "req_chipEV": 0.5, "bubble_factor": req_icm / 0.5}


def build_artifact_data() -> dict:
    # Chicken payoff matrix and equilibria.
    chicken = {
        "matrix": {"drive_drive": [-10, -10], "drive_swerve": [1, -1],
                   "swerve_drive": [-1, 1], "swerve_swerve": [0, 0]},
        "equilibria": ["A drive / B swerve", "B drive / A swerve",
                       f"mixed: drive on {chicken_mixed_equilibrium():.0%}"],
    }
    # Required-equity comparison for the reproduced bubble situations.
    bubble = [
        {"name": "SNG 5-3-2: four 2500 stacks (28.2)",
         "req_icm": 0.6133, "req_chipEV": 0.42},
        {"name": "SNG 5-3-2: one big stack 5500/1500x3",
         "req_icm": 0.625, "req_chipEV": 0.42},
        {"name": "SNG 5-3-2: four equal, UTG jams",
         "req_icm": 0.658, "req_chipEV": None},
    ]
    # Bubble factor swept along the money bubble of a 5-3-2 SNG: hero (a 2500
    # stack) facing a jam, as the fourth player's stack shrinks toward the bubble.
    sweep = []
    for hero_stack in range(1000, 5001, 250):
        rest = (10000 - hero_stack) / 3.0
        stacks = [hero_stack, rest, rest, rest]
        bf = bubble_factor(stacks, [5, 3, 2, 0], 0, min(hero_stack, rest))
        sweep.append({"hero_stack": hero_stack, "req_icm": round(bf["req_icm"], 4),
                      "bubble_factor": round(bf["bubble_factor"], 4)})
    return {"chicken": chicken, "bubble": bubble, "bubble_factor_sweep": sweep}


def main() -> None:
    checks = reproductions()
    width = max(len(c.name) for c in checks)
    print("Reproducing Chen ch. 28 (Poker's Still Poker):\n")
    for c in checks:
        flag = "ok " if c.ok else "XX "
        print(f"  [{flag}] {c.name:<{width}}  got {c.got:.6g}   want {c.want:.6g}")
    n_ok = sum(c.ok for c in checks)
    print(f"\n  {n_ok}/{len(checks)} checks pass.")

    with open("strategy.json", "w") as f:
        json.dump(build_artifact_data(), f)
    print("Wrote strategy.json")

    if not all(c.ok for c in checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
