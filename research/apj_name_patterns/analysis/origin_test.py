"""Part 2: origin of the names x meaning of the members (plan_002_origin.md).

Inputs: names.csv and meaning_table.md through the parsing code of analysis.py (executed up to
its first test, so the coding is identical), and origin.csv (build_origin.py).
Output: results_origin.json.  Run: python3 origin_test.py
"""
import csv, json, math, random, pathlib
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).parent
src = (HERE / 'analysis.py').read_text()
head = src.split('\nrng = random.Random(SEED)')[0]
G = {'__file__': str(HERE / 'analysis.py')}
exec(head, G)                                   # defines NAMES, M, logC, fisher_greater, ...
NAMES, SEED, NPERM = G['NAMES'], G['SEED'], G['NPERM']

ORI = {r['name']: r for r in csv.DictReader(open(HERE / 'origin.csv'))}
raw = {r['name']: r['name'] for r in csv.DictReader(open(HERE / 'names.csv'))}
norm = G['norm']
key = {norm(k): k for k in raw}
for n in NAMES:
    o = ORI[key[n['name']]]
    n['strict'], n['broad'] = o['strict'], o['broad']

MEMBERS = [n for n in NAMES if n['list'] in ('L1', 'L2')]
FORCES = [n for n in NAMES if n['list'] == 'F']
rng = random.Random(SEED)
R = {}

def side(n):
    return n['side'] if n['side'] in ('R', 'L') else ''

VARS = {'degree': lambda n: n['degree'] if n['degree'] in ('C', 'S', 'N', '–') else '',
        'side': side,
        'role': lambda n: n['role']}

# ---------------------------------------------------------------- permutation machinery
def strata(names, blocks):
    """Index groups within which labels are shuffled: each list, or blocks of 5 rows of each list."""
    by = defaultdict(list)
    for i, n in enumerate(names):
        by[n['list']].append(i)
    groups = []
    for lst, idx in by.items():
        idx = sorted(idx, key=lambda i: (int(names[i]['row'][1:]) if names[i]['row'].startswith('F')
                                         else int(names[i]['row'])))
        if blocks:
            groups += [idx[k:k + 5] for k in range(0, len(idx), 5)]
        else:
            groups.append(idx)
    return groups

def shuffled(labels, groups):
    out = labels[:]
    for g in groups:
        vals = [labels[i] for i in g]; rng.shuffle(vals)
        for i, v in zip(g, vals):
            out[i] = v
    return out

def chi2(xs, ys):
    t = Counter(zip(xs, ys)); rx = Counter(xs); cy = Counter(ys); N = len(xs)
    return sum((t[(a, b)] - rx[a] * cy[b] / N) ** 2 / (rx[a] * cy[b] / N) for a in rx for b in cy)

def table(xs, ys):
    rows = sorted(set(xs)); cols = sorted(set(ys)); t = Counter(zip(xs, ys))
    return {r: {c: t[(r, c)] for c in cols} for r in rows}

def perm_p(stat, labels, other, groups, nperm=NPERM):
    obs = stat(labels, other)
    ge = sum(stat(shuffled(labels, groups), other) >= obs - 1e-12 for _ in range(nperm))
    return obs, (1 + ge) / (1 + nperm)

def o1_stat(lab, deg):
    eg = [d == 'N' for l, d in zip(lab, deg) if l == 'EG']
    ot = [d == 'N' for l, d in zip(lab, deg) if l != 'EG']
    return (sum(eg) / len(eg) if eg else 0) - (sum(ot) / len(ot) if ot else 0)

def run(names, coding, label):
    out = {}
    deg = [VARS['degree'](n) for n in names]
    lab = [n[coding] for n in names]
    keep = [i for i, d in enumerate(deg) if d]
    sub = [names[i] for i in keep]; L = [lab[i] for i in keep]; D = [deg[i] for i in keep]
    egN = sum(1 for l, d in zip(L, D) if l == 'EG' and d == 'N'); egK = L.count('EG')
    otN = sum(1 for l, d in zip(L, D) if l != 'EG' and d == 'N'); otK = len(L) - egK
    o1 = dict(eg_on_N=f'{egN}/{egK}', others_on_N=f'{otN}/{otK}', diff=round(o1_stat(L, D), 4))
    for nm, bl in (('p_within_list', False), ('p_within_blocks_of_5', True)):
        o1[nm] = round(perm_p(o1_stat, L, D, strata(sub, bl))[1], 4)
    # detection floor: smallest number of EG names on N giving one-sided hypergeometric p < 0.05
    Ntot, Nn = len(L), D.count('N')
    o1['floor_k_of_K'] = next((f'{k}/{egK}' for k in range(egK + 1)
                               if G['fisher_greater'](k, Nn, egK, Ntot) < 0.05), None)
    out['O1_egypt_on_natural'] = o1
    for var in ('degree', 'side', 'role'):
        v = [VARS[var](n) for n in names]
        keep = [i for i, x in enumerate(v) if x]
        sub = [names[i] for i in keep]; L = [lab[i] for i in keep]; V = [v[i] for i in keep]
        res = dict(n=len(sub), table=table(L, V))
        for nm, bl in (('p_within_list', False), ('p_within_blocks_of_5', True)):
            obs, p = perm_p(chi2, L, V, strata(sub, bl))
            res['chi2'] = round(obs, 3); res[nm] = round(p, 4)
        out[f'origin_x_{var}'] = res
    R[label] = out

def holm(ps):
    m = len(ps); order = sorted(range(m), key=lambda i: ps[i]); adj = [0] * m; run_max = 0
    for rank, i in enumerate(order):
        run_max = max(run_max, min(1, (m - rank) * ps[i])); adj[i] = round(run_max, 4)
    return adj

run(MEMBERS, 'strict', 'members_strict')
run(MEMBERS, 'broad', 'members_broad')
run(MEMBERS + FORCES, 'strict', 'members_and_forces_strict')
run(MEMBERS + FORCES, 'broad', 'members_and_forces_broad')

for lab in ('members_strict', 'members_broad'):
    r = R[lab]
    for nm in ('p_within_list', 'p_within_blocks_of_5'):
        ps = [r['O1_egypt_on_natural'][nm]] + [r[f'origin_x_{v}'][nm] for v in ('degree', 'side', 'role')]
        r[f'holm_O1_O4_{nm}'] = dict(zip(['O1', 'O2_degree', 'O3_side', 'O4_role'], holm(ps)))

R['O5_origin_by_list'] = {c: {lst: dict(Counter(n[c] for n in NAMES if n['list'] == lst))
                              for lst in ('L1', 'L2', 'F')} for c in ('strict', 'broad')}

(HERE / 'results_origin.json').write_text(json.dumps(R, ensure_ascii=False, indent=1))
print(json.dumps(R, ensure_ascii=False, indent=1))
