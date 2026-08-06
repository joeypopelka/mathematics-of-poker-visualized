#!/usr/bin/env python3
"""Build the interactive HTML artifact from sweep.npz + thresholds.json + jumps.json."""
import json
import numpy as np

def sparse_rows(X):
    """Quantize to permille and store sparse [idx, permille, idx, permille, ...]."""
    rows = []
    for r in X:
        q = np.round(r * 1000).astype(int)
        nz = np.where(q > 0)[0]
        flat = []
        for i in nz:
            flat.extend([int(i), int(q[i])])
        rows.append(flat)
    return rows

def main():
    d = np.load("sweep.npz", allow_pickle=True)
    grid, J, C, V, w = d["grid"], d["J"], d["C"], d["V"], d["w"]
    labels = [str(x) for x in d["labels"]]
    thresholds = json.load(open("thresholds.json"))
    jumps = json.load(open("jumps.json"))
    gaps = json.load(open("strict_gaps.json"))

    cards = [
        ["ATs ignites at S = 833.93",
         "The first hand to join AA as stacks descend from infinity — not KK: an ace in hand "
         "halves the number of AA combos the defender can call with, and among ace-highs, ATs "
         "has the best equity vs AA (0.13336; the ten adds the most straights). Chen prints "
         "<b>833.25</b>: his formula values a called jam at 2S·q − S relative to folding, which "
         "drops the attacker's refunded half-blind. Same equity, consistent accounting: "
         "S = 611.5 / (1 − 2q) = <b>833.93</b>."],
        ["A book erratum: A5s vs AA = 0.13307, not 0.13331",
         "Exact enumeration gives A5s 0.13307 vs AA (p. 130 prints 0.13331), moving its entry "
         "to <b>S ≈ 833.26</b> (Chen: 833.12). Downstream consequence: at S = 833 the exact "
         "equilibrium is {AA 100%, ATs 100%, <b>A5s 85.5%</b>} — the forced mixing lands on "
         "A5s, not on ATs as the book's 87.73% calculation suggests."],
        ["ATs vanishes twice on the way down",
         "ATs is jammed on (594, 834), <b>strictly out</b> on (427, 590) — its EV margin is a "
         "decisive −0.027 bb at S = 500 — back in on (157, 424), out again on (137, 157), and "
         "permanently in below 135. The defender's AKs calling window mirrors it exactly: he "
         "calls AKs precisely when the attacker is jamming ATs. Chen's &ldquo;hands eliminated "
         "completely and replaced by other hands,&rdquo; caught in the act."],
        ["Chen's three &ldquo;broken strategies,&rdquo; confirmed",
         "The book's table footnote stars three short-stack hands with split jamming ranges. "
         "This sweep reproduces all three: <b>63s</b> [≤2.39] ∪ [5.1–7.2] (Chen: ≤2.3, 5.1–7.1), "
         "<b>53s</b> [≤2.41] ∪ [4.0–12.90] (Chen: ≤2.4, 4.1–12.9), "
         "<b>43s</b> [≤2.20] ∪ [4.8–10.0] (Chen: ≤2.2, 4.8–10.0)."],
        ["Linked transitions everywhere",
         "QQ's jam threshold and QQ's call threshold die at the same stack (S ≈ 269.4), and "
         "the defender's JJ call flickers back to life exactly on (269.4, 274.1) — the window "
         "between QQ leaving and TT leaving the jam range. Almost every deep-stack transition "
         "arrives in a coupled attacker/defender pair."],
        ["97s jams up to S ≈ 36 — an underdog vs a random hand",
         "Chen highlights 97s as a jam to &ldquo;approximately 36 units&rdquo;; the exact "
         "threshold is <b>36.08</b>. What matters is not equity vs a random hand but equity vs "
         "the calling range — and middle suited connectors fare comparatively well against the "
         "big pairs and big aces that call."],
    ]

    payload = {
        "cards": cards,
        "gaps": gaps,
        "S": [round(float(s), 4) for s in grid],
        "labels": labels,
        "w": [round(float(x), 8) for x in w],
        "jam": sparse_rows(J),
        "call": sparse_rows(C),
        "value": [round(float(v), 6) for v in V],
        "jamPct": [round(float(np.dot(w, J[k])) * 100, 3) for k in range(len(grid))],
        "callPct": [round(float(np.dot(w, C[k])) * 100, 3) for k in range(len(grid))],
        "thresholds": thresholds,
        "jumps": jumps,
    }
    blob = json.dumps(payload, separators=(",", ":"))
    tpl = open("artifact_template.html").read()
    out = tpl.replace("/*__DATA__*/null", blob)
    with open("shove_fold_explorer.html", "w") as f:
        f.write(out)
    print(f"wrote shove_fold_explorer.html ({len(out)/1e6:.1f} MB)")

if __name__ == "__main__":
    main()
