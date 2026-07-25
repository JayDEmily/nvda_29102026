# Semantic receipt — `tests/tier_a/financial_calendar/test_financial_calendar_authority_surface.py`

## 1. Process record

- Sequence: `010`
- Unit: `PM-012`
- Test SHA-256: `a7d838c29341c28572855a3aa201547cc614dcf5bcbf3bcfb82d9eeec9a85652`
- Test read in full: lines `1-163`.
- Local manifest helper and every expected-exception/assertion path read in full.
- Exercised implementation read in full: `src/nvda_desk/calendar/reference/importer.py` lines `1-135`, `src/nvda_desk/calendar/reference/projection.py` lines `1-253`, and `src/nvda_desk/contracts/reference_data.py` lines `1-75`.
- No external fixture, parametrisation, setup/teardown or monkeypatch.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/financial_calendar/test_financial_calendar_authority_surface.py -q` returned `7 passed in 0.20s`, exit `0`.

## 2. Complete file restatement

The file builds one dictionary manifest with two artefacts and one generic layer named `checked-calendar-reference`. It separately verifies duplicate artefact rejection, unknown layer-to-artefact reference rejection, top-level and nested forbidden manifest keys, duplicate layer rejection, unknown event source rejection, forbidden event-row key rejection and duplicate event rejection. Its nominal projection asserts a subset of trace identities, three false permission flags and one crosswalk-derived evaluation tag.

It never uses the exact four governed calendar business-layer names, distinguishes market-session reference from financial-event reference, supplies operational state, composes reference and operational facts, exercises supersession/conflict/degradation, asserts bundle/schema/effective-range identity completeness, version-identifies the projection policy, checks source fact versions in the trace, proves source immutability, verifies context withholding, or behaviourally establishes absence of candidate/capital authority.

## 3. Authority context

- `N03.2-004`, `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:96-119`, mandates exactly four business layers: `market_session_reference`, `financial_event_reference`, `operational_calendar_state`, and `derived_runtime_calendar_context`. The first two reference families are distinct and neither rewrites the other (`100-109`).
- Existing phrases such as `checked calendar/reference` remain implementation evidence only when mapped to one governed layer; they are not competing layer names: the same document `166-170`.
- `N03.2-005`, lines `120-159`, requires layer/bundle/source/schema/effective-range identity, role-correct IDs, semantic-key precedence, explicit supersession and conflict/degradation law.
- `N03.2-006`, lines `160-193`, preserves provider/persistence substitution without altering the four-layer model.
- `C-005` and `C-006`, `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv:6-7`, require authoritative four-layer fixtures, duplicate/identity rules, candidate/sizing separation and explicit reference-plus-operational composition.
- `Financial Calendar Crosswalk` is an accepted versioned deterministic projection mapping policy, not source truth or precedence authority: `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv:50`.
- Surface 5.4 remains `thin_seam`; provider substitution and complete runtime composition are incomplete: `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:48`.

## 4. Assertion group 1 — duplicate reference artefact IDs are rejected (`39-43`)

1. **Behaviour:** duplicates one artefact dictionary and expects `load_manifest` to fail.
2. **Authority meaning:** reference artefacts and facts require unique owner-scoped identities; duplicate/conflict evidence must not silently collapse.
3. **Fit:** this is a bounded negative identity clause.
4. **Proved:** one exact duplicate `artifact_id` is rejected by the current importer.
5. **Not proved:** fact identity, cross-version duplication, same-key conflict semantics, preserved duplicate evidence or namespace scope.
6. **Falsifier:** allow the duplicated ID through.
7. **Required failure:** expected exception at `42-43`.
8. **Authority-violating implementation that passes:** reject exact duplicate strings but silently collapse semantically duplicate facts under different IDs.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `boundary`.
11. **Disposition/gate:** valid narrow Tier-A clause, but not sufficient for final file admission.

## 5. Assertion group 2 — unknown layer-to-artefact references are rejected (`45-48`)

1. **Behaviour:** adds an absent artefact ID to the layer and expects failure.
2. **Authority meaning:** layer/fact material must trace to admitted source artefacts rather than fabricated references.
3. **Fit:** direct bounded source-reference integrity proof.
4. **Proved:** the importer rejects the tested unknown artefact reference.
5. **Not proved:** source content fingerprints, source versions, layer owner, effective range, fact-level lineage or all reference roles.
6. **Falsifier:** accept `not-present`.
7. **Required failure:** expected exception `47-48`.
8. **Authority-violating implementation that passes:** accept fabricated fact IDs inside a known artefact or omit source versions.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `identity_lineage`.
11. **Disposition/gate:** valid narrow clause.

## 6. Assertion group 3 — top-level capital-sizing key is rejected (`51-56`)

1. **Behaviour:** adds `capital_sizing` to the manifest and expects forbidden-authority failure.
2. **Authority meaning:** calendar reference import cannot originate capital-deployment or sizing authority.
3. **Fit:** direct negative boundary for one exact forbidden key.
4. **Proved:** the tested top-level key is rejected.
5. **Not proved:** all capital synonyms/structures, output non-interference, downstream enforcement or absence of capital code elsewhere.
6. **Falsifier:** allow the key.
7. **Required failure:** expected exception `55-56`.
8. **Authority-violating implementation that passes:** accept an equivalent key such as `authorised_notional` not in the blacklist.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `boundary`.
11. **Disposition/gate:** valid tested-key clause only.

## 7. Assertion group 4 — nominal trace carries selected IDs and mode (`59-81`)

1. **Behaviour:** projects one event and checks trace presence, bundle ID, sorted artefact IDs, event ID and projection-mode string.
2. **Authority meaning:** derived context must identify context/policy/effective window, selected source fact identities and versions, completeness/conflict/supersession state and deterministic fingerprint.
3. **Contradiction and partial fit:** the ID assertions are bounded trace evidence, but the nominal manifest uses `checked-calendar-reference`, not either exact governed reference layer, and merges a session artefact and crosswalk under one generic layer. The trace also omits required policy/source versions and context completeness/conflict state.
4. **Proved:** the current trace carries the asserted subset for this fixture and sorts artefact IDs.
5. **Not proved:** exact four-layer mapping, distinct reference families, source fact/version lineage, projection-policy version, effective/as-of identity beyond one datetime field, supersession/conflict/completeness or fingerprint.
6. **Falsifier:** remove/change one asserted trace field or ordering.
7. **Required failure:** assertions `77-81`.
8. **Authority-violating implementation that passes:** preserve these five fields while accepting arbitrary layer names, merging fact families or discarding source versions/conflicts.
9. **Semantic relation:** `authority_contradictory` for the nominal layer model; `bounded_separable_clause` only for the observed ID subset.
10. **Proof strength:** `identity_lineage`.
11. **Disposition/gate:** `BLOCKED_P3_REPAIR`; nominal fixture must use and prove the exact governed layer model.

## 8. Assertion group 5 — three permission flags are false (`82-84`)

1. **Behaviour:** checks `online_mutation_allowed`, `candidate_formation_allowed` and `capital_sizing_allowed` are false.
2. **Authority meaning:** projection is context-only, cannot write source truth and cannot form candidate or capital decisions.
3. **Mismatch:** false metadata flags do not prove non-mutation or absence of decision behaviour.
4. **Proved:** the trace declares the three permissions false.
5. **Not proved:** source immutability, no candidate/capital calculations, no hidden output fields, no downstream override or enforcement.
6. **Falsifier:** return one flag true.
7. **Required failure:** assertions `82-84`.
8. **Authority-violating implementation that passes:** mutate source data or compute capital while returning all flags false.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `boundary` as declarative metadata only.
11. **Disposition/gate:** requires behavioural non-interference proof in P3.

## 9. Assertion group 6 — one FOMC mapping emits `event_risk` (`85`)

1. **Behaviour:** verifies the first event's evaluation tags for one source event type.
2. **Authority meaning:** Financial Calendar Crosswalk is a versioned deterministic mapping policy, but individual mapping rows require admitted policy content/version.
3. **Mismatch:** no exact current proposition specifies `fomc_window -> event_risk`, and the test does not assert a crosswalk policy version.
4. **Proved:** current hard-coded mapping produces the asserted tag.
5. **Not proved:** normative correctness, mapping completeness, version, substitution, unknown-event policy or target legality.
6. **Falsifier:** change the hard-coded mapping/tag.
7. **Required failure:** assertion `85`.
8. **Authority-violating implementation that passes:** keep this row while other rows are wrong or the mapping policy is unversioned and mutable.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `behavioural` for current implementation mapping only.
11. **Disposition/gate:** observational until exact policy content/version authority is proved.

## 10. Assertion group 7 — unknown event source artefact is rejected (`88-104`)

1. **Behaviour:** supplies an unrecognised `source_artifact_id` and expects failure.
2. **Authority meaning:** every projected fact must trace to an admitted source artefact; IDs cannot be fabricated across roles.
3. **Fit:** bounded negative source-lineage clause.
4. **Proved:** the tested unknown source ID is rejected for a multi-artefact bundle.
5. **Not proved:** source version/content fingerprint, fact owner, source-time identity or valid single-artefact fallback semantics.
6. **Falsifier:** accept `not-present`.
7. **Required failure:** expected exception `92-104`.
8. **Authority-violating implementation that passes:** accept a known artefact ID but wrong fact family/version.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `identity_lineage`.
11. **Disposition/gate:** valid narrow clause.

## 11. Assertion group 8 — event-row trading instruction is rejected (`106-119`)

1. **Behaviour:** adds `trading_instruction` to an event row and expects forbidden-authority failure.
2. **Authority meaning:** derived calendar context cannot originate trading/candidate/capital authority.
3. **Fit:** direct tested-key negative boundary.
4. **Proved:** this exact event-row key is rejected.
5. **Not proved:** recursive nested event-row rejection, all equivalent keys, output non-interference or absence elsewhere.
6. **Falsifier:** allow the key.
7. **Required failure:** expected exception `106-119`.
8. **Authority-violating implementation that passes:** accept an equivalent instruction under another spelling or nested object.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `boundary`.
11. **Disposition/gate:** valid tested-key clause only.

## 12. Assertion group 9 — duplicate layer IDs are rejected (`122-127`)

1. **Behaviour:** duplicates the generic layer dictionary and expects failure.
2. **Authority meaning:** governed layers have unique identities and exact allowed meanings.
3. **Partial fit:** duplicate-ID rejection is valid, but the test never rejects the ungoverned base layer name.
4. **Proved:** exact duplicate layer IDs are rejected.
5. **Not proved:** allowed layer vocabulary, exact four-layer count, layer ownership/family separation or versioning.
6. **Falsifier:** accept duplicate layer IDs.
7. **Required failure:** expected exception `126-127`.
8. **Authority-violating implementation that passes:** accept any unique arbitrary layer names, including a blended generic reference layer.
9. **Semantic relation:** `bounded_separable_clause` for duplicate identity; `related_but_not_proved` for layer authority.
10. **Proof strength:** `boundary`.
11. **Disposition/gate:** valid narrow clause but nominal layer repair remains required.

## 13. Assertion group 10 — duplicate event IDs are rejected (`130-151`)

1. **Behaviour:** submits two projected rows with the same event ID and expects failure.
2. **Authority meaning:** event/fact identities must be unique within their owner/namespace and conflicting facts must not silently collapse.
3. **Fit:** bounded duplicate event-ID rejection.
4. **Proved:** duplicate ID within one projection call is rejected.
5. **Not proved:** same-key different-ID conflict, cross-version identity, supersession, preserved conflict evidence or owner namespace.
6. **Falsifier:** accept both rows.
7. **Required failure:** expected exception `134-151`.
8. **Authority-violating implementation that passes:** assign different IDs to semantically conflicting facts and silently select one.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `boundary`.
11. **Disposition/gate:** valid narrow clause.

## 14. Assertion group 11 — nested manifest authority keys are rejected (`154-163`)

1. **Behaviour:** places `candidate_formation` inside an artefact and `capital_sizing` inside a layer; expects both failures.
2. **Authority meaning:** forbidden decision authority must not be smuggled recursively through calendar import material.
3. **Fit:** direct recursive rejection for two tested nested paths/keys.
4. **Proved:** those two nested occurrences are rejected.
5. **Not proved:** every nested collection/type, aliases, event-row recursive rejection or output non-interference.
6. **Falsifier:** stop recursive traversal for either path.
7. **Required failure:** expected exceptions `157-158` or `162-163`.
8. **Authority-violating implementation that passes:** accept a differently named forbidden authority or nested event-row instruction not in the tested manifest traversal.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `boundary`.
11. **Disposition/gate:** valid narrow recursive-key clause.

## 15. Final file disposition

`BLOCKED_P3_REPAIR`

The file contains several strong bounded negative identity and forbidden-key checks. However, its nominal authoritative path contradicts the accepted exact four-layer calendar model by using one generic `checked-calendar-reference` layer that does not distinguish `market_session_reference` from `financial_event_reference`. It also represents non-interference through false flags and asserts an unversioned hard-coded mapping row. These defects prevent current Tier-A admission despite the valid subclauses.

- Assertion-group count: `11`
- Relationship count: `11`
- Return gate: P3 must replace the nominal fixture with exact governed layer identities/families, prove required version/lineage/conflict fields and behavioural non-interference, while preserving the valid duplicate/unknown/forbidden-key tests.
