# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py`

- Sequence `069`, PM-014; test SHA-256 `07b965aa0a7b0b7d7b2d08ac30b4fe0f5375d9cbd6f5b692873d65d61e3930a4`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.domain.parallel_risk.freshness: build_freshness_register_entry.
- Surviving decision summary: manual_receipt_complete_source_temporal_non_substitution_preserved_but_freshness_threshold_taxonomy_impacts_and_token_neutrality_lack_authority

## Complete test restatement

- Lines `8-31` `test_freshness_register_marks_fresh_ageing_and_stale_with_deterministic_defaults`: executes the named specimen/boundary and observes checks at lines `27, 28, 29, 30, 31`. The exact assertions are enumerated in the relationship sections below.
- Lines `34-39` `test_freshness_register_unknown_when_source_or_generated_time_absent`: executes the named specimen/boundary and observes checks at lines `37, 38, 39`. The exact assertions are enumerated in the relationship sections below.
- Lines `42-59` `test_freshness_register_is_metadata_only_and_neutral_state_of_play`: executes the named specimen/boundary and observes checks at lines `53, 54, 55, 56, 57, 58, 59`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_freshness_register_marks_fresh_ageing_and_stale_with_deterministic_defaults`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py:8-31`. Checks: L27 assert `fresh.freshness_state == "fresh"`; L28 assert `fresh.observed_age_seconds == 30`; L29 assert `fresh.max_allowed_age_seconds == 60`; L30 assert `ageing.freshness_state == "ageing"`; L31 assert `stale.freshness_state == "stale"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_source_temporal_non_substitution_preserved_but_freshness_threshold_taxonomy_impacts_and_token_neutrality_lack_authority
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_freshness_register_unknown_when_source_or_generated_time_absent`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py:34-39`. Checks: L37 assert `entry.freshness_state == "unknown"`; L38 assert `entry.observed_age_seconds is None`; L39 assert `entry.impact_on_profile == "freshness_unknown_state_of_play"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_source_temporal_non_substitution_preserved_but_freshness_threshold_taxonomy_impacts_and_token_neutrality_lack_authority
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_freshness_register_is_metadata_only_and_neutral_state_of_play`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py:42-59`. Checks: L53 assert `entry.freshness_state == "stale"`; L54 assert `entry.captured_at_utc == generated - timedelta(seconds=140)`; L55 assert `entry.persisted_at_utc == generated - timedelta(seconds=130)`; L56 assert `entry.source_refs == ["source:options_flow_fixture"]`; L57 assert `entry.impact_on_profile == "freshness_stale_uncertainty_contribution"`; L58 assert `"trade" not in entry.model_dump_json()`; L59 assert `"order" not in entry.model_dump_json()`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_source_temporal_non_substitution_preserved_but_freshness_threshold_taxonomy_impacts_and_token_neutrality_lack_authority
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `state_transition`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `3/3`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
