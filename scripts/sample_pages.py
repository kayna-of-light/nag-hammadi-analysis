#!/usr/bin/env python3
"""Extract sample pages from the NHL PDF to understand structure."""
import fitz

PDF_PATH = "data/The Nag Hammadi Library. The Definitive Translation of the Gnostic Scriptures Complete in One Volume.pdf"

doc = fitz.open(PDF_PATH)
print(f"Total pages: {len(doc)}")

# Print first 20 pages to understand structure
for i in range(min(20, len(doc))):
    text = doc[i].get_text()
    print(f"\n{'='*60}")
    print(f"=== PAGE {i+1} ===")
    print(f"{'='*60}")
    print(text[:800])
