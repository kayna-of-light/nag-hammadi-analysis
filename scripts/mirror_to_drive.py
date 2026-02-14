#!/usr/bin/env python3
"""Mirror NHL tractate markdown files to Google Drive as styled PDFs.

Splits each tractate into:
  - Main text PDF   → uploaded to the Drive root folder
  - Editor notes PDF → uploaded to an "Editor Notes" subfolder

Usage:
  python scripts/mirror_to_drive.py                       # Build + upload all
  python scripts/mirror_to_drive.py --dry-run              # Preview only
  python scripts/mirror_to_drive.py --only II_2_gospel_thomas.md
  python scripts/mirror_to_drive.py --force                # Rebuild all PDFs
  python scripts/mirror_to_drive.py --limit 3              # First N files
  python scripts/mirror_to_drive.py --build-only           # PDFs only, no Drive
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional

# ── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
TRACTATES_DIR = PROJECT_ROOT / "output" / "cleaned" / "tractates"
OUTPUT_ROOT = PROJECT_ROOT / "output" / "pdfs"
CACHE_DIR = PROJECT_ROOT / "cache"
ASSETS_DIR = SCRIPT_DIR / "assets"
DEFAULT_CSS = ASSETS_DIR / "pdf.css"
DEFAULT_TEMPLATE = ASSETS_DIR / "template.html"

# Reuse OAuth credentials from the literary-compilation project
LIT_COMP_SECRETS = Path(r"C:\Users\mlf\source\github\literary-compilation\secrets")
DEFAULT_OAUTH_CLIENT = LIT_COMP_SECRETS / "google_drive_oauth_client.json"
DEFAULT_OAUTH_TOKEN = LIT_COMP_SECRETS / "google_drive_token.json"

DRIVE_ROOT_ID = "1zWhkCJKWBbExzZpV2MskcLLqBA6tTYxF"
EDITOR_NOTES_FOLDER_NAME = "Editor Notes"


# ── Markdown splitting ──────────────────────────────────────────────────────

def split_tractate(md_text: str) -> tuple[str, str | None]:
    """Split a tractate markdown into (main_text, editor_notes_or_None).

    Structure expected:
      # Title
      **metadata lines**
      > **Editor's Introduction** ...blockquote...
      ---
      main text body

    Returns:
      main_text:    The title + everything after the `---` separator
      editor_notes: The title + metadata + blockquote intro (None if no intro exists)
    """
    lines = md_text.split("\n")

    # Find the --- separator (first occurrence of a line that is exactly ---)
    sep_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            sep_idx = i
            break

    if sep_idx is None:
        # No separator found — return entire text as main, no notes
        return md_text, None

    # Everything before --- is the header (title + metadata + intro)
    header_lines = lines[:sep_idx]
    body_lines = lines[sep_idx + 1:]  # skip the ---

    # Extract title (first H1)
    title_line = ""
    for line in header_lines:
        if line.startswith("# "):
            title_line = line
            break

    # Check if there's an editor introduction (blockquote with "Editor's Introduction")
    has_intro = any("Editor's Introduction" in line for line in header_lines)

    if not has_intro:
        # No editor intro — just return main text with title
        main_text = title_line + "\n\n" + "\n".join(body_lines).strip() + "\n"
        return main_text, None

    # Build main text: title + body (no metadata, no intro)
    main_text = title_line + "\n\n" + "\n".join(body_lines).strip() + "\n"

    # Build editor notes: full header section (title + metadata + intro)
    editor_notes = "\n".join(header_lines).strip() + "\n"

    return main_text, editor_notes


def extract_title(md_text: str) -> str:
    """Extract the H1 title from markdown text."""
    for line in md_text.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"


# ── Rendering ───────────────────────────────────────────────────────────────

def render_markdown_to_html(
    md_text: str,
    css_text: str,
    template_text: str,
) -> str:
    """Convert markdown string to a full HTML document."""
    import markdown
    from jinja2 import Template

    extensions = [
        "markdown.extensions.tables",
        "markdown.extensions.fenced_code",
        "markdown.extensions.smarty",
    ]
    body_html = markdown.markdown(md_text, extensions=extensions, output_format="html5")

    title = extract_title(md_text)
    tmpl = Template(template_text)
    return tmpl.render(title=title, css=css_text, body_html=body_html)


async def html_to_pdf(html: str, output_path: Path) -> None:
    """Render HTML to PDF using Playwright Chromium."""
    from playwright.async_api import async_playwright

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html, wait_until="networkidle")
        await page.pdf(
            path=str(output_path),
            format="A4",
            margin={"top": "20mm", "right": "18mm", "bottom": "20mm", "left": "18mm"},
            print_background=True,
        )
        await browser.close()


# ── Build cache ─────────────────────────────────────────────────────────────

@dataclass
class BuildRecord:
    md_sha256: str
    css_sha256: str
    template_sha256: str


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_str(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _safe_mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _load_build_index(path: Path) -> dict[str, BuildRecord]:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {k: BuildRecord(**v) for k, v in raw.items()}


def _save_build_index(path: Path, index: dict[str, BuildRecord]) -> None:
    _safe_mkdir(path.parent)
    raw = {k: asdict(v) for k, v in index.items()}
    path.write_text(json.dumps(raw, indent=2), encoding="utf-8")


# ── Google Drive ────────────────────────────────────────────────────────────

def _drive_service(oauth_client: Path, oauth_token: Path):
    """Build Drive service using OAuth user login."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    scopes = ["https://www.googleapis.com/auth/drive"]
    creds = None
    if oauth_token.exists():
        creds = Credentials.from_authorized_user_file(str(oauth_token), scopes=scopes)

    if creds and getattr(creds, "expired", False) and getattr(creds, "refresh_token", None):
        creds.refresh(Request())
    elif not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(oauth_client), scopes=scopes)
        creds = flow.run_local_server(port=0)

    if not creds:
        raise SystemExit("OAuth credentials could not be created")

    _safe_mkdir(oauth_token.parent)
    oauth_token.write_text(creds.to_json(), encoding="utf-8")
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def _drive_list_children(service, parent_id: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page_token = None
    while True:
        resp = (
            service.files()
            .list(
                q=f"'{parent_id}' in parents and trashed=false",
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token,
                pageSize=1000,
            )
            .execute()
        )
        items.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return items


def _drive_find_child(service, parent_id: str, name: str, mime_type: str | None = None):
    for item in _drive_list_children(service, parent_id):
        if item.get("name") != name:
            continue
        if mime_type and item.get("mimeType") != mime_type:
            continue
        return item
    return None


def _drive_ensure_folder(service, parent_id: str, folder_name: str, dry_run: bool) -> str:
    FOLDER_MIME = "application/vnd.google-apps.folder"
    if dry_run:
        digest = hashlib.sha256(f"{parent_id}/{folder_name}".encode()).hexdigest()[:12]
        return f"DRY_RUN_{digest}"

    found = _drive_find_child(service, parent_id, folder_name, mime_type=FOLDER_MIME)
    if found:
        return found["id"]

    metadata = {"name": folder_name, "mimeType": FOLDER_MIME, "parents": [parent_id]}
    created = service.files().create(body=metadata, fields="id").execute()
    return created["id"]


def _drive_upload_pdf(service, *, parent_id: str, local_pdf: Path, remote_name: str, dry_run: bool):
    from googleapiclient.http import MediaFileUpload

    if dry_run:
        return

    existing = _drive_find_child(service, parent_id, remote_name, mime_type="application/pdf")
    media = MediaFileUpload(str(local_pdf), mimetype="application/pdf", resumable=False)

    if existing:
        service.files().update(fileId=existing["id"], media_body=media).execute()
    else:
        body = {"name": remote_name, "parents": [parent_id]}
        service.files().create(body=body, media_body=media, fields="id").execute()


# ── Main pipeline ───────────────────────────────────────────────────────────

def iter_tractate_files(root: Path) -> list[Path]:
    """Get all markdown tractate files, sorted."""
    return sorted(root.glob("*.md"))


def build_and_upload(
    *,
    tractates_dir: Path,
    output_root: Path,
    css_path: Path,
    template_path: Path,
    drive_root_id: str,
    dry_run: bool,
    force: bool,
    build_only: bool,
    limit: int | None,
    only: list[str] | None,
    oauth_client: Path,
    oauth_token: Path,
) -> tuple[int, int, int]:
    """Build PDFs and upload to Drive.

    Returns (main_built, notes_built, uploaded).
    """
    css_text = css_path.read_text(encoding="utf-8")
    template_text = template_path.read_text(encoding="utf-8")
    css_sha = _sha256_file(css_path)
    template_sha = _sha256_file(template_path)

    index_path = CACHE_DIR / "pdf_build_index.json"
    index = _load_build_index(index_path)

    main_pdf_dir = output_root / "tractates"
    notes_pdf_dir = output_root / "editor_notes"
    _safe_mkdir(main_pdf_dir)
    _safe_mkdir(notes_pdf_dir)

    # Resolve file list
    if only:
        md_files = []
        for name in only:
            p = tractates_dir / name
            if not p.suffix:
                p = p.with_suffix(".md")
            if not p.exists():
                print(f"WARNING: {p} not found, skipping")
                continue
            md_files.append(p)
    else:
        md_files = iter_tractate_files(tractates_dir)

    if limit is not None:
        md_files = md_files[:limit]

    # Drive service (lazy init)
    service = None
    editor_notes_folder_id = None
    if not build_only:
        service = _drive_service(oauth_client, oauth_token)
        editor_notes_folder_id = _drive_ensure_folder(
            service, drive_root_id, EDITOR_NOTES_FOLDER_NAME, dry_run
        )

    main_built = 0
    notes_built = 0
    uploaded = 0
    total = len(md_files)

    for i, md_path in enumerate(md_files, 1):
        filename = md_path.stem
        md_text = md_path.read_text(encoding="utf-8")
        md_sha = _sha256_str(md_text)

        main_text, editor_notes = split_tractate(md_text)

        main_pdf = main_pdf_dir / f"{filename}.pdf"
        notes_pdf = notes_pdf_dir / f"{filename}_notes.pdf"

        # Cache keys
        main_key = f"main/{filename}"
        notes_key = f"notes/{filename}"

        status = f"[{i}/{total}] {filename}"

        # ── Build main text PDF ─────────────────────────────────────────
        main_rec = index.get(main_key)
        main_up_to_date = (
            main_rec is not None
            and main_rec.md_sha256 == md_sha
            and main_rec.css_sha256 == css_sha
            and main_rec.template_sha256 == template_sha
            and main_pdf.exists()
        )

        if main_up_to_date and not force:
            print(f"{status} main: cached", end="")
        else:
            print(f"{status} main: building...", end=" ", flush=True)
            html = render_markdown_to_html(main_text, css_text, template_text)
            asyncio.run(html_to_pdf(html, main_pdf))
            index[main_key] = BuildRecord(md_sha256=md_sha, css_sha256=css_sha, template_sha256=template_sha)
            main_built += 1
            print("done", end="")

        # Upload main PDF
        if service and not build_only:
            print(" → uploading...", end=" ", flush=True)
            _drive_upload_pdf(
                service,
                parent_id=drive_root_id,
                local_pdf=main_pdf,
                remote_name=f"{filename}.pdf",
                dry_run=dry_run,
            )
            uploaded += 1
            print("✓")
        else:
            print()

        # ── Build editor notes PDF (if notes exist) ────────────────────
        if editor_notes:
            notes_rec = index.get(notes_key)
            notes_up_to_date = (
                notes_rec is not None
                and notes_rec.md_sha256 == md_sha
                and notes_rec.css_sha256 == css_sha
                and notes_rec.template_sha256 == template_sha
                and notes_pdf.exists()
            )

            if notes_up_to_date and not force:
                print(f"{'':>{len(status)}} notes: cached", end="")
            else:
                print(f"{'':>{len(status)}} notes: building...", end=" ", flush=True)
                html = render_markdown_to_html(editor_notes, css_text, template_text)
                asyncio.run(html_to_pdf(html, notes_pdf))
                index[notes_key] = BuildRecord(md_sha256=md_sha, css_sha256=css_sha, template_sha256=template_sha)
                notes_built += 1
                print("done", end="")

            # Upload notes PDF
            if service and not build_only and editor_notes_folder_id:
                print(" → uploading...", end=" ", flush=True)
                _drive_upload_pdf(
                    service,
                    parent_id=editor_notes_folder_id,
                    local_pdf=notes_pdf,
                    remote_name=f"{filename}_notes.pdf",
                    dry_run=dry_run,
                )
                uploaded += 1
                print("✓")
            else:
                print()

        # Save index after each file
        _save_build_index(index_path, index)

    return main_built, notes_built, uploaded


def main():
    parser = argparse.ArgumentParser(
        description="Build PDFs from NHL tractates and sync to Google Drive"
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview Drive operations")
    parser.add_argument("--force", action="store_true", help="Rebuild all PDFs even if cached")
    parser.add_argument("--build-only", action="store_true", help="Build PDFs only, skip Drive upload")
    parser.add_argument("--limit", type=int, default=None, help="Process only first N files")
    parser.add_argument(
        "--only", action="append", default=[],
        help="Process specific file(s) by name (repeatable)"
    )
    parser.add_argument("--css", default=str(DEFAULT_CSS), help="CSS file path")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE), help="HTML template path")
    parser.add_argument(
        "--drive-root-id", default=DRIVE_ROOT_ID,
        help=f"Google Drive folder ID (default: {DRIVE_ROOT_ID})"
    )
    parser.add_argument(
        "--oauth-client", default=str(DEFAULT_OAUTH_CLIENT),
        help="OAuth client JSON path"
    )
    parser.add_argument(
        "--oauth-token", default=str(DEFAULT_OAUTH_TOKEN),
        help="OAuth token cache path"
    )

    args = parser.parse_args()

    if not TRACTATES_DIR.exists():
        raise SystemExit(f"Tractates directory not found: {TRACTATES_DIR}")

    main_built, notes_built, uploaded = build_and_upload(
        tractates_dir=TRACTATES_DIR,
        output_root=OUTPUT_ROOT,
        css_path=Path(args.css),
        template_path=Path(args.template),
        drive_root_id=args.drive_root_id,
        dry_run=args.dry_run,
        force=args.force,
        build_only=args.build_only,
        limit=args.limit,
        only=args.only or None,
        oauth_client=Path(args.oauth_client),
        oauth_token=Path(args.oauth_token),
    )

    dry = " (dry-run)" if args.dry_run else ""
    print(f"\nMain PDFs built: {main_built}")
    print(f"Editor notes PDFs built: {notes_built}")
    if not args.build_only:
        print(f"Files uploaded: {uploaded}{dry}")


if __name__ == "__main__":
    main()
