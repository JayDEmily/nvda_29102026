# D003 — controlled IANA local timestamp

ACCEPTED_FOR_IMPLEMENTATION under accepted root EXEC_PLAN.md §§2.1,3,5. Independent final proof remains required.

## 1. Exact source and two cases

M00 R002/R003 produce actual public D001; the same controlled provider/variant/subject/sample supplies separate R004 native IANA string from `time.iana` with role `exchange_iana`, true-instant source 2026-10-09T13:59:50Z, receipt 13:59:55Z and cutoff 14:00Z. Controlled policy `controlled-IANA-Melbourne/1` admits exactly Australia/Melbourne with +11:00 at this instant. Convert actual D001 UTC 13:59:50Z to aware local 2026-10-10T00:59:50+11:00 without changing the instant; retain the exact R004 projection, policy and nested predecessor in typed durable lineage. No native exchange timezone is certified.

The success physically projects three M00 roles, materialises actual D001 and D003 and reopens ordinary SQLite read-only. The refusal changes only the projected R004 native string to `Unknown/Nowhere`, preserves actual D001, and checks no D003 result/history. Exactly two physical cases. D004/D005 remain separate.

## 2. Incorporated bytes

D003-PROOF-CONTRACT-SHA256: e9772d99c216d9a0c6f675113f2c1cb5982893340e4572f5527e89cfd3622be1

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F01_TEMPORAL_E11_SOURCE_EXTRACTION.md | 5cf80f45f10841303d01f992e81b39f0affb335cb6c652ab12bedc17e14a01c7 |
| handoff/foundation_implementation/authority/D003_PROFILE.json | d97557301b420df70759191c655b086803379a3f2bdaa31ad237615285b584c2 |
| handoff/foundation_implementation/authority/D003_PROOF_CONTRACT.json | e9772d99c216d9a0c6f675113f2c1cb5982893340e4572f5527e89cfd3622be1 |
