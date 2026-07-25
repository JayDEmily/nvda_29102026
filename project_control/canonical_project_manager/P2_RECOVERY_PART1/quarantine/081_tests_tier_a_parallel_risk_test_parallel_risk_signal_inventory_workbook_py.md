# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py`

- Sequence `081`, PM-014; test SHA-256 `e5ef45cf61d5a3b00217881684b250d9f0c64eabec88ad4f7b77a88792597767`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: repository paths, fixtures and standard-library helpers referenced directly by the test.
- Surviving decision summary: The governed workbook tab is reference-ledger observation, not normative/runtime authority; exact supported/deferred/excluded rows are planning-derived, and phrase/source scans do not prove non-advice or no workbook I/O.

## Complete test restatement

- Lines `72-79` `test_parallel_risk_signal_inventory_workbook_sheet_and_headers_exist`: executes the named specimen/boundary and observes checks at lines `73, 78, 79`. The exact assertions are enumerated in the relationship sections below.
- Lines `82-92` `test_parallel_risk_signal_inventory_represents_supported_runtime_signals`: executes the named specimen/boundary and observes checks at lines `85, 88, 89, 90, 91, 92`. The exact assertions are enumerated in the relationship sections below.
- Lines `95-105` `test_parallel_risk_signal_inventory_marks_rich_signals_unavailable_not_fabricated`: executes the named specimen/boundary and observes checks at lines `98, 101, 102, 103, 104, 105`. The exact assertions are enumerated in the relationship sections below.
- Lines `108-116` `test_parallel_risk_signal_inventory_excluded_authority_is_not_runtime_demanded`: executes the named specimen/boundary and observes checks at lines `113, 114, 115, 116`. The exact assertions are enumerated in the relationship sections below.
- Lines `119-130` `test_parallel_risk_signal_inventory_and_runtime_boundary_have_no_advice_or_workbook_reads`: executes the named specimen/boundary and observes checks at lines `125, 130`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_parallel_risk_signal_inventory_workbook_sheet_and_headers_exist`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py:72-79`. Checks: L73 assert `WORKBOOK.exists()`; L78 assert `REQUIRED_HEADERS <= headers`; L79 assert `len(rows) >= len(SUPPORTED_SIGNALS | DEFERRED_OR_MISSING_RICH_SIGNALS)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The governed workbook tab is reference-ledger observation, not normative/runtime authority; exact supported/deferred/excluded rows are planning-derived, and phrase/source scans do not prove non-advice or no workbook I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `presence_only`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_parallel_risk_signal_inventory_represents_supported_runtime_signals`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py:82-92`. Checks: L85 assert `SUPPORTED_SIGNALS <= set(rows)`; L88 assert `record["inventory_status"] == "available_now"`; L89 assert `record["required_for_current_atom"] == "yes"`; L90 assert `record["runtime_use_permission"] == "runtime_allowed_from_typed_inputs_only"`; L91 assert `record["lawful_prl_use"] == "yes_after_typed_promotion"`; L92 assert `record["raw_workbook_lineage_ref"] or record["derived_workbook_lineage_ref"]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The governed workbook tab is reference-ledger observation, not normative/runtime authority; exact supported/deferred/excluded rows are planning-derived, and phrase/source scans do not prove non-advice or no workbook I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_parallel_risk_signal_inventory_marks_rich_signals_unavailable_not_fabricated`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py:95-105`. Checks: L98 assert `DEFERRED_OR_MISSING_RICH_SIGNALS <= set(rows)`; L101 assert `record["inventory_status"] in {"deferred", "missing"}`; L102 assert `record["lawful_prl_use"] == "no_until_typed_source_exists"`; L103 assert `record["runtime_use_permission"] == "not_runtime_allowed"`; L104 assert `"no_value" in record["unavailable_handling"]`; L105 assert `"fabricated" in record["notes"].lower() or "lawful source" in record["notes"].lower()`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The governed workbook tab is reference-ledger observation, not normative/runtime authority; exact supported/deferred/excluded rows are planning-derived, and phrase/source scans do not prove non-advice or no workbook I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G4 — `test_parallel_risk_signal_inventory_excluded_authority_is_not_runtime_demanded`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py:108-116`. Checks: L113 assert `record["inventory_status"] == "excluded"`; L114 assert `record["required_for_current_atom"] == "no"`; L115 assert `record["unavailable_handling"] == "excluded_signal_not_demanded"`; L116 assert `record["exclusion_reason"]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The governed workbook tab is reference-ledger observation, not normative/runtime authority; exact supported/deferred/excluded rows are planning-derived, and phrase/source scans do not prove non-advice or no workbook I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `behavioural`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G5 — `test_parallel_risk_signal_inventory_and_runtime_boundary_have_no_advice_or_workbook_reads`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py:119-130`. Checks: L125 assert `forbidden not in workbook_text`; L130 assert `token not in runtime_text`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: The governed workbook tab is reference-ledger observation, not normative/runtime authority; exact supported/deferred/excluded rows are planning-derived, and phrase/source scans do not prove non-advice or no workbook I/O.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `token_only`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `5/5`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
