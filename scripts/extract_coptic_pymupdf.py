#!/usr/bin/env python3
"""
Extract the Coptic transcription (Linssen 2024) into individual tractate markdown files.

Uses PyMuPDF (fitz) to read the PDF text layer directly, which contains
proper Unicode Coptic characters (U+2C80 range + U+03E0 range).

This replaces the DI-based extraction. Azure Document Intelligence
OCR-reads the visual glyphs instead of the text layer, producing
Latin/Greek character approximations that require extensive cleanup.
PyMuPDF reads the embedded Unicode text layer perfectly.

Output:
    output/coptic/          — Individual Coptic text files per tractate
    output/coptic_index.json — Machine-readable index

Usage:
    python scripts/extract_coptic_pymupdf.py                    # Extract all
    python scripts/extract_coptic_pymupdf.py --only II_2        # Single tractate
    python scripts/extract_coptic_pymupdf.py --dry-run          # Show plan
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "data" / "Nag_Hammadi_Library_Complete_Transcripti.pdf"
OUTPUT_DIR = PROJECT_ROOT / "output" / "coptic"

# Column x-boundaries (inches) — from PyMuPDF coordinate analysis
FOLIO_X_MAX = 1.3    # Folio column: x < 1.3" (typical: 0.86")
LINE_X_MAX = 2.1     # Line column: 1.3" <= x < 2.1" (typical: 1.65")
                      # Text column: x >= 2.1" (typical: 2.44")

# Content area boundaries (skip headers/footers)
CONTENT_Y_MIN = 1.2   # Below page header
CONTENT_Y_MAX = 10.5   # Above page footer

# Row grouping threshold (inches)
ROW_Y_THRESHOLD = 0.10

# Page header text to filter out
PAGE_NOISE = {
    "Nag Hammadi Library Complete Transcription",
    "2024",
    "Martijn Linssen",
    "23-8-2024",
    "Folio", "Line", "Text",
}

# ---------------------------------------------------------------------------
# Tractate definitions (identical to extract_coptic.py)
# ---------------------------------------------------------------------------

TRACTATES = [
    # Codex I
    {"codex": "I", "title": "Prayer of Apostle Paul", "codex_ref": "I,1", "start_page": 8, "slug": "I_1_prayer_apostle_paul"},
    {"codex": "I", "title": "Apocryphon of James", "codex_ref": "I,2", "start_page": 10, "slug": "I_2_apocryphon_james"},
    {"codex": "I", "title": "Gospel of Truth", "codex_ref": "I,3", "start_page": 28, "slug": "I_3_gospel_of_truth"},
    {"codex": "I", "title": "Treatise on the Resurrection", "codex_ref": "I,4", "start_page": 57, "slug": "I_4_treatise_resurrection"},
    {"codex": "I", "title": "Tripartite Tractate", "codex_ref": "I,5", "start_page": 65, "slug": "I_5_tripartite_tractate"},
    # Codex II
    {"codex": "II", "title": "Apocryphon of John", "codex_ref": "II,1", "start_page": 158, "slug": "II_1_apocryphon_john"},
    {"codex": "II", "title": "Gospel of Thomas", "codex_ref": "II,2", "start_page": 190, "slug": "II_2_gospel_thomas"},
    {"codex": "II", "title": "Gospel of Philip", "codex_ref": "II,3", "start_page": 210, "slug": "II_3_gospel_philip"},
    {"codex": "II", "title": "Hypostasis of the Archons", "codex_ref": "II,4", "start_page": 246, "slug": "II_4_hypostasis_archons"},
    {"codex": "II", "title": "On the Origin of the World", "codex_ref": "II,5", "start_page": 258, "slug": "II_5_origin_of_world"},
    {"codex": "II", "title": "Exegesis on the Soul", "codex_ref": "II,6", "start_page": 288, "slug": "II_6_exegesis_soul"},
    {"codex": "II", "title": "Book of Thomas the Contender", "codex_ref": "II,7", "start_page": 299, "slug": "II_7_book_thomas_contender"},
    # Codex III
    {"codex": "III", "title": "Apocryphon of John", "codex_ref": "III,1", "start_page": 309, "slug": "III_1_apocryphon_john"},
    {"codex": "III", "title": "Gospel of the Egyptians", "codex_ref": "III,2", "start_page": 334, "slug": "III_2_gospel_egyptians"},
    {"codex": "III", "title": "Eugnostos the Blessed", "codex_ref": "III,3", "start_page": 353, "slug": "III_3_eugnostos_blessed"},
    {"codex": "III", "title": "Sophia of Jesus Christ", "codex_ref": "III,4", "start_page": 366, "slug": "III_4_sophia_jesus_christ"},
    {"codex": "III", "title": "Dialogue of the Saviour", "codex_ref": "III,5", "start_page": 384, "slug": "III_5_dialogue_savior"},
    # Codex IV
    {"codex": "IV", "title": "Apocryphon of John", "codex_ref": "IV,1", "start_page": 403, "slug": "IV_1_apocryphon_john"},
    {"codex": "IV", "title": "Gospel of the Egyptians", "codex_ref": "IV,2", "start_page": 438, "slug": "IV_2_gospel_egyptians"},
    # Codex V
    {"codex": "V", "title": "Eugnostos the Blessed", "codex_ref": "V,1", "start_page": 461, "slug": "V_1_eugnostos_blessed"},
    {"codex": "V", "title": "Apocalypse of Paul", "codex_ref": "V,2", "start_page": 476, "slug": "V_2_apocalypse_paul"},
    {"codex": "V", "title": "(First) Apocalypse of James", "codex_ref": "V,3", "start_page": 482, "slug": "V_3_first_apocalypse_james"},
    {"codex": "V", "title": "(Second) Apocalypse of James", "codex_ref": "V,4", "start_page": 498, "slug": "V_4_second_apocalypse_james"},
    {"codex": "V", "title": "Apocalypse of Adam", "codex_ref": "V,5", "start_page": 514, "slug": "V_5_apocalypse_adam"},
    # Codex VI
    {"codex": "VI", "title": "Acts of Peter and the Twelve Apostles", "codex_ref": "VI,1", "start_page": 532, "slug": "VI_1_acts_peter_twelve"},
    {"codex": "VI", "title": "Thunder, Perfect Mind", "codex_ref": "VI,2", "start_page": 544, "slug": "VI_2_thunder_perfect_mind"},
    {"codex": "VI", "title": "Authoritative Teaching", "codex_ref": "VI,3", "start_page": 553, "slug": "VI_3_authoritative_teaching"},
    {"codex": "VI", "title": "Concept of Our Great Power", "codex_ref": "VI,4", "start_page": 566, "slug": "VI_4_concept_great_power"},
    {"codex": "VI", "title": "Plato, Republic 588A-589B", "codex_ref": "VI,5", "start_page": 579, "slug": "VI_5_plato_republic"},
    {"codex": "VI", "title": "Discourse on the Eighth and Ninth", "codex_ref": "VI,6", "start_page": 583, "slug": "VI_6_discourse_eighth_ninth"},
    {"codex": "VI", "title": "Prayer of Thanksgiving", "codex_ref": "VI,7", "start_page": 595, "slug": "VI_7_prayer_thanksgiving"},
    {"codex": "VI", "title": "Asclepius 21-29", "codex_ref": "VI,8", "start_page": 597, "slug": "VI_8_asclepius"},
    # Codex VII
    {"codex": "VII", "title": "Paraphrase of Shem", "codex_ref": "VII,1", "start_page": 612, "slug": "VII_1_paraphrase_shem"},
    {"codex": "VII", "title": "Second Treatise of the Great Seth", "codex_ref": "VII,2", "start_page": 661, "slug": "VII_2_second_treatise_great_seth"},
    {"codex": "VII", "title": "Apocalypse of Peter", "codex_ref": "VII,3", "start_page": 683, "slug": "VII_3_apocalypse_peter"},
    {"codex": "VII", "title": "Teachings of Silvanus", "codex_ref": "VII,4", "start_page": 697, "slug": "VII_4_teachings_silvanus"},
    {"codex": "VII", "title": "Three Steles of Seth", "codex_ref": "VII,5", "start_page": 731, "slug": "VII_5_three_steles_seth"},
    # Codex VIII
    {"codex": "VIII", "title": "Zostrianos", "codex_ref": "VIII,1", "start_page": 741, "slug": "VIII_1_zostrianos"},
    {"codex": "VIII", "title": "Letter of Peter to Philip", "codex_ref": "VIII,2", "start_page": 834, "slug": "VIII_2_letter_peter_philip"},
    # Codex IX
    {"codex": "IX", "title": "Melchizedek", "codex_ref": "IX,1", "start_page": 841, "slug": "IX_1_melchizedek"},
    {"codex": "IX", "title": "Thought of Norea", "codex_ref": "IX,2", "start_page": 856, "slug": "IX_2_thought_norea"},
    {"codex": "IX", "title": "Testimony of Truth", "codex_ref": "IX,3", "start_page": 858, "slug": "IX_3_testimony_truth"},
    # Codex X
    {"codex": "X", "title": "Marsanes", "codex_ref": "X,1", "start_page": 890, "slug": "X_1_marsanes"},
    # Codex XI
    {"codex": "XI", "title": "Interpretation of Knowledge", "codex_ref": "XI,1", "start_page": 926, "slug": "XI_1_interpretation_knowledge"},
    {"codex": "XI", "title": "Valentinian Exposition", "codex_ref": "XI,2", "start_page": 944, "slug": "XI_2_valentinian_exposition"},
    {"codex": "XI", "title": "On the Anointing", "codex_ref": "XI,2a", "start_page": 958, "slug": "XI_2a_anointing"},
    {"codex": "XI", "title": "On Baptism A", "codex_ref": "XI,2b", "start_page": 959, "slug": "XI_2b_baptism_a"},
    {"codex": "XI", "title": "On Baptism B", "codex_ref": "XI,2c", "start_page": 961, "slug": "XI_2c_baptism_b"},
    {"codex": "XI", "title": "On the Eucharist A", "codex_ref": "XI,2d", "start_page": 962, "slug": "XI_2d_eucharist_a"},
    {"codex": "XI", "title": "On the Eucharist B", "codex_ref": "XI,2e", "start_page": 963, "slug": "XI_2e_eucharist_b"},
    {"codex": "XI", "title": "Allogenes", "codex_ref": "XI,3", "start_page": 964, "slug": "XI_3_allogenes"},
    {"codex": "XI", "title": "Hypsiphrone", "codex_ref": "XI,4", "start_page": 987, "slug": "XI_4_hypsiphrone"},
    # Codex XII
    {"codex": "XII", "title": "Sentences of Sextus", "codex_ref": "XII,1", "start_page": 994, "slug": "XII_1_sentences_sextus"},
    {"codex": "XII", "title": "Gospel of Truth", "codex_ref": "XII,2", "start_page": 1003, "slug": "XII_2_gospel_of_truth"},
    # Codex XIII
    {"codex": "XIII", "title": "Trimorphic Protennoia", "codex_ref": "XIII,1", "start_page": 1009, "slug": "XIII_1_trimorphic_protennoia"},
    {"codex": "XIII", "title": "On the Origin of the World", "codex_ref": "XIII,2", "start_page": 1025, "slug": "XIII_2_origin_of_world"},
]

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class TextItem:
    """A text span with position."""
    text: str
    x: float   # inches
    y: float   # inches
    font: str


@dataclass
class TableRow:
    """A reconstructed table row: folio, line number, Coptic text."""
    folio: str = ""
    line: str = ""
    text: str = ""


# ---------------------------------------------------------------------------
# Page extraction
# ---------------------------------------------------------------------------

def extract_page_items(page: fitz.Page) -> list[TextItem]:
    """Extract all text items from a page with position info."""
    text_dict = page.get_text("dict")
    items = []

    for block in text_dict["blocks"]:
        if block["type"] != 0:  # skip image blocks
            continue
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue

            text = "".join(s["text"] for s in spans).strip()
            if not text:
                continue

            bbox = line["bbox"]
            x_inch = bbox[0] / 72.0
            y_inch = bbox[1] / 72.0
            font = spans[0]["font"]

            items.append(TextItem(text=text, x=x_inch, y=y_inch, font=font))

    return items


def is_noise(text: str) -> bool:
    """Check if text is page header/footer noise.

    Note: pure numbers (folio/line numbers) are NOT noise — they carry
    structural information. Actual page numbers in the footer are already
    excluded by the CONTENT_Y_MAX filter.
    """
    return text.strip() in PAGE_NOISE


def extract_page_rows(page: fitz.Page) -> list[TableRow]:
    """Extract structured table rows from a single page."""
    items = extract_page_items(page)

    # Filter to content area and skip noise / title headers
    items = [
        it for it in items
        if CONTENT_Y_MIN < it.y < CONTENT_Y_MAX
        and not is_noise(it.text)
        and "Bold" not in it.font   # Skip title headers (Constantia-Bold)
    ]

    # Sort by y then x
    items.sort(key=lambda it: (it.y, it.x))

    # Group into rows by y-proximity
    row_groups: list[list[TextItem]] = []
    current_group: list[TextItem] = []
    last_y = -999.0

    for it in items:
        if it.y - last_y > ROW_Y_THRESHOLD:
            if current_group:
                row_groups.append(current_group)
            current_group = [it]
        else:
            current_group.append(it)
        last_y = it.y

    if current_group:
        row_groups.append(current_group)

    # Classify columns and build rows
    rows: list[TableRow] = []
    for group in row_groups:
        row = TableRow()
        for it in group:
            if it.x < FOLIO_X_MAX:
                row.folio = it.text.strip()
            elif it.x < LINE_X_MAX:
                row.line = it.text.strip()
            else:
                row.text += (" " if row.text else "") + it.text

        # Only include rows that have Coptic text
        if row.text:
            rows.append(row)

    return rows


# ---------------------------------------------------------------------------
# Tractate extraction
# ---------------------------------------------------------------------------

def extract_tractate(doc: fitz.Document,
                     start_page: int, end_page: int) -> list[TableRow]:
    """Extract all table rows for a tractate across its page range.

    start_page/end_page are 1-indexed (DI convention, matching TRACTATES).
    PyMuPDF uses 0-indexed pages, so we subtract 1.
    """
    all_rows: list[TableRow] = []
    for pg in range(start_page - 1, end_page):
        if pg < 0 or pg >= len(doc):
            break
        rows = extract_page_rows(doc[pg])
        all_rows.extend(rows)
    return all_rows


def resolve_folios(rows: list[TableRow]) -> list[TableRow]:
    """Forward-fill folio numbers."""
    current_folio = ""
    for row in rows:
        if row.folio:
            # Handle duplicate folio transitions like "84 85"
            parts = row.folio.split()
            if (len(parts) == 2
                    and re.match(r"^\d+$", parts[0])
                    and re.match(r"^\d+$", parts[1])):
                current_folio = parts[1]
            else:
                current_folio = row.folio
            row.folio = current_folio
        else:
            row.folio = current_folio
    return rows


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_tractate_markdown(entry: dict, rows: list[TableRow],
                             end_page: int) -> str:
    """Format a tractate as structured markdown with folio sections."""
    lines = []
    lines.append(f"# {entry['title']} (Coptic)")
    lines.append("")
    lines.append(f"**Codex Reference**: {entry['codex_ref']}  ")
    lines.append(f"**Source**: Linssen, M., *Nag Hammadi Library Complete Transcription* (2024)  ")
    lines.append(f"**Pages**: {entry['start_page']}–{end_page} in source PDF  ")
    lines.append(f"**Extraction**: PyMuPDF (text layer, Unicode Coptic)")
    lines.append("")
    lines.append("---")
    lines.append("")

    if not rows:
        lines.append("*No Coptic text extracted for this tractate.*")
        return "\n".join(lines)

    current_folio = None
    for row in rows:
        if row.folio != current_folio:
            current_folio = row.folio
            if current_folio:
                lines.append("")
                lines.append(f"### Folio {current_folio}")
                lines.append("")

        if row.line:
            lines.append(f"**{row.line}** {row.text}")
        else:
            lines.append(row.text)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Extract Coptic tractates from Linssen PDF using PyMuPDF"
    )
    parser.add_argument("--only", help="Extract only tractates matching this slug prefix")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be extracted")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}")
        sys.exit(1)

    doc = fitz.open(str(PDF_PATH))
    total_pages = len(doc)
    print(f"Opened PDF: {total_pages} pages")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    index_data = []

    for i, entry in enumerate(TRACTATES):
        if args.only and not entry["slug"].startswith(args.only):
            continue

        # Calculate end page (1-indexed, matching TRACTATES convention)
        end_page = TRACTATES[i + 1]["start_page"] - 1 if i + 1 < len(TRACTATES) else total_pages
        page_count = end_page - entry["start_page"] + 1
        filename = f"{entry['slug']}.md"
        out_path = OUTPUT_DIR / filename

        if args.dry_run:
            print(f"  {filename:<50} pages {entry['start_page']:>4}–{end_page:>4} ({page_count} pages)")
            continue

        if out_path.exists() and not args.overwrite:
            # Count existing lines for reporting
            existing = out_path.read_text(encoding="utf-8")
            line_count = existing.count("\n**")
            print(f"  SKIP  {filename:<50} (exists, {line_count} lines)")
            continue

        # Extract, resolve folios, format
        rows = extract_tractate(doc, entry["start_page"], end_page)
        rows = resolve_folios(rows)
        md = format_tractate_markdown(entry, rows, end_page)

        out_path.write_text(md, encoding="utf-8")

        # Count characters and Coptic content
        coptic_chars = sum(
            1 for c in md
            if 0x2C80 <= ord(c) <= 0x2CFF or 0x03E0 <= ord(c) <= 0x03EF
        )

        index_data.append({
            "title": entry["title"],
            "codex_ref": entry["codex_ref"],
            "codex": entry["codex"],
            "slug": entry["slug"],
            "filename": filename,
            "start_page": entry["start_page"],
            "end_page": end_page,
            "coptic_lines": len(rows),
            "coptic_chars": coptic_chars,
        })

        print(f"  {filename:<50} {len(rows):>5} lines  {coptic_chars:>6} Coptic chars")

    doc.close()

    if not args.dry_run and index_data:
        index_path = OUTPUT_DIR / "coptic_index.json"
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        print(f"\nIndex: {index_path}")
        print(f"Total: {len(index_data)} tractates → {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
