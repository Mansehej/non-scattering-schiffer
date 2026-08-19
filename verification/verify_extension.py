#!/usr/bin/env python3
"""Fail-closed exact-rational verifier for the extension certificate."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re
import sys
from typing import Any

HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"VERIFICATION FAILED: {message}")


def decimal(value: str) -> Fraction:
    require(isinstance(value, str), "decimal token is not a string")
    require(re.fullmatch(r"-?[0-9]+(?:\.[0-9]+)?", value) is not None,
            f"unsupported decimal token: {value!r}")
    sign = -1 if value.startswith("-") else 1
    unsigned = value[1:] if sign < 0 else value
    if "." not in unsigned:
        return Fraction(sign * int(unsigned), 1)
    whole, frac = unsigned.split(".")
    return Fraction(sign * int(whole + frac), 10 ** len(frac))


def exact_hex_binary64(token: str) -> Fraction:
    match = re.fullmatch(r"([+-]?)0x([0-9a-fA-F]+)(?:\.([0-9a-fA-F]+))?p([+-]?[0-9]+)", token)
    require(match is not None, f"malformed hexadecimal floating token: {token!r}")
    sign_token, whole, fractional, exponent_token = match.groups()
    fractional = fractional or ""
    mantissa = int(whole + fractional, 16)
    exponent = int(exponent_token) - 4 * len(fractional)
    value = Fraction(mantissa, 1)
    if exponent >= 0:
        value *= 2 ** exponent
    else:
        value /= 2 ** (-exponent)
    return -value if sign_token == "-" else value


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing file: {path.name}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"top-level JSON object required: {path.name}")
    return data


def load_lock(path: Path) -> dict[str, str]:
    require(path.is_file(), f"missing file: {path.name}")
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        require("=" in line, f"malformed lock line: {line!r}")
        key, value = line.split("=", 1)
        require(key not in entries, f"duplicate lock key: {key}")
        entries[key] = value
    return entries


def verify() -> list[str]:
    cert = load_json(HERE / "extension_certificate.json")
    require(cert.get("schema") == "non-scattering-positive-frequency-extension-v3",
            "unsupported extension schema")
    snapshot_name = cert.get("upstream_snapshot")
    require(snapshot_name == "upstream_snapshot.json", "unexpected upstream snapshot path")
    snapshot = load_json(HERE / snapshot_name)
    require(snapshot.get("schema") == "non-scattering-upstream-snapshot-v2",
            "unsupported upstream snapshot schema")

    lock = load_lock(HERE / "upstream.lock")
    hashes = snapshot["authenticated_files"]
    for label, token in hashes.items():
        require(re.fullmatch(r"[0-9a-f]{64}", token) is not None,
                f"malformed SHA-256 value for {label}")
    for label in ("center", "inverse", "certificate", "source_manifest"):
        require(hashes.get(f"{label}_sha256") == lock.get(f"{label}_sha256"),
                f"snapshot/lock hash disagreement for {label}")
    require(snapshot["paper"]["commit"] == lock.get("commit"),
            "snapshot/lock commit disagreement")
    require(snapshot["paper"]["repository"] == lock.get("repository"),
            "snapshot/lock repository disagreement")

    major = snapshot["majorants"]
    Y = decimal(major["Y"])
    Z = decimal(major["Z"])
    C2 = decimal(major["C2"])
    C3 = decimal(major["C3"])
    radius = decimal(major["radius"])
    require((Y, Z, C2, C3, radius) == (
        Fraction(159, 10**12), Fraction(621, 1000), Fraction(122),
        Fraction(3, 250), Fraction(1, 10**6)), "upstream majorants changed")

    center = snapshot["center"]
    b = exact_hex_binary64(center["p0_hex_binary64"])
    p0_lower = decimal(center["p0_lower"])
    p0_upper = decimal(center["p0_upper"])
    p_norm_upper = decimal(center["weighted_p_upper"])
    require(p0_lower == 31 and p0_upper == 32, "unexpected certified p0 interval")
    require(p0_lower < b < p0_upper, "exact center coefficient is outside (31,32)")
    require(b + radius / (2 * p0_lower) < p0_upper,
            "certified ball does not keep p0 below its upper bound")
    require(p_norm_upper == 55, "unexpected certified shape-norm bound")

    ext = cert["extension_majorants"]
    alpha = decimal(ext["preconditioner_norm_upper"])
    value_coeff = decimal(ext["value_perturbation_coefficient"])
    deriv_coeff = decimal(ext["derivative_perturbation_coefficient"])
    phi2 = decimal(ext["conformal_square_norm_upper"])
    require(alpha == 1180, "preconditioner majorant must be 1180")
    require(C3 * 96 * Fraction(32) ** 2 < alpha,
            "coarse authenticated majorants do not imply alpha < 1180")
    require((value_coeff, deriv_coeff, phi2) == (1906, 3, Fraction(5, 4)),
            "extension majorants changed")

    tau_max = decimal(cert["parameter_interval"]["tau_upper"])
    require(tau_max == Fraction(1, 10**13), "unexpected parameter endpoint")
    require(tau_max > 0, "parameter endpoint is not positive")

    # Derivation chain for the perturbation constants from the certified
    # ball bounds ||p|| < 55 and 31 < p0.  The step from psi to |phi|^2 uses
    # the upstream weighted-algebra convention: the weight rho^j attaches to
    # the angular block index only, so multiplication by the radial factor
    # |z|^2 is norm-nonexpansive and || |phi|^2 || <= ||psi||^2.
    psi_upper = 1 + (p_norm_upper - p0_lower) / (11 * p0_lower)
    require(psi_upper < Fraction(11, 10), "conformal factor bound fails")
    require(psi_upper ** 2 < phi2, "conformal square bound fails")

    u_max = tau_max * phi2 / 4
    require(u_max <= Fraction(1, 2), "Bessel majorant condition fails at endpoint")

    bessel_deviation = 2 * (phi2 / 4)
    datum_deviation = bessel_deviation + 2 / p0_lower**2
    require(datum_deviation < Fraction(63, 100), "Bessel datum deviation bound fails")
    require(p_norm_upper ** 2 * Fraction(63, 100) < value_coeff,
            "value perturbation coefficient underivable from ball bounds")

    xi_upper = 1 / (2 * p0_lower)
    dpsi_upper = Fraction(1, 11) * (xi_upper / p0_lower + p_norm_upper * xi_upper / p0_lower**2)
    require(dpsi_upper < Fraction(1, 7000), "conformal factor derivative bound fails")
    dsquare_upper = 2 * Fraction(11, 10) * Fraction(1, 7000)
    require(dsquare_upper < Fraction(1, 3000), "conformal square derivative bound fails")
    dH_upper = Fraction(1, 4) * Fraction(1, 3000) * 4
    deriv_derived = (2 * p_norm_upper * xi_upper * Fraction(63, 100)
                     + p_norm_upper ** 2 * dH_upper
                     + p_norm_upper ** 2 * 2 * xi_upper * 2 / p0_lower**3)
    require(deriv_derived < deriv_coeff,
            "derivative perturbation coefficient underivable from ball bounds")

    base_r = Y + Z * radius + C2 * radius**2 + C3 * radius**3 - radius
    base_l = Z + 2 * C2 * radius + 3 * C3 * radius**2
    endpoint_r = base_r + alpha * value_coeff * tau_max
    endpoint_l = base_l + alpha * deriv_coeff * tau_max

    expected = cert["expected_exact_values"]
    require(base_r == decimal(expected["base_radii"]), "base radii value mismatch")
    require(base_l == decimal(expected["base_lipschitz"]), "base derivative value mismatch")
    require(endpoint_r == decimal(expected["endpoint_radii"]), "endpoint radii value mismatch")
    require(endpoint_l == decimal(expected["endpoint_lipschitz"]), "endpoint derivative value mismatch")
    require(endpoint_r < 0, "invariant-ball inequality does not close")
    require(endpoint_l < 1, "contraction inequality does not close")

    return [
        "POSITIVE-FREQUENCY EXTENSION: VERIFIED",
        f"exact p0 = {b.numerator}/{b.denominator}",
        f"alpha coarse bound = {C3 * 96 * Fraction(32) ** 2} < {alpha}",
        f"psi bound = {psi_upper} < 11/10",
        f"conformal square bound = {psi_upper ** 2} < {phi2}",
        f"datum deviation coefficient = {datum_deviation} < 63/100",
        f"value coefficient derivation = {p_norm_upper ** 2 * Fraction(63, 100)} < {value_coeff}",
        f"derivative coefficient derivation = {deriv_derived} < {deriv_coeff}",
        f"base radii = {base_r}",
        f"base Lipschitz = {base_l}",
        f"tau endpoint = {tau_max}",
        f"endpoint radii = {endpoint_r} < 0",
        f"endpoint Lipschitz = {endpoint_l} < 1",
        "fixed-frequency normalization: k = 1",
    ]


def main() -> int:
    try:
        print("\n".join(verify()))
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
