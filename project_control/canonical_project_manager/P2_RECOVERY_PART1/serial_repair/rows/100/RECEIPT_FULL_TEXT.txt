# Semantic receipt — `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py`

## File evidence

- Sequence `100`, unit `PM-015`; test SHA-256 `5409d16b8c13017c2a333e006d0493a2d1f4e3998f12fe514b0b7a65c5f04d1f`.
- Full reads: test `1-294`; complete contracts `src/nvda_desk/contracts/exit_close.py`; complete service `src/nvda_desk/downstream/exit_close.py`; row-5.14 authority `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:356-371`; P1 `P1-117`/`P1-118` in `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv`.
- Raw test result: `16 passed in 0.15s`.
- Adversarial probe: `project_control/canonical_project_manager/P2_RECOVERY_PART1/validation/100_adversarial_probe.txt` proves whitespace-only authority identities and an aliased broker key are accepted, and that a hold decision can be paired with another decision's close handoff plus an arbitrary unverified fingerprint.

## G1 — hidden-authority key rejection

- Test locator: `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py:35-51`; two tests reject/detect exact nested keys from a finite set.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:364-370` and P1 `P1-117`/`P1-118`.
- Authority match: exit/close inputs must exclude broker execution, capital sizing, raw ingress and hidden inventory mutation; recursive exact-key rejection is a bounded clause.
- Behaviour proved: the exact snake-case keys `order_execution`, `live_order_placement` and `broker_order_id` are found or rejected when nested.
- Limitation: aliases and semantically equivalent payloads are not governed; the probe proves `brokerOrderId` survives. Whitespace-only required trace IDs also pass.
- Adversarial challenge: use renamed keys, object attributes or collaborator authority instead of one finite dictionary key.
- Exact-surface falsifier: stop detecting one tested exact nested key; an assertion at lines `36-51` must fail.
- Assertion that must fail and why: at test lines `35-51`, allowing nested `order_execution`, or failing to return the exact sorted pair `broker_order_id` and `live_order_placement`, breaks the expected validation or list equality. An unlisted alias remains invisible to this finite key registry.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; replace finite-name filtering with typed inputs, canonical identity validation and executable owner boundaries.

## G2 — exit-policy decision state

- Test locator: `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py:54-112`; four tests cover close-ready output, closed/missing-trigger blocks, action/state consistency and false mutation flags.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:356-371` and P1 `P1-117`.
- Authority match: hold/trim/close/blocked decision state and no broker/capital/inventory mutation are lawful clauses of Exit Architecture.
- Behaviour proved: caller-supplied action, trigger IDs and `position_open` produce the asserted deterministic state; inconsistent state and one broker flag are rejected.
- Limitation: no live-position repository, risk context, playbook/exit-policy record, market state or broker constraint is read; policy is reduced to caller strings/booleans and false flags.
- Adversarial challenge: pass fabricated `position_open=True` and arbitrary trigger text for a nonexistent position; the asserted decision still becomes close-ready.
- Exact-surface falsifier: change the tested state/reasons or permit the tested inconsistent/mutation flag; an assertion at lines `62-112` must fail.
- Assertion that must fail and why: at test lines `62-112`, changing the nominal close-ready state or trace echoes, failing to block the closed/missing-trigger fixtures, accepting the action/state mismatch, or allowing `broker_execution_opened=True` breaks a direct assertion or expected `ValidationError`. Fabricated caller truth for position state and triggers is not challenged.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; require admitted live-state/policy/risk inputs and source-linked decision invariants.

## G3 — protocol-only close handoff

- Test locator: `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py:115-168`; four tests cover protocol-only flags, ready-state precondition, live-order rejection and one nested broker key.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:364-370` and P1 `P1-118`.
- Authority match: a non-executing handoff after trim/close-ready is a lawful bounded Close Architecture clause.
- Behaviour proved: the builder emits the asserted protocol-only false-execution flags and refuses hold/blocked decisions and the tested exact broker payload.
- Limitation: decision/handoff identity coupling, quantity/price/order-intent schema, canonical broker-protocol contract, aliases and later execution acknowledgement are unproved.
- Adversarial challenge: construct a handoff for another decision/position or embed aliased broker authority while retaining the asserted flags.
- Exact-surface falsifier: allow a hold handoff, change a protocol flag, or accept the tested nested `broker_execution`; an assertion at lines `125-168` must fail.
- Assertion that must fail and why: at test lines `125-168`, changing any protocol-only/non-execution flag or requested-action preview, accepting a non-protocol boundary, building a handoff from `hold`, allowing live-order placement, or accepting nested `broker_execution` breaks an equality or expected-error assertion. Identity coupling and aliases are not covered.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; preserve the protocol-only guard while adding typed handoff and identity-coupling proof.

## G4 — receipt copy and emitted-output boundary

- Test locator: `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py:171-207`; tests compare a recomputed hash, deep-copy one output and reject one exact forbidden emitted-output key.
- Authority locator: P1 `P1-118` and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:64-70`.
- Authority match: deterministic replay material, copy isolation and non-authoritative emitted output are relevant clauses.
- Behaviour proved: a builder-produced receipt recomputes the same hash, deep-copy mutation is isolated, and exact `capital_sizing` output is rejected.
- Limitation: receipt construction accepts any fingerprint string; the model never verifies it. Source/state/policy versions, original result identity, persistence and restart replay are absent.
- Adversarial challenge: construct a receipt with an arbitrary fingerprint and semantically equivalent aliased authority; the model accepts it.
- Exact-surface falsifier: change builder material without changing the recomputed hash, share the copied output, or accept exact `capital_sizing`; an assertion at lines `185-207` must fail.
- Assertion that must fail and why: at test lines `185-207`, setting either mutation flag true, making helper recomputation differ from the builder fingerprint, sharing the copied emitted-output dictionary, or accepting exact `capital_sizing` breaks a direct assertion or expected validation error. The model still accepts an arbitrary caller-supplied fingerprint string.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `replay`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; validate the stored fingerprint and prove authoritative replay-envelope completeness.

## G5 — receipt consistency and fingerprint sensitivity

- Test locator: `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py:210-274`; tests reject trace mismatch and a live-inventory flag, and show changed handoff material changes a builder-computed fingerprint.
- Authority locator: P1 `P1-118` and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:50-70`.
- Authority match: receipt/decision trace consistency, non-mutation and material-sensitive replay identity are lawful clauses.
- Behaviour proved: the exact tested trace mismatch and mutation flag fail, and the helper hash changes for the changed trigger list.
- Limitation: receipt/handoff decision and position identities are not cross-validated; the probe accepts a `hold-B` decision with `close-A` handoff and arbitrary fingerprint.
- Adversarial challenge: attach a valid handoff from another decision/position; every tested validator can remain green.
- Exact-surface falsifier: accept the tested mismatched trace/live-mutation flag or make the two tested material states hash equal; an assertion at lines `218-274` must fail.
- Assertion that must fail and why: at test lines `218-274`, accepting a receipt trace different from its decision trace, allowing the live-inventory mutation flag, or producing equal helper fingerprints for the original and altered handoff breaks an expected error or inequality assertion. A handoff from another decision can still be attached because that identity is not validated.
- Semantic relation: `authority_contradictory`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; enforce receipt–decision–handoff identity and fingerprint consistency.

## G6 — `test_exit_close_service_wrapper_emits_receipt_without_opening_orders`

- Test locator: `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py:277-294`; one wrapper path creates a decision, handoff and receipt and checks false execution plus hash recomputation.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:356-371` and P1 `P1-117`/`P1-118`.
- Authority match: the wrapper exercises the intended thin seam, but only with caller-authored fixture truth.
- Behaviour proved: the nominal service path produces a non-executing handoff-bearing receipt with a recomputable helper hash.
- Limitation: no authoritative live-state input, policy ownership, persistence, execution acknowledgement or position-closure state transition is proved.
- Adversarial challenge: use fabricated upstream IDs and policy inputs; the wrapper still emits the asserted receipt.
- Exact-surface falsifier: omit the handoff, permit execution or alter the helper recomputation; an assertion at lines `292-294` must fail.
- Assertion that must fail and why: at test lines `292-294`, omitting the wrapper-produced handoff, setting its execution flag true, or returning a fingerprint different from helper recomputation breaks one of the three assertions. The wrapper can still consume fabricated upstream IDs and policy inputs because no authoritative source is read.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain as an alpha integration specimen after the contract defects are repaired.

## File decision

- Groups/relationships: `6/6`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Exact action/state, protocol-only, mutation and deterministic-hash clauses survive; executable probes prove material identity, alias and fingerprint defects, and the policy does not consume authoritative live state.
