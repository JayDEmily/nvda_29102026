# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py`

- Sequence `086`, PM-014; test SHA-256 `35dfc0957c1f288e4aa1fb3f0b3f75fa8280b875ae5e932e982cf5ecdbcf5856`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.options_flow: OptionsFlowContextInput; nvda_desk.contracts.parallel_risk: ParallelRiskPreparationPacket; nvda_desk.contracts.regime: MarketRegimeContextInput; nvda_desk.contracts.temporal: TemporalContextInput; nvda_desk.domain.parallel_risk.environment_assessment: assess_risk_envelope.
- Surviving decision summary: The test faithfully locks the hard-coded inclusive 30/50 implementation, but no current proposition admits those PRL thresholds, flags or default policy; the related coefficient records are posture-owned 24/32, and incomplete/fabricated VIX input is not distinguished.

## Complete test restatement

- Lines `20-25` `test_vix_30_caution_threshold_is_preserved_as_compatibility_mode`: executes the named specimen/boundary and observes checks at lines `23, 24, 25`. The exact assertions are enumerated in the relationship sections below.
- Lines `28-33` `test_vix_50_block_threshold_is_preserved_as_compatibility_mode`: executes the named specimen/boundary and observes checks at lines `31, 32, 33`. The exact assertions are enumerated in the relationship sections below.
- Lines `36-40` `test_subthreshold_vix_does_not_create_legacy_caution`: executes the named specimen/boundary and observes checks at lines `39, 40`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_vix_30_caution_threshold_is_preserved_as_compatibility_mode`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py:20-25`. Checks: L23 assert `envelope.envelope_state == "caution"`; L24 assert `"vix_elevated" in envelope.caution_flags`; L25 assert `envelope.hard_blocks == []`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The test faithfully locks the hard-coded inclusive 30/50 implementation, but no current proposition admits those PRL thresholds, flags or default policy; the related coefficient records are posture-owned 24/32, and incomplete/fabricated VIX input is not distinguished.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_vix_50_block_threshold_is_preserved_as_compatibility_mode`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py:28-33`. Checks: L31 assert `envelope.envelope_state == "block"`; L32 assert `"vix_elevated" in envelope.caution_flags`; L33 assert `envelope.hard_blocks == ["vix_extreme"]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The test faithfully locks the hard-coded inclusive 30/50 implementation, but no current proposition admits those PRL thresholds, flags or default policy; the related coefficient records are posture-owned 24/32, and incomplete/fabricated VIX input is not distinguished.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_subthreshold_vix_does_not_create_legacy_caution`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py:36-40`. Checks: L39 assert `envelope.envelope_state == "tight"`; L40 assert `envelope.contributions == []`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The test faithfully locks the hard-coded inclusive 30/50 implementation, but no current proposition admits those PRL thresholds, flags or default policy; the related coefficient records are posture-owned 24/32, and incomplete/fabricated VIX input is not distinguished.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `3/3`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
