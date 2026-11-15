# D091 pre-implementation technical boundary (no source edits)

**Proposition:** For a lawfully admitted exact R112 signed Decimal fraction for the exact synthetic option/model/identity and receipt-only selection policy, calculate immutable, non-overlapping **absolute-delta category** and persist a public readback with the required identity/provenance. This describes *future* implementation; no D091 implementation or product proof is claimed.

## Accepted meaning versus proposed source choices

- Current canonical D091 row: R112, no D predecessor, K08_RULE_BUCKET_POLICY, P_RULE, category output, as recorded in `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` and original K08 truth brief. The accepted foundation/SQLite-v3 source binding is `implementation/authority/FOUNDATION_IMPLEMENTATION_AUTHORITY_BINDING.yaml`.
- PR #19's `R112_SOURCE_CONTRACT_PROPOSED.json` explicitly proposes a *synthetic-only* source provider `t01-controlled-option-delta`, variant `controlled-option-model-delta/fraction-v1`, model `CONTROLLED_SIGNED_DELTA_V1`, native `model.delta` Decimal in `signed_decimal_fraction` units, identity conversion (no inferred rescaling), inclusive native range [-1,1].
- The proposed profile is `T01-R112-CONTROLLED-FRACTION-1` and proposed selection policy `T01-R112-EXACT-RECEIPT-1`: exact receipt == as_of, as_of ≤ knowledge_cutoff ≤ calculated_at, receipt only, no fabricated event time. Source contract/right/expiry/strike/currency/model/scale/generation/request must match exactly. Within a single declared sequence scope only, rank by latest eligible receipt/sequence; tied distinct observations refuse. Exhaust every page under the configured bound. Explicit exclusive source-batch barrier is a prerequisite; no M00 snapshot API is claimed.
- The V1 D091 rule profile is `D091-SYNTHETIC-TENTATIVE-V1` (synthetic test policy, not production): |δ| in [0,0.10)→ABS_00_10; [0.10,0.25)→ABS_10_25; [0.25,0.50)→ABS_25_50; [0.50,0.75)→ABS_50_75; [0.75,1.00]→ABS_75_100. No output for native absent, nonfinite, >1, wrong provenance or incomplete source.

## Existing contracts inspected — implications, not implementation permission

| Current location | Observed current contract | Necessary bounded extension to review |
|---|---|---|
| `raw_signal_occurrence_truth/api.py` | public raw occurrence admission, mapping, original getter, offset-based projected history | reuse lawful public seam; account for true original observation.native_units instead of relying on mapping.native_units alone; controlled sole-writer closure external to current M00 API |
| `market_measurement_truth/_selection.py` | current pilot selector requires true UTC event instant and empty selection identity | new *narrow* receipt-only R112 selector with exact metadata/identity/time rules, without weakening current pilot |
| `market_measurement_truth/api.py` | `DerivedSignalOccurrenceV1.result: Decimal`; `NativeMeasurementOccurrenceV1.result` allows numeric/pair carriers, not category | explicitly admit a D091 category carrier, exact typed public API/factory/definition; do not encode categories as arbitrary decimals |
| `market_measurement_truth/_native_codec.py` | strict tagged lossless native codec allowlist | add only accepted category record shape and round-trip guard, retaining exact content identity |
| `market_measurement_truth/_native_source.py`, `_native_profiles.py` | existing fixed synthetic source scopes/receipt book reconstruction, not the proposed R112 profile | avoid treating D087 source assembly as R112 model delta; scope any new source adapter/profiles precisely |
| `market_measurement_truth/_record_store.py` and owner-specific SQLite adapters | append/read identity and original durable owner control | independently review correct admitted D091 persistence/codec/read-only reopen path; no new storage backend assumed |
| `tools/product_proof_claims.py` and `config/proof/` | accepted historical claim/generation and physical-test partition machinery | add only approved D091 claim/generation/exact-node inventory; existing runner does not independently cap R2 case count |
| `tests/product/m02_completion_28/d091/test_signal.py` | no tracked file on main at base | after *finite admission*, Worker authors exactly admitted two cases before code; no speculative collection or execution |

## Proposed sequencing and retained proof obligations

1. Independently admit source selection/identity, including closure of multi-page reads and the original observation units/identity recheck; no general provider integration.
2. Independently fix category carrier/codec/durable-identity and proof-control changes as the minimum required implementation contract. A concrete changed-file declaration must be checked against actual APIs before source mutation.
3. Author unexecuted fixed test nodes (not parameterised or hidden additions) only after approved proof admission. One **SUCCESS** node must observe all explicitly enumerated 12 independent `as_of`/receipt requests and compare exact categorisation with independent values; it must not embed expected results as raw input.
4. One **REACHED_REFUSAL** node must drive a lawful signed Decimal 1.01 through public ingress and to the *range* invariant, not fail prematurely for mapping/identity/clock. Nonfinite, absent, wrong identity/time/history and durable failure invariants remain separately enumerated; reviewer must prove genuine reuse or accepted exact coverage within the fixed allocation. A six-case ceiling is not authorisation to invent more.
5. Separate Tester assesses exact collected nodes, independent oracles, durable readback, source/definition/lineage and failure-stage evidence. Any required new physical cases or changed M00 support require prior finite owner authority.
6. Record source and implementation SHA/tree, ownership and independent review outcomes. No downstream D109/D121 claim is released merely because the D091 implementation exists.

**First unclosed semantic requirement:** the operative synthetic source/profile is still only proposed; the documentary independent review accepted its truthfulness as a proposal, not its final source-admission status. Neither technical implementation shape nor local validation can substitute for acceptance of that requirement.
