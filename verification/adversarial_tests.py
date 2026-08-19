#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
FILES = [
    "verify_extension.py",
    "verify_extension.mjs",
    "extension_certificate.json",
    "upstream_snapshot.json",
    "upstream.lock",
]
NODE = shutil.which("node")


def run_python(directory: Path, optimized: bool = False) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable]
    if optimized:
        cmd.append("-O")
    cmd.append("verify_extension.py")
    return subprocess.run(cmd, cwd=directory, text=True, capture_output=True)


def run_node(directory: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([NODE, "verify_extension.mjs"], cwd=directory,
                          text=True, capture_output=True)


def require_rejected(directory: Path, label: str) -> None:
    if run_python(directory).returncode == 0:
        raise RuntimeError(f"python verifier accepted corruption: {label}")
    if NODE and run_node(directory).returncode == 0:
        raise RuntimeError(f"node verifier accepted corruption: {label}")


def copy_fixture(dst: Path) -> None:
    for name in FILES:
        shutil.copy2(HERE / name, dst / name)


def corrupted(label: str, mutate) -> None:
    with tempfile.TemporaryDirectory() as raw:
        d = Path(raw)
        copy_fixture(d)
        mutate(d)
        require_rejected(d, label)


def edit_json(directory: Path, name: str, mutate) -> None:
    path = directory / name
    data = json.loads(path.read_text())
    mutate(data)
    path.write_text(json.dumps(data))


def main() -> int:
    normal = run_python(HERE)
    optimized = run_python(HERE, optimized=True)
    if normal.returncode != 0 or optimized.returncode != 0:
        raise RuntimeError("uncorrupted python verifier failed")
    if normal.stdout != optimized.stdout:
        raise RuntimeError("normal and optimized outputs differ")
    if NODE and run_node(HERE).returncode != 0:
        raise RuntimeError("uncorrupted node verifier failed")

    corrupted("alpha", lambda d: edit_json(
        d, "extension_certificate.json",
        lambda c: c["extension_majorants"].update(preconditioner_norm_upper="1170")))
    corrupted("value coefficient", lambda d: edit_json(
        d, "extension_certificate.json",
        lambda c: c["extension_majorants"].update(value_perturbation_coefficient="1900")))
    corrupted("conformal square norm", lambda d: edit_json(
        d, "extension_certificate.json",
        lambda c: c["extension_majorants"].update(conformal_square_norm_upper="1.3")))
    corrupted("tau endpoint", lambda d: edit_json(
        d, "extension_certificate.json",
        lambda c: c["parameter_interval"].update(tau_upper="0.001")))
    corrupted("expected base radii", lambda d: edit_json(
        d, "extension_certificate.json",
        lambda c: c["expected_exact_values"].update(base_radii="-0.000000378719")))
    corrupted("upstream Y", lambda d: edit_json(
        d, "upstream_snapshot.json",
        lambda s: s["majorants"].update(Y="0.000000000158")))
    corrupted("upstream Z", lambda d: edit_json(
        d, "upstream_snapshot.json",
        lambda s: s["majorants"].update(Z="0.7")))
    corrupted("upstream C3", lambda d: edit_json(
        d, "upstream_snapshot.json",
        lambda s: s["majorants"].update(C3="0.02")))
    corrupted("shape-norm ball bound", lambda d: edit_json(
        d, "upstream_snapshot.json",
        lambda s: s["center"].update(weighted_p_upper="70")))
    corrupted("center p0", lambda d: edit_json(
        d, "upstream_snapshot.json",
        lambda s: s["center"].update(p0_hex_binary64="0x1.0p+6")))
    corrupted("snapshot/lock hash disagreement", lambda d: edit_json(
        d, "upstream_snapshot.json",
        lambda s: s["authenticated_files"].update(center_sha256="0" * 64)))
    corrupted("missing upstream snapshot",
              lambda d: (d / "upstream_snapshot.json").unlink())
    corrupted("missing upstream lock",
              lambda d: (d / "upstream.lock").unlink())

    checkers = "python+node" if NODE else "python"
    print(f"ADVERSARIAL VERIFIER TESTS: PASS ({checkers}, 13 corruptions rejected)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
