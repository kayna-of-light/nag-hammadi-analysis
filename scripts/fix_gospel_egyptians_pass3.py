#!/usr/bin/env python3
"""Third pass: Remove remaining straight-apostrophe verse markers (U+0027)."""
from pathlib import Path
import re

F = Path(r"C:\Users\mlf\source\temp\NagHammadiLIbrary\output\cleaned\tractates\III_2_gospel_egyptians.md")
text = F.read_text(encoding="utf-8")
orig = len(text)

# Remove '. ' or '.' at end of paragraph lines (verse marker after sentence-final period)
# Pattern: `. '` followed by newline  →  `.` + newline
text = re.sub(r"\. '\s*$", ".", text, flags=re.MULTILINE)

# Remove `]. '` at end  →  `].`
text = re.sub(r"\]\. '\s*$", "].", text, flags=re.MULTILINE)

# Remove `'` before a word after space/comma (verse marker before name/word)
# But NOT in possessives like "Adamas'" or "Editor's"
# Verse markers: space + ' + uppercase/lowercase letter
# Possessives: letter + ' + space/end
VERSE_MARKER_REMOVALS = [
    ("uu[uuu] 'uuuuuuuuuuuuuuuuu", "uu[uuu] uuuuuuuuuuuuuuuuu"),
    ("] and 'incorruptions", "] and incorruptions"),
    ("man 'Adamas mingled", "man Adamas mingled"),
    ("of 'Sodom. Some", "of Sodom. Some"),
    ("bosom, 'and (through)", "bosom, and (through)"),
    ("Sesengenpharanges, 'and", "Sesengenpharanges, and"),
    ("and 'Heurumaious", "and Heurumaious"),
    ("fourth, 'Eleleth", "fourth, Eleleth"),
    ("truly, 'aion o on", "truly, aion o on"),
]

fixes = 0
for old, new in VERSE_MARKER_REMOVALS:
    if old in text:
        text = text.replace(old, new, 1)
        fixes += 1
        print(f"  Fixed: {old[:50]}")
    else:
        print(f"  NOT FOUND: {old[:50]}")

# Clean double spaces
while "  " in text:
    text = text.replace("  ", " ")

F.write_text(text, encoding="utf-8")

# Verify remaining apostrophes
remaining = [(i, line) for i, line in enumerate(text.split("\n"), 1) if "'" in line]
print(f"\nDone: {orig} -> {len(text)} chars, {fixes} exact fixes")
print(f"Remaining lines with apostrophes ({len(remaining)}):")
for ln, line in remaining:
    idx = line.index("'")
    ctx = line[max(0, idx-15):idx+15]
    print(f"  L{ln}: ...{ctx}...")
