# Semantic receipt — `tests/tier_a/downstream_runtime/test_downstream_state_reader_service_surface.py`

## File evidence

- Sequence `099`, unit `PM-015`; test SHA-256 `6b3153b87c012f5deff9c6820f40de5732ceab8b4cd7988d57da881476ac97c0`.
- Full reads: test `1-42`; complete service `src/nvda_desk/downstream/state_reader.py`; state-reader authority `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:183-195`; P1 concept `P1-119` in `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv`.
- Raw test result: `2 passed in 0.14s`.

## G1 — `test_downstream_state_reader_service_surface_is_present`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_state_reader_service_surface.py:21-24`; assertions import one module and class attribute.
- Authority locator: `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:183-195`.
- Authority match: the class name aligns with the governed downstream state-reader layer, but presence does not prove any repo-native read or truthful-placeholder evidence.
- Behaviour proved: the exact module and class name are importable.
- Limitation: position, capital and receipt repositories, source classification, reservation evidence and prohibited behavioural decisions are not exercised.
- Adversarial challenge: retain an empty class under the same name; all assertions remain green.
- Exact-surface falsifier: remove or rename `DownstreamStateService`; the assertion at line `24` must fail.
- Assertion that must fail and why: at test lines `22-24`, making the module unimportable or removing/renaming `DownstreamStateService` triggers the helper failure or breaks the identity assertion. A service with no repository reads remains green because presence is the only tested property.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; require behavioural state-read evidence before Tier A admission.

## G2 — `test_downstream_state_reader_detaches_position_id_inputs`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_state_reader_service_surface.py:27-42`; one caller list is copied, the returned list is mutated, and a second constructor call returns the original supplied ID with the same receipt string.
- Authority locator: `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:183-195` and P1 `P1-119`.
- Authority match: copy isolation is a useful local clause, but the normative output must report which repo-native capital, position and receipt surfaces were actually read and whether truth or placeholder evidence was used.
- Behaviour proved: the method copies the input position-ID list and echoes the supplied receipt ID; later caller mutations do not alter a separately created result.
- Limitation: the service reads no repository, emits no read-surface identities or truth/placeholder classification, reserves no concerns, and the second call labelled `replay` is merely another construction with caller-supplied values.
- Adversarial challenge: report arbitrary position IDs and receipt text without reading any state; the test remains green, which is the current implementation.
- Exact-surface falsifier: retain the caller list by reference or stop echoing `receipt-1`; an assertion at lines `41-42` must fail.
- Assertion that must fail and why: at test lines `40-42`, allowing prior caller/result mutations to contaminate a newly constructed result makes its position-ID equality fail, and not echoing the supplied receipt string breaks the second assertion. Returning fabricated caller-supplied IDs without reading any repository still passes, as the implementation currently does.
- Semantic relation: `no_semantic_fit`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; implement and test explicit repo-native capital/position/receipt reads, truthful-placeholder status and non-decision boundaries.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- The test proves input-list detachment and receipt-string echo, not the governed Downstream State-reader Layer.
