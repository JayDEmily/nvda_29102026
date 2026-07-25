# Semantic receipt — `tests/tier_a/downstream_runtime/test_fwd016_daily_pnl_reporting_contract.py`

## File evidence

- Sequence `103`, unit `PM-015`; test SHA-256 `46da6c6be351ea4fc083fc5b979e8d960e50f20c9e7767260961e4e89bf54629`.
- Full reads: test `1-55`; complete contracts `src/nvda_desk/contracts/daily_pnl.py`; complete service `src/nvda_desk/downstream/daily_pnl.py`; API methods; full normative/P1 search found no Daily P&L owner or reporting contract.
- Raw test result: `3 passed in 0.24s`.

## G1 — `test_daily_pnl_report_service_records_and_lists_reports_without_trading_mutation`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd016_daily_pnl_reporting_contract.py:11-26`; one caller-built report is added and arithmetic/list output is asserted.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP`.
- Authority match: no current normative proposition or P1 concept defines Daily P&L ownership, economic identity, source evidence, valuation time, correction or reporting lifecycle.
- Behaviour proved: the model computes `realised + unrealised - fees`, preserves a false mutation flag and the process-memory service lists the stored copy.
- Limitation: evidence IDs are optional and unauthenticated; trade date is untyped text; positions, fills, prices, fees, currency, valuation cut-off, realised/unrealised classification, correction, sequence and persistence are unproved.
- Adversarial challenge: submit arbitrary numbers with no evidence IDs and a malformed date; the test still records a plausible-looking total.
- Exact-surface falsifier: change the arithmetic result, mutation flag or listed tuple; an assertion at lines `24-26` must fail.
- Assertion that must fail and why: at test lines `24-26`, changing the computed sum from `100.5`, allowing the mutation flag to become true, or failing to return the same report as the sole tuple entry breaks a direct assertion. Arbitrary economics, malformed date text and absent evidence remain accepted by this fixture.
- Semantic relation: `authority_missing`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; establish the reporting owner and source/valuation/correction contract before behavioural repair.

## G2 — `test_daily_pnl_report_rejects_hidden_trading_authority_payloads`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd016_daily_pnl_reporting_contract.py:29-37`; exact nested/top-level `order_submitted` in context is rejected.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP`; reporting-only separation is sensible but no Daily P&L contract currently owns the exact surface.
- Authority match: the exact trading-key exclusion is an implementation boundary without an admitted parent reporting authority.
- Behaviour proved: one finite forbidden key triggers validation failure.
- Limitation: aliases, other trading authority channels, invalid economics and false source evidence remain green.
- Adversarial challenge: rename the key or place authority outside `context`; the test remains green.
- Exact-surface falsifier: allow exact `order_submitted`; the `pytest.raises` assertion at lines `30-37` must fail.
- Assertion that must fail and why: at test lines `30-37`, allowing exact nested `order_submitted` makes model construction succeed and fails the expected `ValidationError`. An alias or trading authority placed outside `context` is not tested.
- Semantic relation: `authority_missing`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; retain only as provisional lexical evidence after owner admission.

## G3 — `test_api_records_and_lists_daily_pnl_reports`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd016_daily_pnl_reporting_contract.py:40-55`; two API methods are present and one caller payload is recorded/listed.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP`.
- Authority match: the API exposes the same unowned process-memory reporting surface.
- Behaviour proved: the application records and lists the asserted arithmetic result and report ID.
- Limitation: authentication, idempotency, source reconciliation, persistence, corrections, date/symbol query semantics and concurrency are unproved.
- Adversarial challenge: record fabricated P&L with no underlying fill/position evidence; all assertions remain green.
- Exact-surface falsifier: remove a route or alter the asserted total/report ID; an assertion at lines `42-55` must fail.
- Assertion that must fail and why: at test lines `42-55`, removing either named route breaks the subset assertion; changing the computed API total or first listed report ID breaks a direct equality. The API can still record unauthenticated, unsupported P&L numbers with no source reconciliation.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; no API promotion until the domain/report contract is admitted.

## File decision

- Groups/relationships: `3/3`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Arithmetic and volatile storage are observable, but Daily P&L meaning and ownership are not established.
