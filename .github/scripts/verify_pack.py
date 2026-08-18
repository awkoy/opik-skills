#!/usr/bin/env python3
"""Check a skills tree against the per-file checksums in a pack manifest.

Used twice by the sync, for two different questions that happen to have the same
answer:

1. *Is what we downloaded what we authorised?* The rolling release tag has its
   assets overwritten by every upstream build, so the manifest and the tarball are
   two separate downloads that can come from two different builds. Verifying the
   unpacked tree against the manifest we already validated ties them together —
   and catches a truncated or partial archive before `rsync --delete` gets a
   chance to remove released skills.

2. *Has the committed tree drifted?* The digest lives in a committed file, so a
   hand edit to `skills/` leaves it untouched. Without this check a matching digest
   would end the run and the edit would survive indefinitely.

Usage: verify_pack.py <manifest.json> <skills-root>
Exits 0 when the tree matches the manifest exactly, 1 otherwise, naming what drifted.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys

MAX_REPORTED = 20


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"usage: {argv[0]} <manifest.json> <skills-root>", file=sys.stderr)
        return 2

    manifest_path, root = pathlib.Path(argv[1]), pathlib.Path(argv[2])

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"cannot read manifest {manifest_path}: {error}", file=sys.stderr)
        return 1

    expected = {
        f"{skill['name']}/{entry['path']}": entry["sha256"]
        for skill in manifest.get("skills", [])
        for entry in skill.get("files", [])
    }
    if not expected:
        print(f"manifest {manifest_path} lists no files", file=sys.stderr)
        return 1

    present = (
        {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}
        if root.is_dir()
        else set()
    )

    drift: set[str] = (present - set(expected)) | (set(expected) - present)
    for path, digest in expected.items():
        target = root / path
        if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            drift.add(path)

    if not drift:
        return 0

    ordered = sorted(drift)
    for path in ordered[:MAX_REPORTED]:
        print(f"drifted: {path}", file=sys.stderr)
    if len(ordered) > MAX_REPORTED:
        print(f"... and {len(ordered) - MAX_REPORTED} more", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
