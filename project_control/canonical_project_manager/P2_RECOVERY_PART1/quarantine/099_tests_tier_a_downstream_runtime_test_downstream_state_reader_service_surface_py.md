# Reconstructed semantic receipt — `tests/tier_a/downstream_runtime/test_downstream_state_reader_service_surface.py`

- Sequence `099`, PM-015; test SHA-256 `6b3153b87c012f5deff9c6820f40de5732ceab8b4cd7988d57da881476ac97c0`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: repository paths, fixtures and standard-library helpers referenced directly by the test.
- Surviving decision summary: The service proves only top-level list detachment and receipt-string echo. It reads no position, capital or receipt repository and emits none of the admitted read-surface, truth/placeholder or reserved-concern evidence; the second constructor call labelled replay is not replay.

## Complete test restatement

- Lines `21-24` `test_downstream_state_reader_service_surface_is_present`: executes the named specimen/boundary and observes checks at lines `23, 24`. The exact assertions are enumerated in the relationship sections below.
- Lines `27-42` `test_downstream_state_reader_detaches_position_id_inputs`: executes the named specimen/boundary and observes checks at lines `29, 31, 41, 42`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_downstream_state_reader_service_surface_is_present`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_state_reader_service_surface.py:21-24`. Checks: L23 assert `state_reader.__name__ == "nvda_desk.downstream.state_reader"`; L24 assert `_require_attr(state_reader, "DownstreamStateService") is getattr(state_reader, "DownstreamStateService")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: The service proves only top-level list detachment and receipt-string echo. It reads no position, capital or receipt repository and emits none of the admitted read-surface, truth/placeholder or reserved-concern evidence; the second constructor call labelled replay is not replay.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_downstream_state_reader_detaches_position_id_inputs`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_state_reader_service_surface.py:27-42`. Checks: L29 assert `state_reader.__name__ == "nvda_desk.downstream.state_reader"`; L31 assert `service_class is getattr(state_reader, "DownstreamStateService")`; L41 assert `replay.snapshot.position_ids == ["pos-1"]`; L42 assert `result.receipt_id == "receipt-1"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: The service proves only top-level list detachment and receipt-string echo. It reads no position, capital or receipt repository and emits none of the admitted read-surface, truth/placeholder or reserved-concern evidence; the second constructor call labelled replay is not replay.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `2/2`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
