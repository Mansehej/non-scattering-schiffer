# Convention and specification audit

Timestamp: 18 August 2026 (Europe/London)

## Frozen distinctions

1. **Schiffer datum versus physical incident field.**  The upstream boundary
   value `1` is used only at the auxiliary parameter `tau = 0`.  The final
   exterior incident field is `sqrt(2*pi) J0(|x|)` at wavenumber `k = 1`.
2. **Transmission eigenpair versus non-scattering field.**  The incident
   component is explicitly represented by a normalized `L2` Herglotz
   density.  The exterior total field equals that entire incident field.
3. **Entire Helmholtz versus Herglotz.**  The construction meets the stronger
   Herglotz requirement with constant density `1/sqrt(2*pi)`.
4. **Constant material.**  The physical coefficient is the single positive
   scalar `q_tau = p_tau,0^2/tau`.  The variable coefficient in fixed-disc
   coordinates is solely a conformal pullback.
5. **Exact versus approximate scattering.**  Both Cauchy traces match exactly;
   the exterior scattered field is the literal zero function.
6. **Two-dimensional scalar Maxwell reduction.**  No claim is made for the
   full three-dimensional vector Maxwell system.
7. **Noncircularity.**  The fixed point remains in the upstream ball where the
   first nonconstant shape coefficient is bounded away from zero.
8. **Frequency parameters.**  `tau` is the exterior squared wavenumber before
   scaling.  `p_tau,0^2` is the interior squared wavenumber before scaling.
   Their ratio is the physical contrast.  They are never identified.
9. **Normal orientation and scaling.**  The correction `K gamma` has zero
   normal trace, so conformal and dilation factors cannot change the zero.
10. **Infinite series.**  `J0` is handled by its complete power series with a
    geometric majorant.  No finite Bessel truncation defines the construction.

## Physical normalization

The paper uses arc-length measure on `S^1`:

```text
v(x) = integral_{S^1} exp(i x.d) h(d) ds(d),
h(d) = 1/sqrt(2*pi),
||h||_2 = 1.
```

This gives `v(x) = sqrt(2*pi) J0(|x|)`.
