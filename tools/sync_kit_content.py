#!/usr/bin/env python3
"""Sync the bundled kit content snapshot from an anaplan-kit checkout.

Copies the Markdown of ``docs/``, ``cookbook/`` and ``blueprints/`` from an
anaplan-kit checkout into ``src/anaplan_kit_mcp/_content/`` and records the
source commit hash in ``_content/KIT_COMMIT``. The snapshot ships as package
data, so ``pip install anaplan-kit-mcp`` is fully self-contained.

Usage (from the repo root)::

    python tools/sync_kit_content.py [--source /path/to/anaplan-kit]

The source defaults to ``$ANAPLAN_KIT_ROOT`` or a sibling ``../anaplan-kit``
checkout. Re-run before a release to refresh the snapshot.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT_DEST = REPO_ROOT / "src" / "anaplan_kit_mcp" / "_content"
SYNCED_DIRS = ("docs", "cookbook", "blueprints")
KIT_COMMIT_FILE = "KIT_COMMIT"


def _default_source() -> Path | None:
    env = os.environ.get("ANAPLAN_KIT_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    sibling = REPO_ROOT.parent / "anaplan-kit"
    return sibling if sibling.is_dir() else None


def _source_commit(source: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(source), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return out.stdout.strip() or "unknown"


def sync(source: Path) -> int:
    if not (source / "cookbook").is_dir():
        print(f"error: {source} does not look like an anaplan-kit checkout", file=sys.stderr)
        return 1

    copied = 0
    for name in SYNCED_DIRS:
        src_dir = source / name
        dest_dir = CONTENT_DEST / name
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        if not src_dir.is_dir():
            print(f"warning: source has no {name}/ directory, skipping", file=sys.stderr)
            continue
        for md in sorted(src_dir.rglob("*.md")):
            rel = md.relative_to(src_dir)
            target = dest_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(md, target)
            copied += 1

    commit = _source_commit(source)
    CONTENT_DEST.mkdir(parents=True, exist_ok=True)
    (CONTENT_DEST / KIT_COMMIT_FILE).write_text(commit + "\n", encoding="utf-8")
    print(f"synced {copied} Markdown files from {source}")
    print(f"source commit: {commit} (recorded in _content/{KIT_COMMIT_FILE})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="anaplan-kit checkout to sync from (default: $ANAPLAN_KIT_ROOT or ../anaplan-kit)",
    )
    args = parser.parse_args()
    source = (args.source or _default_source() or Path()).resolve()
    if not source or not source.is_dir():
        print(
            "error: no anaplan-kit checkout found — pass --source or set ANAPLAN_KIT_ROOT",
            file=sys.stderr,
        )
        return 1
    return sync(source)


if __name__ == "__main__":
    raise SystemExit(main())
