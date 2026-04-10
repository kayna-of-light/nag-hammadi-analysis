# The Nag Hammadi Library — Digital Tractate Collection

A structured digital edition of the complete Nag Hammadi Library, extracted from Robinson's *The Nag Hammadi Library in English* (3rd rev. ed., HarperSanFrancisco, 1990) and organized as individual tractate files for research and study.

## Source

Robinson, J.M. (ed.), *The Nag Hammadi Library in English*, 3rd revised edition, translated and introduced by members of the Coptic Gnostic Library Project of the Institute for Antiquity and Christianity (HarperSanFrancisco, 1990).

## What This Repository Contains

**48 tractates** extracted from the Nag Hammadi codices (I–XIII), the Berlin Gnostic Codex (BG 8502), and the Afterword, available in two forms:

| Directory | Description |
|-----------|-------------|
| `output/tractates/` | Full extraction with page-level formatting preserved |
| `output/cleaned/tractates/` | Cleaned versions: OCR artifacts removed, line-break hyphenation resolved, formatting normalized |

Each tractate file includes:
- Title and codex reference
- Translator attribution
- Source citation
- Editor's scholarly introduction (as blockquote)
- The complete translated text

## Tractate Index

| Codex | Tractate | Translators |
|-------|----------|-------------|
| I,1 | The Prayer of the Apostle Paul | Dieter Mueller |
| I,2 | The Apocryphon of James | Francis E. Williams |
| I,3 | The Gospel of Truth | Harold W. Attridge, George W. MacRae |
| I,4 | The Treatise on the Resurrection | Malcolm L. Peel |
| I,5 | The Tripartite Tractate | Harold W. Attridge, Elaine H. Pagels, Dieter Mueller |
| II,1 | The Apocryphon of John | Frederik Wisse |
| II,2 | The Gospel of Thomas | Helmut Koester, Thomas O. Lambdin |
| II,3 | The Gospel of Philip | Wesley W. Isenberg |
| II,4 | The Hypostasis of the Archons | Roger A. Bullard, Bentley Layton |
| II,5 | On the Origin of the World | Hans-Gebhard Bethge, Bentley Layton, et al. |
| II,6 | The Exegesis on the Soul | William C. Robinson Jr., Maddalena Scopello |
| II,7 | The Book of Thomas the Contender | John D. Turner |
| III,2 | The Gospel of the Egyptians | Alexander Bohlig, Frederik Wisse |
| III,3 | Eugnostos the Blessed / The Sophia of Jesus Christ | Douglas M. Parrott |
| III,5 | The Dialogue of the Savior | Stephen Emmel, Helmut Koester, Elaine H. Pagels |
| V,2 | The Apocalypse of Paul | George W. MacRae, et al. |
| V,3 | The (First) Apocalypse of James | William R. Schoedel, Douglas M. Parrott |
| V,4 | The (Second) Apocalypse of James | Charles W. Hedrick, Douglas M. Parrott |
| V,5 | The Apocalypse of Adam | George W. MacRae, Douglas M. Parrott |
| VI,1 | The Acts of Peter and the Twelve Apostles | Douglas M. Parrott, R. McL. Wilson |
| VI,2 | The Thunder, Perfect Mind | George W. MacRae, Douglas M. Parrott |
| VI,3 | Authoritative Teaching | George W. MacRae, Douglas M. Parrott |
| VI,4 | The Concept of Our Great Power | Francis E. Williams, et al. |
| VI,5 | Plato, Republic 588A–589B | James Brashler, et al. |
| VI,6 | The Discourse on the Eighth and Ninth | James Brashler, et al. |
| VI,7 | The Prayer of Thanksgiving | James Brashler, et al. |
| VI,8 | Asclepius 21–29 | James Brashler, et al. |
| VII,1 | The Paraphrase of Shem | Michel Roberge, Frederik Wisse |
| VII,2 | The Second Treatise of the Great Seth | Joseph A. Gibbons, Roger A. Bullard |
| VII,3 | Apocalypse of Peter | James Brashler, Roger A. Bullard |
| VII,4 | The Teachings of Silvanus | Malcolm L. Peel, Jan Zandee |
| VII,5 | The Three Steles of Seth | James E. Goehring, James M. Robinson |
| VIII,1 | Zostrianos | John H. Sieber |
| VIII,2 | The Letter of Peter to Philip | Marvin W. Meyer, Frederik Wisse |
| IX,1 | Melchizedek | Birger A. Pearson, Søren Giversen |
| IX,2 | The Thought of Norea | Birger A. Pearson, Søren Giversen |
| IX,3 | The Testimony of Truth | Birger A. Pearson, Søren Giversen |
| X,1 | Marsanes | Birger A. Pearson |
| XI,1 | The Interpretation of Knowledge | Elaine H. Pagels, John D. Turner |
| XI,2 | A Valentinian Exposition (with liturgical texts) | Elaine H. Pagels, John D. Turner |
| XI,3 | Allogenes | Antoinette Clark Wire, et al. |
| XI,4 | Hypsiphrone | John D. Turner |
| XII,1 | The Sentences of Sextus | Frederik Wisse |
| XII,3 | Fragments | Frederik Wisse |
| XIII,1 | Trimorphic Protennoia | John D. Turner |
| BG 8502,1 | The Gospel of Mary | Karen L. King, et al. |
| BG 8502,4 | The Act of Peter | James Brashler, Douglas M. Parrott |
| — | Afterword: The Modern Relevance of Gnosticism | Richard Smith |

## Project Structure

```
NagHammadiLibrary/
├── data/                              # Source PDF
├── output/
│   ├── tractates/                     # Full extracted tractates (47 files)
│   ├── cleaned/tractates/             # Cleaned tractates (47 files)
│   ├── pdfs/                          # Individual tractate PDFs (for GDrive)
│   └── index.json                     # Structured metadata for all tractates
├── scripts/
│   ├── extract_tractates.py           # PDF → individual markdown files
│   ├── clean_with_claude.py           # GPT-5.2 cleanup pipeline
│   ├── reprocess_batch.py             # Batch re-cleanup for problem files
│   ├── mirror_to_drive.py             # Sync to Google Drive
│   └── ...                            # Additional utility scripts
├── environment.yml                    # Conda environment (nhl)
└── README.md
```

## Usage

### Environment Setup

```bash
conda env create -f environment.yml
conda activate nhl
```

### Extract Tractates from Source PDF

```bash
python scripts/extract_tractates.py
```

### Clean Extracted Text

```bash
python scripts/clean_with_claude.py
```

### Sync to Google Drive

```bash
# Sync a single file
conda run -n nhl python scripts/mirror_to_drive.py --force --only filename.md

# Sync all files
conda run -n nhl python scripts/mirror_to_drive.py --force
```

## Companion Research

This collection supports the research conducted in:

- **[literary-compilation](https://github.com/kayna-of-light/literary-compilation)** — The Divine Bricolage framework
- **[structured-data-analysis](https://github.com/kayna-of-light/structured-data-analysis)** — Empirical data analysis

## Attribution

All translations are the work of the scholars listed above, published in Robinson's edition. This repository provides a structured digital format for research purposes. No content has been altered beyond OCR artifact cleanup and formatting normalization.
