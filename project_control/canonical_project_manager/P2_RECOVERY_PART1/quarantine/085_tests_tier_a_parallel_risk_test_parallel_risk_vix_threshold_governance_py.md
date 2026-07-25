# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_governance.py`

- Sequence `085`, PM-014; test SHA-256 `8e29f3d16fea2d68a060f084ec613e80455acca36201ad63e5ceab9c06241d59`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.config.parallel_risk_lane_profile: ParallelRiskLaneProfileService; nvda_desk.contracts.options_flow: OptionsFlowContextInput; nvda_desk.contracts.parallel_risk: ParallelRiskPreparationPacket, parallel_risk_lane_profile_config_from_dict; nvda_desk.contracts.regime: MarketRegimeContextInput; nvda_desk.contracts.temporal: TemporalContextInput; nvda_desk.domain.parallel_risk.environment_assessment: assess_risk_envelope.
- Surviving decision summary: The file executes exact 30/50 and caller-authored 25/45 VIX policies without a current governing proposition; its coefficient refs point to posture-owned 24/32 records, while migration authority is created by caller labels. Default-deny validators are useful but do not prove runtime non-authority.

## Complete test restatement

- Lines `36-53` `test_parallel_risk_lane_profile_config_loads_and_preserves_compatibility`: executes the named specimen/boundary and observes checks at lines `40, 41, 42, 43, 44, 45, 52, 53`. The exact assertions are enumerated in the relationship sections below.
- Lines `56-62` `test_parallel_risk_lane_profile_invalid_threshold_config_fails`: executes the named specimen/boundary and observes checks at lines `61`. The exact assertions are enumerated in the relationship sections below.
- Lines `65-80` `test_parallel_risk_lane_profile_migration_path_is_explicit_for_governed_config`: executes the named specimen/boundary and observes checks at lines `77, 78, 79, 80`. The exact assertions are enumerated in the relationship sections below.
- Lines `83-88` `test_parallel_risk_lane_profile_hidden_coefficient_mutation_fails`: executes the named specimen/boundary and observes checks at lines `87`. The exact assertions are enumerated in the relationship sections below.
- Lines `91-105` `test_parallel_risk_lane_profile_no_authority_widening`: executes the named specimen/boundary and observes checks at lines `96, 97, 98, 99, 100, 104`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_parallel_risk_lane_profile_config_loads_and_preserves_compatibility`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_governance.py:36-53`. Checks: L40 assert `policy.mode == "compatibility_legacy_30_50"`; L41 assert `policy.caution_threshold == 30.0`; L42 assert `policy.block_threshold == 50.0`; L43 assert `policy.hidden_coefficient_mutation_allowed is False`; L44 assert `policy.authority_flags.capital_sizing_allowed is False`; L45 assert `policy.coefficient_authority_refs == [ "config/coefficient_authority.v1.yaml#risk_vix_caution_threshold", "config/coefficient_authority.v1.yaml#risk_vix_hot_threshold", ]`; L52 assert `caution_envelope.envelope_state == "caution"`; L53 assert `block_envelope.envelope_state == "block"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The file executes exact 30/50 and caller-authored 25/45 VIX policies without a current governing proposition; its coefficient refs point to posture-owned 24/32 records, while migration authority is created by caller labels. Default-deny validators are useful but do not prove runtime non-authority.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_parallel_risk_lane_profile_invalid_threshold_config_fails`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_governance.py:56-62`. Checks: L61 raises `pytest.raises(ValidationError)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The file executes exact 30/50 and caller-authored 25/45 VIX policies without a current governing proposition; its coefficient refs point to posture-owned 24/32 records, while migration authority is created by caller labels. Default-deny validators are useful but do not prove runtime non-authority.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `boundary`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_parallel_risk_lane_profile_migration_path_is_explicit_for_governed_config`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_governance.py:65-80`. Checks: L77 assert `config.vix_threshold_policy.mode == "governed_config"`; L78 assert `config.vix_threshold_policy.migration_status == "explicit_governed_test_migration"`; L79 assert `envelope.envelope_state == "caution"`; L80 assert `"vix_elevated" in envelope.caution_flags`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The file executes exact 30/50 and caller-authored 25/45 VIX policies without a current governing proposition; its coefficient refs point to posture-owned 24/32 records, while migration authority is created by caller labels. Default-deny validators are useful but do not prove runtime non-authority.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G4 — `test_parallel_risk_lane_profile_hidden_coefficient_mutation_fails + test_parallel_risk_lane_profile_no_authority_widening`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_governance.py:83-105`. Checks: L87 raises `pytest.raises(ValidationError)`; L96 assert `authority.candidate_formation_allowed is False`; L97 assert `authority.playbook_selection_allowed is False`; L98 assert `authority.capital_sizing_allowed is False`; L99 assert `authority.broker_execution_allowed is False`; L100 assert `authority.direct_workbook_runtime_read_allowed is False`; L104 raises `pytest.raises(ValidationError)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The file executes exact 30/50 and caller-authored 25/45 VIX policies without a current governing proposition; its coefficient refs point to posture-owned 24/32 records, while migration authority is created by caller labels. Default-deny validators are useful but do not prove runtime non-authority.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `boundary`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `4/4`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
