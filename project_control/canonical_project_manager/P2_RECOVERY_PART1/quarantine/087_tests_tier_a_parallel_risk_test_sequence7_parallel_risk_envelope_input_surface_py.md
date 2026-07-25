# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_input_surface.py`

- Sequence `087`, PM-014; test SHA-256 `cee0317c379eb9d5258b3bbc6f670fd0f99ae71eb02ca3ae9c21d868fabc3c23`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.options_flow: OptionsFlowContextInput; nvda_desk.contracts.parallel_risk: ParallelRiskPreparationPacket; nvda_desk.contracts.regime: MarketRegimeContextInput; nvda_desk.contracts.stage_inputs: StageInputBundle; nvda_desk.contracts.temporal: TemporalContextInput, TemporalEventWindow; nvda_desk.services.parallel_risk_lane_service: ParallelRiskLaneService.
- Surviving decision summary: Selected Stage Input Bundle primitives are genuinely carried, but the test validates only inner data, ignores required DMPV3 identity/lineage/validation, and its second specimen defaults missing trace/run/scenario while proving non-authority through seven payload-token absences.

## Complete test restatement

- Lines `44-62` `test_sequence7_bootstrap_input_carries_all_allowed_parallel_risk_primitives`: executes the named specimen/boundary and observes checks at lines `58, 59, 60, 61, 62`. The exact assertions are enumerated in the relationship sections below.
- Lines `65-86` `test_sequence7_bootstrap_input_excludes_downstream_decision_authority`: executes the named specimen/boundary and observes checks at lines `86`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_sequence7_bootstrap_input_carries_all_allowed_parallel_risk_primitives`

- Test locator: `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_input_surface.py:44-62`. Checks: L58 assert `payload_map["temporal_input"]["next_event_time_utc"] is not None`; L59 assert `payload_map["regime_input"]["vix_level"] == 31.0`; L60 assert `payload_map["options_flow_input"]["front_dte"] == 5`; L61 assert `payload_map["options_flow_input"]["next_dte"] == 1`; L62 assert `payload_map["bootstrap_source"] == "stage_input_bundle.parallel_risk_primitives"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Selected Stage Input Bundle primitives are genuinely carried, but the test validates only inner data, ignores required DMPV3 identity/lineage/validation, and its second specimen defaults missing trace/run/scenario while proving non-authority through seven payload-token absences.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_sequence7_bootstrap_input_excludes_downstream_decision_authority`

- Test locator: `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_input_surface.py:65-86`. Checks: L86 assert `token not in payload_text`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Selected Stage Input Bundle primitives are genuinely carried, but the test validates only inner data, ignores required DMPV3 identity/lineage/validation, and its second specimen defaults missing trace/run/scenario while proving non-authority through seven payload-token absences.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `token_only`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `2/2`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
