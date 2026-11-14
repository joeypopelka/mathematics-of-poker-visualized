#!/usr/bin/env python3
"""Sequence-form LP solver for the finite-pot [0,1] games (ch. 17).

Implements PLAN_sequence_form_LP.md:
  - Game #11 (two bets, check-raise) solved EXACTLY per discretization, with a
    rigorous band test for X's value/check boundary x1 (the question CFR could
    not answer).
  - Game #10 (drop check-raise) and #9 (drop raises) as validation gates
    against the book's closed forms.
  - Game #12 (unlimited raises, no check-raise) as a raise-ladder capped at B
    bets, B swept until the value converges -> the finite-pot game value the
    book declined to compute.

Hands uniform on [0,1], LOWER = better. Bucket i has value v=(i+0.5)/N.
Terminal payoffs identical to the validated game11_cfr_solver.py (constant-sum
P). uX is X's net profit with the pot P treated as dead money; the notes'
ex-showdown game value to Y is  G(Y) = P/2 - E[uX].

LP (Koller–Megiddo–von Stengel): X's realization plan x >= 0 with flow E x = e;
Y's flow F y = f.  max_{x,q} f'q  s.t.  E x = e,  F'q <= A'x.
"""
import json
import sys
import numpy as np
from scipy import sparse
from scipy.optimize import linprog


# ---------------------------------------------------------------- game #9/10/11
# X sequences per bucket: 0 empty, 1 bet, 2 check, 3 bet·call, 4 bet·fold,
#                         5 check·raise, 6 check·call, 7 check·fold
# Y sequences per bucket: 0 empty, 1 raise, 2 call, 3 fold (facing bet),
#                         4 bet, 5 chk (facing check), 6 bet·crcall, 7 bet·crfold
NX, NY = 8, 8


def build_two_bet(P, N, allowCR=True, allowRaise=True):
    """Payoff matrix A (sparse), flows (E,e), (F,f), bounds for #9/#10/#11."""
    v = (np.arange(N) + 0.5) / N
    S = (v[:, None] < v[None, :]).astype(float)
    np.fill_diagonal(S, 0.5)
    c = 1.0 / (N * N)

    def xi(i, k):
        return i * NX + k

    def yj(j, k):
        return j * NY + k

    # --- payoff A: 9 leaf patterns (Cbf is zero, skipped) ---
    rows, cols, vals = [], [], []

    def block(kx, ky, M):
        ii, jj = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")
        rows.append((ii * NX + kx).ravel())
        cols.append((jj * NY + ky).ravel())
        vals.append((c * M).ravel())

    block(2, 5, P * S)                       # CC   check / chk
    block(6, 4, S * (P + 2) - 1)             # Cbc  check·call / bet
    block(1, 3, np.full((N, N), float(P)))   # Bf   bet / fold
    block(1, 2, S * (P + 2) - 1)             # Bc   bet / call
    if allowRaise:
        block(4, 1, np.full((N, N), -1.0))   # BrF  bet·fold / raise
        block(3, 1, S * (P + 4) - 2)         # BrC  bet·call / raise
    if allowCR:
        block(5, 7, np.full((N, N), P + 1.0))  # CbrF check·raise / bet·crfold
        block(5, 6, S * (P + 4) - 2)           # CbrC check·raise / bet·crcall
    A = sparse.coo_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(NX * N, NY * N)).tocsr()

    # --- X flow: 4 rows per bucket ---
    er, ec, ev, e = [], [], [], []
    for i in range(N):
        r0 = 4 * i
        er += [r0]
        ec += [xi(i, 0)]
        ev += [1.0]
        e.append(1.0)                                  # r(empty)=1
        er += [r0 + 1] * 3
        ec += [xi(i, 1), xi(i, 2), xi(i, 0)]
        ev += [1, 1, -1]
        e.append(0.0)                                  # bet+check=empty
        er += [r0 + 2] * 3
        ec += [xi(i, 3), xi(i, 4), xi(i, 1)]
        ev += [1, 1, -1]
        e.append(0.0)                                  # bet·call+bet·fold=bet
        er += [r0 + 3] * 4
        ec += [xi(i, 5), xi(i, 6), xi(i, 7), xi(i, 2)]
        ev += [1, 1, 1, -1]
        e.append(0.0)                                  # cr+cc+cf=check
    E = sparse.coo_matrix((ev, (er, ec)), shape=(4 * N, NX * N)).tocsr()
    e = np.array(e)

    # --- Y flow: 4 rows per bucket ---
    fr, fc, fv, f = [], [], [], []
    for j in range(N):
        r0 = 4 * j
        fr += [r0]
        fc += [yj(j, 0)]
        fv += [1.0]
        f.append(1.0)                                  # r(empty)=1
        fr += [r0 + 1] * 4
        fc += [yj(j, 1), yj(j, 2), yj(j, 3), yj(j, 0)]
        fv += [1, 1, 1, -1]
        f.append(0.0)                                  # raise+call+fold=empty
        fr += [r0 + 2] * 3
        fc += [yj(j, 4), yj(j, 5), yj(j, 0)]
        fv += [1, 1, -1]
        f.append(0.0)                                  # bet+chk=empty
        fr += [r0 + 3] * 3
        fc += [yj(j, 6), yj(j, 7), yj(j, 4)]
        fv += [1, 1, -1]
        f.append(0.0)                                  # crcall+crfold=bet
    F = sparse.coo_matrix((fv, (fr, fc)), shape=(4 * N, NY * N)).tocsr()
    f = np.array(f)

    # disabled actions -> upper bound 0
    ub = np.ones(NX * N)
    vb = np.ones(NY * N)
    if not allowCR:
        for i in range(N):
            ub[xi(i, 5)] = 0.0
    if not allowRaise:
        for j in range(N):
            vb[yj(j, 1)] = 0.0
    return A, E, e, F, f, ub, vb, v


def solve_seq_lp(A, E, e, F, f, ub, opp_keep=None, extra_obj=None,
                 value_floor=None, extra_geq=()):
    """max_{x,q} f'q  s.t. Ex=e, 0<=x<=ub, F'q <= A'x  (+ refinements).

    opp_keep: boolean mask over opponent sequences; disabled opponent actions
    (forced to zero in their primal) must have their dual constraint rows
    dropped here.
    extra_obj: vector L over x -> objective becomes maximize L'x subject to
    f'q >= value_floor (optimality held fixed).
    extra_geq: iterable of (Lvec_over_x, floor) linear constraints L'x >= floor
    (for lexicographic refinements over the optimal face).
    Returns (x, q, objective).
    """
    nx = A.shape[0]
    nq = F.shape[0]
    AT = A.T.tocsr()
    FT = F.T.tocsr()
    if opp_keep is not None:
        AT = AT[opp_keep]
        FT = FT[opp_keep]
    # A_ub rows: F'q - A'x <= 0  (one row per active opponent sequence)
    rows = [sparse.hstack([-AT, FT], format="csr")]
    bub = [np.zeros(AT.shape[0])]
    if value_floor is not None:
        # -f'q <= -value_floor
        frow = sparse.hstack([sparse.csr_matrix((1, nx)),
                              sparse.csr_matrix(f[None, :])], format="csr")
        rows.append(-frow)
        bub.append(np.array([-value_floor]))
    for L, floor in extra_geq:
        lrow = sparse.hstack([sparse.csr_matrix(L[None, :]),
                              sparse.csr_matrix((1, nq))], format="csr")
        rows.append(-lrow)
        bub.append(np.array([-floor]))
    Aub = sparse.vstack(rows, format="csr") if len(rows) > 1 else rows[0]
    bub = np.concatenate(bub)
    Aeq = sparse.hstack([E, sparse.csr_matrix((E.shape[0], nq))], format="csr")
    if extra_obj is None:
        cvec = np.concatenate([np.zeros(nx), -f])      # maximize f'q
    else:
        cvec = np.concatenate([-extra_obj, np.zeros(nq)])
    bounds = [(0.0, u) for u in ub] + [(None, None)] * nq
    res = linprog(cvec, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=e,
                  bounds=bounds, method="highs")
    assert res.status == 0, res.message
    x = res.x[:nx]
    q = res.x[nx:]
    return x, q, -res.fun


def _mono(A, E, e, F, f, ub, keep, K, N, aggr, cont, quit_, floor, eps=1e-8):
    """Lexicographic monotone selection over the optimal face (see below)."""
    w_top = (N - np.arange(N)) / N              # decreasing in hand index
    w_bot = (1 + np.arange(N)) / N              # increasing
    n = K * N

    def vec(cols, w):
        L = np.zeros(n)
        for k in cols:
            L[k::K] = w
        return L

    geq = []
    x = None
    for L in (vec(aggr, w_top), vec(cont, w_top), vec(quit_, w_bot)):
        x, _, opt = solve_seq_lp(A, E, e, F, f, ub, keep, L, floor, geq)
        geq = geq + [(L, opt - eps * max(1.0, abs(opt)))]
    return x.reshape(-1, K)


def monotone_selection(sol, player="X", eps=1e-8):
    """Extract the canonical (book-style) threshold representative from the
    optimal face: lexicographically push aggression toward stronger hands.

    Vs. the optimal opponent these games have large per-hand indifference
    classes; the book's crisp thresholds are the monotone selection. Passes
    (each holding all previous optima fixed):
      1. maximize strength-weighted aggressive mass (bet/raise to the top)
      2. maximize strength-weighted continue-vs-raise mass (calls to the top)
      3. maximize weakness-weighted give-up mass (folds to the bottom)
    """
    N = sol["N"]
    G = sol["value"]
    if player == "X":
        return _mono(sol["A"], sol["E"], sol["e"], sol["F"], sol["f"],
                     sol["ub"], sol["vb"] > 0, NX, N,
                     [1, 5], [3, 6], [4, 7],
                     G - eps * max(1.0, abs(G)), eps)
    return _mono((-sol["A"].T).tocsr(), sol["F"], sol["f"], sol["E"], sol["e"],
                 sol["vb"], sol["ub"] > 0, NY, N,
                 [1, 4], [2, 6], [3, 7],
                 -G - eps * max(1.0, abs(G)), eps)


def monotone_selection_ladder(sol, player="X", eps=1e-8):
    """Monotone selection for the game #12 raise ladder."""
    N = sol["N"]
    G = sol["value"]
    xk, yk = sol["xk"], sol["yk"]
    if player == "X":
        K = len(sol["xseq"])
        aggr = [xk[s] for s in sol["xseq"] if s == "made1" or s.startswith("xr")]
        cont = [xk[s] for s in sol["xseq"]
                if s == "chk_call" or s.startswith("xc")]
        quit_ = [xk[s] for s in sol["xseq"]
                 if s == "chk_fold" or s.startswith("xf")]
        A, E, e, F, f = sol["A"], sol["E"], sol["e"], sol["F"], sol["f"]
        return _mono(A, E, e, F, f, np.ones(K * N), None, K, N,
                     aggr, cont, quit_, G - eps * max(1.0, abs(G)), eps)
    K = len(sol["yseq"])
    aggr = [yk[s] for s in sol["yseq"] if s == "bet" or s.startswith("yr")]
    cont = [yk[s] for s in sol["yseq"] if s.startswith("yc")]
    quit_ = [yk[s] for s in sol["yseq"] if s.startswith("yf")]
    return _mono((-sol["A"].T).tocsr(), sol["F"], sol["f"], sol["E"], sol["e"],
                 np.ones(K * N), None, K, N, aggr, cont, quit_,
                 -G - eps * max(1.0, abs(G)), eps)


def solve_game(P, N, allowCR=True, allowRaise=True):
    """Solve both players' LPs; return behavioral strategies + value."""
    A, E, e, F, f, ub, vb, v = build_two_bet(P, N, allowCR, allowRaise)
    keepX = ub > 0
    keepY = vb > 0
    x, qx, VX = solve_seq_lp(A, E, e, F, f, ub, keepY)
    # mirror: Y maximizes y'(-A')x  ->  same routine with roles swapped
    y, qy, VY = solve_seq_lp((-A.T).tocsr(), F, f, E, e, vb, keepX)
    assert abs(VX + VY) < 1e-6 * max(1.0, abs(VX)), (VX, VY)  # strong duality
    X = x.reshape(-1, NX)
    Y = y.reshape(-1, NY)
    return dict(P=P, N=N, v=v, X=X, Y=Y, value=VX, GY=P / 2.0 - VX,
                A=A, E=E, e=e, F=F, f=f, ub=ub, vb=vb)


# ------------------------------------------------------------ region reporting
def regions_X(X, v, N):
    """RLE classification of X buckets (behavioral, from realization weights)."""
    out = []
    for i in range(N):
        bet, chk = X[i, 1], X[i, 2]
        if bet > 0.5:
            out.append("B-call" if X[i, 3] > X[i, 4] else "B-fold")
        elif chk > 0.5:
            k = np.argmax(X[i, 5:8])
            out.append(["C-raise", "C-call", "C-fold"][k])
        else:
            out.append("mixed")
    return rle(out, v, N)


def regions_Y(Y, v, N):
    outb = []
    outc = []
    for j in range(N):
        outb.append(["raise", "call", "fold"][int(np.argmax(Y[j, 1:4]))])
        if Y[j, 4] > 0.5:
            outc.append("bet-crcall" if Y[j, 6] > Y[j, 7] else "bet-crfold")
        else:
            outc.append("check")
    return rle(outb, v, N), rle(outc, v, N)


def rle(types, v, N):
    segs = []
    i = 0
    while i < N:
        j = i
        while j < N and types[j] == types[i]:
            j += 1
        segs.append((round(v[i] - 0.5 / N, 4), round(v[j - 1] + 0.5 / N, 4),
                     types[i]))
        i = j
    return segs


def crossing(vals, v, up=False, thresh=0.5):
    """First index where vals crosses thresh (decreasing unless up)."""
    cond = vals > thresh if up else vals < thresh
    idx = np.where(cond)[0]
    return None if len(idx) == 0 else float(v[idx[0]] - 0.5 / len(v))


# ------------------------------------------------------------------- band test
def band_test_x1(sol, eps=1e-8):
    """Max/min X's total bet mass over the optimal face; then per-bucket
    min/max of bet probability on buckets where the two extremes differ."""
    A, E, e, F, f, ub = sol["A"], sol["E"], sol["e"], sol["F"], sol["f"], sol["ub"]
    N = sol["N"]
    G = sol["value"]
    floor = G - eps * max(1.0, abs(G))
    keepY = sol["vb"] > 0
    L = np.zeros(NX * N)
    L[1::NX] = 1.0                            # total mass of 'bet'
    xmax, _, Lmax = solve_seq_lp(A, E, e, F, f, ub, keepY, L, floor)
    xmin, _, Lmin = solve_seq_lp(A, E, e, F, f, ub, keepY, -L, floor)
    Lmin = -Lmin
    Xmax = xmax.reshape(-1, NX)
    Xmin = xmin.reshape(-1, NX)
    diff = np.where(np.abs(Xmax[:, 1] - Xmin[:, 1]) > 1e-6)[0]
    if len(diff) > 60:                        # cap LP count; keep coverage
        diff = diff[np.linspace(0, len(diff) - 1, 60).astype(int)]
    per_bucket = []
    for i in diff:
        Li = np.zeros(NX * N)
        Li[i * NX + 1] = 1.0
        _, _, hi = solve_seq_lp(A, E, e, F, f, ub, keepY, Li, floor)
        _, _, lo = solve_seq_lp(A, E, e, F, f, ub, keepY, -Li, floor)
        per_bucket.append((i, -lo, hi))
    return dict(bet_mass_min=Lmin / N, bet_mass_max=Lmax / N,
                band_buckets=diff.tolist(), per_bucket=per_bucket,
                Xmax=Xmax, Xmin=Xmin)


# -------------------------------------------------------------------- game #12
def build_ladder(P, N, B):
    """Game #12: one street, folding, raises capped at B total bets, no c-r.

    X sequences: 0 empty, 1 check, 2 chk·call, 3 chk·fold, 4 'made bet 1',
      then per even facing-level n=2,4,..: fold_n, call_n, raise_n(->bet n+1,
      only if n+1<=B).
    Y sequences: 0 empty, 1 bet (after check), 2 chk, then per odd facing-level
      n=1,3,..: fold_n, call_n, raise_n(->bet n+1, only if n+1<=B).
    """
    v = (np.arange(N) + 0.5) / N
    S = (v[:, None] < v[None, :]).astype(float)
    np.fill_diagonal(S, 0.5)
    c = 1.0 / (N * N)

    # per-bucket sequence catalogs + infosets as (parent, [children])
    xseq = ["empty", "check", "chk_call", "chk_fold", "made1"]
    xinfo = [("empty", ["made1", "check"]),            # root: bet or check
             ("check", ["chk_call", "chk_fold"])]      # facing Y's bet
    yseq = ["empty", "bet", "chk"]
    yinfo = [("empty", ["bet", "chk"])]                # facing X's check
    n = 2
    while n <= B:                              # X faces even bet n
        par = "made1" if n == 2 else f"xr{n - 2}"
        ch = [f"xf{n}", f"xc{n}"]
        xseq += ch
        if n + 1 <= B:
            xseq.append(f"xr{n}")
            ch.append(f"xr{n}")
        xinfo.append((par, ch))
        n += 2
    n = 1
    while n <= B:                              # Y faces odd bet n
        par = "empty" if n == 1 else f"yr{n - 2}"
        ch = [f"yf{n}", f"yc{n}"]
        yseq += ch
        if n + 1 <= B:
            yseq.append(f"yr{n}")
            ch.append(f"yr{n}")
        yinfo.append((par, ch))
        n += 2
    KX, KY = len(xseq), len(yseq)
    xk = {s: k for k, s in enumerate(xseq)}
    yk = {s: k for k, s in enumerate(yseq)}

    rows, cols, vals = [], [], []

    def block(kx, ky, M):
        ii, jj = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")
        rows.append((ii * KX + kx).ravel())
        cols.append((jj * KY + ky).ravel())
        vals.append((c * M).ravel())

    block(xk["check"], yk["chk"], P * S)
    block(xk["chk_call"], yk["bet"], S * (P + 2) - 1)
    # bet line leaves
    n = 1
    while n <= B:                              # Y decision at odd n
        made = "made1" if n == 1 else f"xr{n - 1}"
        block(xk[made], yk[f"yf{n}"], np.full((N, N), float(P + n - 1)))
        block(xk[made], yk[f"yc{n}"], S * (P + 2 * n) - n)
        n += 2
    n = 2
    while n <= B:                              # X decision at even n
        yr = f"yr{n - 1}"
        block(xk[f"xf{n}"], yk[yr], np.full((N, N), -(n - 1.0)))
        block(xk[f"xc{n}"], yk[yr], S * (P + 2 * n) - n)
        n += 2
    A = sparse.coo_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(KX * N, KY * N)).tocsr()

    def flows(seqs, infosets, K):
        kidx = {s: k for k, s in enumerate(seqs)}
        rr, cc, vv, rhs = [], [], [], []
        nrow = 0
        for i in range(N):
            rr.append(nrow)
            cc.append(i * K + kidx["empty"])
            vv.append(1.0)
            rhs.append(1.0)
            nrow += 1
            for p, ch in infosets:             # one row per infoset
                for s in ch:
                    rr.append(nrow)
                    cc.append(i * K + kidx[s])
                    vv.append(1.0)
                rr.append(nrow)
                cc.append(i * K + kidx[p])
                vv.append(-1.0)
                rhs.append(0.0)
                nrow += 1
        M = sparse.coo_matrix((vv, (rr, cc)), shape=(nrow, K * N)).tocsr()
        return M, np.array(rhs)

    E, e = flows(xseq, xinfo, KX)
    F, f = flows(yseq, yinfo, KY)
    ub = np.ones(KX * N)
    vb = np.ones(KY * N)
    return A, E, e, F, f, ub, vb, v, xseq, yseq, xk, yk, KX, KY


def solve_ladder(P, N, B):
    A, E, e, F, f, ub, vb, v, xseq, yseq, xk, yk, KX, KY = build_ladder(P, N, B)
    x, _, VX = solve_seq_lp(A, E, e, F, f, ub)
    y, _, VY = solve_seq_lp((-A.T).tocsr(), F, f, E, e, vb)
    assert abs(VX + VY) < 1e-6 * max(1.0, abs(VX)), (VX, VY)
    return dict(P=P, N=N, B=B, v=v, X=x.reshape(-1, KX), Y=y.reshape(-1, KY),
                xseq=xseq, yseq=yseq, xk=xk, yk=yk, value=VX, GY=P / 2 - VX,
                A=A, E=E, e=e, F=F, f=f)


# ------------------------------------------------------------------ validation
def validate(N=200):
    print(f"=== VALIDATION (N={N}) ===")
    ok = True

    # Gate 0: Game #9 closed forms at P=2 (X-side via monotone selection)
    s = solve_game(2.0, N, allowCR=False, allowRaise=False)
    Xm = monotone_selection(s, "X")
    x1 = crossing(Xm[:, 1], s["v"])
    y1 = crossing(s["Y"][:, 4], s["v"])
    x1s = crossing(Xm[:, 7], s["v"], up=True)   # first check-fold bucket
    GY = s["GY"]
    print(f"#9  P=2: x1={x1:.4f} (1/3)  y1={y1:.4f} (1/2)  "
          f"x1*={x1s:.4f} (2/3)  G(Y)={GY:.4f} (0.0556)")
    ok &= abs(x1 - 1 / 3) < 2.5 / N and abs(y1 - 0.5) < 1.5 / N
    ok &= abs(x1s - 2 / 3) < 2.5 / N
    ok &= abs(GY - 1 / 18) < 2e-3

    # Gate 1: Game #10 at P=2 (no check-raise)
    s = solve_game(2.0, N, allowCR=False)
    Xm = monotone_selection(s, "X")
    x1 = crossing(Xm[:, 1], s["v"])
    x2s = crossing(Xm[:, 3], s["v"])
    x1s = crossing(Xm[:, 7], s["v"], up=True)
    y2 = crossing(s["Y"][:, 1], s["v"])
    y1 = crossing(s["Y"][:, 4], s["v"])
    print(f"#10 P=2: x2*={x2s:.4f} (0.190)  x1={x1:.4f} (0.238)  "
          f"x1*={x1s:.4f} (0.648)  y2={y2:.4f} (0.095)  y1={y1:.4f} (0.443)  "
          f"G(Y)={s['GY']:.4f} (0.068)")
    ok &= abs(x1 - 5 / 21) < 2.5 / N and abs(y2 - 2 / 21) < 1.5 / N
    ok &= abs(x2s - 4 / 21) < 2.5 / N and abs(y1 - 279 / 630) < 1.5 / N
    ok &= abs(x1s - 68 / 105) < 2.5 / N

    # Gate 2: Game #11 Y-side closed forms (Eq. 17.13) at P=2
    s = solve_game(2.0, N, allowCR=True)
    a, a2 = 1 / 3, 1 / 5
    R = (1 - a2) / 2
    y1c = (1 - a) / (1 + a + (1 - a2) * R)
    y2c = R * y1c
    y0c = 1 - a * y1c
    y1n = crossing(s["Y"][:, 4], s["v"])
    y2n = crossing(s["Y"][:, 1], s["v"])
    # y0: bottom of Y's betting range = top of bluffs; bet mass near 1
    yb = s["Y"][:, 4]
    y0n = None
    for j in range(s["N"] - 1, 0, -1):
        if yb[j] > 0.5 and yb[j - 1] < 0.5:
            y0n = float(s["v"][j] - 0.5 / N)
            break
    print(f"#11 P=2: y1={y1n:.4f} ({y1c:.4f})  y2={y2n:.4f} ({y2c:.4f})  "
          f"y0={y0n:.4f} ({y0c:.4f})  G(Y)={s['GY']:.4f} (region-sum 0.062)")
    ok &= abs(y1n - y1c) < 1.5 / N and abs(y2n - y2c) < 1.5 / N
    ok &= abs(y0n - y0c) < 2.5 / N

    # Gate 3: #11 at P=200 approaches no-fold #7 (x1=5/9, y1=2/3, y2=1/3)
    s = solve_game(200.0, N, allowCR=True)
    x1n = crossing(s["X"][:, 1] + s["X"][:, 5], s["v"])  # value continue mass
    y1n = crossing(s["Y"][:, 4], s["v"])
    y2n = crossing(s["Y"][:, 1], s["v"])
    print(f"#11 P=200: x1~{x1n:.3f} (->0.556)  y1={y1n:.3f} (->0.667)  "
          f"y2={y2n:.3f} (->0.333)")

    # Gate 4: ladder with B=2 == game #10
    s10 = solve_game(2.0, N, allowCR=False)
    s12 = solve_ladder(2.0, N, 2)
    print(f"#12[B=2] P=2: G(Y)={s12['GY']:.5f}  vs #10 {s10['GY']:.5f}")
    ok &= abs(s12["GY"] - s10["GY"]) < 1e-6
    print("ALL GATES PASS" if ok else "*** GATE FAILURE ***")
    return ok


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--validate":
        N = int(sys.argv[2]) if len(sys.argv) > 2 else 200
        sys.exit(0 if validate(N) else 1)
    print("usage: seqlp.py --validate [N]   (see game11_exact.py, game12_value.py)")
