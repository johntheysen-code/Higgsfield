#!/usr/bin/env python3
"""Hand generated designs off to the POD pipeline's inbox/ with no manual renames.

Every design has a sidecar in designs/ giving the final name the pipeline wants
(`filename`). This script finds each design's image among your downloads, renames
it to `filename`, and copies image + sidecar into the inbox.

A sidecar's image is located by trying, in order:
  1. Exact name  — a download already named exactly `filename`.
  2. Higgsfield  — a download whose name contains the sidecar's `higgsfield_job_id`
                   UUID (Higgsfield bakes the job-id into every download filename).
  3. Source name — a download named exactly the sidecar's `source_filename`
                   (used for external images, e.g. made in ChatGPT, which carry
                   no Higgsfield UUID — set `source_filename` to the file as saved).

Workflow:
    1. Download the approved images (Higgsfield viewer and/or ChatGPT) into one folder.
    2. Run:  python3 scripts/handoff.py
    3. Done. inbox/ has correctly-named PNGs + matching .json sidecars, no renames.

Defaults can be overridden with flags (see --help). Copies by default; pass
--move to move instead. Use --dry-run to preview without touching anything.
"""
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)
IMAGE_EXTS = {".png", ".webp", ".jpg", ".jpeg"}


def load_sidecars(designs_dir: Path):
    """Return a list of dicts: {path, filename, job_id, source_filename}."""
    out = []
    for sc in sorted(designs_dir.rglob("*.json")):
        try:
            data = json.loads(sc.read_text())
        except (json.JSONDecodeError, OSError) as e:
            print(f"  ! skipping unreadable sidecar {sc}: {e}", file=sys.stderr)
            continue
        filename = data.get("filename")
        if not filename:
            print(f"  ! sidecar {sc.name} has no `filename` — skipped", file=sys.stderr)
            continue
        out.append({
            "path": sc,
            "filename": filename,
            "job_id": (data.get("higgsfield_job_id") or "").lower(),
            "source_filename": data.get("source_filename") or "",
        })
    return out


def index_downloads(downloads_dir: Path):
    """Index downloaded images by exact name and by any UUID found in the name."""
    by_name, by_uuid = {}, {}
    for p in downloads_dir.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in IMAGE_EXTS:
            continue
        by_name[p.name] = p
        m = UUID_RE.search(p.name)
        if m:
            key = m.group(0).lower()
            # keep the most recently modified file if a UUID repeats
            if key not in by_uuid or p.stat().st_mtime > by_uuid[key].stat().st_mtime:
                by_uuid[key] = p
    return by_name, by_uuid


def find_image(sc, by_name, by_uuid):
    """Locate the image for one sidecar; return (path, how) or (None, None)."""
    if sc["filename"] in by_name:
        return by_name[sc["filename"]], "exact-name"
    if sc["job_id"] and sc["job_id"] in by_uuid:
        return by_uuid[sc["job_id"]], "higgsfield-uuid"
    if sc["source_filename"] and sc["source_filename"] in by_name:
        return by_name[sc["source_filename"]], "source-name"
    return None, None


def main():
    repo_root = Path(__file__).resolve().parent.parent
    default_pipeline = os.environ.get("PIPELINE_WORKING_DIR", r"C:\Users\Hello\pod-pipeline")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--designs", type=Path, default=repo_root / "designs",
                    help="Folder of sidecars (default: ./designs)")
    ap.add_argument("--downloads", type=Path, default=Path.home() / "Downloads",
                    help="Where the images were downloaded (default: ~/Downloads)")
    ap.add_argument("--inbox", type=Path, default=Path(default_pipeline) / "inbox",
                    help=r"Pipeline inbox (default: $PIPELINE_WORKING_DIR\inbox or C:\Users\Hello\pod-pipeline\inbox)")
    ap.add_argument("--move", action="store_true", help="Move files instead of copying")
    ap.add_argument("--dry-run", action="store_true", help="Show what would happen, change nothing")
    args = ap.parse_args()

    if not args.designs.is_dir():
        sys.exit(f"designs folder not found: {args.designs}")
    if not args.downloads.is_dir():
        sys.exit(f"downloads folder not found: {args.downloads}")

    sidecars = load_sidecars(args.designs)
    if not sidecars:
        sys.exit(f"no sidecars found under {args.designs}")
    by_name, by_uuid = index_downloads(args.downloads)

    xfer = shutil.move if args.move else shutil.copy2
    verb = "MOVE" if args.move else "COPY"
    matched, missing = 0, []

    if not args.dry_run:
        args.inbox.mkdir(parents=True, exist_ok=True)

    for sc in sorted(sidecars, key=lambda s: s["filename"]):
        img, how = find_image(sc, by_name, by_uuid)
        if not img:
            missing.append(sc["filename"])
            continue
        dest_img = args.inbox / sc["filename"]
        dest_json = args.inbox / (Path(sc["filename"]).stem + ".json")
        print(f"  {verb}  {img.name}  ->  inbox/{sc['filename']}   [{how}]")
        print(f"  COPY  {sc['path'].name}  ->  inbox/{dest_json.name}")
        if not args.dry_run:
            xfer(str(img), str(dest_img))
            shutil.copy2(str(sc["path"]), str(dest_json))  # sidecar always copied, never moved
        matched += 1

    print(f"\n{'(dry run) ' if args.dry_run else ''}done: {matched} handed off, {len(missing)} missing.")
    if missing:
        print("Not found in downloads (download these, or set `source_filename` for external images, then re-run):")
        for f in missing:
            print(f"  - {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
