#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd -- "$HERE/.." && pwd)
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

python3 "$ROOT/verify_manifest.py"
python3 "$HERE/verify_extension.py" > "$WORK/python.txt"
python3 -O "$HERE/verify_extension.py" > "$WORK/python-O.txt"
cmp "$WORK/python.txt" "$WORK/python-O.txt"
cmp "$WORK/python.txt" "$HERE/expected_python.txt"

if command -v node >/dev/null 2>&1; then
  node "$HERE/verify_extension.mjs" > "$WORK/node.txt"
  cmp "$WORK/node.txt" "$HERE/expected_node.txt"
fi

python3 "$HERE/adversarial_tests.py"
python3 "$ROOT/formalization/scripts/check_no_holes.py"
if command -v lake >/dev/null 2>&1; then
  cp -a "$ROOT/formalization" "$WORK/formalization"
  (cd "$WORK/formalization" && lake build) > "$WORK/lean-build.txt" 2>&1
fi
python3 "$ROOT/verify_manifest.py"
echo "REPRODUCTION: PASS"
