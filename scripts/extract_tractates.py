#!/usr/bin/env python3
"""
Extract the Nag Hammadi Library PDF into individual tractate markdown files.

Uses the Robinson translation (3rd edition, HarperSanFrancisco).
PDF page offset: book page + 16 = PDF page (0-indexed: book page + 15).

Output:
  output/english/tractates/       — Individual markdown files per tractate
  output/english/supplementary/   — Introduction, Preface, etc.
"""
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PDF_PATH = Path("data/The Nag Hammadi Library. The Definitive Translation of the "
                "Gnostic Scriptures Complete in One Volume.pdf")

OUTPUT_DIR = Path("output")
TRACTATE_DIR = OUTPUT_DIR / "english" / "tractates"
FRONT_MATTER_DIR = OUTPUT_DIR / "english" / "supplementary"

# PDF page 1 (0-indexed: 0) corresponds to nothing useful (blank).
# Book page 1 = PDF page 17 (0-indexed: 16).  Offset = 16.
PAGE_OFFSET = 16


# ---------------------------------------------------------------------------
# Tractate definitions — hardcoded from the Table of Contents
# ---------------------------------------------------------------------------
# Each entry: (title, codex_ref, book_start_page, translators, filename_slug)
# book_start_page is the page number printed in the book.

FRONT_MATTER = [
    {
        "title": "Preface",
        "book_start": "ix",
        "pdf_start": 9,   # 0-indexed
        "pdf_end": 12,     # exclusive
        "filename": "00_preface.md",
    },
    {
        "title": "Table of Tractates in the Coptic Gnostic Library",
        "book_start": "xiii",
        "pdf_start": 12,
        "pdf_end": 14,
        "filename": "01_table_of_tractates.md",
    },
    {
        "title": "Textual Signs",
        "book_start": "xv",
        "pdf_start": 14,
        "pdf_end": 15,
        "filename": "02_textual_signs.md",
    },
    {
        "title": "Introduction",
        "book_start": "1",
        "pdf_start": 16,
        "pdf_end": 42,  # ends before Pr. Paul at book p.27 = PDF p.43 (0-idx 42)
        "filename": "03_introduction.md",
        "author": "James M. Robinson",
    },
]

TRACTATES = [
    # CODEX I (Jung Codex)
    {
        "title": "The Prayer of the Apostle Paul",
        "codex_ref": "I,1",
        "book_page": 27,
        "translators": "Dieter Mueller",
        "slug": "I_1_prayer_apostle_paul",
    },
    {
        "title": "The Apocryphon of James",
        "codex_ref": "I,2",
        "book_page": 29,
        "translators": "Francis E. Williams",
        "slug": "I_2_apocryphon_james",
    },
    {
        "title": "The Gospel of Truth",
        "codex_ref": "I,3 and XII,2",
        "book_page": 38,
        "translators": "Harold W. Attridge and George W. MacRae",
        "slug": "I_3_gospel_of_truth",
    },
    {
        "title": "The Treatise on the Resurrection",
        "codex_ref": "I,4",
        "book_page": 52,
        "translators": "Malcolm L. Peel",
        "slug": "I_4_treatise_resurrection",
    },
    {
        "title": "The Tripartite Tractate",
        "codex_ref": "I,5",
        "book_page": 58,
        "translators": "Harold W. Attridge, Elaine H. Pagels, and Dieter Mueller",
        "slug": "I_5_tripartite_tractate",
    },

    # CODEX II
    {
        "title": "The Apocryphon of John",
        "codex_ref": "II,1; III,1; IV,1; BG 8502,2",
        "book_page": 104,
        "translators": "Frederik Wisse",
        "slug": "II_1_apocryphon_john",
    },
    {
        "title": "The Gospel of Thomas",
        "codex_ref": "II,2",
        "book_page": 124,
        "translators": "Helmut Koester and Thomas O. Lambdin",
        "slug": "II_2_gospel_thomas",
    },
    {
        "title": "The Gospel of Philip",
        "codex_ref": "II,3",
        "book_page": 139,
        "translators": "Wesley W. Isenberg",
        "slug": "II_3_gospel_philip",
    },
    {
        "title": "The Hypostasis of the Archons",
        "codex_ref": "II,4",
        "book_page": 161,
        "translators": "Roger A. Bullard and Bentley Layton",
        "slug": "II_4_hypostasis_archons",
    },
    {
        "title": "On the Origin of the World",
        "codex_ref": "II,5 and XIII,2",
        "book_page": 170,
        "translators": "Hans-Gebhard Bethge, Bentley Layton, and Societas Coptica Hierosolymitana",
        "slug": "II_5_origin_of_world",
    },
    {
        "title": "The Exegesis on the Soul",
        "codex_ref": "II,6",
        "book_page": 190,
        "translators": "William C. Robinson, Jr. and Maddalena Scopello",
        "slug": "II_6_exegesis_soul",
    },
    {
        "title": "The Book of Thomas the Contender",
        "codex_ref": "II,7",
        "book_page": 199,
        "translators": "John D. Turner",
        "slug": "II_7_book_thomas_contender",
    },

    # CODEX III
    {
        "title": "The Gospel of the Egyptians",
        "codex_ref": "III,2 and IV,2",
        "book_page": 208,
        "translators": "Alexander Bohlig and Frederik Wisse",
        "slug": "III_2_gospel_egyptians",
    },
    {
        "title": "Eugnostos the Blessed and The Sophia of Jesus Christ",
        "codex_ref": "III,3; V,1; III,4; BG 8502,3",
        "book_page": 220,
        "translators": "Douglas M. Parrott",
        "slug": "III_3_eugnostos_sophia",
    },
    {
        "title": "The Dialogue of the Savior",
        "codex_ref": "III,5",
        "book_page": 244,
        "translators": "Stephen Emmel, Helmut Koester, and Elaine H. Pagels",
        "slug": "III_5_dialogue_savior",
    },

    # CODEX V
    {
        "title": "The Apocalypse of Paul",
        "codex_ref": "V,2",
        "book_page": 256,
        "translators": "George W. MacRae, William R. Murdock, and Douglas M. Parrott",
        "slug": "V_2_apocalypse_paul",
    },
    {
        "title": "The (First) Apocalypse of James",
        "codex_ref": "V,3",
        "book_page": 260,
        "translators": "William R. Schoedel and Douglas M. Parrott",
        "slug": "V_3_first_apocalypse_james",
    },
    {
        "title": "The (Second) Apocalypse of James",
        "codex_ref": "V,4",
        "book_page": 269,
        "translators": "Charles W. Hedrick and Douglas M. Parrott",
        "slug": "V_4_second_apocalypse_james",
    },
    {
        "title": "The Apocalypse of Adam",
        "codex_ref": "V,5",
        "book_page": 277,
        "translators": "George W. MacRae and Douglas M. Parrott",
        "slug": "V_5_apocalypse_adam",
    },

    # CODEX VI
    {
        "title": "The Acts of Peter and the Twelve Apostles",
        "codex_ref": "VI,1",
        "book_page": 287,
        "translators": "Douglas M. Parrott and R. McL. Wilson",
        "slug": "VI_1_acts_peter_twelve",
    },
    {
        "title": "The Thunder, Perfect Mind",
        "codex_ref": "VI,2",
        "book_page": 295,
        "translators": "George W. MacRae and Douglas M. Parrott",
        "slug": "VI_2_thunder_perfect_mind",
    },
    {
        "title": "Authoritative Teaching",
        "codex_ref": "VI,3",
        "book_page": 304,
        "translators": "George W. MacRae and Douglas M. Parrott",
        "slug": "VI_3_authoritative_teaching",
    },
    {
        "title": "The Concept of Our Great Power",
        "codex_ref": "VI,4",
        "book_page": 311,
        "translators": "Francis E. Williams, Frederik Wisse, and Douglas M. Parrott",
        "slug": "VI_4_concept_great_power",
    },
    {
        "title": "Plato, Republic 588A-589B",
        "codex_ref": "VI,5",
        "book_page": 318,
        "translators": "James Brashler, Howard M. Jackson, and Douglas M. Parrott",
        "slug": "VI_5_plato_republic",
    },
    {
        "title": "The Discourse on the Eighth and Ninth",
        "codex_ref": "VI,6",
        "book_page": 321,
        "translators": "James Brashler, Peter A. Dirkse, and Douglas M. Parrott",
        "slug": "VI_6_discourse_eighth_ninth",
    },
    {
        "title": "The Prayer of Thanksgiving and Scribal Note",
        "codex_ref": "VI,7 and VI,7a",
        "book_page": 328,
        "translators": "James Brashler, Peter A. Dirkse, and Douglas M. Parrott",
        "slug": "VI_7_prayer_thanksgiving",
    },
    {
        "title": "Asclepius 21-29",
        "codex_ref": "VI,8",
        "book_page": 330,
        "translators": "James Brashler, Peter A. Dirkse, and Douglas M. Parrott",
        "slug": "VI_8_asclepius",
    },

    # CODEX VII
    {
        "title": "The Paraphrase of Shem",
        "codex_ref": "VII,1",
        "book_page": 339,
        "translators": "Michel Roberge and Frederik Wisse",
        "slug": "VII_1_paraphrase_shem",
    },
    {
        "title": "The Second Treatise of the Great Seth",
        "codex_ref": "VII,2",
        "book_page": 362,
        "translators": "Joseph A. Gibbons and Roger A. Bullard",
        "slug": "VII_2_second_treatise_great_seth",
    },
    {
        "title": "Apocalypse of Peter",
        "codex_ref": "VII,3",
        "book_page": 372,
        "translators": "James Brashler and Roger A. Bullard",
        "slug": "VII_3_apocalypse_peter",
    },
    {
        "title": "The Teachings of Silvanus",
        "codex_ref": "VII,4",
        "book_page": 379,
        "translators": "Malcolm L. Peel and Jan Zandee",
        "slug": "VII_4_teachings_silvanus",
    },
    {
        "title": "The Three Steles of Seth",
        "codex_ref": "VII,5",
        "book_page": 396,
        "translators": "James E. Goehring and James M. Robinson",
        "slug": "VII_5_three_steles_seth",
    },

    # CODEX VIII
    {
        "title": "Zostrianos",
        "codex_ref": "VIII,1",
        "book_page": 402,
        "translators": "John H. Sieber",
        "slug": "VIII_1_zostrianos",
    },
    {
        "title": "The Letter of Peter to Philip",
        "codex_ref": "VIII,2",
        "book_page": 431,
        "translators": "Marvin W. Meyer and Frederik Wisse",
        "slug": "VIII_2_letter_peter_philip",
    },

    # CODEX IX
    {
        "title": "Melchizedek",
        "codex_ref": "IX,1",
        "book_page": 438,
        "translators": "Birger A. Pearson and S\u00f8ren Giversen",
        "slug": "IX_1_melchizedek",
    },
    {
        "title": "The Thought of Norea",
        "codex_ref": "IX,2",
        "book_page": 445,
        "translators": "Birger A. Pearson and S\u00f8ren Giversen",
        "slug": "IX_2_thought_norea",
    },
    {
        "title": "The Testimony of Truth",
        "codex_ref": "IX,3",
        "book_page": 448,
        "translators": "Birger A. Pearson and S\u00f8ren Giversen",
        "slug": "IX_3_testimony_truth",
    },

    # CODEX X
    {
        "title": "Marsanes",
        "codex_ref": "X,1",
        "book_page": 460,
        "translators": "Birger A. Pearson",
        "slug": "X_1_marsanes",
    },

    # CODEX XI
    {
        "title": "The Interpretation of Knowledge",
        "codex_ref": "XI,1",
        "book_page": 472,
        "translators": "Elaine H. Pagels and John D. Turner",
        "slug": "XI_1_interpretation_knowledge",
    },
    {
        "title": "A Valentinian Exposition, with On the Anointing, On Baptism A and B, and On the Eucharist A and B",
        "codex_ref": "XI,2",
        "book_page": 481,
        "translators": "Elaine H. Pagels and John D. Turner",
        "slug": "XI_2_valentinian_exposition",
    },
    {
        "title": "Allogenes",
        "codex_ref": "XI,3",
        "book_page": 490,
        "translators": "Antoinette Clark Wire, John D. Turner, and Orval S. Wintermute",
        "slug": "XI_3_allogenes",
    },
    {
        "title": "Hypsiphrone",
        "codex_ref": "XI,4",
        "book_page": 501,
        "translators": "John D. Turner",
        "slug": "XI_4_hypsiphrone",
    },

    # CODEX XII
    {
        "title": "The Sentences of Sextus",
        "codex_ref": "XII,1",
        "book_page": 503,
        "translators": "Frederik Wisse",
        "slug": "XII_1_sentences_sextus",
    },
    {
        "title": "Fragments",
        "codex_ref": "XII,3",
        "book_page": 509,
        "translators": "Frederik Wisse",
        "slug": "XII_3_fragments",
    },

    # CODEX XIII
    {
        "title": "Trimorphic Protennoia",
        "codex_ref": "XIII,1",
        "book_page": 511,
        "translators": "John D. Turner",
        "slug": "XIII_1_trimorphic_protennoia",
    },

    # BG 8502
    {
        "title": "The Gospel of Mary",
        "codex_ref": "BG 8502,1",
        "book_page": 523,
        "translators": "Karen L. King, George W. MacRae, R. McL. Wilson, and Douglas M. Parrott",
        "slug": "BG_1_gospel_mary",
    },
    {
        "title": "The Act of Peter",
        "codex_ref": "BG 8502,4",
        "book_page": 528,
        "translators": "James Brashler and Douglas M. Parrott",
        "slug": "BG_4_act_peter",
    },

    # AFTERWORD
    {
        "title": "Afterword: The Modern Relevance of Gnosticism",
        "codex_ref": None,
        "book_page": 532,
        "translators": "Richard Smith",
        "slug": "ZZ_afterword",
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def book_page_to_pdf_index(book_page: int) -> int:
    """Convert a book page number to a 0-based PDF page index."""
    return book_page + PAGE_OFFSET - 1  # -1 because 0-indexed


def clean_text(raw: str) -> str:
    """Clean OCR artifacts from extracted text."""
    text = raw

    # Fix common OCR ligature / spacing issues
    text = re.sub(r'(?<=[a-z])-\s*\n\s*(?=[a-z])', '', text)  # rejoin hyphenated line breaks
    text = re.sub(r'\n{3,}', '\n\n', text)  # collapse excessive blank lines
    text = re.sub(r'[ \t]+', ' ', text)  # normalize whitespace (keep newlines)

    # Remove running headers like "THE NAG HAMMADI LIBRARY IN ENGLISH"
    text = re.sub(
        r'^(?:THE NAG HAMMADI LIBRARY IN ENGLISH|'
        r'[IVXLC]+\s*\n)',
        '', text, flags=re.MULTILINE
    )

    # Remove bare page numbers at start of text blocks
    text = re.sub(r'^\d{1,3}\s*\n', '', text, flags=re.MULTILINE)

    return text.strip()


def extract_pages(doc: fitz.Document, start_idx: int, end_idx: int) -> str:
    """Extract and clean text from a range of PDF pages (0-indexed, end exclusive)."""
    parts = []
    for i in range(start_idx, min(end_idx, len(doc))):
        raw = doc[i].get_text()
        cleaned = clean_text(raw)
        if cleaned:
            parts.append(cleaned)
    return '\n\n'.join(parts)


def make_tractate_markdown(entry: dict, text: str) -> str:
    """Format a tractate as a markdown document."""
    lines = []

    # Title
    lines.append(f"# {entry['title']}")
    lines.append("")

    # Metadata block
    if entry.get("codex_ref"):
        lines.append(f"**Codex Reference**: {entry['codex_ref']}")
    lines.append(f"**Translated by**: {entry['translators']}")
    lines.append(f"**Source**: Robinson, J.M. (ed.), *The Nag Hammadi Library in English*, "
                 f"3rd rev. ed. (HarperSanFrancisco, 1990), p. {entry['book_page']}ff.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Body
    lines.append(text)

    return '\n'.join(lines)


def make_supplementary_markdown(entry: dict, text: str) -> str:
    """Format a front matter section as markdown."""
    lines = []
    lines.append(f"# {entry['title']}")
    lines.append("")
    if entry.get("author"):
        lines.append(f"**Author**: {entry['author']}")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(text)
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}")
        sys.exit(1)

    doc = fitz.open(str(PDF_PATH))
    print(f"Opened PDF: {len(doc)} pages")

    # Create output directories
    TRACTATE_DIR.mkdir(parents=True, exist_ok=True)
    FRONT_MATTER_DIR.mkdir(parents=True, exist_ok=True)

    # ---- Extract front matter ----
    print("\n--- Front Matter ---")
    for fm in FRONT_MATTER:
        text = extract_pages(doc, fm["pdf_start"], fm["pdf_end"])
        md = make_supplementary_markdown(fm, text)
        out_path = FRONT_MATTER_DIR / fm["filename"]
        out_path.write_text(md, encoding="utf-8")
        print(f"  {fm['filename']} ({fm['pdf_end'] - fm['pdf_start']} pages)")

    # ---- Extract tractates ----
    print("\n--- Tractates ---")

    for i, entry in enumerate(TRACTATES):
        start_idx = book_page_to_pdf_index(entry["book_page"])

        if i + 1 < len(TRACTATES):
            end_idx = book_page_to_pdf_index(TRACTATES[i + 1]["book_page"])
        else:
            # Last entry (Afterword) — go to end of document
            end_idx = len(doc)

        page_count = end_idx - start_idx
        text = extract_pages(doc, start_idx, end_idx)
        md = make_tractate_markdown(entry, text)

        filename = f"{entry['slug']}.md"
        out_path = TRACTATE_DIR / filename
        out_path.write_text(md, encoding="utf-8")

        codex = entry.get("codex_ref") or ""
        print(f"  [{codex:>20s}] {entry['title'][:50]:<50s}  "
              f"({page_count} pp, {len(text):,} chars)")

    print(f"\nTotal: {len(TRACTATES)} tractates extracted")


if __name__ == "__main__":
    main()
