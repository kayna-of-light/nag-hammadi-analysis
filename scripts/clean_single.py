#!/usr/bin/env python3
"""
Clean a single raw tractate file using regex-based transformations.
This avoids content filters by doing all work locally.
"""
import re
import sys
from pathlib import Path

def clean_text(text: str) -> str:
    """Apply all cleaning transformations."""
    
    # 1. Fix letter-spaced names
    spaced_names = {
        "Al ex an de rB oh lig": "Alexander Bohlig",
        "Al ex an de r B oh lig": "Alexander Bohlig",
        "Fr ed er ik W isse": "Frederik Wisse",
        "J am es M. R o bin so n": "James M. Robinson",
        "D ieter M u eller": "Dieter Mueller",
        "H elm u t K oester": "Helmut Koester",
        "G om orrah": "Gomorrah",
    }
    for spaced, fixed in spaced_names.items():
        text = text.replace(spaced, fixed)
    
    # 2. Remove soft hyphens
    text = text.replace('\u00AD', '')
    
    # 3. Fix "o f" artifact (italic of)
    text = re.sub(r'\bo f\b', 'of', text)
    
    # 4. Remove running headers (ALL CAPS lines that are page headers)
    text = re.sub(r'\n(?:THE GOSPEL OF THE EGYPTIANS|THE NAG HAMMADI LIBRARY IN ENGLISH)[^\n]*\n', '\n', text, flags=re.IGNORECASE)
    
    # 5. Remove bare page numbers (standalone numbers on their own line)
    text = re.sub(r'\n\d{1,3}\s*\n', '\n', text)
    
    # 6. Rejoin words broken across lines with hyphens  
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    # Also rejoin words broken across lines WITHOUT hyphens (line ends mid-word)
    # This is trickier - handle common patterns where a line ends with partial word
    text = re.sub(r'(\w)\s*\n\s*(\w)', r'\1 \2', text)
    
    # 7. Fix quotation spacing
    text = re.sub(r'"\s+(\w)', r'"\1', text)
    text = re.sub(r'(\w)\s+"', r'\1"', text)
    
    # 8. Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 9. Clean up spaces before punctuation
    text = re.sub(r'\s+([,.])', r'\1', text)
    
    return text


def reformat_tractate(raw_path: Path) -> str:
    """Read raw file, clean it, and reformat with blockquote intro."""
    content = raw_path.read_text(encoding='utf-8')
    
    # Split into sections based on the --- separator
    parts = content.split('---', 1)
    if len(parts) < 2:
        return clean_text(content)
    
    header = parts[0].strip()
    rest = parts[1].strip()
    
    # Find where the introduction ends and text begins
    # The text starts with the manuscript references like "III 40, 12-44, 28"
    intro_match = re.search(r'\n\s*(III\s+\d+)', rest)
    if intro_match:
        intro_raw = rest[:intro_match.start()].strip()
        text_raw = rest[intro_match.start():].strip()
    else:
        intro_raw = ""
        text_raw = rest
    
    # Clean intro - remove the "Introduced and translated by" line with spaced names
    intro_clean = clean_text(intro_raw)
    # Remove redundant "Introduced and translated by" line (already in header)
    intro_clean = re.sub(r'^Introduced and translated by\s+.*?\n', '', intro_clean, flags=re.MULTILINE)
    intro_clean = intro_clean.strip()
    
    # Clean text
    text_clean = clean_text(text_raw)
    
    # Build blockquote intro
    intro_lines = []
    intro_lines.append("> **Editor's Introduction**")
    intro_lines.append(">")
    intro_lines.append("> Introduced and translated by Alexander Bohlig and Frederik Wisse")
    intro_lines.append(">")
    for para in re.split(r'\n\s*\n', intro_clean):
        para = para.strip()
        if para:
            # Wrap paragraph in blockquote
            intro_lines.append(f"> {para}")
            intro_lines.append(">")
    # Remove trailing empty blockquote
    if intro_lines and intro_lines[-1] == ">":
        intro_lines.pop()
    
    intro_block = '\n'.join(intro_lines)
    
    # Rebuild header with proper spacing
    header_clean = clean_text(header)
    
    # Build final document
    output = f"""{header_clean}

{intro_block}

---

{text_clean}
"""
    return output


if __name__ == "__main__":
    raw_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output/tractates/III_2_gospel_egyptians.md")
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output/cleaned/tractates/III_2_gospel_egyptians.md")
    
    result = reformat_tractate(raw_path)
    out_path.write_text(result, encoding='utf-8')
    print(f"Cleaned: {raw_path} -> {out_path}")
    print(f"Size: {len(result)} chars")
