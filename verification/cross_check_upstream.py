#!/usr/bin/env python3
"""Machine link between the pinned upstream release and the local snapshot.

Given a checkout of the upstream `pompeiu_validation_certificate` directory,
verify every pinned hash from `upstream.lock`, compare the published
upstream certificate values against `upstream_snapshot.json`, and derive the
ball bounds used by the extension (31 < p0 < 32 and ||p||_rho < 55) from the
exact hexadecimal center plus the validated radius.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def fail(message: str) -> None:
    raise RuntimeError(f"UPSTREAM CROSS-CHECK FAILED: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_lock(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            key, value = line.split("=", 1)
            entries[key] = value
    return entries


def decimal(value: str) -> Fraction:
    if "." not in value:
        return Fraction(int(value))
    whole, frac = value.split(".")
    sign = -1 if whole.startswith("-") else 1
    whole = whole.lstrip("-")
    return sign * Fraction(int(whole + frac), 10 ** len(frac))


def main() -> int:
    cert_dir = Path(sys.argv[1]).resolve()
    repo_root = cert_dir.parent
    lock = load_lock(HERE / "upstream.lock")
    snapshot = json.loads((HERE / "upstream_snapshot.json").read_text(encoding="utf-8"))

    for label in ("center", "inverse", "certificate", "source_manifest"):
        target = repo_root / lock[f"{label}_path"]
        require(target.is_file(), f"missing upstream file {target}")
        digest = sha256(target.read_bytes()).hexdigest()
        require(digest == lock[f"{label}_sha256"], f"hash mismatch for {label}: {digest}")
        require(digest == snapshot["authenticated_files"][f"{label}_sha256"],
                f"snapshot hash mismatch for {label}")

    upstream = json.loads((cert_dir / "certificate.json").read_text(encoding="utf-8"))
    require(upstream["status"] == "PROVED", "upstream certificate status is not PROVED")
    require(upstream["checks"]["passed"] is True, "upstream checks flag is not set")
    params = upstream["parameters"]
    require([params[k] for k in ("L", "S", "R", "J")] == [60, 40, 30, 30],
            "upstream split parameters changed")
    require(decimal(str(params["rho"])) == Fraction(21, 20), "upstream rho changed")

    bounds = upstream["bounds"]
    majors = snapshot["majorants"]
    for name in ("Y", "Z", "C2", "C3"):
        require(decimal(str(bounds[name]["hi"])) == decimal(majors[name]),
                f"upstream bound {name} differs from snapshot")
    radius = decimal(majors["radius"])
    require(decimal(str(bounds["radius"])) == radius, "upstream radius differs from snapshot")
    require(decimal(str(bounds["univalence_sum"]["hi"]))
            == decimal(snapshot["geometry"]["univalence_sum_upper"]),
            "upstream univalence sum differs from snapshot")
    require(decimal(str(bounds["p1_abs_lower"]["lo"]))
            >= decimal(snapshot["center"]["first_shape_coefficient_abs_lower"]),
            "upstream first-shape-coefficient bound differs from snapshot")

    tokens = (repo_root / lock["center_path"]).read_text(encoding="ascii").split()
    require(tokens[:4] == ["60", "40", "30", "30"], "unexpected center header")
    require(tokens[4] == snapshot["center"]["p0_hex_binary64"],
            "snapshot p0 token differs from upstream center file")
    shape = [Fraction(*float.fromhex(t).as_integer_ratio()) for t in tokens[4:35]]
    p0 = shape[0]
    rho = Fraction(21, 20)
    shape_ball_slack = radius / (2 * 31)
    require(Fraction(31) < p0, "center p0 is not above 31")
    require(p0 + shape_ball_slack < Fraction(32), "ball p0 bound fails")
    weighted = sum(abs(c) * rho**j for j, c in enumerate(shape))
    require(weighted + shape_ball_slack < Fraction(55), "ball shape-norm bound fails")

    print("UPSTREAM CROSS-CHECK: PASS")
    print(f"pinned hashes verified: center, inverse, certificate, source_manifest")
    print(f"upstream (Y,Z,C2,C3,radius,univalence,p1) match the snapshot")
    print(f"derived ball bounds: 31 < p0 <= {float(p0 + shape_ball_slack):.9f} < 32")
    print(f"derived weighted shape norm <= {float(weighted + shape_ball_slack):.6f} < 55")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
