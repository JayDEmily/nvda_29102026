# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_event_proximity_register.py`

## File evidence

- Sequence `067`, unit `PM-014`; test SHA-256 `7c07eece384e09b5dd1056939623827701868b5d321ee5da289fad9488d0fe74`.
- Full reads: test `1-71`; direct projection `src/nvda_desk/domain/parallel_risk/event_proximity.py:1-33`; operational calendar implementation `src/nvda_desk/calendar/operational/events.py:1-155`; calendar allocation `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:188-201`; Parallel Risk allocation `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; P1 Environment Assessment decision `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv:122`.
- Raw test result: `2 passed in 0.19s`.

## G1 — `test_event_proximity_register_projects_calendar_matches_without_trade_authority`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_event_proximity_register.py:15-55`; assertions at lines `42,44-55` fix one result, exact event/proximity/materiality/tag/lineage fields, one interpretation string, and absence of three substrings.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:188-201,254-269` and `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv:122`; `NO_VALID_AUTHORITY_RELATIONSHIP` for a separately governed `Event Proximity Register` contract.
- Authority match: calendar event-context projection may feed the independent Environment Assessment, but the cited authorities do not define this register, its field set, lifecycle, materiality rank, interpretation string or consumers.
- Behaviour proved: for the exercised snapshot, the projection copies one calendar match into one typed entry with the asserted identity, timing, tags and source reference.
- Limitation: the assertion proves one specimen only; the interpretation field is declarative, materiality ranking is inherited without challenge, and absence of `buy`, `sell` and `order` does not exclude synonymous fields, hidden side effects or downstream authority.
- Adversarial challenge: the implementation could add an `execute_trade` field, mutate a decision service, mis-rank other materialities or omit lineage for a second event while every assertion in this specimen remains green.
- Exact-surface falsifier: change the projected `proximity_seconds`, `materiality_rank`, tags or source references for this fixture so the corresponding assertion at lines `45-50` fails; this would falsify only the bounded projection evidence, not establish the missing register authority.
- Assertion that must fail and why: The field comparisons at lines `45-50` must fail when this fixture’s projected timing, rank, tags or source references differ, because those assertions are the direct checks that the calendar match was carried into the entry unchanged. They do not validate the register’s ownership, ranking policy or behaviour for other events.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after proposition-level and vocabulary admission of the register or re-authoring under the existing calendar/Environment Assessment boundary with structural non-authority proof.

## G2 — `test_event_proximity_register_returns_empty_entries_when_no_calendar_matches`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_event_proximity_register.py:58-71`; assertion at line `71` requires an empty list for one empty snapshot.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:188-201`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the complete empty-state semantics of an `Event Proximity Register`.
- Authority match: an empty calendar projection is compatible with the calendar boundary, but no authority defines the register’s completeness, unknown/error distinction, lifecycle or required empty-state representation.
- Behaviour proved: the exercised no-match snapshot returns `[]`.
- Limitation: the test does not distinguish no events from query failure, incomplete calendar authority, filtered materiality, stale data or missing source access.
- Adversarial challenge: the repository could silently swallow a calendar error and return `[]`; line `71` would still pass while the claimed empty state was false.
- Exact-surface falsifier: return any non-empty entry for this exact empty repository/query so assertion line `71` fails; this falsifies the observed empty-result behaviour only.
- Assertion that must fail and why: Line `71` must fail when this exact empty query returns any entry, because it is the sole detector for the observed empty-list result. It cannot distinguish a legitimate no-match result from swallowed calendar failure, filtering or incomplete source access.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after an admitted empty/unknown/error contract and completeness proof for the owning calendar-to-PRL projection.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve the deterministic calendar-match projection and empty-result observations as implementation evidence. No source, test, config or authority mutation is authorised.
