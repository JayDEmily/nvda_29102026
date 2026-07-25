# Semantic receipt — `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py`

## File evidence

- Sequence `107`, unit `PM-015`; test SHA-256 `09d3a6dfbcdebaef8ae4bfe236e689847b8e654e0cea32b6e6942f88b8983f9c`.
- Full reads: test `1-102`; opening contracts `src/nvda_desk/contracts/downstream.py:217-287`; complete implementation `src/nvda_desk/downstream/opening.py:1-119`; capital decision model `src/nvda_desk/contracts/capital.py:150-179`; row-5.12 authority `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`; working status `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:48-66`; P1 concepts `P1-110` through `P1-114`.
- Raw test result: `5 passed in 0.13s`.

## G1 — `test_placement_trace_contract_rejects_non_protocol_broker_boundary_mode`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py:37-43`; the trace rejects one non-protocol boundary value.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`; P1 `Placement Readiness` and `Broker Protocol` records `P1-112`, `P1-114`.
- Authority match: exact protocol-only broker context is the admitted boundary and concrete adapter operation is reserved.
- Behaviour proved: `PlacementReadinessInputTrace` rejects `live_broker_adapter` and accepts only the literal `protocol_only` mode.
- Limitation: receipt, candidate and constraint identifiers remain unvalidated strings; the trace does not authenticate the capital decision or candidate relationship.
- Adversarial challenge: use fabricated or whitespace lineage IDs while retaining `protocol_only`; construction succeeds.
- Exact-surface falsifier: permit `live_broker_adapter`; the `pytest.raises` assertion at lines `38-43` must fail.
- Assertion that must fail and why: The `pytest.raises` context at lines `38-43` must fail if `PlacementReadinessInputTrace` accepts `broker_boundary_mode="live_broker_adapter"`, because no `ValidationError` containing `protocol_only` would be produced. This directly tests the exact mode validator at contract lines `226-231`; it does not authenticate the receipt, candidate or constraint identifiers carried beside that mode.
- Semantic relation: `exact_full_proof`.
- Proof strength: `boundary`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain this exact protocol-mode invariant inside the repaired opening suite.

## G2 — `test_placement_handoff_contract_cannot_enable_execution`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py:46-52`; the handoff rejects `execution_allowed=True`.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`; P1 `Placement Handoff` record `P1-113`.
- Authority match: the handoff is explicitly non-executing and must remain distinct from broker submission and execution receipts.
- Behaviour proved: the model validator enforces a false execution flag.
- Limitation: a false flag does not prove that the open preview lacks broker authority or that downstream consumers cannot execute it; preview content remains an open mapping with finite key exclusions.
- Adversarial challenge: encode an executable instruction under an unlisted alias while leaving the flag false; validation succeeds.
- Exact-surface falsifier: allow `execution_allowed=True`; the `pytest.raises` assertion at lines `47-52` must fail.
- Assertion that must fail and why: The `pytest.raises` context at lines `47-52` must fail if the handoff model permits `execution_allowed=True`, because the exact false-only validator at contract lines `255-260` would no longer raise. The check is limited to that boolean; executable semantics hidden under an unlisted preview key remain outside the assertion.
- Semantic relation: `exact_full_proof`.
- Proof strength: `boundary`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain the exact false-execution invariant while strengthening payload semantics.

## G3 — `test_placement_handoff_contract_must_remain_protocol_only`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py:55-61`; the handoff rejects `broker_protocol_only=False`.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:330-336`; P1 records `P1-113` and `P1-114`.
- Authority match: the current handoff is an adapter-neutral protocol carrier and no operational broker writer is admitted.
- Behaviour proved: the model enforces the literal true protocol-only flag.
- Limitation: the flag is declarative and does not inspect preview semantics, dependency behaviour or route side effects.
- Adversarial challenge: carry concrete broker fields under renamed keys while preserving the true flag; validation can still succeed.
- Exact-surface falsifier: permit `broker_protocol_only=False`; the `pytest.raises` assertion at lines `56-61` must fail.
- Assertion that must fail and why: The `pytest.raises` context at lines `56-61` must fail if `broker_protocol_only=False` is accepted, because the model validator at contract lines `248-253` is the only mechanism expected to reject that value. A true flag remains merely declarative and does not prove the preview or its consumer stays adapter-neutral.
- Semantic relation: `exact_full_proof`.
- Proof strength: `boundary`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; preserve this narrow carrier-state invariant.

## G4 — `test_placement_readiness_result_cannot_claim_broker_execution_or_resizing`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py:64-86`; the result rejects true broker-opened and capital-resized flags.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`; P1 `Opening Architecture` and `Placement Readiness` records `P1-110`, `P1-112`.
- Authority match: broker execution and capital sizing are expressly outside opening authority.
- Behaviour proved: both prohibited booleans are fixed false by model validation.
- Limitation: readiness state is an unconstrained string; no invariant requires a handoff only for ready state or forbids it for blocked state; input trace and handoff identities need not agree.
- Adversarial challenge: construct a blocked or nonsensical readiness state with a handoff and contradictory IDs while both flags remain false; the tested constraints pass.
- Exact-surface falsifier: permit either prohibited flag to be true; an assertion at lines `70-86` must fail.
- Assertion that must fail and why: The first `pytest.raises` block at lines `70-77` must fail if `broker_execution_opened=True` becomes valid, and the second at lines `79-86` must fail if `capital_sizing_recomputed=True` becomes valid. These are exact false-flag invariants; they do not constrain the free-form readiness state or require identity agreement between the trace and handoff.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; keep both exact false-flag regressions and add cross-object/state invariants.

## G5 — `test_opening_service_emits_protocol_only_non_executing_readiness_material`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_authority_boundary_surface.py:89-102`; one caller-built continue decision yields ready handoff material.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`; P1 records `P1-110` through `P1-114`.
- Authority match: the output shape and prohibited-authority flags align with row 5.12, but the authority remains provisional and requires truthful capital/candidate seam evidence.
- Behaviour proved: the service returns protocol-only trace/handoff, false execution and resizing flags, and a non-null handoff for one positive decision.
- Limitation: the test fabricates capital authority rather than consuming a receipt; the decision model permits absent input trace; candidate identity is caller-supplied and not tied to the decision; constraints are untyped; readiness and handoff IDs are weakly validated; preview aliases remain open.
- Adversarial challenge: pass a fabricated continue decision with no capital input trace and a candidate unrelated to its source; all assertions remain green.
- Exact-surface falsifier: change the service to open execution/resizing, omit the handoff or return non-protocol flags; an assertion at lines `97-102` must fail.
- Assertion that must fail and why: At least one assertion at lines `97-102` must fail if the positive service path returns a non-protocol trace, sets either prohibited authority flag, omits its handoff, or changes the handoff's two boundary booleans. The test still supplies a caller-constructed capital decision with no authenticated input trace and an unrelated candidate ID, so it cannot establish truthful seam lineage.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; require admitted capital receipt/candidate identity, typed constraints and cross-object readiness invariants before Tier-A promotion.

## File decision

- Groups/relationships: `5/5`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Four narrow non-execution/protocol clauses are valid, but the suite materially underproves truthful inputs, identity coherence, readiness-state semantics and handoff payload authority required by row 5.12.
