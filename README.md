# Exact non-scattering homogeneous dielectrics from Schiffer counterexamples

**Preprint release v1.2.0 - 19 August 2026**

This release accompanies the preprint

> **Exact non-scattering homogeneous dielectrics from Schiffer
> counterexamples** - Mansehej Singh.

The paper proves a family of bounded, simply connected, noncircular,
real-analytic, homogeneous isotropic inclusions that are exactly
non-scattering for the fixed normalized Herglotz wave

```text
v(x) = sqrt(2*pi) J0(|x|),        k = 1.
```

The family is certified for every `0 < tau <= 10^-13`, with

```text
Omega_tau = sqrt(tau) * phi_{p_tau}(unit disk),
q_tau     = p_{tau,0}^2 / tau,
```

and every prescribed contrast `Q >= 1.03 * 10^16` is attained.

## Start here

- `non_scattering_preprint.pdf` - focused research article.
- `non_scattering_verification_supplement.pdf` - certificate, verifier, and replay details.
- `paper/main.tex` and `paper/supplement.tex` - rebuildable LaTeX sources.
- `verification/reproduce.sh` - exact executable checks (offline).
- `verification/fetch_and_check_upstream.sh` - upstream fetch, hash check, and replay.
- `formalization/` - narrow Lean 4/mathlib re-verification of the certificate arithmetic.
- `docs/FORMALIZATION_BOUNDARY.md` - exact formalization boundary.

The main article presents the discovery and mathematical proof.  Operational
provenance, hashes, verifier design, formalization boundaries, and replay
commands are deliberately kept in the separate supplement.

The declaration of computational assistance explicitly credits GPT-5.6 Sol
Pro (OpenAI) for its substantial research, formalization, code, and manuscript
assistance.

## Reproduce

```bash
make verify
make lean
make paper
```

or run everything available on the current machine:

```bash
make all
```

The upstream Colbrook--Stepaniants certificate has been replayed from a
clean Zenodo fetch with every pinned hash verified and every imported value
machine-compared; the successful log is `verification/upstream_check.log`.

## Lean scope

The Lean project is pinned to Lean/mathlib v4.32.1.  It re-verifies the
exact rational certificate arithmetic and states the generic fixed-point and
invertibility lemmas in the form the paper uses.  It does **not** formalize
the operator estimates, the upstream MPFR theorem, or the scattering
analysis; see `formalization/README.md` for the precise scope.  A static
scan finds no proof holes or project-defined axioms.  A pinned-toolchain CI
build remains a pre-publication gate for this release: until it has run,
the sources are not described as kernel-checked.

## Licensing

The proposed release license is CC BY 4.0 for the manuscript and MIT for
software/formalization.  Confirm this choice before depositing publicly; see
`SUBMISSION_CHECKLIST.md`.
