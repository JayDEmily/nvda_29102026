# Reconstructed semantic receipt — `tests/tier_a/downstream_runtime/test_fwd016_daily_pnl_reporting_contract.py`

- Sequence `103`, PM-015; test SHA-256 `46da6c6be351ea4fc083fc5b979e8d960e50f20c9e7767260961e4e89bf54629`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.api.app: create_app; nvda_desk.contracts.daily_pnl: DailyPnlReport; nvda_desk.downstream.daily_pnl: DailyPnlReportService.
- Surviving decision summary: Arithmetic and process-memory storage are proved, but no current proposition defines Daily P&L ownership, source evidence, valuation cut-off, economic identity, correction or persistence semantics.

## Complete test restatement

- Lines `11-26` `test_daily_pnl_report_service_records_and_lists_reports_without_trading_mutation`: executes the named specimen/boundary and observes checks at lines `24, 25, 26`. The exact assertions are enumerated in the relationship sections below.
- Lines `29-37` `test_daily_pnl_report_rejects_hidden_trading_authority_payloads`: executes the named specimen/boundary and observes checks at lines `30`. The exact assertions are enumerated in the relationship sections below.
- Lines `40-55` `test_api_records_and_lists_daily_pnl_reports`: executes the named specimen/boundary and observes checks at lines `42, 54, 55`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_daily_pnl_report_service_records_and_lists_reports_without_trading_mutation`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd016_daily_pnl_reporting_contract.py:11-26`. Checks: L24 assert `report.total_pnl_usd == 100.5`; L25 assert `report.trading_decision_mutated is False`; L26 assert `service.list_reports().reports == (report,)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Arithmetic and process-memory storage are proved, but no current proposition defines Daily P&L ownership, source evidence, valuation cut-off, economic identity, correction or persistence semantics.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `state_transition`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G2 — `test_daily_pnl_report_rejects_hidden_trading_authority_payloads`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd016_daily_pnl_reporting_contract.py:29-37`. Checks: L30 raises `pytest.raises(ValidationError, match="trading authority")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Arithmetic and process-memory storage are proved, but no current proposition defines Daily P&L ownership, source evidence, valuation cut-off, economic identity, correction or persistence semantics.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `boundary`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## G3 — `test_api_records_and_lists_daily_pnl_reports`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd016_daily_pnl_reporting_contract.py:40-55`. Checks: L42 assert `{"record_daily_pnl_report", "list_daily_pnl_reports"}.issubset(app.route_handlers)`; L54 assert `result["total_pnl_usd"] == 12.5`; L55 assert `app.list_daily_pnl_reports()[0]["report_id"] == "api-pnl-1"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: no exact current normative proposition was established for the material policy, taxonomy, threshold, inventory or lifecycle meaning promoted by this file. Passing implementation behaviour therefore remains observation rather than Tier-A authority proof.
- What is not proved: Arithmetic and process-memory storage are proved, but no current proposition defines Daily P&L ownership, source evidence, valuation cut-off, economic identity, correction or persistence semantics.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `authority_missing`; proof strength `state_transition`; file disposition `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.

## File decision

- Assertion groups/relationships `3/3`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
