# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_unavailable_signals.py`

- Sequence `084`, PM-014; test SHA-256 `16f79d6a2f90151a4415b01aee0ee09af5f23e2a61b578d93ff152daedea0dcc`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.domain.parallel_risk.unavailable_signals: build_unavailable_signal_snapshot_entry, build_unavailable_signal_watch_entry.
- Surviving decision summary: No current proposition admits the expected-signal inventory, named future signals, absence/freshness/use taxonomy or impact policy; the no-value specimen is useful but inventory authority is caller-invented, one supplied inventory reference is discarded, and non-action is a three-word scan.

## Complete test restatement

- Lines `9-23` `test_unavailable_signal_snapshot_marks_future_signal_without_fabricated_value`: executes the named specimen/boundary and observes checks at lines `18, 19, 20, 21, 22, 23`. The exact assertions are enumerated in the relationship sections below.
- Lines `26-39` `test_unavailable_signal_watch_entry_is_state_of_play_not_action`: executes the named specimen/boundary and observes checks at lines `34, 35, 37, 38, 39`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_unavailable_signal_snapshot_marks_future_signal_without_fabricated_value`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_unavailable_signals.py:9-23`. Checks: L18 assert `entry.value is None`; L19 assert `entry.missing_or_quarantined == "missing"`; L20 assert `entry.freshness_state == "unknown"`; L21 assert `entry.lawful_prl_use_allowed is False`; L22 assert `entry.lawful_prl_use_reason == "typed_runtime_signal_unavailable"`; L23 assert `entry.workbook_lineage_refs == ["Derived_Features_Catalog!A2:H2"]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: No current proposition admits the expected-signal inventory, named future signals, absence/freshness/use taxonomy or impact policy; the no-value specimen is useful but inventory authority is caller-invented, one supplied inventory reference is discarded, and non-action is a three-word scan.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_unavailable_signal_watch_entry_is_state_of_play_not_action`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_unavailable_signals.py:26-39`. Checks: L34 assert `entry.impact_on_profile == "lowers_confidence"`; L35 assert `entry.missing_reason == "dense options chain contract not yet available"`; L37 assert `"buy" not in payload`; L38 assert `"sell" not in payload`; L39 assert `"hedge" not in payload`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: No current proposition admits the expected-signal inventory, named future signals, absence/freshness/use taxonomy or impact policy; the no-value specimen is useful but inventory authority is caller-invented, one supplied inventory reference is discarded, and non-action is a three-word scan.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `token_only`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `2/2`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
