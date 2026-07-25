# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py`

- Sequence `080`, PM-014; test SHA-256 `4aa69a638fc8264c87251adb074332684c7b760fc60b0d37b210af55f43dc15f`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.config.parallel_risk_signal_inventory: ParallelRiskSignalInventoryService; nvda_desk.contracts.parallel_risk: ParallelRiskSignalInventoryDocument, parallel_risk_signal_inventory_document_from_dict.
- Surviving decision summary: General workbook-to-typed-config path is governed, but this 23-record inventory and six required signals are planning/config semantics; test checks hash length/ref strings rather than promotion content and only narrowly observes Path.read_text I/O.

## Complete test restatement

- Lines `35-51` `test_parallel_risk_signal_inventory_config_loads_and_validates`: executes the named specimen/boundary and observes checks at lines `38, 39, 40, 41, 42, 43, 44`. The exact assertions are enumerated in the relationship sections below.
- Lines `54-60` `test_parallel_risk_signal_inventory_config_preserves_workbook_lineage`: executes the named specimen/boundary and observes checks at lines `57, 59, 60`. The exact assertions are enumerated in the relationship sections below.
- Lines `63-82` `test_parallel_risk_signal_inventory_runtime_loader_does_not_read_workbook`: executes the named specimen/boundary and observes checks at lines `69, 76, 77, 82`. The exact assertions are enumerated in the relationship sections below.
- Lines `85-90` `test_parallel_risk_signal_inventory_invalid_status_fails`: executes the named specimen/boundary and observes checks at lines `89`. The exact assertions are enumerated in the relationship sections below.
- Lines `93-98` `test_parallel_risk_signal_inventory_missing_required_field_fails`: executes the named specimen/boundary and observes checks at lines `97`. The exact assertions are enumerated in the relationship sections below.
- Lines `101-119` `test_parallel_risk_signal_inventory_does_not_introduce_trade_authority`: executes the named specimen/boundary and observes checks at lines `108, 111, 112, 113, 114, 118`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_parallel_risk_signal_inventory_config_loads_and_validates`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:35-51`. Checks: L38 assert `isinstance(document, ParallelRiskSignalInventoryDocument)`; L39 assert `document.inventory_id == "parallel_risk_signal_inventory.v1"`; L40 assert `document.source_workbook_path == str(WORKBOOK)`; L41 assert `document.source_workbook_sheet == "Parallel Risk Lane Signal Inventory"`; L42 assert `document.direct_workbook_runtime_read_allowed is False`; L43 assert `document.authority_flags.direct_workbook_runtime_read_allowed is False`; L44 assert `{record.signal_id for record in document.required_runtime_records()} == { "source_time_utc", "scheduled_event_window_active", "vix_level", "spot_price", "front_dte", "next_dte", }`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: General workbook-to-typed-config path is governed, but this 23-record inventory and six required signals are planning/config semantics; test checks hash length/ref strings rather than promotion content and only narrowly observes Path.read_text I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_parallel_risk_signal_inventory_config_preserves_workbook_lineage`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:54-60`. Checks: L57 assert `len(document.source_workbook_sha256) == 64`; L59 assert `record.workbook_lineage_refs`; L60 assert `any("Parallel Risk Lane Signal Inventory!" in ref for ref in record.workbook_lineage_refs)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: General workbook-to-typed-config path is governed, but this 23-record inventory and six required signals are planning/config semantics; test checks hash length/ref strings rather than promotion content and only narrowly observes Path.read_text I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_parallel_risk_signal_inventory_runtime_loader_does_not_read_workbook`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:63-82`. Checks: L69 assert `path.suffix != ".xlsx"`; L76 assert `len(document.records) >= 6`; L77 assert `read_paths == [CONFIG]`; L82 assert `token not in runtime_source`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: General workbook-to-typed-config path is governed, but this 23-record inventory and six required signals are planning/config semantics; test checks hash length/ref strings rather than promotion content and only narrowly observes Path.read_text I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `token_only`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G4 — `test_parallel_risk_signal_inventory_invalid_status_fails`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:85-90`. Checks: L89 raises `pytest.raises(ValidationError)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: General workbook-to-typed-config path is governed, but this 23-record inventory and six required signals are planning/config semantics; test checks hash length/ref strings rather than promotion content and only narrowly observes Path.read_text I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `boundary`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G5 — `test_parallel_risk_signal_inventory_missing_required_field_fails`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:93-98`. Checks: L97 raises `pytest.raises(ValidationError)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: General workbook-to-typed-config path is governed, but this 23-record inventory and six required signals are planning/config semantics; test checks hash length/ref strings rather than promotion content and only narrowly observes Path.read_text I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `boundary`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G6 — `test_parallel_risk_signal_inventory_does_not_introduce_trade_authority`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:101-119`. Checks: L108 assert `authority_flags[field] is False`; L111 assert `records_by_id["capital_sizing_signal"].inventory_status == "excluded"`; L112 assert `records_by_id["capital_sizing_signal"].required_for_current_atom is False`; L113 assert `records_by_id["order_instruction_signal"].inventory_status == "excluded"`; L114 assert `records_by_id["order_instruction_signal"].required_for_current_atom is False`; L118 raises `pytest.raises(ValidationError)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: General workbook-to-typed-config path is governed, but this 23-record inventory and six required signals are planning/config semantics; test checks hash length/ref strings rather than promotion content and only narrowly observes Path.read_text I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `boundary`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `6/6`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
