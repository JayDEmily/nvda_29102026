# D009 — controlled atomic macro vintage statuses

ACCEPTED_FOR_IMPLEMENTATION under owner accepted root EXEC_PLAN.md §§2.1,3,5; independent semantic and strict acceptance remains mandatory.

## 1. Exact nine M00 facts and two physical cases

One synthetic series `controlled-macro-series/1`, reference period `2026-09`, provider foundation-controlled-macro/vintage_v1, subject NVDA, as-of/cutoff 2026-10-09T14:00:00Z. Three immutable vintage IDs v1/v2/v3 each co-reference R280/R281 date-only realtime-start/end and R282 native offset-aware last-updated, nine actually projected facts. Publication ordinal 1/2/3 and distinct publication timestamp 11:00/12:00/13:00Z are projected in each role's selection identity, as are series/reference/vintage/field role. Receipts 11:05/12:05/13:05Z are separate and eligible before cutoff; R282 last-updated 10:50/11:50/12:50Z never substitutes for publication time. All dates and instants remain typed and native scalar lineage is retained.

The one public `materialise_vintage_statuses` operation for one exact series/period/cutoff is atomic/idempotent and returns an ordered tuple of three **separately identified and persisted/readable** typed occurrence records: v1 `initial`, v2 `revised`, v3 `latest_known_at_cutoff`, each with its own realtime period, publication identity/time, cutoff and selected triple. Public reader get/history and ordinary SQLite read-only reopen all three. An earlier initial-only cutoff yields only v1 `initial` under the same operation; this is a declared branch, not an additional physical case.

The refusal keeps v1/v2 and v3 R280/R281 visible but omits v3 R282. The incomplete newest triple is reached and invalidates the whole operation; no tuple, older fallback or partial persistence. Exactly two physical cases. No FRED native source certification.

## 2. Incorporated bytes

D009-PROOF-CONTRACT-SHA256: 0b388ac87c0a419066bbcb5912394d0fad8226a1684a1e4c83e3e75c79bea87d

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F01_TEMPORAL_E11_SOURCE_EXTRACTION.md | 5cf80f45f10841303d01f992e81b39f0affb335cb6c652ab12bedc17e14a01c7 |
| handoff/foundation_implementation/authority/D009_PROFILE.json | 82dcdd7d5ef6290049dfce2e3ca470e89737e08f4ecf35b514df6dcb475bd29c |
| handoff/foundation_implementation/authority/D009_PROOF_CONTRACT.json | 0b388ac87c0a419066bbcb5912394d0fad8226a1684a1e4c83e3e75c79bea87d |
