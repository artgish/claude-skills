#!/usr/bin/env bash
# Install every .skill in dist/ into ~/.claude/skills/.
# Usage: ./scripts/install-all.sh [source-dir]

set -euo pipefail

SRC="${1:-$(dirname "$0")/../dist}"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

if [ ! -d "$SRC" ]; then
  echo "source directory not found: $SRC"
  echo "run scripts/package-all.sh first, or pass a directory containing .skill files"
  exit 1
fi

shopt -s nullglob
skills=("$SRC"/*.skill)
shopt -u nullglob

if [ ${#skills[@]} -eq 0 ]; then
  echo "no .skill files in $SRC"
  exit 0
fi

mkdir -p "$DEST"

for skill_file in "${skills[@]}"; do
  name="$(basename "$skill_file" .skill)"
  echo "installing $name -> $DEST/$name"
  rm -rf "${DEST:?}/$name"
  unzip -q -o "$skill_file" -d "$DEST"
done

echo
echo "installed ${#skills[@]} skill(s) to $DEST"
echo "restart Claude Code (or open a new session) to pick them up"
