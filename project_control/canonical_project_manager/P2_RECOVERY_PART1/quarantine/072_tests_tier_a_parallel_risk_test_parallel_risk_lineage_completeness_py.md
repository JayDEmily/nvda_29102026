# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py`

- Sequence `072`, PM-014; test SHA-256 `ffd8934f8f549f54e71048ea26a03ea6210491dcb1f3bd3402846560a507c07b`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.options_flow: OptionsFlowContextInput; nvda_desk.contracts.parallel_risk: EventProximityRegisterEntry, FreshnessRegisterEntry; nvda_desk.contracts.parallel_risk: ParallelRiskPreparationPacket; nvda_desk.contracts.regime: MarketRegimeContextInput; nvda_desk.contracts.stage_inputs: StageInputBundle; nvda_desk.contracts.temporal: TemporalContextInput; nvda_desk.domain.parallel_risk.minute_profile_assembly: assemble_parallel_risk_minute_profile; nvda_desk.services.parallel_risk_lane_service: ParallelRiskLaneService.
- Surviving decision summary: manual_receipt_complete_partial_string_carriage_preserved_but_lineage_completeness_retrievability_fingerprint_versions_and_non_authority_are_unproved

## Complete test restatement

- Lines `13-66` `test_minute_profile_lineage_preserves_packet_ids_source_refs_and_forbidden_authority_trace`: executes the named specimen/boundary and observes checks at lines `48, 49, 50, 51, 52, 53, 54, 60, 63, 66`. The exact assertions are enumerated in the relationship sections below.
- Lines `69-91` `test_service_optional_profile_carries_lineage_without_hidden_authority`: executes the named specimen/boundary and observes checks at lines `87, 88, 89, 90, 91`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_minute_profile_lineage_preserves_packet_ids_source_refs_and_forbidden_authority_trace [part A]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py:13-52`. Checks: L48 assert `profile.lineage["bootstrap_source"] == "stage_input_bundle.parallel_risk_primitives"`; L49 assert `profile.lineage["parent_packet_ids"] == ["parent-packet"]`; L50 assert `profile.lineage["dependency_packet_ids"] == ["dependency-packet"]`; L51 assert `profile.lineage["source_artifact_ids"] == ["source-artifact"]`; L52 assert `profile.lineage["input_fingerprint"] == "sha256:fixture"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_partial_string_carriage_preserved_but_lineage_completeness_retrievability_fingerprint_versions_and_non_authority_are_unproved
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_minute_profile_lineage_preserves_packet_ids_source_refs_and_forbidden_authority_trace [part B]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py:53-66`. Checks: L53 assert `profile.lineage["forbidden_authority_keys_consumed"] == []`; L54 assert `profile.lineage["admitted_semantic_inputs"] == [ "temporal_input", "regime_input", "options_flow_input", ]`; L60 assert `{"source-artifact"} <= set().union( *(set(entry.lineage_refs) for entry in profile.signal_snapshot) )`; L63 assert `{"market-data-lineage:vix", "calendar-lineage:earnings-nvda"} <= set().union( *(set(atom.source_refs) for atom in profile.active_risk_atoms) )`; L66 assert `all(family.dominant_atoms for family in profile.risk_family_states)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_partial_string_carriage_preserved_but_lineage_completeness_retrievability_fingerprint_versions_and_non_authority_are_unproved
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_service_optional_profile_carries_lineage_without_hidden_authority [part A]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py:69-89`. Checks: L87 assert `profile.lineage["source_artifact_ids"] == ["service-source-artifact"]`; L88 assert `profile.lineage["input_fingerprint"] == "sha256:service-fixture"`; L89 assert `profile.lineage["forbidden_authority_keys_consumed"] == []`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_partial_string_carriage_preserved_but_lineage_completeness_retrievability_fingerprint_versions_and_non_authority_are_unproved
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G4 — `test_service_optional_profile_carries_lineage_without_hidden_authority [part B]`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py:90-91`. Checks: L90 assert `profile.authority_flags.direct_workbook_runtime_read_allowed is False`; L91 assert `profile.authority_flags.capital_sizing_allowed is False`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: manual_receipt_complete_partial_string_carriage_preserved_but_lineage_completeness_retrievability_fingerprint_versions_and_non_authority_are_unproved
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `4/4`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
