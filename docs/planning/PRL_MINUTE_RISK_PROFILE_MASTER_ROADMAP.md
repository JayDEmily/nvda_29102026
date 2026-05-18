# Parallel Risk Lane minute-level risk profile master roadmap

Status: `planning_complete`
Branch: `work/prl-minute-risk-profile-master-roadmap`
Baseline commit: `7eb107f6527ef5dc37e584a88deecd4a5390d1e5`

This document is a planning/control artefact only. It does not implement PRL-MRP-003 or any later behaviour.

## 1. Accepted baseline

Accepted baseline from the completed contract branch:

- PRL-MRP-001 is completed: contract-only schema classes/enums for minute-profile material were added.
- PRL-MRP-002 is completed: `AuthorityFlags` defaults deny candidate, playbook, capital, broker execution, serial mutation, review judgement, and direct workbook runtime reads.
- The current Parallel Risk Lane remains a bounded independent risk-envelope seam.
- The roadmap must enrich environmental risk description without turning the lane into candidate formation, play selection, capital allocation, broker execution, serial mutation, review judgement, or a runtime workbook reader.

Evidence basis:

- Parallel risk lane is independent and does not form the candidate or allocate capital: `docs/01_NORMATIVE_CORE.md:73-79`.
- Runtime ownership says the independent lane answers what it concluded about the present environment and is not candidate formation: `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:108-118`.
- Workbook direct runtime reads are forbidden: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:30-34`.
- Durable terms require vocabulary governance: `docs/01_NORMATIVE_CORE.md:117`, `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md:11-25`.
- Prior implementation plan identifies PRL-MRP-003 as the next leaf but this roadmap does not execute it: `docs/planning/PRL_MINUTE_RISK_PROFILE_IMPLEMENTATION_PLAN.md:135-143`.

## 2. Governance surface map

| File | Governance role | Constraint imposed on PRL roadmap | Applies to which leaves | Evidence |
|---|---|---|---|---|
| `AGENTS.md` | Root worker operating harness | Requires full reading before mutation; forbids replacing reading with grep/summary; restricts mutation to opened boundary | All leaves | `AGENTS.md:85-100`, `AGENTS.md:147` |
| `PLANS.md` | Frozen standing plan | Treat current execution state as ledger-owned; do not mutate PLANS for routine progress | All leaves | `PLANS.md:1-17`, `PLANS.md:27-38` |
| `ROADMAP_LEDGER.md` | Mutable live execution ledger | Every future leaf must record branch, status, scope, evidence, tests, and closeout | All leaves | Current roadmap section `ROADMAP_LEDGER.md` |
| `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md` | Routes numbered control surfaces | Vocabulary, testing, runtime ownership, architecture, and process docs must be read by routed scope | All leaves | `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md:15-84` |
| `docs/01_NORMATIVE_CORE.md` | Top-level authority and runtime boundaries | PRL is independent, not serial stage, not candidate formation, not capital allocation | All PRL leaves | `docs/01_NORMATIVE_CORE.md:73-79` |
| `docs/03_DOMAIN_MODEL_CORE.md` | Domain-part definitions | PRL assesses present environment while serial spine forms candidate; separation must be preserved | All PRL leaves | `docs/03_DOMAIN_MODEL_CORE.md:64-72` |
| `docs/04_TECHNICAL_ARCHITECTURE_CORE.md` | Technical architecture | Parallel risk runtime path evaluates environment in parallel and does not form candidate | Contract/domain/service leaves | `docs/04_TECHNICAL_ARCHITECTURE_CORE.md:95-103` |
| `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md` | Source temporal working law | Source observation time, capture time, persistence time, and field-level provenance must stay distinct | PRL-MRP-003, PRL-MRP-021 | `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:20-37` |
| `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md` | Process/document-touch law | Only opened surfaces are editable; if a new file is needed, stop and reopen scope | All leaves | `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md:48-75` |
| `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md` | Output ownership | PRL output describes the independent environmental assessment and is not candidate formation | PRL-MRP-014 onward | `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:108-118` |
| `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` | Working ownership overlays | Prevents capital/order/position/broker leakage into adjacent surfaces; calendar/coefficient packets may be consumed by PRL through lawful carriers | Calendar, coefficient, service leaves | `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:36-39`, `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:78-85` |
| `docs/08_TESTING_AND_PROMOTION_CORE.md` | Test/proof law | Tests must protect real invariants; proof artefacts must not become vocabulary drift | All test leaves | `docs/08_TESTING_AND_PROMOTION_CORE.md:13`, `docs/08_TESTING_AND_PROMOTION_CORE.md:133-150` |
| `tests/AGENTS.override.md` | Test subtree override | Test work must read test governance and protect invariants, not greenness alone | Any leaf touching `tests/` | `tests/AGENTS.override.md` read in manifest |
| `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` | Vocabulary governance | Durable terms in docs/schemas/manifests/code need governance or same-gate vocabulary update | PRL-MRP-023 to PRL-MRP-025 and any new public terms | `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md:11-25` |
| `docs/vocabulary/README.md` | Vocabulary system index | Points to workflow, canonical vocabulary file, schema, generator | Vocabulary leaves | `docs/vocabulary/README.md:18-23` |
| `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` | Vocabulary workflow | Candidate vocabulary is feeder-only; admission requires reconciliation | Vocabulary leaves | `docs/vocabulary/CONSOLIDATION_WORKFLOW.md:3-22` |
| `docs/vocabulary/vocabulary_registry.md` | Human-readable registry | `Parallel Risk Lane` is governed; new durable terms must be admitted or avoided | All leaves using durable terms | `docs/vocabulary/vocabulary_registry.md:161-163` |
| `data/vocabulary/canonical_vocabulary.json` | Canonical vocabulary data | Deterministic description must reference vocabulary data, not free-form wording | Description leaves | Full read manifest entry |
| `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md` | Workbook reference authority | Governed workbook is reference ledger only; runtime reads forbidden; promotion must go through typed config/contracts | Workbook/signal leaves | `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:3-34`, `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:53-86` |
| `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` | Native architecture placement | Contracts carry data, services orchestrate, boundaries need seam contracts, reserved decisions must not be implemented as locked | All implementation leaves | `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:490-537`, `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:626-674` |

Plain-English deterministic description rule for the roadmap:

- Future description output must be deterministic, template/vocabulary-reference based, and not free-form generative commentary.
- No description leaf may emit trade advice, play selection, capital sizing, or review-layer judgement.
- Description leaves must locate and obey vocabulary-governance files before implementation.

## 3. Existing test surface map

| Test file | Behaviour protected | Current relevance to PRL roadmap | Future leaves it should guard | Needs new tests? |
|---|---|---|---|---|
| `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py` | Minute profile contract construction, authority flags, metadata-only refs | Completed PRL-MRP-001/002 baseline | All enriched-profile leaves | Extend as fields/serialization evolve |
| `tests/tier_a/parallel_risk/test_parallel_risk_contract_models.py` | Existing PRL contract model behaviour | Prevents contract regression | PRL-MRP-014 onward | Preserve unchanged unless contract additive changes need updates |
| `tests/tier_a/parallel_risk/test_parallel_risk_evaluation_surface.py` | PRL evaluation and forbidden authority-key rejection | Protects no hidden authority expansion | PRL-MRP-009 to PRL-MRP-022 | Extend with enriched profile path after integration |
| `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py` | Service-level PRL lane surface | Guards backward-compatible service integration | PRL-MRP-019 | Extend when service emits optional minute profile |
| `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_input_surface.py` | Input boundary for existing envelope | Guards current input semantics | PRL-MRP-010 to PRL-MRP-014 | Preserve and extend only for typed calendar/signal inputs |
| `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_output_surface.py` | Envelope output state/caution/block behaviour | Guards current scheduled-event/VIX/DTE behaviours | PRL-MRP-010 to PRL-MRP-014 | Extend with atom preservation assertions |
| `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py` | PRL specimen expectations | Guards specimen shape | PRL-MRP-014 onward | Extend after enriched specimen is intentionally added |
| `tests/tier_a/parallel_risk/test_fwd013_parallel_risk_candidate_enrichment_contract.py` | Candidate fragility remains descriptive | Prevents PRL crossing into candidate action | PRL-MRP-018, PRL-MRP-022 | Preserve; add no-play assertions if needed |
| `tests/tier_a/parallel_risk/test_parallel_risk_packet_builder_surface.py` | Packet builder surface | Protects packet assembly compatibility | PRL-MRP-018 | Extend when minute profile assembly is added |
| `tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py` | PRL transform boundary | Prevents donor/forbidden imports and authority leakage | All implementation leaves | Preserve; add new module paths if introduced |
| `tests/tier_a/parallel_risk/test_parallel_risk_dmp_fixture_root.py` | DMP fixture root | Protects fixture-root assumptions | PRL-MRP-018 onward | Extend only if new fixtures are introduced |
| `tests/tier_a/upstream_signal/test_fwd007_raw_signal_family_rebuild_contract.py` | Raw signal family contract/admission examples | Relevant to expected signal inventory and missing/unavailable signals | PRL-MRP-004 to PRL-MRP-009, PRL-MRP-020 | New PRL tests should consume outputs, not raw internals |
| `tests/tier_a/upstream_signal/test_raw_signal_contract_copy_boundaries.py` | Copy boundaries for raw signal contracts | Prevents shared mutable signal state | PRL-MRP-004, PRL-MRP-020 | Preserve |
| `tests/tier_a/upstream_signal/test_raw_signal_transform_boundary_surface.py` | Raw signal transform boundaries | Prevents authority leakage in raw signal ingress | PRL-MRP-005, PRL-MRP-020 | Preserve and cite in hidden-read tests |
| `tests/tier_a/upstream_signal/test_upstream_non_interference_and_sanity_traces.py` | Upstream non-interference/traces | Guards PRL from source-ingress authority | PRL-MRP-004 to PRL-MRP-020 | Preserve |
| `tests/tier_a/upstream_signal/test_upstream_signal_coverage_map_and_scope_lock.py` | Coverage map and scope lock | Relevant to expected signal inventory | PRL-MRP-004 to PRL-MRP-009 | Extend with promoted inventory references later |
| `tests/tier_a/upstream_cognition/test_cognition_ingress_mapping_surfaces.py` | Prepared context mapping | Guards lawful stage-input mapping | PRL-MRP-008 to PRL-MRP-019 | Preserve |
| `tests/tier_a/upstream_cognition/test_cognition_ingress_translation_coordinator.py` | Translation coordinator | Ensures prepared ingress boundaries | PRL-MRP-008 to PRL-MRP-019 | Preserve |
| `tests/tier_a/upstream_cognition/test_prepared_context_packet_surface.py` | Prepared context packet | Relevant to lineage and prepared inputs | PRL-MRP-021 | Preserve |
| `tests/tier_a/upstream_cognition/test_prepared_runtime_snapshot_contract_surface.py` | Prepared runtime snapshot | Relevant to source temporal and derived fields | PRL-MRP-003 to PRL-MRP-021 | Preserve |
| `tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py` | Runtime substrate | Relevant to signal snapshot lineage | PRL-MRP-004, PRL-MRP-020 | Preserve |
| `tests/tier_a/upstream_cognition/test_prepared_runtime_transform_boundary_surface.py` | Prepared runtime transform boundary | Prevents upstream internals/authority leakage | PRL-MRP-018 to PRL-MRP-022 | Preserve |
| `tests/tier_a/upstream_cognition/test_regime_contract_models.py` | Regime contract models | VIX/NVDA/NQ input safety | PRL-MRP-012, PRL-MRP-013 | Preserve |
| `tests/tier_a/upstream_cognition/test_regime_ingress_surface.py` | Regime ingress | Relevant to macro/regime signal source | PRL-MRP-012, PRL-MRP-013 | Preserve |
| `tests/tier_a/temporal/test_source_temporal_standard_surface.py` | Source temporal standard | Foundation for freshness; prevents timestamp substitution | PRL-MRP-003, PRL-MRP-021 | New freshness tests required |
| `tests/tier_a/temporal/test_raw_capture_transform_boundary_surface.py` | Raw capture transform boundary | Prevents source temporal drift | PRL-MRP-003 | Preserve |
| `tests/tier_a/financial_calendar/test_fwd008_runtime_calendar_query_contract.py` | Runtime calendar query, proximity, materiality, no trade authority | Direct basis for event proximity | PRL-MRP-008 to PRL-MRP-011 | New PRL event-proximity tests required |
| `tests/tier_a/financial_calendar/test_financial_calendar_authority_surface.py` | Calendar reference/projection authority | Prevents calendar becoming runtime trading authority | PRL-MRP-008 to PRL-MRP-011 | Preserve |
| `tests/tier_a/financial_calendar/test_financial_calendar_transform_boundary_surface.py` | Calendar transform boundaries | Prevents calendar importing PRL/runtime owners wrongly | PRL-MRP-008 to PRL-MRP-011 | Preserve |
| `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py` | Workbook specimen surface | Relevant to workbook reference/provenance | PRL-MRP-006 to PRL-MRP-009 | Preserve; add workbook inventory tests only when workbook scope opens |
| `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_emission_surface.py` | Workbook specimen emission | Guards workbook-derived specimen output | PRL-MRP-006 to PRL-MRP-009 | Preserve |
| `tests/tier_a/testing_harnesses/test_serial_runtime_parallel_risk_boundary_specimen_surface.py` | Serial/parallel boundary specimen | Guards non-collapse of serial and PRL | PRL-MRP-019, PRL-MRP-022 | Preserve/extend after service integration |
| `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py` | Canonical runtime specimen | Relevant to future fixture updates | PRL-MRP-018 onward | Preserve |
| `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py` | Fixture/sidecar contract | Relevant if new specimens are added | PRL-MRP-018 onward | Preserve |
| `tests/tier_a/vocabulary/test_parallel_risk_lane_vocabulary_terms.py` | PRL vocabulary terms | Guards governed PRL term usage | PRL-MRP-023 to PRL-MRP-025 | Extend if new durable PRL terms are admitted |
| `tests/tier_a/vocabulary/test_vocabulary_workflow_surface.py` | Vocabulary workflow doc presence and contents | Guards vocabulary process | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py` | Baseline vocabulary terms | Guards required canonical terms | PRL-MRP-023 to PRL-MRP-025 | Extend only with lawful vocabulary updates |
| `tests/tier_a/vocabulary/test_vocabulary_schema_contract.py` | Vocabulary schema contract | Guards canonical vocabulary shape | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py` | Canonical builder parity | Guards vocabulary regeneration | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py` | Vocabulary JSON helpers | Guards helper behaviour | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py` | Vocabulary document JSON helpers | Guards vocabulary docs/data helper shape | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/vocabulary/test_vocabulary_candidate_*` | Candidate admission/review/classification payload tests | Guards vocabulary candidate workflow | PRL-MRP-023 to PRL-MRP-025 | Preserve; use if new terms are proposed |
| `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py` | Synonym-candidate audit | Prevents uncontrolled language drift | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/vocabulary/test_dmp_v3_vocabulary_terms.py` | DMP vocabulary terms | Guards packet vocabulary | PRL-MRP-018 to PRL-MRP-025 | Preserve |
| `tests/tier_a/vocabulary/test_financial_calendar_vocabulary_terms.py` | Calendar vocabulary terms | Relevant to event-proximity language | PRL-MRP-008 to PRL-MRP-011 | Preserve |
| `tests/tier_a/review_runtime/test_review_explanation_service_surface.py` | Review/explanation service boundary | Prevents PRL description becoming review judgement | PRL-MRP-023 to PRL-MRP-025 | Preserve and add PRL-specific no-review-authority tests |
| `tests/tier_a/review_runtime/test_review_contract_authority_boundaries.py` | Review authority boundary | Guards no review-authority leakage | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/review_runtime/test_review_contract_models.py` | Review contract models | Reference for explanation surfaces only | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/review_runtime/test_review_stage_surface.py` | Review stage surface | Prevents runtime review crossing | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/review_runtime/test_review_transform_boundary_surface.py` | Review transform boundary | Prevents PRL importing review authority wrongly | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/review_runtime/test_review_repository_surface.py` | Review repository | Prevents persistence/authority confusion | PRL-MRP-023 to PRL-MRP-025 | Preserve |
| `tests/tier_a/review_runtime/test_fwd018_review_packet_and_slv_replay_contract.py` | Review packet/replay contract | Relevant to not becoming review layer | PRL-MRP-023 to PRL-MRP-025 | Preserve |

New test files required by roadmap:

- `tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_event_proximity_register.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_supported_risk_atoms.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_family_aggregation.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_enriched_packet_assembly.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_unavailable_signal_handling.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_description_contract.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_description_templates.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_workbook_runtime_boundary.py`

## 4. Dependency graph

### 4A. Dependency layers

1. Governance / planning / ledger control.
2. Contract and model safety.
3. Expected signal inventory workbook governance.
4. Runtime expected-signal promotion boundary.
5. Freshness and missing-signal foundations.
6. Temporal/session and calendar/event enrichment.
7. Current supported risk atom skeleton.
8. Risk-family aggregation.
9. Enriched packet assembly.
10. Backward-compatible service integration.
11. Deterministic vocabulary-governed description.
12. Documentation/current-state updates.
13. Deferred rich signal families.

### 4B. Dependency table

| Dependency | Must precede | Why | Evidence |
|---|---|---|---|
| Full-read governance and ledger entry | Any future leaf | Repo requires read-before-mutate and mutable ledger truth | `AGENTS.md:85-100`; `ROADMAP_LEDGER.md` |
| PRL-MRP-001/002 contracts | Freshness/missing/event/atom leaves | Later leaves need profile/register/atom/authority carrier types | Completed branch and `docs/planning/PRL_MINUTE_RISK_PROFILE_IMPLEMENTATION_PLAN.md:133-134` |
| Workbook inventory planning | Missing/unavailable expected-signal checks | Expected signals must be governed in workbook, not code constants | user decision; `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:30-34` |
| Workbook tab creation | Typed promotion from workbook tab | Promotion needs actual governed tab source | user decision; workbook authority doc |
| Typed promotion | Runtime missing/unavailable checks using inventory | Runtime may not read workbook directly | `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:30-34` |
| Freshness scoring | Missing/quarantined confidence impact and profile confidence | Stale/missing distinction needs temporal truth first | `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:20-37` |
| Missing/quarantined register | Unavailable signal handling | Missing/unavailable/hallucination prevention depends on register shape | prior plan PRL-MRP-004 |
| Event proximity register | Scheduled-event caution atom | Current event caution should be preserved and enriched through typed event proximity | calendar tests and prior plan |
| VIX threshold preservation | VIX reconciliation | Do not silently change current macro risk behaviour | prior plan PRL-MRP-011 |
| Options DTE preservation | Options atom skeleton | Current DTE risk must remain stable before atoms wrap it | prior plan PRL-MRP-006 |
| Atom skeleton | Family aggregation | Families aggregate atom states; no atom means no deterministic aggregation | schema design |
| Family aggregation | Enriched packet assembly | Profile needs family states before assembly | schema design |
| Packet assembly | Service integration | Service should consume assembled profile rather than reimplementing assembly | architecture seam law |
| Vocabulary constraints | Description contract and engine | Plain-English output must be deterministic and vocabulary-governed | user decision; `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md:11-25` |
| Description contract/tests | Description engine | No free-form prose or trade advice without tests first | test-first law |
| Rich signal source contracts | VWAP/spread/depth/gamma/headline/crowding/cognitive atoms | PRL must not hallucinate unavailable signals | user requirement; workbook/runtime-boundary law |

## 5. Master implementation roadmap

| Leaf ID | Title | Status | Objective | Allowed files | Forbidden scope | Inputs / prerequisites | Tests to add/update | Acceptance criterion | Artefacts | Depends on |
|---|---|---|---|---|---|---|---|---|---|---|
| PRL-MRP-001 | Contract schema additions | completed | Add minute-profile contract classes/enums | Already changed on prior branch | No calculations/services | Accepted contracts branch | Existing contract tests | New models construct/serialise | prior branch artefacts | none |
| PRL-MRP-002 | AuthorityFlags default-deny | completed | Add default false authority flags | Already changed on prior branch | No behaviour integration | PRL-MRP-001 | Authority flag tests | Candidate/playbook/capital/order/review/workbook flags false | prior branch artefacts | PRL-MRP-001 |
| PRL-MRP-003 | Freshness register calculation | planned_not_started | Add deterministic freshness states from source/capture/persist/generated times | new domain module; tests; maybe contract helpers | No missing-signal/event/service work | PRL-MRP-001/002; source temporal law | `test_parallel_risk_freshness_register.py` | fresh/stale/unknown classified without timestamp substitution | command log, patch | PRL-MRP-001/002 |
| PRL-MRP-004 | Expected signal availability test scaffold | planned_not_started | Define tests for expected-signal references as metadata-only until workbook promotion exists | tests only; maybe planning doc | No workbook edit; no runtime config | PRL-MRP-001/002; workbook decision | expected inventory metadata tests | Tests prove no runtime workbook read and no code constants as authority | test log | PRL-MRP-001/002 |
| PRL-MRP-005 | Missing/quarantined signal register | planned_not_started | Convert existing missing_fields/quarantine metadata into register entries and confidence impacts | new domain module; tests | No workbook inventory consumption yet except metadata | PRL-MRP-003/004 | `test_parallel_risk_missing_signal_register.py` | missing/quarantined signals reduce confidence or disable atoms without invented values | proof log | PRL-MRP-003/004 |
| PRL-MRP-006 | Workbook signal-inventory tab planning | planned_not_started | Write workbook-tab specification for `Parallel Risk Lane Signal Inventory` | docs/planning; ROADMAP_LEDGER | No Excel edit | accepted user decision; workbook authority | no runtime tests | Workbook tab columns, lineage, classifications, and promotion boundary specified | planning patch | PRL-MRP-004 |
| PRL-MRP-007 | Workbook signal-inventory tab creation | blocked_pending_source | Add the governed Excel tab only after explicit workbook-edit authorisation | workbook + paired receipts/docs if opened | No runtime read; no code constants | PRL-MRP-006 and explicit user authorisation | workbook surface tests if available | New tab exists with lineage to raw/derived tabs | workbook diff/manifest | PRL-MRP-006 |
| PRL-MRP-008 | Typed promotion plan from workbook inventory | planned_not_started | Plan/import typed config/contract promotion from workbook tab into runtime-owned config | docs/planning; maybe future config schema tests | No runtime workbook read | PRL-MRP-006/007 | promotion boundary tests | Runtime contract/config path specified without direct workbook reads | planning artefact | PRL-MRP-006 |
| PRL-MRP-009 | Runtime expected-signal inventory promotion | blocked_pending_source | Implement typed promoted inventory consumption after workbook tab exists | config/contracts/tests/domain | No workbook read; no rich signals without source | PRL-MRP-007/008 | workbook runtime-boundary tests | PRL consumes typed promoted inventory only | proof log | PRL-MRP-007/008 |
| PRL-MRP-010 | Event proximity register | planned_not_started | Add typed event proximity/materiality register from calendar snapshot or temporal windows | domain module; tests; maybe stage input contract | No trade permission; no service integration | calendar query tests; PRL contracts | `test_parallel_risk_event_proximity_register.py` | proximity/materiality descriptive only; lineage preserved | proof log | PRL-MRP-003 |
| PRL-MRP-011 | Scheduled-event caution preservation | planned_not_started | Preserve existing `scheduled_event_window_active` caution while wrapping it as atom/contribution | domain tests; possibly environment assessment adapter | No new calendar behaviour beyond current rule | current PRL envelope tests | extend envelope output tests | Existing event caution behaviour unchanged | proof log | PRL-MRP-010 |
| PRL-MRP-012 | VIX threshold preservation | planned_not_started | Preserve current VIX caution/block behaviour before reconciliation | tests/domain adapter | No threshold migration | current PRL evaluator tests | regression tests | VIX >=30 caution and >=50 block remain unless future leaf changes | proof log | PRL-MRP-003 |
| PRL-MRP-013 | VIX governed threshold reconciliation | planned_not_started | Reconcile hardcoded PRL thresholds with coefficient authority through explicit migration decision | config adapter/tests/docs if authorised | No silent behaviour drift | PRL-MRP-012; coefficient authority | threshold reconciliation tests | Current behaviour preserved or migrated with explicit evidence | proof log | PRL-MRP-012 |
| PRL-MRP-014 | Options DTE risk preservation | planned_not_started | Preserve current `front_dte > next_dte` caution and represent as risk atom later | domain tests | No real options surface/gamma/skew | options-flow contract tests | DTE inversion behaviour unchanged | proof log | PRL-MRP-003 |
| PRL-MRP-015 | Supported risk atom skeleton | planned_not_started | Emit atoms for supported current risks: source freshness, missing/data-quality, scheduled event, VIX, DTE | domain module/tests | No rich unavailable signals as active values | PRL-MRP-003/005/011/012/014 | `test_parallel_risk_supported_risk_atoms.py` | atoms observe/caution/block without trade-action fields | proof log | PRL-MRP-003/005/011/012/014 |
| PRL-MRP-016 | Risk atom no-play authority tests | planned_not_started | Harden tests against atom fields implying trade recommendation/action | tests | No production change unless tests expose issue | PRL-MRP-015 | authority/no-play tests | atom/profile schema contains risk descriptions only | proof log | PRL-MRP-015 |
| PRL-MRP-017 | Risk-family aggregation | planned_not_started | Aggregate atom states into deterministic family states | domain module/tests | No capital/play permission semantics | PRL-MRP-015 | `test_parallel_risk_family_aggregation.py` | family states reflect atom severity/confidence only | proof log | PRL-MRP-015 |
| PRL-MRP-018 | Enriched packet assembly | planned_not_started | Assemble `ParallelRiskMinuteProfile` from supported registers/atoms/families | domain/evaluate adapter/tests | No service API changes yet | PRL-MRP-003/005/010/015/017 | `test_parallel_risk_enriched_packet_assembly.py` | profile assembled with lineage and authority flags; existing packet stable | proof log | PRL-MRP-017 |
| PRL-MRP-019 | Backward-compatible service integration | planned_not_started | Add optional service path/flag to return enriched minute profile | service/tests | No mandatory downstream consumer changes | PRL-MRP-018 | service surface tests | existing service calls still pass; optional profile path works | proof log | PRL-MRP-018 |
| PRL-MRP-020 | Unavailable signal handling | planned_not_started | Mark unavailable Bloomberg-style signals missing/unavailable, not valued | domain/tests/config if inventory promoted | No fabricated VWAP/spread/gamma/headline values | PRL-MRP-005/009 | `test_parallel_risk_unavailable_signal_handling.py` | unavailable signals are visible and non-hallucinated | proof log | PRL-MRP-005, PRL-MRP-009 if inventory-backed |
| PRL-MRP-021 | Lineage completeness | planned_not_started | Ensure profile/signal/atom/family lineage references are complete enough for audit | domain/tests | No hidden upstream reads | PRL-MRP-018/019 | `test_parallel_risk_lineage_completeness.py` | source refs, packet ids, and forbidden-authority list preserved | proof log | PRL-MRP-018 |
| PRL-MRP-022 | Authority regression hardening | planned_not_started | Consolidate regression tests for no candidate/play/capital/order/review/workbook-read leakage | tests | No new behaviour beyond guard hardening | PRL-MRP-019/021 | authority regression suite | hidden authority rejected/absent across enriched path | proof log | PRL-MRP-019 |
| PRL-MRP-023 | Vocabulary-governed description constraints | planned_not_started | Formalise controlled-language requirements before description output | docs/planning/tests maybe vocabulary if authorised | No description engine | vocabulary docs fully read | vocabulary/description contract tests planned | constraints recorded with vocabulary refs | planning/proof artefact | PRL-MRP-022 |
| PRL-MRP-024 | Deterministic description contract and tests | planned_not_started | Add contract fields/tests for template IDs and vocabulary refs only | contracts/tests | No free-form generated prose; no engine | PRL-MRP-023 | `test_parallel_risk_description_contract.py` | description metadata is deterministic refs only | proof log | PRL-MRP-023 |
| PRL-MRP-025 | Deterministic description engine | planned_not_started | Implement template renderer that uses governed vocabulary and emits risk-only descriptions | new description module/tests | No trade advice; no review judgement; no generative prose | PRL-MRP-024 | `test_parallel_risk_description_templates.py` | deterministic strings from template/vocab refs; advice terms rejected | proof log | PRL-MRP-024 |
| PRL-MRP-026 | Documentation/current-state map update | planned_not_started | Update docs/current-state map after implementation leaves land | docs/map/ledger | No source/test changes unless opened | relevant prior leaves | doc/proof checks if available | docs distinguish implemented/upstream/deferred/out-of-scope | doc patch | PRL-MRP-019/022/025 as applicable |
| PRL-MRP-027 | Deferred rich signal-family intake plan | deferred | Plan future lawful upstream sources/contracts for VWAP, spread/depth, tape speed, realised vol/ATR, dense options chain, IV rank/implied move, skew, real gamma/gamma flip, OI concentration/pin, MOC, headline, crowding/flow, cognitive load | docs/planning only unless future source exists | No implementation of rich signals | accepted source-document audit; explicit upstream source evidence | no runtime tests until source contracts exist | each family remains blocked/deferred until typed source exists | planning artefact | PRL-MRP-020 |

Next executable leaf: **PRL-MRP-003 — Freshness register calculation**, provided the future executor rehydrates governance and opens only that leaf.

## 6. Deferred / blocked signal families

| Signal family | Why not now | Required upstream source | Required contract | Future PRL atom |
|---|---|---|---|---|
| VWAP | No typed runtime VWAP signal/source exists in PRL input surface | intraday market-data/VWAP service or promoted prepared-runtime field | `MarketMicrostructureContext` or promoted `SignalSnapshotEntry` family | VWAP reliability / VWAP gravity risk |
| Spread/depth | No typed NBBO/L2 depth contract is available to PRL | quote feed with bid/ask and size/depth | `LiquidityContext` | liquidity-poor order book risk |
| Tape speed / relative volume | No trade-count/volume-curve baseline source is typed | trades, cumulative volume, historical intraday volume curve | `TapeSpeedContext` / `VolumeContext` | open chaos / thin tape risk |
| Realised volatility / ATR | Rolling realised-vol/ATR service not available to PRL | bar series/high-low/returns | `RealizedVolatilityContext` | volatility regime / unstable range risk |
| Dense options chain | Current options input has spot/front/next DTE only | options chain feed with quote, IV, volume, OI, greeks | `OptionsChainSnapshot` | options liquidity / vol-surface risk |
| IV rank / implied move | No IV history/straddle calculation source | IV history and ATM straddle/term surface | `OptionsVolatilityContext` | event vol premium / IV crush risk |
| Skew | Current `skew_state` is not a real skew calculation | IV by strike/expiry | `OptionsSkewContext` | skew asymmetry risk |
| Real gamma exposure / gamma flip | Current gamma state is not dealer gamma exposure | options chain greeks + OI/volume + spot model | `DealerConvexityContext` | gamma flip / dealer acceleration risk |
| OI concentration / strike pin | No OI-by-strike concentration source | option OI by strike/expiry and spot distance | `StrikeConcentrationContext` | strike pin / magnet risk |
| MOC / close auction imbalance | No auction imbalance source exists | exchange auction/MOC imbalance feed | `AuctionContext` | closing auction liquidity risk |
| Headline risk | Financial calendar explicitly covers scheduled facts, not unscheduled news | governed news/headline feed with source time/reliability/conflict metadata | `HeadlineRiskContext` | headline reliability / information lag risk |
| Crowding / real-money flow | No prime/ETF/fund-flow/positioning source exists | ETF flow, fund flow, prime/positioning proxy | `FlowPositioningContext` | crowded deleveraging / forced-flow risk |
| Cognitive load / attention pressure | No operator/context signal contract exists | alert density, signal conflict count, event density, operator-state input if admitted | `CognitiveLoadContext` | attention fragmentation / cognitive load risk |

## 7. Authority guard checklist

Each future implementation leaf must answer `yes` to every applicable guard before closeout:

- No candidate formation is added.
- No playbook selection is added.
- No capital sizing, deployable percentage, or notional authority is added.
- No broker/order/execution instruction is added.
- No serial-stage internals are mutated or read through hidden paths.
- No review-layer judgement authority is added.
- No direct runtime workbook read is introduced.
- No unavailable Bloomberg-style signal is assigned a fabricated value.
- Plain-English description, when opened, is deterministic, vocabulary-governed, and risk-only.
- Tests are written or extended before implementation for the active leaf.
- Ledger entry records status, files changed, tests run, artefacts, and next leaf.

## 8. Vocabulary-governance requirements

Future description work must use:

- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/vocabulary/vocabulary_registry.md`
- `data/vocabulary/canonical_vocabulary.json`

Rules:

- Description output is deterministic template output, not generative commentary.
- Template IDs and vocabulary references are metadata/contract inputs until an implementation leaf opens the renderer.
- Any new durable description terms must be admitted or explicitly kept as noncanonical planning labels.
- Description text must not contain trade advice, play selection, order instruction, capital sizing, or review judgement.

## 9. Workbook signal-inventory requirements

Resolved design decision:

- The expected-signal inventory belongs in the governed Excel workbook.
- The future workbook tab name is `Parallel Risk Lane Signal Inventory`.
- Runtime code must not read the workbook directly.
- Runtime consumption may occur only after typed promotion into config/contracts.

Known workbook path:

- `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`

Known existing raw-signal/raw-primitives tab:

- `Raw_Primitives_Catalog`

Future tab requirements:

- list expected PRL signals;
- classify each as available now, upstream-but-not-projected, missing, deferred, or excluded;
- preserve lineage back to raw/derived workbook tabs;
- support missing/unavailable checks without hallucinating runtime signals.

## 10. Architecture decisions resolved after master roadmap

Decision artefact:

- `docs/planning/PRL_MINUTE_RISK_PROFILE_ARCHITECTURE_DECISIONS.md`

Resolved decisions:

| Question | Decision | Affected leaves |
|---|---|---|
| Freshness age threshold ownership after deterministic defaults | Dedicated governed PRL profile config surface, planned as `config/parallel_risk_lane_profile.v1.yaml`. `PRL-MRP-003` uses deterministic defaults only and does not read config/workbook. | `PRL-MRP-003`, `PRL-MRP-021`, `PRL-MRP-026` |
| Workbook signal-inventory promotion artefact | Typed promotion artefact planned as `config/parallel_risk_signal_inventory.v1.yaml`, validated by future `ParallelRiskSignalInventoryDocument` / `ParallelRiskExpectedSignalRecord` contracts and carrying workbook lineage. | `PRL-MRP-004`, `PRL-MRP-006`, `PRL-MRP-007`, `PRL-MRP-008`, `PRL-MRP-009`, `PRL-MRP-020` |
| VIX threshold reconciliation | Preserve current PRL VIX behaviour as compatibility mode first: VIX >= 30 caution and VIX >= 50 block. Reconciliation must be explicit and test-backed later. | `PRL-MRP-012`, `PRL-MRP-013`, `PRL-MRP-015`, `PRL-MRP-018` |
| Deterministic description template location | Dedicated template registry, planned as `data/parallel_risk/description_templates.v1.json`, with canonical vocabulary refs. Do not store templates inside canonical vocabulary data and do not generate free-form prose. | `PRL-MRP-023`, `PRL-MRP-024`, `PRL-MRP-025` |

Leaf updates from these decisions:

- `PRL-MRP-003` remains the next executable leaf; it must implement deterministic freshness defaults only and must not introduce config loading.
- `PRL-MRP-008` must plan `config/parallel_risk_signal_inventory.v1.yaml` as the exact typed promotion artefact.
- `PRL-MRP-009` remains blocked until the workbook tab exists and the YAML/contract promotion is opened.
- `PRL-MRP-012` is compatibility-preservation only; `PRL-MRP-013` is the explicit threshold reconciliation leaf.
- `PRL-MRP-024` must open a template registry contract before `PRL-MRP-025` opens rendering.

## 11. Ledger entry index

- Master roadmap task: `ROADMAP_LEDGER.md` section `PRL Minute Risk Profile Master Roadmap 001`.
- Architecture-decision task: `ROADMAP_LEDGER.md` section `PRL Minute Risk Profile Architecture Decisions 001`.
- Planned leaf table: roadmap ledger section and this document section 5.
- Future leaves must add their own ledger entries; this roadmap table is not completion evidence for any future leaf.

## 12. Open questions

The four prior master-roadmap open questions are resolved in `docs/planning/PRL_MINUTE_RISK_PROFILE_ARCHITECTURE_DECISIONS.md`. Remaining open questions that do not block `PRL-MRP-003`:

1. Should event proximity intensity use continuous scores, discrete states, or both?
2. Which rich signal family should be sourced first after the current supported atoms are stable?
3. Which proof block should eventually own PRL minute-profile verification?

