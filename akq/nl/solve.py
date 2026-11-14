#!/usr/bin/env python3
"""
Exact equilibrium of the full-street no-limit AKQ game (the Mathematics of
Poker ch. 13-15 family), solved by sequence-form LP on a refined bet-size
grid, swept across starting stack sizes.

Game:
  - Three-card deck {A > K > Q}; each player dealt one card (6 equally
    likely deals). Antes of 0.5 each make a pot of 1; stacks of S pots behind.
  - X acts first (out of position): check or bet any amount u <= S.
  - Y acts second (in position): facing a check, check or bet; facing a bet,
    fold, call, or raise (total raises capped at `raise_cap`; all-in always
    on the grid). One street; showdown when action closes.

Accounting: value = Y's expected net (antes included). Both-check showdown
is EV 0 by symmetry, so V_Y(S=0) = 0 and V_Y > 0 measures the value of
position.

Method: sequence-form zero-sum LP (both players' LPs solved, strong-duality
check) on a bet-size grid refined around the equilibrium support with a
bounded grid budget. `allowed` hooks support restricted variants (ablations:
half-street, no King bets, no raises) used to attribute value to options.
"""
import json
import sys
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, lil_matrix, hstack as sphstack, \
    vstack as spvstack

CARDS = ["Q", "K", "A"]          # index = strength
DEALS = [(x, y) for x in range(3) for y in range(3) if x != y]  # (X, Y)

# ---------------------------------------------------------------- game tree
class Node:
    __slots__ = ("player", "hist", "actions", "children", "kind", "bx", "by")
    def __init__(self, player, hist, kind, bx, by):
        self.player = player      # 0 = X, 1 = Y, None = terminal
        self.hist = hist          # tuple of (action, amount)
        self.kind = kind          # "decision" | "showdown" | "fold"
        self.bx, self.by = bx, by # chips committed beyond antes
        self.actions = []
        self.children = []

def build_tree(S, sizes, raise_cap):
    sizes = sorted({round(float(u), 12) for u in sizes if 0 < u <= S}
                   | {round(float(S), 12)})
    root = Node(0, (), "decision", 0.0, 0.0)

    def expand(node, to_act, facing, nraises):
        own = node.bx if to_act == 0 else node.by
        acts = []
        if facing == own:                     # nothing to call
            acts.append(("k", None))
            acts += [("b", u) for u in sizes if u > own]
        else:
            acts.append(("f", None))
            acts.append(("c", None))
            if nraises < raise_cap:
                acts += [("r", w) for w in sizes if w > facing]
        for a, amt in acts:
            h = node.hist + ((a, amt),)
            bx, by = node.bx, node.by
            if a in ("b", "r"):
                if to_act == 0: bx = amt
                else: by = amt
            if a == "k":
                if to_act == 0:               # X checks -> Y acts
                    child = Node(1, h, "decision", bx, by)
                    expand(child, 1, bx, 0)
                else:                         # Y checks back -> showdown
                    child = Node(None, h, "showdown", bx, by)
            elif a == "f":
                child = Node(None, h, "fold", bx, by)
            elif a == "c":
                if to_act == 0: bx = by
                else: by = bx
                child = Node(None, h, "showdown", bx, by)
            else:                             # bet or raise -> opponent acts
                nxt = 1 - to_act
                child = Node(nxt, h, "decision", bx, by)
                expand(child, nxt, amt, nraises + (1 if a == "r" else 0))
            node.actions.append((a, amt))
            node.children.append(child)

    expand(root, 0, 0.0, 0)
    return root, sizes

# ---------------------------------------------------------------- sequence form
def allow_all(player, card, hist, action):
    return True

def build_sequence_form(root, allowed=allow_all):
    """Infoset = (card, public history). `allowed` may forbid (player, card,
    hist, action) triples for restricted variants; passive actions
    (check/fold/call) are never forbidden."""
    seqs = [{}, {}]
    infosets = [{}, {}]      # (card, hist) -> list of (action, seq_index)
    parent_seq = [{}, {}]
    nseq = [1, 1]

    def acts_of(node, player, card):
        return [a for a in node.actions
                if a[0] in ("k", "f", "c") or allowed(player, card, node.hist, a)]

    def walk(node, card, player, cur_seq):
        if node.player is None:
            return
        if node.player == player:
            key = (card, node.hist)
            if key not in infosets[player]:
                infosets[player][key] = []
                parent_seq[player][key] = cur_seq
                for a in acts_of(node, player, card):
                    seqs[player][(card, node.hist, a)] = nseq[player]
                    infosets[player][key].append((a, nseq[player]))
                    nseq[player] += 1
            for a, child in zip(node.actions, node.children):
                sk = (card, node.hist, a)
                if sk in seqs[player]:
                    walk(child, card, player, seqs[player][sk])
        else:
            for child in node.children:
                walk(child, card, player, cur_seq)

    for player in range(2):
        for card in range(3):
            walk(root, card, player, 0)

    def constraint_matrix(player):
        rows = 1 + len(infosets[player])
        E = lil_matrix((rows, nseq[player]))
        E[0, 0] = 1.0
        for r, (key, alist) in enumerate(infosets[player].items(), start=1):
            E[r, parent_seq[player][key]] = 1.0
            for _, s in alist:
                E[r, s] = -1.0
        e = np.zeros(rows); e[0] = 1.0
        return E.tocsr(), e

    E, e = constraint_matrix(0)
    F, f = constraint_matrix(1)

    A = lil_matrix((nseq[0], nseq[1]))

    def walk_pay(node, sx, sy, cx, cy, prob):
        for a, child in zip(node.actions, node.children):
            nsx, nsy = sx, sy
            if node.player == 0:
                sk = (cx, node.hist, a)
                if sk not in seqs[0]:
                    continue
                nsx = seqs[0][sk]
            else:
                sk = (cy, node.hist, a)
                if sk not in seqs[1]:
                    continue
                nsy = seqs[1][sk]
            if child.player is None:
                if child.kind == "fold":
                    pay = (0.5 + child.bx) if node.player == 0 else -(0.5 + child.by)
                else:
                    pay = (0.5 + child.bx) if cy > cx else -(0.5 + child.by)
                A[nsx, nsy] += prob * pay
            else:
                walk_pay(child, nsx, nsy, cx, cy, prob)

    for cx, cy in DEALS:
        walk_pay(root, 0, 0, cx, cy, 1.0 / 6.0)

    return E, e, F, f, A.tocsr(), seqs, infosets, parent_seq, nseq

# ---------------------------------------------------------------- LP
def solve_lp(E, e, F, f, A):
    """Both players' sequence-form LPs; returns (x, y, value_to_Y)."""
    nX, nY = A.shape
    nQ, nP = E.shape[0], F.shape[0]

    c = np.zeros(nY + nQ); c[nY] = -1.0
    A_ub = sphstack([-A, E.T], format="csr")
    A_eq = sphstack([F, csr_matrix((nP, nQ))], format="csr")
    ry = linprog(c, A_ub=A_ub, b_ub=np.zeros(nX), A_eq=A_eq, b_eq=f,
                 bounds=[(0, None)] * nY + [(None, None)] * nQ, method="highs")
    assert ry.status == 0, f"Y LP failed: {ry.message}"
    y, vy = ry.x[:nY], -ry.fun

    c2 = np.zeros(nX + nP); c2[nX] = 1.0
    A_ub2 = sphstack([A.T, -F.T], format="csr")
    A_eq2 = sphstack([E, csr_matrix((nQ, nP))], format="csr")
    rx = linprog(c2, A_ub=A_ub2, b_ub=np.zeros(nY), A_eq=A_eq2, b_eq=e,
                 bounds=[(0, None)] * nX + [(None, None)] * nP, method="highs")
    assert rx.status == 0, f"X LP failed: {rx.message}"
    x, vx = rx.x[:nX], rx.fun
    assert abs(vx - vy) < 1e-7, f"duality gap {vx - vy}"
    return x, y, 0.5 * (vx + vy)

def clean_plans(E, e, F, f, A, seqs, v, eps=1e-8):
    """Tie-break among optimal strategies: minimize total aggressive
    (bet/raise) realization mass subject to guaranteeing the game value.
    Kills payoff-equivalent aggression (e.g. raising a range that can
    never call) so displayed strategies are canonical."""
    nX, nY = A.shape
    nQ, nP = E.shape[0], F.shape[0]
    aggX = np.zeros(nX); aggY = np.zeros(nY)
    for player, agg in ((0, aggX), (1, aggY)):
        for (card, hist, a), idx in seqs[player].items():
            if a[0] in ("b", "r"):
                agg[idx] = 1.0

    # X: min agg.x  s.t.  A^T x - F^T p <= 0,  p_0 <= v+eps,  E x = e, x >= 0
    c = np.concatenate([aggX, np.zeros(nP)])
    p0row = np.zeros(nX + nP); p0row[nX] = 1.0
    A_ub = spvstack([sphstack([A.T, -F.T], format="csr"),
                     csr_matrix(p0row)], format="csr")
    b_ub = np.concatenate([np.zeros(nY), [v + eps]])
    A_eq = sphstack([E, csr_matrix((nQ, nP))], format="csr")
    rx = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=e,
                 bounds=[(0, None)] * nX + [(None, None)] * nP, method="highs")
    assert rx.status == 0, f"clean X LP failed: {rx.message}"

    # Y: min agg.y  s.t.  E^T q - A y <= 0,  -q_0 <= -(v-eps),  F y = f, y >= 0
    c2 = np.concatenate([aggY, np.zeros(nQ)])
    q0row = np.zeros(nY + nQ); q0row[nY] = -1.0
    A_ub2 = spvstack([sphstack([-A, E.T], format="csr"),
                      csr_matrix(q0row)], format="csr")
    b_ub2 = np.concatenate([np.zeros(nX), [-(v - eps)]])
    A_eq2 = sphstack([F, csr_matrix((nP, nQ))], format="csr")
    ry = linprog(c2, A_ub=A_ub2, b_ub=b_ub2, A_eq=A_eq2, b_eq=f,
                 bounds=[(0, None)] * nY + [(None, None)] * nQ, method="highs")
    assert ry.status == 0, f"clean Y LP failed: {ry.message}"
    return rx.x[:nX], ry.x[:nY]

def onpath_lines(sol, root, thresh=1e-7):
    """Per-infoset behavioral mixes, restricted to infosets actually reached
    at equilibrium. Returns list of dicts."""
    seqs, x, y = sol["seqs"], sol["x"], sol["y"]
    reach = {}   # (player, card, hist) -> P(reach)

    def walk(node, sx, sy, cx, cy, prob):
        if node.player is None:
            return
        card = cx if node.player == 0 else cy
        key = (node.player, card, node.hist)
        own = x[sx] if node.player == 0 else y[sy]
        opp = y[sy] if node.player == 0 else x[sx]
        reach[key] = reach.get(key, 0.0) + prob * x[sx] * y[sy]
        for a, child in zip(node.actions, node.children):
            nsx, nsy = sx, sy
            if node.player == 0:
                sk = (cx, node.hist, a)
                if sk not in seqs[0]: continue
                nsx = seqs[0][sk]
            else:
                sk = (cy, node.hist, a)
                if sk not in seqs[1]: continue
                nsy = seqs[1][sk]
            walk(child, nsx, nsy, cx, cy, prob)

    for cx, cy in DEALS:
        walk(root, 0, 0, cx, cy, 1.0 / 6.0)

    out = []
    for player in range(2):
        plan = x if player == 0 else y
        for (card, hist), alist in sol["infosets"][player].items():
            r = reach.get((player, card, hist), 0.0)
            if r <= thresh:
                continue
            parent = plan[sol["parent"][player][(card, hist)]]
            if parent <= 1e-12:
                continue
            mix = [(a, plan[idx] / parent) for a, idx in alist
                   if plan[idx] / parent > 1e-5]
            out.append({
                "player": "XY"[player], "card": CARDS[card],
                "hist": [[a, amt] for a, amt in hist],
                "reach": r,
                "mix": [[a[0], a[1], p] for a, p in mix],
            })
    return out

# ---------------------------------------------------------------- analysis of a solution
def bet_mass(plan, seqs, player):
    """size -> total realization mass, split by first-bet vs raise."""
    bets, raises = {}, {}
    for (card, hist, a), idx in seqs[player].items():
        if plan[idx] > 1e-9 and a[0] in ("b", "r"):
            d = bets if a[0] == "b" else raises
            d[a[1]] = d.get(a[1], 0.0) + plan[idx]
    return bets, raises

def strategy_lines(plan, seqs, player, thresh=1e-5):
    """Readable per-infoset action mix, realization-weighted."""
    lines = {}
    for (card, hist, a), idx in sorted(seqs[player].items(), key=lambda kv: kv[1]):
        p = plan[idx]
        if p > thresh:
            h = " ".join(f"{aa}{'' if amt is None else format(amt, '.4g')}"
                         for aa, amt in hist)
            act = f"{a[0]}{'' if a[1] is None else format(a[1], '.4g')}"
            lines.setdefault((CARDS[card], h), []).append((act, p))
    return lines

# ---------------------------------------------------------------- refined solve
def solve_S(S, raise_cap=1, rounds=6, lo=0.02, hi=3.0, backbone_n=24,
            grid_cap=110, allowed=allow_all, verbose=False, tol=1e-10,
            clean=False, extra_sizes=()):
    hi = min(hi, S)
    lo = min(lo, S / 2)
    backbone = set(np.geomspace(lo, hi, backbone_n).tolist()) | {float(S)} \
        | {float(u) for u in extra_sizes if 0 < u <= S}
    grid = set(backbone)
    prev_v, out = None, None
    for r in range(rounds):
        root, sizes = build_tree(S, grid, raise_cap)
        E, e, F, f, A, seqs, infosets, parent_seq, nseq = \
            build_sequence_form(root, allowed)
        x, y, v = solve_lp(E, e, F, f, A)
        if clean:
            x, y = clean_plans(E, e, F, f, A, seqs, v)
        bx, rx_ = bet_mass(x, seqs, 0)
        by, ry_ = bet_mass(y, seqs, 1)
        out = {"S": S, "value": v, "x": x, "y": y, "seqs": seqs,
               "infosets": infosets, "parent": parent_seq, "sizes": sizes,
               "betX": bx, "raiseX": rx_, "betY": by, "raiseY": ry_}
        if verbose:
            top = lambda d: sorted(d.items(), key=lambda kv: -kv[1])[:6]
            print(f"  round {r}: |grid|={len(sizes)} V={v:+.9f} "
                  f"betX={[(round(s,4), round(m,3)) for s, m in top(bx)]} "
                  f"betY={[(round(s,4), round(m,3)) for s, m in top(by)]}")
        if prev_v is not None and abs(v - prev_v) < tol:
            break
        prev_v = v
        # refine around the highest-mass bet & raise sizes, bounded budget
        garr = sorted(sizes)
        def midpoints(d, topn):
            pts = set()
            for u, _ in sorted(d.items(), key=lambda kv: -kv[1])[:topn]:
                i = min(range(len(garr)), key=lambda j: abs(garr[j] - u))
                for j in (i - 1, i + 1):
                    if 0 <= j < len(garr):
                        pts.add(0.5 * (garr[i] + garr[j]))
            return pts
        support = {u for d in (bx, by, rx_, ry_) for u in d}
        grid = set(backbone) | support \
            | midpoints(bx, 14) | midpoints(by, 14) \
            | midpoints(rx_, 8) | midpoints(ry_, 8)
        if len(grid) > grid_cap:
            mass = {u: bx.get(u, 0) + by.get(u, 0) + rx_.get(u, 0) + ry_.get(u, 0)
                    for u in grid}
            extra = sorted((u for u in grid if u not in backbone),
                           key=lambda u: -mass.get(u, 0))
            grid = set(backbone) | set(extra[:grid_cap - len(backbone)])
    return out

def describe(sol):
    print(f"S = {sol['S']:g}   V_Y = {sol['value']:+.9f}")
    for player, name, plan in ((0, "X", sol["x"]), (1, "Y", sol["y"])):
        for (card, h), acts in strategy_lines(plan, sol["seqs"], player).items():
            astr = ", ".join(f"{a}:{p:.4f}" for a, p in acts)
            print(f"  {name}[{card}] after '{h or 'root'}': {astr}")

if __name__ == "__main__":
    S = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    sol = solve_S(S, raise_cap=cap, verbose=True)
    describe(sol)
