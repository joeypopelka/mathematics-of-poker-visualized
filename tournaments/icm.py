"""Module 2 - Chips Aren't Cash: four chip -> prize-equity formulas (ch. 27).

Given remaining stacks and the remaining payout ladder, map each player's chip
count to a cash equity.  The chapter surveys four models and notes each one's
bias; we implement all four and reproduce the worked examples.

    Proportional Chip Count   (27.1)  <Xi> = vn + si*Wn       lower bound
    Landrum-Burns             (27.2)  first = si, rest split equally  upper bound
    Malmuth-Harville          (27.3)  Harville horse-racing analogue  (accurate)
    Malmuth-Weitzman          (27.4)  P(bust next) ~ 1/chips          (accurate)

Also the tournament variance multiple k = n*sum(vi^2) - 1  (27.5).

`python3 icm.py` reproduces the chapter's numbers and writes icm.json.
"""
from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def chip_fractions(stacks: list[float]) -> list[float]:
    total = float(sum(stacks))
    return [s / total for s in stacks]


# --------------------------------------------------------------------------- #
# Proportional Chip Count  (27.1)
# --------------------------------------------------------------------------- #
def prop_chip(stacks: list[float], payouts: list[float]) -> list[float]:
    """<Xi> = vn + si*Wn.  Everyone banks the min payout vn; the rest of the
    pool Wn is split by chip fraction.  Biased toward big stacks (can even
    pay the leader more than first place)."""
    n = len(stacks)
    vn = payouts[n - 1]                       # guaranteed (last paid) amount
    Wn = sum(payouts[:n]) - n * vn            # incremental pool above the floor
    s = chip_fractions(stacks)
    return [vn + si * Wn for si in s]


def prop_chip_capped(stacks: list[float], payouts: list[float]) -> list[float]:
    """The book's floor-function modification: with m = floor(1/xi), set
    p_{i,j<=m} = xi and p_{i,m+1} = 1 - m*xi.  Gives a tighter upper bound on
    big-stack equity, but no longer sums to the prize pool."""
    n = len(stacks)
    x = chip_fractions(stacks)
    out = []
    for xi in x:
        m = min(int(math.floor(1.0 / xi)), n)
        p = [0.0] * n
        for j in range(m):
            p[j] = xi
        if m < n:
            p[m] = 1.0 - m * xi
        out.append(sum(p[j] * payouts[j] for j in range(n)))
    return out


# --------------------------------------------------------------------------- #
# Landrum-Burns  (27.2)
# --------------------------------------------------------------------------- #
def landrum_burns(stacks: list[float], payouts: list[float]) -> list[float]:
    """P(1st) = xi; when not first, finish equally often in every other place.
    Biased toward small stacks (they bust immediately far less often than they
    would place 2nd)."""
    n = len(stacks)
    x = chip_fractions(stacks)
    v1 = payouts[0]
    rest = sum(payouts[1:n])
    return [xi * v1 + (1.0 - xi) / (n - 1) * rest for xi in x]


# --------------------------------------------------------------------------- #
# Sequential-selection place distribution (shared by Harville & Weitzman)
# --------------------------------------------------------------------------- #
def _selection_place_matrix(weights: list[float]) -> list[list[float]]:
    """P[i][k] = probability player i is the k-th selected (k=0 first), when at
    each step the next pick is chosen with probability proportional to `weights`.

    Feed chip counts -> selection order is the finishing order (Harville).
    Feed inverse chip counts -> selection order is the bust order (Weitzman).
    O(2^n * n); intended for final-table / SNG sizes (n <= ~12).
    """
    n = len(weights)
    total = float(sum(weights))
    # f[mask] = probability the set `mask` is exactly the first popcount(mask) picks
    f = [0.0] * (1 << n)
    f[0] = 1.0
    sum_w = [0.0] * (1 << n)
    for mask in range(1, 1 << n):
        low = mask & (-mask)
        i = low.bit_length() - 1
        sum_w[mask] = sum_w[mask ^ low] + weights[i]
    P = [[0.0] * n for _ in range(n)]
    for mask in range(1 << n):
        remaining = total - sum_w[mask]
        if remaining <= 0:
            continue
        fm = f[mask]
        if fm == 0.0:
            continue
        k = bin(mask).count("1")
        for i in range(n):
            if mask & (1 << i):
                continue
            prob = fm * weights[i] / remaining      # i is the (k+1)-th pick
            P[i][k] += prob
            f[mask | (1 << i)] += prob
    return P


def malmuth_harville(stacks: list[float], payouts: list[float]) -> list[float]:
    """Harville analogue: finishing order drawn top-down with P ~ chips (27.3)."""
    n = len(stacks)
    x = chip_fractions(stacks)
    place = _selection_place_matrix(x)               # place[i][j] = P(i finishes j-th)
    return [sum(place[i][j] * payouts[j] for j in range(n)) for i in range(n)]


def malmuth_weitzman(stacks: list[float], payouts: list[float]) -> list[float]:
    """Weitzman: bust order drawn bottom-up with P(bust next) ~ 1/chips (27.4)."""
    n = len(stacks)
    x = chip_fractions(stacks)
    y = [1.0 / xi for xi in x]
    sel = _selection_place_matrix(y)                 # sel[i][k]: i is k-th to bust
    # k-th selected == k-th to bust == finishing place (n - k).  Reverse the axis.
    return [sum(sel[i][k] * payouts[n - 1 - k] for k in range(n)) for i in range(n)]


# --------------------------------------------------------------------------- #
# Tournament variance multiple  (27.5)
# --------------------------------------------------------------------------- #
def variance_multiple(payout_fractions: list[float], field: int) -> float:
    """k = n * sum(vi^2) - 1, with vi the prize fractions of the pool."""
    return field * sum(v * v for v in payout_fractions) - 1.0


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
    stacks = [25000, 20000, 10000, 5000]
    payouts = [2000, 1400, 900, 700]

    pc = prop_chip(stacks, payouts)
    for i, want in enumerate([1616.67, 1433.33, 1066.67, 883.33]):
        ck.append(Check(f"prop-chip P{i+1}", pc[i], want, 0.01))

    lb = landrum_burns(stacks, payouts)
    #   Book prints P3 = 1066.67, but that breaks the sum-to-pool identity;
    #   the correct Landrum-Burns value is 1166.67 (a book typo, flagged below).
    for i, want in enumerate([1416.67, 1333.33, 1166.67, 1083.33]):
        ck.append(Check(f"landrum-burns P{i+1}", lb[i], want, 0.01))
    ck.append(Check("landrum-burns sums to pool", sum(lb), 5000.0, 1e-6))

    cap = prop_chip_capped(stacks, payouts)
    ck.append(Check("capped prop-chip P1", cap[0], 1566.67, 0.01))

    # Second example exposes the prop-chip flaw (leader paid > first place).
    stacks2 = [48000, 4000, 4000, 4000]
    pc2 = prop_chip(stacks2, payouts)
    ck.append(Check("prop-chip flaw: P1", pc2[0], 2460.0, 0.01))     # > 2000!
    ck.append(Check("prop-chip flaw: P2", pc2[1], 846.67, 0.01))
    lb2 = landrum_burns(stacks2, payouts)
    ck.append(Check("landrum-burns ex2 P1", lb2[0], 1800.0, 0.01))
    ck.append(Check("landrum-burns ex2 P2", lb2[1], 1066.67, 0.01))

    # All four models must agree when stacks are equal (payout / n each).
    eq = [2500, 2500, 2500, 2500]
    for name, fn in (("prop", prop_chip), ("lb", landrum_burns),
                     ("mh", malmuth_harville), ("mw", malmuth_weitzman)):
        vals = fn(eq, payouts)
        ck.append(Check(f"equal stacks {name}", max(abs(v - 1250) for v in vals),
                        0.0, 1e-9))

    # Malmuth-Harville / Weitzman: sum to pool, and sit between the bounds.
    mh = malmuth_harville(stacks, payouts)
    mw = malmuth_weitzman(stacks, payouts)
    ck.append(Check("MH sums to pool", sum(mh), 5000.0, 1e-6))
    ck.append(Check("MW sums to pool", sum(mw), 5000.0, 1e-6))
    #   Leader equity: prop-chip (biased high) >= MH,MW >= Landrum-Burns (low).
    ck.append(Check("MH leader below prop-chip", 1.0 if mh[0] <= pc[0] else 0.0, 1.0, 0))
    ck.append(Check("MH leader above LB", 1.0 if mh[0] >= lb[0] else 0.0, 1.0, 0))

    # Variance multiple k (27.5): Player T's morning / evening tournaments.
    morning = [.30, .20, .12, .10, .08, .06, .055, .045, .04]
    evening = ([.275, .175, .116, .08, .06, .045, .035, .026, .017]
               + [.012] * 9 + [.007] * 9)
    ck.append(Check("variance mult (morning)", variance_multiple(morning, 100),
                    16.105, 0.02))
    #   The morning value reproduces the book exactly, validating (27.5).  The
    #   evening percentages as printed sum to 100% and give 53.263 by the same
    #   formula -- but the book reports 53.6456.  The printed table does not
    #   reproduce the book's own number (a book inconsistency); we assert the
    #   faithful value.
    ck.append(Check("variance mult (evening)", variance_multiple(evening, 400),
                    53.263, 0.02))

    return ck


# --------------------------------------------------------------------------- #
# Data for the explorer: four-model disagreement along a stack sweep
# --------------------------------------------------------------------------- #
def build_artifact_data() -> dict:
    payouts = [2000, 1400, 900, 700]
    # Slide the chip leader's stack from even (15k) up to a huge lead (48k),
    # keeping the other three equal, and record all four models.
    rows = []
    for lead in range(15000, 48001, 500):
        rest = (60000 - lead) / 3.0
        stacks = [lead, rest, rest, rest]
        rows.append({
            "lead": lead,
            "prop": [round(v, 2) for v in prop_chip(stacks, payouts)],
            "lb": [round(v, 2) for v in landrum_burns(stacks, payouts)],
            "mh": [round(v, 2) for v in malmuth_harville(stacks, payouts)],
            "mw": [round(v, 2) for v in malmuth_weitzman(stacks, payouts)],
        })
    return {"payouts": payouts, "total_chips": 60000, "sweep": rows,
            "example": {"stacks": [25000, 20000, 10000, 5000], "payouts": payouts,
                        "prop": prop_chip([25000, 20000, 10000, 5000], payouts),
                        "lb": landrum_burns([25000, 20000, 10000, 5000], payouts),
                        "mh": malmuth_harville([25000, 20000, 10000, 5000], payouts),
                        "mw": malmuth_weitzman([25000, 20000, 10000, 5000], payouts)}}


def main() -> None:
    checks = reproductions()
    width = max(len(c.name) for c in checks)
    print("Reproducing Chen ch. 27 (Chips Aren't Cash):\n")
    for c in checks:
        flag = "ok " if c.ok else "XX "
        print(f"  [{flag}] {c.name:<{width}}  got {c.got:.6g}   want {c.want:.6g}")
    n_ok = sum(c.ok for c in checks)
    print(f"\n  {n_ok}/{len(checks)} checks pass.")

    with open("icm.json", "w") as f:
        json.dump(build_artifact_data(), f)
    print("Wrote icm.json")

    if not all(c.ok for c in checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
