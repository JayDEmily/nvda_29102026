# Semantic receipt — `tests/tier_a/financial_calendar/test_fwd008_runtime_calendar_query_contract.py`

## 1. Process record

- Sequence: `012`
- Unit: `PM-012`
- Test SHA-256: `b17352353af3b2ec8d8b8a1d1322181c02f9a053ca12becf4ff5327d4a010ce5`
- Test read in full: lines `1-56`.
- Exercised implementation read in full: `src/nvda_desk/calendar/operational/events.py` lines `1-155`.
- Current route inspected: proof block `fwd007_008_010_013_rebuild_surface`; no retained-registry inventory entry.
- No external fixture, parametrisation, setup/teardown or monkeypatch.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/financial_calendar/test_fwd008_runtime_calendar_query_contract.py -q` returned `1 passed in 0.04s`, exit `0`.

## 2. Complete file restatement

The test creates two process-memory operational events, one near high-materiality NVDA earnings event and one later medium-materiality SPX macro event. It builds a runtime snapshot for NVDA over one hour with a minimum materiality of medium. It checks that the query retains the symbol, only the NVDA event matches, proximity is 1,200 seconds, materiality rank is three, one lineage ID is returned, and three declarative fields say the result is context-only with candidate formation and capital sizing disallowed.

It does not compose checked reference facts with operational state, prove operational append/correction identity, exercise duplicate/conflict/supersession behaviour, distinguish the exact four calendar layers, version the materiality/proximity policy, or observe any attempted candidate/capital action. The two false permission fields are values on the returned dataclass, not enforcement of non-authority.

## 3. Authority context

- `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:100-119` defines the exact four-layer model. Operational state is a separate owner and derived runtime context may project admitted facts without originating source or downstream decision authority.
- `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:123-146` requires role-correct identity/version and forbids freshness, insertion order or higher materiality from creating precedence unless an explicit fact-specific policy authorises it.
- `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:150-162` requires explicit unavailable/degraded states and treats process-memory repositories as alpha implementation truth only.
- Gate-C envelope `D-006`, `project_control/normative_authority_top_down_alignment/gate_c2_proof_envelopes/D-006.md:13-29,39-45`, states that this existing test is only a dependant; the positive authority proof must establish duplicate/identity rules, separation from candidate/sizing authority and one explicit composition between checked reference projection and operational query state.
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:40-59` requires the proof level that actually establishes the claimed boundary; flags, object construction and same-process readback are insufficient substitutes.

## 4. Assertion group 1 — query symbol is retained (`49`)

1. **Behaviour:** checks the constructed query retains `NVDA`.
2. **Authority meaning:** a derived context must identify the requested context and effective/as-of window.
3. **Fit:** bounded carrier-field evidence only.
4. **Proved:** the returned snapshot references the same query object and its symbol remains `NVDA`.
5. **Not proved:** context identity, policy version, effective-window identity, copy isolation or role-correct source identity.
6. **Falsifier:** replace/drop the query or symbol.
7. **Required failure:** assertion `49`.
8. **Authority-violating implementation that passes:** preserve the query object while composing no authoritative calendar facts.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `presence_only`.
11. **Disposition/gate:** valid narrow carrier observation.

## 5. Assertion group 2 — symbol/window/materiality filtering returns one event (`50`)

1. **Behaviour:** requires only `earnings-nvda` to match.
2. **Authority meaning:** derived runtime context may select admitted operational facts for a stated query window.
3. **Fit:** bounded deterministic filtering behaviour, but not authoritative four-layer composition.
4. **Proved:** the current process-memory query excludes the later SPX event for this fixture.
5. **Not proved:** each filter independently, boundary inclusivity, unknown materiality, duplicate handling, source/reference composition or policy authority.
6. **Falsifier:** return zero, both events or a different event.
7. **Required failure:** assertion `50`.
8. **Authority-violating implementation that passes:** apply an unversioned or incorrect precedence policy while producing this same single match.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `behavioural`.
11. **Disposition/gate:** valid narrow query behaviour.

## 6. Assertion group 3 — proximity and materiality rank values (`51-52`)

1. **Behaviour:** checks 1,200 seconds and rank three.
2. **Authority meaning:** a derived context may carry deterministic proximity/materiality features under a governed projection policy.
3. **Fit:** exact arithmetic for one fixture, but the policy and rank mapping are not version-identified.
4. **Proved:** proximity uses the absolute start-time difference and `high` maps to three in the current implementation.
5. **Not proved:** authority for the rank scale, interval overlap proximity, timezone variants, policy version or deterministic fingerprint.
6. **Falsifier:** change either calculated value.
7. **Required failure:** assertions `51-52`.
8. **Authority-violating implementation that passes:** hard-code or silently mutate the unversioned rank policy while keeping this one mapping.
9. **Semantic relation:** `related_but_not_proved` for authoritative policy; bounded arithmetic observation only.
10. **Proof strength:** `behavioural`.
11. **Disposition/gate:** observational until policy/version authority is linked.

## 7. Assertion group 4 — lineage list is returned (`53`)

1. **Behaviour:** retrieves one lineage ID by event ID.
2. **Authority meaning:** operational facts and derived contexts must preserve source/lineage identities.
3. **Fit:** bounded lineage carriage.
4. **Proved:** `lineage_for` returns a copied list containing `calendar-ref-1` for the matched event.
5. **Not proved:** lineage role, source version, writer identity, supersession target, missing-event behaviour or source-fact trace completeness.
6. **Falsifier:** omit/change the ID.
7. **Required failure:** assertion `53`.
8. **Authority-violating implementation that passes:** accept fabricated lineage IDs or omit all required identity roles while carrying this string.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `identity_lineage`.
11. **Disposition/gate:** valid narrow carriage clause.

## 8. Assertion group 5 — context-only and no-candidate/no-capital flags (`54-56`)

1. **Behaviour:** checks one string and two false Boolean defaults.
2. **Authority meaning:** calendar projection must not originate candidate, risk, capital, placement or execution authority.
3. **Fit:** the values describe the intended boundary but do not enforce or observe it.
4. **Proved:** the dataclass exposes the asserted defaults.
5. **Not proved:** attempted candidate/capital actions fail, downstream consumers cannot misuse the snapshot, no hidden mutation occurs, or the repository lacks decision logic.
6. **Falsifier:** change one default field.
7. **Required failure:** assertions `54-56`.
8. **Authority-violating implementation that passes:** perform candidate formation or capital sizing elsewhere while returning these unchanged flags.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `presence_only`.
11. **Disposition/gate:** blocking repair required because the test name claims “without trade authority” while only inspecting declarative labels.

## 9. File-level disposition

- Assertion groups: `5`.
- Explicit proposition relationships: `5`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Reason: filtering and lineage assertions provide useful bounded implementation evidence, but the material non-authority claim is represented only by fields, and the test omits the proposition-required reference-plus-operational composition, identity/duplicate rules and policy versions.
- P3 repair gate: retain the bounded query arithmetic as a subordinate test; add explicit four-layer composition, independently test each filter boundary, identify the materiality/proximity policy version, and prove attempted candidate/capital use is impossible or rejected rather than labelled false.
- No implementation or test mutation executed.
