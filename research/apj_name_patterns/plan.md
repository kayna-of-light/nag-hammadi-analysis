# Sound and meaning in the angel names of the Apocryphon of John: research plan

**Started**: 2026-11-09, at the author's request, following *The Body That Waited for Breath* (literary-compilation `data/08_Correspondential_Texts/`). That thesis reads 38 of the 130 surviving names and finds the remaining ~80 unattested in the decan lists, the ritual texts and Crum.

## The question

The author's claim: the names identify spiritual communities. Each name is the identifier of the society that corresponds to its member, in the sense of the Grand Man, where the provinces of the body consist of societies (*AC* §4625). If that is so, members whose spiritual meanings are related should carry related names. A system of that kind might be found in the names themselves, without assuming in advance which sounds carry which meanings.

The design follows the author's specification (2026-11-09):

- **Fixed in advance**: only the structure, namely the spiritual meaning of each member and force as Swedenborg states it, or as it follows from the member's function in the way he derives it (*AC* §4223). This is `meaning_table.md`, which the author reviews before anything is computed.
- **Not assumed**: which features of the names carry meaning (vowels, consonants, syllables, positions), or whether any do. The analysis finds that, or finds nothing.

The model is Ventris's grid for Linear B: record systematically which signs occur in which contexts, without assuming sound values, and let the regularities show themselves.

## Data

- **Names**: the Coptic spellings of both codices, from the Linssen transcription in `nag-hammadi-analysis` (II 15,29–19,2; IV 24,22–29,6), as set out in the thesis's appendix (§14). Codex II is primary; Codex IV variants are used in a robustness run.
- **Members**: as coded in `meaning_table.md` (52 members, 13 forces), by degree (successive and simultaneous order), polarity and use. No member is coded as "good" or "truth": the body as a whole is the union of good and truth in which good rules (*AC* §§3887, 4931), and that relation enters only through degree and polarity (revised 2026-11-09 at the author's correction). Members whose identity is uncertain are left out (ϫⲱ, ⲧⲉⲧⲉ, ϭⲗⲁⲧⲉ ⲛ̅ⲧⲟⲩⲣⲏⲧⲉ), as are lost names.
- **Expected sample**: about 64 names in the first list and 28 in the second attached to coded members, plus about 17 force-names as a secondary set.

## Features of the names (no assumptions)

Each name is described by every letter it contains, every sequence of two and three letters, its first and last letters, and its length. Letter sequences that occur in at least two names are the candidate "pieces". The vowel/consonant distinction is not used unless the data bring it out.

## Tests, in order

**Test 0. Same member, same sound?** (needs no coding at all) About twenty-five members are named in both lists (left out: ϫⲱ, and the left shoulder, whose maker's name is lost), the maker in the first and the mover in the second. Is the maker's name more similar in sound to the mover's name of the *same* member than to the movers of other members? Similarity: shared letter sequences (Jaccard on bigrams and trigrams). Significance: permutation of the second-list names, 10,000 times. The same test for right/left partners: are the two names of a pair more alike than random pairs?

**Test 1. Shared meaning, shared sound?** (the matrix) For every pair of names, compute a sound similarity (as above) and a meaning similarity from the meaning table: same degree, same layer, overlap of use, and polarity. Because the degrees are discrete (*DLW* §§184, 238), degree is treated as a category, never as a scale. A Mantel test asks whether the two matrices are correlated across all pairs: whether names of members that mean similar things sound similar. This is one global test, with no rule assumed. Three contrasts follow directly from the structure and are tested separately: the right and left names of each pair (does something mark the side in which good leads?); the heart-side and lung-side names; and the names of the three degrees.

**Test 2. The grid** (discovery) For every candidate piece × every coded value (each degree, each layer, each polarity, each use), count how often the piece occurs in names whose member carries the component, against what chance gives. Significance by permutation of names over members; false-discovery control (Benjamini–Hochberg) across the grid. Pieces that survive are candidate carriers of a meaning.

**Test 3. Does it hold elsewhere?** (validation) Any rule found in the first list must predict the components of the second-list names, which were not used to find it. A rule that does not carry over is not reported as a finding. As a third check, the rule is applied to the forces, whose meanings are coded separately.

## Controls

1. **Position in the list.** The members are listed from head to foot, so neighbours in the list share meanings; and neighbouring names may share sounds for reasons of composition or copying. Every test is repeated with list distance partialled out (partial Mantel), and Test 2 with permutations restricted to neighbourhoods.
2. **Origin of the names.** Many names are Egyptian decan and god names (Quack 1995; Piwowarczyk 2021). A run excluding the names identified as Egyptian checks that a result is not merely tracking where names came from.
3. **Length.** Long names share more pieces with everything. Similarity measures are normalised, and length is included as a covariate.
4. **The second codex.** The tests are rerun on Codex IV spellings where they survive.

## What counts as a result, and what as a miss

- **Hit**: Test 1 and Test 0 positive beyond the permutation 95th percentile, with the position control; and at least one Test 2 rule that carries over to the second list (Test 3).
- **Partial**: Test 0 or Test 1 positive, but no rule survives Test 3. There is a relation between sound and meaning, but it cannot yet be read.
- **Miss**: Tests 0 and 1 at chance after the controls. With about 90 names, that would show only that no strong system is present; a weak one would not be detectable.
- Whatever the outcome, it is reported. A rule that appears only in the first list is reported as not validated, not as a finding.

## Power

The sample is small. Only a strong regularity, of the kind a deliberate naming system would produce, can be detected. Copying errors and the interchange of ⲉ, ⲏ and ⲓ add noise. These limits are stated in advance so that a null result is read correctly.

## Status

| Step | Status |
|---|---|
| Swedenborg's Grand Man chapters collected (`store/source_001.md`) | Done |
| Meaning table (`meaning_table.md`) | **Frozen 2026-11-10** before any name was attached (§5 of the table); commit `61323ec` |
| Name data assembled from the thesis appendix | Done: `analysis/build_names.py` → `analysis/names.csv` (109 names) |
| Tests 0–3 | Run 2026-11-10: `analysis/analysis.py` → `analysis/results.json`; plan items it omitted (length covariate, neighbourhood permutations, the three contrasts) in `analysis/supplement.py` → `analysis/results_supplement.json` |
| Synthesis | `synthesis/001_first_run.md` |

**Outcome (2026-11-10): Miss** by the criteria above. Tests 0 and 1 are at chance after every control (Test 0a p = 0.070; Mantel r = 0.016, p = 0.20; partial r = 0.012, p = 0.26). No grid cell survives correction, and no first-list lead holds in the second list. The one regularity to pass a familywise threshold within its own family is ⲣ in right-side names of the first list (8 pairs to 0; familywise p = 0.018). It reverses in the second list (3 to 6) and is reported as not validated.

**Part 2** (2026-11-10, at the author's suggestion): whether the *origin* of a name (Egyptian, Greek, Semitic) goes with the meaning of its member. Plan: `plan_002_origin.md`. **Outcome: Miss** — origin is spread across the body without regard to degree, side or role (`synthesis/002_origin.md`).

**Part 3** (2026-11-10): whether blind matchers recover the pairs of the readable word-names and their members. Plan: `plan_003_word_names.md`. **Outcome: the test failed** — the language-model matchers all recognised the Apocryphon, so no blind matchers could be obtained (`synthesis/003_word_names.md`).

## Outputs

- `meaning_table.md` — the coded structure
- `store/source_001.md` — Swedenborg's Grand Man chapters as read for the table
- `context.md` — what the library already establishes about the names
- `analysis/` — the scripts, the name data and the results
- `synthesis/001_first_run.md` — the result
