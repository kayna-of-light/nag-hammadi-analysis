# Nag Hammadi Library — Correspondential Reading Project

## Project Overview

This repository contains the complete Nag Hammadi Library in English translation (48 tractates from Robinson's 3rd rev. ed., 1990), structured as individual markdown files for research. The primary research purpose is **reading these texts through the correspondential lens** — recognizing that many of these texts are written in correspondence, where natural images express spiritual realities organically.

This is not a theological exercise. The correspondential framework is applied because it **organizes the data better than alternatives**. Texts that scholarship has called "incoherent," "difficult to classify," or "confused mythology" become transparent when read as correspondence. The framework doesn't need to be imposed — the texts ask for it (Thomas, Saying 1).

### Companion Repositories

| Repository | Purpose |
|---|---|
| **[literary-compilation](https://github.com/kayna-of-light/literary-compilation)** | The Divine Bricolage framework — knowledge graph, source documents, theological synthesis |
| **[structured-data-analysis](https://github.com/kayna-of-light/structured-data-analysis)** | Empirical data analysis — NDE, past-life memory, MallWorld dream phenomenology |
| **[ProtoLuke](https://github.com/kayna-of-light/ProtoLuke)** | Proto-Luke reconstruction — the Jamesian Protograph |

---

## The Correspondential Lens

### What Correspondence Is

Correspondence is the **organic relationship** between a natural object and the spiritual reality it expresses. It is grounded in the object's actual function, not in arbitrary assignment.

- **Light** corresponds to **wisdom/truth** — because light enables the eye to distinguish forms, which is the function of the intellect
- **Fire** corresponds to **love/will** — because fire is the active principle that gives light existence, as love gives wisdom existence
- **Water** corresponds to **truth in the natural degree** — because water sustains natural life as truth sustains natural understanding
- **Garments** correspond to **external truths** — because garments clothe the body as natural truths clothe spiritual meaning
- **Animals** correspond to **affections** — each species embodies a specific quality of will
- **Seeds** correspond to **interior truths** — a seed contains the whole tree in potential
- **Mountains** correspond to **elevated spiritual states** — height indicates proximity to the source of influx
- **Bridal chamber** corresponds to **union of good and truth** — the joining of love and wisdom in one vessel

### What Correspondence Is NOT

| Category | Description | Why It Fails Here |
|---|---|---|
| **Allegory** | Arbitrary substitution (scales = justice) | Correspondences are grounded in function, not convention |
| **Jungian archetypes** | Spiritual realities as psychic projections | The texts describe objective spiritual realities, not the unconscious |
| **Metaphor** | "A is like B" | Correspondence says "A is B at the natural degree" — one reality, different levels |
| **Symbol** | Conventional sign pointing to abstract concept | Correspondence is organic participation, not pointing |

### Directionality of Correspondence

**Correspondence flows in one direction: inside → outside.** The spiritual causes the natural; the natural is the spiritual in ultimates. This is divine influx — interior reality bringing forth exterior form.

Thomas Saying 89: *"Why do you wash the outside of the cup?"* — This is a rhetorical question. If you clean the inside, the outside will be clean too. The inside produces the outside. Working on effects while ignoring causes is the fundamental error of natural-plane thinking.

The natural does not cause the spiritual. The same maker created inside and outside, but the making flows from within outward.

### Opposite Sense

The same natural image can express its correspondence in positive or negative sense depending on context:

| Image | Positive | Negative |
|---|---|---|
| Fire | Divine love, celestial warmth | Self-love burning, destructive passion |
| Water | Living truth | Falsity (stagnant/poisoned water) |
| Serpent | Prudence of the sensory mind | Deception, sensory mind usurping |
| Darkness | Obscurity before illumination | Active falsity, denial of truth |
| Lion | Strength of good in the natural degree | Power of self-love devouring (Thomas 7) |

Always determine from context which sense applies.

### Discrete Degrees

Reality stratifies into celestial (love/will), spiritual (wisdom/truth), and natural (effects/ultimates). These are **not** a continuum but **discrete levels** — each complete in itself, each containing the levels below it in potential. Influx flows downward through these degrees, becoming more determinate at each level.

### The Proprium

The proprium is the sense of self as separate — self-love. It is **not evil in itself** — it is the vessel that must be formed before it can receive. But when it claims what flows through it as its own possession, it becomes the obstacle. Yaldabaoth saying "I am God and there is no other God beside me" is the proprium's fundamental statement: receiving influx, forgetting its source, declaring ownership.

---

## Repository Structure

```
nag-hammadi-analysis/
├── .github/
│   └── copilot-instructions.md        # This file
├── data/                               # Source PDFs (JSON dumps gitignored)
│   ├── ...Robinson.pdf                 # English translations (22 MB)
│   └── ...Linssen.pdf                  # Coptic source texts (17 MB)
├── output/
│   ├── english/
│   │   ├── tractates/                  # Cleaned English translations (47 files)
│   │   └── supplementary/             # Preface, Introduction, Afterword, etc.
│   └── coptic/                         # Coptic source texts via PyMuPDF (56 files)
├── findings/                           # CORRESPONDENTIAL FINDINGS
│   ├── schema.yaml                    # Schema definition & documentation
│   └── tractates/                     # Per-tractate findings (YAML, 48 files)
├── scripts/
│   ├── extract_tractates.py           # Robinson PDF → English markdown
│   ├── extract_coptic_pymupdf.py      # Linssen PDF → Coptic markdown
│   ├── mirror_to_drive.py             # Build PDFs and sync to Google Drive
│   └── assets/                        # CSS + HTML template for PDF generation
├── CLAUDE.md                          # Agent instructions (Claude Code)
├── environment.yml                    # Conda environment (nhl)
└── README.md
```

---

## The Findings System

### Purpose

As tractates are systematically read through the correspondential lens, findings are recorded in structured YAML files — one per tractate. This captures:

- **What was found** — the specific observation
- **Where it was found** — passage reference
- **What principle it evidences** — which part of the framework
- **How confident we are** — strong, moderate, or tentative
- **What it connects to** — other tractates, traditions, or framework documents

### Findings Directory

```
findings/
├── schema.yaml                        # Full schema with categories, principles, abbreviations
└── tractates/                         # One YAML file per analyzed tractate
    ├── II_1_apocryphon_john.yaml
    ├── II_2_gospel_thomas.yaml
    ├── II_3_gospel_philip.yaml
    └── ...
```

Filenames mirror `output/english/tractates/` exactly.

### Finding Categories

| Category | Description | Example |
|---|---|---|
| `correspondence` | A specific natural→spiritual mapping | "animals in human form" = affections (Philip) |
| `explicit_statement` | Text explicitly teaches correspondence/influx/degrees | "Truth came in types and images" (Philip) |
| `structural_principle` | A framework principle operating as structural element | Voice→Speech→Word = discrete degrees (Protennoia) |
| `person_correspondence` | A named figure functioning as a state rather than a character | Peter = faith apart from love (Gos. Mary, Thomas 114) |
| `divine_human_anatomy` | Body/substance→spiritual-power mappings | "goodness created a bone-soul" (Ap. John) |
| `cross_reference` | Connection to other tractate, Swedenborg, or tradition | "written in the book of Zoroaster" (Ap. John) |
| `anomaly` | Resists or complicates correspondential reading | Christianized editorial layers in Protennoia |

### Framework Principles

Each finding evidences one or more of these:

| Principle | Description |
|---|---|
| `correspondence` | Natural→spiritual mapping (the basic unit) |
| `discrete_degrees` | Celestial/spiritual/natural stratification |
| `influx` | Divine truth/good flowing into natural forms |
| `constant_state_variable_form` | Same reality, different perceptual expressions |
| `opposite_sense` | Same symbol meaning good or evil by context |
| `regeneration` | The spiritual transformation process |
| `proprium` | Self-love claiming what it receives |
| `divine_human` | The Grand Man; body-correspondence system |
| `ancient_word` | Evidence for pre-literary correspondential knowledge |
| `bridal_chamber` | Union of good and truth; celestial marriage |
| `ruling_love` | Core orientation determining everything else |
| `accommodation` | Truth delivered at different levels for different receivers |

### Confidence Levels

| Level | Meaning |
|---|---|
| `strong` | The text explicitly states or clearly demonstrates the finding |
| `moderate` | The finding is well-supported but requires some interpretive work |
| `tentative` | Plausible reading but alternative interpretations exist |

### Finding File Structure

```yaml
tractate: "II,2"
title: "The Gospel of Thomas"
filename: "II_2_gospel_thomas.md"
status: complete            # not_started | in_progress | complete
richness: extraordinary     # extraordinary | rich | moderate | sparse | resistant

summary: >
  Free-form assessment of the tractate's overall correspondential depth.

findings:
  - id: GT-001
    category: explicit_statement
    passage: >
      "Whoever finds the interpretation of these sayings
      will not experience death."
    location: "Saying 1"
    finding: >
      Direct editorial instruction: the text has an exterior (sayings)
      and an interior ("the interpretation" — singular). Finding the
      interior is the stated purpose.
    principles:
      - correspondence
    confidence: strong
    notes: >
      The only text in the ancient record that directly announces
      its own correspondential structure.
```

### Tractate Analysis Workflow

When analyzing a tractate:

1. **Read the full text** — including the editor's scholarly introduction
2. **Create findings file** — `findings/tractates/[filename].yaml`
3. **Set status** to `in_progress`
4. **Record findings** as they emerge, categorized and linked to principles
5. **Assess richness** — how correspondentially dense is this text overall?
6. **Write summary** — overall assessment
7. **Set status** to `complete` when no further findings are expected
8. **Cross-reference** — note connections to findings in other tractate files

### Key Rules

- **Record what the text says, not what you want it to say.** If a passage doesn't yield to correspondential reading, record it as an anomaly.
- **Quote the passage.** Every finding must include the actual text or a close paraphrase.
- **Distinguish explicit from interpretive.** "Explicit statement" means the text teaches it directly. "Correspondence" means the mapping is operating but the text doesn't step back to name it.
- **One finding per entry.** Don't bundle multiple observations into a single finding.
- **Cross-reference aggressively.** If Thomas Saying 22 and Philip's "making the two one" describe the same principle, both findings should reference each other in notes.

---

## Tractate Classification

### By Correspondential Richness (from initial analysis)

**Extraordinary** — saturated with correspondential content:
- Gospel of Thomas (II,2) — the key text; Saying 1 is the editorial instruction
- Gospel of Philip (II,3) — most systematic; explicitly theorizes correspondence
- Apocryphon of John (II,1) — cosmogonic myth AS correspondence map; divine human anatomy
- Gospel of Truth (I,3) — the Living Book; dream/sleep metaphor; fragrance of Spirit

**Rich** — deep correspondential patterns throughout:
- Exegesis on the Soul (II,6) — regeneration cycle narrated step by step
- Trimorphic Protennoia (XIII,1) — three descents as discrete degrees of influx
- Thunder, Perfect Mind (VI,2) — entirely structured as opposite-sense proclamations
- Hypostasis of the Archons (II,4) — proprium personified; spiritual Woman as awakener
- Teachings of Silvanus (VII,4) — explicitly uses the word "correspondence"; discrete degrees taught

**Rich (structural key):**
- Apocalypse of Adam (V,5) — thirteen kingdoms; words on the mountain; the generation without a king

All 48 tractates now have findings files. Richness ratings are recorded per file in `findings/tractates/`; a few remain `in_progress`.

### Cross-tractate synthesis

`findings/SYNTHESIS_the_whole_picture.md` — the corpus read as one composition, keyed on persons-as-states. Read it before starting new per-tractate work so findings are recorded against the established person-correspondences rather than re-derived.

---

## Reading Principles (Do's and Don'ts)

### DO

- Read the natural sense first, then identify correspondential objects, then read the spiritual sense
- Record both levels — natural and correspondential — as parallel, not as one replacing the other
- Check for consistency — the same object should correspond to the same reality across contexts
- **Read persons as correspondences too.** Named figures are states, not characters. Test a proposed person-correspondence by cross-text behaviour: the same figure should act the same way in unrelated tractates. See `SYNTHESIS_the_whole_picture.md`.
- **Watch for split names.** When a state divides, these texts split the name (Echamoth/Echmoth; spiritual woman/carnal woman; Sabaoth as archon/Sabaoth elevated). A doubled or near-doubled name is a signal, not a scribal slip.
- **Derive a person from their relation, not from their name.** A shared name does not merge figures. Philip's three Marys are mother, sister and companion — three distinct relations to the same Lord. Only the companion is the consort, and the consort correspondence comes from *being consort to Divine Wisdom*, not from being called Mary. Pooling figures by name is the standing failure mode here.
- Report hits as hits — when the framework predicts and the text confirms, say so clearly
- **Keep outside witnesses distinct in kind.** Swedenborg is *independent derivation* — he resolved the same structure from his own data, published 1749–1771, before these codices existed. The Manichaean Kephalaia is *shared substrate* — same centuries, same ground, overlapping sources, so a convergence there attests transmission, not rediscovery. Both are witnesses; neither is a baseline the texts are measured against.
- Report anomalies honestly — when the text resists the reading, say so
- Trace cross-textual patterns — the same correspondence appearing in independent texts is significant
- Note when the text cites its own sources (e.g., "the book of Zoroaster")

### DO NOT

- Substitute Jungian, Freudian, or generic "symbolic" interpretation. These texts predate those frameworks.
- Treat "Gnosticism" as a unified system you're confirming or refuting. The texts are diverse.
- Force the framework where it doesn't fit. Honest reporting of resistance is more valuable than false confirmation.
- Hedge against confirmed observations to appear "balanced." Accuracy is the goal, not false equidistance.
- Let the correspondential reading of a person erase the historical-critical one. The polemical layer (e.g. Peter as proto-orthodoxy) is real at the natural plane. Both readings stand; the outer does not cancel the inner.
- Dismiss the long enumeration lists (angel names, body-part correspondences) as meaningless repetition. They are correspondence maps — investigate them before dismissing.
- Read correspondences as running both ways. The direction is inside→outside. Influx flows from spiritual to natural.
- Treat any outside body of work — Swedenborg, the Kephalaia, Zoroastrian material — as the standard these texts are graded against. They are corroborating witnesses. The reading has to stand on cross-text behaviour inside the corpus first.
- **Report an outside witness as "silent" because a name is absent.** Test for the *state*, never the name. Swedenborg has no figure called Sophia and no Yaldabaoth, but he treats wisdom acting apart from love, and he treats the self that receives influx and declares ownership, at length. A witness writing in a non-personifying register is not disagreeing. Calling that a conflict of "genre" or "ontology" is the name-test failure applied to the witness instead of the tractate.
- **Mistake the corpus's vocabulary for a foreign mythology.** It is partly scriptural and openly so: Sophia (Prov 8, Sir 24), Sabaoth (LORD of hosts), Melchizedek (Gen 14), the Genesis persons; and the archon's boast is Isa 45:5/46:9 with Exod 20:5 quoted verbatim. The texts argue with the letter explicitly — "as Moses said", "it is written" + Gen/Exod/Num, Hosea 2:2–7, Ps 91:13 LXX. This is exegesis of shared scripture, which makes divergences arguable passage by passage rather than incommensurable.

---

## Technical Operations

### Conda Environment

```bash
conda activate nhl
```

### Google Drive Sync

```bash
# Single file
conda run -n nhl python scripts/mirror_to_drive.py --force --only filename.md

# All files
conda run -n nhl python scripts/mirror_to_drive.py --force
```

The GDrive sync creates styled PDFs and uploads to a shared Google Drive folder. Both tractates/ and supplementary/ directories are supported.

### GDrive Configuration

- Root folder ID: `1zWhkCJKWBbExzZpV2MskcLLqBA6tTYxF`
- Credentials: `secrets/google_drive_credentials.json`
- Token cache: `secrets/google_drive_token.json`

### NotebookLM

The project NotebookLM notebook is titled **"The Living Library — Reading the Nag Hammadi Texts in Correspondence"**. Instructions for the notebook assistant are in `output/english/supplementary/00_notebooklm_instructions.md`.

---

## Standing Rules

- **No git commits** — the user manages git operations directly
- **Honesty above all** — report what the data shows, including when it contradicts expectations
- **Correspondences are ontological, not symbolic** — A IS B at the natural degree, not "A represents B"
- **Do not overuse analogies as primary evidence** — analogies illustrate; they don't prove
- **The direction is inside→outside** — correspondence is unidirectional; influx flows from spiritual to natural
- **Proprium ≠ evil** — it is the vessel that must be formed; it becomes the obstacle only when it claims ownership
- **Discrete degrees, not a continuum** — celestial, spiritual, natural are complete levels, not points on a spectrum

---

## Key Texts: Quick Reference

### Thomas Saying 1 — The Key

> "Whoever finds the interpretation of these sayings will not experience death."

The only ancient text that directly announces its own correspondential structure. "The interpretation" (singular) = the correspondential interior. This is the key taped to the box.

### Apocalypse of Adam — The Thirteen Kingdoms

Each kingdom routes the Illuminator through a construct built on a ruling truth. The generation without a king receives directly. The "Words of Imperishability and Truth" are **on** a high mountain — the words exist AS the mountain. Knowledge preserved in form, not in text.

### Thomas Saying 89 — Directionality

> "Why do you wash the outside of the cup? Do you not realize that he who made the inside is the same one who made the outside?"

Rhetorical question. Clean the inside and the outside follows — because the inside produces the outside. This IS influx described in a single image.

### Philip — The Doctrine Stated

> "Truth did not come into the world naked, but it came in types and images. The world will not receive truth in any other way."

The clearest ancient statement of correspondential epistemology. Truth cannot enter the natural degree except through natural forms.

### Apocryphon of John — The Divine Human

The 365-angel body-creation passage is a correspondence map of the human form. Seven substance-souls (bone/goodness, sinew/foreknowledge, flesh/divinity, marrow/lordship, blood/kingdom, skin/envy, hair/understanding) progress from structural core to outermost emanation. The text attributes this system to "the book of Zoroaster" — direct evidence for the Ancient Word.

### Silvanus — image and true likeness

> εἰκών (`ⲛⲉⲧⲛⲣ`) reveals (`ⲡⲩⲛⲣ̅⳧̅ ⲉⲃⲁⲓ`) the true likeness (`ⲙ̅ⲡⲉⲓⲛⲉ ⲙ̅ⲙⲉ`) — VII,4 fol. 100:27–31

The Greek loan names the outer image; the native Egyptian words name what it discloses. The sentence performs the stratification while describing it.

**Correction (2026-08-03):** earlier drafts of these instructions claimed Silvanus "uses the word 'correspondence' explicitly." It does not. Robinson's "in correspondence to that which is revealed" renders plain `ⲕⲁⲣⲁ` (κατά). Do not cite Silvanus as an ancient attestation of the term. Cite the εἰκών → ⲙⲉ pairing instead — it is better evidence than the claim it replaces.

---

## Working with the Coptic Files

- **Full-text search does not work on Coptic.** `grep_search` returns empty for every Coptic Unicode query in this workspace — the index does not handle the Coptic block. Do not retry it.
- Navigate `output/coptic/*.md` by **reading directly**. Files are `### Folio N` headings with `**LINE#**` markers; roughly 34–37 lines per folio after an 8–10 line header, so folio offsets are predictable.
- For pattern work across the Coptic, use a Python or PowerShell pass over the files rather than the search tool.
- Transcription conventions (Linssen 2024): `[...]` editorial reconstruction of lacunae; `{{...}}` scribal deletion; `˙` and `'` punctuation/stroke marks; combining macron = supralinear stroke (both syllabic-consonant marking **and** *nomina sacra*).
