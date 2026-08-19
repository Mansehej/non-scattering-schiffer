#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
WORK=${1:-"$HERE/upstream_work"}
rm -rf "$WORK"
mkdir -p "$WORK"

lock() { sed -n "s/^$1=//p" "$HERE/upstream.lock"; }
RECORD=$(lock zenodo_record)
ZIP_MD5=$(lock zenodo_zip_md5)

ARCHIVE="$WORK/upstream_zenodo.zip"
curl -fL "https://zenodo.org/records/${RECORD}/files/MColbrook/Pompeiu_Schiffer-v1.0.0.zip?download=1" -o "$ARCHIVE"
python3 - "$ARCHIVE" "$ZIP_MD5" <<'PY'
import hashlib
import sys

digest = hashlib.md5(open(sys.argv[1], "rb").read()).hexdigest()
if digest != sys.argv[2]:
    raise SystemExit(f"zenodo archive md5 mismatch: {digest}")
print(f"zenodo archive md5 verified: {digest}")
PY
unzip -q "$ARCHIVE" -d "$WORK"
ROOT=$(find "$WORK" -maxdepth 1 -type d -name 'MColbrook-Pompeiu_Schiffer-*' | head -n 1)
test -n "$ROOT"

python3 "$HERE/cross_check_upstream.py" "$ROOT/pompeiu_validation_certificate"
(
  cd "$ROOT/pompeiu_validation_certificate"
  python3 verify_certificate.py certificate.json
)
echo "UPSTREAM AUTHENTICATED-LEAF CHECK: PASS"
echo "Full source-to-audit reproduction, which is substantially more expensive, is available as:"
echo "  cd '$ROOT/pompeiu_validation_certificate' && THREADS=80 ./reproduce.sh"
