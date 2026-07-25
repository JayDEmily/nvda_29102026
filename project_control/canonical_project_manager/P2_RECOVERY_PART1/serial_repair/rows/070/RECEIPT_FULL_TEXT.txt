# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py`

## File evidence

- Sequence `070`, unit `PM-014`; test SHA-256 `228af73e016443281bc6086363c3a56a94ff4cb84b8bf86a0c61652da1260541`.
- Full reads: test `1-108`; implementation `src/nvda_desk/domain/parallel_risk/unavailable_signals.py:1-219`; typed inventory loader and `config/parallel_risk_signal_inventory.v1.yaml:1-460`; workbook authority `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:1-94`; PRL authority `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Raw test result: `5 passed in 0.17s`.

## G1 — `test_inventory_backed_unavailable_signals_marks_present_and_missing_expected`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py:17-30`; assertions at lines `24-30` fix two presence states, one confidence impact and one inventory reference.
- Authority locator: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:26-34`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact PRL inventory records, `missing` state or `lowers_confidence` consequence.
- Authority match: typed promotion with lineage is lawful, but the reference workbook does not normatively own the inventory population or this effect policy.
- Behaviour proved: for the supplied present-ID set, the current projection marks `source_time_utc` present, `vix_level` missing and emits the asserted reference/impact.
- Limitation: caller-provided presence is accepted without source proof; no completeness, freshness, duplicate, unknown-ID or false-present challenge exists.
- Adversarial challenge: a caller could falsely list a missing signal as present and the test would not detect fabricated availability.
- Exact-surface falsifier: change either presence value, the impact or the inventory reference so assertion `24`, `25`, `27` or `28-30` fails.
- Assertion that must fail and why: line `24` fails if the supplied present set no longer yields `source_time_utc=present`; line `25` fails if omitted `vix_level` is not labelled missing; line `27` fails if its configured consequence changes; and lines `28-30` fail if its inventory identity is not carried exactly. None of these assertions authenticates the caller's present-ID set.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after admitted inventory population, presence evidence and missing-consequence law.

## G2 — `test_inventory_backed_deferred_rich_signals_are_unavailable_not_fabricated`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py:33-55`; assertions at lines `51-55` require two configured IDs, `None`, a false use flag and absence of the word `fabricated` from `None`.
- Authority locator: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:66-77`; `NO_VALID_AUTHORITY_RELATIONSHIP` for these exact deferred signal families and state schema.
- Authority match: missing authority must not be invented, but the selected IDs/statuses and runtime-use flag contract are not normatively admitted.
- Behaviour proved: configured deferred records produce valueless snapshots with `lawful_prl_use_allowed=False` for the exercised inventory.
- Limitation: asserting that `None` does not contain the word `fabricated` is vacuous; it does not prove the source is unavailable, that no substitute value exists elsewhere, or that downstream code cannot use it.
- Adversarial challenge: an untested field could carry a fabricated estimate while `value` remains `None` and all assertions pass.
- Exact-surface falsifier: give `dense_options_chain` a non-`None` `value` or true use flag so assertion `53` or `54` fails.
- Assertion that must fail and why: line `53` fails if the deferred snapshot contains any value, and line `54` fails if the exact record becomes lawfully usable. Line `55` contributes no fabrication proof because `str(None)` cannot contain the tested word; a fabricated estimate in another field would escape the group.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact source-availability authority and end-to-end no-substitution proof.

## G3 — `test_inventory_backed_excluded_signals_are_not_demanded_at_runtime`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py:58-67`; assertions at lines `64-67` fix exclusion and absence from snapshot/register for two IDs.
- Authority locator: `docs/01_NORMATIVE_CORE.md:71-79` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269` for PRL non-capital/non-order authority; `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact inventory IDs and exclusion mechanism.
- Authority match: excluding capital sizing and order instruction aligns with the lane boundary, but two identifier checks cannot prove all semantic equivalents or side effects.
- Behaviour proved: the current projection omits exactly `capital_sizing_signal` and `order_instruction_signal` from the asserted collections.
- Limitation: aliases, nested fields, renamed IDs and actual service calls remain untested.
- Adversarial challenge: add `deployable_notional` or call a broker service without those two IDs; assertions `64-67` remain green.
- Exact-surface falsifier: include either exact ID in the prohibited snapshot/register set or mark it non-excluded so assertion `64-67` fails.
- Assertion that must fail and why: lines `64-65` fail if either named signal loses the exact `excluded` state; line `66` fails if `capital_sizing_signal` is emitted as a snapshot; and line `67` fails if `order_instruction_signal` is emitted as missing. The group remains blind to renamed or semantically equivalent capital/order fields.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after structural authority separation and governed inventory exclusion semantics.

## G4 — `test_inventory_backed_unavailable_not_yet_sourced_and_quarantine_states`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py:70-85`; assertions at lines `79-85` fix unavailable/quarantined/rejected states and `None` values.
- Authority locator: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:66-83`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the seven-state inventory taxonomy and caller-driven quarantine/rejection inputs.
- Authority match: explicit unavailable/degraded states and no value invention align with preparation law, but the specific lifecycle and PRL projection are unadmitted.
- Behaviour proved: three caller-designated/configured states map to the asserted labels and valueless snapshots.
- Limitation: no authorised upstream receipt establishes the caller sets; precedence when IDs overlap and error/unknown handling are untested.
- Adversarial challenge: callers could quarantine an admitted signal or mark an unavailable signal present; this test would not establish lawful provenance.
- Exact-surface falsifier: change any asserted state or provide a non-`None` value so an assertion at lines `79-85` fails.
- Assertion that must fail and why: lines `79-81` fail if the three fixture IDs are mapped to different lifecycle labels; lines `83-85` fail if any corresponding snapshot acquires a value. No assertion checks who authorised the quarantine/rejection sets or how overlapping sets are resolved.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after typed upstream disposition evidence and an admitted state-transition/precedence contract.

## G5 — `test_inventory_backed_unavailable_signals_are_state_of_play_not_action_language`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py:88-108`; line `108` asserts absence of eight phrases from serialised selected entries.
- Authority locator: `docs/01_NORMATIVE_CORE.md:71-79`; no exact proposition treats finite phrase absence as proof of non-action authority.
- Authority match: non-action intent matches PRL boundaries, but the observation method cannot establish that meaning.
- Behaviour proved: the current serialised entries omit the eight literal phrases.
- Limitation: synonyms, fields, encoded values, nested side effects and downstream calls remain green.
- Adversarial challenge: add `execute_position=True` or `deploy_capital_pct=1.0`; none of the eight phrases appears and assertion `108` still passes.
- Exact-surface falsifier: insert any one forbidden literal into a serialised entry so the loop assertion at line `108` fails for that phrase.
- Assertion that must fail and why: line `108` fails only when one of the eight literal phrases appears in the selected serialised entries. An authority-bearing field such as `execute_position` or a downstream side effect can be added without triggering that assertion, so the test proves a token blacklist rather than non-action behaviour.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after schema-level forbidden-authority validation and behavioural side-effect tests.

## File decision

- Groups/relationships: `5/5`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve exact valueless-state and exclusion observations; do not promote the inventory taxonomy from config/test behaviour.
