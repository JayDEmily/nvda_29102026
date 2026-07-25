# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_unavailable_signals.py`

## File evidence

- Sequence `084`, unit `PM-014`; test SHA-256 `16f79d6a2f90151a4415b01aee0ee09af5f23e2a61b578d93ff152daedea0dcc`.
- Full reads: test `1-39`; unavailable-signal builder `src/nvda_desk/domain/parallel_risk/unavailable_signals.py:1-63`; directly exercised snapshot/watch contracts; preparation absence law `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:48-83`; Parallel Risk seam `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Raw test result: `2 passed in 0.13s`.

## G1 — `test_unavailable_signal_snapshot_marks_future_signal_without_fabricated_value`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_unavailable_signals.py:9-23`; assertions require no value, missing/unknown states, false lawful-use flag, one reason and workbook lineage.
- Authority locator: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:48-83`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact expected-signal inventory, state labels and lawful-use fields.
- Authority match: explicit absence without fabrication aligns with preparation law, but the caller invents the future-signal expectation and this carrier/taxonomy is unadmitted.
- Behaviour proved: the fixture emits a no-value snapshot with the asserted current labels and lineage list.
- Limitation: source unavailability, inventory membership, completeness and downstream consequence are not verified; the supplied inventory reference is not asserted.
- Adversarial challenge: claim any arbitrary signal is expected/unavailable and receive the same legitimising object.
- Exact-surface falsifier: emit a fabricated value or alter one asserted state/reason/lineage so an assertion at lines `18-23` fails.
- Assertion that must fail and why: Lines `18-23` must fail when the builder invents a value or changes the asserted absence, use, reason or lineage fields because those comparisons are the direct specimen checks. A failure would expose divergence in this one carrier instance, not prove the caller was entitled to classify the signal as expected or unavailable.
- Semantic relation: `authority_missing`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after governed expected-signal inventory and exact absence/use taxonomy are admitted.

## G2 — `test_unavailable_signal_watch_entry_is_state_of_play_not_action`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_unavailable_signals.py:26-39`; assertions require one impact/reason and absence of three selected tokens.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the watch-entry carrier, default confidence impact and complete non-action semantics.
- Authority match: a descriptive absence observation is related to Parallel Risk, but the exact object and consequence lack authority and lexical absence is incomplete.
- Behaviour proved: the fixture echoes the reason, defaults to `lowers_confidence` and omits three literal strings.
- Limitation: aliases, nested instructions, executable consumers and actual confidence calculation are untested.
- Adversarial challenge: include `execute_position` or trigger a side effect without using `buy`, `sell` or `hedge`.
- Exact-surface falsifier: change the asserted impact/reason or insert one listed token so an assertion at lines `34-39` fails.
- Assertion that must fail and why: Lines `34-35` must fail when the watch impact or reason changes, while lines `37-39` must fail only for the three literal action tokens they scan. That distinction matters: the group detects its exact descriptive payload and blacklist, but remains blind to aliases and executable side effects.
- Semantic relation: `authority_missing`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after owned watch semantics and structural non-action proof.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve no-value and lineage observations; the expected inventory, named future signals, state/use taxonomy and impact policy are caller-defined and unadmitted.
