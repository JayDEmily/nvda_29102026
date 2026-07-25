# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_family_aggregation.py`

## File evidence

- Sequence `068`, unit `PM-014`; test SHA-256 `70e62e76e8b1fcb7185d98950192c2eaa14cf0f89eb060a426eea11af5f57a58`.
- Full reads: test `1-37`; implementation `src/nvda_desk/domain/parallel_risk/family_aggregation.py:1-53`; directly exercised `RiskAtomState` and `RiskFamilyState` contracts in `src/nvda_desk/contracts/parallel_risk.py`; PRL/Environment Assessment authority `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66`, `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`, and P1 rows `121-122`.
- Raw test result: `2 passed in 0.13s`.

## G1 — `test_family_aggregation_uses_highest_state_and_max_intensity_without_action_authority`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_family_aggregation.py:19-33`; assertions at lines `29-33` fix selected family state, intensity, confidence, dominant atom and another family state.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the `Risk Atom`/`Risk Family State` abstractions or the ranking/max/min aggregation policy.
- Authority match: the result is related to an independent environmental reading, but higher authority defines only the lane’s risk envelope/caution/block role and does not own these new contracts or aggregation rules.
- Behaviour proved: for three fixture atoms, the implementation groups by caller-supplied family, chooses the highest ranked state, maximum intensity, minimum confidence and exact dominant atom IDs.
- Limitation: it does not prove the state order, max/min policy, family labels, tie handling beyond this specimen, completeness of atoms, or absence of action authority; the fixture’s explanatory string is declarative.
- Adversarial challenge: the implementation could grant capital authority elsewhere, mishandle equal-ranked unequal-intensity atoms, or silently omit an unknown family while assertions `29-33` remain green.
- Exact-surface falsifier: change the calendar family result to `observe`, intensity away from `0.7`, confidence away from `0.6`, or dominant atoms away from `["a2"]` so one of assertions `29-32` fails.
- Assertion that must fail and why: line `29` fails if `calendar_event.state` is no longer `caution`; line `30` fails if the maximum intensity is not `0.7`; line `31` fails if confidence is not the minimum `0.6`; and line `32` fails if `a2` is not the sole dominant atom. Those failures establish only the fixture aggregation outputs, not the unasserted authority boundary named in the test title.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact vocabulary and proposition admission for atom/family state, ranking, intensity/confidence aggregation, tie behaviour and non-authority boundaries.

## G2 — `test_family_aggregation_empty_atoms_returns_empty_list`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_family_aggregation.py:36-37`; assertion line `37` requires `[]` for empty input.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the empty-state semantics of a governed `Risk Family State` collection.
- Authority match: empty-in/empty-out is implementation-compatible but cannot establish the missing abstraction, completeness or unknown/error policy.
- Behaviour proved: the exercised function returns an empty list when given no atoms.
- Limitation: no distinction is made between genuinely no risk atoms, failed atom construction, missing required inputs or suppressed errors.
- Adversarial challenge: an upstream failure could be converted to an empty atom list and this test would report success while risk evidence was lost.
- Exact-surface falsifier: return any non-empty family object for `aggregate_risk_family_states([])` so assertion line `37` fails.
- Assertion that must fail and why: line `37` compares the complete return value with `[]`, so any emitted family record, sentinel or error-carrier object makes that equality false. The assertion cannot distinguish a legitimate absence of atoms from an upstream failure that has already been collapsed to an empty list.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after an admitted empty/unknown/error contract for the owning aggregation surface.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve deterministic grouping observations as implementation evidence only.
