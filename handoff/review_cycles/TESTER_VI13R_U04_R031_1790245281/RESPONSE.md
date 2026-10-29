# Review-cycle response

**Status:** `COMPLETE`

**Disposition:** `FAIL / RETURN_TO_WORKER`

Reviewer 031 independently reviewed exact IWO-U04 candidate
`e7eb44119bdf7fb22abacae8291788619792c96a` / tree
`ea104900fcaf8e2db4177df3909956f464d6a918`.

The bounded U04 proof remains green on the exact candidate, but one implementation-coupled material
escape is established:

- **`R031-U04-F001` — assessment evidence visibility incorrectly depends on optional relation
  materialisation and uses receipt time as the visibility discriminator.** BC-007 explicitly makes
  `CaptureReceiptEvidenceRelation.v1` materialisation optional, while BC-008 requires assessment
  outcome to be derived from eligible committed raw-observation evidence visible to the assessment's
  own transaction. On the candidate, an admitted in-slot observation plus an eligibility authority
  that returns `True` yields `zero_received` when the caller does not first invoke
  `derive_capture_receipt_evidence_relation`; the eligibility authority is never consulted. A second
  probe with the eligibility authority absent likewise silently returns `zero_received` rather than
  surfacing the missing authority when an in-slot observation exists. The implementation also
  decides visibility with `relation.received_ts_utc <= evidence_as_of_ts_utc`, using receipt time as
  a surrogate for committed/system-knowledge visibility.

This can make `zero_received` depend on whether an optional relation object happened to be
materialised rather than on the eligible committed observation evidence governed by BC-008. It also
conflates receipt time with the assessment system-knowledge boundary.

**Recurrence classification:** `ISOLATED`. This is the first VI-13R failure/repair cycle for U04;
there is no prior U04 Reviewer failure/Worker repair lineage establishing a recurrent class.

**Smallest complete repair proposition:** assessment derivation must operate from capture-local,
eligible admitted/committed observation evidence visible to its own transaction independently of
whether a receipt-evidence relation was separately materialised; missing required eligibility
authority must fail closed rather than manufacture zero; and `received_ts_utc` must not stand in for
system-knowledge/commit visibility. Add bounded implementation-coupled regressions for that
mechanism while preserving the existing relation semantics, append-only assessment chain,
U01-U03 behaviour and the U05 boundary.

U04 is not promotable. U05 remains prohibited pending bounded U04 repair and fresh independent
review.
