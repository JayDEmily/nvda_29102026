# D139 — controlled collector-receipt depth insertion rate

ACCEPTED_FOR_IMPLEMENTATION under owner-accepted root EXEC_PLAN.md §§2.2,3,5; independent final semantic and strict proof remain required.

## 1. Exact two cases

One versioned public M00 SMART generation with a complete pre-window bid/ask top book. Four event groups separately project native R001 aware UTC collector-receipt datetime, R185 integer position, R187 integer operation, R188 integer side and R190 Decimal size. Retain separate native true-instant source-event timestamp; select only by actual R001 collector receipt in `(T−4s,T]`, bid positions1–2. Two genuine bid inserts sizes3 and5 produce typed exact count1/2 events/s and size2 shares/s. Preserve full selected and warm-up typed native lineage and ordinary SQLite read-only reopen. Refusal keeps the second selected R001/position/side/size projected but omits R187 operation; no result/history. Controlled receipt-clock semantics do not certify native event-time or SMART source.

D139-PROOF-CONTRACT-SHA256: 4519aa3266c3bfa8a85aa0553965bdd476b52ed206595699a80a0c4607f36e66

## 2. Incorporated bytes

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F33_EXTENDED_E11_E15.md | e045bcc13b70dfb9e238720f4e0ec6113cfc6ccc4496fae733c63416f240ea27 |
| handoff/foundation_implementation/authority/D139_PROFILE.json | cf35e8fa8e81238207ae8e4e0de6697e80749d7e4ba1b34c4fa9c7b2fa568de4 |
| handoff/foundation_implementation/authority/D139_PROOF_CONTRACT.json | 4519aa3266c3bfa8a85aa0553965bdd476b52ed206595699a80a0c4607f36e66 |
