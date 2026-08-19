# Formalization boundary

The release distinguishes three layers.

## Re-verified in the Lean sources

- exact rational certificate arithmetic: the base radii and Lipschitz
  values, the endpoint values, and uniform closure for `0 <= tau <= 10^-13`;
- the `alpha < 1180` hardening from `C3 <= 0.012` and `b < 32`;
- the terminal scalar majorant inequalities `55^2 * 63/100 < 1906` and the
  three-term derivative sum below `3`;
- Banach fixed-point existence/uniqueness and the fixed-point stability
  bound, stated generically on complete metric spaces;
- invertibility transfer through an invertible preconditioner (as a
  statement about bijections);
- the scalar contrast computation: positivity and exclusion of `q = 1`.

The generic lemmas are stated in the form the paper uses but are not
instantiated on the concrete coefficient spaces.  The Lean development is a
third independent checker of the scalar arithmetic, not a formalization of
the non-scattering theorem.  The sources are kernel-checked: the pinned
Lean/mathlib v4.32.1 build succeeds with zero warnings and the
`#print axioms` report shows only standard classical axioms
(`verification/lean_kernel_build_v1.2.1.log`).

## Imported theorem dependency

The degree-301 Schiffer counterexample, its exact zero, the weighted Banach
algebra bounds, preconditioner invertibility, analytic geometry, and infinite
tails are supplied by the authenticated Colbrook--Stepaniants certificate.
The release pins the Zenodo archive digest and four file hashes, replays the
upstream authenticated checker, machine-compares every imported value, and
rederives the ball bounds from the exact center
(`verification/upstream_check.log`).  Reimplementing the entire MPFR audit
in Lean is a separate formal-verification project.

## Standard analysis proved in the paper only

The construction also invokes the Bessel `J0` plane-wave integral, conformal
covariance of the planar Laplacian and normal traces, the weighted-algebra
operator estimates behind the constants `1906` and `3`, and uniqueness for
the direct transmission problem.  These are proved or cited in the paper and
are entirely outside the Lean sources; no Lean structure claims to state
them.

The release therefore uses the precise phrase:

> A kernel-checked Lean re-verification of the exact rational certificate
> arithmetic, together with generic fixed-point and invertibility lemmas
> in the form used by the paper.

It does not claim a formalization of the non-scattering theorem, of the
upstream MPFR proof, or of planar scattering theory.
