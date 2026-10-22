# D017 — controlled session VWAP
Status: ACCEPTED_FOR_IMPLEMENTATION under the owner's D017-only instruction and subsequent “Yes” authorising the necessary exact-ratio/raw-only window interface extension, 22 October 2026. Standing delegation admits these concrete bytes and exact two-case proof; one independent final review remains required. Baseline c57016955fd10beacc1fca955cc9449888192da5. No later signal authorised.

## 1. Fixed meaning and controlled policy
Effective primary meaning: incorporated brief K02 D017, §§6–9,11–15,17 and catalogue D017; preparation F04. VWAP = sum(price*size)/sum(size), selected by admitted session/anchor rather than all loaded history. No D predecessor. Historical PostgreSQL mechanism requirements are replaced by accepted SQLite authority.

Controlled subject NVDA; provider foundation-pilot-fixture; variant cash_quote_v1; ingestion scope foundation-pilot-fixture/cash_quote_v1. Event basis true_instant, UTC ISO-Z timestamps; event<=receipt<=cutoff. Same M00 observation carries explicit R120 trade.price/price and R121 trade.size/shares. Mappings mmt-trade-price/1 and mmt-trade-size/1, no selection identity; units mmt-pilot-price/1 and mmt-trade-shares/1, exact identity conversions. Never infer units from record-wide metadata or values.

Definition D017-SESSION-VWAP-1, K02_ALGEBRA, equation `sum(price * size) / sum(size)`, raw(R120,R121), no derived dependencies, P_BASIC, price, scalar_exact_ratio; authority_refs exactly first two incorporated records below. Parameter mmt-session-vwap/1, P_BASIC, NVDA, membership(NVDA). Policy mmt-vwap-selection/1, joins(subject_instrument), maximum_staleness3600s, maximum_skew0, true_instant only, empty basket, source above,100 records/page,1000 pages.

WindowContextV1 controlled-vwap-session/1: session_start2026-10-20T12:00:00Z, session_end13:00:00Z, history_complete_from12:00:00Z. This immutable controlled fixture declares complete quiescent finite histories of both fields; not a native feed/calendar/completeness certification. Request context refs exactly this context. Require session_start<=as_of<session_end, history_complete_from<=session_start, as_of<=cutoff<=captured_now, and integral-second session elapsed duration. Select [session_start,as_of] inclusively; do not bridge sessions, clip an unavailable start or use UTC midnight. Preserve full context and elapsed window_seconds in result identity. Changing material context values requires a new context version.

Enumerate each public R history completely under subject/event/receipt upper bounds. Reject malformed envelopes, conflicting duplicate IDs, repeated/invalid continuation cursors, exhausted page bounds and inadmissible selected contributors. Out-of-session records must remain visible to enumeration and be excluded by event bounds. Compare complete selected R120 and R121 occurrence-ID sets: nonempty and equal, never take intersection. Pair by exact native occurrence ID, identical subject/provider/variant/sequence scope/sequence/event/receipt, valid explicit mapping/unit/profile. Stable lineage order ascending event then observation ID, interleaved price,size. Nonnegative finite Decimal prices/sizes; zero price is allowed as controlled mathematical value, zero size allowed but total size must be positive. Missing size, mismatch, empty window or zero denominator refuses without persistence.

Convert each Decimal to its exact integer-ratio value and accumulate using exact rational arithmetic; divide only by positive total size. Return canonical reduced existing ExactRatioV1, including nonterminating values without ambient Decimal rounding. The agreed positive is24/5 (4.8 exactly); no extra witness is introduced for nonterminating division.

## 2. Necessary shared extension and reuse
Extend existing WindowMeasurementOccurrenceV1.result from Decimal to Decimal|ExactRatioV1. Permit predecessor_reader=None for raw-only window calculations; D016 still requires its actual reader and retains its exact Decimal/sign validation. Preserve earlier request/result fields, D016 record bytes, definitions/configurations, test/contract/generation files and all earlier source behaviour. Do not make a D017-specific API or store.

Route only exact D017 admission through existing create_window_owner/reader; add the D017 calculation/selection/semantic validation in _session_vwap.py, reusing existing window reads, logical identity and decoder. Add a narrow D017 routing branch to _window.py admission/read/validation paths. No old D016 calculation path is replaced. Use existing _record_store.RecordState unchanged: same schema/profile/canonical hashing, immutable transactions, atomic first fact and ordinary readback. Existing _evaluation typed union/dataclass codec already supports the exact-ratio record; no codec edit or SQL change.

Namespace neutral_market_measurement_truth/window/v1, mmtwindow1: identity, same canonical full-record identity excluding own ID/calculated time, original calculated time retained in payload. Full definition/parameter/policy/unit/mapping/request/context and selected raw lineage retained. D predecessors empty. Durable reads validate complete snapshots, equation and identity without source readers; wrong admission cannot open another signal's record file. Lawful unavailability returns None, exact wrong public types/content TypeError/ValueError and persistence errors existing PersistenceFailureV1.

## 3. Proof and delegated disposition
D017-PROOF-CONTRACT-SHA256: d198acf3ec649d9a98280a970e2480ece6c2da280b17d27fdd0f224dddb0a1a9

Physical tests/product/market_measurement_d017/test_session_vwap.py, sole test_d017_session_vwap, exactly two parameterised cases. Actual public M00 records: trade-a at start+10s price6 size2, trade-b at+20s price4 size3; fully paired outside decoy at start−20s price100 size100, visible to both histories. As-of start+120s, cutoff+1s, now+2s. Positive exact24/5, complete metadata/lineage, public durable reopen. Refusal preserves trade-b price but omits its size field/provenance; asserts intended missing size and empty D017 history. No injected predecessor, hidden extra scenario or expanded suite.

Before behaviour, worker independently inspected primary meaning, exact literals, exposed decoy and genuine missing-size precondition under standing delegation. This is concrete worker adequacy disposition, not fabricated independent review. One strict admitted RED at absent exact window carrier after actual M00 prerequisites, then one independent final strict GREEN: python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d017. One scoped mypy and one changed-path Ruff invocation. Inspect and format cases before hash admission; retain immutable generation if a real later repair changes proof. No old claim, broad suite, extra numeric/boundary/storage/fault tests or duplicated GREEN. One final reviewer covers actual source/fixtures and executes the same two cases. No D018 work.

## 4. Exact incorporated bytes
| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md | a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | f1eedec4aa2fcc543a66b709ecd925dd713d01ecabf19c776d5f1b07d3e15f8e |
| handoff/foundation_implementation/authority/D017_PROOF_CONTRACT.json | d198acf3ec649d9a98280a970e2480ece6c2da280b17d27fdd0f224dddb0a1a9 |

