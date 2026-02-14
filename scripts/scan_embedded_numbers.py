#!/usr/bin/env python3
"""
Scan all cleaned tractate files for suspected embedded manuscript line/page numbers.

Manuscript line numbers typically appear as:
- Standalone numbers 1-35 (line numbers within a codex page)
- Numbers at multiples of 5 (5, 10, 15, 20, 25, 30, 35) are most common
- Page numbers (larger numbers, often at paragraph boundaries)

Pattern: ` N ` or ` N\n` where N is a small integer that doesn't belong grammatically.

This script identifies candidates and reports per-file statistics.
"""

import re
from pathlib import Path

TRACTATES_DIR = Path(r"C:\Users\mlf\source\temp\NagHammadiLIbrary\output\cleaned\tractates")

# Numbers that are commonly line markers (multiples of 5, plus 1)
LINE_NUMBER_PATTERN = re.compile(
    r'(?<=[a-zA-Z\]\),:;.!?\u2019\u201d]) '  # preceded by text char + space
    r'(\d{1,2}) '                                # 1-2 digit number + space
    r'(?=[a-zA-Z\[\(<"\u201c])',                 # followed by space + text char
    re.UNICODE
)

# Also catch numbers before newline (end-of-line markers)
LINE_NUMBER_EOL_PATTERN = re.compile(
    r'(?<=[a-zA-Z\]\),:;.!?\u2019\u201d]) '
    r'(\d{1,2})\s*$',
    re.MULTILINE
)

# Numbers that are likely legitimate (spelled out or in context)
SKIP_CONTEXTS = [
    # Common legitimate numbers in these texts
    "saying", "114", "200", "1990", "100", "400",
    "Codex", "III", "IV", "II", "VII", "VIII",
]


def scan_file(filepath: Path) -> dict:
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    
    # Skip the header (metadata + introduction blockquote)
    body_start = 0
    in_blockquote = False
    past_separator = False
    for i, line in enumerate(lines):
        if line.strip() == "---":
            past_separator = True
            body_start = i + 1
            break
    
    if not past_separator:
        body_start = 0
    
    body_text = "\n".join(lines[body_start:])
    
    # Find all candidate embedded numbers
    candidates = []
    
    for match in LINE_NUMBER_PATTERN.finditer(body_text):
        num = int(match.group(1))
        if num > 50:  # Too large for line numbers
            continue
        # Get surrounding context
        start = max(0, match.start() - 30)
        end = min(len(body_text), match.end() + 30)
        context = body_text[start:end].replace("\n", " ")
        candidates.append((num, match.start(), context))
    
    for match in LINE_NUMBER_EOL_PATTERN.finditer(body_text):
        num = int(match.group(1))
        if num > 50:
            continue
        start = max(0, match.start() - 30)
        end = min(len(body_text), match.end() + 30)
        context = body_text[start:end].replace("\n", " ")
        candidates.append((num, match.start(), context))
    
    # Count by number value
    number_counts = {}
    for num, pos, ctx in candidates:
        number_counts[num] = number_counts.get(num, 0) + 1
    
    return {
        "file": filepath.name,
        "total_candidates": len(candidates),
        "number_distribution": dict(sorted(number_counts.items())),
        "samples": candidates[:10],  # First 10 for review
        "body_length": len(body_text),
    }


def main():
    files = sorted(TRACTATES_DIR.glob("*.md"))
    
    print(f"Scanning {len(files)} tractate files...\n")
    
    results = []
    for f in files:
        result = scan_file(f)
        results.append(result)
    
    # Sort by total candidates (worst first)
    results.sort(key=lambda r: r["total_candidates"], reverse=True)
    
    print(f"{'File':<45} {'Candidates':>10}  Number Distribution")
    print("-" * 120)
    
    affected = 0
    for r in results:
        if r["total_candidates"] > 0:
            affected += 1
            dist = r["number_distribution"]
            # Show which numbers appear most
            top_nums = sorted(dist.items(), key=lambda x: x[1], reverse=True)[:8]
            dist_str = ", ".join(f"{n}×{c}" for n, c in top_nums)
            print(f"{r['file']:<45} {r['total_candidates']:>10}  {dist_str}")
    
    print(f"\n{affected}/{len(files)} files have suspected embedded numbers\n")
    
    # Show detailed samples for worst files
    for r in results[:5]:
        if r["total_candidates"] > 5:
            print(f"\n=== {r['file']} ({r['total_candidates']} candidates) ===")
            for num, pos, ctx in r["samples"]:
                print(f"  [{num:>2}] ...{ctx}...")


if __name__ == "__main__":
    main()
