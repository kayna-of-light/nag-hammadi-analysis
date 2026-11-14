# Synthesis 003 — The blind test of the word-names could not be carried out

**Run**: 2026-11-10. Design `plan_003_word_names.md` (committed `70bec48`), amended after round 1 for the failure of blindness (`0b94d81`), both before the responses they govern. Scripts: `analysis/word_match.py` (round 1), `analysis/word_match2.py` (round 2). Prompts, keys and every response, marked: `analysis/word_match/`. Counts of the excluded round-2 matchers: `analysis/results_word_match_r2_excluded.json`.

**Verdict by the registered rule**: **the test failed**. No two blind matchers could be obtained in either round. Under the amendment's rule ("If no two blind matchers are obtained, the test is reported as failed"), the aptness of the word-names is neither confirmed nor refuted by this test. It remains the judgment of *The Body That Waited for Breath* (§§5.7, 12.3).

---

## 1. What was asked

The thesis judges thirteen of the fourteen word-names of the first list apt to their members. The test asked whether readers who do not know the pairs recover them from the meanings of the words alone, beyond chance. Version A named the members. Version B added each member's natural function and its spiritual counterpart from the frozen meaning table.

## 2. What happened

| Round | Design | Matchers | Blind? | Placed on their own member (of 14) |
|---|---|---|---|---|
| 1 | All 14 meanings and 14 members, matched one to one | A1 | Yes, no sign of recall | 3 (chance ≈ 1.1; p ≈ 0.14 for one matcher) |
| | | A2 | No: cited the angel names in Robinson's spellings | 14 |
| | | B1, B2 | No: both declared they recognised the Apocryphon of John list | 6, 5 |
| 2 | Each meaning its own four-way question among all members, mixed with 28 decoys | A1, A2, A3, A4, B1, B2 | No: every SOURCE line names the Apocryphon of John | 5, 6, 5, 6, 6, 9 (chance 3.5) |

**Why blindness failed.** The matchers were language models. In round 1 the fourteen glosses seen together identified the source. In round 2 the body parts offered as options identified it, because they are the Apocryphon's own members ("breaths in the members", "hypochondrium", "nails of the hands", "uvula"). One matcher also pointed to the project context: every agent started in this repository loads its instructions, and those name "the 365-angel passage" among the project's subjects. The version-B spares (B3, B4) were not run, since version A had used both of its spares without a blind matcher and the outcome was already fixed.

## 3. What the answers show, as a record and not a test

All matchers recognised the source, so none of their answers counts as evidence. They still show which words a reader places on their own member and which ones only the thesis's reasoning places there. In round 2, two matchers (A3, A4) stated that they did not recall which name goes with which member. Counted over the six round-2 matchers (chance would give each word about 1.5 of 6):

| Word (member) | Times placed on its own member, round 2 |
|---|---|
| star (eye; breast) | 7 of 12 questions |
| meninges (brain) | 6 of 6 |
| rough (foot) | 6 of 6 |
| of sacred name (ear) | 5 of 6 |
| firm, true (teeth) | 4 of 6 |
| ruler (elbow) | 3 of 6 |
| book (kidneys) | 2 of 6 |
| judgment (nails of the hands) | 2 of 6, both in version B, where the nails were described as "those who give praise and blame without understanding" |
| body (genitals) | 1 of 6 |
| break (shoulder) | 1 of 6, by the matcher that recalled the list |
| royal (tonsils); well-flowering (forearm); fool (kidneys) | 0 of 6 |

The round-1 blind matcher placed the meninges, one star (the eye) and "fool" (on the left kidney).

Read with every caution that recognition imposes, the answers sort the fourteen into two groups. Five or six words are placed on their member by nearly every reader: the star, the meninges, the rough, the one of sacred name, the firm, and by half of them the ruler. In those cases the fit of word to member is evident. For the other eight, the fit the thesis finds rests on its own reasoning: breaking for the shoulder's power, judgment for the nails, the book for the kidneys' examination, the royal for the tonsils, well-flowering for the forearm, the fool for the kidney, the body for the genitals. Readers do not reach it unaided, or reach it only with Swedenborg's description of the member in front of them, or only by memory of the list.

## 4. What this means for the thesis

- The claim that **no readable name contradicts its member** is unaffected. No matcher's answer bears on it.
- The claim that **thirteen of the fourteen word-names are apt** stands as the thesis's reading. It has not been tested against chance, and the attempt to test it failed. The aptness evident to other readers covers about six of the fourteen.
- **A valid test needs matchers who do not know the Apocryphon and are not given its member list.** That means human readers, with distractor members drawn from a general anatomical vocabulary rather than the text's own. The round-2 sheets can be reused once their option lists are replaced.

## Sources

- `plan_003_word_names.md` (design and amendment); `analysis/word_match/` (all prompts, keys and responses); `analysis/results_word_match_r2_excluded.json`.
- *The Body That Waited for Breath*, literary-compilation `data/08_Correspondential_Texts/` (§§5.7, 12.3).
