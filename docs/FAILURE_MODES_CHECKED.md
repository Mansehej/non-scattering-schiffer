# Failure modes checked

## Mathematical failure modes checked

- The Schiffer eigenvalue is not used as the exterior wavenumber.
- `q = p0^2/tau`, not `p0`, `sqrt(tau)`, or their inverse.
- The constant datum appears only at `tau = 0`.
- The Herglotz density is nonzero and exactly normalized.
- The domain is scaled together with the fields when fixing `k = 1`.
- Conformal normal derivatives acquire a factor, but the correction trace is
  exactly zero before scaling.
- The perturbation equation reduces literally to the upstream equation at
  `tau = 0`.
- The complete Bessel series is majorized; no omitted tail is ignored.
- The bound `|||phi|^2|| <= ||psi||^2` is justified by the upstream
  angular-only weight convention, stated as an explicit lemma with pinpoint
  citations; it is not an unexamined submultiplicativity step.
- The same upstream coefficient ball is invariant for the whole interval.
- The geometry theorem is imported on that whole ball, not inferred from a
  numerical plot, and the non-affine-implies-non-disc step is written out
  via the ten-fold symmetry.
- The prescribed-contrast corollary uses continuity and the intermediate
  value theorem, not an unproved monotonicity claim.
- Uniqueness of the direct transmission problem is cited, so the exhibited
  zero scattered field is the physical scattered field.

## Executable fail-closed tests

`verification/adversarial_tests.py` corrupts, one at a time:

- the preconditioner bound;
- the value-perturbation constant;
- the conformal-square majorant `5/4`;
- the parameter endpoint;
- a stored exact decimal expansion;
- the upstream `Y`, `Z`, and `C3` majorants;
- the certified shape-norm ball bound `55`;
- the exact hexadecimal center coefficient;
- a pinned hash (snapshot/lock disagreement);
- the presence of the snapshot and lock files.

Each corruption must be rejected by the Python checker and, when Node is
available, by the independent BigInt checker.  The suite also requires
byte-identical Python output with and without interpreter optimization.
`formalization/scripts/check_no_holes.py` rejects proof holes,
project-defined axioms, and further escape hatches (`native_decide`,
`opaque`, `unsafe`, `partial`, `implemented_by`, `extern`) in the Lean
project sources.

## Formalization wording audit

The release never uses "formalized" for the scattering content.  The
accurate claim, used everywhere, is a Lean **re-verification of the exact
rational certificate arithmetic** plus generic fixed-point lemmas.  The
upstream MPFR theorem and the standard PDE/Bessel analysis are listed
separately in every public-facing description, and kernel-checking is an
explicitly open gate.
