#!/usr/bin/env python3
"""
Validate a skill folder.

Checks:
  - Folder exists and contains SKILL.md
  - SKILL.md has YAML frontmatter with `name` and `description`
  - Folder name matches the `name:` field
  - Description is non-trivial (>= 30 chars)

Usage:
    python scripts/validate.py skills/my-skill
    python scripts/validate.py skills/*           # validates each folder
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Minimal YAML-ish parser for the simple `key: value` frontmatter we use."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    out: dict[str, str] = {}
    current_key: str | None = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        # Continuation line (indented) - append to previous value
        if line.startswith((" ", "\t")) and current_key:
            out[current_key] = (out[current_key] + " " + line.strip()).strip()
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        current_key = key.strip()
        out[current_key] = value.strip()
    return out


def validate_skill(skill_path: Path) -> tuple[bool, list[str]]:
    """Return (ok, messages). Messages include both errors and warnings."""
    errors: list[str] = []

    if not skill_path.exists():
        return False, [f"path does not exist: {skill_path}"]
    if not skill_path.is_dir():
        return False, [f"not a directory: {skill_path}"]

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, [f"missing SKILL.md in {skill_path}"]

    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        return False, ["SKILL.md is missing YAML frontmatter (--- ... ---)"]

    name = fm.get("name", "").strip()
    description = fm.get("description", "").strip()

    if not name:
        errors.append("frontmatter missing `name`")
    if not description:
        errors.append("frontmatter missing `description`")
    elif len(description) < 30:
        errors.append(
            f"description is suspiciously short ({len(description)} chars); "
            "be specific about when the skill should trigger"
        )

    if name and name != skill_path.name:
        errors.append(
            f"folder name `{skill_path.name}` does not match frontmatter "
            f"name `{name}` — these must match for install/upgrade to work"
        )

    if name and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        errors.append(
            f"name `{name}` should be kebab-case (lowercase letters, digits, hyphens)"
        )

    return len(errors) == 0, errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    paths = [Path(p) for p in argv[1:]]
    # Expand: if `skills/` is passed, validate each child.
    expanded: list[Path] = []
    for p in paths:
        if p.is_dir() and not (p / "SKILL.md").exists():
            expanded.extend(sorted(c for c in p.iterdir() if c.is_dir()))
        else:
            expanded.append(p)

    if not expanded:
        print("no skills to validate", file=sys.stderr)
        return 0

    failed = 0
    for skill in expanded:
        ok, msgs = validate_skill(skill)
        if ok:
            print(f"OK    {skill}")
        else:
            failed += 1
            print(f"FAIL  {skill}")
            for m in msgs:
                print(f"      - {m}")

    if failed:
        print(f"\n{failed} skill(s) failed validation", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
