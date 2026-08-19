import Mathlib

/-!
# Exact certificate arithmetic

All constants in this module are exact rational real numbers.  The proofs use
Lean's exact normalization tactics; no floating-point evaluation is
involved.  A successful pinned-toolchain build is the kernel-checking step.
-/

namespace NonScattering
namespace Certificate

noncomputable section

/-- Upstream residual majorant. -/
def Y : ℝ := 159 / 10^12

/-- Upstream derivative-defect majorant. -/
def Z : ℝ := 621 / 1000

/-- Quadratic nonlinear majorant. -/
def C₂ : ℝ := 122

/-- Cubic nonlinear majorant. -/
def C₃ : ℝ := 3 / 250

/-- Certified contraction-ball radius. -/
def radius : ℝ := 1 / 10^6

/-- Conservative norm bound for the preconditioner used by the extension. -/
def alpha : ℝ := 1180

/-- Coefficient in the value perturbation estimate. -/
def valuePerturbation : ℝ := 1906

/-- Coefficient in the derivative perturbation estimate. -/
def derivativePerturbation : ℝ := 3

/-- Uniform squared-wavenumber interval endpoint. -/
def tauMax : ℝ := 1 / 10^13

/-- Original invariant-ball radii expression minus the radius. -/
def baseRadii : ℝ := Y + Z * radius + C₂ * radius ^ 2 + C₃ * radius ^ 3 - radius

/-- Original contraction constant. -/
def baseLipschitz : ℝ := Z + 2 * C₂ * radius + 3 * C₃ * radius ^ 2

/-- Perturbed invariant-ball expression. -/
def perturbedRadii (τ : ℝ) : ℝ :=
  baseRadii + alpha * valuePerturbation * τ

/-- Perturbed contraction bound. -/
def perturbedLipschitz (τ : ℝ) : ℝ :=
  baseLipschitz + alpha * derivativePerturbation * τ

/-- The coarse authenticated cubic constant and `b < 32` imply `alpha < 1180`. -/
theorem alpha_from_coarse_upstream : C₃ * 96 * 32 ^ 2 < alpha := by
  norm_num [C₃, alpha]

/-- Exact value of the upstream radii expression. -/
theorem baseRadii_exact :
    baseRadii = -(378718999999988 : ℝ) / 10^21 := by
  norm_num [baseRadii, Y, Z, C₂, C₃, radius]

/-- Exact value of the upstream contraction bound. -/
theorem baseLipschitz_exact :
    baseLipschitz = (621244000000036 : ℝ) / 10^15 := by
  norm_num [baseLipschitz, Z, C₂, C₃, radius]

/-- Exact endpoint value after the physical perturbation. -/
theorem perturbedRadii_at_tauMax_exact :
    perturbedRadii tauMax = -(153810999999988 : ℝ) / 10^21 := by
  norm_num [perturbedRadii, tauMax, baseRadii, Y, Z, C₂, C₃, radius,
    alpha, valuePerturbation]

/-- Exact endpoint derivative bound after the physical perturbation. -/
theorem perturbedLipschitz_at_tauMax_exact :
    perturbedLipschitz tauMax = (621244000354036 : ℝ) / 10^15 := by
  norm_num [perturbedLipschitz, tauMax, baseLipschitz, Z, C₂, C₃, radius,
    alpha, derivativePerturbation]

/-- The invariant-ball inequality closes uniformly on the certified interval. -/
theorem perturbedRadii_negative
    {τ : ℝ} (_hτ₀ : 0 ≤ τ) (hτ : τ ≤ tauMax) :
    perturbedRadii τ < 0 := by
  have hcoeff : (0 : ℝ) ≤ alpha * valuePerturbation := by
    norm_num [alpha, valuePerturbation]
  have hstep := mul_le_mul_of_nonneg_left hτ hcoeff
  have hend : perturbedRadii tauMax < 0 := by
    rw [perturbedRadii_at_tauMax_exact]
    norm_num
  have hmono : perturbedRadii τ ≤ perturbedRadii tauMax := by
    unfold perturbedRadii
    linarith
  linarith

/-- The contraction inequality closes uniformly on the certified interval. -/
theorem perturbedLipschitz_lt_one
    {τ : ℝ} (_hτ₀ : 0 ≤ τ) (hτ : τ ≤ tauMax) :
    perturbedLipschitz τ < 1 := by
  have hcoeff : (0 : ℝ) ≤ alpha * derivativePerturbation := by
    norm_num [alpha, derivativePerturbation]
  have hstep := mul_le_mul_of_nonneg_left hτ hcoeff
  have hend : perturbedLipschitz tauMax < 1 := by
    rw [perturbedLipschitz_at_tauMax_exact]
    norm_num
  have hmono : perturbedLipschitz τ ≤ perturbedLipschitz tauMax := by
    unfold perturbedLipschitz
    linarith
  linarith

/-- Combined uniform certificate. -/
theorem uniform_extension_certificate
    {τ : ℝ} (hτ₀ : 0 ≤ τ) (hτ : τ ≤ tauMax) :
    perturbedRadii τ < 0 ∧ perturbedLipschitz τ < 1 :=
  ⟨perturbedRadii_negative hτ₀ hτ, perturbedLipschitz_lt_one hτ₀ hτ⟩

/-- The clean value-majorant arithmetic used in the paper. -/
theorem value_majorant_arithmetic :
    (55 : ℝ) ^ 2 * (63 / 100) < valuePerturbation := by
  norm_num [valuePerturbation]

/-- The clean derivative-majorant arithmetic used in the paper. -/
theorem derivative_majorant_arithmetic :
    (110 / 62 : ℝ) * (63 / 100)
      + 3025 / 3000
      + 12100 / (62 * 31 ^ 3) < derivativePerturbation := by
  norm_num [derivativePerturbation]

/-- Positivity of the uniform endpoint. -/
theorem tauMax_pos : 0 < tauMax := by
  norm_num [tauMax]

end

end Certificate
end NonScattering
