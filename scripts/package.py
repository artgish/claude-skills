#!/usr/bin/env python3
"""
Package a skill folder into a .skill file (zip archive).

Usage:
    python scripts/package.py skills/my-skill
    python scripts/package.py skills/my-skill --output dist/

The resulting .skill file expands to <skill-name>/... so users can unzip it
directly into ~/.claude/skills/.
"""

from __future__ import annotations

import argparse
import fnmatch
import sys
import zipfile
from pathlib import Path

# Mirrors skill-creator's package_skill.py exclusion rules.
EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git", ".venv", "venv"}
EXCLUDE_GLOBS = {"*.pyc", "*.pyo", "*.swp"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}
# Excluded only at the skill root (evals are dev-only artifacts).
ROOT_EXCLUDE_DIRS = {"evals", "tests"}


def should_exclude(rel_path: Path) -> bool:
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    # parts[0] is the skill folder name; parts[1] is its first subdir.
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    name = rel_path.name
    if name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_GLOBS)


def package(skill_path: Path, output_dir: Path) -> Path | None:
    skill_path = skill_path.resolve()
    if not skill_path.is_dir():
        print(f"error: not a directory: {skill_path}", file=sys.stderr)
        return None
    if not (skill_path / "SKILL.md").exists():
        print(f"error: missing SKILL.md in {skill_path}", file=sys.stderr)
        return None

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{skill_path.name}.skill"

    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(skill_path.rglob("*")):
            if not file_path.is_file():
                continue
            arcname = file_path.relative_to(skill_path.parent)
            if should_exclude(arcname):
                continue
            zf.write(file_path, arcname)

    size_kb = out_file.stat().st_size / 1024
    print(f"packaged {skill_path.name} -> {out_file} ({size_kb:.1f} KB)")
    return out_file


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill", type=Path, help="path to skill folder")
    ap.add_argument("--output", "-o", type=Path, default=Path("dist"),
                    help="output directory (default: dist/)")
    args = ap.parse_args()

    result = package(args.skill, args.output)
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
