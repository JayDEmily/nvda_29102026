# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py`

- Sequence `071`, PM-014; test SHA-256 `17c4061336d249f87b27a1fd21d33f656210c7d6a38482e9adf795773b68fedd`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.options_flow: OptionsFlowContextInput; nvda_desk.contracts.regime: MarketRegimeContextInput; nvda_desk.contracts.stage_inputs: StageInputBundle; nvda_desk.contracts.temporal: TemporalContextInput, TemporalEventWindow; nvda_desk.runtime.orchestrator: DeskRuntimeOrchestrator.
- Surviving decision summary: manual_receipt_complete_temporal_boundary_and_input_trace_preserved_but_packet_occurrence_execution_identity_derivedfrom_and_hidden_state_proof_are_nonconforming

## Complete test restatement

- Lines `42-80` `test_parallel_risk_lane_service_runs_serial_runtime_boundary_path_without_hidden_state`: executes the named specimen/boundary and observes checks at lines `51, 52, 53, 54, 58, 59, 60, 63, 67, 70, 73, 74, 77, 80`. The exact assertions are enumerated in the relationship sections below.
- Lines `83-89` `test_parallel_risk_lane_service_fails_closed_on_temporal_packet_id_contract_mismatch`: executes the named specimen/boundary and observes checks at lines `88`. The exact assertions are enumerated in the relationship sections below.
- Lines `92-106` `test_parallel_risk_lane_service_records_serial_temporal_input_trace`: executes the named specimen/boundary and observes checks at lines `100, 101, 102, 103, 106`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_parallel_risk_lane_service_runs_serial_runtime_boundary_path_without_hidden_state [part A]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py:42-60`. Checks: L51 assert `set(result) == {"selected_stage_packets", "bootstrap_input_packet", "lane_packet"}`; L52 assert `set(result["selected_stage_packets"]) == {"temporal"}`; L53 assert `result["selected_stage_packets"]["temporal"].packet_id == temporal_packet_id`; L54 assert `result["bootstrap_input_packet"].packet_id == "dmp::parallel" "_risk::bootstrap_input::20260421T093100Z"`; L58 assert `result["bootstrap_input_packet"].lineage.parentids == [temporal_packet_id]`; L59 assert `result["bootstrap_input_packet"].lineage.dependencyids == [temporal_packet_id]`; L60 assert `result["bootstrap_input_packet"].lineage.derivedfrom == ( "parallel" "_risk_bootstrap_from_serial_runtime_temporal_packet" )`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_temporal_boundary_and_input_trace_preserved_but_packet_occurrence_execution_identity_derivedfrom_and_hidden_state_proof_are_nonconforming
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_parallel_risk_lane_service_runs_serial_runtime_boundary_path_without_hidden_state [part B] [part A]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py:63-73`. Checks: L63 assert `result["bootstrap_input_packet"].data.bootstrap_source == "serial_runtime.stage_packets.temporal"`; L67 assert `[ window.event_id for window in result["bootstrap_input_packet"].data.temporal_input.windows ] == ["serial_boundary_window"]`; L70 assert `result["lane_packet"].data.environment_assessment.window_ids == [ "serial_boundary_window" ]`; L73 assert `result["lane_packet"].packet_id == "dmp::parallel" "_risk::output::20260421T093100Z"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_temporal_boundary_and_input_trace_preserved_but_packet_occurrence_execution_identity_derivedfrom_and_hidden_state_proof_are_nonconforming
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_parallel_risk_lane_service_runs_serial_runtime_boundary_path_without_hidden_state [part B] [part B]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py:74-80`. Checks: L74 assert `result["lane_packet"].lineage.parentids == [ "dmp::parallel" "_risk::bootstrap_input::20260421T093100Z" ]`; L77 assert `result["lane_packet"].lineage.dependencyids == [ "dmp::parallel" "_risk::bootstrap_input::20260421T093100Z" ]`; L80 assert `service.__dict__.keys() == {"_service"}`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_temporal_boundary_and_input_trace_preserved_but_packet_occurrence_execution_identity_derivedfrom_and_hidden_state_proof_are_nonconforming
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `presence_only`; file disposition `BLOCKED_P3_REPAIR`.

## G4 — `test_parallel_risk_lane_service_fails_closed_on_temporal_packet_id_contract_mismatch`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py:83-89`. Checks: L88 raises `pytest.raises(ValueError, match="serial_runtime_temporal_packet_id_contract_mismatch")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_temporal_boundary_and_input_trace_preserved_but_packet_occurrence_execution_identity_derivedfrom_and_hidden_state_proof_are_nonconforming
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G5 — `test_parallel_risk_lane_service_records_serial_temporal_input_trace`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py:92-106`. Checks: L100 assert `payload.input_trace.bootstrap_source == "serial_runtime.stage_packets.temporal"`; L101 assert `payload.input_trace.admitted_semantic_inputs == ["temporal_input"]`; L102 assert `payload.input_trace.selected_stage_packet_ids == [temporal_packet_id]`; L103 assert `payload.input_trace.bootstrap_input_packet_id == result["bootstrap_input_packet"].packet_id`; L106 assert `payload.input_trace.parent_packet_ids == [temporal_packet_id]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_temporal_boundary_and_input_trace_preserved_but_packet_occurrence_execution_identity_derivedfrom_and_hidden_state_proof_are_nonconforming
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `5/5`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
