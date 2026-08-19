# Lean 4 certificate-arithmetic project

This Lake project is pinned to Lean/mathlib `v4.32.1`.  Its scope is
deliberately narrow and is stated precisely below; the project has not yet
been kernel-checked, and no claim beyond "source scan" is made until the
pinned-toolchain CI build has succeeded and its log has been archived.

## What the sources state and prove

1. `Certificate.lean` - every exact rational identity and inequality in the
   positive-frequency extension certificate: the base radii and Lipschitz
   values, the endpoint values at `tau = 10^-13`, uniform closure over
   `0 <= tau <= 10^-13`, the `C3 <= 0.012, b < 32 => alpha < 1180`
   implication, and the two scalar majorant inequalities
   `55^2 * 63/100 < 1906` and `110/62 * 63/100 + 3025/3000
   + 12100/(62*31^3) < 3`.
2. `FixedPoint.lean` - existence and uniqueness of the fixed point of a
   strict contraction on a nonempty complete metric space, and the standard
   stability estimate for fixed points of two nearby contractions.
3. `LinearRegularity.lean` - if `A` and `A o B` are bijective then `B` is
   bijective.
4. `Scaling.lean` - the scalar contrast computation `q = p0^2/tau`, its
   positivity, and `q > 1` on the certified interval.

## What is deliberately not in Lean

- The upstream degree-301 Schiffer certificate (a separately authenticated
  MPFR computer-assisted theorem; pinned and replayed in `verification/`).
- The operator-level perturbation estimates behind the constants `1906` and
  `3`, including the weighted-algebra norm bounds of Section 4 of the paper.
- All planar scattering analysis: the Bessel `J0` Herglotz integral,
  conformal covariance of the Laplacian and normal traces, analytic Jordan
  boundary theory, and radiating exterior uniqueness.
- Any instantiation connecting the generic fixed-point theorems to the
  concrete coefficient spaces; that connection is made in the paper.

Accordingly, the accurate description is **a Lean re-verification of the
exact rational certificate arithmetic, together with generic fixed-point and
invertibility lemmas stated in the form the paper uses**.  It is not a
formalization of the non-scattering theorem.

## Build

```bash
python3 scripts/check_no_holes.py
lake update
lake build
```

`scripts/check_no_holes.py` scans only the project sources
(`NonScattering.lean` and `NonScattering/`), rejecting `sorry`, `admit`,
`axiom`, `native_decide`, `opaque`, `unsafe`, `partial`,
`implemented_by`, `extern`, `initialize`, and `run_cmd`.
`NonScattering/MainTheorem.lean` runs `#print axioms` on the public
theorems; archive that output together with the CI build log before any
public claim that the files are kernel-checked.
