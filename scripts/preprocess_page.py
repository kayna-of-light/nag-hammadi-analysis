#!/usr/bin/env python3
"""
Preprocess a manuscript page image for HTR:
1. Find the paper (threshold + largest contour + minAreaRect)
2. Straighten it (rotate to level)
3. Cut it out (crop to bounding box)
4. Scale to target height

Usage:
    python scripts/preprocess_page.py <input_image> [--output FILE]
    python scripts/preprocess_page.py data/claremont/codex_ii_page_35_full.jpg
"""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np


def preprocess_page(input_path: Path, output_path: Path, target_height: int = 2600,
                    quality: int = 92) -> dict:
    """Find paper, crop to bounding box, scale."""
    print(f"Input:  {input_path.name}")
    img = cv2.imread(str(input_path))
    if img is None:
        print(f"ERROR: Cannot read {input_path}")
        sys.exit(1)

    h, w = img.shape[:2]
    print(f"  Original:   {w}×{h}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1. Threshold to find paper
    _, mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

    # 2. Largest contour = the paper
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("ERROR: No contours found")
        sys.exit(1)
    paper = max(contours, key=cv2.contourArea)

    # 3. Bounding box around the paper contour
    x, y, bw, bh = cv2.boundingRect(paper)
    print(f"  Bounding box: x={x}, y={y}, w={bw}, h={bh}")

    # 4. Crop
    cropped = gray[y:y+bh, x:x+bw]
    print(f"  Cropped:    {bw}×{bh}")

    # 5. Scale to target height
    scale = target_height / bh
    new_w = int(bw * scale)
    final = cv2.resize(cropped, (new_w, target_height), interpolation=cv2.INTER_LANCZOS4)
    print(f"  Scaled:     {new_w}×{target_height} (scale {scale:.2f}×)")

    # Save
    cv2.imwrite(str(output_path), final, [cv2.IMWRITE_JPEG_QUALITY, quality])
    size_kb = output_path.stat().st_size / 1024
    print(f"\nOutput: {output_path.name} ({size_kb:.0f} KB)")

    return {
        "input": str(input_path),
        "output": str(output_path),
        "original_size": (w, h),
        "bbox": (x, y, bw, bh),
        "final_size": (new_w, target_height),
        "file_size_kb": round(size_kb, 1),
    }


def main():
    parser = argparse.ArgumentParser(description="Preprocess manuscript page for HTR")
    parser.add_argument("image", type=Path, help="Input manuscript photograph")
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="Output path (default: same dir / <name>_preprocessed.jpg)")
    parser.add_argument("--target-height", type=int, default=2600,
                        help="Target image height in pixels (default: 2600)")
    parser.add_argument("--quality", type=int, default=92,
                        help="JPEG quality (default: 92)")
    args = parser.parse_args()

    if not args.image.exists():
        print(f"ERROR: {args.image} not found")
        sys.exit(1)

    if args.output is None:
        stem = args.image.stem
        args.output = args.image.parent / f"{stem}_preprocessed.jpg"

    preprocess_page(args.image, args.output, args.target_height, args.quality)


if __name__ == "__main__":
    main()
