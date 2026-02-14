#!/usr/bin/env python3
"""Extract targeted pages to understand tractate headers and page offsets."""
import fitz

PDF_PATH = "data/The Nag Hammadi Library. The Definitive Translation of the Gnostic Scriptures Complete in One Volume.pdf"

doc = fitz.open(PDF_PATH)

# Full TOC pages (5-8)
print("=" * 60)
print("FULL TABLE OF CONTENTS (pages 5-8)")
print("=" * 60)
for i in range(4, 8):
    text = doc[i].get_text()
    print(f"\n--- PDF PAGE {i+1} ---")
    print(text)

# Full tractate table (pages 13-14)
print("\n" + "=" * 60)
print("FULL TRACTATE TABLE (pages 13-14)")
print("=" * 60)
for i in range(12, 14):
    text = doc[i].get_text()
    print(f"\n--- PDF PAGE {i+1} ---")
    print(text)

# Pages around where first tractate should be (book page 27 => ~PDF page 43)
print("\n" + "=" * 60)
print("FIRST TRACTATE AREA (PDF pages 40-50)")
print("=" * 60)
for i in range(39, 50):
    text = doc[i].get_text()
    print(f"\n--- PDF PAGE {i+1} ---")
    print(text[:600])

# Check one more tractate boundary — Gospel of Thomas should be at book page 124 => ~PDF page 140
print("\n" + "=" * 60)
print("GOSPEL OF THOMAS AREA (PDF pages 138-145)")
print("=" * 60)
for i in range(137, 145):
    text = doc[i].get_text()
    print(f"\n--- PDF PAGE {i+1} ---")
    print(text[:600])
