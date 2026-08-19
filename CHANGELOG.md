# Changelog

## v1.2.0 - 2026-08-19

- Expanded the bibliography from 4 to 20 references covering the corner
  scattering, non-scattering regularity, transmission eigenvalue, and
  Pompeiu/Schiffer literature, and added a citation for the archived
  upstream validation certificate (Zenodo DOI 10.5281/zenodo.21765287).
- Added a figure of the certified domain computed from the exact upstream
  center coefficients.
- Stated the imported algebra conventions as an explicit lemma (angular-only
  weights; multiplication by |z|^2 is a nonexpansive radial shift) with
  pinpoint citations to the upstream validation specification, closing the
  main unstated step behind the bound |||phi|^2|| < 5/4.
- Defined R_0 and L_0 in the main article via the cubic Taylor majorants
  (Y, Z, C2, C3) instead of quoting them as opaque constants.
- Renamed the seed zero to (gamma_*, p_*), removing the notation clash with
  the constant coefficient p_0.
- Added the ten-fold-symmetry argument that non-affine implies non-disc, a
  direct-problem uniqueness citation, and an epistemic-status remark making
  the dependence on the Colbrook--Stepaniants preprint explicit.
- Tightened the certified p0 interval to (31,32); the prescribed-contrast
  corollary now covers every Q >= 1.03 * 10^16.
- Verifiers now rederive the perturbation constants (11/10, 5/4, 63/100,
  1/7000, 1/3000, 1906, 3) from the certified ball bounds in exact
  rationals; the Node checker replays the complete check set; the
  adversarial suite grew to thirteen corruptions exercised against both
  verifiers.
- Replaced the failed upstream check log with a successful clean replay:
  Zenodo archive fetched and digest-verified, all four pinned SHA-256
  hashes checked (the certificate and source-manifest hashes are now
  actually verified), every imported value machine-compared, and the ball
  bounds 31 < p0 < 32 and ||p|| < 55 rederived from the exact center.
- Clarified `upstream.lock`: `source_sha256` pinned the upstream source
  manifest, not `certificate.json`; both files now have separate, labelled,
  verified entries.
- Rescoped the Lean project to what it actually contains: removed the
  tautological exterior-zero module, the unused transmission-interface
  structure, and the unused implicit-function wrapper; hardened the
  remaining proofs; extended the source scan to further escape hatches;
  fixed the CI workflow package path.  All Lean claims across the release
  now read "re-verification of the certificate arithmetic", and
  kernel-checking remains an explicitly open gate.

## v1.1.1 - 2026-08-19

- Revised the declaration of computational assistance to explicitly and
  gratefully credit GPT-5.6 Sol Pro (OpenAI) for its substantial role in
  theorem exploration, literature synthesis, symbolic and numerical checks,
  code and Lean-formalization generation, and manuscript drafting and editing.
- No mathematical statement, proof, certificate, or numerical bound changed.

## v1.1.0 - 2026-08-18

- Rewrote the manuscript as a conventional research article centered on the
  new mathematical result and its proof.
- Replaced the defensive abstract and early scope audit with a direct
  statement of the affirmative existence theorem.
- Promoted the regular-Schiffer-zero continuation mechanism as the central
  discovery.
- Condensed the imported computer-assisted theorem to the precise estimates
  used in the proof.
- Moved hashes, replay commands, verifier architecture, exact rational
  expansions, dependency ledgers, and the detailed Lean boundary into a
  separate verification supplement.
- Reduced the main article to eight focused pages while retaining the full
  mathematical construction, quantitative continuation, physical scaling,
  trace matching, and prescribed-contrast corollary.
- Removed the stale Yuzu repository reference from citation metadata.

## v1.0.0 - 2026-08-18

- Reframed the construction at fixed exterior wavenumber `k = 1`.
- Promoted the regular-zero continuation principle to the conceptual main
  theorem and retained the radii calculation as a quantitative corollary.
- Added the certified interval `0 < tau <= 10^-13` and prescribed-contrast
  corollary.
- Replaced the reconstructed preconditioner norm with the authenticated
  coarse derivation `alpha < 1180`.
- Added exact-rational Python and Node checks and a Lean 4 formalization of
  the new deduction layer.
