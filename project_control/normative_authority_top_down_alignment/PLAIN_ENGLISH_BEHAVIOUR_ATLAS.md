# Gate B Plain-English Behaviour Atlas

## Status
Gate B semantic reconstruction. Source, tests, configuration, schemas, fixtures and migrations were read-only. This atlas describes current alpha meaning and behaviour; it is not a repair report and does not upgrade any surface beyond `thin_seam`.

## Reading rule
Each statement separates intended purpose, observed code behaviour, test evidence and conformance. Passing tests are bounded evidence only. Honest placeholders, correct graceful failures and uncomposed seams are not automatically defects.

## B01 — Raw input definitions and source identity

### B01.1 — External source interface declaration

**Plain-English statement:** Declare which external source family and offline ingress mode a payload belongs to before native preparation, while preventing network, credential, trade, sizing or persistence authority from entering through the payload.

- **Inputs:** source_id; source_family; ingress_mode; typed_carrier_name; already-obtained payload; optional source timestamp/reference
- **Interpretation/transformation:** Validates the interface as offline-only, rejects credential declarations, recursively rejects forbidden authority keys, and deep-copies accepted payload material.
- **Outputs:** ExternalSourceValidationResult and/or ExternalPayloadCarrier
- **Downstream use:** An adapter or caller may use the detached payload for source-specific decoding.
- **Time/state dependence:** Stateless; carries source timestamp text but does not interpret it.
- **Identity/lineage:** source_id is required and supplied by the caller; the contract does not prove that it was source-issued or bind it to a captured artefact.
- **Current alpha status:** `locally_implemented_not_composed`
- **Disposition:** aligned thin seam locally; not the active common ingress path
- **Normative view:** 5.1; docs/03.1_DOMAIN_MODEL_WORKING.md:13-45; docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:13-42
- **Observed code:** src/nvda_desk/contracts/external_source.py:10-179
- **Current tests:** tests/tier_a/adapters_ingress/test_external_source_contract_surface.py; tests/tier_a/adapters_ingress/test_external_source_interface_boundary.py; tests/tier_a/adapters_ingress/test_external_source_transform_boundary_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Local validation and copy boundaries reflect the frozen intent, but market/options/calendar adapters do not consistently enter through this carrier, so it is not the authoritative composed ingress.
- **Gate C requirement:** Prove every admitted external family either enters through this contract or through an explicitly different source-owned contract; reject fabricated source identity and forbidden authority recursively.

### B01.2 — Raw market and options bundle decode

**Plain-English statement:** Collect one already-obtained market snapshot and options surface into an upstream typed bundle while preserving source temporal truth before preparation.

- **Inputs:** JSON/API-shaped mapping; optional snapshot_id; market_snapshot; options_surface; source_time_utc or source_date; provenance metadata
- **Interpretation/transformation:** Selects explicit market/options sections when present; otherwise treats the full payload or selected price/DTE subset as the section; constructs RawBundleProvenance and requires timestamp or date truth.
- **Outputs:** RealDataBundle containing market_snapshot, options_surface and provenance
- **Downstream use:** Runtime preparation service.
- **Time/state dependence:** Stateless; preserves timestamp/date and capture/persist metadata without interpreting market phase.
- **Identity/lineage:** snapshot_id is optional; no required source artefact ID, capture ID or content fingerprint is created.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** useful alpha decode seam with source-identity gap
- **Normative view:** 5.2-5.3; docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:44-77
- **Observed code:** src/nvda_desk/ingress/raw_bundle_loader.py:11-128
- **Current tests:** tests/tier_a/ingress/test_raw_bundle_loader_surface.py; tests/tier_a/temporal/test_fwd006_reopened_row_raw_capture_source_temporal_proof.py; tests/tier_a/temporal/test_raw_capture_transform_boundary_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Source temporal truth fails closed, but raw-capture identity and durable capture do not exist. Fallback section inference can blur source semantics.
- **Gate C requirement:** Require and preserve source/capture identity, test explicit section precedence, test that fallback inference cannot silently misclassify unrelated keys, and prove no cognition bypass.

### B01.3 — Market snapshot adapter

**Plain-English statement:** Provide a convenience adapter from a raw mapping to the first prepared runtime snapshot.

- **Inputs:** mapping; optional snapshot_id
- **Interpretation/transformation:** Copies snapshot_id into the mapping, decodes it as an API raw bundle, prepares a dataset, returns primary_snapshot.
- **Outputs:** PreparedRuntimeSnapshot
- **Downstream use:** API market_snapshot route or callers requiring prepared market state.
- **Time/state dependence:** Depends on source temporal fields and preparation alignment.
- **Identity/lineage:** Caller-supplied snapshot_id is optional; no source artefact identity is enforced.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** thin compatibility wrapper; bypasses ExternalPayloadCarrier
- **Normative view:** 5.1, 5.5
- **Observed code:** src/nvda_desk/adapters/ingress/market_snapshot_feed.py:1-23
- **Current tests:** tests/tier_a/adapters_ingress/test_external_source_transform_boundary_surface.py; tests/tier_a/upstream_cognition/test_prepared_runtime_transform_boundary_surface.py
- **Test assessment:** `insufficient`
- **Conformance:** The adapter reaches preparation but does not validate through the declared external source interface and cannot establish provider substitution or source-issued identity.
- **Gate C requirement:** Prove the adapter composes the authoritative external-source contract and preserves identity/temporal lineage.

### B01.4 — Options surface adapter

**Plain-English statement:** Provide a convenience adapter from raw options material to a typed options-flow stage input.

- **Inputs:** mapping with options surface and source temporal material
- **Interpretation/transformation:** Decodes raw bundle, prepares the primary snapshot, then maps spot/front DTE/next DTE into OptionsFlowContextInput.
- **Outputs:** OptionsFlowContextInput with explicit missing_fields
- **Downstream use:** Options-flow context classifier.
- **Time/state dependence:** Source time is required by raw decode but not carried in the options-flow contract.
- **Identity/lineage:** No options source artefact, chain snapshot or surface version identity survives into the output.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** local transform exists; lineage is stripped before cognition
- **Normative view:** 5.1, 5.3, 5.5
- **Observed code:** src/nvda_desk/adapters/ingress/options_surface_feed.py:1-20; src/nvda_desk/cognition/ingress/options_mapper.py:10-27
- **Current tests:** tests/tier_a/upstream_cognition/test_cognition_ingress_mapping_surfaces.py; tests/tier_a/upstream_signal/test_raw_signal_transform_boundary_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Typed missing-field behaviour exists, but source identity, observation time and surface version do not reach the options stage.
- **Gate C requirement:** Prove typed options payload identity/version/time carriage or explicitly define why the stage may consume only derived primitives.

### B01.5 — Financial calendar reference import

**Plain-English statement:** Load checked calendar/reference artefacts and their named layers without granting online mutation, candidate formation, trading or sizing authority.

- **Inputs:** manifest with bundle_id, version, artifacts and arbitrary layer references
- **Interpretation/transformation:** Rejects forbidden runtime-authority keys; types artefacts/layers; requires unique IDs and valid layer-to-artefact references.
- **Outputs:** ImportedReferenceBundle and optionally a reference DMP packet
- **Downstream use:** Calendar projection into precursor runtime context.
- **Time/state dependence:** Reference bundle is versioned; event effective time is introduced during projection.
- **Identity/lineage:** bundle_id, artifact_id and layer_id are explicit; source path and version are retained.
- **Current alpha status:** `operates_consistently_with_intent`
- **Disposition:** aligned local reference-ingress seam
- **Normative view:** 5.4; docs/03.1_DOMAIN_MODEL_WORKING.md:17-45
- **Observed code:** src/nvda_desk/calendar/reference/importer.py:17-135; src/nvda_desk/contracts/reference_data.py:8-35
- **Current tests:** tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py; tests/tier_a/financial_calendar/test_financial_calendar_authority_surface.py
- **Test assessment:** `normatively_aligned`
- **Conformance:** The local importer is explicit and fail-closed. The exact intended business meaning and number of calendar layers are not fixed by code; the manifest accepts any unique layer set.
- **Gate C requirement:** Preserve current negative tests and add authoritative fixture(s) proving the adopted calendar layer model once that model is explicitly specified.

### B01.6 — Operational calendar and event entry

**Plain-English statement:** Accept operator/API-created session and event records for bounded runtime calendar queries, separately from checked reference projection.

- **Inputs:** SessionCalendarDTO or MarketEventDTO with IDs, time window, symbol, materiality, tags and lineage IDs
- **Interpretation/transformation:** Appends records to in-process repositories; queries events by overlap, symbol and materiality; sorts by proximity and materiality.
- **Outputs:** Stored DTOs, lists, RuntimeCalendarSnapshot
- **Downstream use:** API calendar queries and Parallel Risk event-proximity context.
- **Time/state dependence:** Query uses explicit window and observed_at; repository lifetime is the Python process.
- **Identity/lineage:** Caller supplies event_id/session_id and optional lineage_ids; duplicates are not rejected.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** operational context seam exists; ownership/durability/duplicate law incomplete
- **Normative view:** 5.4, 5.16
- **Observed code:** src/nvda_desk/calendar/operational/events.py:11-155; src/nvda_desk/api/app.py:151-187
- **Current tests:** tests/tier_a/calendar_operational/test_calendar_operational_surface.py; tests/tier_a/financial_calendar/test_fwd008_runtime_calendar_query_contract.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Context-only flags are explicit, but process-memory storage, no duplicate protection and separate reference/operational paths prevent one authoritative calendar truth.
- **Gate C requirement:** Prove duplicate/identity rules, separation from candidate/sizing authority, and one explicit composition between checked reference projection and operational query state.

### B01.7 — Raw signal family and market substrate carriers

**Plain-English statement:** Represent raw or minimally derived market observations by signal family before preparation, without trade-decision side effects.

- **Inputs:** observation_id, signal_family_id, symbol, value, units, source_ids, tags and payload
- **Interpretation/transformation:** Validates typed observation/snapshot structure, deep-copies list fields and rejects declared trade-decision side effects.
- **Outputs:** MarketSubstrateSnapshot and raw signal family carriers/coverage records
- **Downstream use:** Preparation and trace/review support.
- **Time/state dependence:** No common timestamp field in MarketSubstrateObservation; temporal truth must arrive through adjacent contracts.
- **Identity/lineage:** Observation and family IDs are explicit; source_ids are optional and not owner-validated.
- **Current alpha status:** `locally_implemented_not_composed`
- **Disposition:** aligned typed seam, not a complete upstream composition
- **Normative view:** 5.3
- **Observed code:** src/nvda_desk/contracts/market_substrate.py:8-39; src/nvda_desk/upstream/market_substrate.py; src/nvda_desk/upstream/raw_signal_ingress.py; src/nvda_desk/upstream/raw_signal_coverage.py
- **Current tests:** tests/tier_a/upstream_signal/test_fwd007_raw_signal_family_rebuild_contract.py; tests/tier_a/upstream_signal/test_raw_signal_contract_copy_boundaries.py; tests/tier_a/upstream_signal/test_upstream_signal_coverage_map_and_scope_lock.py
- **Test assessment:** `partially_aligned`
- **Conformance:** The carriers constrain local authority but are not the types consumed by raw_bundle_loader/runtime_preparer, so the intended family extension seam is not end-to-end.
- **Gate C requirement:** Prove a new signal family can be added through a registry/adapter without changing unrelated preparation or cognition, and preserve timestamp/source identity.

## B02 — Input envelopes, schemas and validation

### B02.1 — Prepared runtime substrate envelope

**Plain-English statement:** Create a runtime-ready, detached snapshot from one or more raw bundles while retaining preparation lineage and explicit enrichment gaps.

- **Inputs:** RealDataBundle(s), optional explicit runtime_bar_time_utc
- **Interpretation/transformation:** Combines market/options/provenance sections, aligns to explicit or minute-floored bar time, derives bounded features, records missing/failed optional enrichments.
- **Outputs:** PreparedRuntimeSnapshot(s) and PreparedRuntimeDataset
- **Downstream use:** Cognition ingress translator and API prepared snapshot output.
- **Time/state dependence:** Uses source_time_utc/source_date and optional runtime bar; dataset order follows input order.
- **Identity/lineage:** snapshot_id remains optional; lineage records source kind, sections, alignment policy and derived field names, not source artefact IDs or payload hash.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** useful prepared boundary with incomplete lineage/schema authority
- **Normative view:** 5.5
- **Observed code:** src/nvda_desk/preparation/runtime_preparer.py:14-321
- **Current tests:** tests/tier_a/upstream_cognition/test_prepared_runtime_snapshot_contract_surface.py; tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py; tests/tier_a/seam_boundaries/test_prepared_ingress_checkpoint_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Prepared state is detached and explicit about enrichment failures, but it remains a generic payload mapping and lacks mandatory identity/version fields.
- **Gate C requirement:** Define and prove the stable common envelope plus strongly typed payload contracts; require source/capture IDs and schema version without generic-dictionary drift.

### B02.2 — Stage input bundle

**Plain-English statement:** Translate one prepared snapshot into the typed primitives consumed by the serial cognitive stages.

- **Inputs:** PreparedRuntimeSnapshot or PreparedRuntimeDataset primary snapshot
- **Interpretation/transformation:** Maps temporal, regime and options-flow fields into three Pydantic contracts; records missing numeric fields and rejects invalid types.
- **Outputs:** StageInputBundle containing temporal, regime and options_flow inputs
- **Downstream use:** DeskRuntimeOrchestrator and Parallel Risk bootstrap.
- **Time/state dependence:** Temporal contract retains source time; regime/options contracts do not retain source identity/time.
- **Identity/lineage:** Bundle has no bundle_id, schema version or input source IDs; identity is later inferred from content/time.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** typed boundary exists but is not a complete authoritative runtime envelope
- **Normative view:** 5.5, 5.7
- **Observed code:** src/nvda_desk/cognition/ingress/translator.py:16-41; src/nvda_desk/contracts/stage_inputs.py
- **Current tests:** tests/tier_a/upstream_cognition/test_cognition_ingress_translation_coordinator.py; tests/tier_a/upstream_cognition/test_fwd009_reopened_row_prepared_ingress_runtime_context_proof.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Typed stage inputs are clear, but the bundle does not carry provenance/configuration versions needed to reconstruct why later decisions occurred.
- **Gate C requirement:** Prove mandatory bundle identity, source lineage and policy/config version carriage while preserving typed stage contracts.

### B02.3 — DMPV3 boundary placement

**Plain-English statement:** Carry outputs between deliberate runtime module boundaries after raw input and preparation, not redefine upstream raw material as packets.

- **Inputs:** Typed stage outputs or admitted reference/prepared/parallel-risk payloads plus packet identity, producer and lineage metadata
- **Interpretation/transformation:** Builds DeskModulePacketV3 envelopes with module/grammar metadata, validation and lineage structures.
- **Outputs:** DMPV3 packets
- **Downstream use:** Serial packet chain, Parallel Risk lane, capital/review/persistence surfaces.
- **Time/state dependence:** emitted_at is packet occurrence time; source time remains payload/lineage material.
- **Identity/lineage:** packet_id is required by explicit builders, but generic defaults can manufacture trace/run/scenario/module-instance identities and wall-clock emission time.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** packet carriage begins at deliberate module outputs; identity defaults remain alpha gaps
- **Normative view:** 5.6; docs/09_DMPV3_PROTOCOL_CORE.md; docs/09.1_DMPV3_PROTOCOL_WORKING.md:15-151
- **Observed code:** src/nvda_desk/contracts/packets.py:1-252; src/nvda_desk/packets/dmp_packets.py:1-408
- **Current tests:** tests/tier_a/packets/test_dmpv3_transform_boundary_surface.py; tests/tier_a/packets/test_fwd004_reopened_row_packet_carriage_proof.py; tests/tier_a/packets/test_dmpv3_extension_canonical_leaf_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Typed carriage exists and correctly begins after preparation/at module seams, but default-generated authority identities and wall-clock packet metadata do not meet the frozen lineage/replay law.
- **Gate C requirement:** Require role-specific mandatory IDs, source artefact lineage and deterministic packet reproduction rules; test that pre-DMP inputs remain non-DMP.

## B03 — Canonicalisation and normalisation

### B03.1 — Raw section canonicalisation

**Plain-English statement:** Resolve overlapping market, options and provenance fields into one prepared payload with predictable precedence.

- **Inputs:** RealDataBundle market_snapshot, options_surface and provenance
- **Interpretation/transformation:** Creates market_spot_price and options_spot_price; chooses options spot as canonical spot when present; copies selected return, volatility, close and temporal keys by market→options→provenance precedence; normalises event windows.
- **Outputs:** Combined prepared payload
- **Downstream use:** Feature derivation and cognition mappers.
- **Time/state dependence:** Source temporal values are copied; no timezone conversion occurs here.
- **Identity/lineage:** No field-level provenance records which source section won each value.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** deterministic local normalisation with semantic-loss risk
- **Normative view:** 5.5
- **Observed code:** src/nvda_desk/preparation/runtime_preparer.py:324-449
- **Current tests:** tests/tier_a/upstream_cognition/test_prepared_runtime_transform_boundary_surface.py; tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Precedence is deterministic but implicit. Different source sections can be collapsed without field-level lineage or conflict reporting.
- **Gate C requirement:** Prove precedence and conflict behaviour, preserve source-section provenance per canonical field, and reject semantic collisions where silent choice is unsafe.

### B03.2 — Prepared feature derivation

**Plain-English statement:** Add simple deterministic runtime features while explicitly distinguishing missing optional inputs from failed derivations.

- **Inputs:** prepared payload fields: windows, source/next event times, front/next DTE, market spot and prior/reference close
- **Interpretation/transformation:** Derives window_count/has_windows, minutes_to_next_event, DTE spread and NVDA return; records missing_optional_enrichments or failed_enrichments.
- **Outputs:** derived_fields merged into prepared payload plus enrichment status lists
- **Downstream use:** Cognition mappers and review/checkpoint surfaces.
- **Time/state dependence:** minutes_to_next_event depends on source observation time; DTE spread and return are point-in-time.
- **Identity/lineage:** Derived fields are named in lineage, but derivation version/formula identity is absent.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** honest alpha derivation seam; versioning incomplete
- **Normative view:** 5.5, 5.9
- **Observed code:** src/nvda_desk/preparation/runtime_preparer.py:146-207
- **Current tests:** tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py; tests/tier_a/upstream_cognition/test_prepared_context_packet_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Missing and failed enrichments are truthfully separated, but formula/version lineage is insufficient for long-lived replay or safe future replacement.
- **Gate C requirement:** Prove derivation version, input provenance and deterministic replay for each material derived field.

### B03.3 — Cognition ingress field mapping

**Plain-English statement:** Convert prepared values into narrowly typed temporal, regime and options-flow inputs without letting downstream stages inspect the whole raw payload.

- **Inputs:** prepared mapping
- **Interpretation/transformation:** Temporal mapper requires timestamp/date and validates windows/types; regime/options mappers cast selected numeric fields and enumerate missing fields.
- **Outputs:** TemporalContextInput, MarketRegimeContextInput, OptionsFlowContextInput
- **Downstream use:** Temporal, regime and options-flow services.
- **Time/state dependence:** Only temporal input carries source time and windows.
- **Identity/lineage:** Source/provider/snapshot identity is not propagated to regime or options-flow inputs.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** good narrowing seam with incomplete cross-stage lineage
- **Normative view:** 5.5, 5.7
- **Observed code:** src/nvda_desk/cognition/ingress/temporal_mapper.py:15-82; src/nvda_desk/cognition/ingress/regime_mapper.py:10-28; src/nvda_desk/cognition/ingress/options_mapper.py:10-27
- **Current tests:** tests/tier_a/upstream_cognition/test_cognition_ingress_mapping_surfaces.py; tests/tier_a/upstream_cognition/test_regime_ingress_surface.py
- **Test assessment:** `normatively_aligned`
- **Conformance:** Type and missing-field handling are clear; lineage/context versions disappear from two of three stage inputs.
- **Gate C requirement:** Preserve source/bundle identity and schema/policy versions without widening stage-specific payloads.

## B04 — Identifier and lineage propagation

### B04.1 — Source, capture, domain and packet identity distinction

**Plain-English statement:** Keep the identity of an upstream source artefact separate from repository capture, domain observation, prepared snapshot, runtime run and packet occurrence.

- **Inputs:** source_id/snapshot_id/observation_id/bundle_id/context_id/packet_id and related metadata across contracts
- **Interpretation/transformation:** Current code validates many local IDs but does not enforce one cross-surface origin/propagation model.
- **Outputs:** Multiple local identifiers with partial relationships
- **Downstream use:** Every stage, persistence, review and replay.
- **Time/state dependence:** Some IDs are derived from source time; others caller supplied.
- **Identity/lineage:** Authoritative owner is inconsistent; snapshot_id optional; serial trace/run IDs derived from time; API can supply/fallback IDs on some paths.
- **Current alpha status:** `behaves_differently_from_intent`
- **Disposition:** cross-cutting hidden-fallback/ownership gap
- **Normative view:** docs/03.1_DOMAIN_MODEL_WORKING.md:25-45; docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:13-42; docs/09.1_DMPV3_PROTOCOL_WORKING.md:15-61
- **Observed code:** src/nvda_desk/ingress/raw_bundle_loader.py:35-42; src/nvda_desk/runtime/orchestrator.py:115-123; src/nvda_desk/packets/dmp_packets.py:1-408; src/nvda_desk/api/app.py:51-471
- **Current tests:** tests/tier_a/temporal/test_fwd006_reopened_row_raw_capture_source_temporal_proof.py; tests/tier_a/packets/test_parallel_risk_lineage_completeness.py; tests/tier_b/review_lineage/test_review_replay_dmp_v3_lineage.py
- **Test assessment:** `insufficient`
- **Conformance:** Local non-empty checks do not prove authoritative origin. Current paths can continue with optional or manufactured identity, contrary to fail-closed lineage law.
- **Gate C requirement:** Create an identifier-role matrix in tests: owner, mandatory/optional status, propagation and forbidden fabrication for every material ID.

### B04.2 — Prepared lineage record

**Plain-English statement:** Explain how one prepared snapshot was formed from raw sections and which derived fields were added.

- **Inputs:** raw bundle provenance, snapshot_id, source sections, runtime bar choice and derived fields
- **Interpretation/transformation:** Stores source_kind, transport, optional source_snapshot_id, source_sections, alignment_policy, runtime_bar_time and derived field names.
- **Outputs:** PreparedRuntimeLineage attached to snapshot and dataset
- **Downstream use:** Prepared context/checkpoint/review consumers.
- **Time/state dependence:** Captures selected runtime bar but not immutable original payload bytes.
- **Identity/lineage:** No source artefact IDs, input fingerprint or schema/config version in this lineage object.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** honest local lineage, insufficient for exact replay
- **Normative view:** 5.2, 5.5, 5.15-5.16
- **Observed code:** src/nvda_desk/preparation/runtime_preparer.py:14-24,291-321
- **Current tests:** tests/tier_a/upstream_cognition/test_prepared_runtime_snapshot_contract_surface.py; tests/tier_a/seam_boundaries/test_prepared_ingress_checkpoint_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** It truthfully describes preparation mechanics but cannot prove which original artefact bytes and policy versions produced the result.
- **Gate C requirement:** Require source artefact IDs/fingerprint and preparation policy/schema versions; prove detached copy and replay equivalence.

### B04.3 — Serial packet lineage chain

**Plain-English statement:** Emit one packet per serial stage with ordered parent/dependency links and a common run/trace context.

- **Inputs:** six stage outputs, source_time_utc, input fingerprint and packet metadata
- **Interpretation/transformation:** Derives deterministic packet IDs from stage name and source time; links previous packet and declared dependencies; adds derivedfrom and summary.
- **Outputs:** six DMPV3 stage packets and IDs
- **Downstream use:** Parallel Risk bootstrap, review and potential persistence.
- **Time/state dependence:** Packet IDs use source time; all emitted_at fields use one current wall-clock time per run.
- **Identity/lineage:** traceid/runid are time-derived, scenarioid hard-coded live, sourceartifactids empty, module_version native.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** ordered local chain with fabricated/empty lineage roles
- **Normative view:** 5.6-5.7; docs/09.1_DMPV3_PROTOCOL_WORKING.md:104-151
- **Observed code:** src/nvda_desk/runtime/orchestrator.py:115-239
- **Current tests:** tests/tier_a/runtime/test_serial_stage_packet_emission_surface.py; tests/tier_a/runtime/test_fwd012_reopened_row_serial_cognition_spine_proof.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Parent/dependency structure is explicit, but packet occurrence and authoritative execution/source lineage are not replay-safe.
- **Gate C requirement:** Prove required sourceartifactids, supplied execution context IDs, deterministic domain outputs independent of emitted_at, and exact dependency semantics.

### B04.4 — Parallel Risk packet lineage

**Plain-English statement:** Carry selected temporal/StageInput evidence into the independent Parallel Risk lane without giving the lane capital-sizing authority.

- **Inputs:** StageInputBundle or selected serial temporal stage packet plus explicit packet IDs and lineage metadata
- **Interpretation/transformation:** Builds bootstrap packet, evaluates lane output, preserves parent/dependency/source artefact and input fingerprint fields when supplied.
- **Outputs:** bootstrap input packet, lane packet and optional minute profile
- **Downstream use:** Risk review, final risk and capital authority inputs.
- **Time/state dependence:** Uses packet emitted time and temporal input; minute profile generated_at follows lane packet.
- **Identity/lineage:** run_bootstrap permits many lineage IDs to be omitted; run_from_serial derives new packet IDs from temporal packet time token.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** explicit boundary with optional lineage and global policy state outside packet chain
- **Normative view:** 5.8; docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:163-171
- **Observed code:** src/nvda_desk/services/parallel_risk_lane_service.py:35-150; src/nvda_desk/risk/parallel/evaluate.py
- **Current tests:** tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py; tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_input_surface.py; tests/tier_a/testing_harnesses/test_serial_runtime_parallel_risk_boundary_specimen_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** The serial-to-PRL selection is explicit, but optional IDs and incomplete composition prevent one authoritative end-to-end lineage.
- **Gate C requirement:** Require input/parent/dependency/source IDs at admitted runtime boundaries and prove no serial outputs other than declared inputs influence the lane.

## B05 — Intermediate state ownership

### B05.1 — Financial calendar state ownership

**Plain-English statement:** Maintain reference calendar truth, operational event/session rows and context projections as separate concerns.

- **Inputs:** checked manifest/bundle; event rows; operational DTOs; runtime queries
- **Interpretation/transformation:** Reference importer/projector is deterministic; operational repositories append/query process-memory rows; bounded SQLite also stores session_calendars separately.
- **Outputs:** ImportedReferenceBundle, PrecursorRuntimePacket, RuntimeCalendarSnapshot, session rows
- **Downstream use:** Preparation, temporal context, Parallel Risk and API.
- **Time/state dependence:** Reference version/effective_at plus operational windows; stores have separate lifetimes.
- **Identity/lineage:** bundle/artifact/layer/event/session IDs exist, but no single calendar-state owner reconciles all stores.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** four-ish technical layers exist, but one authoritative four-layer business model is not established
- **Normative view:** 5.4, 5.16
- **Observed code:** src/nvda_desk/calendar/reference/importer.py:17-135; src/nvda_desk/calendar/reference/projection.py:14-95; src/nvda_desk/calendar/operational/events.py:11-155; src/nvda_desk/persistence/durable_sql.py:1-103
- **Current tests:** tests/tier_a/financial_calendar/test_financial_calendar_authority_surface.py; test_financial_calendar_transform_boundary_surface.py; tests/tier_a/calendar_operational/test_calendar_operational_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** The code separates checked reference import, projection, operational query and SQL fixtures, but does not establish their precedence, synchronisation or exact intended layer model.
- **Gate C requirement:** Before tests, confirm the authoritative calendar layer model; then prove owner, precedence, identity and substitution at each layer.

### B05.2 — Core material runtime state repositories

**Plain-English statement:** Hold capital snapshots, positions, execution events, market observations, options-flow history, review packets and research logs behind repository-like APIs.

- **Inputs:** typed state records or IDs/payloads
- **Interpretation/transformation:** Append/store deep copies, reject selected duplicates, return detached copies.
- **Outputs:** current/list/read state
- **Downstream use:** Live inventory, API, review/replay and downstream decisions.
- **Time/state dependence:** State survives only for the life of the repository/service instance.
- **Identity/lineage:** Local record IDs required; cross-repository transaction or lineage coupling absent.
- **Current alpha status:** `locally_implemented_not_composed`
- **Disposition:** replaceable local repository seams; material state is non-durable
- **Normative view:** 5.13, 5.15-5.16
- **Observed code:** src/nvda_desk/repositories/capital_state_repository.py; src/nvda_desk/repositories/position_repository.py; src/nvda_desk/repositories/execution_event_repository.py; src/nvda_desk/repositories/market_observation_repository.py; src/nvda_desk/repositories/options_flow_history_repository.py; src/nvda_desk/repositories/review_repository.py; src/nvda_desk/repositories/research_logs.py
- **Current tests:** tests/tier_a/persistence/test_append_only_repository_surfaces.py; test_capital_state_repository_surface.py; test_position_repository_surface.py; tests/tier_a/review_runtime/test_review_repository_surface.py
- **Test assessment:** `implementation_locked`
- **Conformance:** Tests prove local process-memory behaviour and copy semantics, not the normative durable-state/replay objective.
- **Gate C requirement:** Retain local contract tests but add restart/durable adapter contract tests only where the normative boundary requires durability; never label memory stores durable.

### B05.3 — Parallel Risk policy-decision state

**Plain-English statement:** Record policy observations produced by the Parallel Risk gateway without capital sizing.

- **Inputs:** policy_id and optional candidate semantics
- **Interpretation/transformation:** Builds a decision and appends it to module-global _RISK_POLICY_DECISIONS.
- **Outputs:** ParallelRiskPolicyDecision and list of all process decisions
- **Downstream use:** API/risk review consumers.
- **Time/state dependence:** Shared across all service instances in one process; lost on restart; no session/run partition.
- **Identity/lineage:** decision_id is constructed from policy_id and candidate_id/no_candidate, allowing collisions across runs.
- **Current alpha status:** `behaves_differently_from_intent`
- **Disposition:** architectural coupling and state-ownership defect
- **Normative view:** 5.8, 5.16
- **Observed code:** src/nvda_desk/services/parallel_risk_lane_service.py:22,169-192
- **Current tests:** tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py; tests/tier_a/parallel_risk/test_fwd013_parallel_risk_candidate_enrichment_contract.py
- **Test assessment:** `insufficient`
- **Conformance:** The lane owns process-global mutable history rather than an injected state owner, undermining isolation, replay and concurrent run separation.
- **Gate C requirement:** Prove injected repository ownership, run/session identity, duplicate law and isolation between service instances/tests.

### B05.4 — API-local veto and risk-block state

**Plain-English statement:** Expose small in-process lists of veto/risk-block events through the API shell.

- **Inputs:** API method payloads
- **Interpretation/transformation:** Appends plain dictionaries to HttpApp instance lists.
- **Outputs:** list/read API responses
- **Downstream use:** API clients only.
- **Time/state dependence:** Per HttpApp instance; lost on restart.
- **Identity/lineage:** No governed event model, owner or persistence identity.
- **Current alpha status:** `honest_placeholder`
- **Disposition:** local shell state, not authoritative risk state
- **Normative view:** 5.1, 5.8, 5.16
- **Observed code:** src/nvda_desk/api/app.py:85-86,376-390
- **Current tests:** tests/tier_a/api/test_api_boundary_surface.py; tests/tier_a/api/test_fwd005_api_exposure_contract.py
- **Test assessment:** `insufficient`
- **Conformance:** Acceptable only as explicitly non-authoritative alpha shell state; current API class also owns too many unrelated responsibilities.
- **Gate C requirement:** Either remove from admitted architecture or define typed owner/contract; test that API storage cannot influence domain decisions directly.

## B06 — Persistence boundaries

### B06.1 — Bounded SQLite persistence

**Plain-English statement:** Provide a simple file-backed store for dev intraday bars, option snapshots and session calendars.

- **Inputs:** database path; seed rows or SQL inserts
- **Interpretation/transformation:** Creates three tables, seeds deterministic demo data, lists rows.
- **Outputs:** SQLite file and row dictionaries
- **Downstream use:** Development fixtures/tests; not main runtime orchestration.
- **Time/state dependence:** Persists across process restart at the supplied path.
- **Identity/lineage:** bar_id, snapshot_id and session_id primary keys; no lineage/config version columns.
- **Current alpha status:** `locally_implemented_not_composed`
- **Disposition:** real bounded persistence, not the material state authority
- **Normative view:** 5.4, 5.16
- **Observed code:** src/nvda_desk/persistence/durable_sql.py:1-103
- **Current tests:** tests/tier_a/persistence/test_fwd003_durable_sql_contract.py; tests/tier_a/persistence/test_persistence_session_boundary_surface.py
- **Test assessment:** `implementation_locked`
- **Conformance:** The store is durable but narrow and disconnected from most runtime owners; calling the wider system durable would be false.
- **Gate C requirement:** Prove only the intended bounded SQL contract; define separate repository ports before connecting material runtime state.

### B06.2 — In-memory persistence adapters

**Plain-English statement:** Offer repository APIs for alpha development while keeping domain code separate from eventual storage technology.

- **Inputs:** typed records
- **Interpretation/transformation:** Stores deep copies in dicts/lists and enforces local duplicate rules.
- **Outputs:** detached reads/lists
- **Downstream use:** Services and API.
- **Time/state dependence:** Process lifetime only.
- **Identity/lineage:** Record-local IDs; no restart or transaction envelope.
- **Current alpha status:** `honest_placeholder`
- **Disposition:** valid alpha adapter if labelled non-durable
- **Normative view:** 5.16; docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:78-110
- **Observed code:** src/nvda_desk/repositories/capital_state_repository.py; src/nvda_desk/repositories/position_repository.py; src/nvda_desk/repositories/execution_event_repository.py; src/nvda_desk/repositories/market_observation_repository.py; src/nvda_desk/repositories/options_flow_history_repository.py; src/nvda_desk/repositories/review_repository.py; src/nvda_desk/repositories/research_logs.py; src/nvda_desk/analysis/replay/sidecar.py
- **Current tests:** tests/tier_a/persistence/*; tests/tier_a/options_flow_history/*
- **Test assessment:** `implementation_locked`
- **Conformance:** The abstraction seam is useful, but current tests and names sometimes imply persistence without proving restart survival.
- **Gate C requirement:** Create shared repository contract tests that run against memory and future durable adapters, explicitly separating persistence semantics from interface semantics.

### B06.3 — Receipt and execution record ledgers

**Plain-English statement:** Record receipts/execution events for later review without mutating trading decisions.

- **Inputs:** receipt_id/type/payload; execution records
- **Interpretation/transformation:** Append with duplicate checks and return copies; current implementations are in memory.
- **Outputs:** receipt/execution record collections
- **Downstream use:** Live inventory, review packet service and API.
- **Time/state dependence:** Process lifetime; ordering is insertion order.
- **Identity/lineage:** Receipt IDs supplied by callers; no atomic link to decisions, positions or capital updates.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** local audit-shaped seam without transaction/recovery guarantee
- **Normative view:** 5.15-5.16
- **Observed code:** src/nvda_desk/persistence/receipt_ledger.py; src/nvda_desk/persistence/execution_records.py
- **Current tests:** tests/tier_a/persistence/test_receipt_ledger_surface.py; test_execution_records_repository_surface.py; tests/tier_b/proof_model/test_checkpoint_receipt_contract.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Receipts can be recorded, but they do not prove that all material state changes were atomically captured or are replayable after restart.
- **Gate C requirement:** Prove receipt sequencing, idempotency and consistency with state changes at the smallest admitted transaction boundary.

## B07 — Deterministic transformations and algorithms

### B07.1 — Temporal context evaluation

**Plain-English statement:** Convert source observation time and scheduled event windows into a coarse session state, active event tags and next-event time.

- **Inputs:** TemporalContextInput with source_time_utc, optional source timezone/date/provenance, windows and optional next event
- **Interpretation/transformation:** Converts UTC observation to supplied timezone; applies fixed clock thresholds; tags active windows; selects earliest future window if next event absent.
- **Outputs:** TemporalContextOutput
- **Downstream use:** Serial posture/execution context, Parallel Risk and capital authority.
- **Time/state dependence:** Point-in-time, dependent on timezone and event window boundaries.
- **Identity/lineage:** Preserves source temporal metadata, not source artefact ID.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** coarse deterministic temporal seam
- **Normative view:** 5.2, 5.4, 5.7
- **Observed code:** src/nvda_desk/services/temporal_context_service.py:14-41; src/nvda_desk/domain/temporal/session_clock.py:7-50; src/nvda_desk/domain/temporal/event_windows.py:11-30
- **Current tests:** tests/tier_a/temporal/test_source_temporal_standard_surface.py; tests/tier_a/financial_calendar/test_fwd008_runtime_calendar_query_contract.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Source-time and scheduled-window handling are explicit; phase logic is coarse and clock-only.
- **Gate C requirement:** Preserve current source-time/timezone tests and add policy/version tests for the accepted temporal classifier.

### B07.2 — Signal-informed intraday phase interpretation

**Plain-English statement:** Represent the human trader’s evolving sense of market phase, where opening/HFT dominance decays according to observed liquidity, volume, spread and microstructure signals rather than at a magical fixed time.

- **Inputs:** Expected: source/session time plus admitted market microstructure and activity signals; current code: source_time_utc and timezone only
- **Interpretation/transformation:** Expected: stateful/evidence-based phase transition; current code: fixed pre_open/opening/mid_session/closing/post_close thresholds at 09:30, 10:30, 15:30 and 16:00.
- **Outputs:** Expected detailed intraday phase and evidence; current output coarse session_state.
- **Downstream use:** Temporal context, posture, playbook/risk interpretation and review.
- **Time/state dependence:** Should depend on recent signal history as well as wall clock; current implementation is stateless clock classification.
- **Identity/lineage:** Expected phase evidence/version not present.
- **Current alpha status:** `behaves_differently_from_intent`
- **Disposition:** direct user-intent gap; frozen normative corpus is too general to specify the detailed algorithm
- **Normative view:** Direct user architecture instruction 2026-07-17; frozen surfaces 5.2, 5.4, 5.7; detailed algorithm remains absent from normative corpus
- **Observed code:** src/nvda_desk/domain/temporal/session_clock.py:7-32; docs/planning/PRL_MINUTE_RISK_PROFILE_IMPLEMENTATION_PLAN.md:72,91 (non-authoritative planning evidence)
- **Current tests:** Current temporal tests cover fixed thresholds; no admitted test proves signal-driven phase transition.
- **Test assessment:** `misleading`
- **Conformance:** Current code can truthfully report a coarse clock bucket but cannot claim to emulate signal-informed intraday phase cognition.
- **Gate C requirement:** PREREQUISITE: create a numbered normative addendum defining phase inputs, transition semantics, state/history, versioning and graceful degradation; then write signal-path and anti-clock-cutoff tests.

### B07.3 — Market regime classification

**Plain-English statement:** Summarise NVDA versus NQ movement and VIX into a bounded volatility/cross-asset regime context.

- **Inputs:** nvda_return_pct, nq_return_pct, vix_level and missing_fields
- **Interpretation/transformation:** Computes absolute NVDA–NQ difference; classifies high_volatility at VIX>=30, divergent at dispersion>=2, normal when complete, otherwise unknown; records reasons.
- **Outputs:** MarketRegimeContextOutput
- **Downstream use:** Posture and execution context.
- **Time/state dependence:** Point-in-time; no rolling history or source identity.
- **Identity/lineage:** No regime policy/version or input IDs.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** simple deterministic placeholder classifier
- **Normative view:** 5.7
- **Observed code:** src/nvda_desk/domain/regime/classification.py:8-52; src/nvda_desk/contracts/regime.py:8-25
- **Current tests:** tests/tier_a/upstream_cognition/test_regime_contract_models.py; test_regime_ingress_surface.py; tests/tier_b/review_lineage/test_bounded_trace_review_regime.py
- **Test assessment:** `partially_aligned`
- **Conformance:** The algorithm is explicit and honest but far narrower than tier-one trader regime cognition; no version/history context is carried.
- **Gate C requirement:** Prove current bounded classifier exactly, unknown handling and policy-version carriage; do not inflate scope until normative requirements expand.

### B07.4 — Options-flow surface classification

**Plain-English statement:** Provide a bounded options context from spot and front/next expiry distance.

- **Inputs:** spot_price, front_dte, next_dte and missing_fields
- **Interpretation/transformation:** Classifies DTE ordering as contango/backwardation/flat, marks gamma active for positive spot, leaves skew unknown.
- **Outputs:** OptionsFlowContextOutput
- **Downstream use:** Execution context and review.
- **Time/state dependence:** Point-in-time; no option chain, flow history, greeks or surface version.
- **Identity/lineage:** No options snapshot/source ID.
- **Current alpha status:** `honest_placeholder`
- **Disposition:** truthful minimal placeholder, not substantive options-flow cognition
- **Normative view:** 5.7
- **Observed code:** src/nvda_desk/domain/options_flow/surface_state.py:8-51; src/nvda_desk/contracts/options_flow.py:8-25
- **Current tests:** tests/tier_a/options_flow_history/test_options_flow_contract_models.py; tests/tier_b/serial_boundaries/test_options_flow_output_contract_isolation.py
- **Test assessment:** `normatively_aligned`
- **Conformance:** The code clearly exposes limited current behaviour and unknown skew; the name “options flow” is broader than the actual DTE/spot logic.
- **Gate C requirement:** Prove honest unknowns and isolation; future richer flow must enter through versioned contracts rather than changing unrelated stages.

### B07.5 — Posture and risk-permission stage

**Plain-English statement:** Translate market regime into a bounded stand-down/permit posture while applying governed posture coefficient modifiers.

- **Inputs:** MarketRegimeContextOutput; optional active modifier IDs or packet
- **Interpretation/transformation:** Loads baseline coefficient values, builds/resolves modifier packet, evaluates posture permission, attaches effective coefficient lineage to local envelope.
- **Outputs:** PostureRiskOutput
- **Downstream use:** Playbook eligibility and execution context.
- **Time/state dependence:** Stateless per call except config file contents; no run/version identity in output.
- **Identity/lineage:** Modifier IDs and coefficient IDs appear in envelope; coefficient document/version fingerprint is not consistently carried.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** local deterministic posture seam with incomplete policy versioning
- **Normative view:** 5.7, 5.9
- **Observed code:** src/nvda_desk/services/posture_service.py; src/nvda_desk/cognition/serial/posture.py; src/nvda_desk/domain/posture/permission.py; src/nvda_desk/cognition/modifiers/state_conditioned.py
- **Current tests:** tests/tier_a/modifiers/test_state_conditioned_modifier_surface.py; tests/tier_b/serial_boundaries/test_posture_permission_envelope.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Modifier application is explicit, but runtime composition usually supplies no active modifiers and the output does not carry one immutable authority-document version.
- **Gate C requirement:** Prove baseline/effective values, modifier precedence, immutable authority version/fingerprint and no policy smuggling.

### B07.6 — Dynamic coefficient authority

**Plain-English statement:** Load named coefficient surfaces and apply only explicitly admitted modifier policies at their owning stage.

- **Inputs:** governed coefficient JSON, owner_stage and active_modifier_ids
- **Interpretation/transformation:** Validates records/policies, rejects duplicates/unknown IDs, starts from baseline values and applies explicit effects only to admitted surfaces.
- **Outputs:** ModifierRuntimePacket and replay receipt
- **Downstream use:** Posture now; execution-side application is reserved/no-op.
- **Time/state dependence:** Configuration-file dependent; deterministic for the same document and requested policy IDs.
- **Identity/lineage:** Coefficient/policy IDs explicit; packet_id is owner-stage based; full document version/fingerprint not universally propagated.
- **Current alpha status:** `locally_implemented_not_composed`
- **Disposition:** good replaceable local authority seam; consumer integration incomplete
- **Normative view:** 5.9
- **Observed code:** src/nvda_desk/config/coefficient_authority.py; src/nvda_desk/contracts/coefficient_authority.py; src/nvda_desk/cognition/modifiers/state_conditioned.py:24-110
- **Current tests:** tests/tier_a/config/test_sequence8_coefficient_modifier_authority_specimen.py; test_coefficient_modifier_replay_surface.py; tests/tier_a/modifiers/test_dynamic_modifier_transform_boundary_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** The local authority boundary is strong, but orchestrated use, version carriage and execution-side modifiers are incomplete.
- **Gate C requirement:** Prove substitution of coefficient documents/policies without changing consumers, carry document fingerprint/version, and keep execution modifiers fail-closed until admitted.

### B07.7 — Six-stage serial runtime orchestration

**Plain-English statement:** Run one deterministic alpha serial pass through temporal, regime, options, posture, playbook eligibility and execution expression.

- **Inputs:** StageInputBundle; optional read-only live inventory attachment
- **Interpretation/transformation:** Evaluates stages in fixed order; eligibility receives an empty candidate family list; builds six packets and a stage-local handoff; non-valid mappings instead return structural executed/missing-stage inspection.
- **Outputs:** runtime receipt with stage outputs, packets, dependencies and handoff; optional read-only inventory
- **Downstream use:** Parallel Risk boundary, review and API.
- **Time/state dependence:** Domain stages mostly deterministic; packet emitted_at uses current wall clock.
- **Identity/lineage:** Run/trace IDs derived from source time; scenario hard-coded live; structural-inspection path can silently replace governed execution on validation failure.
- **Current alpha status:** `behaves_differently_from_intent`
- **Disposition:** partial serial path plus hidden dual-mode fallback
- **Normative view:** 5.7; docs/05.1_GUARDRAILS_WORKING.md fail-closed law
- **Observed code:** src/nvda_desk/runtime/orchestrator.py:33-187,243-320
- **Current tests:** tests/tier_a/runtime/test_runtime_orchestrator_surface.py; test_fwd012_reopened_row_serial_cognition_spine_proof.py; test_serial_stage_packet_emission_surface.py
- **Test assessment:** `misleading`
- **Conformance:** Tests prove both paths locally, but invalid governed input becomes a structural receipt rather than failing closed; the active path cannot select any playbook because candidate_family_ids is hard-coded empty.
- **Gate C requirement:** Separate explicit inspection API from governed run_once; fail closed on invalid execution input; supply candidate families through an owned contract; make domain replay independent of wall clock.

## B08 — Strategy/playbook selection and execution

### B08.1 — Playbook registry and library

**Plain-English statement:** Represent a replaceable set of named strategy/playbook definitions, setup variants, eligibility constraints and selection metadata without hidden capital or broker authority.

- **Inputs:** playbook registry configuration
- **Interpretation/transformation:** Validates IDs, uniqueness and forbidden authority keys; loads enabled playbooks and emits metadata receipts/fingerprints.
- **Outputs:** PlaybookRegistry/PlaybookDefinition/library views and metadata receipts
- **Downstream use:** Playbook eligibility and API strategy listing.
- **Time/state dependence:** Configuration snapshot; no runtime state.
- **Identity/lineage:** playbook_id, setup_family/variant and registry fingerprint explicit.
- **Current alpha status:** `locally_implemented_not_composed`
- **Disposition:** correct modular direction; registry is not wired into serial candidate-family input
- **Normative view:** 5.10; docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md:44-60
- **Observed code:** src/nvda_desk/config/playbook_registry.py; src/nvda_desk/playbooks/library.py; src/nvda_desk/contracts/playbook.py
- **Current tests:** tests/tier_a/playbook/test_playbook_library_architecture_surface.py; test_playbook_transform_boundary_surface.py; test_fwd011_reopened_row_playbook_library_authority_proof.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Definitions are modular and authority-smuggling is rejected, but adding ten playbooks is only easy at registry level; runtime selection remains disconnected.
- **Gate C requirement:** Prove registry-driven composition: add/remove a playbook without editing orchestrator/eligibility/domain code, preserve stable contract and reject unknown/disabled definitions.

### B08.2 — Playbook eligibility compilation

**Plain-English statement:** Filter candidate playbook families through posture permission and registry constraints.

- **Inputs:** PostureRiskOutput and candidate_family_ids; optional registry/service metadata
- **Interpretation/transformation:** If posture does not permit, returns no active families; otherwise compiles/filters candidates. In the orchestrator, candidate_family_ids is always empty.
- **Outputs:** PlaybookEligibilityOutput with active/excluded families and reasons
- **Downstream use:** Execution expression.
- **Time/state dependence:** Stateless.
- **Identity/lineage:** Candidate family IDs supplied by caller; no candidate-source or registry-version identity in orchestrated output.
- **Current alpha status:** `locally_implemented_not_composed`
- **Disposition:** local logic exists; active runtime is guaranteed stand-down
- **Normative view:** 5.7, 5.10
- **Observed code:** src/nvda_desk/services/playbook_eligibility_service.py; src/nvda_desk/cognition/serial/eligibility.py; src/nvda_desk/domain/eligibility/playbook_compilation.py; src/nvda_desk/runtime/orchestrator.py:127-130
- **Current tests:** tests/tier_a/playbook/test_playbook_eligibility_registry_surface.py; tests/tier_b/serial_boundaries/test_playbook_eligibility_decontamination.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Eligibility can be tested in isolation, but the composed serial path never supplies a candidate family and therefore never exercises registry-driven strategy selection.
- **Gate C requirement:** Prove candidate-family origin, registry version and composed selection; preserve stand-down when posture blocks or candidate set is empty.

### B08.3 — Execution expression and lifecycle plan

**Plain-English statement:** Turn eligible playbook families into a bounded candidate expression and review-oriented lifecycle plan, without broker execution.

- **Inputs:** ExecutionExpressionInput and PlaybookEligibilityOutput
- **Interpretation/transformation:** Selects first active family as lead, outputs enter/stand_down scaling token and ready flag; lifecycle plan is stand_down or prepare_candidate_review.
- **Outputs:** ExecutionExpressionOutput and optional lifecycle plan dict
- **Downstream use:** Final risk, capital/opening and review.
- **Time/state dependence:** Stateless; ordering of active families determines lead.
- **Identity/lineage:** No execution candidate ID, policy version or deterministic tie-break authority beyond list order.
- **Current alpha status:** `honest_placeholder`
- **Disposition:** minimal candidate scaffold, not execution strategy
- **Normative view:** 5.7, 5.10-5.11
- **Observed code:** src/nvda_desk/domain/execution/candidate_expression.py:9-21; src/nvda_desk/domain/execution/lifecycle_plan.py:8-12; src/nvda_desk/services/execution_service.py:11-26
- **Current tests:** tests/tier_a/serial_recommendation/test_execution_service_surface.py; test_serial_transform_boundary_surface.py; test_execution_final_join_boundary.py
- **Test assessment:** `partially_aligned`
- **Conformance:** The output is explicitly bounded, but “enter” and lead selection are simplistic and not tied to playbook definitions or candidate identity.
- **Gate C requirement:** Prove deterministic lead-selection authority, candidate identity, no broker/capital authority, and lifecycle extension through contracts.

## B09 — Risk and policy decisions

### B09.1 — Parallel Risk Lane evaluation

**Plain-English statement:** Independently describe fragility, freshness, missing signals, event proximity and environmental risk as context—not as a trading play or capital-sizing decision.

- **Inputs:** StageInputBundle or selected temporal packet; VIX/options/event/freshness/inventory signal material; configured signal inventories/profiles
- **Interpretation/transformation:** Builds bootstrap DMP packet, assesses environment, aggregates families, assembles risk atoms/minute profile and emits descriptive packet; optional candidate semantic enrichment.
- **Outputs:** Parallel Risk lane packet, risk envelope/atoms, minute profile and optional policy observations
- **Downstream use:** Final risk, capital authority, review.
- **Time/state dependence:** Point/minute context with freshness/event windows; some global policy decision state persists per process.
- **Identity/lineage:** Packet lineage partially preserved; signal/profile/config versions not uniformly carried.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** rich local lane, incomplete composition and ownership
- **Normative view:** 5.8
- **Observed code:** src/nvda_desk/services/parallel_risk_lane_service.py; src/nvda_desk/risk/parallel/evaluate.py; src/nvda_desk/domain/parallel_risk/*.py
- **Current tests:** tests/tier_a/parallel_risk/*.py; tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Many local semantics are well tested, but the lane is not composed into one authoritative serial→final-risk→capital run and global mutable decisions violate isolation.
- **Gate C requirement:** Partition tests by normative atom/family semantics, require configuration/version/lineage, prove independence from sizing/playbook authority and replace global state.

### B09.2 — Final risk overlay and terminal join

**Plain-English statement:** Apply a final bounded risk gate after the serial execution expression.

- **Inputs:** ExecutionExpressionOutput
- **Interpretation/transformation:** If no lead playbook, overlay returns stand_down; otherwise continue. Terminal join returns stand_down/confidence 0 or proceed/confidence 1.
- **Outputs:** FinalRiskJoinReceipt
- **Downstream use:** Capital deployment authority.
- **Time/state dependence:** Stateless.
- **Identity/lineage:** No Parallel Risk packet, policy version or receipt/source IDs are consumed by the current helper.
- **Current alpha status:** `honest_placeholder`
- **Disposition:** minimal final gate disconnected from Parallel Risk lane
- **Normative view:** 5.8, 5.11
- **Observed code:** src/nvda_desk/domain/final_risk/overlay.py:8-13; src/nvda_desk/domain/final_risk/terminal_join.py:9-17; src/nvda_desk/services/final_risk_service.py:11-16
- **Current tests:** tests/tier_a/serial_recommendation/test_execution_final_join_boundary.py
- **Test assessment:** `insufficient`
- **Conformance:** The final join does not actually join the Parallel Risk product; it only checks whether a lead playbook exists.
- **Gate C requirement:** Define and prove the actual join contract: required PRL packet identity, hard/caution semantics, precedence, missing-authority failure and receipt lineage.

### B09.3 — Capital deployment authority

**Plain-English statement:** Make the first bounded decision about whether and how much capital may proceed, using explicit serial eligibility, pre-deployment, PRL/final risk, capital state, policy, coefficients and temporal event context.

- **Inputs:** CapitalDeploymentAuthorityInput with IDs, booleans/states, capital amount and requested/max/floor percentages
- **Interpretation/transformation:** Applies deterministic precedence: pre-deployment/risk blocks, serial no-trade, non-positive no-trade, max compression, coefficient floor, PRL caution and elevated event reduction, otherwise continue.
- **Outputs:** CapitalDeploymentDecision and optional receipt with input trace
- **Downstream use:** Opening/placement readiness and review.
- **Time/state dependence:** Point decision based on supplied capital snapshot/event context; no repository mutation.
- **Identity/lineage:** Input trace names major receipt/snapshot/policy IDs; caller may supply all values independently.
- **Current alpha status:** `locally_implemented_not_composed`
- **Disposition:** well-bounded local authority, no end-to-end input construction or state update
- **Normative view:** 5.11
- **Observed code:** src/nvda_desk/capital/authority.py:13-220; src/nvda_desk/services/capital_deployment_service.py:16-40; src/nvda_desk/contracts/capital.py
- **Current tests:** tests/tier_a/capital_deployment/test_sequence9_capital_deployment_decision_surface.py; test_capital_authority_service_surface.py; test_capital_contract_models.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Decision precedence is clear, but no authoritative composer constructs the input from actual upstream owners and no capital-state transaction occurs.
- **Gate C requirement:** Prove owner-sourced input construction, mandatory IDs, precedence, fresh-capital semantics, no serial-confidence sizing and immutable receipt reproduction.

## B10 — Execution or simulated-execution boundaries

### B10.1 — Opening and placement readiness

**Plain-English statement:** Convert a capital decision into a non-executing protocol handoff preview only when authority is complete and positive.

- **Inputs:** CapitalDeploymentDecision, serial_candidate_id, placement constraint IDs, protocol-only broker mode and readiness_id
- **Interpretation/transformation:** Requires capital receipt and candidate ID; blocks unless action CONTINUE and positive percentage/notional; otherwise builds order_intent_preview with execution_allowed false by contract.
- **Outputs:** PlacementReadinessResult and PlacementHandoffMaterial
- **Downstream use:** Paper broker/protocol boundary or review.
- **Time/state dependence:** Stateless.
- **Identity/lineage:** readiness/handoff IDs locally generated from caller IDs; relies on supplied capital receipt.
- **Current alpha status:** `locally_implemented_not_composed`
- **Disposition:** correctly bounded non-executing seam
- **Normative view:** 5.12
- **Observed code:** src/nvda_desk/downstream/opening.py:17-119; src/nvda_desk/domain/downstream/opening.py:13-33
- **Current tests:** tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py; test_opening_authority_boundary_surface.py; test_capital_downstream_placement_boundary.py
- **Test assessment:** `normatively_aligned`
- **Conformance:** Local fail-closed checks are appropriate. The seam is not connected to an authoritative candidate/capital state workflow.
- **Gate C requirement:** Prove missing receipt/candidate fails closed, no broker side effect, handoff identity/constraints, and future broker adapter substitution.

### B10.2 — Paper broker execution lifecycle

**Plain-English statement:** Simulate broker order acknowledgement/fill/cancel/reject events behind a protocol-only boundary without live credentials or broker side effects.

- **Inputs:** BrokerOrderIntent and paper service state
- **Interpretation/transformation:** Creates deterministic paper records/events and maintains in-memory order lifecycle.
- **Outputs:** paper broker execution records/events
- **Downstream use:** Execution record repository, live inventory and review.
- **Time/state dependence:** Process-local lifecycle state.
- **Identity/lineage:** Order/event IDs locally generated or caller supplied; no live broker IDs.
- **Current alpha status:** `honest_placeholder`
- **Disposition:** safe paper boundary, not operational execution
- **Normative view:** 5.12-5.13
- **Observed code:** src/nvda_desk/downstream/broker_execution.py; src/nvda_desk/contracts/broker_execution.py; src/nvda_desk/adapters/egress/broker_protocol.py
- **Current tests:** tests/tier_a/downstream_runtime/test_fwd015_broker_execution_lifecycle_contract.py; tests/tier_a/adapters_egress/test_broker_boundary_surface.py
- **Test assessment:** `normatively_aligned`
- **Conformance:** The current boundary correctly avoids live execution, but persistence/restart and exact integration with opening/inventory are incomplete.
- **Gate C requirement:** Prove protocol-only invariants, lifecycle idempotency, event ordering and adapter replacement without domain change.

### B10.3 — Live position and inventory snapshot

**Plain-English statement:** Read current position and capital state, calculate exposure, optionally normalise fill evidence, and emit a read-only inventory snapshot/receipt without changing serial decisions.

- **Inputs:** position repository, capital repository, optional IDs, execution/fill evidence and receipt ledger
- **Interpretation/transformation:** Reads selected/all positions, reads capital snapshot, builds exposure state, optionally records inventory receipt; orchestrator may attach result read-only.
- **Outputs:** DownstreamLiveInventorySnapshot and InventoryStateReceipt
- **Downstream use:** Exit/close, capital/review and runtime context attachment.
- **Time/state dependence:** Reflects current process-memory repositories; no restart durability.
- **Identity/lineage:** position/capital/inventory/receipt IDs explicit; evidence duplicate checks exist in selected paths.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** useful read model; not authoritative durable live state
- **Normative view:** 5.13, 5.16
- **Observed code:** src/nvda_desk/downstream/live_inventory.py:21-295; src/nvda_desk/domain/downstream/live_inventory.py; src/nvda_desk/runtime/orchestrator.py:243-270
- **Current tests:** tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py; test_live_inventory_authority_boundary_surface.py; test_live_inventory_transform_boundary_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Read-only attachment is correct, but source repositories are process memory and state transitions are not atomically linked to execution receipts.
- **Gate C requirement:** Prove authoritative writer/readers, fill idempotency, restart persistence when admitted, and that inventory cannot alter serial outputs except through an explicit later contract.

## B11 — Exit and close behaviour

### B11.1 — Exit and close policy decision

**Plain-English statement:** Evaluate whether an existing position should be held, trimmed or closed, then produce a non-executing handoff and replayable receipt.

- **Inputs:** ExitClosePolicyInput with position, inventory, risk/event/market state, requested action and lineage trace
- **Interpretation/transformation:** Applies bounded policy rules, builds decision, close handoff and receipt; replay currently returns a deterministic summary string from receipt fields.
- **Outputs:** ExitClosePolicyDecision, CloseHandoffMaterial, ExitCloseReceipt
- **Downstream use:** Overnight carry, paper broker protocol and review.
- **Time/state dependence:** Point decision; depends on supplied live state but does not own it.
- **Identity/lineage:** decision/position/receipt IDs explicit; API may manufacture missing upstream IDs in its composition path.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** active provisional seam; not operational or fully lineage-safe
- **Normative view:** 5.14
- **Observed code:** src/nvda_desk/downstream/exit_close.py:15-155; src/nvda_desk/contracts/exit_close.py; src/nvda_desk/services/exit_close_service.py
- **Current tests:** tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py; test_exit_close_transform_boundary_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Local policy and non-execution boundary exist, but authoritative input construction, durable state and fail-closed lineage are incomplete.
- **Gate C requirement:** Prove all required input IDs originate upstream, missing authority fails closed, policy version is carried and handoff cannot execute directly.

### B11.2 — Overnight carry evaluation and replay

**Plain-English statement:** Translate an exit/close decision into allowed overnight actions, evaluate market context within that ceiling, and compare the next session path without execution.

- **Inputs:** ExitClosePolicyDecision, horizon/lifecycle ceiling, market_state with close/VWAP/VIX, next-session reference
- **Interpretation/transformation:** Caps allowed actions from source exit state; recommends trim at >=4% above VWAP and close at VIX>=30, then caps by handoff; replay calculates open-gap and close-to-close percentages.
- **Outputs:** CarryHandoffPacket, OvernightCarryEvaluation, OvernightCarryReplayResult
- **Downstream use:** Review/reporting.
- **Time/state dependence:** Cross-session; recorded evaluations are process memory.
- **Identity/lineage:** handoff/evaluation/replay IDs explicit; next-session source identity absent.
- **Current alpha status:** `locally_implemented_not_composed`
- **Disposition:** bounded alpha analysis seam, not part of one live lifecycle
- **Normative view:** 5.14-5.15
- **Observed code:** src/nvda_desk/downstream/overnight_carry.py:14-203
- **Current tests:** tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py
- **Test assessment:** `partially_aligned`
- **Conformance:** No execution authority is correctly enforced; thresholds and replay source lineage/version are not normatively grounded end-to-end.
- **Gate C requirement:** Prove action ceiling, no execution, threshold policy version, next-session source identity and deterministic replay.

## B12 — Outputs, receipts, reporting and replay

### B12.1 — Daily P&L reporting

**Plain-English statement:** Record and retrieve daily P&L reports for review.

- **Inputs:** DailyPnlReport
- **Interpretation/transformation:** Stores unique report IDs in memory and supports list/find by symbol/date.
- **Outputs:** DailyPnlReportCollection or selected report
- **Downstream use:** ReviewPacketService and API.
- **Time/state dependence:** Daily report state survives only in process.
- **Identity/lineage:** report_id required; no execution-event reconciliation or durable source trace.
- **Current alpha status:** `honest_placeholder`
- **Disposition:** simple report store, not accounting authority
- **Normative view:** 5.15-5.16
- **Observed code:** src/nvda_desk/downstream/daily_pnl.py:8-26; src/nvda_desk/contracts/daily_pnl.py
- **Current tests:** tests/tier_a/downstream_runtime/test_fwd016_daily_pnl_reporting_contract.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Local uniqueness/read behaviour exists, but report correctness against positions/fills/capital and restart durability are unproved.
- **Gate C requirement:** Prove report derivation/reconciliation, source event IDs, duplicate/idempotent behaviour and explicit non-authoritative alpha status.

### B12.2 — Daily review packet assembly

**Plain-English statement:** Assemble review-safe execution, P&L and module-health material while redacting redirect/authority keys.

- **Inputs:** execution records, daily P&L service, module health and review payloads
- **Interpretation/transformation:** Reads records/reports, deep-copies and recursively redacts selected keys, records missing material and builds review packet.
- **Outputs:** DailyReviewPacket and review-safe rendering
- **Downstream use:** API/reviewer.
- **Time/state dependence:** Reflects process-local stores at assembly time.
- **Identity/lineage:** Review packet IDs plus underlying record/report IDs; complete source packet lineage depends on supplied material.
- **Current alpha status:** `partially_implements_intent`
- **Disposition:** useful review projection; evidence completeness not guaranteed
- **Normative view:** 5.15
- **Observed code:** src/nvda_desk/review/packet_service.py:24-175
- **Current tests:** tests/tier_a/review_runtime/test_review_stage_surface.py; test_review_transform_boundary_surface.py; test_fwd018_review_packet_and_slv_replay_contract.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Review redaction and missing-material reporting are useful, but the underlying evidence is not durably preserved or transactionally complete.
- **Gate C requirement:** Prove redaction, explicit missing-material flags, packet/source lineage and no mutation/promotion of runtime authority.

### B12.3 — Review explanation

**Plain-English statement:** Explain a review packet by combining summary, resolved policy/coefficient surfaces and packet lineage without inventing missing evidence.

- **Inputs:** ReviewPacket, EffectivePolicySnapshot, ReviewLineagePacket, PacketLineageSurface
- **Interpretation/transformation:** Chooses resolved surfaces/coefficients, reports missing summary/surfaces/packet IDs, computes lineage_complete and deterministic text.
- **Outputs:** explanation dict with missing_review_material
- **Downstream use:** Review UI/API.
- **Time/state dependence:** Stateless.
- **Identity/lineage:** Uses supplied packet/source packet IDs; does not validate their origin.
- **Current alpha status:** `operates_consistently_with_intent`
- **Disposition:** aligned local explanation seam
- **Normative view:** 5.15
- **Observed code:** src/nvda_desk/services/review_explanation_service.py:13-55
- **Current tests:** tests/tier_a/review_runtime/test_review_explanation_service_surface.py; tests/tier_b/review_lineage/test_review_effective_policy_lineage.py
- **Test assessment:** `normatively_aligned`
- **Conformance:** The service truthfully exposes missing evidence and avoids generating lineage. Its completeness claim is only as strong as supplied inputs.
- **Gate C requirement:** Preserve negative/missing-material tests and add origin validation at the upstream packet-lineage owner, not inside explanation text.

### B12.4 — Replay comparison

**Plain-English statement:** Compare two bounded output mappings or review decisions without promoting replay results into runtime authority.

- **Inputs:** baseline/candidate mappings or imported-module citations/decisions
- **Interpretation/transformation:** Deep-copies mappings, lists differing/missing fields; citation replay checks missing decisions and emits promoted_to_runtime false.
- **Outputs:** ReplayComparisonResult or ReviewReplayComparisonResult
- **Downstream use:** Analysis/review.
- **Time/state dependence:** Stateless comparison; no original input retrieval.
- **Identity/lineage:** Packet IDs may be supplied to a lineage object; replay run ID optional.
- **Current alpha status:** `honest_placeholder`
- **Disposition:** comparison utility, not end-to-end replay
- **Normative view:** 5.15-5.16
- **Observed code:** src/nvda_desk/analysis/replay/service.py:15-88; src/nvda_desk/replay/review_compare.py:15-35
- **Current tests:** tests/tier_a/analysis/test_replay_evaluation_surface.py; tests/tier_b/review_replay/test_tranche_a_review_replay.py; tests/tier_b/review_lineage/test_review_replay_dmp_v3_lineage.py
- **Test assessment:** `partially_aligned`
- **Conformance:** It can compare supplied snapshots, but cannot reconstruct the original governed decision from durable inputs/config/state/output.
- **Gate C requirement:** Define the minimum replay envelope, then test reconstruction from retained authoritative artefacts; retain comparison utility as a subordinate tool.

### B12.5 — Walk-forward and strategic-ladder analysis

**Plain-English statement:** Rank or compare candidate stacks over supplied market rows for research/review only.

- **Inputs:** rows with candidate/stack IDs, scores and baseline scores; optional windows/scenarios
- **Interpretation/transformation:** Builds comparison summaries, ranks by score, supports simple walk-forward/fragility/batch wrappers and failure/bucket summaries.
- **Outputs:** ComparisonReport and analysis summaries
- **Downstream use:** Research/review API and experiment logs.
- **Time/state dependence:** Depends on supplied row order/windows; sidecar records are process memory.
- **Identity/lineage:** report_id and stack IDs supplied; dataset/source/version lineage not enforced.
- **Current alpha status:** `honest_placeholder`
- **Disposition:** analysis-only utility, not live trader cognition
- **Normative view:** 5.15
- **Observed code:** src/nvda_desk/analysis/replay/walk_forward.py; src/nvda_desk/upstream/strategic_ladder.py
- **Current tests:** tests/tier_a/analysis/test_fwd002_replay_harness_contract.py; tests/tier_b/review_lineage/test_bounded_trace_review_determinism.py
- **Test assessment:** `partially_aligned`
- **Conformance:** The analysis path is bounded from runtime, but its name and wrappers exceed the simple current score comparison.
- **Gate C requirement:** Prove analysis-only boundary, dataset/window identity, deterministic ranking and no runtime promotion.

### B12.6 — API and egress composition

**Plain-English statement:** Expose bounded runtime, configuration, calendar, risk, paper execution, review and analysis functions through one application shell.

- **Inputs:** method-specific mappings/DTOs and dependency singletons
- **Interpretation/transformation:** Constructs DTOs, delegates to services, and also stores some event lists and maps identifiers inside the API class.
- **Outputs:** plain dict/list API responses
- **Downstream use:** External clients/test harnesses.
- **Time/state dependence:** Many dependencies and lists are cached/process-local.
- **Identity/lineage:** Some endpoints accept caller IDs; some composition paths create fallback IDs; private repository representation is read directly in one path.
- **Current alpha status:** `behaves_differently_from_intent`
- **Disposition:** over-broad composition root with domain mapping/state leakage
- **Normative view:** 5.1, 5.15; modularity law in docs/11.1
- **Observed code:** src/nvda_desk/api/app.py:51-471; src/nvda_desk/api/deps.py:1-180; src/nvda_desk/adapters/egress/api_dto_adapter.py
- **Current tests:** tests/tier_a/api/test_api_boundary_surface.py; test_fwd005_api_exposure_contract.py; tests/tier_a/adapters_egress/test_broker_boundary_surface.py
- **Test assessment:** `partially_aligned`
- **Conformance:** Delegation exists, but one class owns unrelated API mapping, process state, fallback identity and private-repository access, so change impact is broad.
- **Gate C requirement:** Split tests by explicit application services/composition ports; prove API cannot invent domain authority or depend on private repository storage.

