"""Part 3, round 2: blind forced-choice matching of the word-names (plan_003_word_names.md, Amendment).

Round 1 failed its blindness condition: three of four matchers recognised the set of glosses as the
Apocryphon of John. Round 2 removes the set cue. Each word-name gloss is its own four-way question
(its member and three others drawn from all coded members, without sides), and the fourteen target
questions are mixed with 28 decoy questions about ordinary words. Matchers that name the source are
excluded and replaced, in order, by the spare prompts.

  python3 word_match2.py prompts  -> word_match/r2_prompt_<V><k>.txt, r2_key_<V><k>.json (k = 1..4)
  python3 word_match2.py score A1 A2 B1 B2   (the accepted matchers) -> results_word_match_r2.json
"""
import json, math, random, re, sys, pathlib
HERE = pathlib.Path(__file__).parent
WM = HERE / 'word_match'
SEED = 20261110

# every coded member (meaning_table.md), without sides; version-B text from the table, sources removed
MEM = {
 'head': 'holds the brain and the senses and directs the body; corresponds to the celestial; those above the head teach',
 'brain': 'seat of will and understanding, origin of the fibres; corresponds to beginnings and ends, the right hemisphere to the will of good, the left to the understanding',
 'eye': 'sight; "the sight of the eye corresponds to the understanding"; those at the eyes are "intelligent and wise"',
 'ear': 'hearing; corresponds to simple obedience and perceptivity, the right ear to "perceptivity of truth from good"',
 'nose': 'smell and breathing; corresponds to general perception',
 'lips': 'take in food and form speech; of the province of the tongue, the affection of truth',
 'teeth': 'bite and break food; correspond to natural truth: "they grind like a mill, and thus prepare the food"; the lowest natural things',
 'molars': 'grind food; as the teeth, grinding like a mill',
 'tonsils': 'guard the narrows between mouth and throat; a guard at an entrance that rejects or admits',
 'uvula': 'closes the way to the nose in swallowing; a guard at an entrance, as the tonsils',
 'neck': 'joins head to body and carries all that passes between them; the joining of the highest degree with the next',
 'throat': 'passage of food and breath; of the province of the tongue',
 'vertebrae': 'bear the body and enclose the spinal marrow; little life, in comparison with the heart and lungs',
 'shoulder': 'bears loads and moves the arm; "the shoulder corresponds to all power"',
 'elbow': 'joint of the arm; the arms signify strength, the joint a joining',
 'forearm': 'grasping, holding; strength of the arm; palms spread out signify supplication',
 'hands': 'grasping and working; the hands signify power',
 'fingers': 'fine work of the hand; part of the hand and its power',
 'nails of the hands': 'hard outer covering of the fingertips; the outermost covering; those who give praise and blame without understanding',
 'breast': 'gives milk; at the breast are those who are in charity',
 'chest': 'encloses heart and lungs; at the chest are those in charity; the union of heart and lungs',
 'belly': 'holds the organs of digestion; the viscera that prepare nourishment',
 'navel': 'joined the unborn to the mother and its food; the embryo is in the kingdom of the heart',
 'hypochondrium': 'region under the ribs holding liver and spleen; separating and purifying, as the liver',
 'ribs': 'hold and protect the chest; little life, like the vertebrae; a support for the chest',
 'loins': 'seat of generation; correspond to genuine conjugial love',
 'marrow': 'the living interior of the bone, which feeds it; the soft living part enclosed by the frame',
 'bones': 'frame of the whole body; support and hold together all the parts; little spiritual life; remains of good',
 'stomach': 'receives and digests food; agitation "in order that evils may be separated, and goods gathered"',
 'heart': 'drives the blood through the whole body; corresponds to the celestial, which is of good; rules the body by the vessels',
 'lungs': 'breathe; correspond to the spiritual, which is of truth; rule the body by respiration',
 'liver': 'separates and purifies the blood; a guard before the heart',
 'spleen': 'works on the blood',
 'intestines': 'continue digestion and expel waste; the functions of the stomach "more vigorous and harsh"',
 'kidneys': 'filter the blood; they "explore whether there is any useless and hurtful serum" and separate it; the reins signify truth, as the heart good',
 'sinews': 'bind and move the members; binding',
 'spine': 'upright support of the body; little life; those near the back act silently and prudently',
 'veins': 'carry the blood; the vessels by which the heart rules the body',
 'arteries': 'carry the blood from the heart; the vessels by which the heart rules the body',
 'breaths in the members': 'breath distributed through the body; the lungs rule all its parts by respiration',
 'flesh': 'the living substance of the body; "the own of man\'s will made alive"',
 'testicles': 'generation; of the members of generation and conjugial love',
 'genitals': 'generation; correspond to conjugial love and the members allotted to generation',
 'thigh': 'bears the trunk, seat of generation; the thigh signifies conjugial love',
 'knee': 'bends the leg; the conjunction of the truth of faith with the good of love',
 'shin': 'bears the body between knee and foot',
 'ankle': 'joint of foot and leg; the heels are the lowest natural things; a joining',
 'foot': 'stand and walk; those at the feet are the natural; "natural things are like the feet, on which the higher things rest"',
 'toes': 'balance and push off in walking; part of the foot, the natural',
 'toenails': 'hard covering of the toes; the outermost covering of the natural',
 'bosom': 'where a child or a beloved is held; holding what is loved',
}
# the fourteen word-names of the first list (thesis §5.7): gloss -> member; members excluded as distractors
TARGETS = [
 ('meninges', 'brain', ['head']),
 ('star', 'eye', ['breast']),
 ('of sacred name', 'ear', []),
 ('firm, true', 'teeth', ['molars']),
 ('royal', 'tonsils', ['uvula']),
 ('break', 'shoulder', []),
 ('ruler', 'elbow', []),
 ('well-flowering', 'forearm', ['hands']),
 ('judgment', 'nails of the hands', ['toenails', 'fingers']),
 ('star', 'breast', ['eye', 'chest', 'bosom']),
 ('book', 'kidneys', []),
 ('fool', 'kidneys', []),
 ('body', 'genitals', ['testicles', 'loins']),
 ('rough', 'foot', ['toes', 'ankle']),
]
DECOYS = ['anchor', 'salt', 'lamp', 'door', 'iron', 'honey', 'wind', 'seed', 'crown', 'mirror', 'thread', 'ladder',
          'gate', 'oil', 'cloud', 'river', 'stone', 'bell', 'sword', 'cup', 'wheel', 'knot', 'bridge', 'shadow',
          'root', 'wing', 'tower', 'arrow']
INTRO = {
 'A': ("Below are 42 short questions. Each gives a word and four parts of the human body. For each question, "
       "choose the part that the word fits best, as a name for that part."),
 'B': ("Below are 42 short questions. Each gives a word and four parts of the human body; each part is given with "
       "its natural function and the spiritual function that Swedenborg's doctrine of correspondences attributes to it. "
       "For each question, choose the part whose function, natural or spiritual, the word fits best, as a name for that part."),
}
RULES = ("Answer from this message alone. Do not use any tools, do not read files, do not search. Reply with one line per "
         "question, in the form  Q<number> -> <letter> : <reason in at most six words>  and nothing else. After the last "
         "answer add one line beginning SOURCE: that names any text or source these words made you think of, or SOURCE: none")

def prompts():
    WM.mkdir(exist_ok=True)
    names = list(MEM)
    for v in ('A', 'B'):
        for k in (1, 2, 3, 4):
            rng = random.Random(SEED + 100 + 10 * (v == 'B') + k)
            qs = []
            for gloss, mem, excl in TARGETS:
                pool = [m for m in names if m != mem and m not in excl]
                opts = rng.sample(pool, 3) + [mem]; rng.shuffle(opts)
                qs.append(dict(word=gloss, options=opts, target=mem))
            for w in DECOYS:
                qs.append(dict(word=w, options=rng.sample(names, 4), target=None))
            rng.shuffle(qs)
            lines = []
            for i, q in enumerate(qs, 1):
                opt = '  '.join(f'{L}. {o}' + (f' ({MEM[o]})' if v == 'B' else '') for L, o in zip('ABCD', q['options']))
                lines.append(f'Q{i}. "{q["word"]}"  {opt}' if v == 'A' else f'Q{i}. "{q["word"]}"\n   ' + '\n   '.join(
                    f'{L}. {o}: {MEM[o]}' for L, o in zip('ABCD', q['options'])))
            (WM / f'r2_prompt_{v}{k}.txt').write_text(INTRO[v] + '\n\n' + RULES + '\n\n' + '\n'.join(lines) + '\n')
            (WM / f'r2_key_{v}{k}.json').write_text(json.dumps(qs, ensure_ascii=False))
    print('written')

def binom_tail(k, n, p=0.25):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))

def score(accepted):
    R = {}; tot = {'A': [0, 0, 0, 0], 'B': [0, 0, 0, 0]}   # correct, n, correct w/o meninges, n w/o
    for m in accepted:
        v = m[0]; qs = json.loads((WM / f'r2_key_{m}.json').read_text())
        text = (WM / f'r2_response_{m}.txt').read_text()
        ans = {int(a): b for a, b in re.findall(r'Q(\d+)\s*[-–=]+>\s*([A-D])\b', text)}
        rows = []; c = n = c2 = n2 = 0
        for i, q in enumerate(qs, 1):
            if q['target'] is None:
                continue
            got = q['options']['ABCD'.index(ans[i])] if i in ans else None
            ok = got == q['target']; c += ok; n += 1
            if q['word'] != 'meninges':
                c2 += ok; n2 += 1
            rows.append(dict(word=q['word'], member=q['target'], chosen=got, correct=ok))
        src = re.findall(r'(?im)^\s*SOURCE:\s*(.*)$', text)
        R[m] = dict(correct=c, n=n, p_single=round(binom_tail(c, n), 5), source_line=src[-1] if src else None,
                    items=rows)
        t = tot[v]; t[0] += c; t[1] += n; t[2] += c2; t[3] += n2
    for v in ('A', 'B'):
        c, n, c2, n2 = tot[v]
        R[f'version_{v}'] = dict(correct=c, n=n, expected=n / 4, p=round(binom_tail(c, n), 6),
                                 correct_without_meninges=c2, n_without=n2, p_without_meninges=round(binom_tail(c2, n2), 6))
    ps = [R['version_A']['p'], R['version_B']['p']]; o = sorted(range(2), key=lambda i: ps[i]); adj = [0, 0]; mx = 0
    for r, i in enumerate(o):
        mx = max(mx, min(1, (2 - r) * ps[i])); adj[i] = round(mx, 6)
    R['holm'] = dict(A=adj[0], B=adj[1])
    (HERE / 'results_word_match_r2.json').write_text(json.dumps(R, ensure_ascii=False, indent=1))
    print(json.dumps({k: ({kk: vv for kk, vv in x.items() if kk != 'items'} if isinstance(x, dict) else x)
                      for k, x in R.items()}, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    if sys.argv[1] == 'prompts':
        prompts()
    else:
        score(sys.argv[2:])
