# D010 — controlled live-source, open/liquid Boolean

ACCEPTED_FOR_IMPLEMENTATION under owner accepted root EXEC_PLAN.md §§2.1,3,5; independent final semantic and strict proof remain required.

## 1. Exact source and two cases

Actual public D001/D003 yield aware Saturday 2026-10-10T00:59:50+11:00. M00 projects R005 as native integer marketDataType=1 under mmt-d010-r005/1 and selection identity requested.mode live, generation controlled-stream/1, value.role delivered_market_mode. Preserve receipt and event instant. Versioned controlled-delivered-mode/1 maps delivered 1 to eligible live; codes 2–4, unknown or missing cannot certify live. R005 is a data-quality precondition, never an open/closed flag. M00 R023 overnight/1 and R024 controlled-overnight/1 project exact native calendar identities. The complete synthetic Melbourne calendar covers Friday00–Sunday00; Saturday overnight/day are open. Separate controlled-market-state/1 knows Saturday open; controlled-phases/1 is nonoverlapping overnight [00,06), day [06,16), and only overnight is declared liquid. Actual D003 with these sources yields typed Boolean true and full selected lineage with ordinary SQLite read-only roundtrip.

The refusal leaves R005=1, R023/R024 and actual D003 unchanged, using controlled-market-state/2 without applicable Saturday state. It yields no Boolean/result/history. A declared known closed v3 yields false, not refusal; no third physical case. These are synthetic controlled facts; no native live feed or exchange certification.

## 2. Incorporated bytes

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F01_TEMPORAL_E11_SOURCE_EXTRACTION.md | 5cf80f45f10841303d01f992e81b39f0affb335cb6c652ab12bedc17e14a01c7 |
| handoff/foundation_implementation/authority/D010_PROFILE.json | fe424d0b29126678c8cb5d03864db12376d827e95d3c0ae1b74ef8307142cb48 |
| handoff/foundation_implementation/authority/D010_PROOF_CONTRACT.json | 33d74d392c97945df5c616d42b1c50855b8dcdc5615b4ad6e26b287f55f5c723 |
