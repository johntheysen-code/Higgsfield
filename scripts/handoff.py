#!/usr/bin/env python3
"""Hand generated designs off to the POD pipeline's inbox/ with no manual renames.

Higgsfield names every download with its job-ID UUID, e.g.
    hf_20260526_231624_3ce77237-9d5a-4271-917b-a8e6b75690e3.png
and every sidecar in designs/ stores that same UUID in `higgsfield_job_id`
plus the final name the pipeline wants in `filename`. This script matches the
two by UUID, then copies each image (renamed to `filename`) and its sidecar
into the inbox.

Workflow:
    1. Download the approved images from the Higgsfield viewer (any names, any folder).
    2. Run:  python3 scripts/handoff.py
    3. Done. inbox/ now has correctly-named PNGs + matching .json sidecars.

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
    """Return {job_id: (sidecar_path, target_filename)} for every sidecar found."""
    out = {}
    for sc in designs_dir.rglob("*.json"):
        try:
            data = json.loads(sc.read_text())
        except (json.JSONDecodeError, OSError) as e:
            print(f"  ! skipping unreadable sidecar {sc}: {e}", file=sys.stderr)
            continue
        job_id = data.get("higgsfield_job_id")
        filename = data.get("filename")
        if not job_id or not filename:
            print(f"  ! sidecar {sc.name} missing job_id/filename — skipped", file=sys.stderr)
            continue
        out[job_id.lower()] = (sc, filename)
    return out


def index_downloads(downloads_dir: Path):
    """Return {job_id: image_path} for every downloaded image whose name holds a UUID.

    If several files share a UUID, keep the most recently modified one.
    """
    found = {}
    for p in downloads_dir.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in IMAGE_EXTS:
            continue
        m = UUID_RE.search(p.name)
        if not m:
            continue
        key = m.group(0).lower()
        if key not in found or p.stat().st_mtime > found[key].stat().st_mtime:
            found[key] = p
    return found


def main():
    repo_root = Path(__file__).resolve().parent.parent
    default_inbox = os.environ.get(
        "PIPELINE_WORKING_DIR", str(Path.home() / "pod-automation")
    )
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--designs", type=Path, default=repo_root / "designs",
                    help="Folder of sidecars (default: ./designs)")
    ap.add_argument("--downloads", type=Path, default=Path.home() / "Downloads",
                    help="Where the Higgsfield images were downloaded (default: ~/Downloads)")
    ap.add_argument("--inbox", type=Path, default=Path(default_inbox) / "inbox",
                    help="Pipeline inbox (default: $PIPELINE_WORKING_DIR/inbox or ~/pod-automation/inbox)")
    ap.add_argument("--move", action="store_true", help="Move files instead of copying")
    ap.add_argument("--dry-run", action="store_true", help="Show what would happen, change nothing")
    args = ap.parse_args()

    if not args.designs.is_dir():
        sys.exit(f"designs folder not found: {args.designs}")
    if not args.downloads.is_dir():
        sys.exit(f"downloads folder not found: {args.downloads}")

    sidecars = load_sidecars(args.designs)
    downloads = index_downloads(args.downloads)
    if not sidecars:
        sys.exit(f"no sidecars found under {args.designs}")

    xfer = shutil.move if args.move else shutil.copy2
    verb = "MOVE" if args.move else "COPY"
    matched, missing = 0, []

    if not args.dry_run:
        args.inbox.mkdir(parents=True, exist_ok=True)

    for job_id, (sidecar, filename) in sorted(sidecars.items(), key=lambda kv: kv[1][1]):
        img = downloads.get(job_id)
        if not img:
            missing.append(filename)
            continue
        dest_img = args.inbox / filename
        dest_json = args.inbox / (Path(filename).stem + ".json")
        print(f"  {verb}  {img.name}  ->  inbox/{filename}")
        print(f"  COPY  {sidecar.name}  ->  inbox/{dest_json.name}")
        if not args.dry_run:
            xfer(str(img), str(dest_img))
            shutil.copy2(str(sidecar), str(dest_json))  # sidecar always copied, never moved
        matched += 1

    print(f"\n{'(dry run) ' if args.dry_run else ''}done: {matched} handed off, {len(missing)} missing.")
    if missing:
        print("Not found in downloads (download these from the viewer, then re-run):")
        for f in missing:
            print(f"  - {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
