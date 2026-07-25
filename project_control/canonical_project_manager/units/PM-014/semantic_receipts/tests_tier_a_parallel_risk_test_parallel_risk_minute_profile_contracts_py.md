# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py`

## File evidence

- Sequence `074`, unit `PM-014`; test SHA-256 `4b6898d812ba426976e6197b3178fc039bcefd050172dae456eec197c7aad5a0`.
- Full reads: test `1-224`; directly exercised model definitions and validators in `src/nvda_desk/contracts/parallel_risk.py:1-623`; Parallel Risk authority `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; proof traceability law `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:28-36,49-59`; P1 decisions `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv:121-124`.
- Raw test result: `14 passed in 0.14s`.

## G1 — `test_parallel_risk_minute_profile_minimal_instantiates_and_serialises`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:35-56`; assertions at lines `51-55` verify five default/serialised fields.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for a canonical `ParallelRiskMinuteProfile` schema, lane ID, inventory reference and description template.
- Authority match: the object is compatible with an independent risk reading, but no admitted proposition defines this product or exact fields.
- Behaviour proved: one minimal model instance serialises with the asserted defaults and references.
- Limitation: construction and serialisation prove only schema presence for one specimen, not semantic ownership, lifecycle, consumers or non-authority.
- Adversarial challenge: the model could add executable authority or incorrect unasserted defaults while every assertion remains green.
- Exact-surface falsifier: change one asserted default such as `lane_id` or `risk_envelope_state` so an assertion at lines `51-55` fails.
- Assertion that must fail and why: lines `51-55` each compare one serialised field with the fixture's expected default or reference, so changing `lane_id`, envelope state, false candidate flag, inventory reference or template ID makes that exact equality fail. The group does not inspect any other default or consumer behaviour.
- Semantic relation: `authority_missing`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact profile schema and field semantics are normatively and vocabulary admitted.

## G2 — `test_authority_flags_default_all_forbidden_capabilities_false`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:58-72`; seven parametrised assertions require each named flag to default false.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; `NO_VALID_AUTHORITY_RELATIONSHIP` for this exact seven-field flag schema.
- Authority match: false defaults align with the normative non-candidate/non-capital boundary, but labels do not prove the prohibited behaviours are impossible.
- Behaviour proved: all seven named fields default to `False` in the model.
- Limitation: no service call or side effect is instrumented, and other authority-bearing fields or pathways are not challenged.
- Adversarial challenge: code could call a broker while leaving every flag false.
- Exact-surface falsifier: default any parametrised field to true so the assertion at line `72` fails for that case.
- Assertion that must fail and why: the parametrised assertion at line `72` fails for whichever named flag defaults to `True`. It would not fail if prohibited authority were exposed through a new field, method, callback or external side effect while all seven existing flags stayed false.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return with exact flag ownership and behavioural rejection/non-interference tests.

## G3 — `test_authority_flags_reject_forbidden_capability_override`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:75-77`; the `pytest.raises` assertion requires rejection of `capital_sizing_allowed=True`.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the carrier itself.
- Authority match: rejecting capital-sizing authority is an exact bounded implementation of the Parallel Risk prohibition, although it is located on an unadmitted model.
- Behaviour proved: the exact capital-sizing override cannot be instantiated through this validator.
- Limitation: only one field and one constructor path are tested; model bypasses, mutation after construction and synonymous authority fields remain unproved.
- Adversarial challenge: add `authorised_notional_usd` or mutate the object post-validation without touching this field.
- Exact-surface falsifier: permit `capital_sizing_allowed=True` so the `pytest.raises` assertion at lines `76-77` fails.
- Assertion that must fail and why: the `pytest.raises` block at lines `76-77` fails if `AuthorityFlags(capital_sizing_allowed=True)` constructs successfully or raises a non-matching error. It proves rejection of this one constructor override only; a synonymous authority field or post-construction bypass is outside the assertion.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `substitution`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; preserve as boundary evidence and return after the carrier and complete authority schema are admitted.

## G4 — `test_risk_atom_state_supports_observe_caution_block_without_trade_action_fields`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:80-98`; assertions at lines `95-97` check three states and absence of selected model-field names.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for `RiskAtomState`, its state taxonomy, intensity/confidence fields or family semantics.
- Authority match: the object describes risk-like states, but existing Parallel Risk propositions do not define this atomic contract.
- Behaviour proved: three fixtures instantiate and selected forbidden field names are absent from the model signature.
- Limitation: signature absence does not reject aliases, nested authority, methods or side effects, and the state vocabulary is implementation-defined.
- Adversarial challenge: add an `action_payload` nested field or broker method while retaining the same model fields tested.
- Exact-surface falsifier: remove one asserted state or add one exact forbidden field name so an assertion at lines `95-97` fails.
- Assertion that must fail and why: line `95` fails if the three fixture states are not retained in order, and line `97` fails when one exact name from `FORBIDDEN_AUTHORITY_FIELD_NAMES` appears in `RiskAtomState.model_fields`. A differently named nested action carrier or method does not touch either assertion.
- Semantic relation: `authority_missing`.
- Proof strength: `signature_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after atom ownership, state taxonomy and structural non-authority law are admitted.

## G5 — `test_signal_snapshot_entry_represents_present_missing_quarantined_and_stale_states`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:100-151`; assertions at lines `145-151` verify four fixture status values and one freshness value.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for this signal-snapshot availability/freshness taxonomy and its lifecycle semantics.
- Authority match: explicit missing and stale states are generally compatible with preparation law, but these exact labels and combinations are not owned by an admitted proposition.
- Behaviour proved: four specimen objects retain the supplied status/freshness labels.
- Limitation: no transition, validation matrix, impossible-combination rejection or downstream consequence is exercised.
- Adversarial challenge: allow contradictory `missing` plus a value, or `fresh` with no source time, without failing any current assertion.
- Exact-surface falsifier: alter one supplied status during validation so an assertion at lines `145-151` fails.
- Assertion that must fail and why: lines `145-150` fail if any fixture's supplied presence label changes, and line `151` fails if the last fixture no longer retains `stale`. The group never asserts invalid combinations, so allowing a missing entry with a value would not necessarily fail.
- Semantic relation: `authority_missing`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact snapshot state vocabulary and invariants are admitted and negatively tested.

## G6 — `test_expected_signal_inventory_refs_are_metadata_only`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:154-168`; assertions at lines `166-168` check two references and a false direct-read flag.
- Authority locator: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:79-83` for typed downstream reading; `NO_VALID_AUTHORITY_RELATIONSHIP` for these exact workbook-reference fields and the claim that they are metadata-only.
- Authority match: retaining source references without direct workbook reads is aligned with preparation law, but the test does not observe runtime I/O.
- Behaviour proved: the model carries the two supplied reference strings and defaults the direct-read flag false.
- Limitation: it does not run the loader/assembler or intercept workbook access; a false label is not runtime non-read proof.
- Adversarial challenge: code can open the workbook elsewhere while these fields remain unchanged.
- Exact-surface falsifier: drop or change either asserted reference so an assertion at lines `166-167` fails; this does not falsify actual workbook-read behaviour.
- Assertion that must fail and why: line `166` fails if the inventory reference no longer ends in the named sheet fragment, and line `167` fails if the workbook lineage list changes. Line `168` only checks a stored false flag; none of the three assertions intercepts an actual workbook read.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact metadata ownership and behavioural no-direct-read proof.

## G7 — `test_description_fields_are_template_and_vocabulary_references_only`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:171-184`; assertions verify two references and absence of selected model-field names.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the profile description template/reference fields and completeness of the forbidden field-name set.
- Authority match: vocabulary references are compatible with governance, but no proposition establishes this exact description surface or that field-name absence guarantees bounded language.
- Behaviour proved: the two strings are retained and selected field names are absent from the current model signature.
- Limitation: templates may contain free-form or action language, aliases may be introduced, and no rendered description is evaluated.
- Adversarial challenge: place trading advice in the referenced template while preserving every model-field assertion.
- Exact-surface falsifier: add exact `plain_english` or `freeform_text` model fields so the loop assertion at line `184` fails.
- Assertion that must fail and why: the first two assertions fail if either reference string is altered, while the loop at line `184` fails only when one exact forbidden field name is added to the model. Trading advice inside the referenced template or under an unlisted field name leaves the group green.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `signature_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after an owned description contract and semantic output tests.

## G8 — `test_register_and_contribution_contracts_remain_descriptive`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:187-224`; assertions at lines `220-224` echo one field from each of five fixture models.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for Missing/Freshness/Event registers, Risk Family State and Contribution Breakdown contracts.
- Authority match: the names are related to an independent risk reading, but no admitted proposition defines these carriers, fields, taxonomies or downstream consequences.
- Behaviour proved: each fixture retains one supplied descriptive value.
- Limitation: value echoing does not prove descriptive-only behaviour, validation boundaries, aggregation meaning or absence of action authority.
- Adversarial challenge: each model could contain an unasserted execution instruction while the five echo assertions remain green.
- Exact-surface falsifier: alter one asserted fixture value during model construction so its assertion at lines `220-224` fails.
- Assertion that must fail and why: each assertion at lines `220-224` echoes one named field from one fixture, so changing that field's stored value makes only its corresponding equality fail. Additional unasserted authority fields or behaviour on any of the five models would not be detected.
- Semantic relation: `authority_missing`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after separate proposition-level and vocabulary admission of each carrier and its invariants.

## File decision

- Groups/relationships: `8/8`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve the exact capital-flag rejection and model-shape observations as implementation evidence. The profile, authority flags, atom/family, snapshot and register/contribution contracts remain unadmitted for Tier A.
