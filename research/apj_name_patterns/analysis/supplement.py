"""Completion of plan.md items that analysis.py did not carry out, run after the first results.

Not new tests: each is named in plan.md (Controls 1 and 3; Test 1's three contrasts; Power).
  A. Length as a covariate (Control 3): partial Mantel with the sound matrix residualised on
     the names' lengths (sum and difference of log length), list distance partialled as before.
  B. Test 2 with permutations restricted to neighbourhoods (Control 1): values shuffled only
     within blocks of five consecutive first-list rows.
  C. Test 1's three contrasts, each as its own family: right vs left names; will side (W) vs
     understanding side (U); the three degrees C/S/N. Fisher per feature, BH within the family,
     permutation min-p threshold within the family; survivors checked in the second list.
  D. Detection floor of the grid: for each coded value, the smallest number of names that a
     piece found ONLY in that class must occur in to pass the familywise threshold.
Run: python3 supplement.py   (imports analysis.py, which re-runs and rewrites results.json
identically: fixed seed, deterministic order). Writes results_supplement.json.
"""
import math, json, random
import analysis as A

rng = random.Random(A.SEED + 1)
S = {}

# ---------------------------------------------------------------- A. length covariate
def ols_resid(y, X):
    """Residuals of y on columns X (intercept added), by normal equations."""
    cols = [[1.0] * len(y)] + X
    k = len(cols)
    XtX = [[sum(a * b for a, b in zip(cols[i], cols[j])) for j in range(k)] for i in range(k)]
    Xty = [sum(a * b for a, b in zip(cols[i], y)) for i in range(k)]
    M = [row[:] + [v] for row, v in zip(XtX, Xty)]          # Gauss-Jordan
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(k):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    beta = [M[i][k] / M[i][i] for i in range(k)]
    return [yy - sum(b * col[t] for b, col in zip(beta, cols)) for t, yy in enumerate(y)], beta

def mantel_length(names, label, nperm=A.NPERM):
    n = len(names)
    idx = [(i, j) for i in range(n) for j in range(i + 1, n)]
    mean = [A.meaning_sim(names[i], names[j]) for i, j in idx]
    dist = [abs(A.order(names[i]) - A.order(names[j])) for i, j in idx]
    ll = [math.log(len(x['name'])) for x in names]
    snd = [A.sound_sim(names[i]['name'], names[j]['name']) for i, j in idx]
    lsum = [ll[i] + ll[j] for i, j in idx]; ldif = [abs(ll[i] - ll[j]) for i, j in idx]
    res, beta = ols_resid(snd, [lsum, ldif])
    Sres = [[0.0] * n for _ in range(n)]
    for (i, j), v in zip(idx, res):
        Sres[i][j] = Sres[j][i] = v
    r = A.pearson(mean, res); rxz = A.pearson(mean, dist); ryz = A.pearson(res, dist)
    pr = A.partial_r(r, rxz, ryz)
    perm = list(range(n)); nr = []; npr = []
    for _ in range(nperm):
        rng.shuffle(perm)
        sp = [Sres[perm[i]][perm[j]] for i, j in idx]
        r_ = A.pearson(mean, sp); nr.append(r_); npr.append(A.partial_r(r_, rxz, A.pearson(sp, dist)))
    S[label] = dict(n_names=n, n_pairs=len(idx),
                    r_sound_vs_length_sum=round(A.pearson(snd, lsum), 4),
                    r_sound_vs_length_diff=round(A.pearson(snd, ldif), 4),
                    r_meaning_vs_length_sum=round(A.pearson(mean, lsum), 4),
                    r_given_length=round(r, 4), p_perm=round((1 + sum(v >= r for v in nr)) / (1 + nperm), 4),
                    partial_r_given_length_and_distance=round(pr, 4),
                    p_perm_partial=round((1 + sum(v >= pr for v in npr)) / (1 + nperm), 4))

mantel_length(A.MEM, 'A_mantel_length_members_L1_L2')
mantel_length(A.L1, 'A_mantel_length_L1_only')

# ---------------------------------------------------------------- shared grid machinery
def cells_for(names, values):
    feats = [A.features_of(n['name']) for n in names]; vals = [A.values_of(n) for n in names]; N = len(names)
    fc = A.Counter(f for fs in feats for f in fs)
    F = sorted(f for f, c in fc.items() if c >= 3)
    V = [v for v in values if sum(v in x for x in vals) >= 3]
    return feats, vals, F, V, N

def scan(feats, vals, F, V, N):
    out = []
    for v in V:
        hv = [v in x for x in vals]; K = sum(hv)
        for f in F:
            hf = [f in x for x in feats]; n_ = sum(hf); k = sum(a and b for a, b in zip(hv, hf))
            out.append((f, v, k, K, n_, A.fisher_greater(k, K, n_, N) if k else 1.0))
    return out

def minp_null(feats, vals, F, V, N, shuffler, nperm=1000):
    m = []
    for _ in range(nperm):
        pv = shuffler(vals)
        m.append(min(c[5] for c in scan(feats, pv, F, V, N)))
    return sorted(m)[int(0.05 * nperm) - 1]

def plain_shuffle(vals):
    pv = vals[:]; rng.shuffle(pv); return pv

# ---------------------------------------------------------------- B. neighbourhood-restricted grid
L1o = sorted(A.L1, key=lambda n: int(n['row']))
feats, vals, F, V, N = cells_for(L1o, sorted(A.V1))
blocks = [list(range(i, min(i + 5, N))) for i in range(0, N, 5)]
def block_shuffle(vals):
    pv = vals[:]
    for b in blocks:
        sub = [vals[i] for i in b]; rng.shuffle(sub)
        for i, v in zip(b, sub): pv[i] = v
    return pv
cells = scan(feats, vals, F, V, N)
thr = minp_null(feats, vals, F, V, N, block_shuffle)
S['B_grid_neighbourhood_restricted'] = dict(block_size=5, n_cells=len(cells), familywise_threshold_p=thr,
                                            n_cells_below=sum(c[5] <= thr for c in cells),
                                            min_p_observed=min(c[5] for c in cells))

# ---------------------------------------------------------------- C. the three contrasts
def contrast(label, keep, values):
    sub = [n for n in A.L1 if keep(n)]
    feats, vals, F, V, N = cells_for(sub, values)
    cs = scan(feats, vals, F, V, N)
    q = A.bh([c[5] for c in cs])
    thr = minp_null(feats, vals, F, V, N, plain_shuffle)
    best = sorted(range(len(cs)), key=lambda i: cs[i][5])[:5]
    sub2 = [n for n in A.L2 + A.FO if keep(n)]
    def rep(f, v):
        hv = [v in A.values_of(n) for n in sub2]; hf = [f in A.features_of(n['name']) for n in sub2]
        k = sum(a and b for a, b in zip(hv, hf)); K = sum(hv); n_ = sum(hf)
        return dict(k=k, K=K, n_with_feature=n_, N=len(sub2),
                    p=A.fisher_greater(k, K, n_, len(sub2)) if (K and n_) else None)
    S[label] = dict(n_names=N, values=V, n_cells=len(cs), familywise_threshold_p=thr,
                    n_q_below_0_10=sum(x < 0.10 for x in q), n_below_familywise=sum(c[5] <= thr for c in cs),
                    best=[dict(feature=cs[i][0], value=cs[i][1], k=cs[i][2], K=cs[i][3], n_with_feature=cs[i][4],
                               p=round(cs[i][5], 5), q=round(q[i], 3), replication_L2_forces=rep(cs[i][0], cs[i][1]))
                          for i in best])

contrast('C1_right_vs_left', lambda n: bool(n['pol'] & {'R', 'L'}), ['pol=R', 'pol=L'])
contrast('C2_will_vs_understanding', lambda n: bool(n['pol'] & {'W', 'U'}), ['pol=W', 'pol=U'])
contrast('C3_three_degrees', lambda n: n['degree'] in ('C', 'S', 'N'), ['degree=C', 'degree=S', 'degree=N'])

# ---------------------------------------------------------------- D. detection floor of the grid
alpha = A.R['test2_grid_L1']['familywise_threshold_p']; N1 = len(A.L1)
vals1 = [A.values_of(n) for n in A.L1]
floor = []
for v in sorted(A.V1):
    K = sum(v in x for x in vals1); kmin = None
    for k in range(1, K + 1):
        if math.exp(A.logC(K, k) - A.logC(N1, k)) <= alpha:   # piece in k names, all of them in the class
            kmin = k; break
    floor.append(dict(value=v, K=K, k_min_exclusive=kmin, share=None if kmin is None else round(kmin / K, 2)))
S['D_detection_floor'] = dict(familywise_threshold_p=alpha, N=N1, by_value=floor)

# ---------------------------------------------------------------- names behind the leading grid cells
lead = []
for t in A.R['test2_grid_L1']['top20'][:6]:
    lead.append(dict(feature=t['feature'], value=t['value'],
                     names=[(n['row'], n['name'], n['member']) for n in A.L1
                            if t['feature'] in A.features_of(n['name']) and t['value'] in A.values_of(n)]))
S['names_behind_top6'] = lead

A.HERE.joinpath('results_supplement.json').write_text(json.dumps(S, ensure_ascii=False, indent=1))
print(json.dumps({k: v for k, v in S.items() if k not in ('names_behind_top6',)}, ensure_ascii=False, indent=1))
print(json.dumps(S['names_behind_top6'], ensure_ascii=False))
