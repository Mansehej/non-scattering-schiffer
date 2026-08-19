# Verification supplement

`extension_certificate.json` is the authoritative scalar certificate.
`upstream_snapshot.json` pins the theorem-level numerical and geometric
outputs imported from Colbrook--Stepaniants, and `upstream.lock` pins the
repository commit, the Zenodo archive digest, and the SHA-256 hashes of the
upstream center, inverse, certificate, and source manifest.

Run:

```bash
./reproduce.sh
```

The Python checker uses exact `Fraction` arithmetic and explicit fail-closed
checks.  Beyond replaying the endpoint inequalities, it rederives the
perturbation constants (11/10, 5/4, 63/100, 1/7000, 1/3000, 1906, 3) from
the certified ball bounds and cross-checks the snapshot against the lock
file.  It is run both normally and with Python optimization enabled, and the
outputs must be byte-identical.  The Node checker is an independently coded
BigInt rational implementation replaying the complete check set.
`adversarial_tests.py` exercises thirteen corruptions against both
checkers.

`fetch_and_check_upstream.sh` downloads the archived upstream release from
Zenodo, verifies the archive digest and all four pinned hashes, replays the
upstream authenticated checker, and runs `cross_check_upstream.py`, which
machine-compares every imported value and rederives the ball bounds
`31 < p0 < 32` and `||p|| < 55` from the exact center coefficients.  The
successful clean-fetch run is recorded in `upstream_check.log`.

The Lean project re-verifies the exact rational certificate arithmetic; a
clean pinned-toolchain build is a pre-publication gate.  Neither scalar
checker regenerates the upstream 2,471-dimensional MPFR audit.  That
upstream proof remains a pinned external theorem dependency, exactly as
stated in the manuscript and formalization boundary document.
