"""Origin of each name, from the published readings in the thesis appendix (§14).

Rules (plan_002_origin.md): STRICT = tradition of the grade-A/B reading, else UN.
BROAD = strict, plus the tradition named by a grade-C proposal when it names exactly one
tradition; two traditions, an unattributed magical word, a "probable coincidence" or
"opaque" stay UN. EG = Egyptian god/decan (incl. Coptic), GR = Greek, SE = Semitic.
Output: origin.csv (list, row, name, member, side, strict, broad, basis).
"""
import csv, pathlib
HERE = pathlib.Path(__file__).parent

# name: (strict, broad, basis — the thesis appendix reading, abridged)
O = {
 # ---- first list (thesis §14.2)
 'ⲉⲧⲉⲣⲁⲫⲁⲱⲡⲉⲁⲃⲣⲱⲛ': ('UN', 'EG', 'C: month-name Paophi; a decan or magical ἀβρα- (Quack 114)'),
 'ⲙⲏⲛⲓⲅⲅⲉⲥⲥⲧⲣⲱⲏⲑ': ('GR', 'GR', 'A: μήνιγγ-'),
 'ⲁⲥⲧⲉⲣⲉⲭⲙⲏ': ('GR', 'GR', 'A: ἀστήρ; second element the decan knm.w (Quack 114-115)'),
 'ⲑⲁⲥⲡⲟⲙⲟⲭⲁ': ('UN', 'EG', 'C: decan ṯms n ḫntt, with emendation (Quack 115)'),
 'ⲓⲉⲣⲱⲛⲩⲙⲟⲥ': ('GR', 'GR', 'B: ἱερώνυμος'),
 'ⲃⲓⲥⲥⲟⲩⲙ': ('UN', 'SE', 'C: Hebrew bōśem proposed'),
 'ⲁⲕⲓⲱⲣⲉⲓⲙ': ('UN', 'UN', 'C: opaque'),
 'ⲃⲁⲛⲏⲛⲉⲫⲣⲟⲩⲙ': ('UN', 'SE', 'C: Ephraim proposed for the second name'),
 'ⲁⲙⲏⲛ': ('SE', 'SE', 'A: Hebrew ʾāmēn'),
 'ⲓⲃⲓⲕⲁⲛ': ('UN', 'UN', 'C: opaque'),
 'ⲃⲁⲥⲓⲗⲓⲁⲇⲏⲙⲏ': ('GR', 'GR', 'A: βασιλ-'),
 'ⲁⲭⲭⲁ': ('UN', 'EG', 'C: decan ḫ.wi, Firmicus Acha (Quack 115)'),
 'ⲁⲇⲁⲃⲁⲛ': ('UN', 'SE', 'C: Semitic dbq proposed'),
 'ⲭⲁⲁⲙⲁⲛ': ('UN', 'EG', 'C: decan ḥry-ib rmn, with emendation (Quack 115); "pillar" (no tradition named)'),
 'ⲇⲉⲁⲣⲭⲱ': ('UN', 'UN', 'C: decan tpy-ꜥ ꜥkw OR ἀρχ- (two traditions)'),
 'ⲧⲏⲃⲁⲣ': ('SE', 'SE', 'B: Aramaic tbr; Quack compares decan forms'),
 'ⲙⲛⲓⲁⲣⲭⲱⲛ': ('GR', 'GR', 'B: ἄρχων'),
 'ⲁⲃⲓⲧⲣⲓⲱⲛ': ('UN', 'UN', 'C: opaque'),
 'ⲉⲩⲁⲛⲑⲏⲛ': ('GR', 'GR', 'B: εὐανθής; Quack compares a decan'),
 'ⲕⲣⲩⲥ': ('UN', 'UN', 'C: χρυσός OR decan ρυαξ (two traditions)'),
 'ⲃⲏⲗⲩⲁⲓ': ('UN', 'SE', 'C: Belial proposed'),
 'ⲧⲣⲏⲛⲉⲩ': ('UN', 'UN', 'C: opaque'),
 'ⲃⲁⲗⲃⲏⲗ': ('EG', 'EG', 'B: decan βελβελ (TSol), also magical (Quack 115)'),
 'ⲕⲣⲓⲙⲁ': ('GR', 'GR', 'B: κρίμα; Quack compares decan forms for IV'),
 'ⲁⲥⲧⲣⲱⲯ': ('GR', 'GR', 'B: ἀστρ-; resembles decan Astiro'),
 'ⲃⲁⲣⲣⲱⲫ': ('UN', 'UN', 'C: opaque'),
 'ⲁⲣⲉⲭ': ('UN', 'GR', 'C: ἀρχή proposed'),
 'ⲫⲑⲁⲩⲏ': ('EG', 'EG', 'B: Ptah the great (Quack 116)'),
 'ⲥⲏⲛⲁⲫⲓⲙ': ('UN', 'EG', 'C: decan sbšsn (Quack 116)'),
 'ⲁⲣⲁⲭⲉⲑⲱⲡⲓ': ('UN', 'UN', 'C: opaque'),
 'ⲍⲁⲃⲉⲇⲱ': ('UN', 'UN', 'C: opaque'),
 'ⲃⲁⲣⲓⲁⲥ': ('UN', 'GR', 'C: βάρος proposed'),
 'ⲫⲛⲟⲩⲑ': ('EG', 'EG', 'B: pꜣ nṯr, "the god" (Quack 116)'),
 'ⲁⲃⲏⲛⲗⲉⲛⲁⲣⲭⲉⲓ': ('UN', 'GR', 'C: possibly ἀρχ-'),
 'ⲭⲛⲟⲩⲙⲉⲛⲓⲛⲟⲣⲓⲛ': ('EG', 'EG', 'B: Khnum or the decan Chnoumis'),
 'ⲅⲏⲥⲟⲗⲉ': ('UN', 'EG', 'C: decan sꜣ sꜣḥ from IV (Quack 116)'),
 'ⲁⲅⲣⲟⲙⲁⲩⲙⲁ': ('UN', 'UN', 'C: opaque'),
 'ⲃⲁⲛⲱ': ('UN', 'UN', 'C: opaque'),
 'ⲥⲱⲥⲧⲣⲁⲡⲁⲗ': ('UN', 'UN', 'C: opaque'),
 'ⲁⲛⲏⲥⲓⲙⲁⲗⲁⲣ': ('UN', 'EG', 'C: decan Ἀνεσιούμ (Gundel 80; this study)'),
 'ⲑⲱⲡⲓⲑⲣⲱ': ('UN', 'EG', 'C: two decan names (Quack 116)'),
 'ⲃⲓⲃⲗⲱ': ('GR', 'GR', 'B: βίβλος; Quack emends to magical βιβιου'),
 'ⲣⲟⲉⲣⲱⲣ': ('UN', 'UN', 'C: opaque'),
 'ⲧⲁⲫⲣⲉⲱ': ('UN', 'GR', 'C: τάφρος proposed'),
 'ⲓⲡⲟⲩⲥⲡⲟⲃⲱⲃⲁ': ('UN', 'EG', 'C: decan ip-ꜥ.s (Quack 117)'),
 'ⲃⲓⲛⲉⲃⲟⲣⲓⲛ': ('UN', 'UN', 'C: opaque'),
 'ⲁⲧⲟⲓⲙⲉⲛⲯⲏⲫⲉⲓ': ('UN', 'EG', 'C: pꜣ šfy, "the divine child" (Quack 117)'),
 'ⲏⲛⲑⲟⲗⲗⲉⲓⲁ': ('UN', 'UN', 'C: opaque'),
 'ⲁⲣⲁⲃⲏⲉⲓ': ('UN', 'EG', 'C: decan ḥry-ib wiꜣ (Quack 117)'),
 'ⲉⲓⲗⲱ': ('UN', 'UN', 'C: opaque'),
 'ⲥⲱⲣⲙⲁ': ('GR', 'GR', 'B: σῶμα (IV corrected)'),
 'ⲅⲟⲣⲙⲁⲕⲁⲓⲟⲭⲗⲁⲃⲁⲣ': ('UN', 'EG', 'C: second name perhaps a decan (Quack 117)'),
 'ⲛⲉⲃⲣⲓⲑ': ('UN', 'EG', 'C: nb rḏw (Quack 117)'),
 'ⲁⲥⲁⲕⲗⲁⲥ': ('SE', 'SE', 'A: Saklas (Aramaic, the archon\'s name)'),
 'ⲟⲣⲙⲁⲱⲑ': ('EG', 'EG', 'B: Horus the justified (Quack 117-118)'),
 'ⲏⲙⲏⲛⲩⲛ': ('UN', 'UN', 'C: opaque'),
 'ⲕⲛⲩⲝ': ('UN', 'UN', 'C: opaque'),
 'ⲧⲩⲡⲏⲗⲟ': ('UN', 'UN', 'C: opaque'),
 'ⲁⲭⲓⲏⲗ': ('SE', 'SE', 'B: theophoric -ēl'),
 'ⲫⲛⲏⲙⲏ': ('UN', 'EG', 'C: "the dwarf", title of the sun-god (Quack 118)'),
 'ⲫⲓⲟⲩⲑⲣⲟⲙ': ('UN', 'UN', 'C: opaque'),
 'ⲃⲟⲁⲃⲉⲗ': ('UN', 'SE', 'C: possibly theophoric'),
 'ⲧⲣⲁⲭⲟⲩⲛ': ('GR', 'GR', 'B: τραχύς'),
 'ⲫⲓⲕⲛⲁ': ('UN', 'UN', 'C: magical φνκρω (no tradition named)'),
 'ⲙⲓⲁⲙⲁⲓ': ('UN', 'UN', 'C: opaque'),
 # ---- second list (thesis §14.4)
 'ⲇⲓⲟⲗⲓⲙⲟⲇⲣⲁⲍⲁ': ('UN', 'UN', 'C: opaque'),
 'ⲓⲁⲙⲙⲉⲁⲝ': ('UN', 'UN', 'C: opaque'),
 'ⲓⲁⲕⲟⲩⲓⲃ': ('SE', 'SE', 'A: Jacob'),
 'ⲟⲩⲉⲣⲧⲱⲛ': ('EG', 'EG', 'B: wr-tꜣ, "great one of the earth" (Quack 118)'),
 'ⲟⲩⲇⲓⲇⲓ': ('UN', 'UN', 'C: Hebrew yādîd OR decan οὐδισίτ (two traditions)'),
 'ⲁⲣⲃⲁⲟ': ('SE', 'SE', 'B: Ἀρβαω, Hebrew "fourfold Iao" (Piwowarczyk)'),
 'ⲗⲁⲙⲡⲛⲱ': ('UN', 'UN', 'C: λάμπω OR decan Ἀμπάναν (two traditions)'),
 'ⲗⲏⲉⲕⲁⲫⲁⲣ': ('UN', 'UN', 'C: opaque'),
 'ⲃⲁⲣⲃⲁⲣ': ('UN', 'EG', 'C: magical name; Coptic ⲃⲉⲣⲃⲉⲣ "boil" (Merkelbach-Totti)'),
 'ⲓⲙⲁⲏ': ('UN', 'SE', 'C: Aramaic ʾimmā proposed'),
 'ⲡⲓⲥⲁⲛⲇⲣⲁⲡⲧⲏⲥ': ('UN', 'GR', 'C: possibly a Greek compound'),
 'ⲁⲥⲫⲓⲝⲓⲝ': ('UN', 'UN', 'C: opaque'),
 'ⲥⲩⲛⲟⲅⲭⲟⲩⲧⲁ': ('GR', 'GR', 'B: συνοχή'),
 'ⲁⲣⲟⲩⲫ': ('UN', 'EG', 'C: decan Arfa/Amarph (Gundel 78; this study)'),
 'ⲥⲁⲃⲁⲗⲱ': ('UN', 'SE', 'C: Semitic sbl proposed'),
 'ⲭⲁⲣⲭⲁⲣⲃ': ('UN', 'EG', 'C: decan forms Χαρχαμ, Χαρχνουμις (Gundel 77, 80)'),
 'ⲭⲑⲁⲱⲛ': ('GR', 'GR', 'B: χθών'),
 'ⲃⲁⲑⲓⲛⲱⲑ': ('SE', 'SE', 'B: Hebrew tabnît; Quack emends to an Egyptian reading'),
 'ⲭⲟⲩⲝ': ('EG', 'EG', 'B: Kk.w, primordial darkness (Quack 118)'),
 'ⲭⲁⲣⲭⲁ': ('UN', 'UN', 'C: magical; decan forms; Hebrew kāraʿ (several traditions)'),
 'ⲁⲣⲟⲏⲣ': ('EG', 'EG', 'B: Haroeris (Quack 118)'),
 'ⲧⲱⲉⲭⲑⲁ': ('UN', 'UN', 'C: opaque'),
 'ⲁⲱⲗ': ('UN', 'UN', 'C: opaque'),
 'ⲭⲁⲣⲁⲛⲏⲣ': ('UN', 'UN', 'C: opaque'),
 'ⲃⲁⲥⲧⲁⲛ': ('UN', 'GR', 'C: possibly βαστάζω'),
 'ⲁⲣⲭⲉⲛⲧⲉⲭⲑⲁ': ('EG', 'EG', 'B: Horus of Athribis (Quack 118-119)'),
 'ⲙⲁⲣⲉⲫⲛⲟⲩⲛⲑ': ('UN', 'EG', 'C: pꜣ nṯr, "the god" (Quack 119)'),
 'ⲁⲃⲣⲁⲛⲁ': ('UN', 'UN', 'C: opaque'),
 # ---- forces (thesis §14.5)
 'ⲁⲣⲭⲉⲛⲇⲉⲕⲧⲁ': ('EG', 'EG', 'B: Horus Khentikheti'),
 'ⲇⲉⲓⲑⲁⲣⲃⲁⲑⲁⲥ': ('UN', 'UN', 'C: opaque'),
 'ⲟⲩⲙⲙⲁⲁ': ('GR', 'GR', 'A: ὄμμα'),
 'ⲁⲁⲭⲓⲁⲣⲁⲙ': ('UN', 'UN', 'C: opaque'),
 'ⲣⲓⲁⲣⲁⲙⲛⲁⲭⲱ': ('UN', 'EG', 'C: decan Ρεμεναχ (Gundel 77; this study)'),
 'ⲫⲗⲟⲝⲟⲫⲁ': ('GR', 'GR', 'A: φλόξ'),
 'ⲟⲣⲟⲟⲣⲣⲟⲑⲟⲥ': ('UN', 'GR', 'C: ὀρρωδέω possible'),
 'ⲉⲣⲓⲙⲁⲭⲱ': ('UN', 'GR', 'C: ἐρημ- possible'),
 'ⲁⲑⲩⲣⲱ': ('EG', 'EG', 'A: Hathor'),
 'ⲟⲛⲟⲣⲑⲟⲭⲣⲁⲥⲁⲉⲓ': ('GR', 'GR', 'B: κρᾶσις'),
 'ⲉⲫⲉⲙⲉⲙⲫⲓ': ('UN', 'EG', 'C: Nefertem of Memphis, one letter restored'),
 'ⲓⲱⲕⲱ': ('UN', 'UN', 'C: opaque'),
 'ⲛⲉⲛⲉⲛⲧⲱⲫⲛⲓ': ('UN', 'UN', 'C: opaque'),
 'ⲃⲗⲁⲟⲙⲏⲛ': ('UN', 'UN', 'C: opaque'),
 'ⲉⲥⲑⲏⲛⲥⲓⲥ': ('GR', 'GR', 'A: αἴσθησις'),
 'ⲁⲛⲁⲣⲱ': ('UN', 'UN', 'C: opaque'),
}

rows = list(csv.DictReader(open(HERE / 'names.csv')))
missing = [r['name'] for r in rows if r['name'] not in O]
extra = [k for k in O if k not in {r['name'] for r in rows}]
assert not missing and not extra, (missing, extra)
with open(HERE / 'origin.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['list', 'row', 'name', 'member', 'side', 'strict', 'broad', 'basis'])
    for r in rows:
        s, b, basis = O[r['name']]
        assert s == 'UN' or s == b
        w.writerow([r['list'], r['row'], r['name'], r['member'], r['side'], s, b, basis])
from collections import Counter
for lst in ('L1', 'L2', 'F'):
    sub = [O[r['name']] for r in rows if r['list'] == lst]
    print(lst, 'strict', dict(Counter(s for s, b, _ in sub)), 'broad', dict(Counter(b for s, b, _ in sub)))
