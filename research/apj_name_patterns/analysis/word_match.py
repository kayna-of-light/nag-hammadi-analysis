"""Part 3: are the readable word-names apt to their members beyond chance? (plan_003_word_names.md)

Blind one-to-one matching. Each matcher sees only the meanings of the word-names (the glosses of
the thesis, §5.7 and §14.4) and the members, both in shuffled order, and pairs them. The score is
the number of glosses placed on their own member; the two "star" glosses (right eye, right breast)
and the two kidney glosses ("book", "fool": kidneys, left kidney) count within their pair, since
their members cannot be told apart otherwise. Null: random one-to-one assignments, scored the same.

  python3 word_match.py prompts   -> word_match/prompt_<V><k>.txt and word_match/key_<V><k>.json
  python3 word_match.py score     -> reads word_match/response_<V><k>.txt, writes ../analysis/results_word_match.json
"""
import json, random, re, sys, pathlib
HERE = pathlib.Path(__file__).parent
WM = HERE / 'word_match'
SEED = 20261110

# first list (thesis §5.7): gloss, member, group of interchangeable members
L1 = [
 ('meninges', 'brain', None),
 ('star', 'right eye', 'STAR'),
 ('of sacred name', 'right ear', None),
 ('firm, true', 'teeth', None),
 ('royal', 'tonsils', None),
 ('break', 'right shoulder', None),
 ('ruler', 'right elbow', None),
 ('well-flowering', 'left forearm', None),
 ('judgment', 'nails of the hands', None),
 ('star', 'right breast', 'STAR'),
 ('book', 'kidneys', 'KIDNEY'),
 ('fool', 'left kidney', 'KIDNEY'),
 ('body', 'genitals', None),
 ('rough', 'left foot', None),
]
# second list (thesis §14.4), secondary
L2 = [
 ('Jacob (the patriarch)', 'right shoulder', None),
 ('holding together', 'left ribs', None),
 ('earth', 'left thigh', None),
 ('pattern, form', 'all the genitals', None),
]
# version B: natural function and spiritual counterpart, from meaning_table.md (frozen), sources removed
DESC = {
 'brain': 'seat of will and understanding, origin of the fibres; corresponds to beginnings and ends, the right hemisphere to the will of good, the left to the understanding',
 'right eye': 'sight; "the sight of the eye corresponds to the understanding"; those at the eyes are "intelligent and wise"',
 'right ear': 'hearing; corresponds to simple obedience and perceptivity; the right ear to "perceptivity of truth from good"',
 'teeth': 'bite and break food; correspond to natural truth: "they grind like a mill, and thus prepare the food"; the lowest natural things',
 'tonsils': 'guard the narrows between mouth and throat; a guard at an entrance that rejects or admits',
 'right shoulder': 'bears loads and moves the arm; "the shoulder corresponds to all power"',
 'right elbow': 'joint of the arm; the arms signify strength, the joint a joining',
 'left forearm': 'grasping, holding; strength of the arm; palms spread out signify supplication',
 'nails of the hands': 'hard outer covering of the fingertips; the outermost covering; those who give praise and blame without understanding',
 'right breast': 'gives milk; at the breast are those who are in charity',
 'kidneys': 'filter the blood; they "explore whether there is any useless and hurtful serum" and separate it; the reins signify truth, as the heart good',
 'left kidney': 'filters the blood; explores whether there is any useless and hurtful serum and separates it; the reins signify truth',
 'genitals': 'generation; correspond to conjugial love and the members allotted to generation',
 'left foot': 'stand and walk; those at the feet are the natural; "natural things are like the feet, on which the higher things rest"',
 'left ribs': 'hold and protect the chest; little life, like the vertebrae; a support for the chest',
 'left thigh': 'bears the trunk, seat of generation; the thigh signifies conjugial love',
 'all the genitals': 'generation; correspond to conjugial love and the members allotted to generation',
}

INTRO = {
 'A': ("Below are two lists. List 1 gives the meanings of names that an ancient text gives to parts of the human body, "
       "one name per part. List 2 gives the parts of the body. Each meaning belongs to exactly one part. "
       "Pair them one to one: for every meaning, choose the part it fits best. Use every part exactly once."),
 'B': ("Below are two lists. List 1 gives the meanings of names that an ancient text gives to parts of the human body, "
       "one name per part. List 2 gives the parts of the body, each with its natural function and the spiritual "
       "function that Swedenborg's doctrine of correspondences (the 'Grand Man') attributes to it. Each meaning belongs "
       "to exactly one part. Pair them one to one: for every meaning, choose the part whose function, natural or spiritual, "
       "it fits best. Use every part exactly once."),
}
RULES = ("Answer from this message alone. Do not use any tools, do not read files, do not search. "
         "Reply with one line per meaning, in the form  G<number> -> <letter> : <reason in at most ten words>  "
         "and nothing else, first for Task 1, then for Task 2.")

def block(items, version, rng):
    g = list(range(len(items))); m = list(range(len(items)))
    rng.shuffle(g); rng.shuffle(m)
    glines = [f'G{i + 1}. {items[j][0]}' for i, j in enumerate(g)]
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if version == 'A':
        mlines = [f'{letters[i]}. {items[j][1]}' for i, j in enumerate(m)]
    else:
        mlines = [f'{letters[i]}. {items[j][1]}: {DESC[items[j][1]]}' for i, j in enumerate(m)]
    key = dict(gloss_order=g, member_order=m)
    return glines, mlines, key

def prompts():
    WM.mkdir(exist_ok=True)
    rng = random.Random(SEED)
    for v in ('A', 'B'):
        for k in (1, 2):
            g1, m1, k1 = block(L1, v, rng)
            g2, m2, k2 = block(L2, v, rng)
            text = (INTRO[v] + '\n\n' + RULES + '\n\nTask 1\n\nList 1 (meanings)\n' + '\n'.join(g1) +
                    '\n\nList 2 (parts)\n' + '\n'.join(m1) + '\n\nTask 2\n\nList 1 (meanings)\n' + '\n'.join(g2) +
                    '\n\nList 2 (parts)\n' + '\n'.join(m2) + '\n')
            (WM / f'prompt_{v}{k}.txt').write_text(text)
            (WM / f'key_{v}{k}.json').write_text(json.dumps(dict(task1=k1, task2=k2)))
    print('written', sorted(p.name for p in WM.iterdir()))

def score_assign(items, assign):
    """assign[i] = index of the member chosen for gloss i (item indices)."""
    s = 0
    for i, j in enumerate(assign):
        gi, mi, grp = items[i]; gj, mj, grpj = items[j]
        s += (i == j) or (grp is not None and grp == grpj)
    return s

def parse(text, key, items, task):
    """Map 'G<n> -> <letter>' lines of one task back to item indices."""
    # answers come in order: the first len(L1) lines are Task 1, the rest Task 2
    # (a "Task 2" heading is not required; matchers did not always write one)
    allpairs = re.findall(r'G(\d+)\s*[-–=]+>\s*([A-Z])\b', text)
    pairs = allpairs[:len(L1)] if task == 1 else allpairs[len(L1):]
    g, m = key['gloss_order'], key['member_order']
    assign = [None] * len(items)
    for gn, letter in pairs:
        gi = g[int(gn) - 1]; mi = m['ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(letter)]
        assign[gi] = mi
    return assign

def null_dist(items, nsim=200000, k=2, rng=None, exclude=None):
    rng = rng or random.Random(SEED + 7); idx = [i for i in range(len(items)) if i != exclude]
    out = []
    for _ in range(nsim):
        t = 0
        for _ in range(k):
            p = idx[:]; rng.shuffle(p)
            a = [None] * len(items)
            for i, j in zip(idx, p): a[i] = j
            t += sum(1 for i in idx if (a[i] == i) or (items[i][2] is not None and items[i][2] == items[a[i]][2]))
        out.append(t)
    return out

def score():
    R = {}
    for task, items, name in ((1, L1, 'first_list'), (2, L2, 'second_list')):
        for v in ('A', 'B'):
            per = []
            for k in (1, 2):
                key = json.loads((WM / f'key_{v}{k}.json').read_text())[f'task{task}']
                text = (WM / f'response_{v}{k}.txt').read_text()
                a = parse(text, key, items, task)
                ok = all(x is not None for x in a) and len(set(a)) == len(a)
                hits = [items[i][0] + ' -> ' + items[j][1] for i, j in enumerate(a)
                        if j is not None and ((i == j) or (items[i][2] is not None and items[i][2] == items[j][2]))]
                sc = score_assign(items, a) if ok else None
                sc_ex = (sum(1 for i, j in enumerate(a) if i != 0 and ((i == j) or (items[i][2] is not None and items[i][2] == items[j][2])))
                         if ok and task == 1 else None)
                per.append(dict(matcher=f'{v}{k}', valid_one_to_one=ok, correct=sc, correct_without_meninges=sc_ex,
                                correct_pairs=hits, assignment={items[i][0] + f' [{i}]': (items[j][1] if j is not None else None)
                                                                for i, j in enumerate(a)}))
            tot = sum(p['correct'] for p in per if p['correct'] is not None)
            null = null_dist(items)
            p = (1 + sum(x >= tot for x in null)) / (1 + len(null))
            crit = next(t for t in range(0, 2 * len(items) + 1) if (sum(x >= t for x in null) / len(null)) < 0.05)
            res = dict(matchers=per, total_correct=tot, null_mean=round(sum(null) / len(null), 3), p=round(p, 5),
                       total_needed_for_p_below_0_05=crit)
            if task == 1:
                tot_ex = sum(p['correct_without_meninges'] for p in per if p['correct_without_meninges'] is not None)
                null_ex = null_dist(items, exclude=0)
                res['total_correct_without_meninges'] = tot_ex
                res['p_without_meninges'] = round((1 + sum(x >= tot_ex for x in null_ex)) / (1 + len(null_ex)), 5)
            agree = sum(1 for x, y in zip(per[0]['assignment'].values(), per[1]['assignment'].values()) if x == y)
            res['agreement_between_matchers'] = f'{agree}/{len(items)}'
            R[f'{name}_{v}'] = res
    # Holm over the two primary tests (first list, versions A and B)
    ps = [R['first_list_A']['p'], R['first_list_B']['p']]
    o = sorted(range(2), key=lambda i: ps[i]); adj = [0, 0]; mx = 0
    for r, i in enumerate(o):
        mx = max(mx, min(1, (2 - r) * ps[i])); adj[i] = round(mx, 5)
    R['holm_first_list'] = dict(A=adj[0], B=adj[1])
    (HERE / 'results_word_match.json').write_text(json.dumps(R, ensure_ascii=False, indent=1))
    print(json.dumps(R, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    {'prompts': prompts, 'score': score}[sys.argv[1]]()
