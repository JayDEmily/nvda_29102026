# Module 4 cognition ingress truth pass report

Date: 2026-04-21  
Brief: `module_4_cognition_ingress_implementation_brief_v2.md`  
Parent corrected Module 3 branch: `work/module-3-preparation-truth-pass-20260421`  
Parent corrected Module 3 HEAD: `cbb3c7f1016fc400ad65c25c48e32c56136ff6e3`  
Work branch: `work/module-4-cognition-ingress-truth-pass-20260421`

## Ordered leaf queue executed

1. `L1-vocabulary-admission-stage-input-bundle`
2. `L2-mapper-contract-hardening`
3. `L3-translator-runtime-boundary`
4. `L4-proof-report-closeout`
5. `L5-live-ledger-reconciliation-and-brief-storage`

## Closed leaf hashes

1. `L1-vocabulary-admission-stage-input-bundle` -> `2e72e8097316d89ce9366c52634abfb4a41c1a62`
2. `L2-mapper-contract-hardening` -> `733cc4d0d94154e1aeb8210e237c929ede51d417`
3. `L3-translator-runtime-boundary` -> `151d0f020b0daf81b45a1bbf982d3daf0c7c8cd0`
4. `L4-proof-report-closeout` -> `88a214fb0978162bd955e3b4482dc09b3d20c173`
5. `L5-live-ledger-reconciliation-and-brief-storage` -> `b0208a3b171b5073b2468752655de1a4f26b919b`

## Vocabulary admission gate

### Candidate-term decision

| Candidate term | Decision | Result |
|---|---|---|
| `StageInputBundle` | `add_new` | Admitted in `src/nvda_desk/vocabulary_builder.py` and regenerated into `data/vocabulary/canonical_vocabulary.json` as canonical slug `stage_input_bundle` mapped to contract `StageInputBundle`. |
| `Prepared substrate -> cognition ingress bundle` | `quarantine` | Workbook seam label only. Not promoted to canonical runtime vocabulary in this tranche. |
| `Prepared substrate -> regime input` | `quarantine` | Reservation-bearing workbook seam label only. Full ownership/completeness resolution remains out of scope under `TR-RS-001`. |
| `CognitionIngressTranslator` | `quarantine` | Implementation class symbol only. Not promoted to canonical durable vocabulary. |
| `build_temporal_input` | `quarantine` | Implementation function symbol only. Not promoted to canonical durable vocabulary. |
| `build_regime_input` | `quarantine` | Implementation function symbol only. Not promoted to canonical durable vocabulary. |
| `build_options_flow_input` | `quarantine` | Implementation function symbol only. Not promoted to canonical durable vocabulary. |
| `convert_snapshot` | `quarantine` | Implementation function symbol only. Not promoted to canonical durable vocabulary. |
| `TemporalContextInput` | `quarantine` | Existing contract class symbol only. Not newly admitted as canonical durable vocabulary in this tranche. |
| `MarketRegimeContextInput` | `quarantine` | Existing contract class symbol only. Not newly admitted as canonical durable vocabulary in this tranche. |
| `OptionsFlowContextInput` | `quarantine` | Existing contract class symbol only. Not newly admitted as canonical durable vocabulary in this tranche. |

### Vocabulary proof executed

1. `PYTHONPATH=src pytest -q tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py tests/tier_a/vocabulary/test_vocabulary_schema_contract.py tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py` -> `5 passed in 0.77s`

## Test-family and invariant gate

### Invariants checked

1. each stage input explicit
2. absent fields represented lawfully
3. deterministic mapping
4. no direct serial-runtime reach into preparation internals

### Test-family decision

| Family | Decision | Reason |
|---|---|---|
| `cognition_ingress_mapping_surfaces` | `re-author` | Existing assertions allowed fabricated wall-clock and zero-certainty defaults; the family now proves truthful absence and deterministic mapping. |
| `cognition_ingress_translation_coordinator` | `re-author` | Existing assertions accepted an untyped dict blob; the family now proves emission of the admitted typed carrier. |
| `runtime_orchestrator_surface` | `re-author` | The runtime consumer boundary now accepts the admitted typed carrier directly. |
| `regime_contract_models` | `preserve` | Contract family remains in scope and stays truthful after explicit-absence hardening. |
| `regime_ingress_surface` | `preserve` | Surface-presence blocker remains lawful and unchanged in role. |
| additional new test family | `defer` | No new family was required because the admitted bounded families already cover the Module 4 seam truthfully after re-authoring. |
| full regime completeness resolution | `defer` | Explicitly out of scope under reservation `TR-RS-001`. This tranche only makes incompleteness typed and explicit. |

## What changed

1. `src/nvda_desk/contracts/regime.py` and `src/nvda_desk/contracts/options_flow.py` now represent missing prepared values explicitly with nullable fields plus `missing_fields` rather than defaulting to zero-certainty.
2. `src/nvda_desk/cognition/ingress/temporal_mapper.py` now requires `observed_at` and rejects non-datetime temporal fields instead of falling back to wall-clock time.
3. `src/nvda_desk/cognition/ingress/regime_mapper.py` and `src/nvda_desk/cognition/ingress/options_mapper.py` now emit explicit missing-field state rather than fabricating numeric certainty.
4. `src/nvda_desk/contracts/stage_inputs.py` now defines the admitted typed seam carrier `StageInputBundle`.
5. `src/nvda_desk/cognition/ingress/translator.py` now emits `StageInputBundle` and remains the cognition-ingress-owned coordinator only.
6. `src/nvda_desk/runtime/orchestrator.py` now accepts `StageInputBundle` directly at the serial consumer boundary without reaching back into preparation internals.
7. The bounded Tier A families covering mapper truth, translator truth, and runtime-consumer truth were re-authored to match the tightened seam invariants.

## Required proof executed

1. Targeted Module 4 proof:
   - `PYTHONPATH=src pytest -q tests/tier_a/upstream_cognition/test_cognition_ingress_mapping_surfaces.py tests/tier_a/upstream_cognition/test_cognition_ingress_translation_coordinator.py tests/tier_a/upstream_cognition/test_regime_contract_models.py tests/tier_a/upstream_cognition/test_regime_ingress_surface.py tests/tier_a/runtime/test_runtime_orchestrator_surface.py` -> `10 passed in 0.43s`
2. Full proof floor:
   - `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` -> `111 passed in 2.17s`
3. Compile proof:
   - `python -m compileall src` -> clean

## Blockers

None.

## Out of scope remainder

1. raw bundle decode redesign
2. preparation redesign beyond the already-required seam adaptation
3. serial-stage reasoning deepening
4. DMPV3 expansion
5. parallel-risk hardening
6. capital deployment changes
7. downstream operations policy or review-policy redesign
8. settling final ownership of full regime completeness beyond explicit typed absence handling

## Branch state

This branch remains **unmerged**. Live-ledger reconciliation and brief storage are now reconciled on this same branch.
