# Reconstructed semantic receipt — `tests/tier_a/options_flow_history/test_options_flow_history_replay_live_state_separation.py`

- Sequence `112`, PM-015; test SHA-256 `e59b0860085386b9b673c52b81ca87bd5030e82e44c13501aa1e42c7bafc30a5`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: repository paths, fixtures and standard-library helpers referenced directly by the test.
- Surviving decision summary: Three distinct import paths prove coexistence only; no replay/live-state relationship, dependency, data flow or side effect is exercised.

## Complete test restatement

- Lines `15-18` `test_options_flow_history_replay_stays_separate_from_live_trade_state`: executes the named specimen/boundary and observes checks at lines `16, 17, 18`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_options_flow_history_replay_stays_separate_from_live_trade_state`

- Test locator: `tests/tier_a/options_flow_history/test_options_flow_history_replay_live_state_separation.py:15-18`. Checks: L16 assert `_require_module("nvda_desk.repositories.options_flow_history_repository").__name__ == "nvda_desk.repositories.options_flow_history_repository"`; L17 assert `_require_module("nvda_desk.services.options_flow_context_service").__name__ == "nvda_desk.services.options_flow_context_service"`; L18 assert `_require_module("nvda_desk.downstream.state_reader").__name__ == "nvda_desk.downstream.state_reader"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is presence/coexistence evidence only and has no sufficient semantic fit to justify retention as a governing proof.
- What is not proved: Three distinct import paths prove coexistence only; no replay/live-state relationship, dependency, data flow or side effect is exercised.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `no_semantic_fit`; proof strength `replay`; file disposition `RETIREMENT_RECOMMENDED_NOT_EXECUTED`.

## File decision

- Assertion groups/relationships `1/1`; final `RETIREMENT_RECOMMENDED_NOT_EXECUTED`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
