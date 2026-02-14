#!/usr/bin/env python3
"""
Clean NHL tractate markdown files using GPT-5.2 to produce properly formatted output.

Reads each raw extracted markdown file, sends it to GPT-5.2 via Azure Foundry with
instructions to clean OCR/PDF artifacts while preserving the exact scholarly text,
and writes the cleaned version to output/cleaned/.

Usage:
    python scripts/clean_with_claude.py                     # Process all files
    python scripts/clean_with_claude.py --file tractates/II_2_gospel_thomas.md  # Single file
    python scripts/clean_with_claude.py --dry-run           # Show what would be processed
    python scripts/clean_with_claude.py --overwrite         # Reprocess already-cleaned files
"""
import argparse
import json
import sys
import time
from pathlib import Path

from openai import OpenAI
from dotenv import dotenv_values

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SECRETS_PATH = PROJECT_ROOT / "secrets" / "azure_openai.env"
RAW_DIR = PROJECT_ROOT / "output"
CLEANED_DIR = PROJECT_ROOT / "output" / "cleaned"

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a scholarly text editor specializing in ancient religious texts. You are \
given a raw markdown file extracted from a PDF of *The Nag Hammadi Library in English* \
(Robinson, 3rd ed., 1990). The extraction introduced various artifacts that need cleaning.

Your task: produce a clean, properly formatted markdown version of the EXACT SAME TEXT. \
You are not rewriting, summarizing, or interpreting. You are restoring the text to what \
the printed book actually says, removing only artifacts of the PDF-to-text extraction process.

## ARTIFACTS TO FIX

1. **Letter-spaced names**: PDF rendered some names with spaces between letters. \
   Example: "D ieter M u eller" → "Dieter Mueller", "H elm u t K oester" → "Helmut Koester", \
   "F r e d e r ik W isse" → "Frederik Wisse". Restore the proper name.

2. **Broken words from line/page breaks**: Words split across lines without hyphens. \
   Example: "collec\\ntion" → "collection", "lan\\nguage" → "language". Rejoin them.

3. **Soft hyphens / formatting hyphens**: Remove invisible soft-hyphen characters (\\u00AD). \
   Where a word was hyphenated across a line break, rejoin the word.

4. **Running headers**: Remove repeated page headers like "THE NAG HAMMADI LIBRARY IN ENGLISH" \
   or the tractate title in ALL CAPS that appear at page boundaries \
   (e.g. "THE GOSPEL OF THOMAS ( il,2 )"). These are page-turn artifacts, not part of the text.

5. **Bare page numbers**: Remove standalone page numbers that appear between paragraphs.

6. **Embedded Coptic manuscript line numbers**: The critical edition prints small line numbers \
   (1, 5, 10, 15, 20, 25, 30, 35) in the running text to mark line positions in the Coptic \
   manuscript. These appear as bare numbers interrupting the English text, e.g. \
   "Let him who seeks continue seeking until he 1 finds" or "said to him, 35 You are like a \
   wise philosopher". REMOVE ALL of these embedded line numbers. They are typographic \
   apparatus, not part of the translated text. Also remove Coptic manuscript page numbers \
   that appear inline (e.g. "33", "34", "35" as standalone numbers marking manuscript page \
   boundaries). The ONLY numbers to preserve are: saying numbers in texts like Gospel of Thomas \
   (which you format as **(1)**, **(2)**, etc.), numbers that are part of the actual content \
   ("five thousand years", "twelve aeons", "114 sayings"), and codex references in the \
   header/introduction.

7. **Italic "of" artifacts**: The PDF sometimes renders italic "of" as "o f" with a space. \
   Fix: "o f" → "of" (but only where this is clearly an artifact, not intentional spacing).

8. **Quotation spacing**: The PDF sometimes adds a space after opening quotes or before \
   closing quotes: '" word' → '"word'. Clean these up.

9. **Excessive line breaks**: Collapse multiple blank lines to at most one blank line \
   between paragraphs.

## STRUCTURE TO PRODUCE

The translated text IS the primary content. The scholarly introduction is secondary \
apparatus. Return a clean markdown document with this structure:

```
# [Tractate Title]

**Codex Reference**: [ref]  
**Translated by**: [names — properly spelled]  
**Source**: Robinson, J.M. (ed.), *The Nag Hammadi Library in English*, \
3rd rev. ed. (HarperSanFrancisco, 1990), p. [N]ff.

> **Editor's Introduction**
>
> [The scholarly introduction as a blockquote. Keep all content, citations, \
cross-references. Just clean the artifacts. Each paragraph is a separate \
blockquote paragraph (blank `>` line between them).]

---

[The actual translated text of the tractate, presented as the primary body \
of the document. Format it with proper markdown to make it readable:

- Use paragraph breaks between natural units of text
- For texts with numbered sayings (e.g. Gospel of Thomas), put each saying \
  as its own paragraph with the saying number in bold: **(1)**, **(2)**, etc.
- For texts with clear structural divisions (steles, chapters, sections), \
  use ### subheadings where the text itself signals them
- Preserve ALL textual apparatus: lacuna markers [...], editorial insertions \
  in (parentheses), alternative readings — but REMOVE embedded line numbers \
  (bare numbers 1-35 interrupting the running text)
- Make the text breathe — a reader should be able to sit down and read this \
  as a text, not parse a wall of undifferentiated prose]
```

## CRITICAL RULES

- **DO NOT alter the content of the translation.** Every word of the translated text \
  must be preserved exactly. You are only fixing extraction artifacts.
- **DO NOT remove textual apparatus** — lacuna brackets [...], editorial notes in \
  parentheses, alternative readings (or: ...). BUT DO remove embedded line numbers \
  (bare numbers 1-35 appearing in the running text) as described above.
- **DO NOT confuse line numbers with content numbers** — "five thousand" stays, \
  "the twelve aeons" stays, saying numbers stay. Only bare numbers that interrupt \
  the flow of English text are line-number artifacts.
- **DO NOT add commentary or interpretation.**
- **DO NOT change British/American spelling variants** in the translation.
- **DO preserve cross-references** to other tractates (e.g., "cf. Gos. Thom. 13").
- The scholarly introduction goes in a blockquote. The text stands on its own below the rule.
- For the Afterword and front matter (which have no "translated text"), just clean \
  the artifacts and format as clean markdown with appropriate section headers.
- Output ONLY the cleaned markdown. No preamble, no explanation, no code fences.\
"""

# ---------------------------------------------------------------------------
# Client setup
# ---------------------------------------------------------------------------

def create_client() -> OpenAI:
    """Create OpenAI client configured for Azure Foundry."""
    if not SECRETS_PATH.exists():
        print(f"ERROR: Secrets file not found at {SECRETS_PATH}")
        sys.exit(1)

    config = dotenv_values(SECRETS_PATH)
    return OpenAI(
        base_url=config["OPENAI_ENDPOINT"],
        api_key=config["OPENAI_API_KEY"],
    )


def get_deployment() -> str:
    """Get the model deployment name."""
    config = dotenv_values(SECRETS_PATH)
    return config["OPENAI_DEPLOYMENT"]


# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------

def clean_file(client: OpenAI, deployment: str, raw_path: Path) -> str:
    """Send a raw markdown file to GPT-5.2 for cleaning. Uses streaming with retry."""
    raw_text = raw_path.read_text(encoding="utf-8")

    user_msg = (
        "I am a scholar preparing a critical edition of the Nag Hammadi Library "
        "for academic study. The following file was extracted from a PDF and contains "
        "OCR/extraction artifacts. Please clean it according to the formatting "
        "instructions in your system prompt. This is purely an editorial/typesetting "
        "task on a published academic text.\n\n"
        f"{raw_text}"
    )

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            result_parts = []
            finish_reason = None
            stream = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                max_completion_tokens=65536,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        result_parts.append(delta.content)
                    if chunk.choices[0].finish_reason:
                        finish_reason = chunk.choices[0].finish_reason

            if finish_reason and finish_reason != "stop":
                print(f"[finish_reason={finish_reason}]", end=" ", flush=True)

            if finish_reason == "content_filter" and attempt < max_retries:
                wait = attempt * 5
                print(f"(filter hit, retry {attempt}/{max_retries} in {wait}s)...",
                      end=" ", flush=True)
                time.sleep(wait)
                continue

            return "".join(result_parts)

        except Exception as e:
            err_str = str(e)
            if "content_filter" in err_str.lower() and attempt < max_retries:
                wait = attempt * 5
                print(f"(filter hit, retry {attempt}/{max_retries} in {wait}s)...",
                      end=" ", flush=True)
                time.sleep(wait)
                continue
            raise


def process_file(
    client: OpenAI,
    deployment: str,
    rel_path: Path,
    overwrite: bool = False,
) -> bool:
    """Process a single file. Returns True if processed, False if skipped."""
    raw_path = RAW_DIR / rel_path
    cleaned_path = CLEANED_DIR / rel_path

    if not raw_path.exists():
        print(f"  SKIP (not found): {rel_path}")
        return False

    if cleaned_path.exists() and not overwrite:
        print(f"  SKIP (exists): {rel_path}")
        return False

    print(f"  Processing: {rel_path} ({raw_path.stat().st_size:,} bytes)...", end=" ", flush=True)

    try:
        cleaned = clean_file(client, deployment, raw_path)
        cleaned_path.parent.mkdir(parents=True, exist_ok=True)
        cleaned_path.write_text(cleaned, encoding="utf-8")
        print(f"OK ({len(cleaned):,} chars)")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def collect_files() -> list[Path]:
    """Collect all markdown files to process, in order."""
    files = []

    # Front matter
    fm_dir = RAW_DIR / "front_matter"
    if fm_dir.exists():
        files.extend(sorted(p.relative_to(RAW_DIR) for p in fm_dir.glob("*.md")))

    # Tractates
    tr_dir = RAW_DIR / "tractates"
    if tr_dir.exists():
        files.extend(sorted(p.relative_to(RAW_DIR) for p in tr_dir.glob("*.md")))

    return files


def main():
    parser = argparse.ArgumentParser(description="Clean NHL tractates with Claude")
    parser.add_argument("--file", type=str, help="Process a single file (relative to output/)")
    parser.add_argument("--dry-run", action="store_true", help="List files without processing")
    parser.add_argument("--overwrite", action="store_true", help="Reprocess existing files")
    args = parser.parse_args()

    if args.file:
        files = [Path(args.file)]
    else:
        files = collect_files()

    if not files:
        print("No files to process.")
        return

    print(f"Files to process: {len(files)}")

    if args.dry_run:
        for f in files:
            raw_path = RAW_DIR / f
            cleaned_path = CLEANED_DIR / f
            status = "EXISTS" if cleaned_path.exists() else "PENDING"
            size = raw_path.stat().st_size if raw_path.exists() else 0
            print(f"  [{status}] {f} ({size:,} bytes)")
        return

    client = create_client()
    deployment = get_deployment()

    processed = 0
    skipped = 0
    errors = 0
    start_time = time.time()

    for i, f in enumerate(files, 1):
        print(f"[{i}/{len(files)}]", end=" ")
        try:
            if process_file(client, deployment, f, overwrite=args.overwrite):
                processed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  FATAL ERROR on {f}: {e}")
            errors += 1

        # Brief pause between API calls to avoid rate limiting
        if i < len(files):
            time.sleep(1)

    elapsed = time.time() - start_time
    print(f"\nDone in {elapsed:.1f}s — Processed: {processed}, Skipped: {skipped}, Errors: {errors}")


if __name__ == "__main__":
    main()
