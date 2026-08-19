#!/usr/bin/env python3
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS"
GENERATED_SUFFIXES = {".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".blg", ".toc"}


def included(path: Path) -> bool:
    if not path.is_file() or path == MANIFEST:
        return False
    rel = path.relative_to(ROOT)
    if ".lake" in rel.parts:
        return False
    if path.suffix in GENERATED_SUFFIXES and rel.parts and rel.parts[0] == "paper":
        return False
    return True


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


lines = [
    f"{digest(path)}  {path.relative_to(ROOT).as_posix()}"
    for path in sorted(ROOT.rglob("*"))
    if included(path)
]
MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"WROTE SHA256SUMS ({len(lines)} files)")
