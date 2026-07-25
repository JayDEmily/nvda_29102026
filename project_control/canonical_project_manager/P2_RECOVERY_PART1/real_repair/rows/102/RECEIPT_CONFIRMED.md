# Semantic receipt — `tests/tier_a/downstream_runtime/test_fwd015_broker_execution_lifecycle_contract.py`

## File evidence

- Sequence `102`, unit `PM-015`; test SHA-256 `29177a8641a2a5cbeb4df5a6ae9d4acc612924e721ce2ad9568b79a8b0ba0682`.
- Full reads: test `1-86`; complete broker contracts `src/nvda_desk/contracts/broker_execution.py`; complete service `src/nvda_desk/downstream/broker_execution.py`; API route implementations; Broker Protocol P1 `P1-114`; architecture status `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:48-66`.
- Raw test result: `3 passed in 0.27s`.

## G1 — `test_paper_broker_order_contract_records_order_event_fill_position_and_account_state`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd015_broker_execution_lifecycle_contract.py:11-33`; one paper order immediately creates accepted order, fill, position and account-state changes.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP`; P1 `P1-114` governs protocol shape only and expressly states that no concrete operational writer, order placement or execution receipt authority is admitted. `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:64-66` does not authorise live or paper operation.
- Authority match: the tested lifecycle exceeds the reserved Broker Protocol boundary by owning acceptance, fills, positions and account mutation.
- Behaviour proved: the in-process service immediately fills one limit order at its limit price, updates one position and subtracts cash.
- Limitation: no authority owns this paper execution algorithm; duplicate order IDs, market orders at zero price, overselling/short exposure, fill identity, state transactionality, execution receipt semantics and durable replay are not proved.
- Adversarial challenge: submit a market buy that fills at `0.0`, reuse an order ID, or sell beyond the position; the test can remain green.
- Exact-surface falsifier: change the tested accepted status, event/fill/position values or cash result; an assertion at lines `26-33` must fail.
- Assertion that must fail and why: at test lines `26-33`, changing the order ID/status/boundary flags, first event type, first fill price, first position quantity or exact cash result breaks a direct assertion. Duplicate IDs, market-order price formation, overselling and durable state are not exercised.
- Semantic relation: `authority_missing`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; require a higher proposition admitting a bounded paper-execution owner and lifecycle semantics before behavioural repair/promotion.

## G2 — `test_broker_order_side_is_closed_and_execution_payloads_stay_offline`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd015_broker_execution_lifecycle_contract.py:36-56`; one invalid side and one exact metadata key are rejected.
- Authority locator: P1 `P1-114` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`.
- Authority match: closed protocol vocabulary and exclusion of live adapter credentials are lawful narrow protocol clauses, but they do not authorise paper order/fill execution.
- Behaviour proved: exact side `short` is outside the enum and exact nested `live_broker_adapter` is rejected.
- Limitation: aliases, other network/execution channels, operational side/position rules and the paper lifecycle remain ungoverned.
- Adversarial challenge: pass equivalent live authority under an unlisted alias or execute unlawful paper state behind false protocol flags.
- Exact-surface falsifier: accept `short` or exact `live_broker_adapter`; a `pytest.raises` assertion at lines `37-56` must fail.
- Assertion that must fail and why: at test lines `37-56`, adding `short` to the side enum or allowing the exact nested `live_broker_adapter` key makes the corresponding constructor succeed and fails `pytest.raises(ValidationError)`. Other live/network aliases and the operational paper lifecycle remain outside these two boundary cases.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; retain only as protocol-boundary evidence pending an admitted execution owner.

## G3 — `test_api_exposes_paper_broker_lifecycle_without_network_execution`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd015_broker_execution_lifecycle_contract.py:59-86`; five API methods are present and one sell request creates accepted event, fill, position and account outputs.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP`; the current architecture does not admit an operational paper broker/API writer.
- Authority match: false `execution_allowed` prevents a live-network claim but does not remove the API's ownership of paper order acceptance, fills, positions and account mutation.
- Behaviour proved: the application exposes and executes the five named in-process lifecycle methods.
- Limitation: route presence, authentication, idempotency, state isolation, market-price formation, account/position invariants, transactions and persistence are unproved.
- Adversarial challenge: mutate shared process state or fill market sells at zero while keeping `execution_allowed=False`; all assertions remain green.
- Exact-surface falsifier: remove one method or change the tested accepted/event/fill/position/account values; an assertion at lines `68-86` must fail.
- Assertion that must fail and why: at test lines `61-86`, removing any of the five named handlers breaks the subset assertion; changing the nominal API result, first order/fill ID, position symbol or account ID breaks a direct equality. False `execution_allowed` does not prevent this API from mutating in-process order, fill, position and cash state.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; no Tier A admission until API paper-operation authority is expressly established.

## File decision

- Groups/relationships: `3/3`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- The test establishes a concrete paper order/fill/position/account lifecycle beyond the currently admitted protocol-only boundary.
