# Reconstructed semantic receipt — `tests/tier_a/downstream_runtime/test_fwd015_broker_execution_lifecycle_contract.py`

- Sequence `102`, PM-015; test SHA-256 `29177a8641a2a5cbeb4df5a6ae9d4acc612924e721ce2ad9568b79a8b0ba0682`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.api.app: create_app; nvda_desk.contracts.broker_execution: BrokerOrderIntent; nvda_desk.downstream.broker_execution: PaperBrokerExecutionService.
- Surviving decision summary: The test creates paper order/fill/position/account authority without a current normative owner; protocol flags and finite metadata tokens do not cure duplicate, zero-price, short-exposure or identity defects.

## Complete test restatement

- Lines `11-33` `test_paper_broker_order_contract_records_order_event_fill_position_and_account_state`: executes the named specimen/boundary and observes checks at lines `26, 27, 28, 29, 30, 31, 32, 33`. The exact assertions are enumerated in the relationship sections below.
- Lines `36-56` `test_broker_order_side_is_closed_and_execution_payloads_stay_offline`: executes the named specimen/boundary and observes checks at lines `37, 47`. The exact assertions are enumerated in the relationship sections below.
- Lines `59-86` `test_api_exposes_paper_broker_lifecycle_without_network_execution`: executes the named specimen/boundary and observes checks at lines `68, 81, 82, 83, 84, 85, 86`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_paper_broker_order_contract_records_order_event_fill_position_and_account_state`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd015_broker_execution_lifecycle_contract.py:11-33`. Checks: L26 assert `result.order_id == "order-1"`; L27 assert `result.status == "accepted"`; L28 assert `result.broker_protocol_only is True`; L29 assert `result.execution_allowed is False`; L30 assert `service.list_order_events().events[0].event_type == "paper_order_accepted"`; L31 assert `service.list_fill_events().fills[0].fill_price == 125.5`; L32 assert `service.list_positions().positions[0].quantity == 2`; L33 assert `service.get_account_state().cash_balance == 99_749.0`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The test creates paper order/fill/position/account authority without a current normative owner; protocol flags and finite metadata tokens do not cure duplicate, zero-price, short-exposure or identity defects.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `state_transition`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_broker_order_side_is_closed_and_execution_payloads_stay_offline`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd015_broker_execution_lifecycle_contract.py:36-56`. Checks: L37 raises `pytest.raises(ValidationError)`; L47 raises `pytest.raises(ValidationError, match="live_broker")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The test creates paper order/fill/position/account authority without a current normative owner; protocol flags and finite metadata tokens do not cure duplicate, zero-price, short-exposure or identity defects.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `boundary`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_api_exposes_paper_broker_lifecycle_without_network_execution`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd015_broker_execution_lifecycle_contract.py:59-86`. Checks: L68 assert `expected.issubset(app.route_handlers)`; L81 assert `result["status"] == "accepted"`; L82 assert `result["execution_allowed"] is False`; L83 assert `app.list_broker_order_events()[0]["order_id"] == "api-order-1"`; L84 assert `app.list_broker_fill_events()[0]["order_id"] == "api-order-1"`; L85 assert `app.list_broker_positions()[0]["symbol"] == "NVDA"`; L86 assert `app.get_broker_account_state()["account_id"] == "paper-account"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The test creates paper order/fill/position/account authority without a current normative owner; protocol flags and finite metadata tokens do not cure duplicate, zero-price, short-exposure or identity defects.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `3/3`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
