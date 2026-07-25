# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_supported_risk_atoms.py`

## File evidence

- Sequence `082`, unit `PM-014`; test SHA-256 `dd2b52ed344cfb6a61535d3130eb0d9ce405ca06b4d5770d9cfc1cdcec462790`.
- Full reads: test `1-93`; atom builder `src/nvda_desk/domain/parallel_risk/risk_atoms.py:1-123`; directly exercised register/envelope/atom contracts `src/nvda_desk/contracts/parallel_risk.py:330-560`; Parallel Risk seam `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; final-join law `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:82-131`.
- Raw test result: `2 passed in 0.13s`.

## G1 — `test_supported_risk_atoms_wrap_current_environmental_inputs_without_trade_actions`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_supported_risk_atoms.py:15-72`; assertions require five generated IDs, non-empty explanatory strings and absence of selected advice tokens.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; `NO_VALID_AUTHORITY_RELATIONSHIP` for Risk Atom schema, ID grammar, families, mappings, constants and source-register meanings.
- Authority match: composing an independent risk reading is related to the lane purpose, but the exact atomic ontology and calculation policy are not admitted.
- Behaviour proved: the supplied freshness, missing, event and envelope fixtures deterministically generate at least the five asserted current atom IDs and explanations.
- Limitation: finite token absence is incomplete; intensities, confidence, mappings, duplicate handling, ordering and all other source states are unproved.
- Adversarial challenge: emit a differently named action instruction or incorrect confidence/intensity while retaining the asserted IDs.
- Exact-surface falsifier: omit one asserted atom ID or empty its explanation so an assertion at lines `61-69` fails.
- Assertion that must fail and why: at test lines `61-72`, omitting any one of the five expected IDs makes the set-superset assertion false, blanking any emitted explanation breaks `all(...)`, and introducing one exact forbidden token into the serialised atoms fails the final loop. Incorrect unasserted intensity, confidence, ordering or synonymous advice can remain green.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after atom ontology, mappings, constants and structural non-authority are admitted.

## G2 — `test_supported_risk_atoms_preserve_constructive_and_uncertainty_semantics`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_supported_risk_atoms.py:75-93`; assertions require `observe`, `constructive` and positive confidence for one fresh-input atom.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the `constructive` risk-side vocabulary, state mapping and confidence policy.
- Authority match: the fixture expresses implementation semantics not defined by the controlling Parallel Risk proposition.
- Behaviour proved: one fresh input produces the three asserted current values.
- Limitation: the test does not establish the meaning, range, calibration, threshold or other state combinations.
- Adversarial challenge: set an arbitrary tiny positive confidence or invert another input’s risk side while preserving this fixture.
- Exact-surface falsifier: change the first atom’s asserted state/risk-side or make confidence non-positive so an assertion at lines `91-93` fails.
- Assertion that must fail and why: at test lines `90-93`, changing the first returned atom from `observe`, changing its `calculation_basis["risk_side"]` from `constructive`, or setting confidence to zero or below breaks one of the three exact assertions. Any positive value, however poorly calibrated, still satisfies this specimen.
- Semantic relation: `authority_missing`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after vocabulary and coefficient/config ownership for all state/risk-side/confidence mappings.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve deterministic current atom construction as implementation evidence; the atom/family ontology, IDs, states, mappings and constants are not admitted Tier A truth.
