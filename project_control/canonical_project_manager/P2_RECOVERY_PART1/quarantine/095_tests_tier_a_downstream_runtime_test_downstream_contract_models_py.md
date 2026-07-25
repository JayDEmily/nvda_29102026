# Reconstructed semantic receipt — `tests/tier_a/downstream_runtime/test_downstream_contract_models.py`

- Sequence `095`, PM-015; test SHA-256 `ad3d6e4eec49c281bc77721b7cd49c709688594b83f1bfaf6beade0775f264ef`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.downstream: DownstreamLiveInventorySnapshot, InventoryExposureState, InventoryStateReceipt, LiveCapitalState, LivePositionState.
- Surviving decision summary: Two exact top-level extra-key rejections and nested position/capital detachment are real, but live-inventory semantics are materially underconstrained: nested broker/execution keys, arbitrary policy-freeze text and mutually inconsistent live/position/exposure/capital/receipt identities are accepted.

## Complete test restatement

- Lines `30-56` `test_downstream_contract_models_are_present`: executes the named specimen/boundary and observes checks at lines `32, 34, 37, 40, 43, 46, 49, 50, 51, 54`. The exact assertions are enumerated in the relationship sections below.
- Lines `59-64` `test_live_inventory_contract_forbids_hidden_authority_fields`: executes the named specimen/boundary and observes checks at lines `60`. The exact assertions are enumerated in the relationship sections below.
- Lines `67-88` `test_live_inventory_contract_carries_position_capital_exposure_and_receipt`: executes the named specimen/boundary and observes checks at lines `86, 87, 88`. The exact assertions are enumerated in the relationship sections below.
- Lines `91-97` `test_inventory_state_receipt_rejects_broker_or_execution_authority_fields`: executes the named specimen/boundary and observes checks at lines `92`. The exact assertions are enumerated in the relationship sections below.
- Lines `100-125` `test_live_inventory_contracts_detach_nested_caller_owned_payload_state`: executes the named specimen/boundary and observes checks at lines `117, 121, 122`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_downstream_contract_models_are_present`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_contract_models.py:30-56`. Checks: L32 assert `contracts.__name__ == "nvda_desk.contracts.downstream"`; L34 assert `_require_attr(contracts, "DownstreamStateReadResult") is getattr( contracts, "DownstreamStateReadResult" )`; L37 assert `_require_attr(contracts, "DownstreamStateSnapshot") is getattr( contracts, "DownstreamStateSnapshot" )`; L40 assert `_require_attr(contracts, "DownstreamArchitectureReceipt") is getattr( contracts, "DownstreamArchitectureReceipt" )`; L43 assert `_require_attr(contracts, "DownstreamOpeningSnapshot") is getattr( contracts, "DownstreamOpeningSnapshot" )`; L46 assert `_require_attr(contracts, "DownstreamLiveInventorySnapshot") is getattr( contracts, "DownstreamLiveInventorySnapshot" )`; L49 assert `_require_attr(contracts, "LivePositionState") is getattr(contracts, "LivePositionState")`; L50 assert `_require_attr(contracts, "LiveCapitalState") is getattr(contracts, "LiveCapitalState")`; L51 assert `_require_attr(contracts, "InventoryExposureState") is getattr( contracts, "InventoryExposureState" )`; L54 assert `_require_attr(contracts, "InventoryStateReceipt") is getattr( contracts, "InventoryStateReceipt" )`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Two exact top-level extra-key rejections and nested position/capital detachment are real, but live-inventory semantics are materially underconstrained: nested broker/execution keys, arbitrary policy-freeze text and mutually inconsistent live/position/exposure/capital/receipt identities are accepted.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_live_inventory_contract_forbids_hidden_authority_fields`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_contract_models.py:59-64`. Checks: L60 raises `pytest.raises(ValidationError)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Two exact top-level extra-key rejections and nested position/capital detachment are real, but live-inventory semantics are materially underconstrained: nested broker/execution keys, arbitrary policy-freeze text and mutually inconsistent live/position/exposure/capital/receipt identities are accepted.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_live_inventory_contract_carries_position_capital_exposure_and_receipt`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_contract_models.py:67-88`. Checks: L86 assert `snapshot.policy_freeze_state == "architecture_only_no_policy"`; L87 assert `snapshot.capital_state is not None`; L88 assert `snapshot.exposure_state.declared_exposure_by_symbol == {"NVDA": 12.5}`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Two exact top-level extra-key rejections and nested position/capital detachment are real, but live-inventory semantics are materially underconstrained: nested broker/execution keys, arbitrary policy-freeze text and mutually inconsistent live/position/exposure/capital/receipt identities are accepted.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G4 — `test_inventory_state_receipt_rejects_broker_or_execution_authority_fields`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_contract_models.py:91-97`. Checks: L92 raises `pytest.raises(ValidationError)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Two exact top-level extra-key rejections and nested position/capital detachment are real, but live-inventory semantics are materially underconstrained: nested broker/execution keys, arbitrary policy-freeze text and mutually inconsistent live/position/exposure/capital/receipt identities are accepted.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G5 — `test_live_inventory_contracts_detach_nested_caller_owned_payload_state`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_contract_models.py:100-125`. Checks: L117 assert `snapshot.position_states[0].source_payload == { "symbol": "NVDA", "metadata": {"source": "fill"}, }`; L121 assert `snapshot.capital_state is not None`; L122 assert `snapshot.capital_state.source_payload == { "cash": 1000.0, "metadata": {"source": "ledger"}, }`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Two exact top-level extra-key rejections and nested position/capital detachment are real, but live-inventory semantics are materially underconstrained: nested broker/execution keys, arbitrary policy-freeze text and mutually inconsistent live/position/exposure/capital/receipt identities are accepted.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `5/5`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
