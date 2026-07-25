# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_service_integration.py`

## File evidence

- Sequence `075`, unit `PM-014`; test SHA-256 `699e93566753bafbbfdc4ccdc56553a035047532d9377f7c1afe7580fb499e89`.
- Full reads: test `1-50`; lane service `src/nvda_desk/services/parallel_risk_lane_service.py:1-229`; profile assembler and directly exercised contracts; Parallel Risk seam `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; proof traceability `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:28-36,59-73`; P1 Parallel Risk decision `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv:121`.
- Raw test result: `2 passed in 0.13s`.

## G1 — `test_run_bootstrap_default_result_remains_backward_compatible`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_service_integration.py:21-28`; assertion at line `28` requires exactly the bootstrap and lane packet keys when the option is not enabled.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Authority match: the default returned packet pair is a bounded compatibility clause on the admitted Parallel Risk packet seam.
- Behaviour proved: one default bootstrap call exposes no third optional result key.
- Limitation: key-set equality does not prove packet content, hidden reads, side effects or all callers remain compatible.
- Adversarial challenge: mutate the lane packet or capital state while preserving the same two keys.
- Exact-surface falsifier: add or remove a default result key so the exact-set assertion at line `28` fails.
- Assertion that must fail and why: line `28` compares the complete default result key set, so any added optional key or missing packet key makes the equality false. The assertion says nothing about whether the two retained packet objects changed internally or whether the call caused an external side effect.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `behavioural`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain only as the bounded default-return compatibility clause.

## G2 — `test_run_bootstrap_can_include_optional_minute_profile_without_changing_lane_packet`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_service_integration.py:31-50`; assertions check the optional key, packet/profile IDs, lineage and a false capital-sizing flag.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for an optional Minute Profile output and its schema.
- Authority match: the optional object is implementation-related to the Parallel Risk reading, but no admitted proposition owns it; despite the test name, no before/after lane-packet equality assertion exists.
- Behaviour proved: enabling the option emits one additional object with the asserted IDs, lineage and false flag.
- Limitation: the lane packet is not compared against a control run, side effects are uninstrumented and false flags do not prove non-authority.
- Adversarial challenge: enabling the option could alter the lane packet, read a workbook or call a capital service while every assertion remains green.
- Exact-surface falsifier: omit the optional object or change an asserted profile/lineage field so an assertion in lines `43-50` fails; this does not test unchanged-lane behaviour.
- Assertion that must fail and why: line `41` fails if the optional key is absent, and lines `43-49` fail if the profile type, identity, envelope or supplied lineage values change. No assertion compares `lane_packet` with the default run, so changing that packet while preserving the optional profile leaves the title's “without changing” claim untested.
- Semantic relation: `authority_missing`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact profile ownership and a control-vs-option packet equality plus side-effect boundary test.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve G1 as bounded compatibility evidence. The file remains blocked because its material optional-product claim depends on an unadmitted Minute Profile and does not prove the named unchanged-lane behaviour.
