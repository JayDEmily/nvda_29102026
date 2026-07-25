# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_supported_risk_atoms.py`

- Sequence `082`, PM-014; test SHA-256 `dd2b52ed344cfb6a61535d3130eb0d9ce405ca06b4d5770d9cfc1cdcec462790`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.parallel_risk: EventProximityRegisterEntry, FreshnessRegisterEntry, MissingSignalRegisterEntry, ParallelRiskEnvelope, ParallelRiskEnvelopeContribution; nvda_desk.domain.parallel_risk.risk_atoms: build_supported_risk_atoms.
- Surviving decision summary: RiskAtomState catalogue, IDs, families, intensities/confidence and constructive/uncertainty formulas are planning-only; advice-word absence does not prove non-trading authority and generated_at is unused.

## Complete test restatement

- Lines `15-72` `test_supported_risk_atoms_wrap_current_environmental_inputs_without_trade_actions`: executes the named specimen/boundary and observes checks at lines `62, 69, 72`. The exact assertions are enumerated in the relationship sections below.
- Lines `75-93` `test_supported_risk_atoms_preserve_constructive_and_uncertainty_semantics`: executes the named specimen/boundary and observes checks at lines `91, 92, 93`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_supported_risk_atoms_wrap_current_environmental_inputs_without_trade_actions`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_supported_risk_atoms.py:15-72`. Checks: L62 assert `ids >= { "freshness:vix_level", "signal_availability:vwap_distance", "event_proximity:earnings-nvda", "envelope:market_volatility_context:vix_elevated", "envelope:options_repricing_context:front_term_structure_backwardation", }`; L69 assert `all(atom.why_this_is_risk_not_play for atom in atoms)`; L72 assert `forbidden not in serialized`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: RiskAtomState catalogue, IDs, families, intensities/confidence and constructive/uncertainty formulas are planning-only; advice-word absence does not prove non-trading authority and generated_at is unused.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_supported_risk_atoms_preserve_constructive_and_uncertainty_semantics`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_supported_risk_atoms.py:75-93`. Checks: L91 assert `atom.state == "observe"`; L92 assert `atom.calculation_basis["risk_side"] == "constructive"`; L93 assert `atom.confidence > 0.0`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: RiskAtomState catalogue, IDs, families, intensities/confidence and constructive/uncertainty formulas are planning-only; advice-word absence does not prove non-trading authority and generated_at is unused.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `2/2`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
