# Reconstructed semantic receipt — `tests/tier_a/persistence/test_fwd003_durable_sql_contract.py`

- Sequence `120`, PM-015; test SHA-256 `a5c7357b7a5010de176623578f2e1a8851c7d1b681086dba2d30d88c4a2248a3`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.persistence.durable_sql: DurableSqliteStore, drift_for, high_pad_for, low_pad_for, volume_for.
- Surviving decision summary: Selected file-backed demo table/seed behaviour and four helper constants are real regressions, but Gate C reserves Tier-A authority for the bounded-demo/non-material-owner contract.

## Complete test restatement

- Lines `12-28` `test_durable_sql_store_creates_schema_and_seeds_bounded_dev_rows`: executes the named specimen/boundary and observes checks at lines `23, 24, 25, 26`. The exact assertions are enumerated in the relationship sections below.
- Lines `31-35` `test_durable_seed_helpers_are_deterministic`: executes the named specimen/boundary and observes checks at lines `32, 33, 34, 35`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_durable_sql_store_creates_schema_and_seeds_bounded_dev_rows`

- Test locator: `tests/tier_a/persistence/test_fwd003_durable_sql_contract.py:12-28`. Checks: L23 assert `bars[0]["symbol"] == "NVDA"`; L24 assert `bars[0]["close_price"] > bars[0]["open_price"]`; L25 assert `option_snapshots[0]["underlying_symbol"] == "NVDA"`; L26 assert `sessions == [ {"session_id": "2026-05-15", "trade_date": "2026-05-15", "session_state": "regular"} ]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is useful regression/structure evidence, but it does not exercise enough governed semantics to become an authoritative proof relationship.
- What is not proved: Selected file-backed demo table/seed behaviour and four helper constants are real regressions, but Gate C reserves Tier-A authority for the bounded-demo/non-material-owner contract.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `NON_AUTHORITATIVE_OBSERVATIONAL`.

## G2 — `test_durable_seed_helpers_are_deterministic`

- Test locator: `tests/tier_a/persistence/test_fwd003_durable_sql_contract.py:31-35`. Checks: L32 assert `drift_for(0) == 0.25`; L33 assert `high_pad_for(1) == 0.75`; L34 assert `low_pad_for(1) == 0.45`; L35 assert `volume_for(2) == 1200`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is useful regression/structure evidence, but it does not exercise enough governed semantics to become an authoritative proof relationship.
- What is not proved: Selected file-backed demo table/seed behaviour and four helper constants are real regressions, but Gate C reserves Tier-A authority for the bounded-demo/non-material-owner contract.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `NON_AUTHORITATIVE_OBSERVATIONAL`.

## File decision

- Assertion groups/relationships `2/2`; final `NON_AUTHORITATIVE_OBSERVATIONAL`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
