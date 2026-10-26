# D004 — complete controlled overnight trading-date calendar

ACCEPTED_FOR_IMPLEMENTATION under owner accepted root EXEC_PLAN.md §§2.1,3,5. Actual D003 public predecessor, full R023/R024 source and independent final proof are mandatory.

## 1. Exact synthetic meaning and two cases

The actual public D001->D003 local instant is Saturday 2026-10-10T00:59:50+11:00. R023/R024 are native strings `overnight/1` and `controlled-overnight/1`, projected under exact controlled provider/variant/subject/sample, event 13:59:50Z and receipt 13:59:55Z before cutoff. No numeric coercion. Versioned `controlled-overnight/1` configuration declares Australia/Melbourne and complete, gap-free, nonoverlapping, half-open coverage from Friday00:00 to Sunday00:00 local: Friday00–16 closed; Friday16–Saturday06 overnight, assigned Friday trading date; Saturday06–16 day, assigned Saturday trading date; Saturday16–Sunday00 closed. Saturday is explicitly open for the two named sessions. Coverage outside this interval is not admitted. Date-only civil midnight or UTC calendar fallback is forbidden.

Success uses version1 and returns typed trading date 2026-10-09, preserving the selected two raw projections, versioned complete calendar and nested actual D003 (itself actual D001/M00), and ordinary SQLite read-only reopen. Refusal uses a version2 full calendar with the overnight interval explicitly closed; the same projected R023/R024 and actual D003 remain, but no applicable session exists and no D004 result/history is emitted. Both policies are validated for complete coverage, boundaries, no overlap, exact IANA zone and day attribution at configuration admission. Exactly two physical cases. No native exchange calendar certification, D005 or D010 acceptance.

## 2. Incorporated bytes

D004-PROOF-CONTRACT-SHA256: 3ac9c18ab2218f61c95c05ed2f915c3ea438c5c460ac4e7053ae13ecba878adc

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F01_TEMPORAL_E11_SOURCE_EXTRACTION.md | 5cf80f45f10841303d01f992e81b39f0affb335cb6c652ab12bedc17e14a01c7 |
| handoff/foundation_implementation/authority/D004_PROFILE.json | 231e7c72a029dd3f8320835cfe0e7b02885788afbe68d0936254f93c1d7acc82 |
| handoff/foundation_implementation/authority/D004_PROOF_CONTRACT.json | 3ac9c18ab2218f61c95c05ed2f915c3ea438c5c460ac4e7053ae13ecba878adc |
