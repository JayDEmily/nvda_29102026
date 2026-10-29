# Review-cycle response

**Status:** `COMPLETE`

**Disposition:** `FAIL / RETURN_TO_WORKER`

Fresh Reviewer 027 independently reviewed only repaired IWO-U03 candidate
`758060930b015c23bf63a5de4d71c4d318760393` / tree
`b819ffa1795e97e40374a59cedd42834233d2225`.

The concrete Reviewer-026 failures are closed. Separately reconstructed same-ID native
`float("nan")` and `Decimal("NaN")` values are idempotent; a same-ID
`complex(-0.0, 0.0)` -> `complex(0.0, 0.0)` retry is rejected without replacing the original
record. The earlier int/float and Decimal-scale conflicts also remain rejected, and the candidate
keeps ordinary equality for the non-native observation fields. Exact pinned validation is green:
Reviewer-026 regressions **3/3**, U01+U02+U03 **371/371**, source mypy, Ruff, product proof,
architecture, dependency/public-seam, architecture/bootstrap **74/74**, promotion **74/74** and
Git integrity all pass.

The bounded realised-U03 challenge nevertheless finds one material remaining exact-content defect:

- `R027-U03-F001`: the native comparator still falls back to Python equality for admitted
  non-numeric native values and uses ordinary set/key equality for nested mappings. Consequently,
  distinct admitted native content can collapse to the same retry identity. A same-ID retry from
  `bytes(b"abc")` to `bytearray(b"abc")` is accepted as idempotent, and a nested native mapping
  changing key `1` to `1.0` is likewise accepted. In both canaries the original record remains
  stored, but the conflicting retry is not rejected.

These values reach the current public admission surface: `native_record` remains
`Mapping[str, object]`, the snapshot restricts only top-level field-name keys to exact `str`, and no
accepted provider-validity rule excludes either witness. BC-009 also prevents this review from
inventing such a provider rule. The defect therefore defeats BC-005 exact native-value preservation,
BC-009 conflicting-payload rejection, BC-010 same-occurrence idempotency for identical content only,
and the IWO-U03 retry/fidelity law.

**Smallest owning-layer repair:** U03 M-owner native retry comparison plus bounded U03 regression
proof. Make native comparison exact/runtime-type-sensitive across the values the public U03 surface
admits, including nested mapping keys, while retaining the specialised reflexive NaN handling and
preserving existing non-native field equality semantics. Add focused regressions for the two
Reviewer-027 witnesses. Do not add provider validity/duplicate semantics, U04 behaviour,
persistence, replay or downstream capability.

U03 is not promotable. U04 remains prohibited pending the bounded repair and a fresh independent U03
re-review.
