#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
sources = [root / "NonScattering.lean", *sorted((root / "NonScattering").rglob("*.lean"))]
forbidden = re.compile(
    r"\b(sorry|sorryAx|admit|axiom|native_decide|opaque|unsafe|partial|"
    r"implemented_by|extern|initialize|run_cmd)\b")
problems: list[str] = []
for path in sources:
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if forbidden.search(line):
            problems.append(f"{path.relative_to(root)}:{line_no}: {line.strip()}")
if problems:
    print("Forbidden proof-hole or escape-hatch marker found in project sources:")
    print("\n".join(problems))
    sys.exit(1)
print(f"Lean project-source scan ({len(sources)} files): "
      "no proof holes, axioms, or escape hatches")
