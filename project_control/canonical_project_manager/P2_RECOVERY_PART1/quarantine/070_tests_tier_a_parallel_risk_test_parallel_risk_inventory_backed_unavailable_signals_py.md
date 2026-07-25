# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py`

- Sequence `070`, PM-014; test SHA-256 `228af73e016443281bc6086363c3a56a94ff4cb84b8bf86a0c61652da1260541`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.config.parallel_risk_signal_inventory: ParallelRiskSignalInventoryService; nvda_desk.domain.parallel_risk.unavailable_signals: build_inventory_backed_unavailable_signals.
- Surviving decision summary: manual_receipt_complete_non_fabrication_and_state_specimens_preserved_but_inventory_rows_policies_promotion_and_authority_blacklists_lack_current_authority

## Complete test restatement

- Lines `17-30` `test_inventory_backed_unavailable_signals_marks_present_and_missing_expected`: executes the named specimen/boundary and observes checks at lines `24, 25, 27, 28`. The exact assertions are enumerated in the relationship sections below.
- Lines `33-55` `test_inventory_backed_deferred_rich_signals_are_unavailable_not_fabricated`: executes the named specimen/boundary and observes checks at lines `51, 52, 53, 54, 55`. The exact assertions are enumerated in the relationship sections below.
- Lines `58-67` `test_inventory_backed_excluded_signals_are_not_demanded_at_runtime`: executes the named specimen/boundary and observes checks at lines `64, 65, 66, 67`. The exact assertions are enumerated in the relationship sections below.
- Lines `70-85` `test_inventory_backed_unavailable_not_yet_sourced_and_quarantine_states`: executes the named specimen/boundary and observes checks at lines `79, 80, 81, 83, 84, 85`. The exact assertions are enumerated in the relationship sections below.
- Lines `88-108` `test_inventory_backed_unavailable_signals_are_state_of_play_not_action_language`: executes the named specimen/boundary and observes checks at lines `108`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_inventory_backed_unavailable_signals_marks_present_and_missing_expected`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py:17-30`. Checks: L24 assert `result.presence_by_signal_id["source_time_utc"] == "present"`; L25 assert `result.presence_by_signal_id["vix_level"] == "missing"`; L27 assert `missing["vix_level"].impact_on_profile == "lowers_confidence"`; L28 assert `missing["vix_level"].expected_signal_inventory_ref == ( "parallel_risk_signal_inventory.v1#vix_level" )`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_non_fabrication_and_state_specimens_preserved_but_inventory_rows_policies_promotion_and_authority_blacklists_lack_current_authority
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_inventory_backed_deferred_rich_signals_are_unavailable_not_fabricated`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py:33-55`. Checks: L51 assert `"dense_options_chain" in deferred_snapshot`; L52 assert `"gamma_exposure_flip" in deferred_snapshot`; L53 assert `deferred_snapshot["dense_options_chain"].value is None`; L54 assert `deferred_snapshot["dense_options_chain"].lawful_prl_use_allowed is False`; L55 assert `"fabricated" not in str(deferred_snapshot["dense_options_chain"].value).lower()`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_non_fabrication_and_state_specimens_preserved_but_inventory_rows_policies_promotion_and_authority_blacklists_lack_current_authority
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_inventory_backed_excluded_signals_are_not_demanded_at_runtime`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py:58-67`. Checks: L64 assert `result.presence_by_signal_id["capital_sizing_signal"] == "excluded"`; L65 assert `result.presence_by_signal_id["order_instruction_signal"] == "excluded"`; L66 assert `"capital_sizing_signal" not in {entry.signal_id for entry in result.signal_snapshot}`; L67 assert `"order_instruction_signal" not in {entry.signal_id for entry in result.missing_signal_register}`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_non_fabrication_and_state_specimens_preserved_but_inventory_rows_policies_promotion_and_authority_blacklists_lack_current_authority
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G4 — `test_inventory_backed_unavailable_not_yet_sourced_and_quarantine_states`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py:70-85`. Checks: L79 assert `states["regime_context_packet"] == "unavailable"`; L80 assert `states["vix_level"] == "quarantined"`; L81 assert `states["front_dte"] == "rejected"`; L83 assert `entries["regime_context_packet"].value is None`; L84 assert `entries["vix_level"].value is None`; L85 assert `entries["front_dte"].value is None`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_non_fabrication_and_state_specimens_preserved_but_inventory_rows_policies_promotion_and_authority_blacklists_lack_current_authority
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `state_transition`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G5 — `test_inventory_backed_unavailable_signals_are_state_of_play_not_action_language`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py:88-108`. Checks: L108 assert `forbidden not in payload`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: manual_receipt_complete_non_fabrication_and_state_specimens_preserved_but_inventory_rows_policies_promotion_and_authority_blacklists_lack_current_authority
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `token_only`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `5/5`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
