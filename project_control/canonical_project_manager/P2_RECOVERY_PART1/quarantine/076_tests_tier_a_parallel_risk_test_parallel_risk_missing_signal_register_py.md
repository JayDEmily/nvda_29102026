# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py`

- Sequence `076`, PM-014; test SHA-256 `c9e3aeec29f40d43f487f42acf459793679f1fcee402683e5a59c97c6a94fecc`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.upstream_signal: RawUpstreamSignalInput; nvda_desk.domain.parallel_risk.missing_signals: build_missing_signal_register_entry, signal_snapshot_from_upstream_ingress_result; nvda_desk.upstream.raw_signal_ingress: ingest_raw_upstream_signal.
- Surviving decision summary: Test codifies direct raw-ingress-result-to-PRL cognition, caller-set admission and silent source-payload stripping, bypassing governed prepared ingress and source-preservation law; missing-register policy is also planning-only.

## Complete test restatement

- Lines `11-25` `test_missing_signal_register_entry_is_metadata_only_and_lowers_confidence`: executes the named specimen/boundary and observes checks at lines `21, 22, 23, 24, 25`. The exact assertions are enumerated in the relationship sections below.
- Lines `28-48` `test_quarantined_upstream_signal_becomes_snapshot_absence_not_runtime_signal_value`: executes the named specimen/boundary and observes checks at lines `42, 43, 44, 45, 46, 47, 48`. The exact assertions are enumerated in the relationship sections below.
- Lines `51-70` `test_admitted_trace_only_signal_snapshot_does_not_strip_trace_lineage`: executes the named specimen/boundary and observes checks at lines `65, 66, 67, 68, 69, 70`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_missing_signal_register_entry_is_metadata_only_and_lowers_confidence`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py:11-25`. Checks: L21 assert `entry.impact_on_profile == "lowers_confidence"`; L22 assert `entry.expected_signal_inventory_ref == "workbook#Parallel Risk Lane Signal Inventory"`; L23 assert `entry.workbook_lineage_refs == ["Raw_Primitives_Catalog!A1:H49"]`; L24 assert `"trade" not in entry.model_dump_json()`; L25 assert `"order" not in entry.model_dump_json()`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Test codifies direct raw-ingress-result-to-PRL cognition, caller-set admission and silent source-payload stripping, bypassing governed prepared ingress and source-preservation law; missing-register policy is also planning-only.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_quarantined_upstream_signal_becomes_snapshot_absence_not_runtime_signal_value`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py:28-48`. Checks: L42 assert `result.quarantined is True`; L43 assert `entry.signal_id == "headline_feed"`; L44 assert `entry.signal_family == "headline_feed"`; L45 assert `entry.value is None`; L46 assert `entry.missing_or_quarantined == "quarantined"`; L47 assert `entry.rejection_reason == "signal_family_not_admitted"`; L48 assert `entry.lawful_prl_use_allowed is False`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Test codifies direct raw-ingress-result-to-PRL cognition, caller-set admission and silent source-payload stripping, bypassing governed prepared ingress and source-preservation law; missing-register policy is also planning-only.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_admitted_trace_only_signal_snapshot_does_not_strip_trace_lineage`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py:51-70`. Checks: L65 assert `result.quarantined is False`; L66 assert `entry.missing_or_quarantined == "present"`; L67 assert `entry.value == {"value": 31.0, "units": "index_level"}`; L68 assert `entry.source_ids == ["source-2"]`; L69 assert `entry.lawful_prl_use_allowed is True`; L70 assert `"trade_allowed" not in str(entry.value)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Test codifies direct raw-ingress-result-to-PRL cognition, caller-set admission and silent source-payload stripping, bypassing governed prepared ingress and source-preservation law; missing-register policy is also planning-only.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `3/3`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
