import Mathlib

/-!
# Algebraic regularity transfer

The upstream proof constructs an invertible preconditioner `A` and proves
that the preconditioned derivative `A ∘ B` is invertible.  The elementary
lemma below verifies that this implies invertibility of `B` itself.
-/

namespace NonScattering

open Function

/-- If `A` and `A ∘ B` are bijective, then `B` is bijective. -/
theorem bijective_right_of_bijective_comp
    {X Y : Type*} {A : Y → X} {B : X → Y}
    (hA : Bijective A) (hAB : Bijective (A ∘ B)) : Bijective B := by
  constructor
  · intro x₁ x₂ hB
    apply hAB.1
    simp only [Function.comp_apply, hB]
  · intro y
    obtain ⟨x, hx⟩ := hAB.2 (A y)
    refine ⟨x, hA.1 ?_⟩
    simpa [Function.comp_apply] using hx

end NonScattering
