# D091 target-relative selector and refusal precedence — RETURN-01 correction candidate

**Status:** REVISED DESIGN CANDIDATE ONLY; not an owner-adopted source-policy amendment or implemented selector. Parent `RETURN`: `c2e4559e648fc3b1a3e2b7d7eaea79568e75b7d4` §3. Original adopted controlled-source contract SHA256 `31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63` is unchanged. All claims below are **proposed executable semantics** subject to independent reconciliation with that contract.

## Discriminate provenance validation from selected-target business validity

The earlier proposal incorrectly risked treating a *historically visible* raw invalid value as a failed **current request**, so the original t12 = 1.01 might mask t13 = NaN and t14 = absent model.delta. The corrected design uses two distinct predicates:

1. **Global structural/provenance integrity** for *every projected candidate* returned across every cursor page: original M00 getter exists, identity and native units match approved contract and projected record, exact version/mapping/source IDs, original exact Decimal type (including possible nonfinite Decimal, since nonfinite is a native-domain failure rather than a projection-provenance failure), unambiguous occurrence content, proper clock metadata and scope, valid returned cursors, sealed-cohort membership. An inconsistent earlier projected record must not be ignored. Global structural/identity/history failure must fail closed at its evidenced stage.
2. **Target-specific classification validity** for the single highest-ranked **exact requested receipt** in a sealed and fully validated population: target value exists, is exact **finite Decimal** and within [-1,1], then abs bin. Prior numeric value 1.01 or NaN **is not the requested value** and does not cause RANGE/NONFINITE if the target is t13/t14. Thus the historic rejection of a prior value is not silently transported to later requested timestamps.

This discriminates **all eligible projected candidates** as required by the source contract, without making past numerical category validity a global invariant unless the source authority independently says that is required. The review MUST determine whether this distinction is faithful to the owner's adopted exact contract. If it is not, the source meaning conflicts with the three original negative oracles and an owner/source-policy clarification is required; the Worker must not quietly "fix" it by changing the source.

## Proposed explicit evaluation order

A. **Preflight request and private cohort**: validate exact D091 request contract and numerical/clock fields; reject a malformed as-of/cutoff/calculated order with `CLOCK_OR_SCOPE`. Under the coordinator guard verify actual `SEALED` state and nonescaped exclusive writer; if absent `UNSEALED` without a projected page. Neither caller nor observer may assert a seal.

B. **Admitted manifest check**: in the sealed private owner, verify exactly the original fifteen IDs/hash/content and every public M00 original getter. The source manifest is used to detect **unprojectable target raw observations** (e.g. missing model.delta) and does not pretend M00 can project a missing field. The manifest's immutable 15-member hash is not proof of runtime closure; the coordinator has to enforce and independently prove it.

C. **Exhaust all projected history** under one lock with `R112`, the exact mapping and subject, `event_at_or_before=None`, `received_at_or_before=knowledge_cutoff`, page size 8 and only returned next cursors. Check page progress/cycle/duplicate IDs; ≤64 *projected* items, no silently omitted eligible pages. `HISTORY_OR_AMBIGUOUS_RANK` for malformed page/cursor, count overflow or distinct equal maximal rank.

D. **Global provenance**: compare projected and original getter for every returned candidate (provider/variant, subject, original native units, temporal kind/source clock absence/receipt/scope/sequence, mapping path/ID/version, native record identity all 11 fields, type fidelity, original source ID). Use `ORIGIN_OR_IDENTITY` for mismatch of native identity/units/source; `CLOCK_OR_SCOPE` for actual temporal/scope disagreement; do not evaluate absolute magnitude, finiteness or D091 bucket of a historical candidate at this stage. A provider/variant wrong **raw input alone** is prefiltered by current M00 mapping and may be rejected by coordinator ingress/seal *before* D091; it is NOT automatically a reached D091 ORIGIN diagnostic.

E. **Find target** using exact receipt equality and request identity after complete history. M00 ranks by receipt, scope, sequence and ID for display; D091 ranks candidates by receipt/sequence only, and distinct IDs tied at maximal eligible pair refuse **HISTORY_OR_AMBIGUOUS_RANK**. Never choose ID as the tie-break. To determine whether a target raw member exists but its `model.delta` is absent, compare the verified sealed **original roster** at the exact requested receipt and original getter. If that target exists with missing `model.delta`, `ABSENT`; if neither projected candidate nor original roster member exists at the exact as-of, distinguish complete absence (ABSENT) from selecting a prior non-zero-age observation (CLOCK_OR_SCOPE) with explicit fixed request policy. A request may not silently return a prior receipt result. An arbitrary missing raw field must not be replaced by zero.

F. **Business domain on exact selected target only**: finite exact `Decimal` required; `NaN` ⇒ `NONFINITE`, finite `1.01` ⇒ `RANGE` after all A–E; otherwise signed delta retained and its absolute value is bucketed under accepted bins. No historical earlier t12 value causes t13/t14 failure, because that value is not selected.

G. **Only after lawful category**: append and read back a strict immutable M02/D091 SQLite DTO. Precommit/uncertain commit/readback failure raises existing `PersistenceFailureV1`, preserving `outcome_uncertain` as applicable. No business-stage diagnostic event is fabricated for persistence failure. Successful `materialise` must not return without committed/readback occurrence.

## Original 15-member fixed negative precedence oracle (documentary only)

| Target exact as-of UTC (2026-11-15) | Exact original raw occurrence | Original native field | Expected D091 domain result **if all prior invariants pass** |
| --- | --- | --- | --- |
| 12:00:12Z | T01-R112-BATCH-12 | `Decimal("1.01")` | One typed `RANGE` event, no stored occurrence |
| 12:00:13Z | T01-R112-BATCH-13 | `Decimal("NaN")` | One typed `NONFINITE` event, no stored occurrence, **not RANGE from t12** |
| 12:00:14Z | T01-R112-BATCH-14 | Missing `model.delta` | One typed `ABSENT` event, no stored occurrence, **not NONFINITE from t13 or RANGE from t12** |

At t14 the projected history has 14 (not 15) entries; the absent source member exists only in the original cohort/readback. An independent reviewer must confirm this **proposed** selected-target distinction against the accepted source meaning, inspect the actual original source and page machinery, and require direct source-independent Tester sequences. No source DTO or D091 implementation exists here.

## Observer distinctions

The existing seven proposed diagnostic stages remain: `UNSEALED`, `ORIGIN_OR_IDENTITY`, `CLOCK_OR_SCOPE`, `HISTORY_OR_AMBIGUOUS_RANK`, `ABSENT`, `NONFINITE`, `RANGE`. The proposed five-field frozen/slots diagnostic event and optional construction-time output-only observer remain unchanged. Source-ingress rejection by the private coordinator is a **different owner boundary**, not an eighth D091 diagnostic stage or an invented D091 callback. Returned-cursor anomalies are controlled read-port fault seams; they prove only D091 fail-closure, not that ordinary M00 emits corrupt pages. No claim of stage reachability is made without executing an admitted case.
