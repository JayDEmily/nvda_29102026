# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_family_aggregation.py`

- Sequence `068`, PM-014; test SHA-256 `70e62e76e8b1fcb7185d98950192c2eaa14cf0f89eb060a426eea11af5f57a58`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.parallel_risk: RiskAtomState; nvda_desk.domain.parallel_risk.family_aggregation: aggregate_risk_family_states.
- Surviving decision summary: manual_receipt_complete_deterministic_family_formula_specimen_but_no_current_authority_for_taxonomy_aggregation_or_empty_state_semantics

## Complete test restatement

- Lines `19-33` `test_family_aggregation_uses_highest_state_and_max_intensity_without_action_authority`: executes the named specimen/boundary and observes checks at lines `29, 30, 31, 32, 33`. The exact assertions are enumerated in the relationship sections below.
- Lines `36-37` `test_family_aggregation_empty_atoms_returns_empty_list`: executes the named specimen/boundary and observes checks at lines `37`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_family_aggregation_uses_highest_state_and_max_intensity_without_action_authority`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_family_aggregation.py:19-33`. Checks: L29 assert `by_family["calendar_event"].state == "caution"`; L30 assert `by_family["calendar_event"].intensity == 0.7`; L31 assert `by_family["calendar_event"].confidence == 0.6`; L32 assert `by_family["calendar_event"].dominant_atoms == ["a2"]`; L33 assert `by_family["operational_tooling"].state == "observe"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_deterministic_family_formula_specimen_but_no_current_authority_for_taxonomy_aggregation_or_empty_state_semantics
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `state_transition`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_family_aggregation_empty_atoms_returns_empty_list`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_family_aggregation.py:36-37`. Checks: L37 assert `aggregate_risk_family_states([]) == []`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_deterministic_family_formula_specimen_but_no_current_authority_for_taxonomy_aggregation_or_empty_state_semantics
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `2/2`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
