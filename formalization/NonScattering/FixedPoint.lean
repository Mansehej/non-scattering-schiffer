import Mathlib

/-!
# Fixed-point layer

This module packages the Banach fixed-point theorem in the exact uniqueness
form used by the paper and proves the basic perturbation estimate for two
fixed points.
-/

namespace NonScattering

open Function
open scoped NNReal

/-- Stability estimate for fixed points of a uniformly contracting family. -/
theorem dist_fixedPoints_le
    {α : Type*} [PseudoMetricSpace α]
    {T S : α → α} {x y : α} {κ ε : ℝ}
    (hκ : κ < 1)
    (hcontract : ∀ a b, dist (T a) (T b) ≤ κ * dist a b)
    (hx : IsFixedPt T x) (hy : IsFixedPt S y)
    (hperturb : dist (T y) (S y) ≤ ε) :
    dist x y ≤ ε / (1 - κ) := by
  have hden : 0 < 1 - κ := sub_pos.mpr hκ
  have hmain : dist x y ≤ κ * dist x y + ε := by
    calc
      dist x y = dist (T x) (S y) := by rw [hx.eq, hy.eq]
      _ ≤ dist (T x) (T y) + dist (T y) (S y) := dist_triangle _ _ _
      _ ≤ κ * dist x y + ε := add_le_add (hcontract x y) hperturb
  apply (le_div_iff₀ hden).2
  have hd : (0 : ℝ) ≤ dist x y := dist_nonneg
  nlinarith

/-- Two fixed points of the same strict contraction coincide. -/
theorem fixedPoint_unique_of_real_contraction
    {α : Type*} [MetricSpace α]
    {T : α → α} {x y : α} {κ : ℝ}
    (hκ : κ < 1)
    (hcontract : ∀ a b, dist (T a) (T b) ≤ κ * dist a b)
    (hx : IsFixedPt T x) (hy : IsFixedPt T y) : x = y := by
  have hzero : dist x y ≤ 0 := by
    simpa using (dist_fixedPoints_le hκ hcontract hx hy (show dist (T y) (T y) ≤ 0 by simp))
  exact dist_eq_zero.mp (le_antisymm hzero dist_nonneg)

/-- A contraction on a nonempty complete metric space has exactly one fixed point. -/
theorem contracting_existsUnique_fixedPoint
    {α : Type*} [MetricSpace α] [CompleteSpace α] [Nonempty α]
    {K : ℝ≥0} {T : α → α} (hT : ContractingWith K T) :
    ∃! x : α, IsFixedPt T x := by
  obtain ⟨x, hx, -, -⟩ := hT.exists_fixedPoint (Classical.arbitrary α) (edist_ne_top _ _)
  have hκ : (K : ℝ) < 1 := by exact_mod_cast hT.1
  exact ⟨x, hx, fun y hy =>
    fixedPoint_unique_of_real_contraction hκ (fun a b => hT.2.dist_le_mul a b) hy hx⟩

end NonScattering
