# Review-cycle response

**Status:** `COMPLETE`

**Disposition:** `FAIL / RETURN_TO_WORKER`

Fresh Reviewer 029 independently reviewed exact repaired IWO-U03 candidate
`d25aedeed5de65d0a241bdce6eae22671ef2ddf8` / tree
`21eb6bd2ba53b29ea6d80f90c01af40668f56955`.

`R028-U03-F001` is **CLOSED**. The required same-ID `array('b',[1])` -> `array('B',[1])` and
`range(0,3,2)` -> `range(0,4,2)` conflicts reject, the first admitted record remains intact, and the
complete U03 proof is **47/47** green including all earlier exactness regressions.

Reviewer 029 found one new concrete U03 defect:

- **`R029-U03-F001` — same-type native `datetime` representation is collapsed by ordinary instant
  equality.** A first native value `2026-09-20T12:00:00+00:00` followed by a same-ID retry
  `2026-09-20T13:00:00+01:00` is accepted as idempotent even though the provider-native wall-clock
  and offset representation changed. An external public-seam canary fails with
  `DID NOT RAISE <class 'ValueError'>`. The first record remains stored, but the conflicting retry is
  not rejected.

This defeats BC-005 unchanged native-value fidelity and BC-010 / IA17-PROD-008 same-occurrence
idempotency for identical content only. The owning layer is the U03 native retry comparator plus
bounded U03 proof.

**Smallest bounded repair:** add representation-sensitive native `datetime` comparison before the
generic ordinary-equality fallback; prove the verified `12:00+00:00` -> `13:00+01:00` witness
rejects without replacing the first record; retain an identical-datetime positive idempotency case;
and preserve all already-closed comparator and non-native equality behaviour.

U03 is not promotable. U04 remains prohibited pending the bounded repair and fresh independent
review.
