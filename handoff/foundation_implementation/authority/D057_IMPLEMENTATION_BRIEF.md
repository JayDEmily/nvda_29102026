# D057 — commissioned controlled volatility relationship

ACCEPTED_FOR_IMPLEMENTATION under the current explicit owner acceptance/execution commission. Independent final semantic review/strict evidence remains required; no native-source certification.

## 1. Owning profile, manifest and proof

D057: accepted root EXEC_PLAN.md §4.1 at 2f2cd9841504702c869412aadc83afb1f96b8d09, owner accepted and execution authorised in current thread. Exact controlled profile {"raw":["R238","R239"],"series":["VIX1D","VIX9D"],"values":["15","20"],"expected":[[-5,1],[3,4]],"fault":"zero"}. Ordered raw bindings follow the listed tuple; no derived predecessors. K02_ALGEBRA, P_BASIC; first-minus-second and first/second as TermPairV1(point_difference,ratio) with mandatory reduced ExactRatioV1 members for D057–59; D060 is ExactRatioV1 ratio only. Units index_points / ratio and shape named_exact_term_pair (D057–59); ratio / exact_ratio (D060). Definition D057-TERM-PAIR-1 (D057–59) or D057-VOL-RATIO-1 (D060). Parameters mmt-d057-controlled/1; selection mmt-d057-selection/1; subject NVDA. T=20Oct2026 13:00Z, cutoff T+1s, now T+2s; current age<=60s and selected event skew=0. Context controlled-volatility-terms/1 spans T-60s to T+1s, history complete from T-60s. Exact request fixed to that T/cutoff/context; no predecessor or other binding. Provider foundation-controlled-macro/macro_snapshot_v1, native metric.value finite Decimal; metric.series as listed, metric.measurement_date matches event UTC date, metric.method=controlled_snapshot/1, metric.quote_orientation=not_applicable, no revision vintage. Mapping mmt-macro-rNNN/1 and mmt-macro-rNNN-units/1 index_points->index_points scale1/offset0. Complete bounded histories, stable latest eligible event/receipt/sequence selection before numeric denominator validation; selected invalid zero never falls back. Zero denominator refuses; no positivity policy invented. Complete typed metadata, actual selected raw lineage, public ordinary SQLite read-only reopen/history in success; named refusal confirms its actual public input facts and no persisted occurrence/history. Exactly two cases, no executed RED/extra probes/native certification. Immutable source/profile and exact arithmetic are reviewed within the pair.

Physical proof: tests/product/market_measurement_d057/test_signal.py; test_d057_signal[success] and [refusal]. Owning production delta: _volatility_terms.py fixed per-ID configuration/brief registry and _window.py routing. D057 introduces public TermPairV1, result union and export; later term IDs reuse them unchanged. No M00, old source/profile/test, storage/codec or runner algorithm change. G01 fixed declaration only. No routine runtime RED; omission reduces test-first evidence.

## 2. Incorporated bytes

D057-PROOF-CONTRACT-SHA256: 465a8dd5aa8b6e3ae8f0c1cccd33d6a911865d6b35230f91172ec004155e521a

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md | a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | f1eedec4aa2fcc543a66b709ecd925dd713d01ecabf19c776d5f1b07d3e15f8e |
| handoff/foundation_implementation/authority/D057_PROOF_CONTRACT.json | 465a8dd5aa8b6e3ae8f0c1cccd33d6a911865d6b35230f91172ec004155e521a |
