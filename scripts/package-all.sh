#!/usr/bin/env bash
# Package every skill in skills/ into dist/.
# Usage: ./scripts/package-all.sh

set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d skills ] || [ -z "$(ls -A skills 2>/dev/null)" ]; then
  echo "no skills found in skills/"
  exit 0
fi

mkdir -p dist
rm -f dist/*.skill

count=0
for skill in skills/*/; do
  [ -d "$skill" ] || continue
  [ -f "${skill}SKILL.md" ] || {
    echo "skipping ${skill} (no SKILL.md)"
    continue
  }
  python3 scripts/validate.py "$skill"
  python3 scripts/package.py "$skill" --output dist
  count=$((count + 1))
done

echo
echo "packaged $count skill(s) into dist/"
ls -lh dist/*.skill 2>/dev/null || true
