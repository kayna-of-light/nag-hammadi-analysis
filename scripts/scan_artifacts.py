#!/usr/bin/env python3
"""Scan all extracted tractates for common artifact patterns."""
import re
from pathlib import Path
from collections import Counter

TRACTATE_DIR = Path("output/tractates")
FRONT_MATTER_DIR = Path("output/front_matter")

artifacts = Counter()

for md_file in sorted(TRACTATE_DIR.glob("*.md")):
    text = md_file.read_text(encoding="utf-8")
    fname = md_file.name
    
    # 1. Soft hyphens (U+00AD)
    sh_count = text.count('\u00AD')
    if sh_count:
        artifacts['soft_hyphens'] += sh_count
    
    # 2. Spaced page numbers (like "2 9 6" or "5 9" on own line)
    spaced_nums = re.findall(r'^\d(?: \d){1,3}\s*$', text, re.MULTILINE)
    if spaced_nums:
        artifacts['spaced_page_numbers'] += len(spaced_nums)
        if len(spaced_nums) <= 3:
            print(f"  [{fname}] Spaced page nums: {spaced_nums}")
    
    # 3. ALL CAPS running headers (> 15 chars, mostly uppercase)
    for line in text.split('\n'):
        stripped = line.strip()
        if len(stripped) > 15:
            alpha = [c for c in stripped if c.isalpha()]
            if len(alpha) > 10:
                upper_ratio = sum(1 for c in alpha if c.isupper()) / len(alpha)
                if upper_ratio > 0.8 and not stripped.startswith('#') and not stripped.startswith('**'):
                    artifacts['all_caps_headers'] += 1
    
    # 4. Italic "o f" pattern
    of_count = len(re.findall(r'\bo f\b', text))
    if of_count:
        artifacts['italic_of'] += of_count
    
    # 5. Quote spacing: " word or word "  
    open_quote_space = len(re.findall(r'" \w', text))
    close_quote_space = len(re.findall(r'\w "', text))
    artifacts['open_quote_space'] += open_quote_space
    artifacts['close_quote_space'] += close_quote_space
    
    # 6. Letter-spaced names (single char, space, single char patterns in name-like contexts)
    name_lines = re.findall(r'^[A-Z](?: [a-z]){2,}', text, re.MULTILINE)
    if name_lines:
        artifacts['letter_spaced_names'] += len(name_lines)
        if len(name_lines) <= 2:
            print(f"  [{fname}] Letter-spaced: {name_lines[:2]}")

    # 7. Look for common OCR issues
    # Double spaces
    dbl_spaces = len(re.findall(r'(?<!\n) {2,}(?!\n)', text))
    artifacts['double_spaces'] += dbl_spaces


print("\n=== ARTIFACT SUMMARY ===")
for artifact, count in artifacts.most_common():
    print(f"  {artifact}: {count}")

# Show some specific examples
print("\n=== SAMPLE ALL-CAPS LINES ===")
sample_file = TRACTATE_DIR / "II_2_gospel_thomas.md"
text = sample_file.read_text(encoding="utf-8")
for line in text.split('\n'):
    stripped = line.strip()
    if len(stripped) > 15:
        alpha = [c for c in stripped if c.isalpha()]
        if len(alpha) > 10:
            upper_ratio = sum(1 for c in alpha if c.isupper()) / len(alpha)
            if upper_ratio > 0.8 and not stripped.startswith('#') and not stripped.startswith('**'):
                print(f"  >>> {stripped[:80]}")

print("\n=== SAMPLE SOFT HYPHEN CONTEXTS ===")
for m in list(re.finditer(r'\w{2}\u00AD\w{2}', text))[:5]:
    start = max(0, m.start()-10)
    end = min(len(text), m.end()+10)
    print(f"  ...{repr(text[start:end])}...")

print("\n=== SAMPLE ITALIC 'o f' CONTEXTS ===")
for m in list(re.finditer(r'\bo f\b', text))[:8]:
    start = max(0, m.start()-15)
    end = min(len(text), m.end()+15)
    print(f"  ...{text[start:end]}...")
