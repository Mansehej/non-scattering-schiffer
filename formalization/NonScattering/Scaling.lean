import Mathlib

/-!
# Physical scaling and contrast

This module verifies the exact algebraic parameter transformation that turns
the small exterior wavenumber `sqrt τ` into the fixed physical wavenumber one.
-/

namespace NonScattering

/-- Constant relative permittivity after scaling to exterior wavenumber one. -/
def contrast (p₀ τ : ℝ) : ℝ := p₀ ^ 2 / τ

/-- The geometric scale used to normalize the exterior wavenumber. -/
def physicalScale (τ : ℝ) : ℝ := Real.sqrt τ

/-- The scale is positive at positive squared wavenumber. -/
theorem physicalScale_pos {τ : ℝ} (hτ : 0 < τ) : 0 < physicalScale τ := by
  exact Real.sqrt_pos.2 hτ

/-- Squaring the physical scale recovers the original parameter. -/
theorem physicalScale_sq {τ : ℝ} (hτ : 0 ≤ τ) : physicalScale τ ^ 2 = τ := by
  simpa [physicalScale] using Real.sq_sqrt hτ

/-- Dividing the original exterior wavenumber by the geometric scale gives one. -/
theorem normalized_exterior_wavenumber {τ : ℝ} (hτ : 0 < τ) :
    Real.sqrt τ / physicalScale τ = 1 := by
  rw [physicalScale]
  exact div_self (ne_of_gt (Real.sqrt_pos.2 hτ))

/-- The scaled contrast is positive. -/
theorem contrast_pos {p₀ τ : ℝ} (hp₀ : 0 < p₀) (hτ : 0 < τ) :
    0 < contrast p₀ τ := by
  exact div_pos (pow_pos hp₀ 2) hτ

/-- A lower bound on the interior parameter excludes unit contrast throughout the interval. -/
theorem contrast_gt_one_on_certified_interval
    {p₀ τ : ℝ}
    (hp₀ : 31 < p₀) (hτ₀ : 0 < τ) (hτ : τ ≤ 1 / 10^13) :
    1 < contrast p₀ τ := by
  rw [contrast, lt_div_iff₀ hτ₀]
  have hp : 31 ^ 2 < p₀ ^ 2 := by nlinarith
  have htiny : τ < (31 : ℝ) ^ 2 := by
    calc
      τ ≤ 1 / 10^13 := hτ
      _ < (31 : ℝ) ^ 2 := by norm_num
  linarith

/-- In particular, the certified material is not the background medium. -/
theorem contrast_ne_one_on_certified_interval
    {p₀ τ : ℝ}
    (hp₀ : 31 < p₀) (hτ₀ : 0 < τ) (hτ : τ ≤ 1 / 10^13) :
    contrast p₀ τ ≠ 1 :=
  ne_of_gt (contrast_gt_one_on_certified_interval hp₀ hτ₀ hτ)

end NonScattering
