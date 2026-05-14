# 2026-04-22 Temporal Standard Tranche 3 Code and Persistence Remediation Report

## Status

- tranche branch: `work/temporal-standard-tranche-3-code-persistence-remediation-20260422`
- baseline branch verified from input zip: `work/temporal-standard-tranche-2-conformance-audit-proof-remediation-20260422`
- baseline commit: `1d487abd4cd5b5cbc5a5ec98d20ce24a5ce1cdc2`
- authoritative baseline ref: `temporal-standard-tranche-2-authoritative-closeout-20260422`
- current tranche state: authoritative closeout created on the unmerged tranche branch
- closeout ref name recorded for tracked receipts: `temporal-standard-tranche-3-authoritative-closeout-20260422`

## Tranche boundary

This tranche is code, persistence, harness, and coupled-proof remediation for the exact deferred set only.
This tranche does not widen unfinished Module 8 Stage B, Module 8 Stage C, Module 9, Module 10, or Module 11 behaviour.
This tranche does not rewrite normative documents.

## L1 scope declarations

### Exact deferred source surfaces to remediate

- `src/nvda_desk/preparation/runtime_preparer.py`
- `src/nvda_desk/cognition/ingress/temporal_mapper.py`
- `src/nvda_desk/cognition/ingress/translator.py`
- `src/nvda_desk/contracts/stage_inputs.py`
- `src/nvda_desk/contracts/parallel_risk.py`
- `src/nvda_desk/services/parallel_risk_lane_service.py`
- `src/nvda_desk/risk/parallel/evaluate.py`
- `src/nvda_desk/domain/parallel_risk/environment_assessment.py`
- `src/nvda_desk/persistence/parallel_risk_observations.py`
- `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py`
- `src/nvda_desk/runtime/orchestrator.py`
- `src/nvda_desk/domain/temporal/event_windows.py`
- `src/nvda_desk/domain/temporal/session_clock.py`
- `src/nvda_desk/contracts/temporal.py`

### Exact target temporal fields and concepts to remediate

- `src/nvda_desk/preparation/runtime_preparer.py` -> replace module-local preparation fields (`observed_at`, `next_event_at`, `aligned_bar_at`, `bar_at`) with admitted source temporal fields plus `runtime_bar_time_utc`; separate source observation time from packet emission and persistence timing.
- `src/nvda_desk/cognition/ingress/temporal_mapper.py` -> consume only admitted source temporal fields; emit `TemporalContextInput` and `TemporalEventWindow` using `source_time_utc`, `source_date`, `next_event_time_utc`, `window_start_utc`, and `window_end_utc`.
- `src/nvda_desk/cognition/ingress/translator.py` -> keep the stage-input translation seam bound to the remediated temporal carrier without reintroducing legacy temporal grammar.
- `src/nvda_desk/contracts/stage_inputs.py` -> keep the admitted `TemporalContextInput` bundle carrier as the only temporal contract at the ingress-to-runtime seam.
- `src/nvda_desk/contracts/parallel_risk.py` -> replace local temporal grammar (`observed_at`, `next_event_at`, `recorded_at`) with the admitted source temporal standard and keep packet emission time distinct.
- `src/nvda_desk/services/parallel_risk_lane_service.py` -> keep the packet emission-time carrier distinct from source temporal fields carried inside `StageInputBundle.temporal`.
- `src/nvda_desk/risk/parallel/evaluate.py` -> preserve source temporal payload inside the evaluation path while keeping packet `time` as packet emission time.
- `src/nvda_desk/domain/parallel_risk/environment_assessment.py` -> emit the admitted source temporal fields and `next_event_time_utc` into the environment assessment surface.
- `src/nvda_desk/persistence/parallel_risk_observations.py` -> separate source temporal provenance from `persisted_at_utc` in the append-only observation record.
- `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py` -> preserve workbook mixed-date provenance truthfully with `source_date`; do not fabricate a false single observation timestamp.
- `src/nvda_desk/runtime/orchestrator.py` -> derive trace/run tokens from admitted source time and keep packet `time` as packet emission time.
- `src/nvda_desk/domain/temporal/event_windows.py` -> replace `starts_at`/`ends_at` grammar with `window_start_utc`/`window_end_utc` and expose `next_event_time_utc`.
- `src/nvda_desk/domain/temporal/session_clock.py` -> classify runtime session state from admitted `source_time_utc`.
- `src/nvda_desk/contracts/temporal.py` -> admit one canonical source temporal contract only; no compatibility aliases or legacy-key coercion.

### Exact coupled proof files to update

- `tests/tier_a/parallel_risk/test_parallel_risk_contract_models.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_evaluation_surface.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py`
- `tests/tier_a/runtime/test_runtime_orchestrator_surface.py`
- `tests/tier_a/runtime/test_serial_stage_packet_emission_surface.py`
- `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_emission_surface.py`
- `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py`
- `tests/tier_a/persistence/test_parallel_risk_observation_store_surface.py`

### Workbook anti-drift ownership references used in this report

No workbook sheet names or row numbers are cited in this report as governing temporal-law authority.
The workbook was read in full as the live audit ledger only.

### Vocabulary gate decisions

Already governed from Tranche 1 and reused lawfully:

- `source_time_raw`
- `source_time_kind`
- `source_timezone_raw`
- `source_time_utc`
- `source_date`
- `captured_at_utc`
- `persisted_at_utc`
- `source_provider`
- `source_channel`
- `time_granularity`

New durable tranche-3 terms required by the remediation:

- `next_event_time_utc`
- `window_start_utc`
- `window_end_utc`
- `runtime_bar_time_utc`

Admission surfaces updated in this tranche:

- `src/nvda_desk/vocabulary_builder.py`
- `data/vocabulary/canonical_vocabulary.json`
- `data/vocabulary/vocabulary_touch_stamp.json`
- `var/vocabulary/synonym_candidates.json`

## Diff usage decision

The surviving patch file was used as directional evidence only.
It was not applied verbatim because the interim handoff records that the surviving code still contains compatibility aliases and legacy-key coercion and that no proof-file edits survive.
The final tranche rewrite therefore preserved the useful field-name direction from the patch while discarding the compatibility layer and rebuilding the proof and receipt surfaces directly on the tranche-2 baseline.

## Exact source surfaces remediated

### Deferred source surfaces with textual delta in this tranche

- `src/nvda_desk/preparation/runtime_preparer.py`
- `src/nvda_desk/cognition/ingress/temporal_mapper.py`
- `src/nvda_desk/contracts/parallel_risk.py`
- `src/nvda_desk/domain/parallel_risk/environment_assessment.py`
- `src/nvda_desk/persistence/parallel_risk_observations.py`
- `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py`
- `src/nvda_desk/runtime/orchestrator.py`
- `src/nvda_desk/domain/temporal/event_windows.py`
- `src/nvda_desk/domain/temporal/session_clock.py`
- `src/nvda_desk/contracts/temporal.py`

### Deferred source surfaces inspected in full and carried by adjacent contract rewrites without textual delta

- `src/nvda_desk/cognition/ingress/translator.py`
- `src/nvda_desk/contracts/stage_inputs.py`
- `src/nvda_desk/services/parallel_risk_lane_service.py`
- `src/nvda_desk/risk/parallel/evaluate.py`

These four deferred surfaces remained in the mandatory tranche set and were re-read after adjacent rewrites.
They require no textual delta because they now consume the remediated `TemporalContextInput` and parallel-risk carriers without asserting their own competing temporal grammar.
They are receipted here explicitly so none of the 14 deferred source surfaces is silently skipped.

## Exact proof surfaces remediated

### Deferred proof surfaces with textual delta in this tranche

- `tests/tier_a/parallel_risk/test_parallel_risk_contract_models.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_evaluation_surface.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py`
- `tests/tier_a/runtime/test_runtime_orchestrator_surface.py`
- `tests/tier_a/runtime/test_serial_stage_packet_emission_surface.py`
- `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_emission_surface.py`
- `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py`
- `tests/tier_a/persistence/test_parallel_risk_observation_store_surface.py`

## Exact unavoidable glue changes outside the deferred set

### Source glue

- `src/nvda_desk/services/temporal_context_service.py`

Reason: this service still constructs temporal-context outputs for active runtime consumers, so the serial-runtime rewrite could not remain truthful without aligning this one minimal glue surface to the admitted source temporal grammar.

### Proof glue

- `tests/tier_a/ingress/test_raw_bundle_loader_surface.py`
- `tests/tier_a/upstream_cognition/test_cognition_ingress_mapping_surfaces.py`
- `tests/tier_a/upstream_cognition/test_cognition_ingress_translation_coordinator.py`
- `tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py`

Reason: these proofs sit directly on the active preparation-to-ingress seam and would otherwise keep asserting the pre-remediation temporal grammar despite the bounded contract rewrite.

## Scope-boundary confirmation

- unfinished modules remained out of scope
- Module 8 Stage B remained reserved
- Module 8 Stage C remained reserved
- Module 9 remained reserved
- Module 10 remained reserved
- Module 11 remained reserved
- no normative documents were rewritten in this tranche

## Leaf chronology

| Leaf | Purpose | Closing commit or authoritative ref |
|---|---|---|
| `L1-read-vocabulary-scope-and-remediation-declarations` | Read completion, vocabulary gate, exact deferred-surface declarations, brief copy | `29fe4e09986b3afe4b7ff6db8436e0cda7a0ccc2` |
| `L2-contract-and-preparation-temporal-remediation` | Canonical source temporal contract plus preparation and ingress remapping | `e8720d5bbbef3d5bae22b80e9ce721404e226f42` |
| `L3-parallel-risk-and-persistence-temporal-remediation` | Parallel-risk, persistence, and workbook specimen temporal remediation | `288cbb59e40291ff870371170915380c02807340` |
| `L4-serial-runtime-and-stage-packet-temporal-remediation` | Serial runtime and stage-packet temporal remediation | `6e2cfcaed309765e7377d1c3adeaf3e1a8d0b147` |
| `L5-coupled-proof-remediation` | Coupled proof updates for the remediated temporal grammar | `8f85f96a5a95d36f103b30818bd1511afbac7f67` |
| `L6-report-workbook-proof-and-clean-closeout` | Workbook reconciliation, exact proof rerun, clean closeout | `temporal-standard-tranche-3-authoritative-closeout-20260422` |

## Exact closeout proof outputs

### Full shell proof

Command:
`PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

Exact output:
```text
........................................................................ [ 56%]
.......................................................                  [100%]
127 passed in 7.04s
```

### Compile proof

Command:
`python -m compileall src`

Exact output:
```text
Listing 'src'...
Listing 'src/nvda_desk'...
Listing 'src/nvda_desk/adapters'...
Listing 'src/nvda_desk/adapters/egress'...
Listing 'src/nvda_desk/adapters/ingress'...
Listing 'src/nvda_desk/analysis'...
Listing 'src/nvda_desk/analysis/replay'...
Listing 'src/nvda_desk/api'...
Listing 'src/nvda_desk/api/http'...
Listing 'src/nvda_desk/calendar'...
Listing 'src/nvda_desk/calendar/operational'...
Listing 'src/nvda_desk/calendar/reference'...
Listing 'src/nvda_desk/capital'...
Listing 'src/nvda_desk/cognition'...
Listing 'src/nvda_desk/cognition/ingress'...
Listing 'src/nvda_desk/cognition/modifiers'...
Listing 'src/nvda_desk/cognition/serial'...
Listing 'src/nvda_desk/config'...
Listing 'src/nvda_desk/contracts'...
Listing 'src/nvda_desk/domain'...
Listing 'src/nvda_desk/domain/capital'...
Listing 'src/nvda_desk/domain/downstream'...
Listing 'src/nvda_desk/domain/eligibility'...
Listing 'src/nvda_desk/domain/execution'...
Listing 'src/nvda_desk/domain/final_risk'...
Listing 'src/nvda_desk/domain/options_flow'...
Listing 'src/nvda_desk/domain/parallel_risk'...
Listing 'src/nvda_desk/domain/posture'...
Listing 'src/nvda_desk/domain/regime'...
Listing 'src/nvda_desk/domain/temporal'...
Listing 'src/nvda_desk/downstream'...
Listing 'src/nvda_desk/entry'...
Listing 'src/nvda_desk/ingress'...
Listing 'src/nvda_desk/packets'...
Listing 'src/nvda_desk/persistence'...
Listing 'src/nvda_desk/persistence/migrations'...
Listing 'src/nvda_desk/preparation'...
Listing 'src/nvda_desk/reference'...
Listing 'src/nvda_desk/repositories'...
Listing 'src/nvda_desk/risk'...
Listing 'src/nvda_desk/risk/join'...
Listing 'src/nvda_desk/risk/parallel'...
Listing 'src/nvda_desk/runtime'...
Listing 'src/nvda_desk/schemas'...
Listing 'src/nvda_desk/services'...
Listing 'src/nvda_desk/testing'...
Listing 'src/nvda_desk/testing/harnesses'...
Listing 'src/scripts'...
```

## Final authoritative packaged state

- final authoritative closeout ref pattern: `temporal-standard-tranche-3-authoritative-closeout-20260422`
- final package target: clean unmerged tranche branch plus annotated closeout tag

## Supplementary raw-truth and specimen-regeneration reconciliation

### Supplementary baseline verification

- supplementary starting branch: `work/temporal-standard-tranche-3-code-persistence-remediation-20260422`
- supplementary starting HEAD: `c941fc92c01d86506c0166f9e618f2ae5c02894a`
- supplementary starting repo clean: `yes`
- pre-existing authoritative closeout ref present at supplementary start: `temporal-standard-tranche-3-authoritative-closeout-20260422`
- supplementary brief copy: `var/audit/briefs/temporal_standard_tranche_3_supplementary_brief_raw_truth_and_specimen_regeneration.md`

### Supplementary SL1 declarations before code

#### Exact files to change in this supplementary pass

- `src/nvda_desk/contracts/temporal.py`
- `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py`
- `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py`
- `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_emission_surface.py`
- `var/audit/2026-04-22_temporal_standard_tranche_3_code_persistence_remediation_report.md`
- `var/audit/nvda_running_audit_log.xlsx`

#### Exact checked-in specimen artefacts to regenerate

- `var/audit/specimens/module_8/stage_input_bundle.json`
- `var/audit/specimens/module_8/bootstrap_input_packet.json`
- `var/audit/specimens/module_8/stage_a_output_packet.json`
- `var/audit/specimens/module_8/append_only_observation_record.json`
- `var/audit/specimens/module_8/specimen_receipt.md`

#### Exact proof files to rerun and proof commands to execute

Narrow directly touched proof surfaces:

- `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py`
- `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_emission_surface.py`

Mandatory closeout proof commands:

- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
- `python -m compileall src`

#### Explicit supplementary execution statements

- `source_time_raw` will no longer be auto-fabricated from `source_time_utc` or `source_date`.
- stale checked-in Module 8 specimen artefacts under `var/audit/specimens/module_8/` will be regenerated from the remediated harness.
- no backward-compatibility shims, aliases, dual temporal grammars, `observed_at`, or `next_event_at` surfaces will be retained in the regenerated specimen set.

### Supplementary leaf sequence

- `SL1-read-scope-and-raw-truth-declarations`
- `SL2-source-time-raw-correction`
- `SL3-specimen-artefact-regeneration`
- `SL4-report-workbook-proof-and-clean-closeout`

### Supplementary exact source surfaces with textual delta

- `src/nvda_desk/contracts/temporal.py`
- `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py`

### Supplementary exact proof surfaces with textual delta

- `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py`
- `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_emission_surface.py`

### Supplementary regenerated checked-in specimen artefacts

- `var/audit/specimens/module_8/stage_input_bundle.json`
- `var/audit/specimens/module_8/bootstrap_input_packet.json`
- `var/audit/specimens/module_8/stage_a_output_packet.json`
- `var/audit/specimens/module_8/append_only_observation_record.json`
- `var/audit/specimens/module_8/specimen_receipt.md`

### Supplementary acceptance-gap closure evidence

- `source_time_raw` is no longer auto-fabricated by `build_source_temporal_payload`; surfaces without an explicitly preserved raw token now carry `null` truthfully.
- The regenerated checked-in Module 8 specimen set now uses the admitted temporal grammar with `source_date`, `source_time_raw`, `next_event_time_utc`, and `persisted_at_utc` where relevant.
- `observed_at` and `next_event_at` are no longer present anywhere under `var/audit/specimens/module_8/` after regeneration.
- No backward-compatibility aliases or dual specimen grammar were introduced in this supplementary pass.

### Supplementary leaf chronology

| Leaf | Purpose | Closing commit or authoritative ref |
|---|---|---|
| `SL1-read-scope-and-raw-truth-declarations` | Supplementary baseline verification, tracked brief copy, exact change/regeneration/proof declarations | `5bc4f6384e1613488dfebbfa575b05a2c09b1336` |
| `SL2-source-time-raw-correction` | Removed helper-side auto-fabrication of `source_time_raw` | `b8410c513e6dc5405a4ff9ab76fc2038e7f47982` |
| `SL3-specimen-artefact-regeneration` | Regenerated the checked-in Module 8 specimen set and tightened the coupled specimen proofs | `77ebc3375de68f5d96b71b5e6ccea9d04634d623` |
| `SL4-report-workbook-proof-and-clean-closeout` | Updated tracked receipts, reran proof, and recorded the supplementary authoritative closeout ref | `temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-raw-truth` |

### Supplementary exact proof outputs

#### Full shell proof

Command:
`PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

Exact output:
```text
........................................................................ [ 56%]
.......................................................                  [100%]
127 passed in 2.07s
```

#### Compile proof

Command:
`python -m compileall src`

Exact output:
```text
Listing 'src'...
Listing 'src/nvda_desk'...
Listing 'src/nvda_desk/adapters'...
Listing 'src/nvda_desk/adapters/egress'...
Listing 'src/nvda_desk/adapters/ingress'...
Listing 'src/nvda_desk/analysis'...
Listing 'src/nvda_desk/analysis/replay'...
Listing 'src/nvda_desk/api'...
Listing 'src/nvda_desk/api/http'...
Listing 'src/nvda_desk/calendar'...
Listing 'src/nvda_desk/calendar/operational'...
Listing 'src/nvda_desk/calendar/reference'...
Listing 'src/nvda_desk/capital'...
Listing 'src/nvda_desk/cognition'...
Listing 'src/nvda_desk/cognition/ingress'...
Listing 'src/nvda_desk/cognition/modifiers'...
Listing 'src/nvda_desk/cognition/serial'...
Listing 'src/nvda_desk/config'...
Listing 'src/nvda_desk/contracts'...
Listing 'src/nvda_desk/domain'...
Listing 'src/nvda_desk/domain/capital'...
Listing 'src/nvda_desk/domain/downstream'...
Listing 'src/nvda_desk/domain/eligibility'...
Listing 'src/nvda_desk/domain/execution'...
Listing 'src/nvda_desk/domain/final_risk'...
Listing 'src/nvda_desk/domain/options_flow'...
Listing 'src/nvda_desk/domain/parallel_risk'...
Listing 'src/nvda_desk/domain/posture'...
Listing 'src/nvda_desk/domain/regime'...
Listing 'src/nvda_desk/domain/temporal'...
Listing 'src/nvda_desk/downstream'...
Listing 'src/nvda_desk/entry'...
Listing 'src/nvda_desk/ingress'...
Listing 'src/nvda_desk/packets'...
Listing 'src/nvda_desk/persistence'...
Listing 'src/nvda_desk/persistence/migrations'...
Listing 'src/nvda_desk/preparation'...
Listing 'src/nvda_desk/reference'...
Listing 'src/nvda_desk/repositories'...
Listing 'src/nvda_desk/risk'...
Listing 'src/nvda_desk/risk/join'...
Listing 'src/nvda_desk/risk/parallel'...
Listing 'src/nvda_desk/runtime'...
Listing 'src/nvda_desk/schemas'...
Listing 'src/nvda_desk/services'...
Listing 'src/nvda_desk/testing'...
Listing 'src/nvda_desk/testing/harnesses'...
Listing 'src/scripts'...
```

### Supplementary authoritative closeout ref

Tracked receipts in this supplementary pass use:
`temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-raw-truth`

## Supplementary preparation / raw-bundle seam reconciliation

### Supplementary preparation/raw-bundle baseline verification

- blocked Tranche 4 attempt status: disregarded for execution purposes and not continued
- supplementary starting branch: `work/temporal-standard-tranche-3-code-persistence-remediation-20260422`
- supplementary starting HEAD: `2c9437ae92642d3213c88b81b65f2e2f19b5ba4b`
- supplementary starting repo clean: `yes`
- pre-existing authoritative closeout ref present at supplementary start: `temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-raw-truth`
- supplementary brief copy: `var/audit/briefs/temporal_standard_tranche_3_supplementary_preparation_raw_bundle_remediation_brief.md`

### Supplementary SL1 declarations before coding

#### Exact files to change in this supplementary pass

- `src/nvda_desk/ingress/raw_bundle_loader.py`
- `src/nvda_desk/preparation/runtime_preparer.py`
- `tests/tier_a/ingress/test_raw_bundle_loader_surface.py`
- `tests/tier_a/upstream_cognition/test_cognition_ingress_translation_coordinator.py`
- `tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py`
- `var/audit/2026-04-22_temporal_standard_tranche_3_code_persistence_remediation_report.md`
- `var/audit/nvda_running_audit_log.xlsx`

#### Exact proof files to change in this supplementary pass

- `tests/tier_a/ingress/test_raw_bundle_loader_surface.py`
- `tests/tier_a/upstream_cognition/test_cognition_ingress_translation_coordinator.py`
- `tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py`

#### Explicit supplementary execution statements

- the blocked Tranche 4 attempt is disregarded for execution purposes and is not continued
- this supplementary remediation starts from accepted Tranche 3 baseline `2c9437ae92642d3213c88b81b65f2e2f19b5ba4b`
- internal `observed_at` will be removed from the active preparation/raw-bundle seam
- no backward compatibility, alias, shim, or dual temporal grammar is allowed in the active seam

### Supplementary leaf sequence

- `SL1-read-scope-and-seam-declarations`
- `SL2-raw-bundle-provenance-remediation`
- `SL3-preparation-seam-remediation`
- `SL4-coupled-proof-and-receipt-remediation`
- `SL5-clean-closeout`

### Supplementary exact source surfaces with textual delta

- `src/nvda_desk/ingress/raw_bundle_loader.py`
- `src/nvda_desk/preparation/runtime_preparer.py`

### Supplementary exact proof surfaces with textual delta

- `tests/tier_a/ingress/test_raw_bundle_loader_surface.py`
- `tests/tier_a/upstream_cognition/test_cognition_ingress_translation_coordinator.py`
- `tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py`

### Supplementary preparation/raw-bundle seam correction evidence

- `RawBundleProvenance` no longer carries `observed_at`; the active internal provenance carrier now uses admitted canonical source temporal fields only.
- `_build_bundle(...)` now binds top-level provenance truth through `source_time_raw`, `source_time_kind`, `source_timezone_raw`, `source_time_utc`, `source_date`, `captured_at_utc`, `persisted_at_utc`, `source_provider`, `source_channel`, and `time_granularity` rather than `observed_at`.
- `_resolve_source_time_utc(...)` in `src/nvda_desk/preparation/runtime_preparer.py` no longer reads `bundle.provenance.observed_at`; it now reads `bundle.provenance.source_time_utc` with lawful section fallback only.
- `_resolve_source_date(...)` now reads canonical `bundle.provenance.source_date` before section fallback.
- `_combine_raw_sections(...)` now preserves canonical provenance fields from the active seam without inventing a legacy alias.
- Direct seam proofs now assert canonical raw-bundle time using `source_time_utc` rather than `observed_at`.
- No backward-compatibility alias, shim, or dual temporal grammar was introduced in the active seam.

### Supplementary leaf chronology

| Leaf | Purpose | Closing commit or authoritative ref |
|---|---|---|
| `SL1-read-scope-and-seam-declarations` | Supplementary baseline verification, tracked brief copy, exact change/proof declarations | `b701d13c4222f0f1e400ec1c8aa74c0fee4cad53` |
| `SL2-raw-bundle-provenance-remediation` | Removed internal `observed_at` from the active raw-bundle provenance carrier | `aec125b15484731663ed323e95debd65360317d4` |
| `SL3-preparation-seam-remediation` | Routed the preparation seam through canonical provenance fields only | `49ded5873948fdca7f3bb2d9a675487c31674703` |
| `SL4-coupled-proof-and-receipt-remediation` | Updated the direct seam proofs to assert canonical raw-bundle time | `58fdbab184f30c391b6ce76f5d0f4d0e14e4cf17` |
| `SL5-clean-closeout` | Updated tracked receipts, reran mandated proofs, and recorded the supplementary authoritative closeout ref | `temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-preparation-raw-bundle` |

### Supplementary exact proof outputs

#### Full shell proof

Command:
`PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

Exact output:
```text
........................................................................ [ 56%]
.......................................................                  [100%]
127 passed in 3.34s
```

#### Compile proof

Command:
`python -m compileall src`

Exact output:
```text
Listing 'src'...
Listing 'src/nvda_desk'...
Listing 'src/nvda_desk/adapters'...
Listing 'src/nvda_desk/adapters/egress'...
Listing 'src/nvda_desk/adapters/ingress'...
Listing 'src/nvda_desk/analysis'...
Listing 'src/nvda_desk/analysis/replay'...
Listing 'src/nvda_desk/api'...
Listing 'src/nvda_desk/api/http'...
Listing 'src/nvda_desk/calendar'...
Listing 'src/nvda_desk/calendar/operational'...
Listing 'src/nvda_desk/calendar/reference'...
Listing 'src/nvda_desk/capital'...
Listing 'src/nvda_desk/cognition'...
Listing 'src/nvda_desk/cognition/ingress'...
Listing 'src/nvda_desk/cognition/modifiers'...
Listing 'src/nvda_desk/cognition/serial'...
Listing 'src/nvda_desk/config'...
Listing 'src/nvda_desk/contracts'...
Listing 'src/nvda_desk/domain'...
Listing 'src/nvda_desk/domain/capital'...
Listing 'src/nvda_desk/domain/downstream'...
Listing 'src/nvda_desk/domain/eligibility'...
Listing 'src/nvda_desk/domain/execution'...
Listing 'src/nvda_desk/domain/final_risk'...
Listing 'src/nvda_desk/domain/options_flow'...
Listing 'src/nvda_desk/domain/parallel_risk'...
Listing 'src/nvda_desk/domain/posture'...
Listing 'src/nvda_desk/domain/regime'...
Listing 'src/nvda_desk/domain/temporal'...
Listing 'src/nvda_desk/downstream'...
Listing 'src/nvda_desk/entry'...
Listing 'src/nvda_desk/ingress'...
Listing 'src/nvda_desk/packets'...
Listing 'src/nvda_desk/persistence'...
Listing 'src/nvda_desk/persistence/migrations'...
Listing 'src/nvda_desk/preparation'...
Listing 'src/nvda_desk/reference'...
Listing 'src/nvda_desk/repositories'...
Listing 'src/nvda_desk/risk'...
Listing 'src/nvda_desk/risk/join'...
Listing 'src/nvda_desk/risk/parallel'...
Listing 'src/nvda_desk/runtime'...
Listing 'src/nvda_desk/schemas'...
Listing 'src/nvda_desk/services'...
Listing 'src/nvda_desk/testing'...
Listing 'src/nvda_desk/testing/harnesses'...
Listing 'src/scripts'...
```

### Supplementary authoritative closeout ref

Tracked receipts in this supplementary pass use:
`temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-preparation-raw-bundle`
