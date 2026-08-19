import NonScattering.Certificate
import NonScattering.FixedPoint
import NonScattering.LinearRegularity
import NonScattering.Scaling

/-!
# Collected certificate-layer theorems

This file collects the theorems intended for kernel checking with the pinned
Lean toolchain.  The scope is deliberately narrow: exact rational certificate
arithmetic, generic fixed-point facts, an algebraic invertibility transfer,
and the scalar contrast computation.  The operator-level estimates, the
upstream Schiffer certificate, and the scattering analysis are proved in the
paper, not here.
-/

namespace NonScattering

/-- The exact quantitative continuation inequalities hold on the entire interval. -/
theorem quantitative_continuation_layer
    {τ : ℝ} (hτ₀ : 0 ≤ τ) (hτ : τ ≤ Certificate.tauMax) :
    Certificate.perturbedRadii τ < 0 ∧
    Certificate.perturbedLipschitz τ < 1 :=
  Certificate.uniform_extension_certificate hτ₀ hτ

/-- At every positive certified parameter, the fixed-frequency contrast is positive and nonunit. -/
theorem physical_material_layer
    {p₀ τ : ℝ} (hp₀ : 31 < p₀)
    (hτ₀ : 0 < τ) (hτ : τ ≤ Certificate.tauMax) :
    0 < contrast p₀ τ ∧ contrast p₀ τ ≠ 1 := by
  have hτ' : τ ≤ 1 / 10^13 := by simpa [Certificate.tauMax] using hτ
  exact ⟨contrast_pos (by linarith) hτ₀,
    contrast_ne_one_on_certified_interval hp₀ hτ₀ hτ'⟩

end NonScattering

#print axioms NonScattering.Certificate.uniform_extension_certificate
#print axioms NonScattering.contracting_existsUnique_fixedPoint
#print axioms NonScattering.dist_fixedPoints_le
#print axioms NonScattering.bijective_right_of_bijective_comp
#print axioms NonScattering.quantitative_continuation_layer
#print axioms NonScattering.physical_material_layer
