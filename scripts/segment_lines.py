#!/usr/bin/env python3
"""
Robust line segmentation for manuscript pages.

Designed to work with any manuscript image (papyrus, parchment, paper).
Handles:
- Automatic text column detection (removes background/gutter/binding)
- Overlap context: each line image includes parts of neighboring lines
  so supralinear strokes and descenders are always visible
- Lacunae / gaps within lines (no false splits)

Usage:
    python scripts/segment_lines.py <input_image> [--output-dir DIR] [--expected-lines N]
    python scripts/segment_lines.py data/claremont/optimal_htr.jpg --expected-lines 36
"""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np


# ─── Configuration ───────────────────────────────────────────────────────────

class SegmentationConfig:
    """All tunable parameters, with generous defaults for manuscript work."""

    # Text column detection
    col_ink_threshold_ratio: float = 0.08  # fraction of max ink density to count as "has ink"

    # Binarization (adaptive threshold)
    adaptive_C: int = 25                   # constant subtracted from mean
    morph_kernel_ratio: float = 0.004      # morph kernel as fraction of image width

    # Horizontal projection — valley detection approach
    projection_smooth_ratio: float = 0.15  # smoothing kernel as fraction of line height
    valley_prominence_ratio: float = 0.3   # required valley depth as fraction of peak-valley range
    min_line_height_ratio: float = 0.4     # min line height as fraction of estimated line spacing

    # Overlap: how much of the neighboring lines to include (as ratio of line height)
    overlap_ratio: float = 0.35           # 35% of line height above and below

    # Quality
    jpeg_quality: int = 95


def detect_papyrus_region(gray: np.ndarray) -> tuple[int, int, int, int]:
    """
    Detect the papyrus/parchment region (excluding black background).
    Returns (row_start, row_end, col_start, col_end).
    Uses brightness thresholding — works for any lighter writing surface.
    """
    # Papyrus/parchment is lighter than the background
    # Use a relatively low threshold to include degraded edges
    bright = gray > 100  # very permissive — captures even dark papyrus

    # Find rows and cols with sufficient bright pixels (>5% of width/height)
    row_bright = bright.sum(axis=1)
    col_bright = bright.sum(axis=0)

    row_thresh = gray.shape[1] * 0.05
    col_thresh = gray.shape[0] * 0.05

    rows_with_papyrus = np.where(row_bright > row_thresh)[0]
    cols_with_papyrus = np.where(col_bright > col_thresh)[0]

    if len(rows_with_papyrus) == 0 or len(cols_with_papyrus) == 0:
        # Fallback: use whole image
        return 0, gray.shape[0], 0, gray.shape[1]

    return (
        int(rows_with_papyrus[0]),
        int(rows_with_papyrus[-1]),
        int(cols_with_papyrus[0]),
        int(cols_with_papyrus[-1]),
    )


def detect_text_column(gray: np.ndarray, papyrus_bounds: tuple, cfg: SegmentationConfig) -> tuple[int, int]:
    """
    Detect the horizontal text column within the papyrus region.
    Uses vertical ink projection — finds where the ink actually is.
    Returns (col_start, col_end) with margin applied.
    """
    r0, r1, c0, c1 = papyrus_bounds
    crop = gray[r0:r1, c0:c1]

    # Scale-adaptive binarization
    block_size = max(11, int(crop.shape[1] * 0.06) | 1)  # ~6% of width, ensure odd
    binary = cv2.adaptiveThreshold(
        crop, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, block_size, cfg.adaptive_C
    )

    # Vertical projection — sum of ink pixels per column
    v_proj = binary.sum(axis=0).astype(float) / 255.0

    # Smooth to ignore isolated noise
    smooth_k = max(11, int(crop.shape[1] * 0.02))
    kernel = np.ones(smooth_k) / smooth_k
    v_proj_smooth = np.convolve(v_proj, kernel, mode='same')

    # Threshold: columns with significant ink
    v_thresh = v_proj_smooth.max() * cfg.col_ink_threshold_ratio
    ink_cols = np.where(v_proj_smooth > v_thresh)[0]

    if len(ink_cols) < 10:
        return c0, c1

    # Find the main continuous ink region (largest connected block)
    # Gap threshold: 5% of papyrus width
    gap_thresh = max(50, int((c1 - c0) * 0.05))
    gaps = np.where(np.diff(ink_cols) > gap_thresh)[0]
    if len(gaps) == 0:
        groups = [ink_cols]
    else:
        groups = np.split(ink_cols, gaps + 1)

    # Take the largest group
    main_group = max(groups, key=len)
    text_start = int(main_group[0]) + c0
    text_end = int(main_group[-1]) + c0

    # Apply margin (scale-adaptive), clipped to papyrus bounds (no background)
    margin = max(10, int((text_end - text_start) * 0.01))
    col_start = max(c0, text_start - margin)
    col_end = min(c1, text_end + margin)

    # Column-wise brightness verification: trim dark columns from both edges.
    # Adaptive threshold can pick up binding/gutter texture as "ink," so the
    # ink-based bounds may extend into dark areas.  Walk inward from each edge
    # until columns are bright enough to be papyrus.
    col_brightness = gray[r0:r1, :].mean(axis=0)
    papyrus_thresh = 130
    min_width = 100  # safety: never shrink below 100px

    while col_start < col_end - min_width and col_brightness[col_start] < papyrus_thresh:
        col_start += 1
    while col_end > col_start + min_width and col_brightness[col_end - 1] < papyrus_thresh:
        col_end -= 1

    return col_start, col_end


def binarize_for_projection(gray_crop: np.ndarray, cfg: SegmentationConfig) -> np.ndarray:
    """
    Produce a clean binary image suitable for horizontal projection.
    Scale-adaptive: works on any resolution.
    Uses minimal morphology to preserve inter-line gaps.
    """
    h, w = gray_crop.shape

    # Adaptive threshold with block size proportional to image
    block_size = max(11, int(w * 0.06) | 1)
    binary = cv2.adaptiveThreshold(
        gray_crop, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, block_size, cfg.adaptive_C
    )

    # Light morphological open with HORIZONTAL-only kernel
    # This cleans horizontal noise without filling vertical inter-line gaps
    k_w = max(3, int(w * cfg.morph_kernel_ratio))
    k_h = 2  # minimal vertical extent to preserve line separation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k_w, k_h))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    return binary


def find_line_boundaries(gray: np.ndarray, papyrus_bounds: tuple,
                         col_bounds: tuple, cfg: SegmentationConfig,
                         est_line_height: float = None) -> list[tuple[int, int]]:
    """
    Find line boundaries using valley detection in horizontal projection.
    Valley detection is more robust than threshold-based approaches because
    it finds the GAPS between lines rather than trying to define what "ink" is.

    Returns list of (row_start, row_end) tuples for each line.
    """
    r0, r1, _, _ = papyrus_bounds
    c0, c1 = col_bounds

    # Crop to text column
    crop = gray[r0:r1, c0:c1]

    # Binarize
    binary = binarize_for_projection(crop, cfg)

    # Horizontal projection — sum of ink pixels per row
    h_proj = binary.sum(axis=1).astype(float) / 255.0

    # If we have an estimated line height, use it for smoothing
    if est_line_height is None:
        est_line_height = estimate_line_height_from_proj(h_proj)

    # Smooth projection — kernel is a fraction of line height
    smooth_size = max(3, int(est_line_height * cfg.projection_smooth_ratio))
    if smooth_size % 2 == 0:
        smooth_size += 1
    smooth_k = np.ones(smooth_size) / smooth_size
    h_proj_smooth = np.convolve(h_proj, smooth_k, mode='same')

    # Valley detection: find minima between lines
    # A valley is where the projection dips significantly
    lines = extract_lines_from_projection(h_proj_smooth, est_line_height, cfg)

    # Convert back to full-image coordinates
    lines_absolute = [(s + r0, e + r0) for s, e in lines]

    # Filter too-small lines (noise fragments)
    min_height = max(10, int(est_line_height * cfg.min_line_height_ratio))
    lines_filtered = [(s, e) for s, e in lines_absolute if (e - s) >= min_height]

    # NOTE: No merge step — valley detection returns correctly-bounded lines
    # that share boundary points. Merging would collapse them all into one.
    return lines_filtered


def estimate_line_height_from_proj(h_proj: np.ndarray) -> float:
    """
    Estimate line height from autocorrelation of horizontal projection.
    """
    h_proj_centered = h_proj - h_proj.mean()
    if h_proj_centered.std() == 0:
        return 70.0

    corr = np.correlate(h_proj_centered, h_proj_centered, mode='full')
    corr = corr[len(corr)//2:]  # positive lags only
    corr = corr / (corr[0] + 1e-10)  # normalize

    # Find first significant peak after lag 0
    min_lag = max(15, int(len(h_proj) * 0.01))
    max_lag = min(int(len(h_proj) * 0.08), len(corr) - 1)

    if max_lag <= min_lag:
        return 70.0

    corr_segment = corr[min_lag:max_lag]
    if len(corr_segment) == 0:
        return 70.0

    peak_offset = np.argmax(corr_segment) + min_lag
    return float(peak_offset)


def extract_lines_from_projection(h_proj: np.ndarray, est_line_height: float,
                                  cfg: SegmentationConfig) -> list[tuple[int, int]]:
    """
    Extract line boundaries from smoothed horizontal projection using valley detection.

    Strategy:
    1. Find all local minima (valleys) in the projection
    2. Lines are the regions between consecutive valleys
    3. Filter by minimum prominence and spacing
    """
    from scipy.signal import find_peaks

    # Invert projection so valleys become peaks
    proj_inverted = -h_proj

    # Minimum distance between valleys ~ half of estimated line height
    min_distance = max(5, int(est_line_height * 0.5))

    # Find valleys (peaks of inverted signal)
    peaks, properties = find_peaks(
        proj_inverted,
        distance=min_distance,
    )

    if len(peaks) < 2:
        return _fallback_threshold_lines(h_proj, est_line_height)

    # Filter valleys by prominence
    proj_range = h_proj.max() - h_proj.min()
    if proj_range == 0:
        return []

    # Use scipy's built-in prominence calculation
    from scipy.signal import peak_prominences
    prominences, _, _ = peak_prominences(proj_inverted, peaks)

    prom_threshold = proj_range * cfg.valley_prominence_ratio * 0.3
    significant_valleys = peaks[prominences > prom_threshold]

    if len(significant_valleys) < 2:
        return _fallback_threshold_lines(h_proj, est_line_height)

    # Find where text starts and ends (projection > 5% of max)
    text_threshold = h_proj.max() * 0.05
    text_rows = np.where(h_proj > text_threshold)[0]
    if len(text_rows) == 0:
        return []

    text_start = int(text_rows[0])
    text_end = int(text_rows[-1])

    # Build line list: regions between consecutive valleys
    # Prepend a boundary one line-height above the first valley
    # so the very first text line gets its own segment
    first_line_top = max(text_start, int(significant_valleys[0] - est_line_height))
    boundaries = [first_line_top] + list(significant_valleys) + [text_end]
    lines = []
    for i in range(len(boundaries) - 1):
        start = int(boundaries[i])
        end = int(boundaries[i + 1])
        if end - start > 5:  # skip trivial gaps
            lines.append((start, end))

    return lines


def _fallback_threshold_lines(h_proj: np.ndarray, est_line_height: float) -> list[tuple[int, int]]:
    """Fallback: simple threshold-based line detection when valleys fail."""
    threshold = h_proj.mean() * 0.3
    ink_mask = h_proj > threshold

    lines = []
    in_line = False
    start = 0
    for i, has_ink in enumerate(ink_mask):
        if has_ink and not in_line:
            start = i
            in_line = True
        elif not has_ink and in_line:
            lines.append((start, i))
            in_line = False
    if in_line:
        lines.append((start, len(ink_mask)))

    return lines


def estimate_line_height(gray: np.ndarray, papyrus_bounds: tuple,
                         col_bounds: tuple, cfg: SegmentationConfig) -> float:
    """
    Estimate typical line height using autocorrelation of horizontal projection.
    This gives us a scale-independent baseline for all other parameters.
    """
    r0, r1, _, _ = papyrus_bounds
    c0, c1 = col_bounds
    crop = gray[r0:r1, c0:c1]

    # Binarize with scale-adaptive parameters
    binary = binarize_for_projection(crop, cfg)

    # Horizontal projection
    h_proj = binary.sum(axis=1).astype(float)

    return estimate_line_height_from_proj(h_proj)


def segment_page(image_path: str, cfg: SegmentationConfig = None,
                 expected_lines: int = None) -> list[tuple[int, int, int, int]]:
    """
    Main entry point. Segments a manuscript page into lines.

    Returns list of (row_start, row_end, col_start, col_end) for each line.
    Each line image includes overlap padding from neighboring lines so that
    supralinear strokes and descenders are always visible in context.

    All parameters are auto-calibrated based on detected line spacing,
    so this works on any manuscript at any resolution.
    """
    if cfg is None:
        cfg = SegmentationConfig()

    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    print(f"Image size: {w}×{h}")

    # Step 1: Detect papyrus/parchment region (excludes black background)
    papyrus = detect_papyrus_region(gray)
    print(f"Papyrus region: rows {papyrus[0]}-{papyrus[1]}, cols {papyrus[2]}-{papyrus[3]}")

    # Step 2: Detect text column (clipped to papyrus — no background leaks)
    col_start, col_end = detect_text_column(gray, papyrus, cfg)
    print(f"Text column: cols {col_start}-{col_end} ({col_end - col_start}px wide)")

    # Step 3: Estimate line height for scale-adaptive parameters
    est_height = estimate_line_height(gray, papyrus, (col_start, col_end), cfg)
    print(f"Estimated line spacing: {est_height:.0f}px")

    # Step 4: Find core line boundaries (valley detection)
    lines = find_line_boundaries(gray, papyrus, (col_start, col_end), cfg, est_height)
    print(f"Raw lines detected: {len(lines)}")

    # Step 5: Filter outliers by height (always run — removes fragments and merges)
    if len(lines) >= 3:
        heights = np.array([e - s for s, e in lines])
        median_h = np.median(heights)
        mask = (heights >= median_h * cfg.min_line_height_ratio) & (heights <= median_h * 2.5)
        lines_filtered = [l for l, keep in zip(lines, mask) if keep]
        if len(lines_filtered) >= len(lines) * 0.7:
            lines = lines_filtered
            print(f"  After height filter (median={median_h:.0f}px): {len(lines)} lines")

    # Tune prominence if count is off
    if expected_lines and len(lines) > expected_lines * 1.3:
        for try_prom in [0.40, 0.50, 0.60]:
            cfg.valley_prominence_ratio = try_prom
            lines = find_line_boundaries(gray, papyrus, (col_start, col_end), cfg, est_height)
            if len(lines) <= expected_lines * 1.2:
                break

    if expected_lines and len(lines) < expected_lines * 0.8:
        for try_prom in [0.20, 0.15, 0.10, 0.05]:
            cfg.valley_prominence_ratio = try_prom
            lines = find_line_boundaries(gray, papyrus, (col_start, col_end), cfg, est_height)
            if len(lines) >= expected_lines * 0.8:
                break

    # Step 6: Add overlap from neighboring lines
    # Each line image includes part of the line above and below
    # so the model can see supralinear strokes and descenders in context
    heights = [e - s for s, e in lines]
    median_h = float(np.median(heights)) if heights else est_height
    overlap_px = max(5, int(median_h * cfg.overlap_ratio))

    pap_top, pap_bot = papyrus[0], papyrus[1]
    final_lines = []
    for top, bot in lines:
        crop_top = max(pap_top, top - overlap_px)
        crop_bot = min(pap_bot, bot + overlap_px)
        final_lines.append((crop_top, crop_bot, col_start, col_end))

    print(f"Final lines: {len(final_lines)} (overlap={overlap_px}px per side)")
    for i, (r0, r1, c0, c1) in enumerate(final_lines):
        print(f"  Line {i+1:2d}: rows {r0:5d}-{r1:5d} ({r1-r0:3d}px) × cols {c0}-{c1}")

    return final_lines


def save_lines(image_path: str, lines: list[tuple[int, int, int, int]],
               output_dir: str, cfg: SegmentationConfig = None):
    """Save each line as a separate JPEG file."""
    if cfg is None:
        cfg = SegmentationConfig()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for i, (r0, r1, c0, c1) in enumerate(lines):
        line_img = img[r0:r1, c0:c1]

        # Add a sequential number ruler at the bottom — dense enough
        # that every vision patch contains a positional anchor
        h, w = line_img.shape[:2]
        ruler_height = 14
        ruler = np.ones((ruler_height, w, 3), dtype=np.uint8) * 255

        # Small sequential numbers every 40px
        n = 1
        for px in range(20, w - 10, 40):
            cv2.putText(ruler, str(n), (px, 11),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)
            n += 1

        line_img = np.vstack([line_img, ruler])

        filename = output_path / f"line_{i+1:02d}.jpg"
        cv2.imwrite(str(filename), line_img,
                    [cv2.IMWRITE_JPEG_QUALITY, cfg.jpeg_quality])

    print(f"\nSaved {len(lines)} line images to {output_dir}/")
    sizes = [(r1 - r0) for r0, r1, _, _ in lines]
    print(f"  Heights: min={min(sizes)}, max={max(sizes)}, mean={sum(sizes)/len(sizes):.0f}px")
    print(f"  Width: {lines[0][3] - lines[0][2]}px")


def main():
    parser = argparse.ArgumentParser(description="Segment manuscript page into lines")
    parser.add_argument("image", help="Path to input manuscript image")
    parser.add_argument("--output-dir", "-o", default=None,
                        help="Output directory for line images (default: same dir as image / lines/)")
    parser.add_argument("--expected-lines", "-n", type=int, default=None,
                        help="Expected number of lines (helps tune parameters)")
    parser.add_argument("--overlap", type=float, default=0.35,
                        help="Overlap ratio: fraction of line height to include from neighbors (default: 0.35)")

    args = parser.parse_args()

    # Validate input
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"Error: Image not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    # Set output dir
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = str(image_path.parent / "lines")

    # Configure
    cfg = SegmentationConfig()
    cfg.overlap_ratio = args.overlap

    # Run segmentation
    lines = segment_page(str(image_path), cfg, args.expected_lines)

    # Save
    save_lines(str(image_path), lines, output_dir, cfg)


if __name__ == "__main__":
    main()
