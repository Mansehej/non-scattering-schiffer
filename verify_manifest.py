#!/usr/bin/env python3
from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS"


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    if not MANIFEST.is_file():
        print("missing SHA256SUMS", file=sys.stderr)
        return 1
    listed: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        token, rel = line.split("  ", 1)
        if rel in listed:
            print(f"duplicate manifest entry: {rel}", file=sys.stderr)
            return 1
        listed[rel] = token
    generated_suffixes = {".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".blg", ".toc"}

    def included(path: Path) -> bool:
        if not path.is_file() or path == MANIFEST:
            return False
        rel = path.relative_to(ROOT)
        if ".lake" in rel.parts:
            return False
        if path.suffix in generated_suffixes and rel.parts and rel.parts[0] == "paper":
            return False
        return True

    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if included(p)}
    if actual != set(listed):
        print(f"manifest set mismatch: missing={sorted(actual-set(listed))}, extra={sorted(set(listed)-actual)}", file=sys.stderr)
        return 1
    for rel, expected in sorted(listed.items()):
        if digest(ROOT / rel) != expected:
            print(f"hash mismatch: {rel}", file=sys.stderr)
            return 1
    print(f"MANIFEST: VERIFIED ({len(listed)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
