# Reconstructed semantic receipt — `tests/tier_a/downstream_runtime/test_opening_transform_boundary_surface.py`

- Sequence `109`, PM-015; test SHA-256 `b0a0bc6b165e89094004b578a1201e6afd74de976fddc91df2c19f2758e2d21e`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.capital: CapitalDeploymentAuthorityAction, CapitalDeploymentDecision; nvda_desk.contracts.downstream: PlacementHandoffMaterial; nvda_desk.downstream.opening: DownstreamOpeningService.
- Surviving decision summary: Exact execution-token rejection and current five-key preview shape are supplemental evidence only; open preview aliases, fabricated upstream truth and one-file token scans do not prove the governed transform boundary.

## Complete test restatement

- Lines `53-67` `test_placement_handoff_rejects_execution_record_donor_payload_shape`: executes the named specimen/boundary and observes checks at lines `54`. The exact assertions are enumerated in the relationship sections below.
- Lines `70-81` `test_opening_service_preview_stays_in_native_handoff_shape`: executes the named specimen/boundary and observes checks at lines `78, 80, 81`. The exact assertions are enumerated in the relationship sections below.
- Lines `84-97` `test_opening_transform_boundary_does_not_import_execution_record_contracts`: executes the named specimen/boundary and observes checks at lines `96, 97`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_placement_handoff_rejects_execution_record_donor_payload_shape`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_transform_boundary_surface.py:53-67`. Checks: L54 raises `pytest.raises(ValidationError, match="execution record")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Exact execution-token rejection and current five-key preview shape are supplemental evidence only; open preview aliases, fabricated upstream truth and one-file token scans do not prove the governed transform boundary.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_opening_service_preview_stays_in_native_handoff_shape`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_transform_boundary_surface.py:70-81`. Checks: L78 assert `result.placement_handoff is not None`; L80 assert `set(preview) == ALLOWED_SERVICE_PREVIEW_KEYS`; L81 assert `not (set(_payload_keys(preview)) & FORBIDDEN_EXECUTION_RECORD_KEYS)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Exact execution-token rejection and current five-key preview shape are supplemental evidence only; open preview aliases, fabricated upstream truth and one-file token scans do not prove the governed transform boundary.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_opening_transform_boundary_does_not_import_execution_record_contracts`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_transform_boundary_surface.py:84-97`. Checks: L96 assert `"ExecutionRecord" not in imported_names`; L97 assert `"broker_execution_record" not in source`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Exact execution-token rejection and current five-key preview shape are supplemental evidence only; open preview aliases, fabricated upstream truth and one-file token scans do not prove the governed transform boundary.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `token_only`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `3/3`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
