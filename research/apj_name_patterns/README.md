# Sound, origin and meaning in the angel names of the Apocryphon of John

Research on the names of the body-creation passage (NHC II 15,13–19,10; IV 24–29). The reading of the passage is
the thesis *The Body That Waited for Breath* (literary-compilation, `data/08_Correspondential_Texts/`). The graded
catalogue of every name is `findings/tractates/AJ_angel_catalogue.yaml`, and the findings are AJ-040 to AJ-049 in
`findings/tractates/II_1_apocryphon_john.yaml`.

## The question

The author's claim is that the names identify the spiritual communities of the members (the provinces of the Grand
Man). The study fixed only the members' meanings, coded from function as Swedenborg derives them, and asked whether
anything in the names follows those meanings.

## Results

| Part | Test | Outcome | Write-up |
|---|---|---|---|
| 1 | Letters: do names of members alike in meaning share letter sequences? | **Miss** (Mantel r = 0.016, p = 0.20; nothing replicates in the second list). One unvalidated lead: ⲣ marks the right-hand name in the first list (8 pairs to 0) and reverses in the second (3 to 6). | `synthesis/001_first_run.md` |
| 2 | Origin: does a name's tradition (Egyptian, Greek, Semitic) follow its member's meaning? | **Miss** (Egyptian names on natural members 4 of 9 vs 28 of 84, p = 0.45) | `synthesis/002_origin.md` |
| 3 | Word-names: do blind readers recover the fourteen word-name pairs? | **Failed**: the language-model matchers all recognised the Apocryphon | `synthesis/003_word_names.md` |

## Files

- `plan.md`, `plan_002_origin.md`, `plan_003_word_names.md`: the registered designs, with amendments and status
- `meaning_table.md`: the frozen coding of 52 members and 13 forces (degree, layer, polarity, use, role)
- `context.md`; `store/source_001.md` (Swedenborg's Grand Man chapters, quoted); `store/gundel_1936_decan_forms.py`
  (transcription of the decan-name tables in Gundel 1936, pp. 77–80, used for the grade-C decan proposals)
- `analysis/`: `build_names.py` (names from the thesis appendix; needs literary-compilation checked out beside this
  repository, or `LITCOMP=/path`), `analysis.py` + `supplement.py` (Part 1), `build_origin.py` + `origin_test.py`
  (Part 2), `word_match.py` + `word_match2.py` and `word_match/` (Part 3: every prompt, key and response, marked),
  `build_catalogue.py` (regenerates the catalogue in `findings/`), and the `results*.json` files.

Everything runs with the Python standard library, except `build_catalogue.py`, which needs PyYAML. Seeds are fixed;
`names.csv` and the results reproduce exactly.

## Where to continue

1. **Part 3 with human readers.** Use the round-2 sheets (`analysis/word_match/r2_prompt_*.txt`) after replacing
   the option lists with a general anatomical vocabulary: the Apocryphon's own member names ("breaths in the
   members", "hypochondrium") give the source away. The readers must not know the Apocryphon. Score with
   `word_match2.py score`.
2. **The ~80 unread names** need a new attestation (a papyrus, gem or decan list not in Gundel or Piwowarczyk).
   When one appears, correct the thesis appendix and rerun `build_catalogue.py` and `build_names.py`.
3. **The ⲣ side lead** cannot be tested further on these lists. A third set of paired names from a related text
   would be needed.
