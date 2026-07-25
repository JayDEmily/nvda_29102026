# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_service_integration.py`

- Sequence `075`, PM-014; test SHA-256 `699e93566753bafbbfdc4ccdc56553a035047532d9377f7c1afe7580fb499e89`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.options_flow: OptionsFlowContextInput; nvda_desk.contracts.parallel_risk: ParallelRiskMinuteProfile; nvda_desk.contracts.regime: MarketRegimeContextInput; nvda_desk.contracts.stage_inputs: StageInputBundle; nvda_desk.contracts.temporal: TemporalContextInput; nvda_desk.services.parallel_risk_lane_service: ParallelRiskLaneService.
- Surviving decision summary: Default two-key result is a narrow API-shape regression; the optional minute-profile product is planning-only, its unchanged-lane claim is untested, and lineage/non-authority are unverified strings/flags.

## Complete test restatement

- Lines `21-28` `test_run_bootstrap_default_result_remains_backward_compatible`: executes the named specimen/boundary and observes checks at lines `28`. The exact assertions are enumerated in the relationship sections below.
- Lines `31-50` `test_run_bootstrap_can_include_optional_minute_profile_without_changing_lane_packet`: executes the named specimen/boundary and observes checks at lines `41, 43, 44, 45, 46, 47, 48, 49, 50`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_run_bootstrap_default_result_remains_backward_compatible`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_service_integration.py:21-28`. Checks: L28 assert `set(result) == {"bootstrap_input_packet", "lane_packet"}`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Default two-key result is a narrow API-shape regression; the optional minute-profile product is planning-only, its unchanged-lane claim is untested, and lineage/non-authority are unverified strings/flags.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_run_bootstrap_can_include_optional_minute_profile_without_changing_lane_packet [part A]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_service_integration.py:31-46`. Checks: L41 assert `set(result) == {"bootstrap_input_packet", "lane_packet", "minute_profile"}`; L43 assert `isinstance(profile, ParallelRiskMinuteProfile)`; L44 assert `profile.packet_id == "dmp::parallel_risk::output::service-profile::minute_profile"`; L45 assert `profile.risk_envelope_state == "caution"`; L46 assert `profile.lineage["parent_packet_ids"] == ["dmp::parallel_risk::bootstrap_input::service-profile"]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Default two-key result is a narrow API-shape regression; the optional minute-profile product is planning-only, its unchanged-lane claim is untested, and lineage/non-authority are unverified strings/flags.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_run_bootstrap_can_include_optional_minute_profile_without_changing_lane_packet [part B]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_service_integration.py:47-50`. Checks: L47 assert `profile.lineage["dependency_packet_ids"] == ["dmp::parallel_risk::bootstrap_input::service-profile"]`; L48 assert `profile.lineage["source_artifact_ids"] == ["source-artifact-1"]`; L49 assert `profile.lineage["input_fingerprint"] == "sha256:fixture"`; L50 assert `profile.authority_flags.capital_sizing_allowed is False`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Default two-key result is a narrow API-shape regression; the optional minute-profile product is planning-only, its unchanged-lane claim is untested, and lineage/non-authority are unverified strings/flags.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `3/3`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
