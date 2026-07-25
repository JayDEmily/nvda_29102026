# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py`

## File evidence

- Sequence `080`, unit `PM-014`; test SHA-256 `4aa69a638fc8264c87251adb074332684c7b760fc60b0d37b210af55f43dc15f`.
- Full reads: test `1-119`; loader `src/nvda_desk/config/parallel_risk_signal_inventory.py:1-43`; directly exercised inventory contracts `src/nvda_desk/contracts/parallel_risk.py:199-299`; YAML `config/parallel_risk_signal_inventory.v1.yaml:1-460`; workbook authority `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:1-94`; Parallel Risk seam `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Raw test result: `6 passed in 0.27s`.

## G1 — `test_parallel_risk_signal_inventory_config_loads_and_validates`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:35-51`; assertions verify typed loading, one tab name and six required records.
- Authority locator: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:1-94`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact inventory document, tab, required-record set and policy.
- Authority match: typed promotion is lawful, but reference-workbook content and current config do not self-admit exact runtime semantics.
- Behaviour proved: the current YAML validates and exposes the asserted tab and six records.
- Limitation: this proves current shape only, not semantic completeness, cell truth or governance of the required set.
- Adversarial challenge: omit a materially required signal not in the hard-coded six and all assertions remain green.
- Exact-surface falsifier: change the asserted tab or remove one asserted record so an assertion in lines `43-51` fails.
- Assertion that must fail and why: lines `38-45` fail if the YAML no longer validates into the expected document identity, workbook path/sheet or false direct-read flags, and lines `46-51` fail if the exact six required records change. The fixed six-record set cannot reveal a missing signal that was never included in the expected set.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact inventory/schema/population authority and promotion evidence.

## G2 — `test_parallel_risk_signal_inventory_config_preserves_workbook_lineage`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:54-60`; assertions require document and record workbook lineage fields.
- Authority locator: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:1-94` and `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:58-64`.
- Authority match: preserving governed source references is a bounded lawful promotion clause, although it does not validate each referenced cell.
- Behaviour proved: every current record carries a non-empty workbook lineage reference and the document identifies the workbook.
- Limitation: references may be stale, wrong or incomplete; no cell-level reconciliation is performed.
- Adversarial challenge: point all records to the same incorrect range and still satisfy non-empty checks.
- Exact-surface falsifier: blank the document or any record lineage field so the assertion at lines `58-60` fails.
- Assertion that must fail and why: line `57` fails if the workbook hash is not 64 characters, line `59` fails for any record with no lineage references, and line `60` fails if none of that record's references names the inventory sheet. Incorrect but non-empty cell ranges can satisfy every assertion.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; preserve as source-reference evidence and return with cell-level promotion proof.

## G3 — `test_parallel_risk_signal_inventory_runtime_loader_does_not_read_workbook`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:63-82`; monkeypatch assertions restrict loader reads to YAML and a token scan checks four workbook-reader strings.
- Authority locator: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:1-94` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Authority match: runtime must consume promoted typed authority rather than directly reading the reference workbook; the intercepted loader read is a bounded proof of this implementation path.
- Behaviour proved: the exercised loader opens only the YAML path and its source lacks four selected workbook-reader tokens.
- Limitation: imports, delegated readers, dynamic calls and other runtime paths are not comprehensively instrumented; token absence is supporting only.
- Adversarial challenge: call a workbook reader through an imported helper whose name is not in the token list.
- Exact-surface falsifier: make the loader read the XLSX path so the monkeypatch assertion in lines `63-82` fails.
- Assertion that must fail and why: the guard at line `69` fails if `Path.read_text` is invoked on an `.xlsx` path, and line `77` fails if any path other than the configured YAML was read through that method. The source-token loop adds only four-name support and would not detect a delegated or dynamically named workbook reader.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; preserve the bounded no-direct-read evidence pending complete inventory authority.

## G4 — `test_parallel_risk_signal_inventory_invalid_status_fails`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:85-90`; assertion requires an invented status to fail validation.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the accepted status vocabulary.
- Authority match: strict rejection is useful, but the test cannot establish which status set is semantically correct.
- Behaviour proved: one out-of-schema status is rejected.
- Limitation: valid-status meaning, transitions and consequences are unproved.
- Adversarial challenge: an incomplete or incorrect allowed set can still reject this invented value.
- Exact-surface falsifier: accept `invented_status` without raising `ValidationError`; the `pytest.raises` context at lines `89-90` must fail.
- Assertion that must fail and why: the `pytest.raises` context at lines `89-90` fails if `invented_status` is accepted or if validation raises a different exception type. Rejection of one invented value does not prove that the allowed status enumeration is complete or semantically correct.
- Semantic relation: `authority_missing`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after status vocabulary ownership and state-law tests.

## G5 — `test_parallel_risk_signal_inventory_missing_required_field_fails`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:93-98`; assertion requires omission of `signal_family` to fail.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact inventory-record schema.
- Authority match: required-field strictness is structurally useful but depends on an unadmitted record definition.
- Behaviour proved: the current validator rejects one record missing `signal_family`.
- Limitation: it does not prove the complete required-field set or field semantics.
- Adversarial challenge: another materially required field can remain optional without affecting this test.
- Exact-surface falsifier: accept a record with `signal_family` omitted; the `pytest.raises` context at lines `97-98` must fail.
- Assertion that must fail and why: the `pytest.raises` context at lines `97-98` fails if a record with `signal_family` removed validates successfully or raises a non-`ValidationError`. The group establishes this one required field only, not the complete mandatory schema.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact record-schema authority.

## G6 — `test_parallel_risk_signal_inventory_does_not_introduce_trade_authority`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py:101-119`; assertions cover false flags, two excluded records and rejection of one true capital flag.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact flag/exclusion schema.
- Authority match: capital/order exclusion aligns with normative Parallel Risk boundaries, and the exact true-capital override rejection is bounded evidence; the surrounding taxonomy remains unowned.
- Behaviour proved: current config carries the asserted false/excluded values and rejects one capital-authority override.
- Limitation: labels do not prove side-effect absence, and other authority shapes or synonyms are not challenged.
- Adversarial challenge: add a differently named authorised-notional field or broker callback while all assertions remain green.
- Exact-surface falsifier: permit the true capital flag or change an asserted exclusion so an assertion in lines `105-119` fails.
- Assertion that must fail and why: the loop at line `107` fails if one of the five named flags is true; lines `110-113` fail if the two exact capital/order records lose their excluded/non-required values; and lines `117-119` fail if a true `capital_sizing_allowed` override is accepted. A differently named authority field or external side effect remains outside these assertions.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `substitution`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact flag/exclusion ownership and structural authority-boundary tests.

## File decision

- Groups/relationships: `6/6`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve workbook lineage, no-direct-read and true-capital rejection as bounded evidence. Exact inventory schema, population, statuses and exclusions remain unadmitted.
