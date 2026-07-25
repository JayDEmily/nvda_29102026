# Semantic receipt — `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py`

## 1. Process record

- Sequence: `005`
- Unit: `PM-012`
- Test SHA-256: `022203decd6eb9be1bafd3bc3a00d9ee3bba9a69e9262e11f3efea86526494f7`
- Test read in full: lines `1-60`.
- Helpers `_require_module` and `_require_attr` read in full.
- Exercised implementation read in full: `src/nvda_desk/calendar/reference/importer.py` lines `1-135` and `src/nvda_desk/calendar/reference/projection.py` lines `1-253`.
- No external fixture, parametrisation, setup/teardown or monkeypatch.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py -q` returned `4 passed in 0.22s`, exit `0`.

## 2. Complete file restatement

The first test imports the calendar-reference importer module and verifies the module name plus the presence/identity of `FinancialCalendarImporter`, `load_manifest`, `load_layers` and `build_reference_packet`. The second imports the projection module and verifies the module name plus the presence/identity of two service classes and two projection functions. The third verifies the presence/identity of the crosswalk function and record class. The fourth calls the crosswalk function, mutates two list fields on the first returned record, calls the function again and verifies that the second call does not contain either mutation.

The file observes importability, exact attribute presence and detached list copies for two fields of one returned crosswalk record. It never calls the importer, loads a manifest/layer, projects a runtime context, stitches precursor context, validates reference identity/version/lineage, exercises one of the four calendar business layers, proves cross-layer composition, checks forbidden authority, checks duplicate/conflict/supersession behaviour, asserts deterministic projection identity/fingerprint or verifies context withholding/degradation.

## 3. Authority context

- `N03.2-004`, `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:96-119`, defines exactly four semantic business layers and states at line `107` that modules, files, packets and projection services are implementations/carriers, not additional business layers.
- The same proposition requires immutable selected reference bundles and distinct ownership for `market_session_reference`, `financial_event_reference`, `operational_calendar_state` and `derived_runtime_calendar_context` (`113-119`).
- `N03.2-005`, lines `120-159`, requires role-correct identity/version/source/effective-range facts, semantic-key-specific precedence, explicit supersession and fail-closed conflict/degradation behaviour.
- `N03.2-006`, lines `160-193`, requires provider replacement and persistence separation without changing the four-layer model or promoting operational/derived material to reference truth.
- `C-005`, `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv:6`, requires authoritative fixtures proving the adopted layer model and explicitly rejects a green result based only on model/registry/process-memory presence.
- `C-006`, the same register line `7`, requires duplicate/identity rules, candidate/sizing separation and explicit checked-reference projection plus operational-query composition.
- Surface 5.4 is structurally locked but remains implementation-truth `thin_seam`: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:186-201` and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:48`.

## 4. Assertion group 1 — importer module and attributes are present (`21-27`)

1. **Behaviour:** imports one module and requires four exact current attributes.
2. **Authority meaning:** the calendar reference authority must admit checked, versioned reference facts through a governed import/update process with layer, bundle, source, schema and effective-range identity.
3. **Mismatch:** module and symbol presence establish neither the admitted import contract nor any reference-layer behaviour. The exact Python names are implementation grammar.
4. **Proved:** the current importer module imports and exposes the four named objects.
5. **Not proved:** manifest acceptance/rejection, exact four-layer mapping, unique identity, source artefact lineage, immutable bundle selection, forbidden-authority rejection, version/effective-range carriage or packet role correctness.
6. **Falsifier:** remove or rename the module or any required attribute.
7. **Required failure:** module-name assertion `23` or `_require_attr` assertions `25-27`.
8. **Authority-violating implementation that passes:** keep four empty or mis-owned callables under the same names while accepting fabricated identities or promoting operational data to reference truth.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `presence_only`.
11. **Disposition/gate:** `NON_AUTHORITATIVE_OBSERVATIONAL`; no import-authority claim.

## 5. Assertion group 2 — projection module and attributes are present (`30-37`)

1. **Behaviour:** imports one projection module and requires two service classes plus two functions.
2. **Authority meaning:** the projection boundary may deterministically select/relate admitted facts into context-only output, must preserve stated identities/versions/conflicts/completeness and must not write source truth.
3. **Mismatch:** symbol existence does not exercise projection, ownership, deterministic output or source-layer non-mutation.
4. **Proved:** the current projection module imports and exposes the four named objects.
5. **Not proved:** selected-fact lineage, projection-policy version, effective/as-of window, supersession/conflict state, deterministic fingerprint, fail-closed withholding, no source write-back or composition with operational state.
6. **Falsifier:** remove or rename the module or one required attribute.
7. **Required failure:** module-name assertion `32` or `_require_attr` assertions `34-37`.
8. **Authority-violating implementation that passes:** retain the names while the functions fabricate context identity, discard lineage, mutate the reference bundle or originate candidate/capital authority.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `presence_only`.
11. **Disposition/gate:** `NON_AUTHORITATIVE_OBSERVATIONAL`; no projection-authority claim.

## 6. Assertion group 3 — crosswalk function and record class are present (`40-45`)

1. **Behaviour:** verifies two exact crosswalk-related symbols exist in the projection module.
2. **Authority meaning:** `Financial Calendar Crosswalk` is vocabulary for a governed mapping/projection surface whose lawful evidence must preserve the four-layer calendar model and projection boundary.
3. **Mismatch:** the accepted phrase and a same-named implementation symbol are not interchangeable authority. Presence does not prove any mapping row, semantics, owner, consumer or boundary.
4. **Proved:** the current module exports `financial_calendar_crosswalk` and `FinancialCalendarCrosswalkRecord`.
5. **Not proved:** completeness/correctness of mappings, layer ownership, versioning, extension/substitution, target legality, reference/operational separation or actual runtime use.
6. **Falsifier:** remove or rename either symbol.
7. **Required failure:** `_require_attr` assertions `44-45`.
8. **Authority-violating implementation that passes:** return arbitrary or candidate-forming mappings from the same function and class names.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `presence_only`.
11. **Disposition/gate:** `NON_AUTHORITATIVE_OBSERVATIONAL`; vocabulary resemblance does not establish calendar authority.

## 7. Assertion group 4 — repeated crosswalk calls return detached tested lists (`48-60`)

1. **Behaviour:** mutates `runtime_tags` and `projection_targets` on the first record from one call and verifies those mutations are absent from the first record returned by a second call.
2. **Authority meaning:** runtime consumers must not mutate selected reference truth, and derived context must not write its result back as source truth; lawful projection must preserve bounded ownership.
3. **Mismatch:** the test proves defensive copying for two list fields in a static implementation crosswalk. The crosswalk is configuration/mapping data, not a selected reference bundle or derived runtime context, and no exact proposition requires this specific function to expose detached records.
4. **Proved:** each call reconstructs at least the first record's `runtime_tags` and `projection_targets` lists sufficiently to prevent the two tested mutations leaking into the next call.
5. **Not proved:** detachment of `evaluation_tags` (not mutated), all records under all mutations, immutable selected bundles/source facts, deterministic mapping content, extension/substitution behaviour, runtime projection, source non-write-back or any four-layer identity/precedence rule.
6. **Falsifier:** return shared list objects for either tested field so the mutation persists into the second call.
7. **Required failure:** non-membership assertions `59-60`.
8. **Authority-violating implementation that passes:** return detached but semantically wrong mappings, omit required event families, target an unlawful consumer, or let the actual projection mutate source truth; these assertions still pass.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `behavioural` only for two-field copy isolation.
11. **Disposition/gate:** `NON_AUTHORITATIVE_OBSERVATIONAL`; useful implementation regression evidence but no authoritative calendar proposition.

## 8. Final file disposition

`NON_AUTHORITATIVE_OBSERVATIONAL`

The passing file is useful smoke/regression evidence for current module shape and two-field crosswalk copy isolation. It does not prove a separable authoritative part of `N03.2-004` through `N03.2-006`, `C-005` or `C-006`; presence of implementation symbols expressly cannot create the governed calendar layers.

- Assertion-group count: `4`
- Relationship count: `4`
- Return gate: remove/demote from current Tier-A authority projection in PM-019; P3 may author or repair behavioural proof of the reference import, four-layer model and governed projection boundary if required.
