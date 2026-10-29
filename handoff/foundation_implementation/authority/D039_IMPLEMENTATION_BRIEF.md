# D039 — commissioned controlled implementation

ACCEPTED_FOR_IMPLEMENTATION under owner execution of final D037–D056 plan 8bc212b, with independent final semantic review/strict evidence required. Native-source certification remains held.

## 1. Owning profile and proof

D039 fixed two300-second OHLC bars, bar_count=2. Three close instants20October2026 12:30/12:35/12:40Z in controlled-atr-session/1, bounds12–13Z/historycomplete12Z; cutoff12:40:01/now12:40:02. R141 bar.high/R142 bar.low/R143 bar.close native price; mmt-atr-high/low/close/1, same public observation per bar, identity session.id,bar.id ISO-Z event,bar.duration_seconds300,adjustment.basis unadjusted. Controlled provider foundation-pilot-fixture/cash_quote_v1. Previous close100; complete bars110/90/105 and112/99/108. TR1=20 TR2=13 mean=ExactRatioV1(33,2) price. Select required close positions before validating co-fields; never skip incomplete latest bar for older complete one. Negative omits only latest high, retains all3 closes and older complete OHLC. Definition D039-ATR-1 K05_REALIZED_RISK/P_VOL_WINDOW, mmt-d039-controlled/1 (immutable bar_count2), mmt-d039-selection/1 maxstaleness600s/zero skew, mmt-pilot-price/1. Exact public lineage previousclose then high/low/close eachbar, fulltyped/config/time/reopen success and nooccurrence refusal. No D predecessors or native certification.

Exactly two cases in tests/product/market_measurement_d039/test_signal.py, function test_d039_signal [success]/[refusal]. Success asserts full typed metadata/configuration/selected actual public M00 lineage and read-only SQLite reopen; refusal reaches its specified defect and persists no occurrence. No runtime RED; discriminatory power independently reviewed. Reuse unchanged public M00/M02 storage, codec and selection mechanisms; no old tests.

## 2. Incorporated bytes

D039-PROOF-CONTRACT-SHA256: 4bd28d0999489c0e2a61bd8d1a117834624f422bd7f28f098867033dfce30c57

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md | a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | f1eedec4aa2fcc543a66b709ecd925dd713d01ecabf19c776d5f1b07d3e15f8e |
| handoff/foundation_implementation/authority/D039_PROOF_CONTRACT.json | 4bd28d0999489c0e2a61bd8d1a117834624f422bd7f28f098867033dfce30c57 |

