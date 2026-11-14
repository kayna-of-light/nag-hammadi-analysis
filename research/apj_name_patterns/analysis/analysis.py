"""Sound and meaning in the angel names of the Apocryphon of John.

Tests 0-3 of research/apj_name_patterns/plan.md, in pure Python (no packages needed).
Inputs:  names.csv (build_names.py) and ../meaning_table.md (frozen 2026-11-10).
Outputs: results.json and results.md in this folder.
Run:     python3 analysis.py
"""
import csv, json, math, random, re, unicodedata, pathlib, itertools, statistics
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).parent
SEED = 20261110
NPERM = 10000

# ---------------------------------------------------------------- meaning table
def parse_meaning_table():
    t = (HERE.parent / 'meaning_table.md').read_text()
    M = {}
    for l in t.split('\n'):
        c = [x.strip() for x in l.split('|')]
        if len(c) < 8:
            continue
        key = c[1]
        if re.fullmatch(r'\d+', key) and len(c) >= 14:          # members: 12 data columns
            deg, layer, pol, use, role = c[8], c[9], c[10], c[11], c[12]
        elif re.fullmatch(r'F\d+', key) and len(c) >= 12:       # forces: 10 data columns
            deg, layer, pol, use, role = c[7], '–', c[8], c[9], c[10]
        else:
            continue
        deg = deg.split(' ')[0]
        pols = set(re.findall(r'\b(R|L|W|U)\b', pol.split('(')[0])) if 'contains' not in pol else set()
        clear = 'clear' if 'clear' in pol else ('obscure' if 'obscure' in pol else '')
        uses = set(re.findall(r'[A-Z]{4,}', use))
        M[key] = dict(degree=deg, layer=layer if layer in ('in', 'out') else '', pol=pols,
                      clear=clear, use=uses, role=role if role in ('END', 'CAUSE', 'EFFECT') else '')
    return M

M = parse_meaning_table()

# ---------------------------------------------------------------- names
def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r'[^Ⲁ-⳿Ϣ-ϯ]', '', s)

NAMES = []
for r in csv.DictReader(open(HERE / 'names.csv')):
    m = M[r['member']]
    pol = set(m['pol'])
    if pol & {'R', 'L'}:                     # symmetric member: the name's own side
        pol = (pol - {'R', 'L'}) | ({r['side']} if r['side'] in 'RL' else set())
    if r['side'] in 'RL' and r['member'] == '35':
        pol = pol | {r['side']}              # the left kidney: U and L
    NAMES.append(dict(list=r['list'], row=r['row'], name=norm(r['name']), name_IV=norm(r['name_IV']),
                      member=r['member'], side=r['side'], egyptian=r['egyptian'] == '1',
                      degree=m['degree'], layer=m['layer'], pol=pol, clear=m['clear'],
                      use=m['use'], role=m['role']))

# member order head -> feet (meaning_table numbering follows the body); forces after
def order(n):
    return int(n['member']) if n['member'].isdigit() else 100 + int(n['member'][1:])

# ---------------------------------------------------------------- sound features
def grams(s, ns=(2, 3)):
    s = '^' + s + '$'
    return {s[i:i + k] for k in ns for i in range(len(s) - k + 1)}

def jacc(a, b):
    return len(a & b) / len(a | b) if (a or b) else 0.0

def sound_sim(x, y):
    return jacc(grams(x), grams(y))

# ---------------------------------------------------------------- meaning similarity
def meaning_sim(a, b):
    parts = []
    parts.append(1.0 if a['degree'] == b['degree'] else 0.0)            # discrete: category only
    if a['layer'] or b['layer']:
        parts.append(1.0 if a['layer'] == b['layer'] else 0.0)
    if a['pol'] or b['pol']:
        parts.append(jacc(a['pol'], b['pol']))
    if a['use'] or b['use']:
        parts.append(jacc(a['use'], b['use']))
    if a['role'] or b['role']:
        parts.append(1.0 if a['role'] == b['role'] else 0.0)
    return sum(parts) / len(parts)

# ---------------------------------------------------------------- statistics helpers
def pearson(x, y):
    mx, my = statistics.fmean(x), statistics.fmean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x); syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0

def partial_r(rxy, rxz, ryz):
    d = math.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))
    return (rxy - rxz * ryz) / d if d else 0.0

_lc = {}
def logC(n, k):
    key = (n, k)
    if key not in _lc:
        _lc[key] = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    return _lc[key]

_fc = {}
def fisher_greater(k, K, n, N):
    """P(X >= k) for X ~ Hypergeom(N population, K successes, n draws)."""
    key = (k, K, n, N)
    if key in _fc:
        return _fc[key]
    hi = min(K, n); tot = logC(N, n); p = 0.0
    for x in range(k, hi + 1):
        if n - x > N - K:
            continue
        p += math.exp(logC(K, x) + logC(N - K, n - x) - tot)
    _fc[key] = min(1.0, p)
    return _fc[key]

def bh(ps):
    m = len(ps); idx = sorted(range(m), key=lambda i: ps[i]); q = [0.0] * m; prev = 1.0
    for rank, i in reversed(list(enumerate(idx, 1))):
        prev = min(prev, ps[i] * m / rank); q[i] = prev
    return q

rng = random.Random(SEED)
R = {}

# ================================================================ TEST 0a: same member, both lists
def key_of(n):
    return (n['member'], n['side'])

L1 = [n for n in NAMES if n['list'] == 'L1']
L2 = [n for n in NAMES if n['list'] == 'L2']
FO = [n for n in NAMES if n['list'] == 'F']
MEM = L1 + L2

l1_by = {key_of(n): n for n in L1}
pairs = [(l1_by[key_of(b)], b) for b in L2 if key_of(b) in l1_by]

def test_matched(pairs, label):
    A = [a['name'] for a, b in pairs]; B = [b['name'] for a, b in pairs]
    obs = statistics.fmean(sound_sim(a, b) for a, b in zip(A, B))
    # rank of the true partner among all candidates in B
    ranks = []
    for i, a in enumerate(A):
        sims = sorted(((sound_sim(a, b), j) for j, b in enumerate(B)), reverse=True)
        ranks.append(1 + [j for s, j in sims].index(i))
    null = []
    for _ in range(NPERM):
        Bp = B[:]; rng.shuffle(Bp)
        null.append(statistics.fmean(sound_sim(a, b) for a, b in zip(A, Bp)))
    p = (1 + sum(v >= obs for v in null)) / (1 + NPERM)
    R[label] = dict(n_pairs=len(pairs), mean_sim_true=round(obs, 4), mean_sim_null=round(statistics.fmean(null), 4),
                    p_perm=round(p, 4), median_rank_of_true_partner=statistics.median(ranks),
                    expected_median_rank=(len(B) + 1) / 2,
                    pairs=[(a['name'], b['name'], round(sound_sim(a['name'], b['name']), 3)) for a, b in pairs])

test_matched(pairs, 'test0a_same_member_L1_vs_L2')

# ================================================================ TEST 0b: right/left partners
def rl_pairs(names):
    by = defaultdict(dict)
    for n in names:
        if n['side'] in 'RL':
            by[n['member']][n['side']] = n
    return [(d['R'], d['L']) for d in by.values() if 'R' in d and 'L' in d]

test_matched(rl_pairs(L1) + rl_pairs(L2), 'test0b_right_left_partners')

# ================================================================ TEST 1: Mantel, meaning x sound
def mantel(names, label, exclude_same_member=False):
    n = len(names)
    idx = [(i, j) for i in range(n) for j in range(i + 1, n)
           if not (exclude_same_member and names[i]['member'] == names[j]['member'])]
    mean = [meaning_sim(names[i], names[j]) for i, j in idx]
    dist = [abs(order(names[i]) - order(names[j])) for i, j in idx]
    S = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            S[i][j] = S[j][i] = sound_sim(names[i]['name'], names[j]['name'])
    snd = [S[i][j] for i, j in idx]
    r = pearson(mean, snd); rxz = pearson(mean, dist); ryz = pearson(snd, dist)
    pr = partial_r(r, rxz, ryz)
    nr, npr = [], []
    perm = list(range(n))
    for _ in range(NPERM):
        rng.shuffle(perm)
        sp = [S[perm[i]][perm[j]] for i, j in idx]
        r_ = pearson(mean, sp); ryz_ = pearson(sp, dist)
        nr.append(r_); npr.append(partial_r(r_, rxz, ryz_))
    R[label] = dict(n_names=n, n_pairs=len(idx), r=round(r, 4),
                    p_perm=round((1 + sum(v >= r for v in nr)) / (1 + NPERM), 4),
                    partial_r_given_list_distance=round(pr, 4),
                    p_perm_partial=round((1 + sum(v >= pr for v in npr)) / (1 + NPERM), 4),
                    r_meaning_vs_distance=round(rxz, 4), r_sound_vs_distance=round(ryz, 4))

mantel(MEM, 'test1_mantel_members_L1_L2')
mantel(MEM, 'test1_mantel_excluding_same_member_pairs', exclude_same_member=True)
mantel(L1, 'test1_mantel_L1_only')
mantel([n for n in MEM if not n['egyptian']], 'test1_mantel_without_egyptian_names')

# ================================================================ TEST 2: the grid (discovery on L1)
def values_of(n):
    v = {'degree=' + n['degree']}
    if n['layer']: v.add('layer=' + n['layer'])
    v |= {'pol=' + p for p in n['pol']}
    v |= {'use=' + u for u in n['use']}
    if n['role']: v.add('role=' + n['role'])
    return v

def features_of(name):
    return grams(name, ns=(1, 2, 3))

def grid(names):
    feats = [features_of(n['name']) for n in names]
    vals = [values_of(n) for n in names]
    N = len(names)
    fcount = Counter(f for fs in feats for f in fs)
    F = sorted(f for f, c in fcount.items() if c >= 3)
    V = sorted({v for vs in vals for v in vs if sum(v in x for x in vals) >= 3})
    cells = []
    for v in V:
        has_v = [v in x for x in vals]; K = sum(has_v)
        for f in F:
            has_f = [f in x for x in feats]; n_ = sum(has_f)
            k = sum(a and b for a, b in zip(has_v, has_f))
            cells.append((f, v, k, K, n_, N, fisher_greater(k, K, n_, N)))
    return F, V, cells

F1, V1, cells = grid(L1)
q = bh([c[6] for c in cells])
# family-wise check: min p under 1,000 permutations of the name-to-member assignment
feats = [features_of(n['name']) for n in L1]; vals = [values_of(n) for n in L1]; N = len(L1)
minps = []
for _ in range(1000):
    pv = vals[:]; rng.shuffle(pv); best = 1.0
    for v in V1:
        has_v = [v in x for x in pv]; K = sum(has_v)
        for f in F1:
            has_f = [f in x for x in feats]; n_ = sum(has_f)
            k = sum(a and b for a, b in zip(has_v, has_f))
            if k:
                p = fisher_greater(k, K, n_, N)
                if p < best: best = p
    minps.append(best)
alpha_fw = sorted(minps)[49]          # 5th percentile of the permutation min-p
top = sorted(range(len(cells)), key=lambda i: cells[i][6])[:20]
R['test2_grid_L1'] = dict(n_names=N, n_features=len(F1), n_values=len(V1), n_cells=len(cells),
                          familywise_threshold_p=alpha_fw,
                          n_cells_q_below_0_10=sum(x < 0.10 for x in q),
                          n_cells_below_familywise=sum(c[6] <= alpha_fw for c in cells),
                          top20=[dict(feature=cells[i][0], value=cells[i][1], k=cells[i][2], K=cells[i][3],
                                      n_with_feature=cells[i][4], N=cells[i][5], p=cells[i][6], q=q[i])
                                 for i in top])

# ================================================================ TEST 3: do the L1 leads hold in L2 and in the forces?
def check(names, feature, value):
    feats = [features_of(n['name']) for n in names]; vals = [values_of(n) for n in names]
    has_v = [value in x for x in vals]; K = sum(has_v); has_f = [feature in x for x in feats]; n_ = sum(has_f)
    k = sum(a and b for a, b in zip(has_v, has_f))
    return dict(k=k, K=K, n_with_feature=n_, N=len(names),
                p=fisher_greater(k, K, n_, len(names)) if K and n_ else None)

R['test3_replication_of_top20'] = [dict(feature=cells[i][0], value=cells[i][1],
                                       in_L2=check(L2, cells[i][0], cells[i][1]),
                                       in_forces=check(FO, cells[i][0], cells[i][1]))
                                  for i in top]

# ================================================================ robustness: Codex IV spellings
iv = [dict(n, name=n['name_IV'] or n['name']) for n in MEM]
pairs_iv = [(a, b) for a, b in [(dict(a, name=a['name_IV'] or a['name']), dict(b, name=b['name_IV'] or b['name']))
                                for a, b in pairs]]
test_matched(pairs_iv, 'robust_test0a_codex_IV_spellings')
mantel(iv, 'robust_test1_codex_IV_spellings')

(HERE / 'results.json').write_text(json.dumps(R, ensure_ascii=False, indent=1))
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ('pairs', 'top20')} if isinstance(v, dict) else len(v)
                  for k, v in R.items()}, ensure_ascii=False, indent=1))
