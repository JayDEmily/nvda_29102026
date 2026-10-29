# Review-cycle response

**Status:** `COMPLETE`

**Disposition:** `FAIL / RETURN_TO_WORKER`

Fresh Reviewer 028 independently reviewed only repaired IWO-U03 candidate
`06735b3682d79387ebaa4da70002e6685d52740a` / tree
`b73b6ba4486eba9ae3aa4c1facc626579c8b8ee5`.

The two concrete Reviewer-027 regressions are closed: same-ID native `bytes` -> `bytearray` and
nested mapping-key `int(1)` -> `float(1.0)` changes now reject without replacing the first admitted
record. Earlier int/float, Decimal-scale, reconstructed NaN-idempotency and complex signed-zero
behaviours also remain closed. Exact pinned validation is green: Reviewer-027 regressions **2/2**,
U01+U02+U03 **373/373**, source mypy, Ruff, product proof, architecture,
dependency/public-seam, architecture/bootstrap **74/74**, promotion **74/74** and Git integrity all
pass.

`R027-U03-F001` is nevertheless **not fully closed** because the active Reviewer-028 acceptance
condition requires native retry equality to remain exact/runtime-type-sensitive through admitted
standard sequence values rather than falling back to Python equality where it collapses
representation. The repaired comparator recursively handles only `list`/`tuple` sequences and then
returns ordinary `left == right` for other admitted values.

A bounded public-seam challenge proves one remaining root defect:

- `R028-U03-F001`: a same-ID retry from `array('b', [1])` to `array('B', [1])` is accepted as
  idempotent despite a changed standard-library sequence representation (`typecode`); and a same-ID
  retry from `range(0, 3, 2)` to `range(0, 4, 2)` is also accepted despite changed range bounds. Both
  pairs have the same runtime type and ordinary Python equality returns true, so the generic fallback
  collapses the changed native content. In each canary the first record remains stored, but the
  conflicting retry is not rejected.

Both witnesses pass through the current public U03 admission seam. `native_record` remains
`Mapping[str, object]`, neither accepted authority nor the realised contract excludes these values,
and BC-009 prevents this review from inventing provider-validity rules to exclude them. This defeats
BC-005 exact native-value fidelity, BC-009 conflicting-payload rejection, BC-010 same-occurrence
idempotency for identical content only, and the IWO-U03 native-fidelity/retry law.

**Smallest owning-layer repair:** U03 M-owner native retry comparison plus bounded
implementation-coupled U03 proof. Remove the remaining ordinary-equality collapse for admitted
standard sequence values, preserving representation-bearing state needed for exact content (the two
verified witnesses are `array.array` typecode and `range` start/stop/step), while preserving all
already-closed comparator behaviour and existing non-native field equality semantics. Add focused
regressions for the two Reviewer-028 witnesses. Do not invent provider validity/duplicate semantics,
implement U04, add persistence/replay or activate downstream capability.

U03 is not promotable. U04 remains prohibited pending the bounded repair and a fresh independent U03
re-review.
