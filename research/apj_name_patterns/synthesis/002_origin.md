# Synthesis 002 — The origin of a name does not follow the meaning of its member

**Run**: 2026-11-10. Design, coding rules and script committed before any result (`aa2b0a7`, "origin plan, coding and script (before any result)"): `plan_002_origin.md`; `analysis/build_origin.py` → `analysis/origin.csv`; `analysis/origin_test.py` → `analysis/results_origin.json` (seed 20261110, 10,000 permutations per test and null model). Meanings: the frozen `meaning_table.md`, unchanged since Part 1.

**Verdict by the registered criteria**: **Miss** on the one directional prediction (O1). The three neutral tests (O2–O4) find no association under either coding or either null model. After Holm correction every p is 1.

---

## 1. What was asked

Part 1 found no code in the letters of the names (`synthesis/001_first_run.md`). Its discussion noted that a meaning carried as whole words from several languages cannot show at the letter level. Part 2 moves up one level: does the tradition a name comes from (Egyptian, Greek, Semitic) go with the meaning of its member? Origins were taken from the published readings (thesis appendix §14: Quack 1995, Piwowarczyk 2021, Gundel 1936, Crum), coded *strict* (grade A/B only; 29 of the 93 member names) and *broad* (with grade-C proposals that name a single tradition; 60 of 93).

## 2. The prediction from the text (O1)

Swedenborg: "because 'Egypt' is memory-knowledge, it is also the natural; for all the memory-knowledge in man is natural" (*AC* §4967); "the 'land of Egypt' is the natural mind" (*AC* §5276); "natural [things constitute] the feet" (*AC* §4938). If the names identify communities, and Egyptian names identify communities of the natural, Egyptian names should fall on members of the natural degree.

| Coding | Egyptian names on natural members | Other names on natural members | Difference | p (within list) | p (blocks of 5) | Needed for p < 0.05 |
|---|---|---|---|---|---|---|
| Strict | 4 of 9 (44%) | 28 of 84 (33%) | +0.11 | 0.45 | 0.48 | 6 of 9 |
| Broad | 6 of 27 (22%) | 26 of 66 (39%) | −0.17 | 0.97 | 0.66 | 14 of 27 |
| Strict, with the forces | 5 of 11 | 39 of 98 | +0.06 | 0.60 | 0.57 | 8 of 11 |
| Broad, with the forces | 9 of 31 | 35 of 78 | −0.16 | 0.96 | 0.71 | 17 of 31 |

Under the strict coding the direction is as predicted, but the excess is one name: four Egyptian names on natural members where the overall rate gives three. Under the broad coding the direction reverses: most of the broadly coded Egyptian names, largely Quack's decan proposals, stand in the trunk, the spiritual degree (15 of 27).

## 3. The neutral tests (O2–O4)

**Origin × degree** (93 names; strict χ² = 6.81, p = 0.66 within lists, 0.33 in blocks; broad χ² = 9.66, p = 0.37, 0.62):

| Origin | Strict: C / S / N / all | Broad: C / S / N / all |
|---|---|---|
| Egyptian | 0 / 4 / 4 / 1 | 3 / 15 / 6 / 3 |
| Greek | 4 / 5 / 4 / 0 | 4 / 9 / 5 / 1 |
| Semitic | 1 / 2 / 4 / 0 | 4 / 4 / 6 / 0 |
| Unread | 11 / 27 / 20 / 6 | 5 / 10 / 15 / 3 |

**Origin × side** (54 names of paired members; strict χ² = 0.46, p = 0.94; broad χ² = 0.58, p = 0.93): Egyptian 4 right, 3 left; Greek 4, 4; Semitic 3, 2 (strict). The sides are as even as they could be.

**Origin × role** (92 names; strict χ² = 5.49, p = 0.45; broad χ² = 7.82, p = 0.25): every tradition supplies both causes and effects. Only five names belong to members that are ends, too few to say anything.

Holm across O1–O4: all adjusted p = 1, under both codings and both null models.

## 4. Origin by list (O5, descriptive)

| | Egyptian | Greek | Semitic | Unread |
|---|---|---|---|---|
| First list, strict / broad | 5 / 19 | 11 / 15 | 4 / 9 | 45 / 22 |
| Second list, strict / broad | 4 / 8 | 2 / 4 | 3 / 5 | 19 / 11 |
| Forces, strict / broad | 2 / 4 | 4 / 6 | 0 / 0 | 10 / 6 |

The Egyptian share is about the same in both lists under the broad coding (29% and 29%). Quack's observation that the *decan* names stop after the first list holds; Egyptian *divine* names continue in the second list (Ouertōn, Choux, Haroeris, Horus of Athribis), as he says.

## 5. What the result means

**Origin is spread across the body.** Each tradition appears at every degree, on both sides and in both causes and effects. The one gap is that no strictly read Egyptian name stands in the head. Under the broad coding three do (the proposals for the head, Paophi and a decan, and the decans proposed for the left eye and the uvula), and the gap was not significant in any case. Nothing in the data shows a compiler choosing the tradition of a name according to what the member is.

**The two misses together.** A name could carry its member's meaning at three levels: in its letters (Part 1), in the tradition it was taken from (Part 2), or in what the individual word means. Neither of the first two shows any relation to the members. The third is the level at which *The Body That Waited for Breath* found its hit: thirteen of the fourteen word-names of the first list are apt to their members, and none of the readable names contradicts its member (§§5.7, 12.3). The tradition is mixed and irrelevant. Where there is a relation, it is word by word: a Hebrew "firm" for the teeth, an Aramaic "break" for the shoulder, a Greek "judgment" for the nails.

**What this says about the author's claim.** If the names identify the communities of the members, neither their letters nor their origin carries that identity. Only the meaning of the individual word does, in the names that can be read.

**The natural-plane account.** The result is what Quack's account predicts: the compiler drew on a stock of Egyptian power-names and Greek and Semitic words, and placed them without regard to astronomical order (Quack 1995, 119: "Kein erkennbares Prinzip regelt das Verhältnis von ursprünglicher Abfolge in einer Dekanliste und Position innerhalb der Erschaffung des Körpers"). The present test adds that the origin of a name was not chosen by any principle visible in the members' meanings either.

## 6. Limits

- **Power.** Under the strict coding there are nine Egyptian names among the members; six of nine on natural members were needed for p < 0.05. A moderate preference would have been invisible.
- **The data were not new.** The readings and their members were set out in the thesis before this test was designed. The registration fixed the tests and the coding rules, not the coder's ignorance.
- **An origin is an identification.** Grade-B Egyptian names are Quack's or Piwowarczyk's equations, and the broad coding rests partly on grade-C proposals, four of them this study's own comparisons with Gundel's tables.
- **The prediction is derived.** Swedenborg's statements concern Egypt as a nation in the Word. The step to the Egyptian origin of a name is the author's hypothesis and was what O1 tested. It does not test the signification of Egypt.

## 7. What is left

The third level has not been tested against chance. The thesis's hit rests on the judgment that the word-names are apt to their members. A shuffle test would ask how many of the same words would look apt if they were attached to members at random. It would need the words' meanings coded by someone who does not know which member each belongs to. A fresh coder can be given only the glosses ("firm", "break", "judgment", "rough", "holding together" …) and the use categories of `meaning_table.md` §2.4, and the result compared with the members' frozen codes. That is the remaining test at which a name–member relation could be shown or fail.

## Sources

- `analysis/results_origin.json`, `analysis/origin.csv` (this study).
- `plan_002_origin.md`; `meaning_table.md`; `synthesis/001_first_run.md`.
- Swedenborg, *Arcana Coelestia* §§1151–1155, 1165, 1462, 4938, 4967, 5276 (Potts translation; e-swedenborg static pages, accessed 2026-11-10).
- *The Body That Waited for Breath*, literary-compilation `data/08_Correspondential_Texts/` (§§5.7, 12.3–12.4, 14).
- Quack, Joachim Friedrich. "Dekane und Gliedervergottung: Altägyptische Traditionen im Apokryphon Johannis." *Jahrbuch für Antike und Christentum* 38 (1995): 97–122.
