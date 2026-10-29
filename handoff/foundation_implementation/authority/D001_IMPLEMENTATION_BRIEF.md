# D001 — controlled true-instant UTC conversion

ACCEPTED_FOR_IMPLEMENTATION under owner accepted root EXEC_PLAN.md §§2.1,3,5; independent final semantic review and strict acceptance still required.

## 1. Exact source and two cases

Controlled M00 provider foundation-controlled-temporal/clock_v1, subject NVDA, sample controlled-temporal-sample/1; two co-referenced roles R002 source timestamp and R003 supplied offset, with exact source/event/receipt identity. As-of and cutoff 2026-10-09T14:00:00Z, receipt 13:59:55Z, event 13:59:50Z. R002 native 2026-10-10T00:59:50+11:00, R003 +11:00. The offset of R002 must agree with R003 and source timezone; convert the same true instant to UTC 2026-10-09T13:59:50Z, never invent midnight. Unit native_time is an exact typed temporal projection, not Decimal arithmetic. Own D001-TRUE-INSTANT-UTC-1/K01/P_TIME, mmt-d001-selection/1; immutable definition, mapping, unit, parameter, typed raw lineage, public typed owner and SQLite read-only reopen.

Success projects both actual M00 facts, verifies their complete metadata/co-reference and exact aware UTC result and all selected lineage after public reopen. Refusal changes only R002 to visible date_only/native 2026-10-10; R003 remains projected, no occurrence/history. Two physical cases only; date-only source must be inspected before kind refusal, without prefilling D001 or running an old test. No native exchange/vendor timezone certification, D002 age or D003 local timestamp acceptance.

## 2. Incorporated bytes

D001-PROOF-CONTRACT-SHA256: c27c969ffdfff8a5f4ed716e03e7cf009a5e2d5546de9f6bb9383dc97032bbdc

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F01_TEMPORAL_E11_SOURCE_EXTRACTION.md | 5cf80f45f10841303d01f992e81b39f0affb335cb6c652ab12bedc17e14a01c7 |
| handoff/foundation_implementation/authority/D001_PROFILE.json | bf761ed8631ef5dc2526af33b3f550a97399268acdfbdd9c2fa8de7934713cef |
| handoff/foundation_implementation/authority/D001_PROOF_CONTRACT.json | c27c969ffdfff8a5f4ed716e03e7cf009a5e2d5546de9f6bb9383dc97032bbdc |
