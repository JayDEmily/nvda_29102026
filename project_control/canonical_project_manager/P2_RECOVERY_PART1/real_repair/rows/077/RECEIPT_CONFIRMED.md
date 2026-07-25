# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_options_dte_preservation.py`

## File evidence

- Sequence `077`, unit `PM-014`; test SHA-256 `453d115bd67151d8f81f564a7e4efa9c15b46a5203cd473d717d9b5b8c234605`.
- Full reads: test `1-33`; environment assessment `src/nvda_desk/domain/parallel_risk/environment_assessment.py:1-126`; options-flow contract `src/nvda_desk/contracts/options_flow.py:1-14`; Parallel Risk seam `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; proof traceability `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:28-36`.
- Raw test result: `2 passed in 0.13s`.

## G1 — `test_front_dte_greater_than_next_dte_preserves_options_repricing_caution`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_options_dte_preservation.py:12-23`; assertions require a named caution and contribution when `front_dte > next_dte`.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact DTE inequality, `front_term_structure_backwardation` label or caution consequence.
- Authority match: options context is a lawful input to an independent risk reading, but the exact financial interpretation and mapping are not normatively or vocabulary owned.
- Behaviour proved: the exercised inequality emits the asserted current caution and contribution.
- Limitation: equality, missing/invalid DTE, calendar-day versus trading-day semantics and other term structures are not covered.
- Adversarial challenge: a reversed financial interpretation or off-by-one expiry convention could remain green for this single fixture.
- Exact-surface falsifier: suppress or rename the asserted caution/contribution so an assertion in lines `20-23` fails.
- Assertion that must fail and why: line `20` fails if the inequality no longer yields a caution envelope, line `21` fails if the exact caution label changes, and line `22` fails if the sole contribution no longer names `options_repricing_context`. The group does not prove that the inequality is the financially correct or governed definition of backwardation.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after owned term-structure semantics and complete boundary cases are admitted.

## G2 — `test_front_dte_not_greater_than_next_dte_does_not_create_legacy_caution`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_options_dte_preservation.py:26-33`; assertions require the reverse ordering to remain tight and omit the named caution.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the complete negative boundary and state mapping.
- Authority match: this narrows current implementation behaviour but does not derive from an admitted DTE policy.
- Behaviour proved: one reverse-order fixture does not produce the named caution.
- Limitation: it does not establish all non-caution states, equal DTE, invalid values or alternative caution reasons.
- Adversarial challenge: another unsupported DTE arrangement may be misclassified without affecting this fixture.
- Exact-surface falsifier: emit any non-`tight` envelope state for the reverse-order fixture; the assertion at line `33` must fail. The test has no direct assertion on the caution flag’s absence.
- Assertion that must fail and why: line `33` fails whenever the reverse-order fixture returns an envelope state other than `tight`. Because the test never inspects `caution_flags`, it does not independently fail on an incorrectly retained `front_term_structure_backwardation` label unless that label also changes the envelope state.
- Semantic relation: `authority_missing`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return with an admitted state table and edge-case tests.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve both DTE regression observations; Tier A remains blocked because the inequality, labels and consequences are not admitted semantic truth.
