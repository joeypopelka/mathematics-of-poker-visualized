"""Run all three modules' reproduction suites and report a combined tally.

    python3 analyze.py          # reproduce every worked number in ch. 26-28
"""
from __future__ import annotations

import sys

import doubling_up
import icm
import strategy


def main() -> None:
    suites = [
        ("ch. 26 / 28  Theory of Doubling Up + Rebuy", doubling_up.reproductions()),
        ("ch. 27       Chips Aren't Cash (four ICM formulas)", icm.reproductions()),
        ("ch. 28       Poker's Still Poker (strategy)", strategy.reproductions()),
    ]
    total = passed = 0
    for title, checks in suites:
        n_ok = sum(c.ok for c in checks)
        total += len(checks)
        passed += n_ok
        status = "ok" if n_ok == len(checks) else "FAIL"
        print(f"[{status:>4}] {title}: {n_ok}/{len(checks)}")
        for c in checks:
            if not c.ok:
                print(f"         XX {c.name}: got {c.got:.6g}, want {c.want:.6g}")

    print(f"\n{passed}/{total} reproduction checks pass across ch. 26-28.")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
