# Semantic receipt — `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_input_surface.py`

## File evidence

- Sequence `087`, unit `PM-014`; test SHA-256 `cee0317c379eb9d5258b3bbc6f670fd0f99ae71eb02ca3ae9c21d868fabc3c23`.
- Full reads: test `1-86`; lane service and bootstrap builder; directly exercised preparation/stage-input contracts; lawful Parallel Risk inputs `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:163-170`; Parallel Risk seam `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; current StageInputBundle limitation `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:213-217`.
- Raw test result: `2 passed in 0.13s`.

## G1 — `test_sequence7_bootstrap_input_carries_all_allowed_parallel_risk_primitives`

- Test locator: `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_input_surface.py:44-63`; assertions verify temporal event time, VIX, two DTE fields and bootstrap source.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:163-170` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Authority match: admitted Stage Input Bundle temporal/regime/options-flow primitives are explicitly lawful Parallel Risk inputs, and the group exercises their typed bootstrap carriage.
- Behaviour proved: the fixture’s four primitive values and bootstrap-source label survive into the typed preparation packet.
- Limitation: current StageInputBundle lacks complete prepared/source identity and schema/policy/fingerprint lineage under `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:213-217`; this group does not cure that broader alpha gap.
- Adversarial challenge: detach the regime/options values from their prepared authority or substitute stale inputs while preserving the asserted values.
- Exact-surface falsifier: alter or omit one asserted primitive/source so an assertion at lines `58-62` fails.
- Assertion that must fail and why: at test lines `58-62`, deleting the next-event value, changing VIX from `31.0`, changing either DTE, or changing the exact bootstrap-source label makes its corresponding equality/non-null assertion fail. The group does not compare preparation identity, source freshness or fingerprints, so those can be wrong without touching this surface.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; retain as bounded bootstrap-carriage evidence until the StageInputBundle preparation/identity gap is repaired.

## G2 — `test_sequence7_bootstrap_input_excludes_downstream_decision_authority`

- Test locator: `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_input_surface.py:65-86`; loop asserts absence of seven selected strings from one payload dump.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Authority match: the prohibited authority is normative, but finite token absence does not prove structural or behavioural exclusion.
- Behaviour proved: the seven literal strings are absent from the exercised payload.
- Limitation: aliases, nested authority, callbacks and side effects remain unobserved.
- Adversarial challenge: add `deployable_fraction` or a broker callback without any listed token.
- Exact-surface falsifier: insert one listed token so the corresponding assertion at line `86` fails.
- Assertion that must fail and why: at test lines `76-86`, placing any one of the seven exact forbidden strings in the dumped preparation packet makes the loop assertion fail. A semantically equivalent authority field under another name, or a side effect outside the payload, is not detected.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; return to Tier A only with schema rejection and side-effect/consumer boundary proof.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `ADMIT_TIER_B_SHADOW`.
- Demote from blocking Tier A: lawful primitive carriage is bounded evidence, but incomplete prepared identity and lexical non-authority proof prevent current Tier A admission.
