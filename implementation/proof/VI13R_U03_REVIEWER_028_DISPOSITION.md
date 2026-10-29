# VI-13R U03 Reviewer 028 disposition

## Binding

- Role: fresh independent Reviewer 028.
- Scope: repaired `IWO-U03 — Raw observation admission, native fidelity and temporal-kind truth` only.
- Frozen repaired candidate: `06735b3682d79387ebaa4da70002e6685d52740a`.
- Candidate tree: `b73b6ba4486eba9ae3aa4c1facc626579c8b8ee5`.
- Prior finding under repair: `R027-U03-F001`.
- U04 was not assessed and remains prohibited.

## Disposition

**`FAIL / RETURN_TO_WORKER`**.

The two concrete Reviewer-027 escapes are **closed**. Same-ID `bytes` -> `bytearray` and nested
mapping-key `int(1)` -> `float(1.0)` changes reject without replacing the original record. Earlier
numeric/NaN/complex comparator regressions remain closed. Exact pinned U01+U02+U03 proof is
independently **373/373** and current mypy/Ruff/product/architecture/dependency/public-seam controls
are green.

`R027-U03-F001` is nevertheless **not fully closed**. Its repair request and the active Reviewer-028
request require exact/runtime-type-sensitive native retry equality through admitted standard
sequence values rather than ordinary Python equality where that equality collapses representation.
The realised comparator handles `list`/`tuple` explicitly but still falls back to `left == right` for
other admitted same-type values.

### R028-U03-F001 — same-type standard sequence representation still collapses

Two bounded public-seam canaries expose the same remaining comparator defect:

1. same-ID native `array('b', [1])` -> `array('B', [1])` is accepted as idempotent even though the
   standard-library sequence's representation-bearing `typecode` changes;
2. same-ID native `range(0, 3, 2)` -> `range(0, 4, 2)` is accepted as idempotent even though the
   native range bound changes.

Both pairs have the same runtime type. Python ordinary equality returns true for each pair, so the
candidate's generic fallback collapses the changed content. The original first record remains stored,
but the conflicting retry is not rejected.

These are realised public-seam inputs. `native_record` remains `Mapping[str, object]`; both witness
families are admitted by the current contract and no accepted provider-validity rule excludes them.
BC-009 also prevents this review from inventing such a restriction.

This defeats BC-005 exact native-value fidelity, BC-009 conflicting-payload rejection, BC-010
idempotency only for identical same-occurrence content, the IWO-U03 native-fidelity/retry law and the
active Reviewer-028 standard-sequence exactness condition.

## Smallest bounded repair

The owning layer is the U03 M-owner native retry comparator plus bounded implementation-coupled U03
proof. Remove the remaining ordinary-equality collapse for admitted standard sequence values while
preserving representation-bearing state required for exact retry identity. The verified witnesses
require exact treatment of `array.array` typecode/content and `range` start/stop/step. Retain all
already-closed Decimal/float/complex/mapping/list/tuple/set/frozenset behaviour and existing
non-native field equality semantics. Add focused regressions for only the two Reviewer-028 witnesses.

Do not add provider validity, duplicate/retransmission equivalence, U04 behaviour, persistence,
replay or downstream capability.

U03 is not promotable. U04 remains prohibited pending a repaired candidate and fresh independent U03
review.
