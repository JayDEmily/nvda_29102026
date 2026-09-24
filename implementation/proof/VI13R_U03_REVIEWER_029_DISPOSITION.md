# VI-13R U03 Reviewer 029 disposition

## Binding

- Role: fresh independent Reviewer 029.
- Scope: repaired `IWO-U03 — Raw observation admission, native fidelity and temporal-kind truth` only.
- Frozen repaired candidate: `d25aedeed5de65d0a241bdce6eae22671ef2ddf8`.
- Candidate tree: `21eb6bd2ba53b29ea6d80f90c01af40668f56955`.
- Prior finding under repair: `R028-U03-F001`.
- U04 was not assessed and remains prohibited.

## Disposition

**`FAIL / RETURN_TO_WORKER`**.

`R028-U03-F001` is **CLOSED**. The repaired `array.array` and `range` cases reject changed same-ID
native content and preserve the first admitted record. The complete U03 proof is independently
**47/47** green, including all earlier numeric/NaN/complex/bytes/mapping regressions.

### R029-U03-F001 — same-type native datetime representation collapses

The native comparator still reaches ordinary `left == right` for admitted values not covered by an
explicit exact branch. A bounded public-seam witness uses two aware `datetime` values:

- `2026-09-20T12:00:00+00:00`;
- `2026-09-20T13:00:00+01:00`.

They have the same runtime type and Python equality reports them equal because they represent the
same instant, while their provider-native wall-clock/offset representation differs. Same-ID retry is
therefore accepted instead of rejected. Reviewer 029's external regression fails with
`DID NOT RAISE <class 'ValueError'>`. The original first record remains stored.

`native_record` is `Mapping[str, object]`; the realised contract admits this value family and no
accepted rule excludes it. This defeats BC-005 native-value fidelity and BC-010 / IA17-PROD-008
same-occurrence retry identity for identical content only.

## Smallest bounded repair

The owning layer is the U03 native retry comparator plus bounded U03 proof. Add
representation-sensitive native `datetime` comparison before generic ordinary equality, with a
regression for the verified `12:00+00:00` -> `13:00+01:00` conflict and a positive independently
reconstructed identical-representation datetime case. Preserve all already-closed comparator
behaviour and existing non-native field equality semantics.

Do not add provider validity or duplicate/retransmission equivalence, persistence/replay or U04
behaviour.

U03 is not promotable. U04 remains prohibited pending repair and fresh independent review.
