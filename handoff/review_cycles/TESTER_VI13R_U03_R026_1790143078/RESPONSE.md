# Review-cycle response

**Status:** `COMPLETE`

**Disposition:** `FAIL / RETURN_TO_WORKER`

Fresh Reviewer 026 independently reviewed only repaired IWO-U03 candidate
`6316735eb22bdbe243b02637f09376bf1200e43d` / tree
`a9cc881f50b7a6adf021ce80fce52a330e9d203d`.

The two concrete Reviewer-025 escapes are repaired: same-ID `int(1)` to `float(1.0)` and
`Decimal("1.0")` to `Decimal("1.00")` retries are rejected, the first admitted record remains
unchanged, and the bounded U01+U02+U03 suite is independently green at **368/368** under the exact
pinned Python/pytest toolchain. Static/Ruff/product/architecture/dependency/public-seam controls are
also independently green. Those results do not close `R025-U03-F001` completely.

Two concrete public-seam canaries defeat the required exact retry law for native numeric values that
the current U03 contract admits:

- `R026-U03-F001`: a separately reconstructed same-ID payload containing `float("nan")` is rejected
  as conflicting even when reconstructed with the same native value. `Decimal("NaN")` shows the
  same false-conflict behaviour. The outer ordinary dataclass equality check is non-reflexive for
  these admitted NaN values, so the fidelity-aware native comparator is never allowed to establish
  identical content.
- `R026-U03-F002`: a same-ID retry changing native `complex(-0.0, 0.0)` to
  `complex(0.0, 0.0)` is accepted as idempotent even though the stored native representation changes
  in a fidelity-bearing signed-zero component. The complex branch falls back to ordinary `==`,
  which collapses that distinction.

The current public contract types `native_record` as `Mapping[str, object]` and the production
snapshot validates field-name type but does not exclude these values. Accepted BC-009 also forbids
this review from inventing provider bad-tick/validity rules to exclude them. The failures therefore
occur on the realised public admission path, not in a hypothetical provider-equivalence model.

Together these failures defeat BC-005 exact native-value preservation, BC-009 conflicting-payload
rejection without replacement, BC-010 same-occurrence idempotency for identical content only, and
the IWO-U03 same-occurrence retry law. `R025-U03-F001` is therefore **not fully closed**.

**Smallest owning-layer repair:** U03 M-owner retry comparison plus bounded U03 regression proof.
Do not use ordinary full-observation equality as a prerequisite for native-record exactness; compare
non-native observation content without letting native non-reflexive equality decide the result, and
make the admitted native numeric comparator preserve the distinctions it claims while remaining
idempotent for separately reconstructed identical values. Add focused regressions for the two
Reviewer-026 escapes. Do not add provider validity/duplicate semantics, U04 behaviour, persistence,
replay or downstream capability.

U03 is not promotable. U04 remains prohibited pending the bounded repair and a fresh independent
U03 re-review.
