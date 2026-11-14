# Synthesis 001 — First run: no sound–meaning code is detectable in the names

**Run**: 2026-11-10. Design frozen before any result in commit `61323ec` ("Freeze meaning table and add analysis scripts (before any result)"): `meaning_table.md` (52 members, 13 forces), `analysis/build_names.py` → `analysis/names.csv` (109 names: 65 of the first list, 28 of the second, 16 forces), `analysis/analysis.py` (seed 20261110, 10,000 permutations) → `analysis/results.json`. Plan items that `analysis.py` did not carry out were run afterwards in `analysis/supplement.py` → `analysis/results_supplement.json` (see "Departures from the plan" below).

**Verdict by the registered criteria (`plan.md`, "What counts as a result")**: **Miss.** Tests 0 and 1 are at chance after every control. No rule found in the first list holds in the second. In the words fixed in advance: with about ninety names this shows that no strong system is present; a weak one would not be detectable.

---

## 1. What was asked

The author's claim is that the names identify spiritual communities: each name is the identifier of the society that corresponds to its member in the Grand Man. If the names were composed from a key, members whose spiritual meanings are related should carry related names. The study fixed only the meanings (degree in successive order, layer in simultaneous order, polarity, use, role in the series end–cause–effect, each derived from the member's function as Swedenborg derives it, *AC* §4223) and left open which parts of the names, if any, carry them. Every letter, every sequence of two and three letters, and every first and last letter was a candidate.

## 2. Results

### 2.1 Test 0 — Does the same member get similar names in the two lists?

| Test | Pairs | Mean similarity, true pairs | Mean, permuted | p (10,000 perm.) | Median rank of the true partner (expected) |
|---|---|---|---|---|---|
| 0a. Maker (first list) vs mover (second list) of the same member | 25 | 0.0275 | 0.0171 | 0.070 | 12 (13) |
| 0a with Codex IV spellings | 25 | 0.0242 | 0.0171 | 0.136 | 12 (13) |
| 0b. Right vs left name of the same member | 25 | 0.0158 | 0.0181 | 0.558 | 10 (13) |

Similarity is the Jaccard index over the names' two- and three-letter sequences, with the beginning and end of the name marked. Sixteen of the twenty-five same-member pairs share no sequence at all. The slight excess in Test 0a comes from four pairs, and the sequences they share are among the commonest in the corpus:

| Member | First list | Second list | Shared | Similarity |
|---|---|---|---|---|
| Belly | ⲁⲣⲉⲭ | ⲁⲣⲟⲩⲫ | initial ⲁⲣ- | 0.176 |
| Left toes | ⲫⲓⲕⲛⲁ | ⲁⲃⲣⲁⲛⲁ | final -ⲛⲁ | 0.143 |
| Right ankle | ⲁⲭⲓⲏⲗ | ⲁⲱⲗ | initial ⲁ-, final -ⲗ | 0.125 |
| Left foot | ⲧⲣⲁⲭⲟⲩⲛ | ⲙⲁⲣⲉⲫⲛⲟⲩⲛⲑ | ⲟⲩⲛ | 0.091 |

Three of the four are the last members of both lists. The true partner is not, as a rule, the closest name: its median rank is 12 of 25, where chance gives 13. Test 0 does not pass (p = 0.070 with Codex II spellings, 0.136 with Codex IV).

### 2.2 Test 1 — Do names of members with related meanings sound alike?

Mantel test of meaning similarity against sound similarity over all pairs of names, permuting names over members.

| Set | Names | Pairs | r | p | Partial r (list distance) | p |
|---|---|---|---|---|---|---|
| Both lists | 93 | 4,278 | 0.016 | 0.204 | 0.012 | 0.255 |
| Both lists, same-member pairs excluded | 93 | 4,206 | 0.012 | 0.265 | 0.009 | 0.309 |
| First list only | 65 | 2,080 | −0.004 | 0.546 | −0.016 | 0.738 |
| Without the names identified as Egyptian | 79 | 3,081 | 0.016 | 0.231 | 0.009 | 0.335 |
| Codex IV spellings | 93 | 4,278 | 0.017 | 0.189 | 0.011 | 0.278 |
| Both lists, sound residualised on length | 93 | 4,278 | 0.016 | 0.208 | 0.012 (length and distance) | 0.261 |
| First list, sound residualised on length | 65 | 2,080 | 0.004 | 0.419 | −0.009 (length and distance) | 0.632 |

The structure is visible in the meaning matrix: members near each other in the list share meaning (r = −0.28 between meaning similarity and list distance), as the head-to-foot order requires. The sounds do not follow: sound similarity is unrelated to list distance (r = −0.01) and to meaning (r = 0.02). Length does not drive the measure (r = 0.01 between sound similarity and the pair's summed log length; 0.06 in the first list alone).

### 2.3 Test 2 — The grid

Every sequence of one to three letters found in at least three names of the first list (108 pieces), crossed with every coded value held by at least three of its members (22 values): 2,376 cells, each a one-sided Fisher test of whether the piece is concentrated in names whose member has the value.

| Correction | Threshold | Cells below |
|---|---|---|
| Benjamini–Hochberg, q < 0.10 | — | 0 |
| Familywise, permutation of names over members (1,000) | p ≤ 0.000137 | 0 |
| Familywise, permutation within blocks of five neighbouring rows (1,000) | p ≤ 0.000186 | 0 |

The lowest cell is p = 0.0008. The leading cells are runs of neighbouring names, the pattern Control 1 of the plan was written for:

| Piece | Value | Names | Rows |
|---|---|---|---|
| ⲙ | use PERCEPTION, 6 of 6 | ⲁⲥⲧⲉⲣⲉⲭⲙⲏ, ⲑⲁⲥⲡⲟⲙⲟⲭⲁ, ⲓⲉⲣⲱⲛⲩⲙⲟⲥ, ⲃⲓⲥⲥⲟⲩⲙ, ⲁⲕⲓⲱⲣⲉⲓⲙ, ⲃⲁⲛⲏⲛⲉⲫⲣⲟⲩⲙ | 3–8, consecutive; ⲙ is in 24 of the 65 names |
| ⲣⲙⲁ | use CONJUGIAL, 3 of 9 | ⲥⲱⲣⲙⲁ, ⲅⲟⲣⲙⲁⲕⲁⲓⲟⲭⲗⲁⲃⲁⲣ, ⲟⲣⲙⲁⲱⲑ | 56, 57, 61; ⲟⲣⲙⲁⲱⲑ is "Horus the justified" (Quack 1995) |
| ⲉⲛ | degree "all degrees", 3 of 7 | ⲁⲃⲏⲛⲗⲉⲛⲁⲣⲭⲉⲓ, ⲭⲛⲟⲩⲙⲉⲛⲓⲛⲟⲣⲓⲛ, ⲁⲧⲟⲓⲙⲉⲛⲯⲏⲫⲉⲓ | 38, 39, 51; ⲭⲛⲟⲩⲙ- is Khnum or the decan Chnoumis |

### 2.4 Test 3 — Do the first-list leads hold elsewhere?

None of the twenty leading cells replicates. Fifteen cannot be checked in the second list at all, because no second-list member carries the value (the second list has no organ of sense, nothing of the "all degrees" systems, no will or understanding side) or no second-list name carries the piece. The five that can be checked give p = 0.33 to 1.0. Ten can be checked in the forces and give p = 0.21 to 1.0.

### 2.5 The three contrasts of Test 1, each as its own family

| Contrast | Names (first list) | Cells | Familywise threshold | Cells below | Best cell | In the second list |
|---|---|---|---|---|---|---|
| Right vs left (*AC* §10061) | 32 | 98 | 0.0034 | **1** | ⲣ in right-side names: 13 of 16 (17 of the 32 names carry ⲣ), p = 0.0019; familywise p = 0.018 (10,000 perm.); q = 0.19 | right-side names 4 of 11 (11 of 22 carry ⲣ), p = 0.96 |
| Will side (heart, vessels, flesh) vs understanding side (lungs, breaths, kidneys) | 8 | 26 | 0.014 | 0 | p = 0.071 | — |
| The three degrees C/S/N | 58 | 288 | 0.0016 | 0 | ⲏⲗ in natural-degree names, 4 of 18, p = 0.0072 | 0 of 26 natural-degree names (second list and forces) |

**The right/left lead.** In the first list the letter ⲣ marks the right-side name. Of the fourteen members whose right and left names both survive, the right name alone has ⲣ in eight, the left alone in none, both in three, neither in three:

| Member | Right | Left |
|---|---|---|
| Eyes | ⲁⲥⲧⲉⲣⲉⲭⲙⲏ | ⲑⲁⲥⲡⲟⲙⲟⲭⲁ |
| Ears | ⲓⲉⲣⲱⲛⲩⲙⲟⲥ | ⲃⲓⲥⲥⲟⲩⲙ |
| Forearm/palm | ⲁⲃⲓⲧⲣⲓⲱⲛ | ⲉⲩⲁⲛⲑⲏⲛ |
| Hands | ⲕⲣⲩⲥ | ⲃⲏⲗⲩⲁⲓ |
| Fingers | ⲧⲣⲏⲛⲉⲩ | ⲃⲁⲗⲃⲏⲗ |
| Ribs | ⲁⲣⲁⲭⲉⲑⲱⲡⲓ | ⲍⲁⲃⲉⲇⲱ |
| Loins | ⲃⲁⲣⲓⲁⲥ | ⲫⲛⲟⲩⲑ |
| Knees | ⲟⲣⲙⲁⲱⲑ | ⲏⲙⲏⲛⲩⲛ |
| *both* — breasts, thighs, feet | ⲁⲥⲧⲣⲱⲯ, ⲅⲟⲣⲙⲁⲕⲁⲓⲟⲭⲗⲁⲃⲁⲣ, ⲫⲓⲟⲩⲑⲣⲟⲙ | ⲃⲁⲣⲣⲱⲫ, ⲛⲉⲃⲣⲓⲑ, ⲧⲣⲁⲭⲟⲩⲛ |
| *neither* — shins, ankles, toes | ⲕⲛⲩⲝ, ⲁⲭⲓⲏⲗ, ⲃⲟⲁⲃⲉⲗ | ⲧⲩⲡⲏⲗⲟ, ⲫⲛⲏⲙⲏ, ⲫⲓⲕⲛⲁ |

Eight to none is an exact sign-test probability of 0.0039 one-sided. Three names differ in side between the codices: Tebar, Mniarchōn and Barias are right in Codex IV and left in Codex II, which lost one entry of each of these pairs when the scribe's eye leapt from one occurrence of the member to the next (thesis §5.2). Tebar and Mniarchōn have no surviving partner and are not among the fourteen. The loins pair (Barias right, Phnouth left) exists only in Codex IV, which alone preserves Phnouth; without it the count is seven to none (p = 0.0078). In the second list the pattern reverses: of its eleven complete pairs, the right name alone has ⲣ in three, the left alone in six (ⲟⲩⲉⲣⲧⲱⲛ, ⲁⲣⲃⲁⲟ, ⲗⲏⲉⲕⲁⲫⲁⲣ, ⲭⲁⲣⲭⲁ, ⲭⲁⲣⲁⲛⲏⲣ, ⲙⲁⲣⲉⲫⲛⲟⲩⲛⲑ on the left). Taken together, 11 to 6 (one-sided p = 0.17). By the plan's rule this is a pattern of the first list that does not carry over, and it is reported as not validated, not as a finding. No other data can test it: the forces have no sides, and the Codex IV spellings are a second copy of the same lists, not an independent sample.

### 2.6 What the grid could have seen

For each coded value, the smallest number of names that a piece occurring *only* in that class would have to appear in to pass the familywise threshold (first list, 65 names):

| Value | Names in class | Must carry the piece | Share |
|---|---|---|---|
| Degree C / S / N | 14 / 26 / 18 | 6 / 9 / 7 | 43% / 35% / 39% |
| Right / left | 16 / 16 | 6 / 6 | 38% |
| Will side / understanding side | 4 / 4 | 3 / 3 | 75% |
| Role END / CAUSE / EFFECT | 4 / 34 / 26 | 3 / 12 / 9 | 75% / 35% / 35% |
| Degree "all degrees"; layer *out* | 7; 5 | 4; 4 | 57%; 80% |
| Uses | 5–11 each | 4–5 | 45–80% |

This is the best case, a piece found nowhere outside its class. A marker that also occurs in other names, or that appears in fewer than a third of its class, was below what ninety names can show.

## 3. What the result means

**What it rules out.** A naming system in which shared spiritual meaning (degree, layer, polarity, use, role) is carried by shared letters or letter sequences, consistently enough to show in ninety names and holding across both lists, is not present. The test covered every surviving name attached to a coded member: the word-names, the Egyptian decan and god names, and the ~80 names no source reads.

**What it does not test.** It does not test whether each name identifies a society. A name can identify without describing, as a proper name does, and nothing in a letter-level test can see that. It also cannot see meaning carried by *words* drawn from several languages, and that is the one form of name–member relation the library has already established. The readable word-names are apt to their members (*The Body That Waited for Breath* §§5.7, 12.3): the teeth are made by Amen, Hebrew "firm"; the shoulder by Tebar, Aramaic "break"; the nails by κρίμα, Greek "judgment"; the brain by μῆνιγξ; the left foot by τραχύς, "rough". The same kind of meaning (the firm, the power that breaks, judgment) is spelled with entirely different letters in Hebrew, Aramaic and Greek. A grid of the Ventris kind works on one script for one language. Here the names come from at least four languages (Egyptian, Hebrew, Aramaic, Greek), so a meaning carried in this list would not, in general, line up with any one letter sequence. The null is therefore what one would observe both if the names carry no meaning and if they carry it as words from several languages. The letter-level test cannot separate the two. The word-level test that could separate them needs the meanings of the unread names, which is the very thing missing.

**The natural-plane account.** The result is also what the source history predicts. Quack places the passage's source in the circle of Greek astrological writing in Egypt, while stressing that the attribution cannot be proved (thesis §11). The decan names come from an astrological melothesia, in which each star-power holds a member (§12.4). On that account the sounds come from where the names were taken, not from the members' spiritual meaning. The thesis already draws the consequence for the decan and god names: such a name "says who rules the member … a statement about governance, not about function" (§12.4). The letter-level null extends that to the ~80 unread names. Whatever they are, their letters do not encode the members' functions.

This bears directly on the author's claim. A name that says *who rules* a member is an identifier of a power, not a description of a use. If the names identify the societies of the members, as the claim holds, the evidence of this study and of the thesis together says they do so as names, not as compositions from a sound key.

**The one lead.** In the first list, ⲣ marks the right-hand name of a pair, eight pairs to none. It is the only regularity in the study that passed a familywise threshold within its own registered family, and it fails in the second list. A compositional convention of the makers' list alone cannot be distinguished from chance in one list, because no third set of paired names exists to test it on. It is recorded here so that it is not rediscovered later and taken for a finding.

## 4. Departures from the plan

1. **Candidate pieces in at least three names, not two.** A piece in only two names cannot reach the familywise threshold in any class: the most favourable case, two of two names in the smallest class (4 of 65), gives p = 0.0029, against a threshold of 0.000137.
2. **Controls run after the first results.** `analysis.py` omitted three items named in the plan: length as a covariate (Control 3), neighbourhood-restricted permutations for the grid (Control 1), and Test 1's three contrasts as separate families. They were run in `supplement.py` after the main results were seen. All three come from the plan text, and none changes the verdict. The one cell to pass a threshold (§2.5) did so in the registered contrast, and it fails the registered validation.
3. **`results.md` was not produced.** The docstring of `analysis.py` names it. `results.json`, `results_supplement.json` and this file stand in its place.
4. **The coder had read the names** before coding the members (`meaning_table.md` §5). With a null result, any bias of this kind did not produce an association.

## 5. Status

The study's question is answered at the level the data allow. The ~80 unread names stay unread (thesis §12.4). Any further reading would need a new source, such as an attestation of the names outside this passage or a fuller copy of the "book of Zoroaster" the passage excerpts (II 19,8–10), not another pass over the same ninety names.

## Sources

- `analysis/results.json`, `analysis/results_supplement.json` (this study).
- `meaning_table.md`; `store/source_001.md` (Swedenborg's Grand Man chapters); `plan.md`.
- *The Body That Waited for Breath: The Angelic Anthropogony of the Apocryphon of John Read from the Coptic*, literary-compilation `data/08_Correspondential_Texts/` (§§5.2, 5.7, 11, 12.3–12.4, 14).
- Quack, Joachim Friedrich. "Dekane und Gliedervergottung: Altägyptische Traditionen im Apokryphon Johannis." *Jahrbuch für Antike und Christentum* 38 (1995): 97–122.
