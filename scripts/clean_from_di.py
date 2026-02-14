#!/usr/bin/env python3
"""
Clean Gospel of the Egyptians from Azure Document Intelligence output.

Uses the AI OCR paragraphs (much cleaner than PyMuPDF) and applies
precise targeted fixes.
"""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DI_JSON = PROJECT_ROOT / "data" / "The Nag Hammadi Library. The Definitive Translation of the Gnostic Scriptures Complete in One Volume.pdf.json"
OUTPUT = PROJECT_ROOT / "output" / "cleaned" / "tractates" / "III_2_gospel_egyptians.md"


def load_paragraphs(start_page: int, end_page: int) -> list[tuple[int, str]]:
    """Load paragraphs from Azure DI JSON for given page range."""
    with open(DI_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    paragraphs = []
    for p in data["analyzeResult"]["paragraphs"]:
        regions = p.get("boundingRegions", [])
        if regions:
            pg = regions[0].get("pageNumber", 0)
            if start_page <= pg <= end_page:
                paragraphs.append((pg, p["content"]))
    return paragraphs


def is_page_header(text: str) -> bool:
    """Detect page headers and page numbers to strip."""
    stripped = text.strip()
    # Pure page numbers: "209", "210", etc.
    if re.match(r'^\d{3}$', stripped):
        return True
    # Running headers
    if stripped in (
        "THE GOSPEL OF THE EGYPTIANS (III,2 AND IV,2)",
        "THE NAG HAMMADI LIBRARY IN ENGLISH",
    ):
        return True
    return False


# Precise list of hyphenated line breaks to rejoin.
# Each entry: (broken form, correct form)
HYPHEN_FIXES = [
    ("pro- claim", "proclaim"),
    ("incor- ruptible", "incorruptible"),
    ("incorrupt- ible", "incorruptible"),
    ("vir- tue", "virtue"),
    ("un- marked", "unmarked"),
    ("plero- ma", "pleroma"),
    ("in- visible", "invisible"),
    ("unin- terpretable", "uninterpretable"),
    ("unpro- claimable", "unproclaimable"),
    ("ap- pear", "appear"),
    ("confla- gration", "conflagration"),
    ("im- movable", "immovable"),
    ("recon- ciliation", "reconciliation"),
    ("convoca- tions", "convocations"),
    ("bos- om", "bosom"),
    ("sur- passes", "surpasses"),
    ("es- tablished", "established"),
    ("unconquer- able", "unconquerable"),
    ("Gama- liel", "Gamaliel"),
    ("Yes- sedekeus", "Yessedekeus"),
    ("Yessede- keus", "Yessedekeus"),
    ("Mi- char", "Michar"),
    ("some- one", "someone"),
    ("every- one", "everyone"),
    ("ex- ists", "exists"),
    ("thir- ty", "thirty"),
    ("un- traceable", "untraceable"),
    ("Har- mozel", "Harmozel"),
    ("ple- roma", "pleroma"),
    ("de- ficiency", "deficiency"),
    ("ves- sel", "vessel"),
    ("sing- ing", "singing"),
    ("mention- ed", "mentioned"),
    ("be- fore", "before"),
]


def fix_hyphenated_breaks(text: str) -> str:
    """Fix all known hyphenated line breaks."""
    for broken, fixed in HYPHEN_FIXES:
        text = text.replace(broken, fixed)
    # Catch any remaining "word- word" patterns (conservative: lowercase only)
    # But only if it makes a real word - skip this, too risky
    return text


def clean_line_numbers(text: str) -> str:
    """Remove embedded verse line reference numbers.
    
    These appear as standalone numbers like ' 5 ', ' 10 ', ' 15 ', ' 20 ', ' 25 '
    at transitions in the original manuscript pagination.
    Also numbers like '18', '1º', etc.
    """
    # Remove ' followed by number at start (like "' 5 " or "' 10 ")  
    # The DI output uses ' as line-number markers
    # Pattern: number at specific positions that are clearly line refs
    # These are tricky - they appear as e.g. "Father,5 the" or "Spirit, 10 from"
    # We'll handle them carefully
    
    # Remove superscript-like numbers: 1º → nothing (these are line refs)
    text = re.sub(r'\b1º\b', '10', text)  # 1º is OCR for 10
    text = re.sub(r'\b2º\b', '20', text)  # 2º is OCR for 20
    text = re.sub(r'\b3º\b', '30', text)  # 3º is OCR for 30
    
    # Now remove line reference numbers that appear mid-text
    # Pattern: these are typically 1, 5, 10, 15, 18, 20, 25, 30 standing alone
    # They appear after punctuation or between words as " 5 " or " 10 "
    # We need to be careful not to remove actual content numbers
    
    # Remove ' (curly quote used as verse marker)
    text = text.replace(" ' ", " ")
    text = text.replace("' ", " ")
    # But preserve actual apostrophes in contractions
    
    return text


def clean_ocr_quotes(text: str) -> str:
    """Fix OCR quote/apostrophe artifacts."""
    # | and ! sometimes appear as verse markers instead of '
    # These are line-number separators in the original
    # Replace | that appears between words (not in brackets)
    text = re.sub(r" \| ", " ", text)
    text = re.sub(r" ! ", " ", text)
    return text


def clean_verse_numbers(text: str) -> str:
    """Remove manuscript verse/line numbers embedded in the text.
    
    The original text has numbers like 5, 10, 15, 18, 20, 25 that mark
    line positions in the Coptic manuscript. These appear mid-sentence.
    Also page references like '42', '43', '44', '49', '50', etc.
    """
    # Remove codex page numbers that appear mid-text (40-69 range for III, 50-81 for IV)
    # These look like: "Father,5 the" or "silence, 10 from" 
    # Pattern: a number 1-30 that appears between words, preceded by space or punctuation
    # This is very context-dependent, so we'll be conservative
    
    # Remove clear manuscript page transitions like "42 the three" or "43 Mother"
    # These are codex page numbers (III 40-69)
    text = re.sub(r'\b(4[0-9]|5[0-9]|6[0-9])\b(?=\s+[a-z\[])', '', text)
    
    # Remove line numbers (1-30) that appear after punctuation+space or start of content
    # Pattern: ", 5 " or ". 10 " etc - number between comma/period and lowercase word
    text = re.sub(r'(?<=[,;.!?])\s+(?:1|5|10|13|15|18|20|21|25|30)\s+', ' ', text)
    # Pattern: "word 5 word" where 5 is a line number
    text = re.sub(r'(?<=\w)\s+(?:1|5|10|13|15|18|20|21|25|30)\s+(?=[a-z\[(])', ' ', text)
    
    return text


def format_introduction(paragraphs: list[str]) -> str:
    """Format the introduction section as blockquotes."""
    lines = ["> **Editor's Introduction**", ">"]
    lines.append("> Introduced and translated by Alexander Böhlig and Frederik Wisse")
    lines.append(">")
    
    for para in paragraphs:
        # Wrap each paragraph with > prefix
        lines.append(f"> {para}")
        lines.append(">")
    
    # Remove trailing empty blockquote
    if lines[-1] == ">":
        lines.pop()
    
    return "\n".join(lines)


def build_document(raw_paragraphs: list[tuple[int, str]]) -> str:
    """Build the complete cleaned document."""
    
    # Filter out page headers and numbers
    filtered = [(pg, text) for pg, text in raw_paragraphs if not is_page_header(text)]
    
    # Separate into sections
    # First paragraph is the title
    # Then "Introduced and translated by" 
    # Then "ALEXANDER BÖHLIG..."
    # Then intro paragraphs (on page 224)
    # Then "THE GOSPEL OF THE EGYPTIANS" (section title on page 225)
    # Then "III 40, 12-44, 28..." (manuscript references)
    # Then the actual text
    
    intro_paras = []
    text_paras = []
    phase = "pre_intro"  # pre_intro -> intro -> text_title -> text
    
    for pg, text in filtered:
        stripped = text.strip()
        
        if phase == "pre_intro":
            # Skip the title and translator line
            if stripped == "THE GOSPEL OF THE EGYPTIANS (III,2 AND IV,2)":
                continue
            if stripped == "Introduced and translated by":
                continue
            if stripped == "ALEXANDER BÖHLIG and FREDERIK WISSE":
                continue
            if stripped.startswith("The so-called"):
                phase = "intro"
                intro_paras.append(stripped)
                continue
        
        if phase == "intro":
            # Introduction paragraphs (all on page 224)
            if stripped == "THE GOSPEL OF THE EGYPTIANS":
                phase = "text_title"
                continue
            if stripped.startswith("III 40,") or stripped.startswith("III 40, "):
                phase = "text"
                # This is the manuscript reference line - include it
                text_paras.append(stripped)
                continue
            intro_paras.append(stripped)
            continue
        
        if phase == "text_title":
            # Skip the section title repetition
            if stripped == "THE GOSPEL OF THE EGYPTIANS":
                continue
            if stripped.startswith("III 40"):
                phase = "text"
                text_paras.append(stripped)
                continue
            phase = "text"
            text_paras.append(stripped)
            continue
        
        if phase == "text":
            text_paras.append(stripped)
    
    # Build the document
    header = """# The Gospel of the Egyptians

**Codex Reference**: III,2 and IV,2
**Translated by**: Alexander Böhlig and Frederik Wisse
**Source**: Robinson, J.M. (ed.), *The Nag Hammadi Library in English*, 3rd rev. ed. (HarperSanFrancisco, 1990), p. 208ff.
"""
    
    # Format introduction
    intro = format_introduction(intro_paras)
    
    # Join text paragraphs
    text_body = "\n\n".join(text_paras)
    
    # Apply all cleanup passes to the full text
    full_text = f"{header}\n{intro}\n\n---\n\n{text_body}"
    
    # Apply fixes
    full_text = fix_hyphenated_breaks(full_text)
    full_text = clean_ocr_quotes(full_text)
    
    # Clean up multiple spaces
    full_text = re.sub(r'  +', ' ', full_text)
    
    # Fix the "111,2" OCR error if present
    full_text = full_text.replace("111,2", "III,2")
    
    return full_text


def main():
    print("Loading Azure DI JSON...")
    paragraphs = load_paragraphs(start_page=224, end_page=235)
    print(f"Found {len(paragraphs)} paragraphs")
    
    print("Building document...")
    doc = build_document(paragraphs)
    
    print(f"Writing to {OUTPUT}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(doc)
    
    print(f"Done. Output: {len(doc)} chars, {doc.count(chr(10))} lines")


if __name__ == "__main__":
    main()
