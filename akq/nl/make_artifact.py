#!/usr/bin/env python3
"""Build the self-contained interactive explorer from features.json +
landmarks.json. Emits akq_explorer.html (and index.html for GitHub Pages)."""
import json
import numpy as np

CARDS = ["A", "K", "Q"]

def g(row, key, default=0.0):
    return float(row.get(key, default))

def main():
    feats = json.load(open("features.json"))
    lm = json.load(open("landmarks.json"))
    feats.sort(key=lambda r: r["S"])

    S = [round(r["S"], 6) for r in feats]
    V = [round(r["V"], 8) for r in feats]

    def series(player, card, suffix):
        return [round(g(r, f"{player}_{card}_{suffix}"), 4) for r in feats]

    payload = {
        "S": S, "V": V,
        "landmarks": {
            "half_V": lm["half_V"], "polar_V": lm["polar_V"],
            "S_A": lm["S_A_jam_only_ends"], "S_K": lm["S_K_blocker_enters"],
            "S_star": lm["S_star_plateau_begins"],
            "V_plateau": lm["V_plateau_cap1"],
        },
        # X opens (root): check / bet(size)
        "Xopen": {c: {
            "k": series("X", c, "Xroot_k"),
            "b": series("X", c, "Xroot_b"),
            "size": series("X", c, "Xroot_b_size"),
        } for c in CARDS},
        # Y facing a bet: fold / call / raise(size)
        "YvsBet": {c: {
            "f": series("Y", c, "YvsBet_f"),
            "c": series("Y", c, "YvsBet_c"),
            "r": series("Y", c, "YvsBet_r"),
            "size": series("Y", c, "YvsBet_r_size"),
        } for c in CARDS},
        # Y after a check: check / bet(size)
        "Ycheck": {c: {
            "k": series("Y", c, "Ycheck_k"),
            "b": series("Y", c, "Ycheck_b"),
            "size": series("Y", c, "Ycheck_b_size"),
        } for c in CARDS},
        # betting-line frequencies (for the area chart)
        "lineKeys": ["k-k", "b-f", "b-c", "b-r-f", "b-r-c", "k-b-f", "k-b-c"],
        "lines": [[round(r["lines"].get(k, 0.0), 5)
                   for k in ["k-k", "b-f", "b-c", "b-r-f", "b-r-c",
                             "k-b-f", "k-b-c"]] for r in feats],
        # exact-law curves (evaluated on the same S grid where applicable)
        "lawI": [round(s * s / (6 * (1 + s)), 8) for s in S],
        "lawII": [round((s / (1 + s) - (3 - 2 * 2**0.5)) / 6, 8) for s in S],
    }
    blob = json.dumps(payload, separators=(",", ":"))
    tpl = open("akq_template.html").read()
    out = tpl.replace("/*__DATA__*/null", blob)
    with open("akq_explorer.html", "w") as f:
        f.write(out)
    print(f"wrote akq_explorer.html ({len(out)/1e3:.0f} KB)")
    with open("index.html", "w") as f:
        f.write('<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
                + out + "\n</html>\n")
    print("wrote index.html")

if __name__ == "__main__":
    main()
