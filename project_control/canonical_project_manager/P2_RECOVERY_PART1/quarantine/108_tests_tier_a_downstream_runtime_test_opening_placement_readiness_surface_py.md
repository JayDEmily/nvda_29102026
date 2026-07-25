# Reconstructed semantic receipt — `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py`

- Sequence `108`, PM-015; test SHA-256 `818d3d2e8262e70ce7eaa4d24f52812d21b3247b6fac06e25a1d5cc8258b3598`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.capital: CapitalDeploymentAuthorityAction, CapitalDeploymentDecision; nvda_desk.contracts.downstream: PlacementHandoffMaterial; nvda_desk.downstream.opening: DownstreamOpeningService.
- Surviving decision summary: Useful local block, protocol and copy clauses remain, but fabricated upstream capital/candidate truth, weak identity/constraint validation, inconsistent readiness models and open preview aliases prevent Tier-A admission.

## Complete test restatement

- Lines `28-47` `test_opening_readiness_consumes_capital_decision_without_broker_execution`: executes the named specimen/boundary and observes checks at lines `38, 39, 40, 41, 42, 43, 44, 45, 46, 47`. The exact assertions are enumerated in the relationship sections below.
- Lines `50-62` `test_opening_readiness_blocks_non_continue_capital_decisions`: executes the named specimen/boundary and observes checks at lines `59, 60, 61, 62`. The exact assertions are enumerated in the relationship sections below.
- Lines `65-73` `test_opening_readiness_rejects_concrete_broker_boundary`: executes the named specimen/boundary and observes checks at lines `68`. The exact assertions are enumerated in the relationship sections below.
- Lines `76-84` `test_opening_readiness_requires_capital_deployment_receipt_id`: executes the named specimen/boundary and observes checks at lines `79, 84`. The exact assertions are enumerated in the relationship sections below.
- Lines `87-95` `test_opening_readiness_rejects_blank_serial_candidate_id`: executes the named specimen/boundary and observes checks at lines `90, 95`. The exact assertions are enumerated in the relationship sections below.
- Lines `98-113` `test_opening_readiness_blocks_continue_decision_with_zero_notional`: executes the named specimen/boundary and observes checks at lines `109, 110, 111, 112, 113`. The exact assertions are enumerated in the relationship sections below.
- Lines `116-133` `test_opening_readiness_detaches_placement_constraints_from_caller_list`: executes the named specimen/boundary and observes checks at lines `128, 129, 130`. The exact assertions are enumerated in the relationship sections below.
- Lines `136-146` `test_opening_readiness_protocol_handoff_rejects_broker_execution_fields`: executes the named specimen/boundary and observes checks at lines `141`. The exact assertions are enumerated in the relationship sections below.
- Lines `149-161` `test_opening_readiness_protocol_handoff_rejects_nested_broker_execution_preview`: executes the named specimen/boundary and observes checks at lines `154`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_opening_readiness_consumes_capital_decision_without_broker_execution`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:28-47`. Checks: L38 assert `result.readiness_state == "ready_for_protocol_handoff"`; L39 assert `result.input_trace.capital_deployment_receipt_id == "cap-receipt-001"`; L40 assert `result.input_trace.serial_candidate_id == "serial-candidate-001"`; L41 assert `result.input_trace.broker_boundary_mode == "protocol_only"`; L42 assert `result.broker_execution_opened is False`; L43 assert `result.capital_sizing_recomputed is False`; L44 assert `result.placement_handoff is not None`; L45 assert `result.placement_handoff.broker_protocol_only is True`; L46 assert `result.placement_handoff.execution_allowed is False`; L47 assert `result.placement_handoff.order_intent_preview["authorised_deployable_pct"] == 12.5`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Useful local block, protocol and copy clauses remain, but fabricated upstream capital/candidate truth, weak identity/constraint validation, inconsistent readiness models and open preview aliases prevent Tier-A admission.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_opening_readiness_blocks_non_continue_capital_decisions`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:50-62`. Checks: L59 assert `result.readiness_state == "blocked"`; L60 assert `result.placement_handoff is None`; L61 assert `"capital_deployment_action_block" in result.blocked_reasons`; L62 assert `"no_authorised_deployable_percentage" in result.blocked_reasons`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Useful local block, protocol and copy clauses remain, but fabricated upstream capital/candidate truth, weak identity/constraint validation, inconsistent readiness models and open preview aliases prevent Tier-A admission.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_opening_readiness_rejects_concrete_broker_boundary`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:65-73`. Checks: L68 raises `pytest.raises(ValueError, match="protocol_only")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Useful local block, protocol and copy clauses remain, but fabricated upstream capital/candidate truth, weak identity/constraint validation, inconsistent readiness models and open preview aliases prevent Tier-A admission.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G4 — `test_opening_readiness_requires_capital_deployment_receipt_id`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:76-84`. Checks: L79 raises `pytest.raises(ValueError)`; L84 assert `str(exc_info.value) == "placement readiness requires capital_deployment_receipt_id"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Useful local block, protocol and copy clauses remain, but fabricated upstream capital/candidate truth, weak identity/constraint validation, inconsistent readiness models and open preview aliases prevent Tier-A admission.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G5 — `test_opening_readiness_rejects_blank_serial_candidate_id`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:87-95`. Checks: L90 raises `pytest.raises(ValueError)`; L95 assert `str(exc_info.value) == "placement readiness requires serial_candidate_id"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Useful local block, protocol and copy clauses remain, but fabricated upstream capital/candidate truth, weak identity/constraint validation, inconsistent readiness models and open preview aliases prevent Tier-A admission.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G6 — `test_opening_readiness_blocks_continue_decision_with_zero_notional`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:98-113`. Checks: L109 assert `result.readiness_state == "blocked"`; L110 assert `result.placement_handoff is None`; L111 assert `result.broker_execution_opened is False`; L112 assert `result.capital_sizing_recomputed is False`; L113 assert `result.blocked_reasons == ["no_authorised_notional"]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Useful local block, protocol and copy clauses remain, but fabricated upstream capital/candidate truth, weak identity/constraint validation, inconsistent readiness models and open preview aliases prevent Tier-A admission.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G7 — `test_opening_readiness_detaches_placement_constraints_from_caller_list`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:116-133`. Checks: L128 assert `result.input_trace.placement_constraint_ids == ["limit-only", "day-session"]`; L129 assert `result.placement_handoff is not None`; L130 assert `result.placement_handoff.order_intent_preview["placement_constraint_ids"] == [ "limit-only", "day-session", ]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Useful local block, protocol and copy clauses remain, but fabricated upstream capital/candidate truth, weak identity/constraint validation, inconsistent readiness models and open preview aliases prevent Tier-A admission.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G8 — `test_opening_readiness_protocol_handoff_rejects_broker_execution_fields`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:136-146`. Checks: L141 raises `pytest.raises(ValidationError)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Useful local block, protocol and copy clauses remain, but fabricated upstream capital/candidate truth, weak identity/constraint validation, inconsistent readiness models and open preview aliases prevent Tier-A admission.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G9 — `test_opening_readiness_protocol_handoff_rejects_nested_broker_execution_preview`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:149-161`. Checks: L154 raises `pytest.raises(ValidationError, match="broker execution")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Useful local block, protocol and copy clauses remain, but fabricated upstream capital/candidate truth, weak identity/constraint validation, inconsistent readiness models and open preview aliases prevent Tier-A admission.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `9/9`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
