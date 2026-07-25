# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py`

- Sequence `074`, PM-014; test SHA-256 `4b6898d812ba426976e6197b3178fc039bcefd050172dae456eec197c7aad5a0`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.parallel_risk: AuthorityFlags, ContributionBreakdownEntry, EventProximityRegisterEntry, FreshnessRegisterEntry, MissingSignalRegisterEntry, ParallelRiskMinuteProfile, RiskAtomState, RiskFamilyState, SignalSnapshotEntry.
- Surviving decision summary: Rich minute-profile, atom/family/register/inventory and description contracts are planning-only; retain exact true-flag rejection and unverified reference carriage only as bounded clauses.

## Complete test restatement

- Lines `35-55` `test_parallel_risk_minute_profile_minimal_instantiates_and_serialises`: executes the named specimen/boundary and observes checks at lines `51, 52, 53, 54, 55`. The exact assertions are enumerated in the relationship sections below.
- Lines `70-72` `test_authority_flags_default_all_forbidden_capabilities_false`: executes the named specimen/boundary and observes checks at lines `72`. The exact assertions are enumerated in the relationship sections below.
- Lines `75-77` `test_authority_flags_reject_forbidden_capability_override`: executes the named specimen/boundary and observes checks at lines `76`. The exact assertions are enumerated in the relationship sections below.
- Lines `80-97` `test_risk_atom_state_supports_observe_caution_block_without_trade_action_fields`: executes the named specimen/boundary and observes checks at lines `95, 97`. The exact assertions are enumerated in the relationship sections below.
- Lines `100-151` `test_signal_snapshot_entry_represents_present_missing_quarantined_and_stale_states`: executes the named specimen/boundary and observes checks at lines `145, 151`. The exact assertions are enumerated in the relationship sections below.
- Lines `154-168` `test_expected_signal_inventory_refs_are_metadata_only`: executes the named specimen/boundary and observes checks at lines `166, 167, 168`. The exact assertions are enumerated in the relationship sections below.
- Lines `171-184` `test_description_fields_are_template_and_vocabulary_references_only`: executes the named specimen/boundary and observes checks at lines `181, 182, 184`. The exact assertions are enumerated in the relationship sections below.
- Lines `187-224` `test_register_and_contribution_contracts_remain_descriptive`: executes the named specimen/boundary and observes checks at lines `220, 221, 222, 223, 224`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_parallel_risk_minute_profile_minimal_instantiates_and_serialises`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:35-55`. Checks: L51 assert `payload["lane_id"] == "parallel_risk_lane"`; L52 assert `payload["risk_envelope_state"] == "observe"`; L53 assert `payload["authority_flags"]["candidate_formation_allowed"] is False`; L54 assert `payload["expected_signal_inventory_ref"] == "workbook:Parallel Risk Lane Signal Inventory"`; L55 assert `payload["description_template_id"] == "prl.minute_profile.summary.v1"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Rich minute-profile, atom/family/register/inventory and description contracts are planning-only; retain exact true-flag rejection and unverified reference carriage only as bounded clauses.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_authority_flags_default_all_forbidden_capabilities_false`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:70-72`. Checks: L72 assert `getattr(flags, field_name) is False`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Rich minute-profile, atom/family/register/inventory and description contracts are planning-only; retain exact true-flag rejection and unverified reference carriage only as bounded clauses.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_authority_flags_reject_forbidden_capability_override`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:75-77`. Checks: L76 raises `pytest.raises(ValidationError, match="parallel_risk_authority_flags_must_remain_false")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Rich minute-profile, atom/family/register/inventory and description contracts are planning-only; retain exact true-flag rejection and unverified reference carriage only as bounded clauses.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `boundary`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G4 — `test_risk_atom_state_supports_observe_caution_block_without_trade_action_fields`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:80-97`. Checks: L95 assert `[atom.state for atom in atoms] == ["observe", "caution", "block"]`; L97 assert `forbidden_field not in RiskAtomState.model_fields`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Rich minute-profile, atom/family/register/inventory and description contracts are planning-only; retain exact true-flag rejection and unverified reference carriage only as bounded clauses.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `token_only`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G5 — `test_signal_snapshot_entry_represents_present_missing_quarantined_and_stale_states`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:100-151`. Checks: L145 assert `[entry.missing_or_quarantined for entry in entries] == [ "present", "missing", "quarantined", "present", ]`; L151 assert `entries[-1].freshness_state == "stale"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Rich minute-profile, atom/family/register/inventory and description contracts are planning-only; retain exact true-flag rejection and unverified reference carriage only as bounded clauses.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `state_transition`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G6 — `test_expected_signal_inventory_refs_are_metadata_only`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:154-168`. Checks: L166 assert `payload["expected_signal_inventory_ref"].endswith("#Parallel Risk Lane Signal Inventory")`; L167 assert `payload["workbook_lineage_refs"] == ["Raw_Primitives_Catalog!A1:H49"]`; L168 assert `profile.authority_flags.direct_workbook_runtime_read_allowed is False`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Rich minute-profile, atom/family/register/inventory and description contracts are planning-only; retain exact true-flag rejection and unverified reference carriage only as bounded clauses.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G7 — `test_description_fields_are_template_and_vocabulary_references_only`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:171-184`. Checks: L181 assert `profile.description_template_id == "prl.minute_profile.summary.v1"`; L182 assert `profile.description_vocabulary_refs == ["data/vocabulary/canonical_vocabulary.json"]`; L184 assert `forbidden_field not in ParallelRiskMinuteProfile.model_fields`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Rich minute-profile, atom/family/register/inventory and description contracts are planning-only; retain exact true-flag rejection and unverified reference carriage only as bounded clauses.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `token_only`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G8 — `test_register_and_contribution_contracts_remain_descriptive`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py:187-224`. Checks: L220 assert `missing.impact_on_profile == "lowers_confidence"`; L221 assert `freshness.freshness_state == "fresh"`; L222 assert `event.risk_interpretation == "event proximity context only"`; L223 assert `family.state == "observe"`; L224 assert `contribution.reason == "scheduled event context present"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Rich minute-profile, atom/family/register/inventory and description contracts are planning-only; retain exact true-flag rejection and unverified reference carriage only as bounded clauses.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `8/8`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
