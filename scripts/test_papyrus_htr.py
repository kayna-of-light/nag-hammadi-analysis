#!/usr/bin/env python3
"""Iterative papyrus HTR test with adaptive thinking and prompt optimization.

Tests Claude Opus 4.7 on real Nag Hammadi papyrus photographs with:
- Adaptive thinking enabled (max effort for Opus 4.7)
- System prompt optimization across iterations
- Detailed accuracy analysis with edit distance

Usage:
    python scripts/test_papyrus_htr.py                    # Default: folio 35
    python scripts/test_papyrus_htr.py --folio 36         # Different page
    python scripts/test_papyrus_htr.py --effort max       # Max thinking effort
    python scripts/test_papyrus_htr.py --prompt-version 4 # Diacritics-aware prompt
    python scripts/test_papyrus_htr.py --enhance          # Send enhanced image variants
"""

import argparse
import base64
import difflib
import json
import os
import re
import sys
import time
from pathlib import Path

import io

import httpx
from anthropic import AnthropicFoundry
from dotenv import dotenv_values
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

REPO_ROOT = Path(__file__).resolve().parent.parent
SECRETS_PATH = REPO_ROOT / "secrets" / "azure_openai.env"
COPTIC_GT_DIR = REPO_ROOT / "output" / "coptic"
TEMP_DIR = REPO_ROOT / "temp"

# ── Image Enhancement ─────────────────────────────────────────────────────────

def enhance_image(image_bytes: bytes, variant: str = "high_contrast") -> bytes:
    """Create enhanced variants of the papyrus image."""
    img = Image.open(io.BytesIO(image_bytes))

    if variant == "high_contrast":
        # Boost contrast significantly to make ink stand out from papyrus
        img = ImageEnhance.Contrast(img).enhance(2.0)
        img = ImageEnhance.Sharpness(img).enhance(1.5)
    elif variant == "adaptive":
        # Convert to grayscale, auto-contrast (like CLAHE), then sharpen
        img = ImageOps.grayscale(img)
        img = ImageOps.autocontrast(img, cutoff=2)
        img = ImageEnhance.Sharpness(img).enhance(2.0)
    elif variant == "ink_isolation":
        # Grayscale + aggressive contrast to isolate dark ink from background
        img = ImageOps.grayscale(img)
        img = ImageOps.autocontrast(img, cutoff=5)
        img = ImageEnhance.Contrast(img).enhance(3.0)
        img = ImageEnhance.Brightness(img).enhance(1.2)

    buf = io.BytesIO()
    fmt = "JPEG" if img.mode in ("RGB", "L") else "PNG"
    if img.mode == "L":
        img = img.convert("RGB")  # JPEG needs RGB
    img.save(buf, format=fmt, quality=95)
    return buf.getvalue()


def prepare_image_variants(image_bytes: bytes) -> list[tuple[bytes, str, str]]:
    """Create multiple enhanced variants for cross-referencing.

    Returns list of (bytes, media_type, description).
    """
    variants = [(image_bytes, "image/jpeg", "original")]

    for name in ("high_contrast", "adaptive", "ink_isolation"):
        enhanced = enhance_image(image_bytes, name)
        variants.append((enhanced, "image/jpeg", name))

    return variants


# ── Prompt Versions ───────────────────────────────────────────────────────────
# Keep prompts general. The model knows Coptic. Help it enter the right mode.

SYSTEM_PROMPTS = {
    1: (
        "You are a papyrologist and Coptic philologist performing manuscript "
        "transcription. You read ancient handwritten Coptic with precision, "
        "distinguishing individual letter forms even on damaged papyrus. "
        "You use Unicode Coptic (U+2C80–U+2CFF) for output."
    ),
    2: (
        "You are a specialist in Coptic paleography performing diplomatic "
        "transcription of manuscript photographs. You transcribe exactly what "
        "is visible on the page, letter by letter, without reconstruction or "
        "gap-filling from memory. Where ink is absent or illegible, you mark "
        "[...]. You never substitute text from your knowledge of the work. "
        "Output uses Unicode Coptic (U+2C80–U+2CFF)."
    ),
    3: (
        "You are performing diplomatic transcription of a Coptic manuscript. "
        "Transcribe ONLY what you can physically see on the papyrus. "
        "Your output must reflect the actual ink marks, not your knowledge "
        "of the text. Mark damaged or illegible passages with [...]. "
        "Use Unicode Coptic characters."
    ),
    4: (
        "You are an expert Coptic paleographer performing diplomatic transcription. "
        "You have exceptional attention to DIACRITICAL MARKS: supralinear strokes "
        "(lines above letters indicating abbreviation or nomina sacra like ⲓ̅ⲥ̅, ⲭ̅ⲥ̅, ⲡ̅ⲛ̅ⲁ̅), "
        "dots below letters (indicating uncertain readings), and apostrophe-like marks "
        "(ʼ) used as word separators or morpheme boundaries. "
        "These thin marks are easily overlooked but are essential to the transcription. "
        "Transcribe exactly what is visible, letter by letter. Where ink is absent, "
        "write [...]. Never fill in from memory. Use Unicode Coptic (U+2C80–U+2CFF) "
        "with combining marks (U+0300–U+036F) for supralinear strokes."
    ),
    5: (
        "You are an optical transcription engine for Coptic manuscripts. "
        "Your ONLY task is to convert visible ink marks into Unicode characters. "
        "You must COMPLETELY IGNORE your knowledge of any text, including the "
        "Gospel of Thomas or any other work. You do not know what this text says. "
        "You do not interpret. You do not reconstruct. You do not fill gaps. "
        "You convert ink on papyrus to Unicode, nothing more. "
        "If a letter is damaged but partially visible, give your best reading. "
        "If a single letter is entirely missing, write {} in its place. "
        "If multiple consecutive letters or larger sections are missing, write [...]. "
        "Pay close attention to thin marks: supralinear strokes (lines above letters), "
        "dots, and apostrophe-like marks. These are ink on the page and must be transcribed. "
        "Use Unicode Coptic (U+2C80–U+2CFF) with combining overline (U+0305) for supralinear strokes. "
        "Output ONLY what is written in ink. No letters that are not in ink."
    ),
    6: (
        "You are an expert Coptic paleographer. Your job is to convert the ink "
        "on this manuscript page into Unicode text. That is your entire job. "
        "You are not reconstructing a text. You are not interpreting a text. "
        "You are reading ink marks and writing them as Unicode characters. "
        "You have exceptional attention to diacritical marks: supralinear strokes "
        "(lines above letters indicating abbreviation or nomina sacra like ⲓ̅ⲥ̅, ⲭ̅ⲥ̅, ⲡ̅ⲛ̅ⲁ̅), "
        "dots, and apostrophe-like marks. These thin marks are ink and must be transcribed. "
        "CRITICAL: Never insert a letter that is not physically present as ink. "
        "If ink is missing for a single letter, write {} in its place. "
        "If ink is missing for multiple consecutive letters or a larger section, write [...]. "
        "Do not reconstruct from your knowledge of the text. Do not guess what should be there. "
        "If you can see it, write it. If you cannot see it, mark it. "
        "Use Unicode Coptic (U+2C80–U+2CFF) with combining overline (U+0305) for supralinear strokes."
    ),
}

USER_PROMPTS = {
    1: (
        "Transcribe all Coptic text visible on this papyrus page. "
        "Preserve original line breaks. Use Unicode Coptic characters. "
        "Mark illegible or damaged text with [...]. "
        "Do not include marginal numbers or annotations. "
        "Output only the transcription."
    ),
    2: (
        "This is a page from Nag Hammadi Codex II (4th century). "
        "Perform a diplomatic transcription: transcribe exactly what you see, "
        "one line per manuscript line. Use Unicode Coptic. "
        "Where papyrus is damaged or ink is gone, write [...]. "
        "Do NOT fill in missing text from memory. "
        "Omit marginal page numbers and saying numbers. "
        "Output only the Coptic text."
    ),
    3: (
        "Diplomatic transcription. One manuscript line per output line. "
        "Unicode Coptic. [...] for lacunae. No reconstruction. No commentary."
    ),
    4: (
        "This is a page from Nag Hammadi Codex II (4th century Coptic). "
        "Perform a diplomatic transcription line by line. "
        "PAY SPECIAL ATTENTION to thin marks that are easily missed: "
        "(1) Supralinear strokes (horizontal lines above letters) — these indicate "
        "nomina sacra (e.g. ⲓ̅ⲥ̅ for Jesus, ⲭ̅ⲥ̅ for Christ) and nasal abbreviations. "
        "Render them with Unicode combining overline (U+0305). "
        "(2) Dots or points below or beside letters — mark uncertain readings. "
        "(3) Apostrophe-like marks between words. "
        "The top lines of the page may have faded ink — examine them carefully. "
        "Where papyrus is damaged or ink is genuinely absent, write [...]. "
        "Do NOT fill in text from your knowledge of the work. "
        "Output only the Coptic text, one line per manuscript line."
    ),
    5: (
        "Photograph of a handwritten Coptic manuscript page. "
        "Transcribe ONLY the ink marks you can see. One manuscript line per output line. "
        "CRITICAL RULES: "
        "(1) You MUST NOT use your knowledge of this text or any text. Pretend you have "
        "never seen Coptic literature. You are reading shapes on paper, not a known work. "
        "(2) If you cannot see a letter, do NOT guess it. Write {} for a single missing "
        "letter, [...] for multiple missing letters or larger gaps. "
        "(3) Write ONLY letters that exist as ink on the page. Every character in your "
        "output must correspond to a visible ink mark. No exceptions. "
        "(4) Supralinear strokes (thin horizontal lines above letters) are ink marks. "
        "Transcribe them with combining overline U+0305. "
        "(5) Dots, apostrophes, and other small marks ARE ink. Transcribe them. "
        "(6) Do not add, remove, or move any letter from where it physically appears. "
        "Unicode Coptic (U+2C80–U+2CFF). Output only the transcription."
    ),
    6: (
        "Transcribe this manuscript page. One manuscript line per output line. "
        "The top lines may have faded ink — examine them with extra care. "
        "Output only the transcription."
    ),
}


def create_client() -> tuple[AnthropicFoundry, str]:
    """Create Claude client from .env credentials."""
    os.environ.pop("ANTHROPIC_FOUNDRY_RESOURCE", None)

    config = dotenv_values(SECRETS_PATH)
    endpoint = config.get("ANTHROPIC_ENDPOINT", "").rstrip("/")
    api_key = config.get("ANTHROPIC_API_KEY", "")
    deployment = config.get("ANTHROPIC_DEPLOYMENT", "claude-opus-4-7-1")

    if not endpoint or not api_key:
        print("ERROR: ANTHROPIC_ENDPOINT and ANTHROPIC_API_KEY required")
        sys.exit(1)

    client = AnthropicFoundry(
        api_key=api_key,
        base_url=endpoint,
        timeout=httpx.Timeout(600.0, connect=30.0),
    )
    return client, deployment


def load_ground_truth(folio_num: int, tractate_file: str = "II_2_gospel_thomas.md") -> list[str]:
    """Extract ground truth lines for a specific folio."""
    gt_path = COPTIC_GT_DIR / tractate_file
    text = gt_path.read_text(encoding="utf-8")

    pattern = rf"### Folio {folio_num}\n"
    match = re.search(pattern, text)
    if not match:
        print(f"ERROR: Folio {folio_num} not found in {gt_path}")
        sys.exit(1)

    start = match.end()
    next_folio = re.search(r"\n### Folio \d+", text[start:])
    section = text[start:start + next_folio.start()] if next_folio else text[start:]

    lines = []
    for line in section.strip().split("\n"):
        m = re.match(r"\*\*(\d+)\*\*\s+(.*)", line)
        if m:
            lines.append(m.group(2))
    return lines


def load_english_for_folio(english_file: Path, folio_num: int) -> str:
    """Load relevant English translation text for a given folio.

    Extracts the sayings whose Coptic text appears on this folio.
    """
    text = english_file.read_text(encoding="utf-8")
    # Mapping of folio numbers to the saying range they contain
    folio_sayings = {
        35: (13, 16),
        36: (16, 18),
        37: (18, 21),
        38: (21, 24),
        39: (24, 27),
    }
    if folio_num not in folio_sayings:
        # Fallback: return a chunk of the file
        print(f"  WARNING: No saying mapping for folio {folio_num}")
        return text[2000:5000]

    start_saying, end_saying = folio_sayings[folio_num]
    start_match = re.search(rf"\*\*\({start_saying}\)\*\*", text)
    if not start_match:
        print(f"  WARNING: Saying {start_saying} not found in English file")
        return ""
    end_match = re.search(rf"\*\*\({end_saying + 1}\)\*\*", text)
    if end_match:
        return text[start_match.start():end_match.start()].strip()
    else:
        return text[start_match.start():].strip()


def strip_editorial(text: str) -> str:
    """Remove editorial conventions for fair comparison."""
    text = text.replace("-", "")        # Line-end hyphens
    text = text.replace("\u2019", "")   # Right single quote
    text = text.replace("'", "")        # Apostrophe
    text = text.replace("[", "").replace("]", "")  # Editorial brackets
    text = text.replace("\u0323", "")   # Combining dot below
    return text


def strip_combining(text: str) -> str:
    """Remove combining marks for base-character comparison."""
    import unicodedata
    return "".join(c for c in text if not unicodedata.combining(c))


def analyze(gt_lines: list[str], tr_lines: list[str]) -> dict:
    """Comprehensive accuracy analysis including spaceless CER."""
    gt_text = strip_editorial(" ".join(gt_lines))
    tr_text = strip_editorial(" ".join(tr_lines))
    gt_text = re.sub(r"\s+", " ", gt_text).strip()
    tr_text = re.sub(r"\s+", " ", tr_text).strip()

    # Character-level (with combining marks)
    sm = difflib.SequenceMatcher(None, gt_text, tr_text)
    char_sim = sm.ratio()

    # Base character (no combining marks)
    gt_base = strip_combining(gt_text)
    tr_base = strip_combining(tr_text)
    sm_base = difflib.SequenceMatcher(None, gt_base, tr_base)
    base_sim = sm_base.ratio()

    # Word-level (base chars)
    gt_words = gt_base.split()
    tr_words = tr_base.split()
    wsm = difflib.SequenceMatcher(None, gt_words, tr_words)
    word_sim = wsm.ratio()

    # Exact word matches
    word_ops = wsm.get_opcodes()
    exact_words = sum(i2 - i1 for tag, i1, i2, j1, j2 in word_ops if tag == "equal")

    # Line-level exact matches (base chars, stripping editorial)
    gt_base_lines = [strip_combining(strip_editorial(l)) for l in gt_lines]
    tr_base_lines = [strip_combining(strip_editorial(l)) for l in tr_lines]
    exact_lines = sum(1 for gl in gt_base_lines if gl in tr_base_lines)

    # ── Spaceless CER (fair comparison: no spaces, no line breaks, no combining) ──
    gt_spaceless = gt_base.replace(" ", "")
    tr_spaceless = tr_base.replace(" ", "")
    cer_sm = difflib.SequenceMatcher(None, gt_spaceless, tr_spaceless)
    n_sub = n_ins = n_del = 0
    for tag, i1, i2, j1, j2 in cer_sm.get_opcodes():
        if tag == "replace":
            n_sub += max(i2 - i1, j2 - j1)
        elif tag == "insert":
            n_ins += j2 - j1
        elif tag == "delete":
            n_del += i2 - i1
    total_errors = n_sub + n_ins + n_del
    cer = total_errors / len(gt_spaceless) if gt_spaceless else 0

    return {
        "gt_lines": len(gt_lines),
        "tr_lines": len(tr_lines),
        "exact_line_matches": exact_lines,
        "char_similarity": char_sim,
        "base_char_similarity": base_sim,
        "word_similarity": word_sim,
        "exact_words": exact_words,
        "total_gt_words": len(gt_words),
        "word_accuracy": exact_words / len(gt_words) if gt_words else 0,
        "cer": cer,
        "cer_errors": total_errors,
        "cer_total_chars": len(gt_spaceless),
    }


def run_transcription(client, deployment: str,
                      image_variants: list[tuple[bytes, str, str]],
                      system_prompt: str, user_prompt: str, effort: str,
                      max_tokens: int = 16000, no_thinking: bool = False) -> dict:
    """Send image(s) to Opus 4.7 with adaptive thinking.

    image_variants: list of (bytes, media_type, description) tuples.
    When multiple variants are provided, all are sent in the same message.
    """

    # "omitted" = Opus 4.7 default; avoids broken summarizer on non-English thinking
    if no_thinking:
        thinking_config = {"type": "disabled"}
    else:
        thinking_config = {"type": "adaptive", "display": "omitted"}

    t0 = time.time()

    full_text = ""
    thinking_text = ""
    input_tokens = 0
    output_tokens = 0

    # Build content blocks: images first, then text prompt
    content_blocks = []
    for img_bytes, mtype, desc in image_variants:
        b64 = base64.standard_b64encode(img_bytes).decode("utf-8")
        if len(image_variants) > 1:
            content_blocks.append({"type": "text", "text": f"[Image: {desc}]"})
        content_blocks.append({
            "type": "image",
            "source": {"type": "base64", "media_type": mtype, "data": b64},
        })
    content_blocks.append({"type": "text", "text": user_prompt})

    kwargs = dict(
        model=deployment,
        system=system_prompt,
        max_tokens=max_tokens,
        thinking=thinking_config,
        messages=[{"role": "user", "content": content_blocks}],
    )

    # Add effort via output_config if not default (effort requires thinking)
    if effort != "high" and not no_thinking:
        kwargs["output_config"] = {"effort": effort}

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        event_count = 0
        full_text = ""
        thinking_text = ""
        try:
            with client.messages.stream(**kwargs) as stream:
                for event in stream:
                    event_count += 1
                    if event.type == "content_block_start":
                        block_type = getattr(event.content_block, "type", "unknown")
                        print(f"  [stream] block start: {block_type}", flush=True)
                    elif event.type == "content_block_delta":
                        delta_type = getattr(event.delta, "type", "unknown")
                        if delta_type == "thinking_delta":
                            chunk = getattr(event.delta, "thinking", "") or ""
                            thinking_text += chunk
                            sys.stdout.write(chunk)
                            sys.stdout.flush()
                        elif delta_type == "text_delta":
                            chunk = getattr(event.delta, "text", "") or ""
                            full_text += chunk
                        elif delta_type == "signature_delta":
                            pass  # encrypted thinking signature
                        else:
                            if event_count <= 5:
                                print(f"  [stream] delta type: {delta_type}", flush=True)
                    elif event.type == "content_block_stop":
                        block_type_hint = "thinking" if thinking_text and not full_text else "text"
                        if block_type_hint == "thinking" and thinking_text:
                            print()  # newline after streamed thinking
                        print(f"  [stream] block stop: {block_type_hint} (events: {event_count})", flush=True)
                    elif event.type == "message_delta":
                        pass

                msg = stream.get_final_message()
                input_tokens = msg.usage.input_tokens
                output_tokens = msg.usage.output_tokens
            print(f"  [stream] done. {event_count} events total.", flush=True)
            break  # success — exit retry loop

        except (httpx.RemoteProtocolError, httpx.ReadError, httpx.ReadTimeout,
                ConnectionError, OSError) as e:
            print(f"\n  [retry] Connection error on attempt {attempt}/{max_retries}: {e}", flush=True)
            if attempt == max_retries:
                raise
            print(f"  [retry] Waiting 5s before retry...", flush=True)
            time.sleep(5)

    elapsed = time.time() - t0

    return {
        "transcription": full_text,
        "thinking": thinking_text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "elapsed_seconds": round(elapsed, 1),
    }


def main():
    parser = argparse.ArgumentParser(description="Iterative papyrus HTR test")
    parser.add_argument("--image", type=Path, default=TEMP_DIR / "nag_hammadi_II_35.jpg")
    parser.add_argument("--folio", type=int, default=35)
    parser.add_argument("--tractate", default="II_2_gospel_thomas.md")
    parser.add_argument("--effort", default="max", choices=["low", "medium", "high", "xhigh", "max"])
    parser.add_argument("--prompt-version", type=int, default=1, choices=[1, 2, 3, 4, 5, 6])
    parser.add_argument("--max-tokens", type=int, default=128000)
    parser.add_argument("--enhance", action="store_true",
                        help="Send enhanced image variants alongside original")
    parser.add_argument("--no-thinking", action="store_true",
                        help="Disable extended thinking (ignores effort)")
    parser.add_argument("--english", action="store_true",
                        help="Include English translation as semantic context")
    parser.add_argument("--english-file", type=Path,
                        default=REPO_ROOT / "output" / "english" / "tractates" / "II_2_gospel_thomas.md",
                        help="English translation file")
    args = parser.parse_args()

    pv = args.prompt_version
    system_prompt = SYSTEM_PROMPTS[pv]
    user_prompt = USER_PROMPTS[pv]

    print("=" * 70)
    print(f"PAPYRUS HTR — Opus 4.7 + Adaptive Thinking (effort={args.effort})")
    print(f"Prompt version: {pv}")
    print("=" * 70)

    # Load image
    if not args.image.exists():
        print(f"ERROR: Image not found: {args.image}")
        sys.exit(1)
    image_bytes = args.image.read_bytes()
    suffix = args.image.suffix.lower()
    media_type = "image/jpeg" if suffix in (".jpg", ".jpeg") else "image/png"
    print(f"\nImage: {args.image.name} ({len(image_bytes):,} bytes)")

    # Prepare image variants
    if args.enhance:
        image_variants = prepare_image_variants(image_bytes)
        print(f"Image variants: {', '.join(d for _, _, d in image_variants)}")
    else:
        image_variants = [(image_bytes, media_type, "original")]

    # Load ground truth
    gt_lines = load_ground_truth(args.folio, args.tractate)
    print(f"Ground truth: Folio {args.folio}, {len(gt_lines)} lines")

    # Append multi-image guidance if enhancing
    if args.enhance and len(image_variants) > 1:
        user_prompt += (
            " Multiple variants of the same page are provided (original + "
            "enhanced). Cross-reference them to resolve ambiguous or faded "
            "characters, especially in damaged areas and for thin diacritical marks."
        )

    # Append English translation as semantic context
    if args.english:
        english_text = load_english_for_folio(args.english_file, args.folio)
        print(f"English context: {len(english_text)} chars (Sayings from folio {args.folio})")
        user_prompt += (
            "\n\nSEMANTIC CONTEXT — The English translation of this page is provided below. "
            "Use it ONLY to help you resolve ambiguous letter forms (e.g., distinguishing "
            "ϩ from ⲍ, or ⲁ from ⲟ, when the ink is unclear). Do NOT invent characters "
            "that are not visible as ink. The English helps you IDENTIFY what you see — "
            "it does not replace reading the manuscript.\n\n"
            "--- ENGLISH TRANSLATION ---\n" + english_text + "\n--- END ---"
        )

    print(f"\nSystem: {system_prompt[:80]}...")
    print(f"User: {user_prompt[:80]}...")

    # Run transcription
    thinking_mode = "disabled" if args.no_thinking else "adaptive"
    print(f"\nSending to Opus 4.7 (effort={args.effort}, thinking={thinking_mode})...")
    client, deployment = create_client()

    result = run_transcription(
        client, deployment, image_variants,
        system_prompt, user_prompt, args.effort, args.max_tokens,
        no_thinking=args.no_thinking
    )

    tr_text = result["transcription"]
    tr_lines = [l.strip() for l in tr_text.strip().split("\n") if l.strip()]

    print(f"\nCompleted in {result['elapsed_seconds']}s")
    print(f"Tokens: {result['input_tokens']} in / {result['output_tokens']} out")

    # Show thinking summary if available
    if result["thinking"]:
        print(f"\n--- THINKING SUMMARY ({len(result['thinking'])} chars) ---")
        thinking_preview = result["thinking"][:500]
        print(thinking_preview)
        if len(result["thinking"]) > 500:
            print("...")

    # Show transcription
    print(f"\n--- TRANSCRIPTION ({len(tr_lines)} lines) ---")
    for i, line in enumerate(tr_lines[:10], 1):
        print(f"  {i:2d}: {line}")
    if len(tr_lines) > 10:
        print(f"  ... ({len(tr_lines)} total)")

    # Analyze
    print("\n--- ACCURACY ---")
    metrics = analyze(gt_lines, tr_lines)
    print(f"  Lines: {metrics['tr_lines']}/{metrics['gt_lines']} (exact match: {metrics['exact_line_matches']})")
    print(f"  Char similarity: {metrics['char_similarity']:.1%}")
    print(f"  Base char similarity: {metrics['base_char_similarity']:.1%}")
    print(f"  Word similarity: {metrics['word_similarity']:.1%}")
    print(f"  Word accuracy: {metrics['exact_words']}/{metrics['total_gt_words']} ({metrics['word_accuracy']:.1%})")
    print(f"  CER (spaceless): {metrics['cer']:.2%} ({metrics['cer_errors']} errors / {metrics['cer_total_chars']} chars)")

    # Line-by-line diff (first 15)
    print("\n--- LINE DIFF (first 15) ---")
    for i in range(min(15, max(len(gt_lines), len(tr_lines)))):
        gt = gt_lines[i] if i < len(gt_lines) else "(missing)"
        tr = tr_lines[i] if i < len(tr_lines) else "(missing)"
        gt_b = strip_combining(strip_editorial(gt))
        tr_b = strip_combining(strip_editorial(tr))
        status = "✓" if gt_b == tr_b else "✗"
        print(f"  {status} GT[{i+1:2d}]: {gt}")
        if gt_b != tr_b:
            print(f"    TR[{i+1:2d}]: {tr}")

    # Save
    TEMP_DIR.mkdir(exist_ok=True)
    enh_tag = "_enhanced" if args.enhance else ""
    out_name = f"htr_v{pv}_effort_{args.effort}{enh_tag}_folio_{args.folio}.json"
    out_path = TEMP_DIR / out_name
    save_data = {
        "folio": args.folio,
        "prompt_version": pv,
        "effort": args.effort,
        "enhanced": args.enhance,
        "image_variants": [d for _, _, d in image_variants],
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "ground_truth_lines": gt_lines,
        "transcription_raw": tr_text,
        "transcription_lines": tr_lines,
        "thinking": result["thinking"],
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
        "elapsed_seconds": result["elapsed_seconds"],
        "metrics": metrics,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {out_path}")

    # Summary
    print("\n" + "=" * 70)
    print(f"v{pv} | effort={args.effort} | CER={metrics['cer']:.2%} | "
          f"words={metrics['word_accuracy']:.1%} | "
          f"{result['elapsed_seconds']}s | {result['output_tokens']} tokens")
    print("=" * 70)


if __name__ == "__main__":
    main()
