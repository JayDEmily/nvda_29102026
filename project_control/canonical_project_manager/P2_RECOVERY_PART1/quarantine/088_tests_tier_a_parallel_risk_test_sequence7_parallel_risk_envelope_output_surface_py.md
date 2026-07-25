# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_output_surface.py`

- Sequence `088`, PM-014; test SHA-256 `85e79acfadf331e7887ac9783649546661f2eca6221bc2eadbec951b25ffe0de`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.options_flow: OptionsFlowContextInput; nvda_desk.contracts.parallel_risk: ParallelRiskLanePacket; nvda_desk.contracts.regime: MarketRegimeContextInput; nvda_desk.contracts.stage_inputs: StageInputBundle; nvda_desk.contracts.temporal: TemporalContextInput, TemporalEventWindow; nvda_desk.services.parallel_risk_lane_service: ParallelRiskLaneService.
- Surviving decision summary: The output specimen proves current envelope shape and three hard-coded transformations, but those event/DTE/VIX formulas lack exact authority; the non-authority test is a seven-token scan and accepts defaulted trace/run/scenario plus missing lineage while inspecting only inner data.

## Complete test restatement

- Lines `44-73` `test_sequence7_parallel_risk_output_contains_independent_risk_envelope`: executes the named specimen/boundary and observes checks at lines `60, 61, 62, 63, 68, 69`. The exact assertions are enumerated in the relationship sections below.
- Lines `76-98` `test_sequence7_parallel_risk_output_is_not_capital_or_execution_authority`: executes the named specimen/boundary and observes checks at lines `98`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_sequence7_parallel_risk_output_contains_independent_risk_envelope`

- Test locator: `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_output_surface.py:44-73`. Checks: L60 assert `envelope["envelope_state"] == "caution"`; L61 assert `envelope["state_ladder"] == ["tight", "broad", "caution", "block"]`; L62 assert `envelope["decision_authority"] == "independent_risk_envelope_only"`; L63 assert `{item["source_family"] for item in envelope["contributions"]} == { "temporal_event_context", "options_repricing_context", "market_volatility_context", }`; L68 assert `envelope["hard_blocks"] == []`; L69 assert `set(envelope["caution_flags"]) >= { "scheduled_event_window_active", "front_term_structure_backwardation", "vix_elevated", }`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: The output specimen proves current envelope shape and three hard-coded transformations, but those event/DTE/VIX formulas lack exact authority; the non-authority test is a seven-token scan and accepts defaulted trace/run/scenario plus missing lineage while inspecting only inner data.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_sequence7_parallel_risk_output_is_not_capital_or_execution_authority`

- Test locator: `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_output_surface.py:76-98`. Checks: L98 assert `token not in payload_text`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: The output specimen proves current envelope shape and three hard-coded transformations, but those event/DTE/VIX formulas lack exact authority; the non-authority test is a seven-token scan and accepts defaulted trace/run/scenario plus missing lineage while inspecting only inner data.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `token_only`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `2/2`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
