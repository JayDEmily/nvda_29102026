# Reconstructed semantic receipt — `tests/tier_a/persistence/test_capital_state_repository_surface.py`

- Sequence `118`, PM-015; test SHA-256 `fe5dc41ad8069cdbfe0c511878c94588dc53b6965fedbad92de0a9d555cdaae1`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.repositories.capital_state_repository: CapitalStateRepository.
- Surviving decision summary: Strong local process-memory copy/order/ID regressions, but arbitrary mappings and no typed owner, durability, version, transaction, idempotency or receipt semantics.

## Complete test restatement

- Lines `8-24` `test_capital_state_repository_rejects_duplicate_ids_and_preserves_copy_boundary`: executes the named specimen/boundary and observes checks at lines `15, 16, 19, 23`. The exact assertions are enumerated in the relationship sections below.
- Lines `27-35` `test_capital_state_repository_lists_snapshots_in_insertion_order`: executes the named specimen/boundary and observes checks at lines `35`. The exact assertions are enumerated in the relationship sections below.
- Lines `38-55` `test_capital_state_repository_reads_and_lists_identifier_records_copy_safely`: executes the named specimen/boundary and observes checks at lines `43, 47, 50`. The exact assertions are enumerated in the relationship sections below.
- Lines `58-68` `test_capital_state_repository_rejects_empty_id_and_duplicate_after_normalisation`: executes the named specimen/boundary and observes checks at lines `61, 65, 68`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_capital_state_repository_rejects_duplicate_ids_and_preserves_copy_boundary`

- Test locator: `tests/tier_a/persistence/test_capital_state_repository_surface.py:8-24`. Checks: L15 assert `readback == {"cash": 1000.0, "metadata": {"source": "seed"}}`; L16 assert `readback is not None`; L19 assert `repository.read_snapshot("cap-1") == { "cash": 1000.0, "metadata": {"source": "seed"}, }`; L23 raises `pytest.raises(ValueError, match="duplicate snapshot_id")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is useful regression/structure evidence, but it does not exercise enough governed semantics to become an authoritative proof relationship.
- What is not proved: Strong local process-memory copy/order/ID regressions, but arbitrary mappings and no typed owner, durability, version, transaction, idempotency or receipt semantics.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `NON_AUTHORITATIVE_OBSERVATIONAL`.

## G2 — `test_capital_state_repository_lists_snapshots_in_insertion_order`

- Test locator: `tests/tier_a/persistence/test_capital_state_repository_surface.py:27-35`. Checks: L35 assert `repository.list_snapshots() == [{"cash": 1000.0}, {"cash": 900.0}]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is useful regression/structure evidence, but it does not exercise enough governed semantics to become an authoritative proof relationship.
- What is not proved: Strong local process-memory copy/order/ID regressions, but arbitrary mappings and no typed owner, durability, version, transaction, idempotency or receipt semantics.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `NON_AUTHORITATIVE_OBSERVATIONAL`.

## G3 — `test_capital_state_repository_reads_and_lists_identifier_records_copy_safely`

- Test locator: `tests/tier_a/persistence/test_capital_state_repository_surface.py:38-55`. Checks: L43 assert `record == { "snapshot_id": "cap-1", "snapshot": {"cash": 1000.0, "metadata": {"source": "ledger"}}, }`; L47 assert `record is not None`; L50 assert `repository.list_snapshot_records() == [ { "snapshot_id": "cap-1", "snapshot": {"cash": 1000.0, "metadata": {"source": "ledger"}}, } ]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is useful regression/structure evidence, but it does not exercise enough governed semantics to become an authoritative proof relationship.
- What is not proved: Strong local process-memory copy/order/ID regressions, but arbitrary mappings and no typed owner, durability, version, transaction, idempotency or receipt semantics.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `NON_AUTHORITATIVE_OBSERVATIONAL`.

## G4 — `test_capital_state_repository_rejects_empty_id_and_duplicate_after_normalisation`

- Test locator: `tests/tier_a/persistence/test_capital_state_repository_surface.py:58-68`. Checks: L61 raises `pytest.raises(ValueError, match="snapshot_id must be non-empty")`; L65 raises `pytest.raises(ValueError, match="duplicate snapshot_id: cap-1")`; L68 assert `repository.read_snapshot(" cap-1 ") == {"cash": 1000.0}`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is useful regression/structure evidence, but it does not exercise enough governed semantics to become an authoritative proof relationship.
- What is not proved: Strong local process-memory copy/order/ID regressions, but arbitrary mappings and no typed owner, durability, version, transaction, idempotency or receipt semantics.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `NON_AUTHORITATIVE_OBSERVATIONAL`.

## File decision

- Assertion groups/relationships `4/4`; final `NON_AUTHORITATIVE_OBSERVATIONAL`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
