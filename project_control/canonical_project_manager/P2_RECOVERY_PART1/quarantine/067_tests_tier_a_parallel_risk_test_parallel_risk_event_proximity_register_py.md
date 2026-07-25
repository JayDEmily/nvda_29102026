# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_event_proximity_register.py`

- Sequence `067`, PM-014; test SHA-256 `7c07eece384e09b5dd1056939623827701868b5d321ee5da289fad9488d0fe74`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.calendar.operational.events: MarketEventDTO, OperationalEventRepository, RuntimeCalendarQuery; nvda_desk.domain.parallel_risk.event_proximity: event_proximity_entries_from_calendar_snapshot.
- Surviving decision summary: manual_receipt_complete_projection_specimen_but_four_layer_identity_and_policy_missing_token_non_authority_and_empty_source_collapses_unknown_completeness

## Complete test restatement

- Lines `15-55` `test_event_proximity_register_projects_calendar_matches_without_trade_authority`: executes the named specimen/boundary and observes checks at lines `42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55`. The exact assertions are enumerated in the relationship sections below.
- Lines `58-71` `test_event_proximity_register_returns_empty_entries_when_no_calendar_matches`: executes the named specimen/boundary and observes checks at lines `71`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_event_proximity_register_projects_calendar_matches_without_trade_authority [part A]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_event_proximity_register.py:15-48`. Checks: L42 assert `len(entries) == 1`; L44 assert `entry.event_id == "earnings-nvda"`; L45 assert `entry.proximity_seconds == 1200`; L46 assert `entry.materiality == "high"`; L47 assert `entry.materiality_rank == 3`; L48 assert `entry.runtime_tags == ["earnings", "scheduled_event_window_active"]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_projection_specimen_but_four_layer_identity_and_policy_missing_token_non_authority_and_empty_source_collapses_unknown_completeness
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_event_proximity_register_projects_calendar_matches_without_trade_authority [part B]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_event_proximity_register.py:49-55`. Checks: L49 assert `entry.evaluation_tags == ["earnings", "scheduled_event_window_active"]`; L50 assert `entry.source_refs == ["calendar-ref-1"]`; L51 assert `entry.risk_interpretation == "event_proximity_state_of_play_only"`; L53 assert `"buy" not in payload`; L54 assert `"sell" not in payload`; L55 assert `"order" not in payload`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_projection_specimen_but_four_layer_identity_and_policy_missing_token_non_authority_and_empty_source_collapses_unknown_completeness
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `token_only`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_event_proximity_register_returns_empty_entries_when_no_calendar_matches`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_event_proximity_register.py:58-71`. Checks: L71 assert `event_proximity_entries_from_calendar_snapshot(snapshot) == []`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_projection_specimen_but_four_layer_identity_and_policy_missing_token_non_authority_and_empty_source_collapses_unknown_completeness
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `3/3`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
