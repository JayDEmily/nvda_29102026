# D042 — commissioned controlled implementation

ACCEPTED_FOR_IMPLEMENTATION under owner execution of final D037–D056 plan 8bc212b, with independent final semantic review/strict evidence required. Native-source certification remains held.

## 1. Owning profile and proof

D042 controlled2s10s slope =100*(R249−R247). R247 DGS2=.0425 and R249 DGS10=.0390 at20October2026 13Z give Decimal(-0.35) percentage_points. Negative changes only R247 receipt to cutoff+1s; source remains publicly projectable at late cutoff, but result cutoffT+1s must exclude it and emit no occurrence. Canonical rate_fraction identity scale, metric.value Decimal; metadata metric.series matching named series, metric.measurement_date exact selected event date, metric.method controlled_snapshot/1, metric.quote_orientation not_applicable. Provider foundation-controlled-macro/macro_snapshot_v1; mapping mmt-macro-r247/1,mmt-macro-r249/1; corresponding identity units. Definition D042-RATE-SLOPE-1 K02_ALGEBRA/P_BASIC; mmt-d042-controlled/1,mmt-d042-selection/1, current fresh60seconds, public full bounded history30days. Separate typed WindowContext controlled-macro-history/1 spansT−30days toT+1s with historycompleteT−30days. Two current source roles must share measurement date, no D predecessors. Fulltypedidentity/orderedlineage/SQLite reopen asserted; no native certification.

Exactly two cases in tests/product/market_measurement_d042/test_signal.py, function test_d042_signal [success]/[refusal]. Success asserts full typed metadata/configuration/selected actual public M00 lineage and read-only SQLite reopen; refusal reaches its specified defect and persists no occurrence. No runtime RED; discriminatory power independently reviewed. Reuse unchanged public M00/M02 storage, codec and selection mechanisms; no old tests.

## 2. Incorporated bytes

D042-PROOF-CONTRACT-SHA256: 39d0bf4a88be1df9db83b679fa058f689d32a936ad8b004daab7b73cfb048a0f

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md | a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | f1eedec4aa2fcc543a66b709ecd925dd713d01ecabf19c776d5f1b07d3e15f8e |
| handoff/foundation_implementation/authority/D042_PROOF_CONTRACT.json | 39d0bf4a88be1df9db83b679fa058f689d32a936ad8b004daab7b73cfb048a0f |

