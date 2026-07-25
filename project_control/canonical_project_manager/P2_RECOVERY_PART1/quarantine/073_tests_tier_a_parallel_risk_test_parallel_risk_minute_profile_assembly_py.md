# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_assembly.py`

- Sequence `073`, PM-014; test SHA-256 `5d277b38d12979ac5014e81ca9512711b01634b0e894a2ad612f0ff9e16ee445`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.options_flow: OptionsFlowContextInput; nvda_desk.contracts.parallel_risk: FreshnessRegisterEntry, ParallelRiskMinuteProfile; nvda_desk.contracts.parallel_risk: ParallelRiskPreparationPacket; nvda_desk.contracts.regime: MarketRegimeContextInput; nvda_desk.contracts.temporal: TemporalContextInput, TemporalEventWindow; nvda_desk.domain.parallel_risk.minute_profile_assembly: assemble_parallel_risk_minute_profile.
- Surviving decision summary: manual_receipt_complete_thin_envelope_and_carriage_fragments_preserved_but_minute_profile_atom_family_register_design_is_planning_only_and_non_authority_is_token_declarative

## Complete test restatement

- Lines `13-67` `test_minute_profile_assembly_preserves_current_envelope_and_authority_flags`: executes the named specimen/boundary and observes checks at lines `48, 49, 50, 51, 52, 57, 64, 65, 66, 67`. The exact assertions are enumerated in the relationship sections below.
- Lines `70-83` `test_minute_profile_assembly_contains_no_trade_action_fields`: executes the named specimen/boundary and observes checks at lines `83`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_minute_profile_assembly_preserves_current_envelope_and_authority_flags`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_assembly.py:13-67`. Checks: L48 assert `isinstance(profile, ParallelRiskMinuteProfile)`; L49 assert `profile.risk_envelope_state == "caution"`; L50 assert `profile.authority_flags.candidate_formation_allowed is False`; L51 assert `profile.authority_flags.capital_sizing_allowed is False`; L52 assert `{atom.family for atom in profile.active_risk_atoms} >= { "temporal_event_context", "market_volatility_context", "options_repricing_context", }`; L57 assert `{entry.signal_id for entry in profile.signal_snapshot} >= { "source_time_utc", "vix_level", "spot_price", "front_dte", "next_dte", }`; L64 assert `profile.lineage["parent_packet_ids"] == ["parent-1"]`; L65 assert `profile.lineage["dependency_packet_ids"] == ["dep-1"]`; L66 assert `profile.lineage["source_artifact_ids"] == ["artifact-1"]`; L67 assert `profile.lineage["forbidden_authority_keys_consumed"] == []`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_thin_envelope_and_carriage_fragments_preserved_but_minute_profile_atom_family_register_design_is_planning_only_and_non_authority_is_token_declarative
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_minute_profile_assembly_contains_no_trade_action_fields`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_assembly.py:70-83`. Checks: L83 assert `forbidden not in payload`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_thin_envelope_and_carriage_fragments_preserved_but_minute_profile_atom_family_register_design_is_planning_only_and_non_authority_is_token_declarative
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `token_only`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `2/2`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
