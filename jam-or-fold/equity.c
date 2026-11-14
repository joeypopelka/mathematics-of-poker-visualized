/*
 * Exact preflop all-in equity calculator for heads-up NLHE.
 *
 * Computes the full 1326x1326 combo-vs-combo equity matrix by exhaustive
 * enumeration of all C(48,5) = 1,712,304 boards per matchup, reduced by
 * suit isomorphism (24 suit permutations) and multithreaded.
 *
 * Card encoding: c in 0..51, rank r = c>>2 (0=deuce .. 12=ace), suit = c&3
 * (0=c, 1=d, 2=h, 3=s).  Combo index: pairs (a<b) in lexicographic order.
 *
 * Output: equity.f32 - 1326*1326 float32, row = hero combo, col = villain
 * combo, value = hero equity (wins + ties/2) / boards; -1 for overlapping
 * combos.
 *
 * Modes:
 *   ./equity            full run -> equity.f32
 *   ./equity --selftest verify 7-card evaluator against known frequencies
 *   ./equity --eq AsAh KdKc   single matchup equity
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>

static uint16_t straightTable[8192]; /* 13-bit rank mask -> high rank of best straight, else 0 */

static void buildStraightTable(void) {
    for (int m = 0; m < 8192; m++) {
        int st = 0;
        for (int high = 12; high >= 4; high--) {
            int need = 0x1F << (high - 4);
            if ((m & need) == need) { st = high; break; }
        }
        if (!st) {
            /* wheel: A,2,3,4,5 = ranks 12,0,1,2,3 */
            int need = (1 << 12) | 0xF;
            if ((m & need) == need) st = 3;
        }
        straightTable[m] = (uint16_t)st;
    }
}

static inline int topbit(int m) { return 31 - __builtin_clz((unsigned)m); }

typedef struct {
    uint8_t  rc[13];  /* rank counts */
    uint8_t  sc[4];   /* suit counts */
    uint16_t sm[4];   /* per-suit rank masks */
} St;

static inline void addc(St *s, int c) {
    s->rc[c >> 2]++; s->sc[c & 3]++; s->sm[c & 3] |= (uint16_t)(1 << (c >> 2));
}
static inline void subc(St *s, int c) {
    s->rc[c >> 2]--; s->sc[c & 3]--; s->sm[c & 3] &= (uint16_t)~(1 << (c >> 2));
}

/* Evaluate a 7-card hand held in state s.  Higher value = better hand. */
static inline uint32_t evalSt(const St *s) {
    for (int su = 0; su < 4; su++) {
        if (s->sc[su] >= 5) {
            int m = s->sm[su];
            int st = straightTable[m];
            if (st) return (8u << 24) | ((uint32_t)st << 20);
            int v = 0;
            for (int i = 0; i < 5; i++) { int b = topbit(m); v = (v << 4) | b; m &= ~(1 << b); }
            return (5u << 24) | (uint32_t)v;
        }
    }
    int rankMask = 0, quad = -1, t1 = -1, t2 = -1, p1 = -1, p2 = -1;
    for (int r = 12; r >= 0; r--) {
        int c = s->rc[r];
        if (!c) continue;
        rankMask |= 1 << r;
        if (c == 4) quad = r;
        else if (c == 3) { if (t1 < 0) t1 = r; else if (t2 < 0) t2 = r; }
        else if (c == 2) { if (p1 < 0) p1 = r; else if (p2 < 0) p2 = r; }
    }
    if (quad >= 0) {
        int k = topbit(rankMask & ~(1 << quad));
        return (7u << 24) | ((uint32_t)quad << 20) | ((uint32_t)k << 16);
    }
    if (t1 >= 0 && (t2 >= 0 || p1 >= 0)) {
        int pp = t2;
        if (p1 > pp) pp = p1;
        return (6u << 24) | ((uint32_t)t1 << 20) | ((uint32_t)pp << 16);
    }
    int st = straightTable[rankMask];
    if (st) return (4u << 24) | ((uint32_t)st << 20);
    if (t1 >= 0) {
        int m = rankMask & ~(1 << t1);
        int k1 = topbit(m); m &= ~(1 << k1);
        int k2 = topbit(m);
        return (3u << 24) | ((uint32_t)t1 << 20) | ((uint32_t)k1 << 16) | ((uint32_t)k2 << 12);
    }
    if (p2 >= 0) {
        int m = rankMask & ~(1 << p1) & ~(1 << p2);
        int k = topbit(m);
        return (2u << 24) | ((uint32_t)p1 << 20) | ((uint32_t)p2 << 16) | ((uint32_t)k << 12);
    }
    if (p1 >= 0) {
        int m = rankMask & ~(1 << p1);
        int k1 = topbit(m); m &= ~(1 << k1);
        int k2 = topbit(m); m &= ~(1 << k2);
        int k3 = topbit(m);
        return (1u << 24) | ((uint32_t)p1 << 20) | ((uint32_t)k1 << 16) | ((uint32_t)k2 << 12) | ((uint32_t)k3 << 8);
    }
    int v = 0, mm = rankMask;
    for (int i = 0; i < 5; i++) { int b = topbit(mm); v = (v << 4) | b; mm &= ~(1 << b); }
    return (uint32_t)v;
}

/* Hero equity for hero {h0,h1} vs villain {k0,k1}: (2*wins + ties) / (2*1712304). */
static double equityPair(int h0, int h1, int k0, int k1) {
    St hs, vs;
    memset(&hs, 0, sizeof hs); memset(&vs, 0, sizeof vs);
    addc(&hs, h0); addc(&hs, h1);
    addc(&vs, k0); addc(&vs, k1);
    int deck[48], nd = 0;
    for (int c = 0; c < 52; c++)
        if (c != h0 && c != h1 && c != k0 && c != k1) deck[nd++] = c;
    int64_t win2 = 0;
    for (int a = 0; a < 44; a++) {
        addc(&hs, deck[a]); addc(&vs, deck[a]);
        for (int b = a + 1; b < 45; b++) {
            addc(&hs, deck[b]); addc(&vs, deck[b]);
            for (int c = b + 1; c < 46; c++) {
                addc(&hs, deck[c]); addc(&vs, deck[c]);
                for (int d = c + 1; d < 47; d++) {
                    addc(&hs, deck[d]); addc(&vs, deck[d]);
                    for (int e = d + 1; e < 48; e++) {
                        addc(&hs, deck[e]); addc(&vs, deck[e]);
                        uint32_t hv = evalSt(&hs), vv = evalSt(&vs);
                        win2 += (hv > vv) ? 2 : (hv == vv ? 1 : 0);
                        subc(&hs, deck[e]); subc(&vs, deck[e]);
                    }
                    subc(&hs, deck[d]); subc(&vs, deck[d]);
                }
                subc(&hs, deck[c]); subc(&vs, deck[c]);
            }
            subc(&hs, deck[b]); subc(&vs, deck[b]);
        }
        subc(&hs, deck[a]); subc(&vs, deck[a]);
    }
    return (double)win2 / (2.0 * 1712304.0);
}

/* ---------- selftest: 7-card hand-type frequencies over all C(52,7) ---------- */
static const int64_t EXPECT[9] = {
    23294460,  /* high card       */
    58627800,  /* one pair        */
    31433400,  /* two pair        */
    6461620,   /* three of a kind */
    6180020,   /* straight        */
    4047644,   /* flush           */
    3473184,   /* full house      */
    224848,    /* four of a kind  */
    41584      /* straight flush  */
};

static int selftest(void) {
    static const char *names[9] = {"high card","pair","two pair","trips","straight",
                                   "flush","full house","quads","straight flush"};
    int64_t cnt[9] = {0};
    St s; memset(&s, 0, sizeof s);
    for (int a = 0; a < 46; a++) { addc(&s, a);
    for (int b = a+1; b < 47; b++) { addc(&s, b);
    for (int c = b+1; c < 48; c++) { addc(&s, c);
    for (int d = c+1; d < 49; d++) { addc(&s, d);
    for (int e = d+1; e < 50; e++) { addc(&s, e);
    for (int f = e+1; f < 51; f++) { addc(&s, f);
    for (int g = f+1; g < 52; g++) { addc(&s, g);
        cnt[evalSt(&s) >> 24]++;
        subc(&s, g);
    } subc(&s, f);
    } subc(&s, e);
    } subc(&s, d);
    } subc(&s, c);
    } subc(&s, b);
    } subc(&s, a);
    }
    int ok = 1;
    for (int i = 0; i < 9; i++) {
        printf("%-15s %12lld  expect %12lld  %s\n", names[i], (long long)cnt[i],
               (long long)EXPECT[i], cnt[i] == EXPECT[i] ? "OK" : "MISMATCH");
        if (cnt[i] != EXPECT[i]) ok = 0;
    }
    printf(ok ? "SELFTEST PASSED\n" : "SELFTEST FAILED\n");
    return ok ? 0 : 1;
}

/* ---------- canonicalization and full run ---------- */

#define NCOMBO 1326

static int comboCard[NCOMBO][2];
static int comboOfCards[52][52];

static void buildCombos(void) {
    int n = 0;
    for (int a = 0; a < 52; a++)
        for (int b = a + 1; b < 52; b++) {
            comboCard[n][0] = a; comboCard[n][1] = b;
            comboOfCards[a][b] = comboOfCards[b][a] = n;
            n++;
        }
}

/* 24 permutations of 4 suits */
static int perms[24][4];
static void buildPerms(void) {
    int n = 0, s[4];
    for (s[0] = 0; s[0] < 4; s[0]++)
    for (s[1] = 0; s[1] < 4; s[1]++) { if (s[1] == s[0]) continue;
    for (s[2] = 0; s[2] < 4; s[2]++) { if (s[2] == s[0] || s[2] == s[1]) continue;
        s[3] = 6 - s[0] - s[1] - s[2];
        memcpy(perms[n++], s, sizeof s);
    }}
}

static inline uint32_t pairKey(int h0, int h1, int k0, int k1) {
    /* minimal encoding over all suit permutations; roles (hero/villain) fixed */
    uint32_t best = 0xFFFFFFFFu;
    for (int p = 0; p < 24; p++) {
        const int *pm = perms[p];
        int a = ((h0 >> 2) << 2) | pm[h0 & 3];
        int b = ((h1 >> 2) << 2) | pm[h1 & 3];
        int c = ((k0 >> 2) << 2) | pm[k0 & 3];
        int d = ((k1 >> 2) << 2) | pm[k1 & 3];
        if (a > b) { int t = a; a = b; b = t; }
        if (c > d) { int t = c; c = d; d = t; }
        uint32_t key = (uint32_t)a | ((uint32_t)b << 6) | ((uint32_t)c << 12) | ((uint32_t)d << 18);
        if (key < best) best = key;
    }
    return best;
}

typedef struct { uint32_t key; int32_t i, j; } PairRec;

static int cmpPair(const void *x, const void *y) {
    uint32_t a = ((const PairRec *)x)->key, b = ((const PairRec *)y)->key;
    return a < b ? -1 : (a > b ? 1 : 0);
}

/* work arrays for threads */
static int nClasses;
static int (*classRep)[4];   /* representative h0,h1,k0,k1 per class */
static double *classEq;
static _Atomic int nextClass;
static _Atomic int doneCount;

static void *worker(void *arg) {
    (void)arg;
    for (;;) {
        int c = __atomic_fetch_add((int *)&nextClass, 1, __ATOMIC_RELAXED);
        if (c >= nClasses) break;
        classEq[c] = equityPair(classRep[c][0], classRep[c][1], classRep[c][2], classRep[c][3]);
        int d = __atomic_fetch_add((int *)&doneCount, 1, __ATOMIC_RELAXED) + 1;
        if (d % 1000 == 0) fprintf(stderr, "  %d / %d classes\n", d, nClasses);
    }
    return NULL;
}

static int parseCard(const char *s) {
    const char *ranks = "23456789TJQKA", *suits = "cdhs";
    const char *rp = strchr(ranks, s[0]), *sp = strchr(suits, s[1]);
    if (!rp || !sp) { fprintf(stderr, "bad card %s\n", s); exit(1); }
    return (int)(rp - ranks) * 4 + (int)(sp - suits);
}

int main(int argc, char **argv) {
    buildStraightTable();
    buildCombos();
    buildPerms();

    if (argc > 1 && !strcmp(argv[1], "--selftest")) return selftest();

    if (argc > 3 && !strcmp(argv[1], "--eq")) {
        int h0 = parseCard(argv[2]), h1 = parseCard(argv[2] + 2);
        int k0 = parseCard(argv[3]), k1 = parseCard(argv[3] + 2);
        printf("%.10f\n", equityPair(h0, h1, k0, k1));
        return 0;
    }

    /* enumerate all unordered disjoint combo pairs (i < j) */
    PairRec *ps = malloc(sizeof(PairRec) * 812175);
    int np = 0;
    for (int i = 0; i < NCOMBO; i++) {
        int h0 = comboCard[i][0], h1 = comboCard[i][1];
        for (int j = i + 1; j < NCOMBO; j++) {
            int k0 = comboCard[j][0], k1 = comboCard[j][1];
            if (k0 == h0 || k0 == h1 || k1 == h0 || k1 == h1) continue;
            ps[np].key = pairKey(h0, h1, k0, k1);
            ps[np].i = i; ps[np].j = j;
            np++;
        }
    }
    fprintf(stderr, "disjoint unordered pairs: %d\n", np);

    qsort(ps, np, sizeof(PairRec), cmpPair);

    /* group into classes */
    int *pairClass = malloc(sizeof(int) * np);
    classRep = malloc(sizeof(int[4]) * np);
    nClasses = 0;
    for (int t = 0; t < np; t++) {
        if (t == 0 || ps[t].key != ps[t - 1].key) {
            uint32_t k = ps[t].key;
            classRep[nClasses][0] = k & 63;
            classRep[nClasses][1] = (k >> 6) & 63;
            classRep[nClasses][2] = (k >> 12) & 63;
            classRep[nClasses][3] = (k >> 18) & 63;
            nClasses++;
        }
        pairClass[t] = nClasses - 1;
    }
    fprintf(stderr, "isomorphism classes: %d\n", nClasses);

    classEq = malloc(sizeof(double) * nClasses);
    nextClass = 0; doneCount = 0;

    int nThreads = argc > 1 ? atoi(argv[1]) : 8;
    if (nThreads < 1 || nThreads > 64) nThreads = 8;
    fprintf(stderr, "threads: %d\n", nThreads);
    pthread_t th[64];
    for (int t = 0; t < nThreads; t++) pthread_create(&th[t], NULL, worker, NULL);
    for (int t = 0; t < nThreads; t++) pthread_join(th[t], NULL);

    /* fill full matrix */
    float *mat = malloc(sizeof(float) * NCOMBO * NCOMBO);
    for (int i = 0; i < NCOMBO * NCOMBO; i++) mat[i] = -1.0f;
    for (int t = 0; t < np; t++) {
        double e = classEq[pairClass[t]];
        mat[ps[t].i * NCOMBO + ps[t].j] = (float)e;
        mat[ps[t].j * NCOMBO + ps[t].i] = (float)(1.0 - e);
    }
    FILE *f = fopen("equity.f32", "wb");
    fwrite(mat, sizeof(float), (size_t)NCOMBO * NCOMBO, f);
    fclose(f);
    fprintf(stderr, "wrote equity.f32\n");
    return 0;
}
