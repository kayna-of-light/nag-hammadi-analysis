"""Build names.csv: every angel name of the two lists and the rulers, attached to its member
(meaning_table.md numbering) and side. Spellings are taken from the tables of
'The Body That Waited for Breath' (Codex II, with Codex IV variants in parentheses)."""
import re, csv, unicodedata, pathlib
import os
# the thesis lives in the companion repository literary-compilation, checked out beside this one
LITCOMP = pathlib.Path(os.environ.get("LITCOMP", pathlib.Path(__file__).resolve().parents[4] / "literary-compilation"))
THESIS = LITCOMP / "data/08_Correspondential_Texts/The Body That Waited for Breath_ The Angelic Anthropogony of the Apocryphon of John Read from the Coptic.md"

# first list: thesis row -> (member id in meaning_table.md, side); None = left out
L1 = {1:(1,'-'),2:(2,'-'),3:(3,'R'),4:(3,'L'),5:(4,'R'),6:(4,'L'),7:(5,'-'),8:(6,'-'),9:(7,'-'),10:(8,'-'),
      11:(9,'-'),12:(10,'-'),13:(11,'-'),14:(13,'-'),15:(12,'-'),16:(14,'R'),18:(15,'R'),20:(16,'R'),21:(16,'L'),
      22:(17,'R'),23:(17,'L'),24:(18,'R'),25:(18,'L'),26:(19,'-'),27:(20,'R'),28:(20,'L'),29:None,30:None,
      31:(22,'-'),32:(23,'-'),33:(24,'-'),34:(25,'R'),35:(25,'L'),36:(26,'R'),37:(26,'L'),38:(27,'-'),39:(28,'-'),
      40:(29,'-'),41:(30,'-'),42:(31,'-'),43:(32,'-'),44:(33,'-'),45:(34,'-'),46:(35,'-'),47:(36,'-'),48:(37,'-'),
      49:(38,'-'),50:(39,'-'),51:(40,'-'),52:(41,'-'),53:None,54:(44,'L'),55:(42,'-'),56:(43,'-'),57:(45,'R'),
      58:(45,'L'),59:None,60:(35,'L'),61:(46,'R'),62:(46,'L'),63:(47,'R'),64:(47,'L'),65:(48,'R'),66:(48,'L'),
      67:(49,'R'),68:(50,'R'),69:(49,'L'),70:(50,'L'),71:(51,'-'),72:None}
# second list: thesis row -> (member id, side)
L2 = {1:(1,'-'),2:(11,'-'),3:(14,'R'),4:(14,'L'),5:(17,'R'),6:(17,'L'),7:(18,'R'),8:(18,'L'),9:(20,'R'),10:(20,'L'),
      11:(21,'-'),12:None,13:None,14:(25,'R'),15:(25,'L'),16:(22,'-'),17:(52,'-'),18:(45,'R'),19:(45,'L'),20:(43,'-'),
      21:(46,'R'),22:(46,'L'),23:(47,'R'),24:(47,'L'),25:(48,'R'),26:(48,'L'),27:(49,'R'),28:(50,'R'),29:(49,'L'),30:(50,'L')}
# rulers (forces table, meaning_table.md section 4)
FORCES = [('F1','ⲁⲣⲭⲉⲛⲇⲉⲕⲧⲁ'),('F2','ⲇⲉⲓⲑⲁⲣⲃⲁⲑⲁⲥ'),('F3','ⲟⲩⲙⲙⲁⲁ'),('F4','ⲁⲁⲭⲓⲁⲣⲁⲙ'),('F5','ⲣⲓⲁⲣⲁⲙⲛⲁⲭⲱ'),
          ('F6','ⲫⲗⲟⲝⲟⲫⲁ'),('F7','ⲟⲣⲟⲟⲣⲣⲟⲑⲟⲥ'),('F8','ⲉⲣⲓⲙⲁⲭⲱ'),('F9','ⲁⲑⲩⲣⲱ'),('F10','ⲟⲛⲟⲣⲑⲟⲭⲣⲁⲥⲁⲉⲓ'),
          ('F11','ⲉⲫⲉⲙⲉⲙⲫⲓ'),('F11','ⲓⲱⲕⲱ'),('F11','ⲛⲉⲛⲉⲛⲧⲱⲫⲛⲓ'),('F11','ⲃⲗⲁⲟⲙⲏⲛ'),('F12','ⲉⲥⲑⲏⲛⲥⲓⲥ'),('F13','ⲁⲛⲁⲣⲱ')]
EGYPTIAN = {'ⲫⲑⲁⲩⲏ','ⲫⲛⲟⲩⲑ','ⲭⲛⲟⲩⲙⲉⲛⲓⲛⲟⲣⲓⲛ','ⲟⲣⲙⲁⲱⲑ','ⲃⲁⲗⲃⲏⲗ','ⲁⲣⲟⲏⲣ','ⲟⲩⲉⲣⲧⲱⲛ','ⲭⲟⲩⲝ','ⲁⲣⲭⲉⲛⲧⲉⲭⲑⲁ',
            'ⲁⲣⲭⲉⲛⲇⲉⲕⲧⲁ','ⲁⲑⲩⲣⲱ','ⲁⲭⲭⲁ','ⲯⲏⲣⲏⲙ','ⲁⲣⲁⲃⲏⲉⲓ','ⲉⲫⲉⲙⲉⲙⲫⲓ','ⲙⲁⲣⲉⲫⲛⲟⲩⲛⲑ','ⲃⲁⲑⲓⲛⲱⲑ','ⲃⲓⲃⲗⲱ'}

def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^Ⲁ-⳿Ϣ-ϯ]', '', s)

def rows(section_start, section_end, name_col):
    t = THESIS.read_text()
    blk = t[t.index(section_start):t.index(section_end)]
    out = {}
    for l in blk.split('\n'):
        c = [x.strip() for x in l.split('|')]
        if len(c) > 5 and re.fullmatch(r'\d+(–\d+)?', c[1]):
            out[c[1]] = c[name_col]
    return out

def split_name(cell):
    """'ⲕⲣⲓⲙⲁ (IV ⲕⲣⲓⲙⲁⲛ)' -> ('ⲕⲣⲓⲙⲁ','ⲕⲣⲓⲙⲁⲛ'); pair cells 'A; B (IV)' handled by caller."""
    iv = re.search(r'\(IV ([^)]*)\)', cell)
    main = re.sub(r'\([^)]*\)', '', cell)
    return norm(main), (norm(iv.group(1)) if iv else '')

recs = []
r1 = rows('### 5.3', '## 6.', 2)
for key, cell in r1.items():
    if '–' in key:   # paired rows 16–17, 18–19, 36–37
        a, b = [int(x) for x in key.split('–')]
        parts = [p.strip() for p in cell.split(';')]
        for num, part in zip((a, b), parts):
            if L1.get(num) is None or 'lost' in part or part.startswith('[') or part.startswith('['):
                continue
            nm, iv = split_name(part)
            if num == 37: nm, iv = '', nm          # Phnouth survives in Codex IV only
            if num == 18: iv = 'ⲙⲛⲓⲁⲭⲱⲣ'
            if not (nm or iv) or nm == 'ⲉ': continue
            m, side = L1[num]
            recs.append(dict(list='L1', row=num, name_II=nm, name_IV=iv, member=m, side=side))
        continue
    num = int(key)
    if L1.get(num) is None: continue
    nm, iv = split_name(cell)
    if num == 56: iv = 'ⲥⲟⲙⲁ'              # IV ⲥⲟ{ⲣ}ⲙⲁ: the scribe struck out the ⲣ
    m, side = L1[num]
    recs.append(dict(list='L1', row=num, name_II=nm, name_IV=iv, member=m, side=side))
r2 = rows('## 7.', '## 8.', 3)
for key, cell in r2.items():
    num = int(key)
    if L2.get(num) is None: continue
    nm, iv = split_name(cell)
    m, side = L2[num]
    recs.append(dict(list='L2', row=num, name_II=nm, name_IV=iv, member=m, side=side))
for f, nm in FORCES:
    recs.append(dict(list='F', row=f, name_II=nm, name_IV='', member=f, side='-'))
for r in recs:
    key = r['name_II'] or r['name_IV']
    r['name'] = key
    r['egyptian'] = int(key in EGYPTIAN)
with open(pathlib.Path(__file__).parent / 'names.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['list','row','name','name_II','name_IV','member','side','egyptian'])
    w.writeheader(); w.writerows(recs)
print(len(recs), 'names;', sum(r['list']=='L1' for r in recs), 'L1,', sum(r['list']=='L2' for r in recs), 'L2,',
      sum(r['list']=='F' for r in recs), 'forces')
