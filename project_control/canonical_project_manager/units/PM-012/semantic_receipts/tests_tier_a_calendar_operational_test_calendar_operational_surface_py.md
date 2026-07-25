# Semantic receipt — `tests/tier_a/calendar_operational/test_calendar_operational_surface.py`

## 1. Process record

- Sequence: `004`
- Unit: `PM-012`
- Test SHA-256: `fdbcf1bb828d8137f9e9f5567c401d9c692bd0331e8912879c22564a1546e865`
- Test read in full: lines `1-57`.
- Helpers `_require_module` and `_require_attr` read in full.
- Exercised implementation read in full: `src/nvda_desk/calendar/operational/events.py` lines `1-155`.
- No external fixture, parametrisation, setup/teardown or monkeypatch.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/calendar_operational/test_calendar_operational_surface.py -q` returned `2 passed in 0.05s`, exit `0`.

## 2. Complete file restatement

The first test imports `nvda_desk.calendar.operational.events`, checks its module name and checks the presence/identity of four attributes. The second test repeats the import/attribute checks, verifies two DTO classes are dataclasses, creates one market event and one session in two newly constructed in-memory repository instances, then verifies each repository lists the created object's identifier.

The file observes module importability, attribute presence, dataclass decoration, constructor availability, append-to-list create methods and list-copy reads. It never exercises runtime calendar queries, projection, materiality, lineage, event/session times, corrections, cancellations, supersession, conflict handling, operational writer identity, schema/version facts, append-preserved history, reference layers, checked-reference composition, context-only restrictions, missing-state degradation, persistence replacement or durability.

## 3. Authority context

- `N03.2-004`, `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:96-119`, defines exactly four semantic business layers and states explicitly at line `107` that repositories, tables and files are implementations/carriers, not layers.
- The same proposition assigns `operational_calendar_state` to an operational boundary whose authorised writer may append observed facts or explicit corrections and must not originate candidate/risk/capital/placement/execution/inventory/close/review authority (`113-119`).
- `N03.2-005`, lines `120-159`, requires layer/fact/version identity, explicit same-family supersession and rejection of global insertion-order precedence.
- `N03.2-006`, lines `160-193`, requires explicit degradation and persistence/business-layer separation.
- `C-005`, `GATE_C_TEST_REQUIREMENTS.tsv:6`, requires authoritative fixtures proving the adopted calendar layer model; model/presence-only success is not enough.
- `C-006`, line `7`, requires duplicate/identity rules, separation from candidate/sizing authority and explicit reference-to-operational composition.
- Surface 5.4 remains `thin_seam`, `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:186-201` and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:48`.

## 4. Assertion group 1 — module and four attributes are present (`22-32`)

1. **Behaviour:** imports one module and requires four exact attribute names to exist.
2. **Authority meaning:** the calendar architecture requires governed semantic layers, owners, identity/version rules and projection boundaries.
3. **Mismatch:** importability and attribute presence do not establish any semantic layer, authority, contract or behaviour. Exact class names are implementation grammar.
4. **Proved:** the module imports under the expected name and exposes the four current objects.
5. **Not proved:** DTO field correctness; operational ownership; four-layer separation; append/correction semantics; identity, version, lineage, time, conflicts, degradation or composition.
6. **Falsifier:** remove or rename one exported class.
7. **Required failure:** `_require_attr`/identity assertion line `32`.
8. **Authority-violating implementation that passes:** leave the four names in place but make all classes empty shells or let the operational repository overwrite reference truth; this group still passes.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `presence_only`.
11. **Disposition/gate:** `NON_AUTHORITATIVE_OBSERVATIONAL`; no calendar-authority claim.

## 5. Assertion group 2 — dataclass and create/list shell behaviour (`35-57`)

1. **Behaviour:** confirms two DTO types are dataclasses; creates one event and one session in separate new process-memory repositories; lists each identifier.
2. **Authority meaning:** operational calendar state is a semantic layer of append-preserved observations/corrections with authoritative identity/time/version/lineage and no cross-layer substitution.
3. **Mismatch:** the test demonstrates local list storage only. It does not establish an operational fact contract or any required semantic rule. The normative text expressly says a repository is not itself a business layer.
4. **Proved:** `create_event` and `create_session` append and return the supplied objects; `list_*` returns them for these two instances.
5. **Not proved:** CRUD (update/delete are absent), append-preserved correction history, duplicate handling, immutable identities, fact family, observed/effective time, writer/source identity, schema version, supersession, conflict, reference separation, context projection, durability or candidate/sizing exclusion.
6. **Falsifier:** stop appending the supplied object or return an empty list.
7. **Required failure:** identifier list assertions `56-57`.
8. **Authority-violating implementation that passes:** retain these methods but silently overwrite a same-key reference fact, use insertion order as precedence, omit all required lineage/version/time fields or grant candidate authority elsewhere. The assertions still pass.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `behavioural` only for the in-memory create/list shell, not calendar authority.
11. **Disposition/gate:** `NON_AUTHORITATIVE_OBSERVATIONAL`. A Tier-A calendar relationship requires new or repaired proof of the semantic operational layer and its boundaries.

## 6. Final file disposition

`NON_AUTHORITATIVE_OBSERVATIONAL`

The passing file is useful current implementation evidence for a process-memory shell. It does not prove a separable authoritative calendar proposition. In particular, neither repository presence nor create/list behaviour establishes `operational_calendar_state`, the exact four-layer model, C-005 or C-006.

- Assertion-group count: `2`
- Relationship count: `2`
- Return gate: remove/demote from current Tier-A authority projection in PM-019; P3 may author or repair authoritative calendar proof if required.
