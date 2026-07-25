# Semantic receipt — `tests/tier_a/downstream_runtime/test_downstream_contract_models.py`

## File evidence

- Sequence `095`, unit `PM-015`; test SHA-256 `ad3d6e4eec49c281bc77721b7cd49c709688594b83f1bfaf6beade0775f264ef`.
- Full reads: test `1-125`; complete contract module `src/nvda_desk/contracts/downstream.py`; downstream operating law `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:95-103`; ownership law `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-195`; target live-inventory architecture `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`; P1 live-position/inventory adjudications in `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv`.
- Raw test result: `5 passed in 0.13s`.

## G1 — `test_downstream_contract_models_are_present`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_contract_models.py:30-56`; assertions import one module and require nine class attributes.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-354` and `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:152-195`.
- Authority match: the named opening, inventory and state-read concepts are governed architecture surfaces, but class presence alone does not prove their contracts or owner boundaries.
- Behaviour proved: the module imports and exposes the nine exact attribute names at test time.
- Limitation: schema fields, validation, lifecycle, consistency, lawful inputs/outputs, state reading and forbidden authority are not exercised.
- Adversarial challenge: replace every class with an empty placeholder retaining its name; all assertions remain green while every normative behaviour is absent.
- Exact-surface falsifier: remove or rename one required attribute; the corresponding assertion at lines `34-55` must fail.
- Assertion that must fail and why: at test lines `31-56`, making the module unimportable or deleting/renaming any of the nine required class exports triggers the helper failure or breaks the identity comparison. Empty placeholder classes with those names still satisfy every assertion in this group.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; replace or supplement presence checks with executable contract and boundary behaviour before Tier A admission.

## G2 — `test_live_inventory_contract_forbids_hidden_authority_fields`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_contract_models.py:59-64`; the constructor must reject one top-level `broker_order_id` extra field.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:347-353` and `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-181`.
- Authority match: rejecting broker-placement authority from a live-inventory snapshot is a lawful bounded clause of the prohibited-decision boundary.
- Behaviour proved: the model rejects that exact top-level field through its extra-field boundary.
- Limitation: nested or aliased broker/execution authority inside open `source_payload` mappings, indirect dependencies and side effects are not tested.
- Adversarial challenge: place `broker_order_id` or equivalent execution authority inside a nested position/capital payload; this assertion can remain green.
- Exact-surface falsifier: permit the top-level `broker_order_id` so construction succeeds; the `pytest.raises` assertion at lines `60-64` must fail.
- Assertion that must fail and why: at test lines `60-64`, allowing the undeclared top-level `broker_order_id` makes construction succeed and causes `pytest.raises(ValidationError)` to fail. The same key nested inside an open `source_payload`, or equivalent authority under an alias, is not challenged by this group.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; add recursive typed authority rejection and alias/indirect boundary proof.

## G3 — `test_live_inventory_contract_carries_position_capital_exposure_and_receipt`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_contract_models.py:67-88`; one snapshot is built and three selected fields/defaults are asserted.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354` and `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:95-103`.
- Authority match: position, capital, exposure and inventory-receipt carriers belong to the live-inventory architecture, but the authority requires truthful post-entry state rather than arbitrary caller-assembled consistency.
- Behaviour proved: the current models can carry the supplied position, capital, declared exposure and receipt objects and default the policy-freeze label.
- Limitation: the test does not require position/live-ID equality, receipt/inventory equality, receipt position coverage, capital snapshot identity, exposure derivation, execution/fill provenance, policy-freeze enumeration or repository source truth.
- Adversarial challenge: construct mutually inconsistent live IDs, position IDs, exposure IDs, receipt inventory ID and capital snapshot ID while preserving the three asserted values.
- Exact-surface falsifier: change the default policy-freeze label, drop capital state, or alter the declared exposure map; an assertion at lines `86-88` must fail.
- Assertion that must fail and why: at test lines `86-88`, changing the default freeze label, returning `None` for the supplied capital state, or changing the declared exposure map breaks one of the three assertions. Contradictory IDs among live positions, capital, exposure and receipt remain accepted because the test never compares them.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; require cross-object identity, provenance and exposure-consistency validators with negative tests.

## G4 — `test_inventory_state_receipt_rejects_broker_or_execution_authority_fields`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_contract_models.py:91-97`; one top-level `broker_order_id` must be rejected from the receipt.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:347-353` and `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-181`.
- Authority match: the receipt must not acquire broker execution authority; the exact top-level exclusion is a bounded clause.
- Behaviour proved: this exact undeclared field is rejected by the receipt model.
- Limitation: no receipt identity, position coverage, capital linkage, provenance or duplicate/replay semantics are tested.
- Adversarial challenge: emit a receipt with false inventory/position/capital identities and no extra broker field; the test remains green.
- Exact-surface falsifier: allow the top-level `broker_order_id`; the `pytest.raises` assertion at lines `92-97` must fail.
- Assertion that must fail and why: at test lines `92-97`, admitting the undeclared top-level `broker_order_id` makes the receipt constructor succeed and fails the expected `ValidationError`. False inventory, position or capital identities use declared fields and therefore remain outside this rejection test.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain the narrow exclusion but add executable receipt identity and provenance invariants.

## G5 — `test_live_inventory_contracts_detach_nested_caller_owned_payload_state`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_contract_models.py:100-125`; nested caller and intermediate-model mutations must not alter snapshot payloads.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354` and `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-181`.
- Authority match: copy isolation is a useful implementation invariant for preserved state, but it is only one clause of truthful live-inventory ownership.
- Behaviour proved: the snapshot deep-copies the tested nested position and capital payload structures at construction.
- Limitation: payload typing, authority provenance, subsequent model mutation, repository durability, transactionality and cross-object consistency remain unproved.
- Adversarial challenge: deep-copy arbitrary false or broker-authoritative payloads; the test passes although semantic state remains unlawful.
- Exact-surface falsifier: retain a shared nested reference so either mutation changes the snapshot; an equality assertion at lines `117-125` must fail.
- Assertion that must fail and why: at test lines `117-125`, retaining either caller-owned or intermediate-model nested dictionaries by reference lets one of the four mutations alter the snapshot and breaks the final position or capital payload equality. Deep-copying unlawful or semantically false payload content still passes.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; preserve copy isolation while replacing open mappings with governed typed carriers and consistency proof.

## File decision

- Groups/relationships: `5/5`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- The file contains narrow boundary and copy-isolation regressions, but materially underproves truthful live-inventory contract semantics and accepts inconsistent or nested-authority-bearing state.
