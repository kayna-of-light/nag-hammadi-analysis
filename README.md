# The Nag Hammadi Library — Correspondential Reading Project

A structured digital edition of the complete Nag Hammadi Library, containing both English translations and Coptic source texts, organized for systematic reading through the correspondential lens.

## Sources

| Source | Description |
|--------|-------------|
| **Robinson** | J.M. Robinson (ed.), *The Nag Hammadi Library in English*, 3rd rev. ed. (HarperSanFrancisco, 1990) — English translations |
| **Linssen** | *Nag Hammadi Library: Complete Transcriptions* — Coptic source texts in Antinoou font (Unicode) |

## What This Repository Contains

**48 English tractates** and **56 Coptic tractates** extracted from the source PDFs:

| Directory | Description | Files |
|-----------|-------------|-------|
| `output/english/tractates/` | Cleaned English translations (OCR artifacts removed, formatting normalized) | 47 |
| `output/english/supplementary/` | Preface, Introduction, Textual Signs, Afterword | 7 |
| `output/coptic/` | Coptic source texts extracted via PyMuPDF (Unicode, page/line referenced) | 56 + index |
| `findings/tractates/` | Correspondential analysis findings per tractate (YAML) | 48 |

Each English tractate file includes:
- Title and codex reference
- Translator attribution
- Source citation
- Editor's scholarly introduction (as blockquote)
- The complete translated text

Each Coptic tractate file includes:
- Codex, tractate, and page references
- Folio side indicators (recto/verso)
- Line-numbered Coptic text in Unicode

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

## Companion Repositories

| Repository | Purpose |
|---|---|
| **[literary-compilation](https://github.com/kayna-of-light/literary-compilation)** | The Divine Bricolage — research collection and synthesis |
| **[structured-data-analysis](https://github.com/kayna-of-light/structured-data-analysis)** | Empirical data analysis — NDE phenomenology, past-life memory, MallWorld dream data |
| **[manichaean-analysis](https://github.com/kayna-of-light/manichaean-analysis)** | Manichaean corpus — correspondential reading of the Kephalaia and related texts |
| **[proto-luke-reconstruction](https://github.com/kayna-of-light/ProtoLuke)** | Proto-Luke reconstruction — the Jamesian Protograph |

## Attribution

English translations are the work of the scholars listed above, published in Robinson's edition. Coptic transcriptions are from the Linssen edition. This repository provides a structured digital format for research purposes. No content has been altered beyond OCR artifact cleanup and formatting normalization.

```
nag-hammadi-analysis/
├── data/                              # Source PDFs (gitignored: *.json)
│   ├── ...Robinson.pdf                # English translations (22 MB)
│   └── ...Linssen.pdf                 # Coptic source texts (17 MB)
├── output/
│   ├── english/
│   │   ├── tractates/                 # 47 cleaned English translations
│   │   └── supplementary/            # Preface, Introduction, etc.
│   └── coptic/                        # 56 Coptic tractates (PyMuPDF)
├── findings/
│   ├── schema.yaml                    # Findings schema definition
│   └── tractates/                     # Per-tractate YAML findings (48 files)
├── scripts/
│   ├── extract_tractates.py           # Robinson PDF → English markdown
│   ├── extract_coptic_pymupdf.py      # Linssen PDF → Coptic markdown
│   ├── mirror_to_drive.py             # Build PDFs and sync to Google Drive
│   └── assets/                        # CSS and HTML template for PDF generation
├── CLAUDE.md                          # Agent instructions
├── environment.yml                    # Conda environment (nhl)
└── README.md
```

## Usage

### Environment Setup

```bash
conda env create -f environment.yml
conda activate nhl
```

### Extract English Translations

```bash
python scripts/extract_tractates.py
```

Extracts Robinson's English translations from the source PDF into `output/english/tractates/` and `output/english/supplementary/`.

### Extract Coptic Source Texts

```bash
python scripts/extract_coptic_pymupdf.py
```

Extracts Coptic Unicode text from the Linssen PDF into `output/coptic/`. Uses PyMuPDF to read the PDF text layer directly (the Antinoou font maps to proper Unicode Coptic codepoints U+2C80–U+2CFF).

### Sync to Google Drive

```bash
# Sync a single file
conda run -n nhl python scripts/mirror_to_drive.py --force --only filename.md

# Sync all files
conda run -n nhl python scripts/mirror_to_drive.py --force
```

Builds styled PDFs from the English tractates and uploads them to Google Drive.

## Companion Research

This collection supports the research conducted in:

- **[literary-compilation](https://github.com/kayna-of-light/literary-compilation)** — The Divine Bricolage framework
- **[structured-data-analysis](https://github.com/kayna-of-light/structured-data-analysis)** — Empirical data analysis
- **[manichaean-analysis](https://github.com/kayna-of-light/manichaean-analysis)** — Manichaean corpus analysis

## Attribution

All translations are the work of the scholars listed above, published in Robinson's edition. Coptic transcriptions are from the Linssen edition. This repository provides a structured digital format for research purposes. No content has been altered beyond OCR artifact cleanup and formatting normalization.
