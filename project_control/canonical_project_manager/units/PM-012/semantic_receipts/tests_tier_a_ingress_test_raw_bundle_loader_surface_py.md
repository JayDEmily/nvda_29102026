# Semantic receipt — `tests/tier_a/ingress/test_raw_bundle_loader_surface.py`

## 1. Process record

- Sequence: `013`
- Unit: `PM-012`
- Test SHA-256: `538a691a0c42f484b3695b20699b426ff087d9dcd9c7a23e5b17a9bd9895732b`
- Test read in full: lines `1-113`.
- Exercised implementation read in full: `src/nvda_desk/ingress/raw_bundle_loader.py` lines `1-128`, `src/nvda_desk/adapters/ingress/market_snapshot_feed.py` lines `1-21`, `src/nvda_desk/adapters/ingress/options_surface_feed.py` lines `1-17`, `src/nvda_desk/adapters/ingress/calendar_feed.py` lines `1-12`, `src/nvda_desk/preparation/runtime_preparer.py` lines `1-321`, and `src/nvda_desk/cognition/ingress/options_mapper.py` lines `1-27`.
- Current routes inspected: retained family `ingress_raw_bundle_loader_surface` and proof blocks `raw_capture_source_temporal_law_surface` plus `roadmap_external_source_api_ingress_authority_surface`.
- No external fixture, parametrisation, setup/teardown or monkeypatch.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/ingress/test_raw_bundle_loader_surface.py -q` returned `3 passed in 0.20s`, exit `0`.

## 2. Complete file restatement

The file first checks that one ingress module and five named symbols exist. It then sends one API-shaped mapping through the raw-bundle loader, market preparation wrapper, options wrapper and calendar wrapper. It checks source-kind labelling, separate market/options spot values, snapshot ID, minute-floor runtime alignment, selected payload aliases, three missing optional-enrichment labels, three options values, and a calendar bundle ID. Finally, it verifies that capture and persistence timestamps without source observation time/date are rejected.

The test spans at least four authority surfaces under one raw-loader name. It does not require repository-owned capture identity, source-contract identity, schema/policy versions, fingerprints, validation status or immutable source references. It treats the current generic-dictionary prepared snapshot and lineage-stripping options mapper as successful outputs despite current normative documents explicitly recording those alpha surfaces as nonconforming. It also accepts an empty calendar bundle and proves only its ID.

## 3. Authority context

- `docs/03.1_DOMAIN_MODEL_WORKING.md:17-49` requires source semantics, contract, temporal truth, validation, lineage, owner-issued source identity and a separate repository-owned capture identity.
- `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:44-72` distinguishes source observation truth from capture/persistence clocks and forbids substituting the latter for the former.
- `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:17-80` requires typed options material with source/capture identities, schema/policy versions, time and fingerprint before a derived-only serial-stage contract; the stage input must retain governed lineage and reject generic mappings.
- `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:27-89` requires the prepared common envelope, typed payload variants and fail-closed validation. Lines `85-89` explicitly state that current `PreparedRuntimeSnapshot`/`PreparedRuntimeDataset` surfaces do not conform because identity is optional, payloads are generic dictionaries, version/fingerprint facts are incomplete and no mandatory semantic fingerprint exists.
- `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:96-129` requires the exact four-layer calendar model and complete reference/context identity; an empty bundle ID is not calendar-authority proof.
- Gate-C requirements `C-002`, `C-004`, `C-005` and `C-008` require capture identity, explicit section precedence and fallback rejection; typed options identity/version/time and lineage; authoritative calendar fixtures; and the stable prepared envelope. Existing-test disposition classifies this file only as partially aligned for raw decode.

## 4. Assertion group 1 — module and symbol surface presence (`22-30`)

1. **Behaviour:** imports one module and confirms five attributes exist.
2. **Authority meaning:** the ingress architecture has an explicit typed-carrier seam.
3. **Fit:** symbol presence only.
4. **Proved:** the named module and symbols currently import.
5. **Not proved:** contract semantics, ownership, validation, identity, temporal law or behaviour.
6. **Falsifier:** remove/rename one symbol.
7. **Required failure:** helper failure or assertions `24-30`.
8. **Authority-violating implementation that passes:** expose empty or misleading classes/functions with the same names.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `presence_only`.
11. **Disposition/gate:** non-blocking inventory evidence only.

## 5. Assertion group 2 — raw loader labels source kind and preserves explicit market/options sections (`43-55`)

1. **Behaviour:** loads one mapping and checks `api_payload` plus different spot values in the explicit sections.
2. **Authority meaning:** typed ingress must preserve source-family semantics and explicit source material before preparation.
3. **Fit:** bounded explicit-section and source-kind behaviour.
4. **Proved:** explicit `market_snapshot` and `options_surface` mappings remain separate for this fixture; the local source-kind literal is carried.
5. **Not proved:** source-contract identity, provider/channel, source-issued identity, repository capture identity, schema version, fingerprint, validation outcome, copy isolation, fallback precedence or unrelated-key misclassification.
6. **Falsifier:** merge the sections or change the source-kind value.
7. **Required failure:** assertions `53-55`.
8. **Authority-violating implementation that passes:** retain these fields while inventing no capture identity and accepting arbitrary fallback mappings as authoritative source families.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `behavioural`.
11. **Disposition/gate:** valid narrow alpha decode evidence, not full raw-input admission proof.

## 6. Assertion group 3 — market wrapper emits current prepared snapshot shape (`57-77`)

1. **Behaviour:** checks snapshot ID, source-kind lineage, source time, minute-floor alignment, payload aliases, return value and exact optional-gap strings.
2. **Authority meaning:** preparation must produce a typed, identity/version/time/fingerprint-complete substrate and explicitly represent permitted optional gaps.
3. **Contradiction:** the assertions endorse the current generic payload/optional identity shape that `docs/04.2...:85-89` explicitly says does not conform. The snapshot has no mandatory prepared identity, capture/source references, schema/policy versions or fingerprints.
4. **Proved:** current wrapper copies the tested values, applies minute flooring and reports three optional enrichment gaps.
5. **Not proved:** authoritative prepared envelope, immutable input lineage, versioned alignment/derivation policy, semantic fingerprint, typed payload variant, validation/completeness state or rejection of generic payload authority.
6. **Falsifier:** alter one asserted output or gap list.
7. **Required failure:** assertions `64-77`.
8. **Authority-violating implementation that passes:** emit an unidentifiable generic dictionary with no capture ID or fingerprints—the current implementation does exactly this and remains green.
9. **Semantic relation:** `authority_contradictory` as current prepared-authority proof; bounded arithmetic observation only.
10. **Proof strength:** `behavioural`.
11. **Disposition/gate:** blocking repair required.

## 7. Assertion group 4 — options wrapper selects options-surface values (`79-88`)

1. **Behaviour:** checks options spot/DTE values after raw loading, preparation and stage-input mapping.
2. **Authority meaning:** the serial options stage may consume only typed derived primitives with an enclosing governed lineage reference to typed options material.
3. **Contradiction:** the current mapper consumes a generic `Mapping` and returns only three values plus missing-field names; the test does not require source/capture identity, version, time, fingerprint or lineage.
4. **Proved:** explicit options-surface values take precedence over the market spot for this fixture and are cast into the current input model.
5. **Not proved:** typed options evidence admission, lineage preservation, schema/policy version, generic-mapping rejection, missing mandatory authority or provider substitution.
6. **Falsifier:** source the spot from market data or change DTE values.
7. **Required failure:** assertions `86-88`.
8. **Authority-violating implementation that passes:** strip all options lineage before cognition while retaining the three values—the current path does so.
9. **Semantic relation:** `authority_contradictory` as `N-01` proof; bounded value-selection evidence only.
10. **Proof strength:** `behavioural`.
11. **Disposition/gate:** blocking repair required.

## 8. Assertion group 5 — calendar wrapper returns an empty bundle ID (`90-93`)

1. **Behaviour:** adapts a manifest with no artefacts/layers and checks `bundle_id`.
2. **Authority meaning:** checked calendar reference requires exact layer, bundle, version, source artefact/schema/effective-range identities.
3. **Fit:** object-construction presence only; the fixture contains none of the governed calendar authority.
4. **Proved:** the current importer accepts the empty manifest and copies the ID.
5. **Not proved:** any calendar layer, checked source truth, version, fact identity, projection or context.
6. **Falsifier:** stop copying the ID or reject the empty manifest.
7. **Required failure:** assertion `93` or construction.
8. **Authority-violating implementation that passes:** accept an empty unversioned bundle as if it were authoritative calendar evidence.
9. **Semantic relation:** `no_semantic_fit` for calendar-authority proof.
10. **Proof strength:** `presence_only`.
11. **Disposition/gate:** remove from this ingress test or replace with an authoritative/explicitly non-authoritative fixture and exact expected status.

## 9. Assertion group 6 — capture/persistence clocks cannot replace source observation truth (`96-113`)

1. **Behaviour:** supplies only capture and persistence times and expects a bounded validation error.
2. **Authority meaning:** source observation time/date and repository process clocks are different facts; process clocks must not substitute for missing source truth.
3. **Fit:** exact negative clause under the repo-wide temporal standard.
4. **Proved:** the current raw provenance model rejects the tested capture-only payload with the specified message.
5. **Not proved:** date-only precision preservation, local-time/offset consistency, identity/version/fingerprint completeness, contradiction handling or all source families.
6. **Falsifier:** accept the payload or raise a different failure.
7. **Required failure:** `pytest.raises` block `101-113`.
8. **Authority-violating implementation that passes:** require one source timestamp but invent provider, capture identity, schema version or fingerprint.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `boundary`.
11. **Disposition/gate:** valid narrow Tier-A temporal clause.

## 10. File-level disposition

- Assertion groups: `6`.
- Explicit proposition relationships: `6`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Reason: the file contains two valid bounded ingress/temporal behaviours, but it also treats explicitly nonconforming prepared and options surfaces as successful authority, proves only symbol presence for the public surface, and accepts an empty calendar bundle. The broad cross-surface test can stay green while mandatory identity, version, fingerprint and lineage obligations are absent.
- P3 repair gate: split the file by authority surface; retain explicit-section and capture-clock rejection clauses; replace prepared/options/calendar nominal assertions with proposition-complete typed fixtures and required negative tests from `C-002`, `C-004`, `C-005` and `C-008`.
- No implementation or test mutation executed.
