# Reconstructed semantic receipt — `tests/tier_a/persistence/test_append_only_repository_surfaces.py`

- Sequence `117`, PM-015; test SHA-256 `94b0936c5ed3f1e172076285740476069ca6f6861e01668dc1b097a4d2e3aca1`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.repositories.execution_event_repository: ExecutionEventRepository; nvda_desk.repositories.market_observation_repository: MarketObservationRepository.
- Surviving decision summary: Two strong local memory order/copy regressions are retained, but a finite mutator-name blacklist does not prove append-only authority or typed/durable repository semantics.

## Complete test restatement

- Lines `7-20` `test_execution_event_repository_preserves_append_order_and_copy_boundary`: executes the named specimen/boundary and observes checks at lines `17`. The exact assertions are enumerated in the relationship sections below.
- Lines `23-36` `test_market_observation_repository_preserves_append_order_and_copy_boundary`: executes the named specimen/boundary and observes checks at lines `33`. The exact assertions are enumerated in the relationship sections below.
- Lines `39-64` `test_append_only_observation_repositories_do_not_expose_keyed_mutators`: executes the named specimen/boundary and observes checks at lines `64`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_execution_event_repository_preserves_append_order_and_copy_boundary`

- Test locator: `tests/tier_a/persistence/test_append_only_repository_surfaces.py:7-20`. Checks: L17 assert `repository.list_events() == [ {"event_id": "evt-1", "payload": {"stage": "submitted"}}, {"event_id": "evt-2", "payload": {"stage": "accepted"}}, ]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Two strong local memory order/copy regressions are retained, but a finite mutator-name blacklist does not prove append-only authority or typed/durable repository semantics.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_market_observation_repository_preserves_append_order_and_copy_boundary`

- Test locator: `tests/tier_a/persistence/test_append_only_repository_surfaces.py:23-36`. Checks: L33 assert `repository.list_observations() == [ {"observation_id": "obs-1", "payload": {"spot": 101.0}}, {"observation_id": "obs-2", "payload": {"spot": 102.0}}, ]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Two strong local memory order/copy regressions are retained, but a finite mutator-name blacklist does not prove append-only authority or typed/durable repository semantics.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_append_only_observation_repositories_do_not_expose_keyed_mutators`

- Test locator: `tests/tier_a/persistence/test_append_only_repository_surfaces.py:39-64`. Checks: L64 assert `public_methods.isdisjoint(prohibited_mutators)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Two strong local memory order/copy regressions are retained, but a finite mutator-name blacklist does not prove append-only authority or typed/durable repository semantics.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `3/3`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
