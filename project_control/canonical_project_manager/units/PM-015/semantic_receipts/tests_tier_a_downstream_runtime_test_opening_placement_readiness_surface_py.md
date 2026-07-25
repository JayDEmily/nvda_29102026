# Semantic receipt — `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py`

## File evidence

- Sequence `108`, unit `PM-015`; test SHA-256 `818d3d2e8262e70ce7eaa4d24f52812d21b3247b6fac06e25a1d5cc8258b3598`.
- Full reads: test `1-161`; complete `src/nvda_desk/downstream/opening.py:1-119`; opening contracts `src/nvda_desk/contracts/downstream.py:217-287`; capital decision `src/nvda_desk/contracts/capital.py:150-179`; row-5.12 authority `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`; working status `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:48-66`; P1 records `P1-110` through `P1-114`.
- Raw test result: `9 passed in 0.14s`.

## G1 — `test_opening_readiness_consumes_capital_decision_without_broker_execution`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:28-47`; one caller-built continue decision produces ready protocol handoff material.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`; P1 `Opening Architecture`, `Placement Readiness` and `Placement Handoff` records `P1-110`, `P1-112`, `P1-113`.
- Authority match: the local output shape and non-execution flags align with row 5.12, but truthful admitted capital/candidate inputs and complete constraints are not proved.
- Behaviour proved: the service copies the receipt/candidate IDs, returns ready state, false execution/resizing flags, protocol-only handoff and the asserted deployment percentage.
- Limitation: the test fabricates the capital decision with no `input_trace`; candidate identity is independently caller-authored; constraints are untyped; notional/percentage consistency, receipt authenticity and preview schema are unproved.
- Adversarial challenge: pass a forged continue decision and unrelated candidate while retaining positive numbers; every assertion remains green.
- Exact-surface falsifier: alter the asserted state, trace IDs, flags, handoff or percentage; an assertion at lines `38-47` must fail.
- Assertion that must fail and why: One or more assertions at lines `38-47` must fail if the positive path changes the readiness token, copied receipt/candidate IDs, protocol mode, prohibited booleans, handoff presence or copied percentage. The fixture itself is caller-authored and lacks a capital input trace, so the group confirms output copying and flags but cannot prove that the capital or candidate lineage was truthful.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; require admitted capital receipt/candidate lineage and typed constraints before promotion.

## G2 — `test_opening_readiness_blocks_non_continue_capital_decisions`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:50-63`; one block decision with zero values yields blocked state and two reasons.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:326-336`; P1 `Placement Readiness` record `P1-112`.
- Authority match: blocked readiness is governed, but the exact action/value-to-reason policy is implementation behaviour not fixed by the cited proposition.
- Behaviour proved: a `BLOCK` action prevents handoff and records action/percentage reasons for the tested zero values.
- Limitation: the zero-notional reason is not asserted here; duplicate or contradictory reasons, untyped constraints, forged decisions and identity mismatch remain untested.
- Adversarial challenge: return an incomplete reason set or use a fabricated block decision; the narrow assertions can still pass.
- Exact-surface falsifier: return ready state, emit a handoff or omit either asserted reason; an assertion at lines `59-63` must fail.
- Assertion that must fail and why: The assertions at lines `59-63` must expose a mutation that changes the tested block case to ready, emits a handoff, removes the action reason or removes the zero-percentage reason. They do not assert the simultaneously generated zero-notional reason or the completeness and ordering of the reason taxonomy, leaving broader policy defects green.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; govern and test the complete readiness policy and reason taxonomy.

## G3 — `test_opening_readiness_rejects_concrete_broker_boundary`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:65-73`; service invocation rejects `live_broker_adapter`.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:330-336`; P1 `Broker Protocol` record `P1-114`.
- Authority match: the current seam is protocol-only and concrete broker adapter implementation is explicitly outside row 5.12.
- Behaviour proved: the service rejects the exact concrete mode before building readiness material.
- Limitation: aliases or broker behaviour hidden in other fields are not examined.
- Adversarial challenge: pass broker-operational content under an unlisted constraint or preview alias while using `protocol_only`; this assertion does not detect it.
- Exact-surface falsifier: allow `live_broker_adapter`; the `pytest.raises` assertion at lines `68-73` must fail.
- Assertion that must fail and why: The `pytest.raises` context at lines `68-73` must fail if the service accepts the exact `live_broker_adapter` mode, because `_require_protocol_only_boundary` at implementation lines `45-47` would no longer raise. Broker-operational meaning carried under an allowed constraint or preview alias does not exercise this assertion.
- Semantic relation: `exact_full_proof`.
- Proof strength: `boundary`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain this exact protocol-only service boundary.

## G4 — `test_opening_readiness_requires_capital_deployment_receipt_id`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:76-84`; absence of the capital receipt ID is rejected with an exact message.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:330-336`; P1 `Placement Readiness` record `P1-112`.
- Authority match: placement readiness must consume capital-authority output, so a named capital receipt is a bounded required lineage clause.
- Behaviour proved: `None` receipt identity is rejected before readiness output.
- Limitation: whitespace is truthy and accepted; the ID is not resolved to a receipt; the decision may lack input trace and conflict with candidate truth.
- Adversarial challenge: provide a fabricated or whitespace receipt ID; the tested absence check no longer protects lineage.
- Exact-surface falsifier: permit a `None` receipt ID or change the exact failure path; an assertion at lines `79-84` must fail.
- Assertion that must fail and why: The exception context and exact message assertion at lines `79-84` must fail if a decision with `capital_deployment_receipt_id=None` proceeds or raises by a different route. The implementation checks truthiness only at lines `57-59`; whitespace and fabricated identifiers still satisfy it and are never resolved against receipt evidence.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain the requirement but normalise, resolve and cross-check the receipt identity.

## G5 — `test_opening_readiness_rejects_blank_serial_candidate_id`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:87-95`; whitespace candidate identity is rejected.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:330-336`; P1 `Placement Readiness` record `P1-112`.
- Authority match: candidate identity is a lawful input and the nonblank boundary is a valid bounded clause.
- Behaviour proved: the service strips for validation and rejects an all-whitespace candidate ID.
- Limitation: a nonblank ID is not resolved or linked to the capital decision; the unstripped original value is stored when nonblank whitespace surrounds it.
- Adversarial challenge: pass a nonblank but unrelated candidate identifier; the tested assertion does not establish identity truth.
- Exact-surface falsifier: accept the all-whitespace candidate; the `pytest.raises` assertion at lines `90-95` must fail.
- Assertion that must fail and why: The exception context and message assertion at lines `90-95` must fail if the service accepts an all-whitespace candidate ID, because implementation lines `60-61` explicitly strip only for that rejection. A nonblank but invented or unrelated ID remains accepted, and surrounding whitespace is retained in the emitted trace.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; preserve nonblank validation and add canonicalisation, resolution and cross-object identity checks.

## G6 — `test_opening_readiness_blocks_continue_decision_with_zero_notional`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:98-113`; a continue decision with positive percentage but zero notional is blocked.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:326-336`; P1 `Placement Readiness` record `P1-112`.
- Authority match: readiness may evaluate capital output, but the exact positive-notional rule and reason token are not specified by the higher proposition.
- Behaviour proved: zero notional suppresses handoff, preserves false prohibited flags and yields the exact one-item reason list.
- Limitation: percentage, notional, currency, price and quantity consistency and finite-value semantics are not tested; the capital decision remains fabricated.
- Adversarial challenge: provide an economically inconsistent positive notional and percentage; the test regards it as ready.
- Exact-surface falsifier: emit a handoff, set a prohibited flag or alter the exact reason list; an assertion at lines `109-113` must fail.
- Assertion that must fail and why: The assertions at lines `109-113` must fail if the zero-notional continue case becomes ready, emits a handoff, enables either prohibited authority flag or changes the exact one-item reason list. They do not test whether positive notional and percentage are economically coherent, finite, currency-consistent or backed by an authentic capital decision.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; govern economic readiness invariants and reason semantics.

## G7 — `test_opening_readiness_detaches_placement_constraints_from_caller_list`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:116-133`; caller-list mutation after the call does not change trace or preview lists.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:330-336`; placement constraints are lawful inputs, but copy semantics are not the full authority contract.
- Authority match: detachment is useful local boundary evidence, not proof that constraints are valid, complete or authoritative.
- Behaviour proved: the service copies the input list into both output locations for this case.
- Limitation: constraint entries are arbitrary strings with no schema, uniqueness, ordering law, source identity or cross-copy invariant after construction.
- Adversarial challenge: pass contradictory, duplicate or broker-operational constraint strings; copy isolation remains green.
- Exact-surface falsifier: retain the caller list by reference so the appended item appears in either output; an assertion at lines `128-133` must fail.
- Assertion that must fail and why: After the caller appends `mutated-after-call`, either equality at lines `128-133` must fail if the trace or preview retained the caller's list by reference. This proves detachment for one list instance; it does not validate the strings, prohibit duplicates or contradictions, establish provenance, or guarantee the two output copies remain coherent after later mutation.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `substitution`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain copy isolation after typed constraint authority is introduced.

## G8 — `test_opening_readiness_protocol_handoff_rejects_broker_execution_fields`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:136-146`; an undeclared top-level `broker_order_id` is rejected.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:330-336`; P1 `Placement Handoff` and `Broker Protocol` records `P1-113`, `P1-114`.
- Authority match: a concrete broker order ID is outside the handoff carrier; the model's `extra=forbid` enforces this exact top-level clause.
- Behaviour proved: the exact extra field cannot be added to the handoff model.
- Limitation: this test does not prove preview-content safety and does not assert the error cause; aliases remain possible.
- Adversarial challenge: put the same broker identity under an unlisted key inside `order_intent_preview`; this assertion does not detect it.
- Exact-surface falsifier: permit the exact top-level extra field; the `pytest.raises` assertion at lines `141-146` must fail.
- Assertion that must fail and why: The `pytest.raises` context at lines `141-146` must fail if the model accepts the undeclared top-level `broker_order_id`, because `extra="forbid"` is the tested rejection mechanism. The group neither checks the error cause nor constrains broker identity carried under a declared open-mapping field.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain as one exact schema boundary, not as complete handoff proof.

## G9 — `test_opening_readiness_protocol_handoff_rejects_nested_broker_execution_preview`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py:149-161`; recursive key scanning rejects nested exact `broker_order_id`.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:330-336`; P1 `Placement Handoff` and `Broker Protocol` records `P1-113`, `P1-114`.
- Authority match: excluding concrete broker-execution truth is authoritative; this test proves one exact nested-key guard.
- Behaviour proved: the current recursive validator rejects the tested hidden key.
- Limitation: the guard is a finite exact-key blacklist; aliases, values, encoded instructions and future broker fields pass.
- Adversarial challenge: rename the nested key to `broker_reference` or `submit_instruction`; validation succeeds.
- Exact-surface falsifier: allow the exact nested `broker_order_id`; the `pytest.raises` assertion at lines `154-161` must fail.
- Assertion that must fail and why: The `pytest.raises` context at lines `154-161` must fail if the recursive preview validator accepts the exact nested `broker_order_id` key, because contract lines `243-246` route that mapping through the finite broker-key guard. Renamed keys, values encoding submission instructions and future broker fields remain admissible in the open preview mapping.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain the regression while replacing open preview mappings with a typed adapter-neutral contract.

## File decision

- Groups/relationships: `9/9`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Useful protocol, non-execution, identity-presence and copy clauses remain, but fabricated upstream truth, untyped constraints, weak cross-object identity and open preview aliases prevent Tier-A acceptance.
