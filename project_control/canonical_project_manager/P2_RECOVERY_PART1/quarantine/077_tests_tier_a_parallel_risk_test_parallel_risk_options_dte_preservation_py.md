# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_options_dte_preservation.py`

- Sequence `077`, PM-014; test SHA-256 `453d115bd67151d8f81f564a7e4efa9c15b46a5203cd473d717d9b5b8c234605`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.options_flow: OptionsFlowContextInput; nvda_desk.contracts.parallel_risk: ParallelRiskPreparationPacket; nvda_desk.contracts.regime: MarketRegimeContextInput; nvda_desk.contracts.temporal: TemporalContextInput; nvda_desk.domain.parallel_risk.environment_assessment: assess_risk_envelope.
- Surviving decision summary: The exact front_dte > next_dte caution/flag/family mapping is current implementation and planning observation only; no normative options evidence, formula, policy version or missing/degraded semantics governs it.

## Complete test restatement

- Lines `12-23` `test_front_dte_greater_than_next_dte_preserves_options_repricing_caution`: executes the named specimen/boundary and observes checks at lines `21, 22, 23`. The exact assertions are enumerated in the relationship sections below.
- Lines `26-33` `test_front_dte_not_greater_than_next_dte_does_not_create_legacy_caution`: executes the named specimen/boundary and observes checks at lines `33`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_front_dte_greater_than_next_dte_preserves_options_repricing_caution`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_options_dte_preservation.py:12-23`. Checks: L21 assert `envelope.envelope_state == "caution"`; L22 assert `envelope.caution_flags == ["front_term_structure_backwardation"]`; L23 assert `[c.source_family for c in envelope.contributions] == ["options_repricing_context"]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The exact front_dte > next_dte caution/flag/family mapping is current implementation and planning observation only; no normative options evidence, formula, policy version or missing/degraded semantics governs it.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_front_dte_not_greater_than_next_dte_does_not_create_legacy_caution`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_options_dte_preservation.py:26-33`. Checks: L33 assert `assess_risk_envelope(packet).envelope_state == "tight"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The exact front_dte > next_dte caution/flag/family mapping is current implementation and planning observation only; no normative options evidence, formula, policy version or missing/degraded semantics governs it.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `2/2`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
