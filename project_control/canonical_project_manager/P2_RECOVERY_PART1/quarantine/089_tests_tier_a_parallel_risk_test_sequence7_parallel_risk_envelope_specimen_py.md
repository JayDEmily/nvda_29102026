# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py`

- Sequence `089`, PM-014; test SHA-256 `f037de5d9a1116e1e5cbe3ba0a8850c1be9281b003e0cb8a2d37e3884898fbe7`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: repository paths, fixtures and standard-library helpers referenced directly by the test.
- Surviving decision summary: The test checks literals in a hand-maintained specimen but never validates or generates it. It ignores null/empty lineage, default identity, false-valid generic validation, quarantined stage-state semantics and wrong output-model extension names; non-authority is a specimen-controlled envelope token list.

## Complete test restatement

- Lines `14-33` `test_sequence7_expected_parallel_risk_envelope_specimen_is_bounded`: executes the named specimen/boundary and observes checks at lines `21, 22, 23, 24, 25, 33`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_sequence7_expected_parallel_risk_envelope_specimen_is_bounded [part A]`

- Test locator: `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py:14-23`. Checks: L21 assert `packet["packetrole"] == "parallel_risk_packet"`; L22 assert `packet["producer"]["grammar_role"] == "parallel_risk_lane"`; L23 assert `envelope["state_ladder"] == ["tight", "broad", "caution", "block"]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: The test checks literals in a hand-maintained specimen but never validates or generates it. It ignores null/empty lineage, default identity, false-valid generic validation, quarantined stage-state semantics and wrong output-model extension names; non-authority is a specimen-controlled envelope token list.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_sequence7_expected_parallel_risk_envelope_specimen_is_bounded [part B]`

- Test locator: `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py:24-33`. Checks: L24 assert `envelope["decision_authority"] == "independent_risk_envelope_only"`; L25 assert `{item["source_family"] for item in envelope["contributions"]} == { "temporal_event_context", "options_repricing_context", "market_volatility_context", }`; L33 assert `token not in forbidden_text`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: The test checks literals in a hand-maintained specimen but never validates or generates it. It ignores null/empty lineage, default identity, false-valid generic validation, quarantined stage-state semantics and wrong output-model extension names; non-authority is a specimen-controlled envelope token list.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `2/2`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
