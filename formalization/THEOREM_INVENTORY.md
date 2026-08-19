# Lean theorem inventory

## Exact certificate arithmetic (`Certificate.lean`)

- `Certificate.alpha_from_coarse_upstream`
- `Certificate.baseRadii_exact`
- `Certificate.baseLipschitz_exact`
- `Certificate.perturbedRadii_at_tauMax_exact`
- `Certificate.perturbedLipschitz_at_tauMax_exact`
- `Certificate.perturbedRadii_negative`
- `Certificate.perturbedLipschitz_lt_one`
- `Certificate.uniform_extension_certificate`
- `Certificate.value_majorant_arithmetic`
- `Certificate.derivative_majorant_arithmetic`
- `Certificate.tauMax_pos`

## Generic fixed-point lemmas (`FixedPoint.lean`)

- `dist_fixedPoints_le`
- `fixedPoint_unique_of_real_contraction`
- `contracting_existsUnique_fixedPoint`

## Algebraic invertibility transfer (`LinearRegularity.lean`)

- `bijective_right_of_bijective_comp`

## Scalar contrast computation (`Scaling.lean`)

- `physicalScale_pos`
- `physicalScale_sq`
- `normalized_exterior_wavenumber`
- `contrast_pos`
- `contrast_gt_one_on_certified_interval`
- `contrast_ne_one_on_certified_interval`

## Collected corollaries (`MainTheorem.lean`)

- `quantitative_continuation_layer`
- `physical_material_layer`

The generic lemmas are stated in exactly the form the paper invokes but are
not instantiated on the concrete coefficient spaces; that instantiation, the
operator-level perturbation estimates, and all scattering analysis live in
the paper.  `MainTheorem.lean` runs `#print axioms` on the public theorems.
Any foundational entries reported there must come from Lean/mathlib's
standard classical infrastructure; the source scan rejects project-defined
axioms.  The pinned-toolchain build has been completed and the axiom report
shows only `propext`, `Classical.choice`, and `Quot.sound` (and `propext`
alone for `bijective_right_of_bijective_comp`); see
`../verification/lean_kernel_build_v1.2.1.log`.
