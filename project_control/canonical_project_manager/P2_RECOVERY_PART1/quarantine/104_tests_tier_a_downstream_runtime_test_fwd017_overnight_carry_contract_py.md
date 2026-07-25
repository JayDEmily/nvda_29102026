# Reconstructed semantic receipt — `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py`

- Sequence `104`, PM-015; test SHA-256 `6eceb47ddfa298b45bb4121a3a2a65c77118a7b2aedf769fd3c09c65d40f65ba`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.api.app: create_app; nvda_desk.contracts.exit_close: ExitCloseInputTrace; nvda_desk.downstream.exit_close: evaluate_exit_close_policy; nvda_desk.downstream.overnight_carry: CarryHandoffService, OvernightCarryMarketService, OvernightCarryReplayService.
- Surviving decision summary: Carry handoff, overnight recommendation thresholds, next-open fallback, replay label and API surface lack a governing proposition; API fabricates upstream receipt IDs and numeric/action invariants are incomplete.

## Complete test restatement

- Lines `24-44` `test_carry_handoff_builds_lifecycle_limited_action_envelope_with_open_fallback`: executes the named specimen/boundary and observes checks at lines `40, 41, 42, 43, 44`. The exact assertions are enumerated in the relationship sections below.
- Lines `47-70` `test_market_carry_evaluation_applies_handoff_envelope_and_derives_vwap_distance`: executes the named specimen/boundary and observes checks at lines `67, 68, 69, 70`. The exact assertions are enumerated in the relationship sections below.
- Lines `73-92` `test_carry_replay_compares_market_evaluation_against_next_session_reference`: executes the named specimen/boundary and observes checks at lines `90, 91, 92`. The exact assertions are enumerated in the relationship sections below.
- Lines `95-116` `test_api_exposes_overnight_carry_dependency_surfaces`: executes the named specimen/boundary and observes checks at lines `105, 115, 116`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_carry_handoff_builds_lifecycle_limited_action_envelope_with_open_fallback`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py:24-44`. Checks: L40 assert `handoff.position_id == "position-1"`; L41 assert `handoff.horizon == "overnight"`; L42 assert `handoff.allowed_actions == ("hold", "trim")`; L43 assert `handoff.next_session_open_utc == "2026-05-18T13:30:00Z"`; L44 assert `handoff.execution_allowed is False`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Carry handoff, overnight recommendation thresholds, next-open fallback, replay label and API surface lack a governing proposition; API fabricates upstream receipt IDs and numeric/action invariants are incomplete.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_market_carry_evaluation_applies_handoff_envelope_and_derives_vwap_distance`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py:47-70`. Checks: L67 assert `output.recommendation == "trim"`; L68 assert `output.close_distance_to_vwap_pct == 5.0`; L69 assert `output.scalar_context["vix_close"] == 22.0`; L70 assert `output.execution_allowed is False`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Carry handoff, overnight recommendation thresholds, next-open fallback, replay label and API surface lack a governing proposition; API fabricates upstream receipt IDs and numeric/action invariants are incomplete.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_carry_replay_compares_market_evaluation_against_next_session_reference`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py:73-92`. Checks: L90 assert `replay.path_summary["open_gap_pct"] == 3.0`; L91 assert `replay.path_summary["close_to_close_pct"] == 1.0`; L92 assert `replay.runtime_mutated is False`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Carry handoff, overnight recommendation thresholds, next-open fallback, replay label and API surface lack a governing proposition; API fabricates upstream receipt IDs and numeric/action invariants are incomplete.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `replay`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G4 — `test_api_exposes_overnight_carry_dependency_surfaces`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py:95-116`. Checks: L105 assert `expected.issubset(app.route_handlers)`; L115 assert `result["recommendation"] in {"hold", "trim", "close"}`; L116 assert `result["execution_allowed"] is False`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Carry handoff, overnight recommendation thresholds, next-open fallback, replay label and API surface lack a governing proposition; API fabricates upstream receipt IDs and numeric/action invariants are incomplete.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `4/4`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
