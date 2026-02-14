#!/usr/bin/env python3
"""
Post-process extracted NHL tractate files to clean up PDF artifacts.

Fixes:
  1. Soft hyphens (U+00AD) — removed to rejoin hyphenated words
  2. Running headers — ALL CAPS tractate titles at page breaks
  3. Spaced page numbers — digits separated by spaces (e.g. "2 9 6")
  4. Italic "o f" — OCR artifact from italic rendering in title references
  5. Letter-spaced translator names — collapsed to normal spacing
  6. Stray bare page numbers — leftover from page breaks
"""
import re
import json
from pathlib import Path

OUTPUT_DIR = Path("output")
TRACTATE_DIR = OUTPUT_DIR / "tractates"
FRONT_MATTER_DIR = OUTPUT_DIR / "supplementary"


# ---------------------------------------------------------------------------
# Artifact fixers
# ---------------------------------------------------------------------------

def fix_soft_hyphens(text: str) -> str:
    """Remove soft hyphens (U+00AD) used for line-break hyphenation."""
    return text.replace('\u00AD', '')


def fix_spaced_page_numbers(text: str) -> str:
    """Remove lines that are spaced-out page numbers like '2 9 6' or '5 9'."""
    return re.sub(r'^\d(?: \d){1,3}\s*$', '', text, flags=re.MULTILINE)


def fix_bare_page_numbers(text: str) -> str:
    """Remove standalone page numbers (1-3 digits) on their own line."""
    # Only match if the line before or after is blank (page boundary context)
    return re.sub(r'(?<=\n)\n\d{1,3}\n(?=\n)', '\n\n', text)


def fix_running_headers(text: str) -> str:
    """Remove ALL CAPS running headers that appear at page breaks.
    
    These look like:
      THE GOSPEL OF THOMAS ( il,2 )
      THE TRIPARTITE TRACTATE (i ,5 )
      THE NAG HAMMADI LIBRARY IN ENGLISH
    """
    lines = text.split('\n')
    cleaned = []
    
    for line in lines:
        stripped = line.strip()
        
        # Skip blank lines — keep them
        if not stripped:
            cleaned.append(line)
            continue
        
        # Check if this is a running header
        if _is_running_header(stripped):
            continue
        
        cleaned.append(line)
    
    return '\n'.join(cleaned)


def _is_running_header(line: str) -> bool:
    """Determine if a line is a running header from the book layout."""
    # Must be substantial (not just a word or two in the actual text)
    if len(line) < 15:
        return False
    
    # Skip our own markdown headers and metadata
    if line.startswith('#') or line.startswith('**'):
        return False
    
    # Remove parenthetical codex references for analysis
    base = re.sub(r'\([^)]*\)', '', line).strip()
    
    # Get only alphabetic characters
    alpha_chars = [c for c in base if c.isalpha()]
    if len(alpha_chars) < 8:
        return False
    
    # Check if >80% uppercase
    upper_ratio = sum(1 for c in alpha_chars if c.isupper()) / len(alpha_chars)
    if upper_ratio < 0.80:
        return False
    
    # Additional safety: must look like a title (mostly letters, spaces, colons, digits)
    non_alpha = re.sub(r'[A-Za-z0-9\s:,\-\'\(\)]', '', base)
    if len(non_alpha) > 3:
        return False
    
    return True


def fix_italic_of(text: str) -> str:
    """Fix 'o f' artifact from PDF italic rendering.
    
    In the PDF, italicized book titles render 'of' as 'o f' due to 
    character spacing. Fix when in title-like context.
    """
    # The standalone sequence 'o f' (single-char word "o" + single-char word "f")
    # never occurs in normal English. It is always a PDF artifact from italic
    # character spacing. Safe to replace globally.
    text = re.sub(r'\bo f\b', 'of', text)
    
    return text


def fix_letter_spaced_names(text: str) -> str:
    """Collapse letter-spaced translator names.
    
    These appear after 'Introduced by', 'Translated by', 'Edited by' lines.
    Pattern: 'H a r o ld W. A ttr id g e' → 'Harold W. Attridge'
    """
    # Strategy: find lines after Introduced/Translated/Edited that have 
    # letter-spacing patterns, and collapse single-char-space sequences
    
    lines = text.split('\n')
    result = []
    in_credit_block = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect credit block start
        if re.match(r'^(Introduced|Translated|Edited)\b', stripped):
            in_credit_block = True
            result.append(line)
            continue
        
        # In a credit block, try to collapse letter-spaced names
        if in_credit_block:
            if stripped == '' or stripped.startswith('The ') or stripped.startswith('This '):
                # End of credit block
                in_credit_block = False
                result.append(line)
                continue
            
            collapsed = _collapse_letter_spacing(stripped)
            if collapsed != stripped:
                result.append(collapsed)
            else:
                # If we couldn't collapse, check if this is still a name line
                # (short, starts with capital)
                if len(stripped) < 80 and stripped[0].isupper():
                    result.append(line)
                else:
                    in_credit_block = False
                    result.append(line)
            continue
        
        result.append(line)
    
    return '\n'.join(result)


def _collapse_letter_spacing(text: str) -> str:
    """Collapse letter-spaced text like 'H a r o ld' → 'Harold'.
    
    Heuristic: if a segment has many single chars separated by spaces,
    collapse them. Handle mixed spacing like 'H a r o ld W. A ttr id g e'.
    """
    # Split into words by 2+ spaces (to separate name parts)
    # Then within each part, check for single-char-space patterns
    
    # First try: detect if this looks letter-spaced at all
    # Count single characters separated by single spaces
    single_char_runs = re.findall(r'(?:[A-Za-z] ){2,}', text)
    if not single_char_runs:
        return text
    
    # Collapse: remove spaces between single characters 
    # Pattern: a single letter followed by space followed by single letter
    result = text
    
    # Iteratively collapse single-char spaces
    prev = None
    while prev != result:
        prev = result
        # Collapse single-char + space + single-char
        result = re.sub(r'(?<![A-Za-z])([A-Za-z]) ([A-Za-z])(?![A-Za-z]{2})', r'\1\2', result)
    
    # Also handle remaining artifacts like "ld W." → keep the space before initials
    # Clean up any double spaces
    result = re.sub(r' {2,}', ' ', result)
    
    return result


def fix_known_split_words(text: str) -> str:
    """Fix specific known split-word artifacts from page breaks."""
    splits = {
        'Hypo stasis': 'Hypostasis',
        'Hypos tasis': 'Hypostasis',
        'Configura tions': 'Configurations',
        'Redem ption': 'Redemption',
        'Auto genes': 'Autogenes',
    }
    for broken, fixed in splits.items():
        text = text.replace(broken, fixed)
    return text


def fix_collapsed_blank_lines(text: str) -> str:
    """Collapse runs of 3+ blank lines into 2."""
    return re.sub(r'\n{4,}', '\n\n\n', text)


# ---------------------------------------------------------------------------
# Main processing pipeline
# ---------------------------------------------------------------------------

def process_file(filepath: Path, stats: dict) -> None:
    """Apply all fixes to a single markdown file."""
    original = filepath.read_text(encoding='utf-8')
    text = original
    
    # Apply fixes in order (order matters for some)
    text = fix_soft_hyphens(text)
    text = fix_spaced_page_numbers(text)
    text = fix_running_headers(text)
    text = fix_bare_page_numbers(text)
    text = fix_italic_of(text)
    text = fix_letter_spaced_names(text)
    text = fix_known_split_words(text)
    text = fix_collapsed_blank_lines(text)
    
    if text != original:
        filepath.write_text(text, encoding='utf-8')
        chars_removed = len(original) - len(text)
        stats['files_modified'] += 1
        stats['chars_removed'] += chars_removed
        print(f"  ✓ {filepath.name} ({chars_removed:+d} chars)")
    else:
        print(f"  · {filepath.name} (no changes)")


def main():
    stats = {'files_modified': 0, 'chars_removed': 0, 'files_total': 0}
    
    print("=== Cleaning tractate files ===")
    for md_file in sorted(TRACTATE_DIR.glob("*.md")):
        stats['files_total'] += 1
        process_file(md_file, stats)
    
    print("\n=== Cleaning front matter files ===")
    for md_file in sorted(FRONT_MATTER_DIR.glob("*.md")):
        stats['files_total'] += 1
        process_file(md_file, stats)
    
    print(f"\n--- Summary ---")
    print(f"  Files processed: {stats['files_total']}")
    print(f"  Files modified:  {stats['files_modified']}")
    print(f"  Chars removed:   {stats['chars_removed']:,}")


if __name__ == "__main__":
    main()
