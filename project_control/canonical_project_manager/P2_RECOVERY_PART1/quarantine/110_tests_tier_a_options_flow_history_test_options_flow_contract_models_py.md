# Reconstructed semantic receipt — `tests/tier_a/options_flow_history/test_options_flow_contract_models.py`

- Sequence `110`, PM-015; test SHA-256 `6b9f90544d3eb0972e5cd42525737af6d8b4c76cc64bd11e36cb35a52aa56b3c`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: repository paths, fixtures and standard-library helpers referenced directly by the test.
- Surviving decision summary: Imports and exact class-name presence are structural observations only; no schema, stage, persistence, replay or authority behaviour is exercised.

## Complete test restatement

- Lines `21-30` `test_options_flow_contract_models_are_present`: executes the named specimen/boundary and observes checks at lines `23, 25, 27, 28, 29, 30`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_options_flow_contract_models_are_present [part A]`

- Test locator: `tests/tier_a/options_flow_history/test_options_flow_contract_models.py:21-27`. Checks: L23 assert `contracts.__name__ == "nvda_desk.contracts.options_flow"`; L25 assert `history_contracts.__name__ == "nvda_desk.contracts.options_flow_history"`; L27 assert `_require_attr(contracts, "OptionsFlowContextInput") is getattr(contracts, "OptionsFlowContextInput")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is useful regression/structure evidence, but it does not exercise enough governed semantics to become an authoritative proof relationship.
- What is not proved: Imports and exact class-name presence are structural observations only; no schema, stage, persistence, replay or authority behaviour is exercised.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `NON_AUTHORITATIVE_OBSERVATIONAL`.

## G2 — `test_options_flow_contract_models_are_present [part B]`

- Test locator: `tests/tier_a/options_flow_history/test_options_flow_contract_models.py:28-30`. Checks: L28 assert `_require_attr(contracts, "OptionsFlowContextOutput") is getattr(contracts, "OptionsFlowContextOutput")`; L29 assert `_require_attr(history_contracts, "OptionsFlowHistoryObservationRecord") is getattr(history_contracts, "OptionsFlowHistoryObservationRecord")`; L30 assert `_require_attr(history_contracts, "OptionsFlowHistoryWriteResult") is getattr(history_contracts, "OptionsFlowHistoryWriteResult")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is useful regression/structure evidence, but it does not exercise enough governed semantics to become an authoritative proof relationship.
- What is not proved: Imports and exact class-name presence are structural observations only; no schema, stage, persistence, replay or authority behaviour is exercised.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `NON_AUTHORITATIVE_OBSERVATIONAL`.

## File decision

- Assertion groups/relationships `2/2`; final `NON_AUTHORITATIVE_OBSERVATIONAL`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
