import numpy as np

def solve(P, N=240, T=3000, allowCR=True, allowFold=True, seed=0):
    # buckets: value v_i=(i+0.5)/N, lower = better hand (0 nuts, 1 worst)
    v = (np.arange(N)+0.5)/N
    # showdown X-wins matrix: X wins if i<j (X strictly better)
    S = (v[:,None] < v[None,:]).astype(float)  # S[i,j]
    # terminal uX(i,j) arrays
    CC   = P*S                       # check-check showdown
    Cbf  = np.zeros((N,N))           # X checks, Y bets, X folds -> 0
    Cbc  = S*(P+2)-1                 # X checks, Y bets, X calls
    CbrF = np.full((N,N), P+1.0)     # X check-raise, Y folds -> X wins pot+... = P+1
    CbrC = S*(P+4)-2                 # X check-raise, Y calls
    Bf   = np.full((N,N), float(P))  # X bets, Y folds -> P
    Bc   = S*(P+2)-1                 # X bets, Y calls
    BrF  = np.full((N,N), -1.0)      # X bets, Y raises, X folds -> -1
    BrC  = S*(P+4)-2                 # X bets, Y raises, X calls

    # regret + strategy-sum tables
    def z(k): return np.zeros((N,k))
    R_Xopen=z(2); Su_Xopen=z(2)
    R_XcB = z(3); Su_XcB = z(3)   # RAISE,CALL,FOLD
    R_XbR = z(2); Su_XbR = z(2)   # CALL,FOLD
    R_Yb  = z(3); Su_Yb  = z(3)   # RAISE,CALL,FOLD
    R_Yc  = z(2); Su_Yc  = z(2)   # BET,CHECK
    R_YcR = z(2); Su_YcR = z(2)   # CALL,FOLD

    def rm(R):
        pos=np.maximum(R,0.0); s=pos.sum(1,keepdims=True)
        return np.where(s>0, pos/np.where(s>0,s,1), 1.0/R.shape[1])

    for t in range(1,T+1):
        sX=rm(R_Xopen); sXcB=rm(R_XcB); sXbR=rm(R_XbR)
        sYb=rm(R_Yb);  sYc=rm(R_Yc);   sYcR=rm(R_YcR)
        if not allowCR: sXcB=np.stack([np.zeros(N),sXcB[:,1]/(sXcB[:,1]+sXcB[:,2]+1e-12),sXcB[:,2]/(sXcB[:,1]+sXcB[:,2]+1e-12)],1)
        if not allowFold:
            # disallow folding: renormalize fold prob into call
            pass
        xo_bet=sX[:,0][:,None]; xo_chk=sX[:,1][:,None]
        # ---- forward: node utilities uX(i,j) given current strategies
        uYcR = sYcR[:,0][None,:]*CbrC + sYcR[:,1][None,:]*CbrF
        uXcB = sXcB[:,0][:,None]*uYcR + sXcB[:,1][:,None]*Cbc + sXcB[:,2][:,None]*Cbf
        uYc  = sYc[:,0][None,:]*uXcB + sYc[:,1][None,:]*CC
        uXbR = sXbR[:,0][:,None]*BrC + sXbR[:,1][:,None]*BrF
        uYb  = sYb[:,0][None,:]*uXbR + sYb[:,1][None,:]*Bc + sYb[:,2][None,:]*Bf
        # ---- X infoset regrets (CF reach = opp reach; average over j via mean)
        # Xopen
        cfBET=uYb.mean(1); cfCHK=uYc.mean(1)
        node=sX[:,0]*cfBET+sX[:,1]*cfCHK
        R_Xopen[:,0]+=cfBET-node; R_Xopen[:,1]+=cfCHK-node
        Su_Xopen+=t*sX
        # XcB (reach j = yc_bet[j])
        w=sYc[:,0][None,:]
        cfR=(w*uYcR).mean(1); cfC=(w*Cbc).mean(1); cfF=(w*Cbf).mean(1)
        node=sXcB[:,0]*cfR+sXcB[:,1]*cfC+sXcB[:,2]*cfF
        R_XcB[:,0]+=cfR-node; R_XcB[:,1]+=cfC-node; R_XcB[:,2]+=cfF-node
        if not allowCR: R_XcB[:,0]=-1e9
        Su_XcB+=t*(xo_chk*sXcB)
        # XbR (reach j = yb_raise[j])
        w=sYb[:,0][None,:]
        cfC=(w*BrC).mean(1); cfF=(w*BrF).mean(1)
        node=sXbR[:,0]*cfC+sXbR[:,1]*cfF
        R_XbR[:,0]+=cfC-node; R_XbR[:,1]+=cfF-node
        Su_XbR+=t*(xo_bet*sXbR)
        # ---- Y infoset regrets (Y minimizes uX): regret = node-uX_a ; CF reach over i
        # Yb (reach i = xo_bet[i])
        w=sX[:,0][:,None]
        vR=(w*uXbR).mean(0); vC=(w*Bc).mean(0); vF=(w*Bf).mean(0)
        node=sYb[:,0]*vR+sYb[:,1]*vC+sYb[:,2]*vF
        R_Yb[:,0]+=node-vR; R_Yb[:,1]+=node-vC; R_Yb[:,2]+=node-vF
        Su_Yb+=t*sYb
        # Yc (reach i = xo_chk[i])
        w=sX[:,1][:,None]
        vB=(w*uXcB).mean(0); vK=(w*CC).mean(0)
        node=sYc[:,0]*vB+sYc[:,1]*vK
        R_Yc[:,0]+=node-vB; R_Yc[:,1]+=node-vK
        Su_Yc+=t*sYc
        # YcR (reach i = xo_chk[i]*xcb_raise[i])
        w=(sX[:,1]*sXcB[:,0])[:,None]
        vC=(w*CbrC).mean(0); vF=(w*CbrF).mean(0)
        node=sYcR[:,0]*vC+sYcR[:,1]*vF
        R_YcR[:,0]+=node-vC; R_YcR[:,1]+=node-vF
        Su_YcR+=t*sYcR
        # CFR+ : floor regrets
        for Rr in (R_Xopen,R_XcB,R_XbR,R_Yb,R_Yc,R_YcR): np.maximum(Rr,0.0,out=Rr)
        if not allowCR: R_XcB[:,0]=-1e9

    def norm(Su):
        s=Su.sum(1,keepdims=True); return np.where(s>0,Su/np.where(s>0,s,1),0)
    return dict(v=v, N=N,
        Xopen=norm(Su_Xopen), XcB=norm(Su_XcB), XbR=norm(Su_XbR),
        Yb=norm(Su_Yb), Yc=norm(Su_Yc), YcR=norm(Su_YcR))

def firstcross(prob, thresh=0.5):
    # first bucket index where prob<thresh (prob assumed decreasing), return value
    idx=np.where(prob<thresh)[0]
    return None if len(idx)==0 else idx[0]

def report_X(sol, label=""):
    v=sol['v']; N=sol['N']
    xo=sol['Xopen']; xcb=sol['XcB']; xbr=sol['XbR']
    # classify each X bucket
    print("  X regions ("+label+"):")
    types=[]
    for i in range(N):
        bet = xo[i,0]>0.5
        if bet:
            call = xbr[i,0]>0.5
            types.append('B-call' if call else 'B-fold')
        else:
            a=np.argmax(xcb[i])  # 0 raise,1 call,2 fold
            types.append(['C-raise','C-call','C-fold'][a])
    _rle(types, v)

def report_Y(sol, label=""):
    v=sol['v']; N=sol['N']
    yb=sol['Yb']; yc=sol['Yc']
    print("  Y|Xbets regions ("+label+"):")
    tb=[['raise','call','fold'][np.argmax(yb[j])] for j in range(N)]
    _rle(tb, v)
    print("  Y|Xchecks regions ("+label+"):")
    tc=[('bet' if yc[j,0]>0.5 else 'check') for j in range(N)]
    _rle(tc, v)

def _rle(types, v):
    i=0; N=len(types)
    while i<N:
        j=i
        while j<N and types[j]==types[i]: j+=1
        print("    [%.3f, %.3f]  %s" % (v[i]-0.5/N, v[j-1]+0.5/N, types[i]))
        i=j

if __name__=="__main__":
    import sys
    NN=420; TT=12000
    print("=== VALIDATE: Game #10 (no check-raise) at P=2 ===")
    print("   exact: x2*=0.190 x1=0.238 y2=0.095 y1=0.443 x1*=y1*=0.648 y2#=0.667 y0=0.852 x0=0.921")
    s10=solve(2.0, N=NN, T=TT, allowCR=False)
    report_X(s10,"#10 P=2"); report_Y(s10,"#10 P=2")

    print("\n=== Game #11 (CHECK-RAISE) at large pot P=200  (should approach Game #7: x1=.556 x2=.111 y1=.667 y2=.333) ===")
    s11big=solve(200.0, N=NN, T=TT, allowCR=True)
    report_X(s11big,"#11 P=200"); report_Y(s11big,"#11 P=200")

    print("\n=== Game #11 (CHECK-RAISE) at P=2 ===")
    s11=solve(2.0, N=NN, T=TT, allowCR=True)
    report_X(s11,"#11 P=2"); report_Y(s11,"#11 P=2")
