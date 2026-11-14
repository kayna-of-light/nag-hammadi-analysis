# Part 2 — The origin of the names and the meaning of the members: research plan

**Started**: 2026-11-10, at the author's suggestion after the miss of Part 1 (`synthesis/001_first_run.md`): "test for origin of the name, not specifically the structure of the name itself".

## The question

Does the tradition a name comes from (Egyptian, Greek, Semitic) go with the spiritual meaning of the member it names? Part 1 found that the letters of the names carry no code. It also found that a letter-level test cannot see meaning carried as words from several languages. The tradition a name was drawn from is one level up from its letters. If the names identify communities, as the author holds, the choice of tradition could be part of what identifies them, even where the letters carry nothing.

## Data

- **Origins**: taken from the published readings collected in the appendix of *The Body That Waited for Breath* (§14), which rest on Quack 1995, Piwowarczyk 2021, Gundel 1936, Crum and the lexica. Coded in `analysis/build_origin.py` → `analysis/origin.csv`, by two rules fixed here:
  - **Strict**: only readings graded A or B. The origin is the tradition of the graded reading, the first stated in the reading column. **EG** = Egyptian god or decan name (including Coptic ⲡⲛⲟⲩⲧⲉ, "the god"); **GR** = Greek word; **SE** = Hebrew, Aramaic or other Semitic word or name, including theophoric -ēl, biblical and Sethian names, and Ἀρβαω, "fourfold Iao". Every grade-C name is **UN** (unread).
  - **Broad**: strict, plus grade-C proposals. A C reading that names one tradition takes that tradition. A C reading that names two different traditions (for example χρυσός *or* the decan ρυαξ), names only an unattributed magical word, or calls itself "probably a coincidence" stays UN. "Opaque" stays UN.
- **Meanings**: the frozen `meaning_table.md`, unchanged.
- **Names**: `analysis/names.csv`, unchanged: 93 names of members (65 in the first list, 28 in the second) and 16 force names (secondary).

## The prediction found in the text (one directional test)

**O1. Egyptian names fall on members of the natural degree.**

- "because 'Egypt' is memory-knowledge, it is also the natural; for all the memory-knowledge in man is natural, because it is in his natural man" (*AC* §4967).
- "the 'land of Egypt' is the natural mind in which is memory-knowledge" (*AC* §5276); "Egypt" signifies memory-knowledges (*AC* §§1165, 1462).
- "in the Grand Man celestial things constitute the head, spiritual the body, and natural the feet" (*AC* §4938); degree N in `meaning_table.md` §2.1.

These statements concern Egypt as a nation in the Word. Connecting that meaning to the Egyptian origin of a name in the list is the author's hypothesis that the names identify communities, and that connection is what O1 tests. The prediction holds whether Egypt is taken in its good or its opposite sense: both senses are memory-knowledge (*AC* §1165), and all memory-knowledge is natural (*AC* §4967).

Statistic: the share of EG names whose member has degree N, minus the share among all other names. One-sided. **Hit**: p < 0.05 under the strict coding with both null models. **Miss**: p ≥ 0.05 under the strict coding. The broad coding is reported as a sensitivity check.

No statement assigning a degree to Greece (Javan: "external worship", *AC* §§1151–1155) or to the Hebrews was found that would give a direction for GR or SE, so they enter only the neutral tests.

## Neutral tests (no direction in the text)

- **O2.** Origin (EG, GR, SE, UN) × degree (C, S, N, all degrees).
- **O3.** Origin × side (right, left), among names of paired members.
- **O4.** Origin × role (END, CAUSE, EFFECT).

Statistic: χ² on the contingency table, used only as a distance. p by permutation.

**Correction**: Holm across O1–O4, strict coding.

**O5 (descriptive)**: origin by list (first, second) and among the forces. Quack reports that the decan names stop after the first list (Quack 1995, 114–119; thesis §12.4).

## Null models

1. Origin labels permuted over the names within each list.
2. Origin labels permuted within blocks of five consecutive rows of each list. Names may have been taken in runs from a source, and meanings run in body order, so a run of one origin over a run of one degree would otherwise pass for an association.

10,000 permutations each, seed 20261110.

## Stated in advance

- **The data are not new to the coder.** The readings and their members were set out in the thesis. Registration fixes the tests and the coding rules; it cannot make the coder ignorant of where the readable names stand.
- **Power is low.** The strict coding has about nine Egyptian names among the members. The script prints the detection floor for O1 from the margins.
- **An origin is someone's identification, not a certainty.** A grade-B Egyptian name is Quack's or Piwowarczyk's equation.
- **What a result means.** A hit on O1 supports the author's hypothesis at this one point. An association in O2–O4 that survives Holm under both null models is a pattern to explain, not a confirmed prediction. A null result is reported as such.

## Status

**Run 2026-11-10: Miss.** O1: Egyptian names on natural members 4 of 9 against 28 of 84 others (strict; p = 0.45 within lists, 0.48 in blocks; 6 of 9 were needed), and reversed under the broad coding (6 of 27 against 26 of 66). O2–O4: no association (p 0.25–0.94); Holm-adjusted p = 1 throughout. See `synthesis/002_origin.md`.

## Outputs

- `analysis/build_origin.py` → `analysis/origin.csv`
- `analysis/origin_test.py` → `analysis/results_origin.json`
- `synthesis/002_origin.md`
