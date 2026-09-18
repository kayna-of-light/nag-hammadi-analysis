---
name: coptic-correspondential-reading
description: Process a Coptic text into a seam-by-seam correspondential reading, working ONLY from the Coptic — published English translations (Robinson) are forbidden as a source and must not be opened. Natural seams first, then per seam a nuance-preserving English translation, the story underneath written as story, a lexicon of names and complex correspondences, and translation footnotes. Grounded in Swedenborg's doctrine of correspondences with the framework's corrections applied. Use when asked to read, translate, process, or render a Coptic text (Nag Hammadi tractate, Manichaean text, Kephalaia page) in correspondence. Keywords: coptic, tractate, translate, translation, correspondence, correspondential, seam, lexicon, folio, Linssen, Robinson, register, Nag Hammadi, story underneath, reading.
---

# Coptic Correspondential Reading

## STOP — do not open the English

**The source is the Coptic. Only the Coptic.**

Do not open `output/english/tractates/`. Do not fetch a translation. Do not "check Robinson first to get oriented". Do not read a translation to find the passage and then go to the Coptic. If a Coptic file is attached or named, that file is the text — start there and stay there.

This is not a preference. **The English translations destroy the evidence this method runs on.** Robinson's edition is a competent literary translation and it is unusable here, because:

- **It collapses the distinctions that carry the argument.** `ⲥⲙⲁⲧ`, `ⲉⲓⲛⲉ`, `ⲙⲟⲣⲫⲏ`, `ⲧⲩⲡⲟⲥ`, `ϩⲓⲕⲱⲛ` all become "form", "likeness" or "image". `ⲅⲛⲱⲥⲓⲥ` and `ⲥⲟⲟⲩⲛ` both become "knowledge". `ⲭⲁⲣⲓⲥ` and `ϩⲙⲟⲧ` both become "grace". The text builds its entire teaching on the difference between these pairs and the English erases it without trace.
- **It destroys register.** Which words are Greek loans and which are native Egyptian is load-bearing evidence. Translation flattens all of it into one English.
- **It invents terms the Coptic does not have.** It has twice supplied the word "correspondence" where the Coptic reads bare `ⲕⲁⲧⲁ` (κατά) — in Silvanus VII,4 and in Apocryphon of John fol. 15:5–8. Both were cited in this repo as ancient attestations of the term. Both were wrong. **Never cite a translation as evidence for what a text says.**
- **It smooths lacunae.** Restorations read as confident prose.
- **It hides the folio and line structure** that every reference in this project depends on.

A reading produced from the English is not a weaker version of this work. It is a different, worthless artifact, and it will be discarded.

**Where a published translation may be used:** as a check after your own translation exists, and only to report a disagreement in Notes with the Coptic that decides it. Never before, never as a source, never as a shortcut to locate a passage.

**If the Coptic is not available**, say so and stop. Do not substitute.

---

## What this produces

One document per text, built in two phases: **seams first, then one seam at a time.** Never write the seams out of order and never write two in a single pass.

Each seam section carries four parts, always in this order:

1. **The text in English** — translated to preserve the distinctions the Coptic makes
2. **What is being said** — the story underneath, written as story
3. **Lexicon** — names and non-obvious correspondences used in that seam
4. **Notes** — translation footnotes: where the English had to choose, what it lost, what is bracketed

Output goes to `findings/readings/<tractate_filename_base>_reading.md`. **One text, one file.** Never split a reading across multiple files, whatever its length.

---

## Phase 1 — Seams

Read the **whole text in Coptic** before deciding anything. Not the English, not a summary. The seams are determined from the source.

A seam is a natural joint in the composition. Find them by looking for:

- **Formula changes** — a repeated construction starting or stopping (`ⲕⲁⲧⲁ ⲑⲉ ⲁⲛ ⲉⲛⲧⲁϥϫⲟⲟⲥ ⲛ̅ϭⲓ ⲙⲱⲩ̈ⲥⲏⲥ`, "not as Moses said", marks one such series)
- **Register shifts** — a run of native Egyptian vocabulary giving way to Greek loans, or the reverse
- **Speaker or frame changes** — dialogue opening or closing, a question answered, a hymn beginning
- **Enumeration boundaries** — a list starting and ending
- **Repetition of a motif at a distance** — the same image returning marks the span between its occurrences as a unit

Do **not** use the modern editorial subheadings from Robinson or any other translation. Those are a translator's chapter divisions and they routinely cut across the composition's own joints.

Write the seam list into the file first, with `[TO BE WRITTEN]` under each, before writing any content. Each seam gets:

```markdown
## N. <A phrase from the seam itself, or a plain description>
**fol. X:nn – Y:nn**

[TO BE WRITTEN]
```

Track every seam as a separate item with `TaskCreate`/`TaskUpdate`. Mark one `in-progress`, write it, mark it `completed`, move on.

Typical seam count: 8 to 20 for a full tractate. Seam size follows the composition, not a target length — a long seam stays one seam if the text does not join anywhere inside it.

---

## Phase 2 — Per seam

### Step 1: Research before writing

For every seam, in this order:

1. **Read the Coptic of the seam again**, closely, at the line level.
2. **Check what the repo already has.** In order:
   - `findings/tractates/<this tractate>.yaml` — existing findings, including their errors
   - `findings/SYNTHESIS_the_whole_picture.md` — established person-correspondences and the naming law. **Record against these, do not re-derive them.**
   - Other tractates' YAML for the same motif
   - Any apparatus document already written for this text
3. **Check the Swedenborg library** for any correspondence you are unsure of — see §"Grounding" below.
4. **Note what you will need to say is uncertain.** Collect it now; it goes in Notes and in the closing limits section.

Do not skip step 2. Re-deriving something the corpus has already settled wastes the pass and produces a second, slightly different version of an established reading.

### Step 2: The text in English

Translate the seam. This is not a paraphrase and not a literary rendering. The requirement is precise:

> **A reader who has only the English must be able to see the correspondence that the Coptic carries.**

That means the English has to preserve distinctions the Coptic makes, even where idiomatic English would flatten them.

**Preserve register.** Where the Coptic sets up a native/Greek doublet, the English must show it. Do not translate `ⲟⲩⲅⲛⲱⲥⲓⲥ ⲡⲉ ⲉϥϯ ⲛ̅ⲟⲩⲥⲟⲟⲩⲛ` as "he is knowledge, giving knowledge" — that is a tautology in English and is not one in Coptic. Render it so the two-degree structure survives, and gloss the Coptic inline:

> he is **knowledge** (`ⲅⲛⲱⲥⲓⲥ`), giving **knowing** (`ⲥⲟⲟⲩⲛ`)

**Preserve the form/likeness family.** `ⲥⲙⲁⲧ`, `ⲉⲓⲛⲉ`, `ⲙⲟⲣⲫⲏ`, `ⲧⲩⲡⲟⲥ`, `ϩⲓⲕⲱⲛ`, `ⲥⲙⲟⲧ` all become "form", "likeness" or "image" in ordinary English and the text's whole argument runs through the difference. Fix one English word per Coptic word for the whole document and keep to it. State the mapping in the document header.

**Keep the verb.** Where the same verb does opposite work in two places (`ⲧⲱϩⲥ̅` anointing the Christ and blooming on the tree of death; `ⲉⲓⲱⲣⲙ` for the Father's gaze and the archons'), use the same English verb in both. The opposite sense is only visible if the word is the same.

**Keep the negations.** `ⲟⲩⲥⲱⲙⲁⲧⲓⲕⲟⲥ ⲁⲛ ⲡⲉ ⲟⲩⲧⲉ ⲟⲩⲁⲧⲥⲱⲙⲁ ⲁⲛ ⲡⲉ` is "not corporeal, nor incorporeal" — both halves declined. Do not smooth it into "beyond body".

**Mark the manuscript.** Carry Linssen's conventions into the English:

| Convention | Meaning | In the English |
|---|---|---|
| `[...]` | editorial reconstruction of a lacuna | keep the square brackets around the restored English |
| `{{...}}` | scribal deletion | keep, or footnote |
| combining macron | supralinear stroke — syllabic consonant **or** *nomen sacrum* | footnote when it is a *nomen sacrum* |
| `˙` `'` | punctuation / stroke marks | ignore unless they bear on a reading |

**Never smooth a lacuna into confident prose.** A bracketed word stays bracketed in the English.

### Step 3: What is being said

This is the part that matters and the part most easily got wrong.

**Write the story underneath as a story.** Not a commentary on the story. The seam has a natural sense and an interior sense; the interior sense is also a narrative, with the same shape, and it is what the text is actually about. Write that narrative.

**Do not explain. Do not teach. Do not argue.** No "this corresponds to", no "which signifies", no "the reader should note", no "in Swedenborgian terms", no framework vocabulary imported as label. If the prose contains the word "corresponds", it is the wrong prose.

**Test:** could this section be read aloud on its own, by someone who has never heard of correspondence, as a coherent account of something that happens? If yes, it is right. If it reads as annotation attached to a text, it is wrong — rewrite it.

Worked example. The Coptic, fol. 19:23–28:

> `ⲁϥⲛⲓϥⲉ ⲉϩⲟⲩⲛ ⲉϩⲣⲁϥ ⲙ̅ⲡⲉϥⲡ̅ⲛ̅ⲁ̅ ⲉⲧⲉ ⲧⲁⲓ̈ ⲧⲉ ⲧϭⲟⲙ ⲛ̅ⲧⲉϥⲙⲁⲁⲩ ⲙ̅ⲡⲉϥⲙ̅ⲙⲉ`

**Wrong** — this explains:

> The archon's breath corresponds to divine influx. He is a conduit for a power that originates above him, which illustrates the principle that the self claims what flows through it. This is the doctrine of influx expressed narratively.

**Right** — this tells it:

> He leant over the thing he had made and breathed into its face, and what went out of him was not his. It had come down through him from his mother and he had never once felt it arrive. He thought he was giving it life out of his own supply. The moment he spent it he was empty and the shape on the ground stood up and shone, and he could not think where the light had come from.

The second version carries the whole reading and never names it. That is the target.

**Rules for this section:**

- Present tense or past, consistently, chosen per document
- No section headings inside it
- Names may be kept (Sophia, Yaldabaoth) or replaced by what the figure is in that seam ("the one who did not know where he came from") — choose per document and be consistent
- Where the natural narrative has a gap or a lacuna, the interior narrative has one too. Do not fill it.
- Length: proportional to the seam. A dense seam may run longer than its translation; an enumeration may run much shorter.

**What licenses a reading.** Every correspondence used here must be either (a) established in `findings/SYNTHESIS_the_whole_picture.md` or an existing tractate YAML, (b) grounded in the Swedenborg library (see §"Grounding"), or (c) built inside this text from its own usage — the text using an image consistently across seams. If it is none of those three, it does not go in. It goes in Notes as an open question.

### Step 4: Lexicon

A table, per seam, of names and correspondences that are not self-evident from the English. Only what this seam actually uses.

```markdown
**Lexicon**

| Coptic | In the text | What it is |
|---|---|---|
| `ⲡϣⲟⲣⲡ ⲛ̅ⲣⲱⲙⲉ` | the First Man | the human form as the first thing outside the source, not the last |
| `ⲉⲡⲓⲛⲟⲓⲁ` | the Epinoia of light | the faculty that recognises; what cannot be seized (`ⲟⲩⲁⲧⲧⲉϩⲟⲥ`) |
| `ⲕⲱϩ` | envy | also the sixth power, which makes the skin — one word for the affection and the substance |
```

Rules:

- **Persons are states.** Give the state, not a character description. Test a person-correspondence by cross-text behaviour, never by name — see the standing rules in the repo instructions.
- **A shared name is not a shared figure.** Derive from relation, not from a name pool.
- **A split or doubled name is a signal.** Record it.
- Where a word carries the opposite sense in this seam, say which sense and what fixes it.
- Do not repeat a lexicon entry across seams unless it has changed sense.

### Step 5: Notes

Numbered footnotes, per seam, covering only translation and manuscript matters. This is the observation layer and it must be dry.

Put in Notes:

- Where the English had to choose between two defensible renderings, and what the other one was
- What the English lost (register, wordplay, a verb doing double duty elsewhere)
- Bracketed text: what is restored and how much of the surrounding line is legible
- *Nomina sacra* and other supralinear strokes that bear on sense
- Scriptural citations and allusions, with reference
- Where a reading in §3 rests on something contestable
- Disagreements with Robinson or any published translation, with the Coptic that decides it

Do **not** put interpretation in Notes. If it is a reading, it belongs in §3 or in the closing limits section.

---

## Document frame

Every reading document opens with:

```markdown
# <Text name> — read in correspondence

**Source.** <edition>, <what was read>, folios N–M.
**Companion files.** <links to the tractate YAML, apparatus, synthesis>

**How to read this.** Quoted Coptic with a folio reference is the manuscript.
The English translation is a translation. "What is being said" is a reading —
it is the interior sense told as narrative, and it is not in the manuscript in
that form. Where the reading goes past what the text will carry, that is
recorded at the end.

**Fixed renderings in this document.**

| Coptic | English used throughout |
|---|---|
| `ⲥⲙⲁⲧ` / `ⲥⲙⲟⲧ` | form |
| `ⲉⲓⲛⲉ` | likeness |
| `ⲙⲟⲣⲫⲏ` | shape |
| `ⲧⲩⲡⲟⲥ` | imprint |
| `ϩⲓⲕⲱⲛ` | image |
```

and closes with:

```markdown
## Where this reading goes beyond the text

<numbered list — every place the narrative supplied something the manuscript
does not contain, every restoration the reading leans on, every correspondence
imported rather than derived here>
```

That closing section is mandatory. The `[OBSERVATION]` / `[READING]` labelling used in the apparatus documents does not survive continuous prose; declaring the convention in the header and listing the overreach at the end is what replaces it.

---

## Grounding: Swedenborg, and what not to import

The correspondential lexicon this project works from is Swedenborg's. These texts are written in a different register — personified, narrative, sometimes polemical where he is expository — but they follow the same rules: correspondence grounded in the object's function, one direction (inside → outside), discrete degrees, opposite sense fixed by context.

**When a correspondence is not obvious, ask what Swedenborg says before inventing one.** Consult, in `literary-compilation/data/02_Swedenborgian_Theology/`:

| Need | Document |
|---|---|
| Objects, elements, minerals, plants, animals, weather | *The Universal Mirror: An Exhaustive Cartography of Natural Correspondences* |
| Scriptural objects | *A Library of Biblical Correspondences in Nature and Objects* |
| Body parts, organs, anatomy | *The Grand Man: An Exhaustive Anatomical Atlas of the Divine Human* |
| Persons, roles, relations | *The Spiritual Correspondence of Human Roles* |
| Numbers | *The Spiritual Numerology of the Word*; then *The Resolution of the Finite Mind* |
| Discrete degrees, influx mechanics, why the natural does not break | *Asking the Skin to Be the Heart* |
| Whether a Swedenborg claim is safe to use at all | *The Selfhood of the Prophet* |

### Swedenborg is a witness, not an authority

He derived this structure independently, publishing 1749–1771, before these codices were found. That makes a convergence evidential. It does not make him the standard the texts are graded against. The reading has to stand on the text's own cross-seam behaviour first.

Two failure modes, both fatal:

- **Testing the witness for a name.** Swedenborg has no figure called Sophia and no Yaldabaoth. He treats wisdom acting apart from love, and he treats the self that receives influx and declares ownership, at length. Test for the **state**, never the name. A witness writing in a non-personifying register is not disagreeing.
- **Grading the text against his conclusions instead of his method.** Where the tractate and Swedenborg differ, record the difference. Do not adjust the tractate.

### Never import these — they are corrected in this framework

The framework has audited Swedenborg's system and identified a layer of 18th-century scientific artifacts that are separable from the validated doctrine. **None of the following may appear in a reading, in a lexicon, or in a note.**

| Do not import | Why it fails | Use instead |
|---|---|---|
| **The limbus** — a fringe of "purest natural substances" retained after death | Cartesian epicycle, built to solve an interaction problem that correspondence itself dissolves | The vessel is **biography** — accumulated states, choices and loves |
| **Substance dualism; matter as "dead"** | Newtonian inheritance. There are not two substances needing a bridge | One reality in discrete degrees. The physical **expresses** the spiritual |
| **The body as an obstacle to be escaped** | Follows from the above. It also misreads these texts — II,1 declines both halves of the body/non-body split at fol. 3:23–24 and ends with the Pronoia descending **into** the body | Descent, indwelling, and return through the same way it came down |
| **Soul from the father, body from the mother**; Virgin Birth as biological necessity | Aristotelian embryology forced into theology. Makes the Glorification theatrical | The transparency model: a complete human soul through which the Lord flows without obstruction |
| **Uniform canonicity** — a text having one continuous internal sense throughout | Pre-critical. Swedenborg's own key produces a quality gradient that tracks compositional strata | Stratified: correspondential yield varies by layer, and that variation is data |
| **1757 as a datable event** | Empiricist date-fixing; his own diary says "what they signify I do not clearly know" | Numbers are qualitative states, in his visions as in scripture |
| **Categorical denial of return to the body** | Fell with the limbus chain. And II,1 fol. 27:8–21 states its own position: return is remedial and terminating, `ⲉϣⲁⲩⲛⲟⲩϫⲉ ϭⲉ ⲁⲛ ⲙ̅ⲙⲟⲥ ⲉϩⲟⲩⲛ ⲉⲕⲉⲥⲁⲣⲝ` | Read what the text says. Do not overwrite it with his denial |
| **The word "proprium"** | New Church jargon in a Latin costume. Swedenborg wrote Latin; it means "what is one's own" and he did not reify it | Plain English: "what is one's own", "the self", "the self that claims". In YAML, `proprium` remains a schema key — that is the schema's vocabulary, not prose |

Two further prohibitions, from the repo's standing rules:

- **Never substitute Jungian, Freudian or generic "symbolic" reading.** These texts predate those frameworks and the substitution creates anomalies the data does not support.
- **Never condemn a figure.** Describe the structural move — an order reversed, a source unrecognised — and assign no guilt. The framework follows data; it does not accuse. This holds for figures inside the text as much as for named thinkers outside it.

---

## Operating notes

**Coptic search does not work.** `Grep` returns empty for every Coptic Unicode query in this workspace. Do not retry it. Navigate `output/coptic/*.md` by reading directly — `### Folio N` headings, `**LINE#**` markers, 34–37 lines per folio after an 8–10 line header, so folio N starts near line `8 + (N-1)*38`. For pattern work across files, use a Python or PowerShell pass.

**Robinson's English is not evidence.** See the prohibition at the top of this file. It is repeated here because it is the single most common way this method fails: the agent opens the translation to "get oriented", and every register distinction the reading depends on is gone before work begins.

**Never rest an argument on a bracketed word alone.** Folio 1 of most codices is heavily restored. If the only support for a reading is inside `[...]`, the reading is at most `moderate` and must say so.

**The historical-critical reading is not cancelled.** Second-century sectarian conflict, editorial layering, translation from Greek — all real, all retained. It describes the outer. It does not reach the inner and it does not need to be wrong for the inner to be there.

**Record findings as you go.** Anything that would be a finding — a correspondence, an explicit statement, a structural principle, an anomaly — gets an entry in `findings/tractates/<tractate>.yaml` when the seam is finished, not at the end of the document. Use the schema in `findings/schema.yaml`. Confidence is `strong` only where the text demonstrates it; a reading built on restoration or on a lexical judgement that cannot be settled from this text is `moderate` or `tentative`, and the note says which.

**No git commits.** The user manages git directly.

**Escape-sequence check.** After writing, scan the output:

```powershell
$f='findings/readings/<file>.md'; $c=Get-Content -Raw $f
"unicode-escapes: " + ([regex]::Matches($c,'\\u[0-9a-fA-F]{4}')).Count
"escaped-quotes: " + ([regex]::Matches($c,'\\"')).Count
"coptic-chars: " + ([regex]::Matches($c,'[Ⲁ-⳿]')).Count
```

Nonzero on the first two means the edit tool wrote literal escapes; fix in the terminal and revert the editor buffer before continuing.

---

## Checklist

Before declaring a reading complete:

- [ ] No published translation was opened at any point before your own translation existed
- [ ] Whole text read in Coptic before seams were chosen
- [ ] Seams derived from the composition, not from a translator's subheadings
- [ ] Seam list written to the file before any seam was filled
- [ ] Every seam tracked and written individually
- [ ] Header declares the convention and fixes the form/likeness renderings
- [ ] Every seam has all four parts, in order
- [ ] English preserves register doublets, the form/likeness family, repeated verbs, and both halves of every negation
- [ ] Brackets carried into the English
- [ ] "What is being said" contains no explanation, no framework vocabulary, no "corresponds to" — reads as narrative on its own
- [ ] Every correspondence used is established in the repo, grounded in the Swedenborg library, or built from this text's own usage
- [ ] Lexicon gives states, not character descriptions
- [ ] Notes are dry — translation and manuscript only
- [ ] Nothing from the "never import" table appears anywhere
- [ ] The word "proprium" does not appear in prose
- [ ] Closing "Where this reading goes beyond the text" section is present and specific
- [ ] Findings entered in the tractate YAML
- [ ] Escape-sequence scan is clean
