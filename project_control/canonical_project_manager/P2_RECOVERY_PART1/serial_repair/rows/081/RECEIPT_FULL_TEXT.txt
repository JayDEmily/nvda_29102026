# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py`

## File evidence

- Sequence `081`, unit `PM-014`; test SHA-256 `e5ef45cf61d5a3b00217881684b250d9f0c64eabec88ad4f7b77a88792597767`.
- Full reads: test `1-130`; complete workbook sheet `Parallel Risk Lane Signal Inventory!A1:Q26` in `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`; workbook authority `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:1-94`; Parallel Risk seam `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`. The workbook is a governed reference ledger, not normative prose or direct runtime authority.
- Raw test result: `5 passed in 0.35s`.

## G1 — `test_parallel_risk_signal_inventory_workbook_sheet_and_headers_exist`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py:72-79`; assertions verify file/tab/header presence and a minimum row count.
- Authority locator: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:1-94`; `NO_VALID_AUTHORITY_RELATIONSHIP` for treating physical workbook shape as blocking semantic truth.
- Authority match: the workbook is valid reference evidence, but its tab, columns and population do not self-admit a runtime inventory contract.
- Behaviour proved: the inspected workbook currently contains the named sheet, required headers and enough non-empty rows.
- Limitation: presence and count do not prove semantic correctness, completeness, ownership or promotion status.
- Adversarial challenge: populate incorrect statuses and meanings while preserving every header and row-count assertion.
- Exact-surface falsifier: remove the sheet/header or reduce rows below the asserted minimum so an assertion at lines `73-79` fails.
- Assertion that must fail and why: at test lines `73-79`, deleting the named worksheet makes `_inventory_rows()` fail at `assert SHEET in workbook.sheetnames`; deleting a required column makes `REQUIRED_HEADERS <= headers` false; and removing enough populated signal rows makes the minimum-count comparison false. Those are the only workbook-shape claims made by this group.
- Semantic relation: `authority_missing`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact workbook-to-runtime promotion authority and semantic reconciliation.

## G2 — `test_parallel_risk_signal_inventory_represents_supported_runtime_signals`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py:82-92`; assertions check six rows, statuses, requirement/permission strings and lineage.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact supported-signal set and row taxonomies.
- Authority match: typed-input-only intent is aligned with the preparation seam, but reference rows cannot establish admitted runtime requirements.
- Behaviour proved: the six named workbook rows currently contain the asserted strings and at least one lineage reference.
- Limitation: row truth, source availability, promotion completeness and omitted required signals are unproved.
- Adversarial challenge: omit another necessary signal or cite an incorrect lineage cell while every assertion remains green.
- Exact-surface falsifier: change one asserted row status/permission or remove its lineage so an assertion at lines `85-92` fails.
- Assertion that must fail and why: at test lines `85-92`, for any of the six enumerated signal IDs, changing `inventory_status`, `required_for_current_atom`, `runtime_use_permission` or `lawful_prl_use` breaks its corresponding equality assertion; clearing both lineage cells breaks the final truthiness assertion. The test would still not notice a required signal omitted from `SUPPORTED_SIGNALS`.
- Semantic relation: `authority_missing`.
- Proof strength: `historical_observational`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after proposition-level ownership of the supported set and cell-level promotion evidence.

## G3 — `test_parallel_risk_signal_inventory_marks_rich_signals_unavailable_not_fabricated`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py:95-105`; assertions verify five rows are deferred/missing, disallowed and contain no-value/anti-fabrication text.
- Authority locator: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:1-94` and `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:66-83`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact five-signal set and consequences.
- Authority match: no fabrication and explicit absence align with preparation law, but selected workbook rows do not prove complete source unavailability or a governed downstream policy.
- Behaviour proved: the five current rows carry the asserted status and text values.
- Limitation: textual declarations are not runtime rejection proof and may be stale relative to actual source/config capability.
- Adversarial challenge: fabricate one value in runtime while leaving the workbook row unchanged.
- Exact-surface falsifier: mark one asserted row available or remove its no-value/anti-fabrication text so an assertion at lines `98-105` fails.
- Assertion that must fail and why: at test lines `98-105`, changing one of the five selected rows to an unaccepted status or permission, removing `no_value` from `unavailable_handling`, or removing both accepted note phrases makes the exact membership, equality or substring assertion fail. A runtime fabricator would not affect this workbook-only group.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `historical_observational`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return with governed source-capability decisions and behavioural non-fabrication tests.

## G4 — `test_parallel_risk_signal_inventory_excluded_authority_is_not_runtime_demanded`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py:108-116`; assertions check two excluded authority rows and their fields.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; workbook rows remain reference evidence only.
- Authority match: excluding capital sizing and order instructions aligns with the admitted Parallel Risk boundary, but the workbook does not itself enforce runtime non-demand.
- Behaviour proved: the two reference rows currently record excluded/not-demanded values and non-empty reasons.
- Limitation: no runtime consumer or schema rejection is exercised.
- Adversarial challenge: runtime can demand an order signal despite the workbook row and the test remains green.
- Exact-surface falsifier: change an asserted exclusion/not-demanded field so an assertion at lines `111-116` fails.
- Assertion that must fail and why: at test lines `111-116`, either excluded row ceases to satisfy the group when its status is not `excluded`, its current-atom requirement is not `no`, its unavailable handling is not the exact exclusion token, or its reason is blank. No runtime demand is exercised, so changing a consumer while leaving these two rows intact would remain green.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `historical_observational`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; preserve as aligned reference evidence and return with enforced runtime-boundary proof.

## G5 — `test_parallel_risk_signal_inventory_and_runtime_boundary_have_no_advice_or_workbook_reads`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py:119-130`; loops check selected advice phrases in workbook values and selected workbook-reader tokens across a bounded runtime file list.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; `NO_VALID_AUTHORITY_RELATIONSHIP` for finite token absence as complete proof of non-authority/no direct workbook reads.
- Authority match: both intended boundaries are normatively aligned, but the scan is lexical and path-bounded.
- Behaviour proved: the selected strings are absent from the inspected sheet text and selected runtime files.
- Limitation: synonyms, dynamic imports, delegated readers, other paths and side effects are not excluded.
- Adversarial challenge: use `execute_position` or an imported helper to open XLSX without any forbidden token.
- Exact-surface falsifier: insert one listed phrase/token into the scanned material so the assertion at lines `124-130` fails.
- Assertion that must fail and why: at test lines `124-130`, placing any exact lower-case advice phrase in the joined workbook values makes the first loop fail; placing any exact workbook-reader token in one of the enumerated runtime files makes the second loop fail. Synonyms, indirect helper calls and files outside `RUNTIME_PRL_PATHS` are outside the asserted surface.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return with structural schema/side-effect and repository-wide runtime-read boundary proof.

## File decision

- Groups/relationships: `5/5`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve the inspected workbook observations and aligned exclusion intent as reference evidence; physical rows and lexical scans do not establish Tier A semantic authority.
