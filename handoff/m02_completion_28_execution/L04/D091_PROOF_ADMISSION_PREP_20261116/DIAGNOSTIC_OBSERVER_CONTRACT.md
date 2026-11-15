# D091 diagnostic observer — proposed exact implementation binding

**STATUS: PROPOSAL FOR INDEPENDENT ADMISSION; NO PRODUCT API OR TEST IMPLEMENTED.**

Authority chain: installed EXEC_PLAN.md L01b/L04 and §4; owner-adopted R112 exact source SHA-256 31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63; independent source-meaning verdict 37fab2c81e1ed98b227f75f600d3e0c12347d7d5; independent D091 design verdict 05f6b4b707c6231dc9b4d54a4a6cb626711808de §4–§7 (ACCEPT_DESIGN_ONLY). Reviewer accepted the **requirement** for immutable, typed, nonpersistent failure-stage evidence but did not approve this exact Protocol or execute its path.

## Proposed public-facing minimal shape

- **D091RefusalStageV1** is a finite exact literal enum with seven permitted stage names: UNSEALED; ORIGIN_OR_IDENTITY; CLOCK_OR_SCOPE; HISTORY_OR_AMBIGUOUS_RANK; ABSENT; NONFINITE; RANGE. Refusal stages never include a numeric value or label result.
- **D091DiagnosticEventV1** is frozen/slots and exact-type validated; fields: request_identity (nonempty, deterministic versioned ID covering the entire exact requested source/rule/as-of identity); source_observation_occurrence_id (nonempty exact M00 ID string or None); stage (exact enum member); source_profile_ref (exact T01-R112-CONTROLLED-FRACTION-1 v1); rule_profile_ref (exact D091-SYNTHETIC-TENTATIVE-V1 v1). Preserve only these five fields; no mutable M00 owner/state/commands or arbitrary raw payload.
- **D091DiagnosticObserverV1**: a construction-time optional callable receiving exactly one immutable D091DiagnosticEventV1 per refused materialise invocation. It is **output only**, not a source/clock/selector input or an event-factory injection. The full coordinator read capability is retained internally and never provided to the observer.
- **D091 materialise(request) → occurrence or None** remains the ordinary narrow result contract, retaining no persistent refusal DTO. A refusal event accompanies None only if an observer was explicitly installed at owner construction. The absence of a configured observer cannot turn a refusal into success. The observer must not be able to set or spoof a diagnostic stage; stage is selected by the actual evaluator after the completed preconditions.
- **Constructor and failure discipline:** allow only a bounded construction-time observer, with validation of callable shape. If it raises, propagate/fail closed without returning an apparent success or appending a D091 record. Exactly one event per refused materialise invocation must be observed under the strict Tester observer when installed. A successful occurrence produces no refusal event.

## Exact stage order and reached-refusal invariant

1. Reject unsealed/private source capability as **UNSEALED** before the first history page. Caller must never supply a boolean to simulate a seal.
2. Verify source provider/variant, subject/contract, original native units, all **11** option/model/generation/request identities, mapping path/version, exact native type, R112 catalogue role and original public M00 observation getter; mismatches yield **ORIGIN_OR_IDENTITY**.
3. Check actual receipt-only event absence, exact scope, `received_ts_utc == as_of_utc <= knowledge_cutoff_utc <= calculated_at_utc`, no source timezone/instant; mismatches yield **CLOCK_OR_SCOPE**.
4. Consume all returned M00 projected-history cursors (page size 8; <=64 projected members), verify no cycles/nonprogress/duplicate conflicts, unambiguous max `(receipt, sequence)` and stable sealed roster. Any incomplete/ambiguous history yields **HISTORY_OR_AMBIGUOUS_RANK**.
5. If there is no exact eligible projected `model.delta` at the requested receipt, emit **ABSENT** (never return a preceding receipt as a zero-age substitute); an absent raw model field is not a projected history item and may need an independent cohort manifest assertion.
6. If exact raw decimal is nonfinite, emit **NONFINITE**, not a numerical category. Raw M00 may lawfully carry Decimal('NaN').
7. Only after all foregoing applicable conditions and complete history check may a native exact **finite Decimal** outside inclusive [-1,1] emit **RANGE**. A strict Tester must correlate RANGE with **T01-R112-BATCH-12** / original Decimal('1.01'), its actual public M00 readback and an absence of persistent D091 occurrence. An incorrect origin, source metadata, missing value or incomplete history **must never** be rebranded RANGE to obtain a reached-refusal pass.

The ranking/negative-condition order above is a **proposed evaluator design**, not a claim of current execution. The independent reviewer must resolve the nuanced interaction of validating all eligible projections versus the current targeted as-of request: a foreign or out-of-range earlier candidate must not be silently ignored without documenting source policy. Observer tests must assert which invariant was truly reached, not merely a returned None.

## Persistence errors are not business refusals

SQLite append/readback/schema failure or a commit whose outcome is uncertain uses existing M02 PersistenceFailureV1 semantics and retains outcome_uncertain where applicable; never suppress into None, RANGE or a diagnostic business-stage event. A persisted successful D091 occurrence may only be returned after accepted transaction commit and readback. Separate standalone reader validates exact type/definition/source/source-sign/codec content and original first calculation time without live M00.

## Verification and release conditions

Independently inspect exact factory signature, observer exposure, immutability, event count, real call sequence, no command-handle escape, absent original projection path and failure propagation. No test has been admitted; observer code and tests must not be authored until exact changed-path, claim/generation and physical-case/fixture authority is admitted. An observer alone never proves a seal.
