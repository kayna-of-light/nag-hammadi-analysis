#!/usr/bin/env python3
"""
Second pass of targeted fixes for Gospel of Egyptians.

Addresses remaining issues after clean_from_di.py and fix_gospel_egyptians.py:
1. Remove verse/line marker apostrophes (RIGHT SINGLE QUOTATION MARK U+2019, SALTILLO U+A78C)
2. Remove remaining embedded line/page reference numbers
3. Fix vowel string OCR artifacts (0→o, hyphen joins, formatting)
4. Fix '. !' OCR artifact (! misread of ')
5. Remove stray 'I' OCR artifacts of verse markers
6. Clean up resulting whitespace
"""

from pathlib import Path
import re

INPUT = Path(r"C:\Users\mlf\source\temp\NagHammadiLIbrary\output\cleaned\tractates\III_2_gospel_egyptians.md")


def fix_file():
    text = INPUT.read_text(encoding="utf-8")
    original_len = len(text)
    fixes_applied = 0

    def apply(old: str, new: str, desc: str = ""):
        nonlocal text, fixes_applied
        if old in text:
            text = text.replace(old, new, 1)
            fixes_applied += 1
            print(f"  \u2713 {desc or old[:60]}")
        else:
            print(f"  \u2717 NOT FOUND: {desc or old[:60]}")

    # === DIAGNOSTICS: What quote chars are present? ===
    print("=== Character diagnostics ===")
    for char, name in [
        ("\u0027", "APOSTROPHE U+0027"),
        ("\u2018", "LEFT SINGLE QUOTATION MARK U+2018"),
        ("\u2019", "RIGHT SINGLE QUOTATION MARK U+2019"),
        ("\u02BC", "MODIFIER LETTER APOSTROPHE U+02BC"),
        ("\uA78C", "LATIN SMALL LETTER SALTILLO U+A78C"),
    ]:
        count = text.count(char)
        if count > 0:
            print(f"  Found {count} x {name}")

    # === PHASE 1: Vowel string fixes (exact replacements, before global char removal) ===
    print("\n=== Phase 1: Vowel string fixes ===")

    # Main vowel string paragraph (line ~45)
    apply('[A] \u201c hidden', "[A] hidden", "Remove stray left double quote before 'hidden'")
    # Try alternate quote character
    apply('[A] " hidden', "[A] hidden", "Remove stray straight double quote before 'hidden'")

    apply(
        "\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113- \u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113",
        "\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113\u0113",
        "Join hyphenated \u0113 sequence",
    )

    apply(
        "[\u0113\u0113 o ] > 000000000000000000000",
        "[\u0113\u0113] ooooooooooooooooooooo",
        "Fix \u0113\u0113 brackets, remove > artifact, 0\u21920",
    )
    # If the above didn't match, try with the > as separate
    apply(
        "[\u0113\u0113 o ] >",
        "[\u0113\u0113]",
        "Fix \u0113\u0113 brackets and > artifact (alt)",
    )

    # Replace zeros with o in the vowel string
    apply(
        "000000000000000000000",
        "ooooooooooooooooooooo",
        "Replace zeros with o in vowel string",
    )

    apply(
        "uuuuuuuuuuuu- uuuuu",
        "uuuuuuuuuuuuuuuuu",
        "Join hyphenated u sequence",
    )

    apply(
        "[aaaa] 1 aaaa",
        "[aaaa] aaaa",
        "Remove line number 1 from a string",
    )

    apply(
        "\u014D\u014D\u00F5\u014D\u014D\u014D\u014D\u014D\u014D",
        "\u014D\u014D\u014D\u014D\u014D\u014D\u014D\u014D\u014D",
        "Fix \u00F5 \u2192 \u014D in \u014D sequence",
    )

    # Doxology vowel string (near end of text, lines ~159)
    apply("oo 1 00 uuuu 000\u014D", "oooo uuuu ooo\u014D", "Dox: fix zeros, remove 1")
    apply("00 1 00, O existing", "oooo, O existing", "Dox: fix zeros, remove 1 (2)")

    # === PHASE 2: Remove ALL verse marker characters globally ===
    print("\n=== Phase 2: Remove verse marker characters ===")

    count_2019 = text.count("\u2019")
    if count_2019 > 0:
        text = text.replace("\u2019", "")
        fixes_applied += count_2019
        print(f"  \u2713 Removed {count_2019} x U+2019 (RIGHT SINGLE QUOTATION MARK)")
    else:
        print("  No U+2019 found")

    count_a78c = text.count("\uA78C")
    if count_a78c > 0:
        text = text.replace("\uA78C", "")
        fixes_applied += count_a78c
        print(f"  \u2713 Removed {count_a78c} x U+A78C (SALTILLO)")
    else:
        print("  No U+A78C found")

    # === PHASE 3: Fix `. !` OCR artifact (! misread of ') ===
    print("\n=== Phase 3: Fix OCR artifacts ===")
    count_bang = text.count(". !")
    if count_bang > 0:
        text = text.replace(". !", ".")
        fixes_applied += count_bang
        print(f"  \u2713 Fixed {count_bang} x `. !` \u2192 `.`")

    # === PHASE 4: Remove embedded line/page reference numbers ===
    print("\n=== Phase 4: Remove embedded line/page numbers ===")

    # --- First half (lines ~30-55) ---
    apply("who] 15 presides", "who] presides", "Line ref 15 near 'presides'")
    apply("he is 15 [the great]", "he is [the great]", "Line ref 15 near 'the great'")
    apply("[whose] 25 power", "[whose] power", "Line ref 25 near 'power'")
    apply("[ ... ] 56 which", "[ ... ] which", "Page ref 56 near 'which'")
    apply("greatness 5 [of]", "greatness [of]", "Line ref 5 near '[of]'")
    # fallback without 'greatness' prefix
    apply(" 5 [of] the silence", " [of] the silence", "Line ref 5 near 'silence' (alt)")
    apply("[great, 10 invisible", "[great, invisible", "Line ref 10 near 'invisible'")
    apply("] 21 him", "] him", "Line ref 21 near 'him'")
    apply("] 25 myriads", "] myriads", "Line ref 25 near 'myriads'")
    apply("... 13 who]", "... who]", "Line ref 13 near 'who'")
    apply("] 18 eternal", "] eternal", "Line ref 18 near 'eternal'")
    apply("five] 59 seals", "five] seals", "Page ref 59 near 'seals'")
    apply("and 15 all the]", "and all the]", "Line ref 15 near 'all the'")

    # --- Second half (lines ~55-142) ---
    apply("from 10 the light", "from the light", "Line ref 10 near 'the light'")
    apply("great 5 Doxomedon-aeon", "great Doxomedon-aeon", "Line ref 5 near 'Doxomedon'")
    apply("great 25 Samlo", "great Samlo", "Line ref 25 near 'Samlo'")
    apply("one, 5 the first", "one, the first", "Line ref 5 near 'the first'")
    apply("placed 15 in the cloud", "placed in the cloud", "Line ref 15 near 'cloud'")
    apply("called] 15 Sabaoth", "called] Sabaoth", "Line ref 15 near 'Sabaoth'")
    apply("of the 5 corrupted", "of the corrupted", "Line ref 5 near 'corrupted'")
    apply("world 5 because", "world because", "Line ref 5 near 'because'")
    apply("to 1 guard", "to guard", "Line ref 1 near 'guard'")
    apply("really 15 truly", "really truly", "Line ref 15 near 'truly'")
    apply("eternity. 5 Amen", "eternity. Amen", "Line ref 5 near 'Amen'")

    # === PHASE 5: Remove stray 'I' OCR artifacts ===
    print("\n=== Phase 5: Remove 'I' OCR artifacts ===")
    apply("the I glorious", "the glorious", "'I' artifact near 'glorious'")
    apply("Adamas, I the second", "Adamas, the second", "'I' artifact near 'the second'")

    # === PHASE 6: Clean up whitespace ===
    print("\n=== Phase 6: Clean up whitespace ===")

    # Double spaces from removals
    rounds = 0
    while "  " in text:
        text = text.replace("  ", " ")
        rounds += 1
    if rounds > 0:
        print(f"  \u2713 Collapsed double spaces ({rounds} rounds)")

    # Trailing spaces on lines
    text = re.sub(r" +$", "", text, flags=re.MULTILINE)
    print("  \u2713 Removed trailing spaces")

    # Triple+ newlines → double
    text = re.sub(r"\n{3,}", "\n\n", text)
    print("  \u2713 Collapsed triple newlines")

    # Space before punctuation (at word boundary only, not in `. . .` lacunae)
    # Only fix: `word ,` or `word .` followed by space+letter (not `.`)
    text = re.sub(r"(\w) ,", r"\1,", text)
    print("  \u2713 Fixed 'word ,' patterns")

    INPUT.write_text(text, encoding="utf-8")
    print(f"\nDone: {original_len} \u2192 {len(text)} chars ({fixes_applied} fixes applied)")


if __name__ == "__main__":
    fix_file()
