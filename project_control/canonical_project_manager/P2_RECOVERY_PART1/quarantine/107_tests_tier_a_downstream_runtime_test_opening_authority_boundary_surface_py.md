# Reconstructed semantic receipt — `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py`

- Sequence `107`, PM-015; test SHA-256 `09d3a6dfbcdebaef8ae4bfe236e689847b8e654e0cea32b6e6942f88b8983f9c`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.capital: CapitalDeploymentAuthorityAction, CapitalDeploymentDecision; nvda_desk.contracts.downstream: PlacementHandoffMaterial, PlacementReadinessInputTrace, PlacementReadinessResult; nvda_desk.downstream.opening: DownstreamOpeningService.
- Surviving decision summary: Exact protocol and false-authority flags are valid narrow clauses, but open preview payloads, unconstrained readiness states/handoffs and fabricated upstream capital/candidate truth materially underprove row 5.12.

## Complete test restatement

- Lines `37-43` `test_placement_trace_contract_rejects_non_protocol_broker_boundary_mode`: executes the named specimen/boundary and observes checks at lines `38`. The exact assertions are enumerated in the relationship sections below.
- Lines `46-52` `test_placement_handoff_contract_cannot_enable_execution`: executes the named specimen/boundary and observes checks at lines `47`. The exact assertions are enumerated in the relationship sections below.
- Lines `55-61` `test_placement_handoff_contract_must_remain_protocol_only`: executes the named specimen/boundary and observes checks at lines `56`. The exact assertions are enumerated in the relationship sections below.
- Lines `64-86` `test_placement_readiness_result_cannot_claim_broker_execution_or_resizing`: executes the named specimen/boundary and observes checks at lines `70, 79`. The exact assertions are enumerated in the relationship sections below.
- Lines `89-102` `test_opening_service_emits_protocol_only_non_executing_readiness_material`: executes the named specimen/boundary and observes checks at lines `97, 98, 99, 100, 101, 102`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_placement_trace_contract_rejects_non_protocol_broker_boundary_mode`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py:37-43`. Checks: L38 raises `pytest.raises(ValidationError, match="protocol_only")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Exact protocol and false-authority flags are valid narrow clauses, but open preview payloads, unconstrained readiness states/handoffs and fabricated upstream capital/candidate truth materially underprove row 5.12.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_placement_handoff_contract_cannot_enable_execution`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py:46-52`. Checks: L47 raises `pytest.raises(ValidationError, match="execution_allowed")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Exact protocol and false-authority flags are valid narrow clauses, but open preview payloads, unconstrained readiness states/handoffs and fabricated upstream capital/candidate truth materially underprove row 5.12.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_placement_handoff_contract_must_remain_protocol_only`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py:55-61`. Checks: L56 raises `pytest.raises(ValidationError, match="broker_protocol_only")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Exact protocol and false-authority flags are valid narrow clauses, but open preview payloads, unconstrained readiness states/handoffs and fabricated upstream capital/candidate truth materially underprove row 5.12.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G4 — `test_placement_readiness_result_cannot_claim_broker_execution_or_resizing`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py:64-86`. Checks: L70 raises `pytest.raises(ValidationError, match="broker_execution_opened")`; L79 raises `pytest.raises(ValidationError, match="capital_sizing_recomputed")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Exact protocol and false-authority flags are valid narrow clauses, but open preview payloads, unconstrained readiness states/handoffs and fabricated upstream capital/candidate truth materially underprove row 5.12.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G5 — `test_opening_service_emits_protocol_only_non_executing_readiness_material`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py:89-102`. Checks: L97 assert `result.input_trace.broker_boundary_mode == "protocol_only"`; L98 assert `result.broker_execution_opened is False`; L99 assert `result.capital_sizing_recomputed is False`; L100 assert `result.placement_handoff is not None`; L101 assert `result.placement_handoff.broker_protocol_only is True`; L102 assert `result.placement_handoff.execution_allowed is False`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Exact protocol and false-authority flags are valid narrow clauses, but open preview payloads, unconstrained readiness states/handoffs and fabricated upstream capital/candidate truth materially underprove row 5.12.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `5/5`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
