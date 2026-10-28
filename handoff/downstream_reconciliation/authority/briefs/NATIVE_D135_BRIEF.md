# Native D135 immutable implementation brief v1

Owner-commissioned source compatibility implementation for L06: SMART ask top-two/top-one depth.
External acceptance reference: `owner-chat/20261028/downstream-reconciliation/execute-entire-plan`; bounded synthetic receipt, quote250ms/1000ms, directC2scope and two-native-plus-two-legacy allocation explicitly commissioned.

Implement only the exact owning obligation in the source/API/allocation contracts below. Existing accepted equations and M02 ownership remain unchanged. This is synthetic compatibility authority, never live provider policy. D145 remains PAUSED. Existing old/M00 source facts, fixtures, tests and immutable proofs stay preserved. All runtime/product/static execution is deferred to independent L14; implementation status is IMPLEMENTED_UNTESTED.

The following exact bytes are normative components of this brief. Read the source contract, public API, allocation, fixed profile facts, recipes and independent literal oracles in full where they define this owner's obligation. No lower-layer implementation/test may change their meaning.

| Component path | SHA256 |
| --- | --- |
| handoff/downstream_reconciliation/authority/CONSUMER_SOURCE_CONTRACT_V1.md | e68e33d4e6992d3541f9f243233d047ad553657c806072c6ced16bdb1b2f9645 |
| handoff/downstream_reconciliation/authority/NATIVE_PUBLIC_API_V1.md | d4011188c91cd92bc43a3c71043542a0440b0d0b9ba2a05abec1d339ce7439d1 |
| handoff/downstream_reconciliation/authority/PROFILE_AND_PROOF_ALLOCATION.md | cd91dfc90cf44f4a137c768cc88004618ccd469987820da5759769116752a560 |
| handoff/downstream_reconciliation/authority/fixtures/SOURCE_PROFILES_V1.json | e8a1cce559da057e4e92c6d03ed9ba8ac4da7638b15129e118a268578c5cff31 |
| handoff/downstream_reconciliation/authority/fixtures/CALCULATION_PROFILES_V1.json | c57d3e8bf1d2c0cae27308c898e4974e78252e78aba960387da21c3cae687886 |
| handoff/downstream_reconciliation/authority/fixtures/SYNTHETIC_RECIPES_V1.json | 18aed11491ba57e4d0c4eeb1aa01f27002850c395d802b47b84106797971a83e |
| handoff/downstream_reconciliation/authority/fixtures/FROZEN_M00_PUBLIC_OUTPUT_V1.jsonl | 028c7b393d47caad1343ecebb0571c54ce4fd6c492ff6a8386a8ed8c04518fa4 |
| handoff/downstream_reconciliation/authority/fixtures/FROZEN_M00_MAPPINGS_V1.json | edfa78c2c09c793a16878f9cf911e0e6beb028b15f0977dbd9ef69ce44220cb8 |
| handoff/downstream_reconciliation/authority/fixtures/FROZEN_M00_CONTROLS_V1.jsonl | 5b808cd12cbe566aa26e41c11935cb3efce5f6258299925cb14ed97739267501 |
| handoff/downstream_reconciliation/authority/fixtures/PROVENANCE_V1.json | 0e7d0446eeb21b789aec9dab33c9ece34fbafd894d6d271531467e670f160d63 |
| handoff/downstream_reconciliation/authority/expected/SYNTHETIC_REFERENCE_ORACLES_V1.json | 263dec140dbfda57eb50bd8961a9180069176adf8433102e977cccbeaa87e8c3 |

The fixed native claim is `neutral_market_measurement_truth_native_d135`. Its physical root is `tests/product/market_measurement_native_d135`; family is test_signal.py and exactly two physical cases as allocated. Native SOURCE proves source/control semantics, not a D output. Original legacy D cases remain separately scoped. No cross-module replay or new M00 production requirement.

Admission requires exact M02 owner admission against this brief SHA, exact public native profile/request and immutable versioned proof generation before any L14 strict run. Native source/codec/API code may be owner-local siblings; do not change old V1 interpretation or relax generic proof machinery. Subsequent shared-helper changes require explicit affected-claim invalidation and new immutable generation; never mutate prior generations.
