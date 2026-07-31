# Vocabulary Registry

Projection schema version: `v2_namespaced`
Projection registry version: `2026-07-31-m07-k12-normative-authority-v1`
Projection document notes: ["P1 integrated semantic authority remains preserved from accepted PM-003 through PM-009 decisions.","The 2026-07-25 user-accepted module-architecture amendment adds durable ownership, dependency-plane and local-proof control terms.","M13-PROOF admits only the exported alpha state-kernel contract vocabulary; implementation and durability remain unproved.","The 2026-07-29 repair admits PM-controlled parallel-workflow terms without parallelising canonical acceptance.","The 2026-07-30 M04 K07 amendment admits ten exact DMPV3 packet-role concepts without admitting tests or implementation conformance.","The 2026-07-30 M15 repair gives module-owned vocabulary a namespaced machine identity and bounded audit scope without prefixing human labels or ordinary code symbols.","Canonical entries are deterministic transformations of these human records; builder, JSON, audit, stamp and tests remain downstream evidence.","Contextual disallowed-use prose remains authoritative even when an exact token is omitted from the machine collision lexicon.","The 2026-07-31 M07 K12 amendment admits the exact PolicyBundle, ModifierDecision and ModifierApplicationReceipt public-contract concepts under a bounded M07 namespace."]
Projection namespace scopes: {"global":{"imports":[],"scan_paths":["src","tests","docs","config"]},"m04":{"imports":["global"],"scan_paths":["docs/09_DMPV3_PROTOCOL_CORE.md","docs/09.1_DMPV3_PROTOCOL_WORKING.md","src/nvda_desk/contracts/packets.py","src/nvda_desk/packets","src/nvda_desk/schemas/dmp.py","src/nvda_desk/schemas/dmp_envelope.py","src/nvda_desk/preparation/context_packet.py","src/nvda_desk/risk/parallel","src/nvda_desk/runtime/orchestrator.py","src/nvda_desk/services/parallel_risk_lane_service.py","src/nvda_desk/testing/harnesses/serial_runtime_parallel_risk_boundary_specimen.py","tests/tier_a/calendar_reference","tests/tier_a/capital_deployment","tests/tier_a/downstream_runtime","tests/tier_a/normative_authority","tests/tier_a/packets","tests/tier_a/parallel_risk","tests/tier_a/runtime","tests/tier_a/testing_harnesses","tests/tier_a/upstream_cognition","tests/tier_b/capital_deployment"]},"m07":{"imports":["global"],"scan_paths":["docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md","docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md","docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md","config/coefficient_authority.v1.yaml","config/coefficients_registry.example.yaml","src/nvda_desk/config/coefficient_authority.py","src/nvda_desk/contracts/coefficient_authority.py","src/nvda_desk/contracts/modifiers.py","src/nvda_desk/cognition/modifiers","src/nvda_desk/domain/posture/modifier_application.py","src/nvda_desk/services/coefficient_authority_service.py","tests/tier_a/m07_k12"]}}

### Ownership Module
Definition: Accepted target code capability identified by one `M00`–`M15` architecture ID and bounded by explicit responsibility, public contracts, state ownership, dependencies and prohibited authority.
Scope: target modular-monolith ownership boundary
Owner: Native Architecture Blueprint authority
Relationships: Allocates one or more Architecture Surfaces to a code capability; may contain several implementation obligations; is not equivalent to a surface, file, class, service process or `D-xxx` record.
Aliases: target ownership module; Mxx module
Disallowed or misleading use: architecture surface as exact synonym; implementation work unit; microservice; proof that code already owns the responsibility
Lifecycle: accepted_target_architecture
Projection metadata: {"projection_status":"canonical","canonical_label":"Ownership Module","canonical_slug":"ownership_module","category":"authority_surface","stage_owner":"native_architecture_blueprint","maps_to_contract":"docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:11.10","raw_or_derived":"not_applicable","allowed_aliases":["target ownership module","Mxx module"],"disallowed_phrases":["architecture surface as exact synonym","implementation work unit","microservice","proof that code already owns the responsibility"],"semantic_decision_refs":["USER-20260725:MODULE-ARCHITECTURE-ACCEPTANCE"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Module-local Proof Gate
Definition: Two-step governed acceptance boundary that closes normative meaning and admits the smallest truthful public-seam proof for one bounded behaviour before module-local implementation opens.
Scope: one-module semantic and proof acceptance boundary
Owner: proof and promotion governance
Relationships: Applies `C-NORM` then `C-PROOF`; preserves the normative-authority-to-test-to-code direction while avoiding mandatory routing, observation, disposition, specification and review checkpoints that add no semantic state; remains subject to final alpha consolidation.
Aliases: local module proof gate; module-local Gate C
Disallowed or misleading use: skip tests; code-first implementation; whole-repository acceptance; automatic authority from passing tests
Lifecycle: active_programme_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Module-local Proof Gate","canonical_slug":"module_local_proof_gate","category":"promotion_surface","stage_owner":"proof_promotion","maps_to_contract":"project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md","raw_or_derived":"not_applicable","allowed_aliases":["local module proof gate","module-local Gate C"],"disallowed_phrases":["skip tests","code-first implementation","whole-repository acceptance","automatic authority from passing tests"],"semantic_decision_refs":["USER-20260725:MODULE-LOCAL-PROOF","USER-20260731:MVP-FAST-TRACK"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Runtime/Contract Dependency
Definition: Directed production relationship in which one Ownership Module calls another module or consumes its accepted public contract during runtime.
Scope: production runtime and cross-module contract graph
Owner: Native Architecture Blueprint authority
Relationships: Contributes to the acyclic runtime graph; distinct from State/Transaction Participation, Governance/Promotion Prerequisite and development-only build/test dependencies.
Aliases: runtime dependency; contract dependency
Disallowed or misleading use: proof prerequisite; vocabulary approval; shared transaction participation; test fixture dependency
Lifecycle: accepted_dependency_plane
Projection metadata: {"projection_status":"canonical","canonical_label":"Runtime/Contract Dependency","canonical_slug":"runtime_contract_dependency","category":"authority_class","stage_owner":"native_architecture_blueprint","maps_to_contract":"docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:11.10.1","raw_or_derived":"not_applicable","allowed_aliases":["runtime dependency","contract dependency"],"disallowed_phrases":["proof prerequisite","vocabulary approval","shared transaction participation","test fixture dependency"],"semantic_decision_refs":["USER-20260725:DEPENDENCY-PLANES"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### State/Transaction Participation
Definition: Relationship in which a domain-owning module uses the shared `M13` transaction mechanism for atomic state and receipt effects while retaining semantic ownership of its records.
Scope: transaction participation without domain-ownership transfer
Owner: Native Architecture Blueprint authority
Relationships: Connects state-owning modules to State Kernel mechanics; distinct from a runtime business dependency and does not make `M13` owner of positions, capital, calendar facts, risk observations or other domain records.
Aliases: transaction participation; state-kernel participation
Disallowed or misleading use: shared semantic ownership; state kernel owns all records; ordinary runtime dependency; persistence proves durability
Lifecycle: accepted_dependency_plane
Projection metadata: {"projection_status":"canonical","canonical_label":"State/Transaction Participation","canonical_slug":"state_transaction_participation","category":"authority_class","stage_owner":"native_architecture_blueprint","maps_to_contract":"docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:11.10.1","raw_or_derived":"not_applicable","allowed_aliases":["transaction participation","state-kernel participation"],"disallowed_phrases":["shared semantic ownership","state kernel owns all records","ordinary runtime dependency","persistence proves durability"],"semantic_decision_refs":["USER-20260725:DEPENDENCY-PLANES"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Governance/Promotion Prerequisite
Definition: Non-runtime relationship requiring accepted proof, vocabulary or other governance evidence before a module or behaviour may be promoted.
Scope: architecture governance and acceptance plane
Owner: proof and vocabulary governance
Relationships: Commonly links runtime modules to `M14` and `M15`; must not be drawn as a universal production import or used to create false runtime cycles.
Aliases: governance prerequisite; promotion prerequisite
Disallowed or misleading use: hard runtime dependency; production import; business decision call; module implementation dependency
Lifecycle: accepted_dependency_plane
Projection metadata: {"projection_status":"canonical","canonical_label":"Governance/Promotion Prerequisite","canonical_slug":"governance_promotion_prerequisite","category":"promotion_rule","stage_owner":"proof_promotion","maps_to_contract":"docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:11.10.1","raw_or_derived":"not_applicable","allowed_aliases":["governance prerequisite","promotion prerequisite"],"disallowed_phrases":["hard runtime dependency","production import","business decision call","module implementation dependency"],"semantic_decision_refs":["USER-20260725:DEPENDENCY-PLANES"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Legacy Shadow Unadmitted
Definition: Neutral status for a runnable existing test that has not been admitted as authority for the active Module-local Proof Gate and therefore cannot dictate the active implementation.
Scope: unrelated or not-yet-reviewed legacy test evidence
Owner: proof and promotion governance
Relationships: Remains visible during full-suite shadow execution; may later be admitted, repaired, classified as observational or retired through semantic review; neither passing nor failing establishes current authority.
Aliases: unadmitted legacy shadow
Disallowed or misleading use: ignored test; approved Tier B test; failed authoritative proof; permission to delete
Lifecycle: active_test_status
Projection metadata: {"projection_status":"canonical","canonical_label":"Legacy Shadow Unadmitted","canonical_slug":"legacy_shadow_unadmitted","category":"audit_classification","stage_owner":"proof_promotion","maps_to_contract":"project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md","raw_or_derived":"not_applicable","allowed_aliases":["unadmitted legacy shadow"],"disallowed_phrases":["ignored test","approved Tier B test","failed authoritative proof","permission to delete"],"semantic_decision_refs":["USER-20260725:MODULE-LOCAL-PROOF"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Coefficient and Modifier Authority
Definition: Bounded ownership surface for versioned coefficient and modifier bundles, precedence, stage ownership, hard bounds and application receipts.
Scope: target module `M07` only
Owner: coefficient and modifier authority
Relationships: Supplies governed coefficient/modifier decisions to eligible consumers; distinct from calendar, playbook, capital, execution, lifecycle and replay policy ownership.
Aliases: dynamic coefficient and modifier authority; M07 coefficient_modifier_authority
Disallowed or misleading use: policy authority; global policy engine; capital policy owner; playbook catalogue
Lifecycle: accepted_target_module_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"Coefficient and Modifier Authority","canonical_slug":"coefficient_and_modifier_authority","category":"authority_surface","stage_owner":"coefficient_modifier_authority","maps_to_contract":"docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:11.10","raw_or_derived":"not_applicable","allowed_aliases":["dynamic coefficient and modifier authority","M07 coefficient_modifier_authority"],"disallowed_phrases":["policy authority","global policy engine","capital policy owner","playbook catalogue"],"semantic_decision_refs":["USER-20260725:M07-NARROWING"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Component Skeleton
Definition: Architecture control surface that defines the permitted module-level component form, bounded responsibility, lawful inputs and outputs, dependencies, forbidden co-location, and honest status.
Scope: native architecture component-form control
Owner: Native Architecture Blueprint Core
Relationships: Instantiates Target Structure and Ownership Matrix decisions at module level; must obey Seam Contracts, Persistence Architecture and Test Architecture.
Aliases: None admitted.
Disallowed or misleading use: Do not use for a generic code template or as proof that a component is implemented.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Component Skeleton","canonical_slug":"component_skeleton","category":"authority_surface","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:107-119,465-489","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["generic code template","implementation proof"],"semantic_decision_refs":["PM-003:AMC-001"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Module Allocation Appendix
Definition: Migration-facing allocation surface that maps current-state or donor material to lawful target modules without overriding target structure, ownership, seam, persistence, test, or reservation law.
Scope: migration allocation evidence
Owner: Native Architecture Blueprint Core
Relationships: Subordinate to Target Structure, Component Skeleton, Ownership Matrix, Seam Contracts, Persistence Architecture, Test Architecture and Reservations; informed by Traceability Appendix.
Aliases: None admitted.
Disallowed or misleading use: Do not use as target-architecture authority or as permission to preserve legacy placement.
Lifecycle: active_normative_migration_surface
Projection metadata: {"projection_status":"canonical","canonical_label":"Module Allocation Appendix","canonical_slug":"module_allocation_appendix","category":"authority_surface","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:118-119,643-665","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["target architecture authority","legacy-placement permission"],"semantic_decision_refs":["PM-003:AMC-002"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Native Architecture Blueprint Core
Definition: Accepted numbered normative architecture authority governing native target placement, component form, ownership, seams, persistence, proof families, reservations, allocation and traceability under the project authority hierarchy.
Scope: native code-structure architecture authority
Owner: Normative authority stack
Relationships: Owns and orders the architecture control surfaces; remains subordinate to higher normative authority and does not by itself prove implementation conformity.
Aliases: None admitted.
Disallowed or misleading use: Do not shorten to blueprint when that would obscure its specific numbered normative authority; do not use as an implementation-status receipt.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Native Architecture Blueprint Core","canonical_slug":"native_architecture_blueprint_core","category":"authority_surface","stage_owner":"Normative authority stack","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:103-121; docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md:139-145","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["implementation status receipt","generic blueprint"],"semantic_decision_refs":["PM-003:AMC-003"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["11 native architecture blueprint core"]}

### Ownership Matrix
Definition: Architecture control surface that assigns each capability one target owner, lawful inputs and outputs, forbidden placement, and honest status.
Scope: native architecture capability ownership
Owner: Native Architecture Blueprint Core
Relationships: Constrains Target Structure and Component Skeleton; target-owner decisions govern migration allocation and seam responsibility.
Aliases: None admitted.
Disallowed or misleading use: Do not use file location, class name, current writer or historical owner as a substitute for target ownership.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Ownership Matrix","canonical_slug":"ownership_matrix","category":"authority_surface","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:112,490-508","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["current-file ownership","historical ownership"],"semantic_decision_refs":["PM-003:AMC-004"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Persistence Architecture
Definition: Architecture control surface governing durable-state semantic owners, authorised writers, readers, persistence classes, stores, fallback rules, forbidden mixing and migration traceability.
Scope: native durable-state architecture
Owner: Native Architecture Blueprint Core
Relationships: Must align with Ownership Matrix, Seam Contracts, Component Skeleton and Test Architecture; technology choice is subordinate to state ownership.
Aliases: None admitted.
Disallowed or misleading use: Do not use database technology, repository existence or in-memory state as proof of complete durability.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Persistence Architecture","canonical_slug":"persistence_architecture","category":"authority_surface","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:115,568-593","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["database technology as architecture completion"],"semantic_decision_refs":["PM-003:AMC-005"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Reservations
Definition: Visible bounded architecture decisions whose final allocation is unresolved and must not be implemented as locked until required evidence resolves them.
Scope: unresolved native architecture allocation
Owner: Native Architecture Blueprint Core
Relationships: Distinct from Provisional Allocations: a reservation preserves an unresolved decision rather than a bounded likely direction.
Aliases: None admitted.
Disallowed or misleading use: Do not call a reservation a target allocation, accepted design or implementation permission.
Lifecycle: active_unresolved
Projection metadata: {"projection_status":"canonical","canonical_label":"Reservations","canonical_slug":"reservations","category":"authority_class","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:117,618-640","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["locked allocation","accepted design"],"semantic_decision_refs":["PM-003:AMC-006"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Provisional Allocations
Definition: Bounded likely target allocations whose final detail is not locked and which must not expand beyond their stated options without lawful update.
Scope: bounded but not final native architecture allocation
Owner: Native Architecture Blueprint Core
Relationships: Distinct from Reservations: a provisional allocation records a bounded likely direction while preserving explicit non-final status.
Aliases: None admitted.
Disallowed or misleading use: Do not call a provisional allocation locked, final, implemented or unrestricted.
Lifecycle: active_provisional
Projection metadata: {"projection_status":"canonical","canonical_label":"Provisional Allocations","canonical_slug":"provisional_allocations","category":"authority_class","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:618-640","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["locked or unrestricted allocation"],"semantic_decision_refs":["PM-003:AMC-007"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Seam Contract
Definition: One explicit architecture-boundary contract identifying upstream and downstream owners, carrier type, required invariants, side effects, variants, category and migration traceability where applicable.
Scope: single native architecture boundary contract
Owner: Native Architecture Blueprint Core
Relationships: One member of the governed Seam Contracts family; must agree with Ownership Matrix, Persistence Architecture and Test Architecture.
Aliases: None admitted.
Disallowed or misleading use: Do not use for an implicit call path, shared dictionary, undocumented coupling or mere function signature.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Seam Contract","canonical_slug":"seam_contract","category":"protocol_surface","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:113,514-542","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["implicit call path","function signature alone"],"semantic_decision_refs":["PM-003:AMC-008"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Seam Contracts
Definition: The governed collective control surface comprising explicit boundary contracts between architecture surfaces; each member preserves ownership, carrier and proof rules.
Scope: collective native architecture boundary-control surface
Owner: Native Architecture Blueprint Core
Relationships: Collective concept distinct from the singular Seam Contract instance; governs the family and its required consistency.
Aliases: None admitted.
Disallowed or misleading use: Do not treat the plural as a free synonym for one contract where instance-level identity matters.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Seam Contracts","canonical_slug":"seam_contracts","category":"protocol","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:113,514-542","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["one unnamed contract when identity matters"],"semantic_decision_refs":["PM-003:AMC-009"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Sequential Native Architecture Surface
Definition: One governed runtime or control architecture surface in the ordered native sequence, with bounded ownership, lawful carriers, proof obligation and honest status.
Scope: one native architecture sequence member
Owner: Native Architecture Blueprint Core
Relationships: One member of Sequential Native Architecture Surfaces; its predecessor, successor and cross-cutting controls must remain explicit.
Aliases: None admitted.
Disallowed or misleading use: Do not use for an arbitrary module, file, UI screen or legacy workflow stage.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Sequential Native Architecture Surface","canonical_slug":"sequential_native_architecture_surface","category":"authority_surface","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:125-133","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["arbitrary module/file/workflow stage"],"semantic_decision_refs":["PM-003:AMC-010"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Sequential Native Architecture Surfaces
Definition: The ordered collective architecture from external source ingress through runtime/control surfaces to review, proof and vocabulary governance.
Scope: ordered collective native architecture sequence
Owner: Native Architecture Blueprint Core
Relationships: Collective concept distinct from one Sequential Native Architecture Surface; controls top-to-bottom review and migration order.
Aliases: None admitted.
Disallowed or misleading use: Do not start the sequence at serial desk cognition or use informal architecture metaphors as normative labels.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Sequential Native Architecture Surfaces","canonical_slug":"sequential_native_architecture_surfaces","category":"workflow","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:109,125-133","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["serial-cognition-first architecture","informal metaphor"],"semantic_decision_refs":["PM-003:AMC-011"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Bridge and Shell Policy
Definition: Architecture control surface governing explicitly labelled transitional, advisory, optional and shell surfaces, including allowed behaviour, forbidden behaviour, resolution path and honest status.
Scope: transitional and incomplete native architecture surfaces
Owner: Native Architecture Blueprint Core
Relationships: Governs bridge and shell legal status; Shell Policy is a lawful contextual alias, not a separate control concept.
Aliases: Shell Policy.
Disallowed or misleading use: Do not present a bridge, shell, advisory or optional surface as completed behaviour or implementation proof.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Bridge and Shell Policy","canonical_slug":"bridge_and_shell_policy","category":"authority_surface","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:114,543-567","raw_or_derived":"not_applicable","allowed_aliases":["Shell Policy"],"disallowed_phrases":["completed-behaviour claim for partial surface"],"semantic_decision_refs":["PM-003:AMC-012","PM-003:AMC-013"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Target Structure
Definition: Architecture control surface governing target package and subpackage placement so capabilities land in lawful native homes rather than inherited current-state locations.
Scope: native package and subpackage placement
Owner: Native Architecture Blueprint Core
Relationships: Precedes Component Skeleton and Module Allocation Appendix; constrained by Ownership Matrix and Reservations.
Aliases: None admitted.
Disallowed or misleading use: Do not use current file location, donor structure or convenience placement as target authority.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Target Structure","canonical_slug":"target_structure","category":"authority_surface","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:110,443-464","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["current or donor file layout"],"semantic_decision_refs":["PM-003:AMC-014"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Test Architecture
Definition: Architecture control surface governing required proof families, target subsystem, failure signal, constraints and honest proof status for architecture claims.
Scope: native architecture proof-family design
Owner: Native Architecture Blueprint Core
Relationships: Maps architecture claims to proof obligations; test results remain evidence and cannot override normative meaning.
Aliases: None admitted.
Disallowed or misleading use: Do not use test colour, fixture shape or test existence as semantic or architecture authority.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Test Architecture","canonical_slug":"test_architecture","category":"authority_surface","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:116,594-617; docs/08_TESTING_AND_PROMOTION_CORE.md:1-67","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["test colour as semantic authority"],"semantic_decision_refs":["PM-003:AMC-015"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Traceability Appendix
Definition: Migration-evidence surface explaining why current-state or donor material is carried forward and the lawful target architecture path it must follow; it is not implementation authority.
Scope: current-state and donor migration traceability
Owner: Native Architecture Blueprint Core
Relationships: Feeds Module Allocation Appendix and must resolve to lawful target structure, component form, owner, seam, persistence owner and test family.
Aliases: None admitted.
Disallowed or misleading use: Do not use traceability, provenance or historical receipts as target design or implementation authority.
Lifecycle: active_normative_migration_surface
Projection metadata: {"projection_status":"canonical","canonical_label":"Traceability Appendix","canonical_slug":"traceability_appendix","category":"review_surface","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:119,669-687","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["target design or implementation authority"],"semantic_decision_refs":["PM-003:AMC-016"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Donor Evidence
Definition: Retained legacy source consulted only as historical evidence for reconstructing a bounded behaviour or claim; it is not live native authority.
Scope: historical migration evidence
Owner: Vocabulary governance under normative/process authority
Relationships: May support Behaviour Block and Intent Unit recovery and Traceability Appendix entries; remains subordinate to current normative authority.
Aliases: None admitted.
Disallowed or misleading use: Do not use donor source, legacy behaviour or predecessor tests as live normative or implementation authority.
Lifecycle: retained_historical
Projection metadata: {"projection_status":"canonical","canonical_label":"Donor Evidence","canonical_slug":"donor_evidence","category":"carrier","stage_owner":"Vocabulary governance under normative/process authority","maps_to_contract":"docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:138-146; docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:669-687","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["legacy source as live authority"],"semantic_decision_refs":["PM-003:AMC-017"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Behaviour Block
Definition: A bounded donor-reading subdivision inside one source file used to recover one or more intent units without treating file structure as target architecture.
Scope: historical migration analysis
Owner: Vocabulary governance under migration/process authority
Relationships: Derived from Donor Evidence; decomposed into Intent Units; does not determine Target Structure or Component Skeleton.
Aliases: None admitted.
Disallowed or misleading use: Do not use as a target module, runtime component or acceptance unit merely because it follows donor file boundaries.
Lifecycle: retained_historical
Projection metadata: {"projection_status":"canonical","canonical_label":"Behaviour Block","canonical_slug":"behaviour_block","category":"carrier","stage_owner":"Vocabulary governance under migration/process authority","maps_to_contract":"docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:138-146","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["target component or module"],"semantic_decision_refs":["PM-003:AMC-018"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Intent Unit
Definition: The atomic migration-rebuild concept representing one bounded behavioural job with one lawful target owner and one bounded proof family.
Scope: migration behaviour recovery and allocation
Owner: Vocabulary governance under migration/process authority
Relationships: Recovered from Behaviour Blocks; assigned to a Target Owner; distinct from Leaf, which is an execution-plan unit.
Aliases: Atomic Intent Unit.
Disallowed or misleading use: Do not use for a donor file, broad feature bundle, implementation task list or arbitrary code fragment.
Lifecycle: retained_historical
Projection metadata: {"projection_status":"canonical","canonical_label":"Intent Unit","canonical_slug":"intent_unit","category":"carrier","stage_owner":"Vocabulary governance under migration/process authority","maps_to_contract":"docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:138-146","raw_or_derived":"not_applicable","allowed_aliases":["Atomic Intent Unit"],"disallowed_phrases":["file, feature bundle or arbitrary task"],"semantic_decision_refs":["PM-003:AMC-019","PM-003:AMC-020"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["intent unit id"]}

### Target Owner
Definition: The lawful native architecture owner assigned to a capability or recovered intent unit, independent of its legacy location or current incidental writer.
Scope: native ownership assignment during migration
Owner: Native Architecture Blueprint Core
Relationships: Expressed by Ownership Matrix; required before migration allocation or carried-forward implementation is accepted.
Aliases: None admitted.
Disallowed or misleading use: Do not use current file, class, legacy module, coordinator or data reader as owner without normative assignment.
Lifecycle: active_normative_migration_term
Projection metadata: {"projection_status":"canonical","canonical_label":"Target Owner","canonical_slug":"target_owner","category":"authority_class","stage_owner":"Native Architecture Blueprint Core","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:490-508; docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:142-149","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["legacy owner","current writer by inference"],"semantic_decision_refs":["PM-003:AMC-021"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["target owner evidence"]}

### Leaf
Definition: One bounded executable work unit selected inside the active tranche or ExecPlan, with one objective, scope, proof boundary and recorded outcome.
Scope: programme execution control
Owner: Repo-root AGENTS and active bounded pack
Relationships: Executes one Semantic Acceptance unit where the plan so defines; distinct from Intent Unit because a leaf is work sequencing, not recovered behaviour ontology.
Aliases: None admitted.
Disallowed or misleading use: Do not use for an arbitrary file, checklist item, worker, cohort or unbounded batch.
Lifecycle: active_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Leaf","canonical_slug":"leaf","category":"carrier","stage_owner":"Repo-root AGENTS and active bounded pack","maps_to_contract":"AGENTS.md:7-16,145-177; docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:147-150","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["file, worker, cohort or unbounded batch"],"semantic_decision_refs":["PM-003:AMC-022"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Authority Intake Gate
Definition: The pre-edit control step that declares in-scope authority files, full-read status, pass/fail criterion and authority conflicts before repo claims or mutations.
Scope: programme authority intake control
Owner: Process and tranche law / active bounded pack
Relationships: Precedes semantic adjudication; supplies evidence to a Leaf and must obey the Execution Read Sequence.
Aliases: None admitted.
Disallowed or misleading use: Do not use a manifest, search result or file count alone as proof that semantic authority was understood.
Lifecycle: active_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Authority Intake Gate","canonical_slug":"authority_intake_gate","category":"workflow","stage_owner":"Process and tranche law / active bounded pack","maps_to_contract":"docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:147-150; docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md:18-31","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["manifest-only proof of semantic read"],"semantic_decision_refs":["PM-003:AMC-023"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Execution Read Sequence
Definition: The ordered substantive repository reading sequence owned by process law: standing controls and active pack first, routed normative authority next, execution-plan surfaces next and retained evidence last.
Scope: programme reading order
Owner: Process and Tranche Law Core
Relationships: Constrains Authority Intake Gate and every substantive Leaf; distinct from a full-read manifest, which records evidence of reading.
Aliases: None admitted.
Disallowed or misleading use: Do not use alphabetical, file-system, test-first or code-first order as a substitute for routed authority order.
Lifecycle: active_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Execution Read Sequence","canonical_slug":"execution_read_sequence","category":"workflow","stage_owner":"Process and Tranche Law Core","maps_to_contract":"docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md:18-31","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["test-first, code-first or filesystem order"],"semantic_decision_refs":["PM-003:AMC-024"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Active Bounded Pack
Definition: The one currently routed, expressly declared bundle of scope, authority, mutable surfaces, gate law and execution-plan surfaces for one active repository objective.
Scope: programme mutation authority
Owner: Process and Tranche Law Core plus current working declaration
Relationships: Comprises one or more Active Bounded Pack Surfaces; bounds Leafs and mutable paths; no nearby file joins by implication.
Aliases: active pack
Disallowed or misleading use: Do not use historical pack, relevant folder, nearby document or informal task description as mutation authority.
Lifecycle: active_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Active Bounded Pack","canonical_slug":"active_bounded_pack","category":"carrier","stage_owner":"Process and Tranche Law Core plus current working declaration","maps_to_contract":"docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md:33-51; docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:14-50","raw_or_derived":"not_applicable","allowed_aliases":["active pack"],"disallowed_phrases":["historical pack","relevant folder"],"semantic_decision_refs":["PM-003:AMC-025"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["active bounded pack path","bounded pack"]}

### Active Bounded Pack Surface
Definition: A specific live-routed file that declares or constrains the Active Bounded Pack for the current programme route.
Scope: programme control-surface membership
Owner: Process and Tranche Law Core plus current working declaration
Relationships: One member of the Active Bounded Pack; may define authority, scope, gate boundaries or execution order.
Aliases: None admitted.
Disallowed or misleading use: Do not treat a related, historical or merely referenced file as a pack surface without explicit live routing.
Lifecycle: active_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Active Bounded Pack Surface","canonical_slug":"active_bounded_pack_surface","category":"authority_surface","stage_owner":"Process and Tranche Law Core plus current working declaration","maps_to_contract":"docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md:37-49; docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:14-50","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["nearby or referenced file"],"semantic_decision_refs":["PM-003:AMC-026"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Semantic Acceptance
Definition: A proposition-level human or LLM judgement reached after full contextual reading, cross-document comparison, explicit reasoning and full reread; mechanical evidence may support but cannot decide it.
Scope: normative and behavioural adjudication
Owner: Active semantic-acceptance programme under normative authority
Relationships: Closes one Semantic Acceptance Unit when its proof boundary is satisfied; distinct from test pass, lint pass, receipt existence or string classification.
Aliases: None admitted.
Disallowed or misleading use: Do not use green tests, automated classification, consensus, file completion or unchanged hashes as semantic acceptance by themselves.
Lifecycle: active_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Semantic Acceptance","canonical_slug":"semantic_acceptance","category":"authority_class","stage_owner":"Active semantic-acceptance programme under normative authority","maps_to_contract":"PLANS.md:77-97; docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:82-103","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["green test, lint or classifier result"],"semantic_decision_refs":["PM-003:AMC-027"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Implementation Truth
Definition: Directly evidenced present behaviour, composition, persistence, proof or status, stated separately from target architecture and planned intent.
Scope: current implementation state
Owner: Technical Architecture Working authority
Relationships: Compared against normative target architecture; supported by target code and applicable proof, not created by ledgers or receipts.
Aliases: None admitted.
Disallowed or misleading use: Do not use planned, desired, documented, tested-in-isolation or historically claimed state as present implementation truth without direct evidence.
Lifecycle: active_alpha_status_term
Projection metadata: {"projection_status":"canonical","canonical_label":"Implementation Truth","canonical_slug":"implementation_truth","category":"authority_class","stage_owner":"Technical Architecture Working authority","maps_to_contract":"docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:15-18; docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:103-103; docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:21-66","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["planned, desired or receipt-only state"],"semantic_decision_refs":["PM-003:AMC-028"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Normative Baseline
Definition: The versioned accepted set of normative cores, admitted working addenda, authority order, hashes, effective status and explicit unresolved reservations for a stated programme point.
Scope: versioned normative authority state
Owner: Normative authority stack
Relationships: Governs later implementation alignment; includes unresolved reservations explicitly and excludes implementation evidence from becoming normative by proximity.
Aliases: None admitted.
Disallowed or misleading use: Do not use repository snapshot, test baseline, code baseline or historical receipt as a synonym unless it is the expressly accepted normative set.
Lifecycle: active_alpha_status_term
Projection metadata: {"projection_status":"canonical","canonical_label":"Normative Baseline","canonical_slug":"normative_baseline","category":"authority_class","stage_owner":"Normative authority stack","maps_to_contract":"docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:24-34; docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:135-148","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["repository or test baseline"],"semantic_decision_refs":["PM-003:AMC-029"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Alpha Implementation
Definition: An incomplete pre-operational implementation whose current behaviour and gaps must be stated honestly and which carries no production, paper-trading, durability or end-to-end maturity implication.
Scope: current developmental implementation maturity
Owner: Technical Architecture Working authority
Relationships: Implementation Truth is assessed within this maturity state; target architecture may exceed current alpha behaviour.
Aliases: None admitted.
Disallowed or misleading use: Do not use production-ready, validated, complete, operational, durable or end-to-end as implied properties of alpha implementation.
Lifecycle: active_alpha_status_term
Projection metadata: {"projection_status":"canonical","canonical_label":"Alpha Implementation","canonical_slug":"alpha_implementation","category":"authority_class","stage_owner":"Technical Architecture Working authority","maps_to_contract":"docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:21-66; docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:145-145","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["production-ready, complete or durable"],"semantic_decision_refs":["PM-003:AMC-030"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Modular Monolith
Definition: One maintained deployable codebase partitioned into bounded modules with explicit ownership and contracts so implementations can change independently without requiring distributed deployment.
Scope: target alpha deployment and module form
Owner: Native Architecture Blueprint Working authority
Relationships: Implemented through Target Structure, Component Skeleton, Ownership Matrix, Seam Contracts and a Composition Root; separation may occur later only for evidenced requirements.
Aliases: None admitted.
Disallowed or misleading use: Do not use as a synonym for microservices, unrestricted in-process coupling, shared internals, dynamic plugins or one mixed-responsibility module.
Lifecycle: active_target_architecture_term
Projection metadata: {"projection_status":"canonical","canonical_label":"Modular Monolith","canonical_slug":"modular_monolith","category":"authority_surface","stage_owner":"Native Architecture Blueprint Working authority","maps_to_contract":"docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:94-94,145-145; docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:68-87","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["microservices","shared internals","mixed-responsibility monolith"],"semantic_decision_refs":["PM-003:AMC-031"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Composition Root
Definition: The bounded assembly surface that constructs concrete dependencies and connects adapters, services, repositories and entry points without owning the domain decisions performed by those components.
Scope: runtime dependency assembly
Owner: Native Architecture Blueprint Working authority
Relationships: Realises modular-monolith wiring and dependency direction; infrastructure dependencies enter bounded services through explicit construction here or an equivalent lawful boundary.
Aliases: None admitted.
Disallowed or misleading use: Do not use as a global service locator, domain orchestrator, policy owner or container for hidden business logic.
Lifecycle: active_target_architecture_term
Projection metadata: {"projection_status":"canonical","canonical_label":"Composition Root","canonical_slug":"composition_root","category":"authority_surface","stage_owner":"Native Architecture Blueprint Working authority","maps_to_contract":"docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:68-98","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["global service locator","domain orchestrator"],"semantic_decision_refs":["PM-003:AMC-032"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Coefficient Authority
Definition: Governed typed configuration and contract authority that owns coefficient identity, owner stage, baseline value, surface class, hard floor and cap, promoted version, and the currently authorised coefficient record.
Scope: coefficient value and bound authority
Owner: Coefficient and modifier authority, row 5.9
Relationships: Owns baseline and hard-bound records consumed by Modifier Authority; source workbooks and evaluations may inform promotion but are not direct runtime authority.
Aliases: Coefficient authority config; coefficient authority refs.
Disallowed or misleading use: Coefficient authority import; coefficient authority marker; coefficient authority path; coefficient authority seq8; coefficient authority service; coefficient modifier authority.
Lifecycle: active_alpha_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"Coefficient Authority","canonical_slug":"coefficient_authority","category":"authority_surface","stage_owner":"posture_risk_permission","maps_to_contract":"CoefficientAuthorityDocument","raw_or_derived":"not_applicable","allowed_aliases":["Coefficient authority config","coefficient authority refs"],"disallowed_phrases":["Coefficient authority import","coefficient authority marker","coefficient authority path","coefficient authority seq8","coefficient authority service","coefficient modifier authority"],"semantic_decision_refs":["PM-004:CME-002"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["coefficient authority \\u00761"]}

### Modifier Authority
Definition: Governed policy authority that owns modifier-policy identity, owner stage, admitted coefficient surfaces, state-conditioned effects, policy version, and modifier output meaning.
Scope: state-conditioned coefficient-policy authority
Owner: Coefficient and modifier authority, row 5.9
Relationships: Changes effective values only through admitted State-conditioned Modifiers over Coefficient Authority records; it does not own coefficient baselines, hard bounds, or promotion evidence.
Aliases: None admitted.
Disallowed or misleading use: Coefficient Authority; coefficient modifier authority when used to collapse the two propositions; unbounded live self-tuning.
Lifecycle: active_alpha_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"Modifier Authority","canonical_slug":"modifier_authority","category":"authority_surface","stage_owner":"posture_risk_permission","maps_to_contract":"ModifierPolicyRecord","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["coefficient modifier authority when used to collapse the two propositions","unbounded live self-tuning"],"semantic_decision_refs":["PM-004:CME-001"],"machine_projection_omissions":["Coefficient Authority [canonical-token:coefficient_authority]"],"audit_noncanonical_phrases":[]}

### Effective Coefficient Lineage
Definition: Deterministic review and replay record linking an effective coefficient value to its coefficient-authority identity/version, baseline, hard bounds, owner stage, active modifier identities/versions, and applied effect.
Scope: coefficient resolution lineage and replay evidence
Owner: Coefficient and modifier authority, row 5.9
Relationships: Records the result of Coefficient Authority plus Modifier Authority resolution; it does not own or promote the value it records.
Aliases: Effective lineage.
Disallowed or misleading use: Effective authority; promotion receipt when no promotion occurred; runtime authority by receipt alone.
Lifecycle: active_alpha_review_evidence
Projection metadata: {"projection_status":"canonical","canonical_label":"Effective Coefficient Lineage","canonical_slug":"effective_coefficient_lineage","category":"review_surface","stage_owner":"posture_risk_permission","maps_to_contract":"ResolvedCoefficientValue","raw_or_derived":"not_applicable","allowed_aliases":["Effective lineage"],"disallowed_phrases":["Effective authority","promotion receipt when no promotion occurred","runtime authority by receipt alone"],"semantic_decision_refs":["PM-004:CME-005"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["effective coefficient"]}

### State-conditioned Modifier
Definition: Governed modifier policy that changes an admitted Mutable Runtime Surface only when its explicit state condition is active, within the coefficient hard bounds, policy direction, and owner-stage boundary.
Scope: state-conditioned effective-coefficient transformation
Owner: Modifier Authority
Relationships: Operates over Bounded Dynamic Coefficients classified as mutable; emits Effective Coefficient Lineage and cannot target Baseline-only Surfaces.
Aliases: State conditioned.
Disallowed or misleading use: State conditioned modifier surface; state conditioned modifier tests; self-tuning coefficient.
Lifecycle: active_alpha_policy
Projection metadata: {"projection_status":"canonical","canonical_label":"State-conditioned Modifier","canonical_slug":"state_conditioned_modifier","category":"authority_surface","stage_owner":"posture_risk_permission","maps_to_contract":"ModifierPolicyRecord","raw_or_derived":"not_applicable","allowed_aliases":["State conditioned"],"disallowed_phrases":["State conditioned modifier surface","state conditioned modifier tests","self-tuning coefficient"],"semantic_decision_refs":["PM-004:CME-006"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Bounded Dynamic Coefficient
Definition: Coefficient whose runtime effective value may vary only through admitted State-conditioned Modifiers inside declared hard bounds and governed owner-stage and promotion authority.
Scope: runtime-mutable bounded coefficient class
Owner: Coefficient Authority
Relationships: A coefficient-value class associated with Mutable Runtime Surface; distinct from a modifier policy and from a Baseline-only Surface.
Aliases: Bounded coefficient; dynamic coefficient.
Disallowed or misleading use: Unbounded dynamic coefficient; adaptive self-tuning coefficient; modifier policy.
Lifecycle: active_alpha_authority_class
Projection metadata: {"projection_status":"canonical","canonical_label":"Bounded Dynamic Coefficient","canonical_slug":"bounded_dynamic_coefficient","category":"authority_class","stage_owner":"posture_risk_permission","maps_to_contract":"CoefficientAuthorityRecord","raw_or_derived":"not_applicable","allowed_aliases":["Bounded coefficient","dynamic coefficient"],"disallowed_phrases":["Unbounded dynamic coefficient","adaptive self-tuning coefficient","modifier policy"],"semantic_decision_refs":["PM-004:CME-007"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Policy Bundle
Definition: Immutable, versioned M07 coefficient/modifier authority bundle containing governed coefficient members, modifier members, precedence/conflict law, hard bounds, resolution-law version and promotion/workbook lineage.
Scope: K12 M07 coefficient/modifier authority bundle
Owner: Coefficient and Modifier Authority
Relationships: Supplies the exact authority material consumed to produce a Modifier Decision; contains only M07 coefficient/modifier policy and is distinct from global, calendar, playbook, capital, execution, lifecycle, replay and transaction policy.
Aliases: PolicyBundle; coefficient/modifier policy bundle.
Disallowed or misleading use: Global policy bundle; arbitrary policy mapping; capital policy bundle; playbook bundle; caller-constructed runtime authority.
Lifecycle: active_k12_contract
Projection metadata: {"projection_status":"canonical","namespace":"m07","canonical_label":"Policy Bundle","canonical_slug":"policy_bundle","category":"protocol_surface","stage_owner":"coefficient_modifier_authority","maps_to_contract":"docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:7.7","raw_or_derived":"not_applicable","allowed_aliases":["PolicyBundle","coefficient/modifier policy bundle"],"disallowed_phrases":["global policy bundle","arbitrary policy mapping","capital policy bundle","playbook bundle","caller-constructed runtime authority"],"semantic_decision_refs":["M07-K12-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Modifier Decision
Definition: Deterministic, side-effect-free M07 result resolving one identified valid Policy Bundle against identified owner-stage input facts under the bundle's precedence, conflict and hard-bound law.
Scope: K12 coefficient/modifier resolution output
Owner: Coefficient and Modifier Authority
Relationships: Preserves ordered modifier disposition and baseline-to-effective coefficient lineage; may be consumed by lawful owner-stage consumers and may produce a Modifier Application Receipt when not rejected.
Aliases: ModifierDecision; coefficient/modifier resolution decision.
Disallowed or misleading use: Capital decision; strategy-selection decision; execution decision; hidden state mutation; caller-order result.
Lifecycle: active_k12_contract
Projection metadata: {"projection_status":"canonical","namespace":"m07","canonical_label":"Modifier Decision","canonical_slug":"modifier_decision","category":"protocol_surface","stage_owner":"coefficient_modifier_authority","maps_to_contract":"docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:7.7.5","raw_or_derived":"derived","allowed_aliases":["ModifierDecision","coefficient/modifier resolution decision"],"disallowed_phrases":["modifier decision used as capital authority","modifier decision used as strategy-selection authority","modifier decision used as execution authority","modifier decision claiming hidden state mutation","modifier decision resolved by caller order"],"semantic_decision_refs":["M07-K12-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Modifier Application Receipt
Definition: Immutable M07 evidence that one non-rejected Modifier Decision was resolved for one identified owner-stage application context, including bundle/version, ordered modifier and bounded coefficient lineage.
Scope: K12 coefficient/modifier resolution and application evidence
Owner: Coefficient and Modifier Authority
Relationships: References a Modifier Decision and preserves no-op or applied resolution facts; distinct from an M12 replay result, M13 Atomic Receipt, capital receipt, execution receipt and proof of downstream state mutation.
Aliases: ModifierApplicationReceipt; modifier resolution receipt.
Disallowed or misleading use: Replay receipt; transaction receipt; proof of external mutation; capital application receipt; successful receipt for a rejected decision.
Lifecycle: active_k12_contract
Projection metadata: {"projection_status":"canonical","namespace":"m07","canonical_label":"Modifier Application Receipt","canonical_slug":"modifier_application_receipt","category":"review_surface","stage_owner":"coefficient_modifier_authority","maps_to_contract":"docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:7.7.6","raw_or_derived":"derived","allowed_aliases":["ModifierApplicationReceipt","modifier resolution receipt"],"disallowed_phrases":["modifier application receipt used as replay authority","modifier application receipt used as transaction authority","modifier application receipt claiming external mutation","modifier application receipt used as capital authority","successful modifier application receipt for a rejected decision"],"semantic_decision_refs":["M07-K12-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Review Horizon
Definition: Declared evidence window or trigger at which a coefficient or modifier candidate may be reviewed for promotion; it is not a runtime state trigger and cannot mutate live authority.
Scope: coefficient/modifier promotion review timing
Owner: Coefficient promotion authority
Relationships: Gates Champion/Challenger Evaluation and requires the declared evidence modes; does not activate a State-conditioned Modifier.
Aliases: None admitted.
Disallowed or misleading use: Live trigger; single-backtest trigger; automatic tuning interval.
Lifecycle: active_promotion_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Review Horizon","canonical_slug":"review_horizon","category":"promotion_surface","stage_owner":"posture_risk_permission","maps_to_contract":"CoefficientReviewHorizon","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Live trigger","single-backtest trigger","automatic tuning interval"],"semantic_decision_refs":["PM-004:CME-008"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Champion/Challenger Evaluation
Definition: Non-deploying comparison in which the current promoted coefficient/modifier authority remains champion and a candidate challenger is evaluated without live authority until an explicit promotion gate accepts it.
Scope: coefficient/modifier candidate evaluation
Owner: Coefficient promotion authority
Relationships: Uses Review Horizon and separated historical/live-paper evidence; produces promotion evidence, not runtime value changes.
Aliases: None admitted.
Disallowed or misleading use: Automatic promotion; online learning; self-tuning; challenger live authority.
Lifecycle: active_promotion_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Champion/Challenger Evaluation","canonical_slug":"champion_challenger_evaluation","category":"promotion_surface","stage_owner":"posture_risk_permission","maps_to_contract":"CoefficientPromotionEvaluation","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Automatic promotion","online learning","self-tuning","challenger live authority"],"semantic_decision_refs":["PM-004:CME-009"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Live-paper / Historical Evaluation Separation
Definition: Promotion rule requiring live-paper evidence and historical evaluation evidence to remain separately identified, neither stream directly mutating live coefficient or modifier authority.
Scope: coefficient/modifier evaluation evidence separation
Owner: Coefficient promotion authority
Relationships: Constrains Champion/Challenger Evaluation and promotion receipts; distinct from the promoted runtime authority consumed after the gate.
Aliases: None admitted.
Disallowed or misleading use: Combined backtest/live authority; direct live update; capital deployment authority.
Lifecycle: active_promotion_rule
Projection metadata: {"projection_status":"canonical","canonical_label":"Live-paper / Historical Evaluation Separation","canonical_slug":"live_paper_historical_evaluation_separation","category":"promotion_rule","stage_owner":"posture_risk_permission","maps_to_contract":"CoefficientEvaluationSeparationRule","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Combined backtest/live authority","direct live update"],"semantic_decision_refs":["PM-004:CME-010"],"machine_projection_omissions":["capital deployment authority [contextual prohibition; canonical authority is separately governed]"],"audit_noncanonical_phrases":[]}

### Event Calendar
Definition: Umbrella term for the governed financial-calendar architecture that preserves reference, operational and derived timing material for downstream context without owning candidate, risk, capital or execution decisions.
Scope: financial-calendar architecture umbrella
Owner: Financial-calendar domain authority
Relationships: Contains the four distinct layers Market Session Reference, Financial Event Reference, Operational Calendar State and Derived Runtime Calendar Context; it is not itself a fifth layer.
Aliases: Event calendar architecture.
Disallowed or misleading use: Calendar event; single event record; reference layer when the four-layer distinction matters.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Event Calendar","canonical_slug":"event_calendar","category":"reference_data","stage_owner":"calendar_reference","maps_to_contract":"EventCalendarProjection","raw_or_derived":"not_applicable","allowed_aliases":["Event calendar architecture"],"disallowed_phrases":["Calendar event","single event record","reference layer when the four-layer distinction matters"],"semantic_decision_refs":["PM-005:CTP-001"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Market Session Reference
Definition: Checked, versioned reference facts for trading dates, venue/session states, holidays, half-days and admitted session boundaries.
Scope: financial-calendar layer 1
Owner: Checked calendar-reference authority for session facts
Relationships: Distinct from Financial Event Reference; may inform a derived context but is never rewritten by events, operational observations or projections.
Aliases: None admitted.
Disallowed or misleading use: Session calendar when it obscures whether operational or reference truth is meant; market session state without version/source.
Lifecycle: active_normative_reference_layer
Projection metadata: {"projection_status":"canonical","canonical_label":"Market Session Reference","canonical_slug":"market_session_reference","category":"reference_data","stage_owner":"Checked calendar-reference authority for session facts","maps_to_contract":"docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:100-146","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Session calendar when it obscures whether operational or reference truth is meant","market session state without version/source"],"semantic_decision_refs":["PM-005:CTP-002"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["market session"]}

### Financial Event Reference
Definition: Checked, versioned reference facts for scheduled issuer, macroeconomic, expiry and other admitted financial-event timing.
Scope: financial-calendar layer 2
Owner: Checked calendar-reference authority for scheduled-event facts
Relationships: Distinct from Market Session Reference and Operational Calendar State even when all concern the same named date/event.
Aliases: None admitted.
Disallowed or misleading use: Event calendar when layer ownership is required; operational event observation; no-events claim from unavailable evidence.
Lifecycle: active_normative_reference_layer
Projection metadata: {"projection_status":"canonical","canonical_label":"Financial Event Reference","canonical_slug":"financial_event_reference","category":"reference_data","stage_owner":"Checked calendar-reference authority for scheduled-event facts","maps_to_contract":"docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:100-156","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Event calendar when layer ownership is required","operational event observation","no-events claim from unavailable evidence"],"semantic_decision_refs":["PM-005:CTP-003"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["financial event"]}

### Operational Calendar State
Definition: Append-preserved observations, confirmations, corrections, cancellations or actual-state facts about a named session or financial event after reference publication.
Scope: financial-calendar layer 3
Owner: Operational calendar state boundary
Relationships: May supplement or explicitly supersede a named compatible reference/operational fact; never masquerades as immutable reference or derived context.
Aliases: None admitted.
Disallowed or misleading use: Live calendar reference; mutable overwrite of reference; operational event as candidate/risk/capital authority.
Lifecycle: active_normative_operational_layer
Projection metadata: {"projection_status":"canonical","canonical_label":"Operational Calendar State","canonical_slug":"operational_calendar_state","category":"authority_surface","stage_owner":"Operational calendar state boundary","maps_to_contract":"docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:100-146","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Live calendar reference","mutable overwrite of reference","operational event as candidate/risk/capital authority"],"semantic_decision_refs":["PM-005:CTP-004"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["calendar operational"]}

### Derived Runtime Calendar Context
Definition: Deterministic context-only projection for a stated effective/as-of window, assembled from selected Market Session Reference, Financial Event Reference and Operational Calendar State facts under a versioned projection policy.
Scope: financial-calendar layer 4
Owner: Calendar projection boundary
Relationships: May select, relate and tag admitted facts for temporal/serial/risk consumers; cannot create precedence or write derived values back to source layers.
Aliases: None admitted.
Disallowed or misleading use: Calendar truth; reference update; operational correction; trade decision.
Lifecycle: active_normative_derived_layer
Projection metadata: {"projection_status":"canonical","canonical_label":"Derived Runtime Calendar Context","canonical_slug":"derived_runtime_calendar_context","category":"carrier","stage_owner":"Calendar projection boundary","maps_to_contract":"docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:100-156","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Calendar truth","reference update","operational correction","trade decision"],"semantic_decision_refs":["PM-005:CTP-005"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Financial Calendar Reference Bundle
Definition: Typed selected bundle of checked calendar-reference artefacts, layer/version metadata and effective ranges used by import and projection; it is a carrier, not a fifth calendar business layer.
Scope: calendar reference carrier
Owner: Checked calendar-reference authority
Relationships: Carries Market Session Reference and/or Financial Event Reference artefacts; projection and operational state remain separate.
Aliases: None admitted.
Disallowed or misleading use: Event Calendar; operational calendar state; derived context; direct runtime authority from unchecked files.
Lifecycle: active_alpha_reference_carrier
Projection metadata: {"projection_status":"canonical","canonical_label":"Financial Calendar Reference Bundle","canonical_slug":"financial_calendar_reference_bundle","category":"reference_data","stage_owner":"calendar_reference","maps_to_contract":"ImportedReferenceBundle","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["derived context","direct runtime authority from unchecked files"],"semantic_decision_refs":["PM-005:CTP-006"],"machine_projection_omissions":["Event Calendar [canonical-token:event_calendar]","operational calendar state [canonical-token:operational_calendar_state]"],"audit_noncanonical_phrases":[]}

### Financial Calendar Crosswalk
Definition: Versioned deterministic mapping policy from admitted source event types to runtime tags, evaluation tags and projection targets without changing the source event fact.
Scope: calendar projection mapping policy
Owner: Calendar projection boundary
Relationships: Consumed during Derived Runtime Calendar Context projection; distinct from reference facts, import records and the broad financial calendar.
Aliases: None admitted.
Disallowed or misleading use: Financial calendar; source event truth; precedence rule by mapping alone.
Lifecycle: active_alpha_projection_policy
Projection metadata: {"projection_status":"canonical","canonical_label":"Financial Calendar Crosswalk","canonical_slug":"financial_calendar_crosswalk","category":"reference_data","stage_owner":"calendar_reference","maps_to_contract":"FinancialCalendarCrosswalkRecord","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["source event truth","precedence rule by mapping alone"],"semantic_decision_refs":["PM-005:CTP-007"],"machine_projection_omissions":["Financial calendar [contextual-disallowed-use only; broad architecture is canonical]"],"audit_noncanonical_phrases":[]}

### Financial Calendar Import Record
Definition: Audit/provenance record of one checked calendar reference import, identifying bundle/layer/artifact versions, validation outcome, writer and import lineage; it is not the imported reference fact itself.
Scope: calendar reference import audit
Owner: Checked calendar-reference authority
Relationships: Records construction/update of a Financial Calendar Reference Bundle; distinct from source facts, operational observations and projection context.
Aliases: None admitted.
Disallowed or misleading use: Reference truth; import service; packet ID as fact identity.
Lifecycle: active_semantic_reserved_implementation
Projection metadata: {"projection_status":"canonical","canonical_label":"Financial Calendar Import Record","canonical_slug":"financial_calendar_import_record","category":"reference_data","stage_owner":"calendar_reference","maps_to_contract":"FinancialCalendarImportRecord","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Reference truth","import service","packet ID as fact identity"],"semantic_decision_refs":["PM-005:CTP-008"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Source Temporal Standard
Definition: Repo-wide provider-agnostic authority defining source observation, repository capture, persistence, provider/channel and granularity fields above DMPV3 packet carriage.
Scope: repo-wide source temporal grammar
Owner: Technical architecture source-temporal authority
Relationships: Governs raw captures, reference/workbook specimens, persistence, replay and packets; distinct from packet emission metadata and calendar projection fields.
Aliases: None admitted.
Disallowed or misleading use: Source temporal standard field; source temporal standard surface; DMP timestamp standard.
Lifecycle: active_normative
Projection metadata: {"projection_status":"canonical","canonical_label":"Source Temporal Standard","canonical_slug":"source_temporal_standard","category":"authority_surface","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Source temporal standard field","source temporal standard surface","DMP timestamp standard"],"semantic_decision_refs":["PM-005:CTP-009"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["source temporal","source temporal standard requires"]}

### source_time_raw
Definition: Exact source-supplied temporal token preserved as captured from the source artefact.
Scope: Source Temporal Standard field
Owner: Technical architecture source-temporal authority
Relationships: Raw token for later interpretation; paired with source_time_kind, source_timezone_raw and any lawful normalised value.
Aliases: Source raw; source time.
Disallowed or misleading use: Raw source; parsed/normalised time presented as raw.
Lifecycle: active_normative_field
Projection metadata: {"projection_status":"canonical","canonical_label":"source_time_raw","canonical_slug":"source_time_raw","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard.source_time_raw","raw_or_derived":"not_applicable","allowed_aliases":["Source raw","source time"],"disallowed_phrases":["Raw source","parsed/normalised time presented as raw"],"semantic_decision_refs":["PM-005:CTP-010"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### source_time_kind
Definition: Declared kind of temporal truth carried by the source artefact, such as timestamp or date; it describes ontology, not precision alone.
Scope: Source Temporal Standard field
Owner: Technical architecture source-temporal authority
Relationships: Determines lawful interpretation of source_time_raw/source_time_utc/source_date; distinct from time_granularity.
Aliases: Source kind.
Disallowed or misleading use: Source type when non-temporal; granularity.
Lifecycle: active_normative_field
Projection metadata: {"projection_status":"canonical","canonical_label":"source_time_kind","canonical_slug":"source_time_kind","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard.source_time_kind","raw_or_derived":"not_applicable","allowed_aliases":["Source kind"],"disallowed_phrases":["Source type when non-temporal","granularity"],"semantic_decision_refs":["PM-005:CTP-011"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### source_timezone_raw
Definition: Source-supplied timezone or offset label exactly as declared by the source.
Scope: Source Temporal Standard field
Owner: Technical architecture source-temporal authority
Relationships: Used with source_time_raw to justify source_time_utc; may be absent where the source declares none.
Aliases: Source timezone.
Disallowed or misleading use: Repository timezone; inferred timezone without source authority.
Lifecycle: active_normative_field
Projection metadata: {"projection_status":"canonical","canonical_label":"source_timezone_raw","canonical_slug":"source_timezone_raw","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard.source_timezone_raw","raw_or_derived":"not_applicable","allowed_aliases":["Source timezone"],"disallowed_phrases":["Repository timezone","inferred timezone without source authority"],"semantic_decision_refs":["PM-005:CTP-012"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### source_time_utc
Definition: UTC-normalised source observation time only when lawful source time and timezone/offset truth exists.
Scope: Source Temporal Standard field
Owner: Technical architecture source-temporal authority
Relationships: Source observation truth; distinct from captured_at_utc, persisted_at_utc, packet emission time and derived runtime times.
Aliases: None admitted.
Disallowed or misleading use: Capture time; persistence time; invented timestamp for date-only source.
Lifecycle: active_normative_field
Projection metadata: {"projection_status":"canonical","canonical_label":"source_time_utc","canonical_slug":"source_time_utc","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard.source_time_utc","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Capture time","persistence time","invented timestamp for date-only source"],"semantic_decision_refs":["PM-005:CTP-013"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### source_date
Definition: Source observation date supplied or lawfully derived without inventing finer precision than the source supplied.
Scope: Source Temporal Standard field
Owner: Technical architecture source-temporal authority
Relationships: Authoritative for date-only sources; may coexist with source_time_utc where the contract permits.
Aliases: None admitted.
Disallowed or misleading use: Midnight UTC timestamp used to fake date precision.
Lifecycle: active_normative_field
Projection metadata: {"projection_status":"canonical","canonical_label":"source_date","canonical_slug":"source_date","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard.source_date","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Midnight UTC timestamp used to fake date precision"],"semantic_decision_refs":["PM-005:CTP-014"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### captured_at_utc
Definition: UTC process time when the repository or governed process captured/ingested the exact source artefact.
Scope: Source Temporal Standard field
Owner: Technical architecture source-temporal authority
Relationships: Distinct from source observation and persistence time; does not repair missing source time.
Aliases: None admitted.
Disallowed or misleading use: Observed time; event time; source time.
Lifecycle: active_normative_field
Projection metadata: {"projection_status":"canonical","canonical_label":"captured_at_utc","canonical_slug":"captured_at_utc","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard.captured_at_utc","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Observed time","event time"],"semantic_decision_refs":["PM-005:CTP-015"],"machine_projection_omissions":["source time [alias-token:source_time_raw]"],"audit_noncanonical_phrases":[]}

### persisted_at_utc
Definition: UTC process time when the repository persisted the record or artefact.
Scope: Source Temporal Standard field
Owner: Technical architecture source-temporal authority
Relationships: Distinct from source observation and capture time; records storage action only.
Aliases: None admitted.
Disallowed or misleading use: Observed time; capture time; source time.
Lifecycle: active_normative_field
Projection metadata: {"projection_status":"canonical","canonical_label":"persisted_at_utc","canonical_slug":"persisted_at_utc","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard.persisted_at_utc","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":[],"semantic_decision_refs":["PM-005:CTP-016"],"machine_projection_omissions":["Observed time [disallowed-token:captured_at_utc]","capture time [disallowed-token:source_time_utc]","source time [alias-token:source_time_raw]"],"audit_noncanonical_phrases":[]}

### source_provider
Definition: Upstream provider identity for the observed source artefact.
Scope: Source Temporal Standard field
Owner: Technical architecture source-temporal authority
Relationships: Names origin organisation/system; distinct from source_channel and from repository writer.
Aliases: None admitted.
Disallowed or misleading use: Packet source; repository module; inferred default provider.
Lifecycle: active_normative_field
Projection metadata: {"projection_status":"canonical","canonical_label":"source_provider","canonical_slug":"source_provider","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard.source_provider","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Packet source","repository module","inferred default provider"],"semantic_decision_refs":["PM-005:CTP-017"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### source_channel
Definition: Acquisition channel or provider-local lane through which the source artefact was obtained.
Scope: Source Temporal Standard field
Owner: Technical architecture source-temporal authority
Relationships: Qualifies source_provider; distinct from transport-independent domain owner.
Aliases: None admitted.
Disallowed or misleading use: Provider identity; packet source; generic channel without declared source.
Lifecycle: active_normative_field
Projection metadata: {"projection_status":"canonical","canonical_label":"source_channel","canonical_slug":"source_channel","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard.source_channel","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Provider identity","generic channel without declared source"],"semantic_decision_refs":["PM-005:CTP-018"],"machine_projection_omissions":["packet source [disallowed-token:source_provider]"],"audit_noncanonical_phrases":[]}

### time_granularity
Definition: Declared precision/granularity of source observation truth, such as date or timestamp, without upgrading the source’s precision.
Scope: Source Temporal Standard field
Owner: Technical architecture source-temporal authority
Relationships: Constrains lawful normalisation and comparison; distinct from source_time_kind.
Aliases: None admitted.
Disallowed or misleading use: Sampling frequency when it does not describe source temporal precision; inferred precision.
Lifecycle: active_normative_field
Projection metadata: {"projection_status":"canonical","canonical_label":"time_granularity","canonical_slug":"time_granularity","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"SourceTemporalStandard.time_granularity","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Sampling frequency when it does not describe source temporal precision","inferred precision"],"semantic_decision_refs":["PM-005:CTP-019"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### next_event_time_utc
Definition: UTC time of the next relevant admitted calendar event for a stated context/as-of calculation; a derived context field, not source observation time.
Scope: temporal context derived field
Owner: Calendar/temporal projection boundary
Relationships: Derived from Financial Event Reference and applicable operational facts; distinct from window boundaries and source_time_utc.
Aliases: None admitted.
Disallowed or misleading use: Source event observation time; capture time; guaranteed next event when completeness is unknown.
Lifecycle: active_alpha_derived_field
Projection metadata: {"projection_status":"canonical","canonical_label":"next_event_time_utc","canonical_slug":"next_event_time_utc","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"TemporalContextInput.next_event_time_utc","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Source event observation time","guaranteed next event when completeness is unknown"],"semantic_decision_refs":["PM-005:CTP-020"],"machine_projection_omissions":["capture time [disallowed-token:source_time_utc]"],"audit_noncanonical_phrases":[]}

### window_start_utc
Definition: Inclusive governed UTC start boundary of one temporal event/query window.
Scope: temporal window boundary
Owner: Temporal context contract owner
Relationships: Paired with window_end_utc; bounds selection/proximity and does not describe source observation, capture or persistence time.
Aliases: None admitted.
Disallowed or misleading use: Source start time unless the source contract says so; as-of time by implication.
Lifecycle: active_alpha_contract_field
Projection metadata: {"projection_status":"canonical","canonical_label":"window_start_utc","canonical_slug":"window_start_utc","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"TemporalEventWindow.window_start_utc","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Source start time unless the source contract says so","as-of time by implication"],"semantic_decision_refs":["PM-005:CTP-021"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### window_end_utc
Definition: Inclusive governed UTC end boundary of one temporal event/query window and must not precede its start.
Scope: temporal window boundary
Owner: Temporal context contract owner
Relationships: Paired with window_start_utc; does not describe source observation, capture or persistence time.
Aliases: None admitted.
Disallowed or misleading use: Source end time unless the source contract says so; persistence time.
Lifecycle: active_alpha_contract_field
Projection metadata: {"projection_status":"canonical","canonical_label":"window_end_utc","canonical_slug":"window_end_utc","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"TemporalEventWindow.window_end_utc","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Source end time unless the source contract says so"],"semantic_decision_refs":["PM-005:CTP-022"],"machine_projection_omissions":["persistence time [disallowed-token:source_time_utc]"],"audit_noncanonical_phrases":[]}

### runtime_bar_time_utc
Definition: Prepared-runtime UTC alignment time for the bar or observation selected from admitted source temporal data; it is derived preparation context, not source, capture or persistence time.
Scope: prepared runtime alignment field
Owner: Prepared ingress/runtime preparation authority
Relationships: Derived from admitted source temporal truth or an explicitly authorised runtime alignment input; consumed downstream without rewriting source fields.
Aliases: None admitted.
Disallowed or misleading use: source_time_utc; packet emission time; wall-clock now.
Lifecycle: active_alpha_derived_field
Projection metadata: {"projection_status":"canonical","canonical_label":"runtime_bar_time_utc","canonical_slug":"runtime_bar_time_utc","category":"protocol_field","stage_owner":"temporal_context","maps_to_contract":"PreparedRuntimeSnapshot.runtime_bar_time_utc","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["packet emission time","wall-clock now"],"semantic_decision_refs":["PM-005:CTP-023"],"machine_projection_omissions":["source_time_utc [canonical-token:source_time_utc]"],"audit_noncanonical_phrases":[]}

### Workbook Temporal Provenance
Definition: Rule that dates and times in the governed signal workbook are reference-ledger provenance, not same-moment live runtime capture by default.
Scope: workbook-specific temporal provenance
Owner: Governed signal-workbook authority
Relationships: Requires Field-level Provenance where rows blend source dates; distinct from general DMP provenance reserved to PM-006.
Aliases: None admitted.
Disallowed or misleading use: Live observation time; direct runtime authority; packet emission time.
Lifecycle: active_reference_provenance_rule
Projection metadata: {"projection_status":"canonical","canonical_label":"Workbook Temporal Provenance","canonical_slug":"workbook_temporal_provenance","category":"authority_surface","stage_owner":"temporal_context","maps_to_contract":"SignalWorkbookTemporalProvenanceRule","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["Live observation time","direct runtime authority"],"semantic_decision_refs":["PM-005:CTP-029"],"machine_projection_omissions":["packet emission time [disallowed-token:runtime_bar_time_utc]"],"audit_noncanonical_phrases":[]}

### Field-level Provenance
Definition: Per-field attribution of source artefact/location, source date/time and applicable version/lineage where fields in one record or workbook row derive from different source moments.
Scope: temporal/source provenance granularity
Owner: Owning source/preparation or workbook-promotion boundary
Relationships: Supports Source Temporal Standard and Workbook Temporal Provenance; distinct from general packet lineage and prevents false same-moment timestamps.
Aliases: None admitted.
Disallowed or misleading use: One row-level timestamp for mixed-date fields; packet lineage as source proof.
Lifecycle: active_normative_provenance_rule
Projection metadata: {"projection_status":"canonical","canonical_label":"Field-level Provenance","canonical_slug":"field_level_provenance","category":"authority_surface","stage_owner":"temporal_context","maps_to_contract":"SignalWorkbookTemporalProvenanceRule.field_level_provenance","raw_or_derived":"not_applicable","allowed_aliases":[],"disallowed_phrases":["One row-level timestamp for mixed-date fields","packet lineage as source proof"],"semantic_decision_refs":["PM-005:CTP-030"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["field level"]}

### DMP V3
Definition: Canonical version-3 Desk Module Packet protocol for normalising the outer carriage of live packetised inter-module outputs.
Scope: cross-stage packet-carriage protocol, not payload/domain authority
Owner: DMPV3 protocol authority
Relationships: Implemented by the canonical DmpV3Envelope and repo-owned packet helpers; payload contracts and docs/07 retain domain/runtime ownership.
Aliases: DMPV3.
Disallowed or misleading use: DMP V3 root; payload schema; event bus; module owner.
Lifecycle: active_normative_protocol
Projection metadata: {"projection_status":"canonical","canonical_label":"DMP V3","canonical_slug":"dmp_v3","category":"protocol","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope","raw_or_derived":"not_applicable","allowed_aliases":["DMPV3"],"disallowed_phrases":["DMP V3 root","payload schema","event bus","module owner"],"semantic_decision_refs":["PM-006:DIL-001"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### DmpV3Envelope
Definition: Typed contract surface representing the canonical DMPV3 outer envelope and its mandatory carriage fields.
Scope: protocol contract surface
Owner: DMPV3 protocol authority; implementation allocation in contracts/packets.py
Relationships: Concrete carrier of DMP V3; base for DmpV3Packet; distinct from payload data and from compatibility wrappers.
Aliases: DMPV3 envelope.
Disallowed or misleading use: generic event envelope; payload contract; source record.
Lifecycle: active_alpha_protocol_surface
Projection metadata: {"projection_status":"canonical","canonical_label":"DmpV3Envelope","canonical_slug":"dmp_v3_envelope","category":"protocol_surface","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope","raw_or_derived":"not_applicable","allowed_aliases":["DMPV3 envelope"],"disallowed_phrases":["generic event envelope","payload contract","source record"],"semantic_decision_refs":["PM-006:DIL-002"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### DmpV3Packet
Definition: Generic typed helper surface for carrying a typed payload through DmpV3Envelope.
Scope: repo-facing protocol helper
Owner: DMPV3 protocol implementation allocation
Relationships: Subclasses DmpV3Envelope; distinct from DeskModulePacketV3 and from a concrete emitted packet occurrence.
Aliases: DMPV3 packet.
Disallowed or misleading use: DMP V3; packet occurrence; DmpV3Envelope when class precision matters.
Lifecycle: active_alpha_protocol_helper
Projection metadata: {"projection_status":"canonical","canonical_label":"DmpV3Packet","canonical_slug":"dmp_v3_packet","category":"protocol_surface","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Packet","raw_or_derived":"not_applicable","allowed_aliases":["DMPV3 packet"],"disallowed_phrases":["DmpV3Envelope when class precision matters"],"semantic_decision_refs":["PM-006:DIL-003"],"machine_projection_omissions":["DMP V3 [canonical-token:dmp_v3]","packet occurrence [canonical-token:packet_occurrence]"],"audit_noncanonical_phrases":[]}

### DeskModulePacketV3
Definition: Typed repo helper for bounded live module payload carriage where a generic payload type is not statically retained.
Scope: module-packet helper surface
Owner: DMPV3 protocol implementation allocation
Relationships: Subclasses DmpV3Packet[Any]; it does not create a separate protocol, payload meaning or module authority.
Aliases: Desk module packet V3.
Disallowed or misleading use: canonical envelope; domain packet contract; proof of live module completion.
Lifecycle: active_alpha_protocol_helper
Projection metadata: {"projection_status":"canonical","canonical_label":"DeskModulePacketV3","canonical_slug":"desk_module_packet_v3","category":"protocol_surface","stage_owner":"cross_stage_protocol","maps_to_contract":"DeskModulePacketV3","raw_or_derived":"not_applicable","allowed_aliases":["Desk module packet V3"],"disallowed_phrases":["canonical envelope","domain packet contract","proof of live module completion"],"semantic_decision_refs":["PM-006:DIL-004"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### packetrole
Definition: Canonical outer-envelope field declaring the admitted packet-carriage role used to interpret one packet occurrence.
Scope: DMPV3 protocol field
Owner: Owning packet-role contract under DMPV3 protocol authority
Relationships: Works with producer.grammar_role, producer.behaviour_class and dataschema; cannot be inferred from payload shape.
Aliases: packet role.
Disallowed or misleading use: payload type; stage name; behaviour class; generic role.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"packetrole","canonical_slug":"packetrole","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope.packetrole","raw_or_derived":"not_applicable","allowed_aliases":["packet role"],"disallowed_phrases":["payload type","stage name","generic role"],"semantic_decision_refs":["PM-006:DIL-005"],"machine_projection_omissions":["behaviour class [alias-token:behaviour_class]"],"audit_noncanonical_phrases":[]}

### producer
Definition: Canonical outer-envelope block containing the bounded technical identity of the module instance that emitted the DMP data structure.
Scope: DMPV3 producer-identity carrier
Owner: Emitting module under DMPV3 producer-identity law
Relationships: Contains module_id, module_version, module_instance_id, grammar_role, behaviour_class and optional stage_name; distinct from packet source and external provider.
Aliases: DMP producer.
Disallowed or misleading use: external provider; packet source; payload owner when different.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"producer","canonical_slug":"producer","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope.producer","raw_or_derived":"not_applicable","allowed_aliases":["DMP producer"],"disallowed_phrases":["external provider","payload owner when different"],"semantic_decision_refs":["PM-006:DIL-006"],"machine_projection_omissions":["packet source [disallowed-token:source_provider]"],"audit_noncanonical_phrases":[]}

### lineage
Definition: Canonical DMPV3 block declaring typed causal, dependency, derivation, source-artifact, fingerprint and replay/review/decision relationships for one packet occurrence.
Scope: packet lineage carrier
Owner: Owning packet-role/domain contracts under DMPV3 lineage law
Relationships: Distinct from broad Provenance; each field has a bounded meaning and empty defaults do not prove absence.
Aliases: packet lineage; DMP lineage.
Disallowed or misleading use: provenance as an interchangeable synonym; arbitrary identifier bag; trace context.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"lineage","canonical_slug":"lineage","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope.lineage","raw_or_derived":"not_applicable","allowed_aliases":["packet lineage","DMP lineage"],"disallowed_phrases":["provenance as an interchangeable synonym","arbitrary identifier bag","trace context"],"semantic_decision_refs":["PM-006:DIL-007"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### validation
Definition: Canonical DMPV3 block recording role-specific packet-carriage checks, status and named violations for one emission boundary.
Scope: packet validation carriage
Owner: Owning packet-role validation contract and emitting boundary
Relationships: Distinct from source-data truth, domain correctness, trading validity and whole-system correctness; degraded carriage is lawful only where expressly allowed.
Aliases: packet validation.
Disallowed or misleading use: payload model validated; strategy valid; source verified; system green.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"validation","canonical_slug":"validation","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope.validation","raw_or_derived":"not_applicable","allowed_aliases":["packet validation"],"disallowed_phrases":["payload model validated","strategy valid","source verified","system green"],"semantic_decision_refs":["PM-006:DIL-008"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### summary
Definition: Canonical DMPV3 human-inspection block carrying headline, key flags and human state derived from already governed packet facts.
Scope: packet inspection summary
Owner: Emitting packet role, as a deterministic projection
Relationships: Subordinate to data, lineage and validation; material machine inputs must remain typed outside summary.
Aliases: packet summary.
Disallowed or misleading use: payload contract; decision authority; validation substitute; free-form source truth.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"summary","canonical_slug":"summary","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope.summary","raw_or_derived":"not_applicable","allowed_aliases":["packet summary"],"disallowed_phrases":["decision authority","validation substitute","free-form source truth"],"semantic_decision_refs":["PM-006:DIL-009"],"machine_projection_omissions":["payload contract [disallowed-token:dmp_v3_envelope]"],"audit_noncanonical_phrases":[]}

### dmpextensions
Definition: Canonical DMPV3 extension block for versioned, owned compatibility metadata whose name, type and consumer rule are admitted.
Scope: protocol compatibility extension carrier
Owner: DMPV3 extension authority for each admitted extension namespace
Relationships: Subordinate to canonical envelope and typed payload; unknown extensions may be preserved/ignored but not reinterpreted as authority.
Aliases: DMP extensions.
Disallowed or misleading use: payload overflow; hidden mandatory fields; arbitrary metadata; behavioural switch bag.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"dmpextensions","canonical_slug":"dmpextensions","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope.dmpextensions","raw_or_derived":"not_applicable","allowed_aliases":["DMP extensions"],"disallowed_phrases":["payload overflow","hidden mandatory fields","arbitrary metadata","behavioural switch bag"],"semantic_decision_refs":["PM-006:DIL-010"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### module_id
Definition: Producer field identifying the logical emitting module under the governed module namespace.
Scope: DMPV3 producer identity field
Owner: Emitting module owner
Relationships: Combines with module_version and module_instance_id; distinct from stage_name, grammar_role, behaviour_class and packet source.
Aliases: module ID.
Disallowed or misleading use: packet id; source id; stage name; class name inferred from payload.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"module_id","canonical_slug":"module_id","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Producer.module_id","raw_or_derived":"not_applicable","allowed_aliases":["module ID"],"disallowed_phrases":["packet id","source id","class name inferred from payload"],"semantic_decision_refs":["PM-006:DIL-011"],"machine_projection_omissions":["stage name [disallowed-token:packetrole]"],"audit_noncanonical_phrases":[]}

### module_version
Definition: Producer field identifying the governed version of the emitting module/executable meaning relevant to the packet.
Scope: DMPV3 producer version field
Owner: Emitting module owner and release/config authority
Relationships: Pairs with module_id and module_instance_id; distinct from protocol version, payload schema version and source artefact version.
Aliases: module version.
Disallowed or misleading use: dmpversion; specversion; dataschema version; source version.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"module_version","canonical_slug":"module_version","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Producer.module_version","raw_or_derived":"not_applicable","allowed_aliases":["module version"],"disallowed_phrases":["dmpversion","specversion","dataschema version","source version"],"semantic_decision_refs":["PM-006:DIL-012"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### module_instance_id
Definition: Producer field identifying the concrete admitted emitting instance within the module’s instance namespace.
Scope: DMPV3 concrete producer-instance identity
Owner: Concrete emitting-module instance owner
Relationships: More specific than module_id; distinct from packet source, process id unless contract says so, and packet occurrence id.
Aliases: module instance ID.
Disallowed or misleading use: packet id; process id by assumption; module_id::default as governed identity.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"module_instance_id","canonical_slug":"module_instance_id","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Producer.module_instance_id","raw_or_derived":"not_applicable","allowed_aliases":["module instance ID"],"disallowed_phrases":["process id by assumption","module_id::default as governed identity"],"semantic_decision_refs":["PM-006:DIL-013"],"machine_projection_omissions":["packet id [disallowed-token:module_id]"],"audit_noncanonical_phrases":["module instance"]}

### grammar_role
Definition: Producer field declaring the packet emitter’s admitted grammatical role in the packetised workflow.
Scope: DMPV3 producer classification field
Owner: Owning packet-role/module contract
Relationships: Used with packetrole, behaviour_class and dataschema; distinct from stage name and logical module identity.
Aliases: grammar role.
Disallowed or misleading use: packet role; stage; payload class inferred from shape.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"grammar_role","canonical_slug":"grammar_role","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Producer.grammar_role","raw_or_derived":"not_applicable","allowed_aliases":["grammar role"],"disallowed_phrases":["stage","payload class inferred from shape"],"semantic_decision_refs":["PM-006:DIL-014"],"machine_projection_omissions":["packet role [alias-token:packetrole]"],"audit_noncanonical_phrases":[]}

### behaviour_class
Definition: Producer field declaring the bounded behaviour class of the emitted output for packet interpretation.
Scope: DMPV3 producer classification field
Owner: Owning module/packet-role contract
Relationships: Works with packetrole, grammar_role and dataschema; does not grant runtime/domain ownership.
Aliases: behaviour class.
Disallowed or misleading use: module type; packetrole; strategy class inferred from payload.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"behaviour_class","canonical_slug":"behaviour_class","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Producer.behaviour_class","raw_or_derived":"not_applicable","allowed_aliases":["behaviour class"],"disallowed_phrases":["module type","strategy class inferred from payload"],"semantic_decision_refs":["PM-006:DIL-015"],"machine_projection_omissions":["packetrole [canonical-token:packetrole]"],"audit_noncanonical_phrases":[]}

### traceid
Definition: Outer-envelope execution-context field identifying the admitted correlation trace spanning related packet occurrences.
Scope: DMPV3 trace-context identity
Owner: Trace-context boundary
Relationships: Distinct from lineage.parentids, packet id, runid and scenarioid; must be propagated, not derived from packet id.
Aliases: trace ID.
Disallowed or misleading use: packet id; parent id; run id; random correlation substitute for missing domain identity.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"traceid","canonical_slug":"traceid","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope.traceid","raw_or_derived":"not_applicable","allowed_aliases":["trace ID"],"disallowed_phrases":["parent id","random correlation substitute for missing domain identity"],"semantic_decision_refs":["PM-006:DIL-016"],"machine_projection_omissions":["packet id [disallowed-token:module_id]","run id [alias-token:runid]"],"audit_noncanonical_phrases":[]}

### runid
Definition: Outer-envelope execution-context field identifying one governed execution or replay run.
Scope: DMPV3 run identity
Owner: Execution/replay run boundary
Relationships: Distinct from traceid, scenarioid, packet occurrence and module instance; one run may contain multiple traces and packets.
Aliases: run ID.
Disallowed or misleading use: packet id; trace id; scenario id; wall-clock timestamp.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"runid","canonical_slug":"runid","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope.runid","raw_or_derived":"not_applicable","allowed_aliases":["run ID"],"disallowed_phrases":["wall-clock timestamp"],"semantic_decision_refs":["PM-006:DIL-017"],"machine_projection_omissions":["packet id [disallowed-token:module_id]","trace id [alias-token:traceid]","scenario id [alias-token:scenarioid]"],"audit_noncanonical_phrases":[]}

### scenarioid
Definition: Outer-envelope execution-context field identifying the governed scenario/specimen/operating context for the occurrence.
Scope: DMPV3 scenario identity
Owner: Scenario/specimen/operating-context owner
Relationships: Distinct from runid, traceid, packetrole and generic live mode; absence/default law is role-specific.
Aliases: scenario ID.
Disallowed or misleading use: live; run id; trace id; environment string without admitted contract.
Lifecycle: active_normative_protocol_field
Projection metadata: {"projection_status":"canonical","canonical_label":"scenarioid","canonical_slug":"scenarioid","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Envelope.scenarioid","raw_or_derived":"not_applicable","allowed_aliases":["scenario ID"],"disallowed_phrases":["live","environment string without admitted contract"],"semantic_decision_refs":["PM-006:DIL-018"],"machine_projection_omissions":["run id [alias-token:runid]","trace id [alias-token:traceid]"],"audit_noncanonical_phrases":[]}

### Dependency Packet IDs
Definition: Human concept for the identities carried in DmpV3Lineage.dependencyids: explicitly consumed material dependencies, including packets or other governed records, that are not represented as immediate causal parent packet occurrences.
Scope: DMPV3 dependency-lineage field meaning
Owner: Owning packet-role/domain contract
Relationships: Distinct from parentids and from generic packet IDs; may include non-packet governed dependency identities where the role contract permits.
Aliases: dependencyids; dependency packet identifiers.
Disallowed or misleading use: packet ids; parent ids; all upstream ids; arbitrary dependency names.
Lifecycle: active_normative_protocol_concept
Projection metadata: {"projection_status":"canonical","canonical_label":"Dependency Packet IDs","canonical_slug":"dependency_packet_ids","category":"protocol_field","stage_owner":"cross_stage_protocol","maps_to_contract":"DmpV3Lineage.dependencyids","raw_or_derived":"not_applicable","allowed_aliases":["dependencyids","dependency packet identifiers"],"disallowed_phrases":["packet ids","parent ids","all upstream ids","arbitrary dependency names"],"semantic_decision_refs":["PM-006:DIL-019"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["dependency packet"]}

### Packet Occurrence
Definition: One emitted DMPV3 carriage instance, uniquely identified within its packet source context by the source and id pair.
Scope: packet-occurrence identity concept
Owner: DMPV3 packet-emission boundary
Relationships: Distinct from protocol/class names, producer instance, upstream source/domain object, preserved original, trace, run and scenario.
Aliases: packet occurrence; DMP packet occurrence.
Disallowed or misleading use: packet id alone; source artefact; event; domain object; producer instance.
Lifecycle: active_normative_identity_concept
Projection metadata: {"projection_status":"canonical","canonical_label":"Packet Occurrence","canonical_slug":"packet_occurrence","category":"protocol_surface","stage_owner":"DMPV3 packet-emission boundary","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:11-23,114-130; docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:161-177","raw_or_derived":"not_applicable","allowed_aliases":["DMP packet occurrence"],"disallowed_phrases":["packet id alone","source artefact","event","domain object","producer instance"],"semantic_decision_refs":["PM-006:DIL-020"],"machine_projection_omissions":["packet occurrence [canonical-token:packet_occurrence]"],"audit_noncanonical_phrases":[]}

### Provenance
Definition: Governed evidence describing where a claim, artefact, field, packet or decision came from, which owner/source supplied it, and the material lineage or transformations needed to interpret it.
Scope: cross-domain origin and evidence concept
Owner: The owner of the underlying evidence/claim, with vocabulary governance over the term
Relationships: Broader than DMP lineage and Field-level Provenance; donor path/line/evidence-type is a bounded migration form; does not itself confer target or runtime authority.
Aliases: evidence provenance.
Disallowed or misleading use: lineage as an exact synonym; receipt; historical fact as authority; donor path alone for all provenance.
Lifecycle: active_normative_cross_domain_concept
Projection metadata: {"projection_status":"canonical","canonical_label":"Provenance","canonical_slug":"provenance","category":"authority_class","stage_owner":"The owner of the underlying evidence/claim, with vocabulary governance over the term","maps_to_contract":"docs/03.1_DOMAIN_MODEL_WORKING.md:21-55,77-87; docs/09.1_DMPV3_PROTOCOL_WORKING.md:43-70; docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:138-159","raw_or_derived":"not_applicable","allowed_aliases":["evidence provenance"],"disallowed_phrases":["lineage as an exact synonym","receipt","historical fact as authority","donor path alone for all provenance"],"semantic_decision_refs":["PM-006:DIL-021"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Raw Signal Families
Definition: Governed upstream families of admitted raw/source evidence retained with source identity, capture limitations and lineage before runtime preparation. Scope: source-boundary evidence families only.
Scope: before ordered runtime step 1; Supplies evidence to preparation before the six-stage spine; is not part of the spine.
Owner: source-family contracts and ingress/raw-capture boundary
Relationships: Upstream of Prepared Ingress; may be translated into typed candidates but is not Prepared Ingress, Runtime Context, a cognition stage or packet carriage.
Aliases: raw signal family
Disallowed or misleading uses: prepared runtime truth; runtime context; generic payload; cognition decision
Lifecycle: active_normative_domain_term
Projection metadata: {"projection_status":"canonical","canonical_label":"Raw Signal Families","canonical_slug":"raw_signal_families","category":"authority_surface","stage_owner":"upstream_raw_signal","maps_to_contract":"RawSignalFamilyCoverage","raw_or_derived":"not_applicable","allowed_aliases":["raw signal family"],"disallowed_phrases":["prepared runtime truth","generic payload","cognition decision"],"semantic_decision_refs":["PM-007:SSC-001"],"machine_projection_omissions":["runtime context [canonical-token:runtime_context]"],"audit_noncanonical_phrases":["5.3 raw signal families","raw signal"]}

### Prepared Ingress
Definition: Governed preparation seam that validates, resolves and maps admitted upstream truth into typed cognition inputs and their lineage. Scope: preparation-to-cognition boundary.
Scope: ordered runtime step 1, before calendar projection and serial stage 1; Creates the lawful inputs consumed by the spine; is structurally upstream and outside the six stages.
Owner: runtime preparation and cognition-ingress authority
Relationships: Consumes Raw Signal Families; emits Stage Input Bundle/common context; precedes Runtime Context and all six serial stages; cannot reassign source meaning or make stage decisions.
Aliases: cognition ingress; runtime preparation
Disallowed or misleading uses: runtime decision engine; temporal stage; candidate builder; capital gate
Lifecycle: active_normative_preparation_seam
Projection metadata: {"projection_status":"canonical","canonical_label":"Prepared Ingress","canonical_slug":"prepared_ingress","category":"authority_surface","stage_owner":"prepared_ingress","maps_to_contract":"PreparedRuntimeContextBuilder","raw_or_derived":"not_applicable","allowed_aliases":["cognition ingress","runtime preparation"],"disallowed_phrases":["runtime decision engine","candidate builder","capital gate"],"semantic_decision_refs":["PM-007:SSC-002"],"machine_projection_omissions":["temporal stage [alias-token:temporal_context]"],"audit_noncanonical_phrases":[]}

### Runtime Context
Definition: Governed umbrella term for immutable prepared facts, references and bounded runtime substrate available to lawful consumers. Scope: runtime information carriage, not a decision or stage.
Scope: available after preparation; consumed across ordered runtime steps as lawfully typed; Supplies bounded context to stages without joining the six-stage order as an owner.
Owner: the owners of each contained fact and carrier; no independent Runtime Context decision owner
Relationships: Produced through Prepared Ingress and consumed through typed carriers; broader than any one stage input but must not become an untyped dictionary or hidden authority.
Aliases: prepared runtime context
Disallowed or misleading uses: global mutable context; decision owner; generic metadata bag; stage output
Lifecycle: active_normative_carrier_term
Projection metadata: {"projection_status":"canonical","canonical_label":"Runtime Context","canonical_slug":"runtime_context","category":"carrier","stage_owner":"prepared_ingress","maps_to_contract":"PreparedRuntimeSnapshot","raw_or_derived":"not_applicable","allowed_aliases":["prepared runtime context"],"disallowed_phrases":["global mutable context","decision owner","generic metadata bag","stage output"],"semantic_decision_refs":["PM-007:SSC-003"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["ithout runtime context","pared runtime context","project runtime context","runtime context preparation"]}

### Temporal Context
Definition: First serial stage that interprets admitted temporal/calendar facts into bounded temporal phase, event-window and timing context. Scope: temporal interpretation for downstream cognition.
Scope: serial stage 1 of 6; ordered runtime step 3; Stage 1 contributes one bounded output to candidate formation; it is not the whole spine.
Owner: Temporal Context stage authority
Relationships: Consumes temporal input from Stage Input Bundle/calendar projection; emits TemporalContextOutput; precedes every other serial stage and remains distinct from calendar reference authority.
Aliases: temporal stage
Disallowed or misleading uses: calendar authority; regime stage; time of day as complete cognition; capital timing gate
Lifecycle: active_normative_serial_stage
Projection metadata: {"projection_status":"canonical","canonical_label":"Temporal Context","canonical_slug":"temporal_context","category":"stage","stage_owner":"temporal_context","maps_to_contract":"TemporalContextOutput","raw_or_derived":"not_applicable","allowed_aliases":["temporal stage"],"disallowed_phrases":["calendar authority","regime stage","time of day as complete cognition","capital timing gate"],"semantic_decision_refs":["PM-007:SSC-004"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["temporal context seq5","temporal context service","temporal event context"]}

### Market Regime Context
Definition: Second serial stage that interprets admitted market facts into bounded regime context. Scope: market-regime classification and supporting evidence for later stages.
Scope: serial stage 2 of 6; ordered runtime step 4; Stage 2 contributes regime context to later candidate formation; it cannot absorb earlier/later jobs.
Owner: Market Regime Context stage authority
Relationships: Consumes its typed regime input and lawful earlier context; emits MarketRegimeContextOutput; distinct from raw market data, posture permission and capital risk.
Aliases: regime context stage
Disallowed or misleading uses: market data feed; posture decision; parallel risk; capital regime override
Lifecycle: active_normative_serial_stage
Projection metadata: {"projection_status":"canonical","canonical_label":"Market Regime Context","canonical_slug":"market_regime_context","category":"stage","stage_owner":"market_regime_context","maps_to_contract":"MarketRegimeContextOutput","raw_or_derived":"not_applicable","allowed_aliases":["regime context stage"],"disallowed_phrases":["market data feed","posture decision","capital regime override"],"semantic_decision_refs":["PM-007:SSC-005"],"machine_projection_omissions":["parallel risk [alias-token:parallel_risk_lane]"],"audit_noncanonical_phrases":["market context","market regime","regime context"]}

### Options and Flow Context
Definition: Third serial stage that converts admitted options and flow inputs into bounded contextual interpretation for candidate formation. Scope: options/flow context, not source capture or execution.
Scope: serial stage 3 of 6; ordered runtime step 5; Stage 3 contributes options/flow context to later candidate formation; it remains one stage only.
Owner: Options and Flow Context stage authority
Relationships: Consumes typed options-flow input and lawful prior context; emits OptionsFlowContextOutput; distinct from raw options data, posture, expression and broker execution.
Aliases: options-flow context stage
Disallowed or misleading uses: options feed; order flow execution; posture permission; broker flow
Lifecycle: active_normative_serial_stage
Projection metadata: {"projection_status":"canonical","canonical_label":"Options and Flow Context","canonical_slug":"options_and_flow_context","category":"stage","stage_owner":"options_flow_context","maps_to_contract":"OptionsFlowContextOutput","raw_or_derived":"not_applicable","allowed_aliases":["options-flow context stage"],"disallowed_phrases":["options feed","order flow execution","posture permission","broker flow"],"semantic_decision_refs":["PM-007:SSC-006"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["options flow context"]}

### Posture and Risk Permission
Definition: Fourth serial stage that determines the bounded posture and permission state available to later candidate formation. Scope: serial posture/permission only.
Scope: serial stage 4 of 6; ordered runtime step 6; Stage 4 constrains candidate formation; it neither replaces nor consumes the independent lane by implication.
Owner: Posture and Risk Permission stage authority
Relationships: Consumes lawful temporal/regime/options context; emits PostureRiskOutput; distinct from the independent Parallel Risk Lane, final risk, capital deployment and position sizing.
Aliases: posture permission stage
Disallowed or misleading uses: parallel risk; final risk; capital permission; position sizing
Lifecycle: active_normative_serial_stage
Projection metadata: {"projection_status":"canonical","canonical_label":"Posture and Risk Permission","canonical_slug":"posture_and_risk_permission","category":"stage","stage_owner":"posture_risk_permission","maps_to_contract":"PostureRiskPermissionOutput","raw_or_derived":"not_applicable","allowed_aliases":["posture permission stage"],"disallowed_phrases":["final risk","capital permission","position sizing"],"semantic_decision_refs":["PM-007:SSC-007"],"machine_projection_omissions":["parallel risk [alias-token:parallel_risk_lane]"],"audit_noncanonical_phrases":["posture and risk","posture risk permission"]}

### Playbook Eligibility
Definition: Fifth serial stage that determines which governed playbook families or setup variants are eligible under the formed context and posture. Scope: eligibility decision only.
Scope: serial stage 5 of 6; ordered runtime step 7; Stage 5 narrows lawful candidate expressions before stage 6; it is not the library itself.
Owner: Playbook Eligibility stage authority
Relationships: Consumes posture/context and library metadata; emits PlaybookEligibilityOutput; Playbook Library owns definitions, while this stage owns eligibility.
Aliases: eligibility stage
Disallowed or misleading uses: playbook library; playbook implementation; strategy selection with hidden capital authority
Lifecycle: active_normative_serial_stage
Projection metadata: {"projection_status":"canonical","canonical_label":"Playbook Eligibility","canonical_slug":"playbook_eligibility","category":"stage","stage_owner":"playbook_eligibility","maps_to_contract":"PlaybookEligibilityOutput","raw_or_derived":"not_applicable","allowed_aliases":["eligibility stage"],"disallowed_phrases":["playbook implementation","strategy selection with hidden capital authority"],"semantic_decision_refs":["PM-007:SSC-008"],"machine_projection_omissions":["playbook library [canonical-token:playbook_library]"],"audit_noncanonical_phrases":["compile playbook eligibility","evaluate playbook eligibility","playbook eligibility service"]}

### Expression and Execution
Definition: Sixth serial stage that forms the candidate execution expression, lifecycle intent and bounded downstream handoff material. Scope: candidate formation before pre-deployment.
Scope: serial stage 6 of 6; ordered runtime step 8; Final stage of the six-stage spine; completes candidate material but does not authorise fresh capital.
Owner: Expression and Execution stage authority
Relationships: Consumes all lawful prior stage outputs and eligibility; emits ExecutionExpressionOutput/StageLocalHandoffSurface; distinct from placement readiness, broker submission, fills and live state.
Aliases: execution-expression stage; expression stage
Disallowed or misleading uses: broker execution; order placement; fill handling; placement readiness; live inventory
Lifecycle: active_normative_serial_stage
Projection metadata: {"projection_status":"canonical","canonical_label":"Expression and Execution","canonical_slug":"expression_and_execution","category":"stage","stage_owner":"expression_execution","maps_to_contract":"ExpressionExecutionOutput","raw_or_derived":"not_applicable","allowed_aliases":["execution-expression stage","expression stage","execution expression"],"disallowed_phrases":["broker execution","order placement","fill handling","live inventory"],"semantic_decision_refs":["PM-007:SSC-009"],"machine_projection_omissions":["placement readiness [canonical-token:placement_readiness]"],"audit_noncanonical_phrases":["execution expression","expression execution"]}

### Serial Desk-cognition Spine
Definition: Governed structural term for the mandatory ordered six-stage candidate-formation spine. Scope: stage ordering, lawful dependencies and collective candidate formation.
Scope: ordered runtime steps 3-8 collectively; Is the structural spine itself, not a seventh stage and not an alias for Serial Candidate.
Owner: serial desk-cognition authority
Relationships: Comprises six distinct stage owners; consumes prepared inputs and forms Serial Candidate; distinct from Parallel Risk Lane, pre-deployment and capital authority.
Aliases: Serial Desk-cognition; serial cognition spine
Disallowed or misleading uses: single monolithic stage; orchestrator authority; end-to-end trading workflow
Lifecycle: active_normative_architecture_term
Projection metadata: {"projection_status":"canonical","canonical_label":"Serial Desk-cognition Spine","canonical_slug":"serial_desk_cognition_spine","category":"workflow","stage_owner":"serial_desk_cognition","maps_to_contract":"SerialDeskCognitionPacket","raw_or_derived":"not_applicable","allowed_aliases":["Serial Desk-cognition","serial cognition spine"],"disallowed_phrases":["single monolithic stage","orchestrator authority","end-to-end trading workflow"],"semantic_decision_refs":["PM-007:SSC-010","PM-007:SSC-015"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["desk cognition","serial desk cognition authority","serial desk cognition behaviour","serial desk cognition output"]}

### Serial Candidate
Definition: Governed carrier for candidate material formed after all six serial stages and before downstream pre-deployment and capital authority. Scope: candidate state and trace only.
Scope: after serial stage 6 and before ordered runtime step 9; Is the output of the spine, not the spine itself and not the Capital Deployment Decision.
Owner: serial desk-cognition authority for formation; downstream consumers are read-only
Relationships: Result of Serial Desk-cognition; input to pre-deployment and capital authority; may be blocked or declined downstream without changing its historical identity.
Aliases: formed candidate; candidate material
Disallowed or misleading uses: capital decision; authorised position; order; live position
Lifecycle: active_normative_carrier_term
Projection metadata: {"projection_status":"canonical","canonical_label":"Serial Candidate","canonical_slug":"serial_candidate","category":"carrier","stage_owner":"serial_desk_cognition","maps_to_contract":"serial_candidate_id","raw_or_derived":"not_applicable","allowed_aliases":["formed candidate","candidate material"],"disallowed_phrases":["authorised position","order"],"semantic_decision_refs":["PM-007:SSC-011"],"machine_projection_omissions":["capital decision [alias-token:capital_deployment_decision]","live position [canonical-token:live_position]"],"audit_noncanonical_phrases":["serial candidate 001","serial candidate 002","serial candidate 003","serial candidate 004","serial candidate 005","serial candidate 006","serial candidate 007","serial candidate 008","serial candidate eligible","serial candidate id","serial candidate rebuild","serial candidate row039","serial candidate row041","serial candidate row042","serial candidate seq9"]}

### Capital Deployment Decision
Definition: Governed downstream decision and receipt meaning for no-trade/reduce/continue/block action, authorised deployable percentage and bounded notional. Scope: fresh-capital deployment authority only.
Scope: ordered runtime step 10, after pre-deployment and before opening; Consumes but never rewrites the Serial Candidate; remains downstream of the six-stage spine.
Owner: capital deployment authority
Relationships: Consumes Serial Candidate, pre-deployment/final-risk/capital-state/policy truth; precedes opening; distinct from candidate formation, placement and live inventory.
Aliases: capital decision; deployment decision
Disallowed or misleading uses: serial candidate; opening authorisation; placement readiness; broker order; position sizing by confidence
Lifecycle: active_normative_downstream_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"Capital Deployment Decision","canonical_slug":"capital_deployment_decision","category":"authority_surface","stage_owner":"downstream_capital_deployment","maps_to_contract":"CapitalDeploymentDecision","raw_or_derived":"not_applicable","allowed_aliases":["capital decision","deployment decision"],"disallowed_phrases":["opening authorisation","broker order","position sizing by confidence"],"semantic_decision_refs":["PM-007:SSC-012"],"machine_projection_omissions":["serial candidate [canonical-token:serial_candidate]","placement readiness [canonical-token:placement_readiness]"],"audit_noncanonical_phrases":["capital deployment","capital deployment decision dataschema","capital deployment decision emitted","capital deployment decision seq9"]}

### Stage Input Bundle
Definition: Generic typed preparation-to-serial seam carrier that groups immutable common-stage context and admitted stage-specific input carriers. Scope: cognition-ingress output carriage.
Scope: pre-serial preparation-to-stage dispatch seam; Feeds the six-stage spine but is neither a stage-specific family nor an alias for the spine/Runtime Context.
Owner: cognition ingress owns bundle construction; contained facts retain their semantic owners
Relationships: Emitted by Prepared Ingress and consumed by stage owners; related to Runtime Context but narrower and typed; current alpha class carries only temporal/regime/options-flow inputs and does not prove complete six-stage coverage.
Aliases: stage-input bundle; cognition ingress bundle
Disallowed or misleading uses: runtime context as exact synonym; stage output; complete serial spine; generic dictionary
Lifecycle: active_normative_carrier_with_alpha_implementation_gap
Projection metadata: {"projection_status":"canonical","canonical_label":"Stage Input Bundle","canonical_slug":"stage_input_bundle","category":"carrier","stage_owner":"cognition_ingress","maps_to_contract":"StageInputBundle","raw_or_derived":"not_applicable","allowed_aliases":["stage-input bundle","cognition ingress bundle"],"disallowed_phrases":["runtime context as exact synonym","complete serial spine","generic dictionary"],"semantic_decision_refs":["PM-007:SSC-013"],"machine_projection_omissions":["stage output [disallowed-token:runtime_context]"],"audit_noncanonical_phrases":["stage input","stage input bundle json"]}

### Opening Architecture
Definition: Governed downstream architecture for opening authorisation, placement-readiness evaluation and non-executing handoff after bounded capital deployment. Scope: row 5.12 structure and owned outputs.
Scope: architecture; Capital-authorised candidate -> bounded opening/readiness structure -> protocol-only handoff.
Owner: downstream opening authority
Relationships: Contains Downstream Opening, Placement Readiness and Placement Handoff; may expose Broker Protocol context but is not broker execution, live position or inventory architecture.
Aliases: opening architecture and placement readiness
Disallowed or misleading uses: capital deployment authority; broker execution architecture; entry order; live inventory
Lifecycle: provisional_thin_seam
Projection metadata: {"projection_status":"canonical","canonical_label":"Opening Architecture","canonical_slug":"opening_architecture","category":"authority_surface","stage_owner":"downstream_opening","maps_to_contract":"DownstreamOpeningService","raw_or_derived":"not_applicable","allowed_aliases":["opening architecture and placement readiness"],"disallowed_phrases":["broker execution architecture","entry order"],"semantic_decision_refs":["PM-008:OPC-001"],"machine_projection_omissions":["capital deployment authority [disallowed-token:live_paper_historical_evaluation_separation]","live inventory [disallowed-token:expression_and_execution]"],"audit_noncanonical_phrases":["stream opening architecture"]}

### Downstream Opening
Definition: Governed authority surface that converts admitted capital-authority output and candidate seam truth into an opening snapshot/authorisation state. Scope: opening state before placement readiness and execution.
Scope: decision/authority surface; Capital-authorised candidate -> preserved opening authorisation/snapshot -> readiness assessment.
Owner: downstream opening authority
Relationships: Part of Opening Architecture; feeds Placement Readiness; distinct from Capital Deployment Decision, Placement Handoff, broker submission and Live Position creation.
Aliases: opening authority surface
Disallowed or misleading uses: capital deployment decision; order opening; position opening; broker placement
Lifecycle: provisional_thin_seam
Projection metadata: {"projection_status":"canonical","canonical_label":"Downstream Opening","canonical_slug":"downstream_opening","category":"authority_surface","stage_owner":"downstream_opening","maps_to_contract":"DownstreamOpeningSnapshot","raw_or_derived":"not_applicable","allowed_aliases":["opening authority surface"],"disallowed_phrases":["order opening","position opening","broker placement"],"semantic_decision_refs":["PM-008:OPC-002"],"machine_projection_omissions":["capital deployment decision [canonical-token:capital_deployment_decision]"],"audit_noncanonical_phrases":["downstream opening service"]}

### Placement Readiness
Definition: Governed non-executing readiness state that evaluates capital-authority output, candidate identity and placement constraints at a protocol-only broker boundary. Scope: ready/blocked result and trace.
Scope: readiness state; Opening authorisation -> blocked or ready-for-protocol-handoff; no broker state transition occurs.
Owner: downstream opening authority
Relationships: Consumes Downstream Opening/capital truth and may emit Placement Handoff only when ready; distinct from Broker Protocol implementation and order authority.
Aliases: placement-readiness result
Disallowed or misleading uses: placement authorisation; order permission; broker ready; execution approval
Lifecycle: provisional_thin_seam
Projection metadata: {"projection_status":"canonical","canonical_label":"Placement Readiness","canonical_slug":"placement_readiness","category":"authority_surface","stage_owner":"downstream_opening","maps_to_contract":"PlacementReadinessResult","raw_or_derived":"not_applicable","allowed_aliases":["placement-readiness result"],"disallowed_phrases":["placement authorisation","order permission","broker ready","execution approval"],"semantic_decision_refs":["PM-008:OPC-003"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["evaluate placement readiness","placement readiness 001","placement readiness id"]}

### Placement Handoff
Definition: Governed non-executing carrier containing bounded order-intent preview and trace after Placement Readiness. Scope: adapter-neutral handoff material only.
Scope: handoff carrier; Ready state -> protocol-only transfer material -> future separately authorised broker boundary.
Owner: downstream opening authority owns handoff construction; a future execution bridge may consume it
Relationships: Output of ready Placement Readiness; consumed by Broker Protocol/execution bridge; distinct from broker adapter, submission, execution receipt, fill and Live Position state.
Aliases: placement-handoff material
Disallowed or misleading uses: broker order; execution request; placement receipt; broker protocol
Lifecycle: provisional_protocol_only_carrier
Projection metadata: {"projection_status":"canonical","canonical_label":"Placement Handoff","canonical_slug":"placement_handoff","category":"carrier","stage_owner":"downstream_opening","maps_to_contract":"PlacementHandoffMaterial","raw_or_derived":"not_applicable","allowed_aliases":["placement-handoff material"],"disallowed_phrases":["execution request","placement receipt"],"semantic_decision_refs":["PM-008:OPC-004"],"machine_projection_omissions":["broker order [disallowed-token:capital_deployment_decision]","broker protocol [canonical-token:broker_protocol]"],"audit_noncanonical_phrases":[]}

### Broker Protocol
Definition: Governed protocol-boundary term for broker-facing message shape, constraints and mode while concrete adapter selection, credentials, submission and receipts remain separately owned. Scope: protocol semantics only.
Scope: protocol; Protocol-only handoff -> future validated adapter interaction -> separately owned execution receipt/state feedback.
Owner: execution-bridge/broker-boundary protocol authority; no concrete operational writer admitted here
Relationships: Consumes Placement Handoff at a future authorised seam; distinct from the handoff carrier, broker adapter implementation, order placement and execution receipt.
Aliases: broker-boundary protocol; protocol-only broker boundary
Disallowed or misleading uses: broker adapter; broker API; order execution; placement handoff
Lifecycle: reserved_protocol_boundary
Projection metadata: {"projection_status":"canonical","canonical_label":"Broker Protocol","canonical_slug":"broker_protocol","category":"protocol","stage_owner":"downstream_opening","maps_to_contract":"BrokerBoundaryMode","raw_or_derived":"not_applicable","allowed_aliases":["broker-boundary protocol","protocol-only broker boundary"],"disallowed_phrases":["broker adapter","broker API","order execution"],"semantic_decision_refs":["PM-008:OPC-005"],"machine_projection_omissions":["placement handoff [canonical-token:placement_handoff]"],"audit_noncanonical_phrases":["broker protocol only"]}

### Live Position
Definition: Governed per-position state representing one open or lifecycle-tracked position and its declared source evidence after entry. Scope: one position identity and state record.
Scope: live state; Lawful execution/state evidence -> open position state -> updates/monitoring -> exit/close consumption -> eventual closure state.
Owner: position-state authority through its repository contract
Relationships: Contained and read by Inventory Architecture; input to Exit Architecture; distinct from opening/readiness/handoff, inventory aggregate, exit decision and close completion.
Aliases: live position state; open-position state
Disallowed or misleading uses: opening authorisation; inventory; order; candidate; close state
Lifecycle: provisional_thin_seam_non_durable_alpha
Projection metadata: {"projection_status":"canonical","canonical_label":"Live Position","canonical_slug":"live_position","category":"authority_surface","stage_owner":"live_inventory","maps_to_contract":"LivePositionSnapshot","raw_or_derived":"not_applicable","allowed_aliases":["live position state","open-position state"],"disallowed_phrases":["inventory","candidate","close state"],"semantic_decision_refs":["PM-008:OPC-006"],"machine_projection_omissions":["opening authorisation [disallowed-token:capital_deployment_decision]","order [disallowed-token:serial_candidate]"],"audit_noncanonical_phrases":["live position management"]}

### Inventory Architecture
Definition: Governed row-5.13 architecture for identifier-keyed position state, inventory snapshots, declared exposure, capital-state reads and receipts. Scope: aggregate live-inventory structure after entry.
Scope: inventory owner/architecture; Entered/fill evidence -> reconciled per-position state -> aggregate inventory/exposure snapshot -> exit/review consumers.
Owner: live inventory authority together with bounded position and capital-state authorities
Relationships: Aggregates Live Position states and lawful capital/exposure facts; supplies Exit Architecture and review/replay; distinct from one position, opening authority and close authority.
Aliases: live inventory architecture; inventory state architecture
Disallowed or misleading uses: live position; portfolio strategy; opening architecture; exit architecture
Lifecycle: provisional_thin_seam_non_durable_alpha
Projection metadata: {"projection_status":"canonical","canonical_label":"Inventory Architecture","canonical_slug":"inventory_architecture","category":"authority_surface","stage_owner":"live_inventory","maps_to_contract":"LiveInventorySnapshot","raw_or_derived":"not_applicable","allowed_aliases":["live inventory architecture","inventory state architecture"],"disallowed_phrases":["portfolio strategy"],"semantic_decision_refs":["PM-008:OPC-007"],"machine_projection_omissions":["live position [canonical-token:live_position]","opening architecture [canonical-token:opening_architecture]","exit architecture [canonical-token:exit_architecture]"],"audit_noncanonical_phrases":[]}

### Downstream State-reader Layer
Definition: Governed downstream evidence layer that reports which repo-native capital, position and receipt surfaces were read, distinguishes execution-record truth from truthful placeholders, and reserves recommendation-history/every-pass receipt concerns without policy.
Scope: downstream state-read evidence only; no behavioural decision or state mutation authority.
Owner: downstream state-reader authority; capital, position and receipt repositories retain semantic and write ownership
Relationships: Reads bounded repo-native state for downstream opening, inventory, review and replay consumers; distinct from Inventory Architecture aggregation, Live Position state, Parallel Risk input trace and behavioural decisions.
Aliases: downstream repo-native state reader; downstream state reader
Disallowed or misleading uses: Stage-read State; behavioural decision packet; inventory decision; capital decision; state mutation owner
Lifecycle: active_normative_downstream_evidence_layer
Projection metadata: {"projection_status":"canonical","canonical_label":"Downstream State-reader Layer","canonical_slug":"downstream_state_reader_layer","category":"authority_surface","stage_owner":"downstream_state_reader","maps_to_contract":"DownstreamStateReadResult","raw_or_derived":"not_applicable","allowed_aliases":["downstream repo-native state reader","downstream state reader"],"disallowed_phrases":["Stage-read State","behavioural decision packet","inventory decision","state mutation owner"],"semantic_decision_refs":["PM-008:OPC-010"],"machine_projection_omissions":["capital decision [alias-token:capital_deployment_decision]"],"audit_noncanonical_phrases":["state read","state reader layer"]}

### Exit Architecture
Definition: Governed row-5.14 decision architecture for evaluating live-position state, policy and risk context into hold, trim-ready, close-ready or blocked exit state. Scope: exit-policy judgement and trace.
Scope: exit authority; Live position -> hold/trim-ready/close-ready/blocked decision -> optional Close Architecture handoff.
Owner: exit and close authority, specifically the exit-policy decision owner
Relationships: Consumes Live Position/Inventory Architecture truth; may trigger Close Architecture handoff; distinct from position state, inventory ownership, broker execution and confirmed closure.
Aliases: exit-policy architecture; exit decision authority
Disallowed or misleading uses: close execution; broker close order; inventory mutation; position state
Lifecycle: provisional_thin_seam
Projection metadata: {"projection_status":"canonical","canonical_label":"Exit Architecture","canonical_slug":"exit_architecture","category":"authority_surface","stage_owner":"exit_close","maps_to_contract":"ExitCloseDecision","raw_or_derived":"not_applicable","allowed_aliases":["exit-policy architecture","exit decision authority"],"disallowed_phrases":["close execution","broker close order","inventory mutation","position state"],"semantic_decision_refs":["PM-008:OPC-008"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Close Architecture
Definition: Governed closure architecture for protocol-only close handoff, close receipt/replay evidence and the future separately authorised confirmation of position wind-down. Scope: close transition after Exit Architecture decision.
Scope: closure authority; Exit decision -> protocol-only close handoff -> future broker/execution result -> lawful position/inventory closure update.
Owner: exit and close authority, specifically the closure-transition owner; execution and inventory owners retain their own writes
Relationships: Consumes trim-ready/close-ready Exit Architecture decision; emits CloseHandoffMaterial and ExitCloseReceipt; confirmed closure later requires broker/execution evidence and lawful Live Position/Inventory updates.
Aliases: position-close architecture; closure architecture
Disallowed or misleading uses: exit decision; broker close order; live inventory; position closed merely because handoff exists
Lifecycle: provisional_protocol_only_thin_seam
Projection metadata: {"projection_status":"canonical","canonical_label":"Close Architecture","canonical_slug":"close_architecture","category":"authority_surface","stage_owner":"exit_close","maps_to_contract":"ExitCloseDecision","raw_or_derived":"not_applicable","allowed_aliases":["position-close architecture","closure architecture"],"disallowed_phrases":["exit decision","position closed merely because handoff exists"],"semantic_decision_refs":["PM-008:OPC-009"],"machine_projection_omissions":["broker close order [disallowed-token:exit_architecture]","live inventory [disallowed-token:expression_and_execution]"],"audit_noncanonical_phrases":["and close architecture"]}

### Parallel Risk Lane
Definition: Governed independent advisory lane that evaluates admitted temporal, regime and options/flow primitives into an environmental risk envelope, caution/block observations and traceable packet. Scope: row 5.8 independent risk observation.
Scope: advisory/observation authority; May supply caution flags, hard-block observations and packet identity as explicit downstream inputs. It may not mutate the serial spine or decide deployable percentage/notional.
Owner: parallel risk authority
Relationships: Runs alongside Serial Desk-cognition; may be consumed by downstream pre-deployment/capital/final-risk/review but remains distinct from candidate formation, posture permission and capital deployment.
Aliases: parallel risk; independent risk lane
Disallowed or misleading uses: serial risk stage; capital risk authority; candidate builder; portfolio arbiter
Lifecycle: locked_thin_seam_advisory
Projection metadata: {"projection_status":"canonical","canonical_label":"Parallel Risk Lane","canonical_slug":"parallel_risk_lane","category":"workflow","stage_owner":"parallel_risk_lane","maps_to_contract":"ParallelRiskLanePacket","raw_or_derived":"not_applicable","allowed_aliases":["parallel risk","independent risk lane"],"disallowed_phrases":["serial risk stage","capital risk authority","portfolio arbiter"],"semantic_decision_refs":["PM-009:PRP-001"],"machine_projection_omissions":["candidate builder [disallowed-token:prepared_ingress]"],"audit_noncanonical_phrases":["5.8 parallel risk lane","parallel lane","parallel risk lane dataschema","parallel risk lane profile","parallel risk lane service","roadmap parallel risk lane"]}

### Environment Assessment
Definition: Governed advisory observation describing present temporal/regime/options-flow conditions and the independent risk-envelope state. Scope: environment-only assessment inside Parallel Risk Lane.
Scope: advisory assessment; May inform explicit downstream caution/block evaluation. It cannot select a playbook, form/alter a candidate, authorise capital or issue action language.
Owner: parallel risk authority
Relationships: Feeds the lane packet and may coexist with Candidate Audit; distinct from serial stage outputs, candidate semantics, review explanation and deploy/stand-down authority.
Aliases: parallel-risk environment assessment
Disallowed or misleading uses: market regime context; candidate audit; capital risk decision; trade recommendation
Lifecycle: active_alpha_observation_surface
Projection metadata: {"projection_status":"canonical","canonical_label":"Environment Assessment","canonical_slug":"environment_assessment","category":"parallel_risk_surface","stage_owner":"parallel_risk_lane","maps_to_contract":"ParallelRiskEnvironmentAssessment","raw_or_derived":"not_applicable","allowed_aliases":["parallel-risk environment assessment"],"disallowed_phrases":["capital risk decision","trade recommendation"],"semantic_decision_refs":["PM-009:PRP-002"],"machine_projection_omissions":["market regime context [canonical-token:market_regime_context]","candidate audit [canonical-token:candidate_audit]"],"audit_noncanonical_phrases":["bounded environment assessment","environment assessment basis","environment assessment only"]}

### Parallel-risk Observation Store
Definition: Governed persistence interface that accepts one typed Parallel Risk observation record, rejects duplicate observation identity and returns an append receipt. Scope: lane-owned observation writes only.
Scope: persistence seam; May preserve evidence and receipt identity for later review/replay. It cannot influence serial/capital decisions except by supplying lawfully retrieved historical evidence through a separately admitted reader.
Owner: parallel-risk observation persistence authority
Relationships: Stores Append-only Observation Records produced from lawful packet pairs; distinct from lane evaluation, Review Layer, decision ledger and durable replay system.
Aliases: parallel-risk observation store; PRL observation store
Disallowed or misleading uses: risk decision engine; observation database as durable by default; review repository
Lifecycle: active_process_memory_alpha_non_durable
Projection metadata: {"projection_status":"canonical","canonical_label":"Parallel-risk Observation Store","canonical_slug":"parallel_risk_observation_store","category":"persistence_surface","stage_owner":"parallel_risk_lane","maps_to_contract":"ParallelRiskObservationStore","raw_or_derived":"not_applicable","allowed_aliases":["PRL observation store"],"disallowed_phrases":["risk decision engine","observation database as durable by default","review repository"],"semantic_decision_refs":["PM-009:PRP-005"],"machine_projection_omissions":["parallel-risk observation store [canonical-token:parallel_risk_observation_store]"],"audit_noncanonical_phrases":[]}

### Write-only Persistence
Definition: Governed access/authority constraint on the Parallel-risk Observation Store: append is exposed to the lane-side writer, while observation readback is absent from that operational interface. Scope: writer-facing persistence semantics.
Scope: persistence access constraint; Provides no runtime feedback capable of changing serial or capital decisions. Historical use requires a separately governed read model/repository.
Owner: parallel-risk observation persistence authority
Relationships: Qualifies the store interface; complements Append-only Observation Record; does not mean data is irretrievable forever or physically durable.
Aliases: write-only observation persistence
Disallowed or misleading uses: durable persistence; no audit access ever; fire-and-forget decision; append-only record
Lifecycle: active_alpha_access_constraint
Projection metadata: {"projection_status":"canonical","canonical_label":"Write-only Persistence","canonical_slug":"write_only_persistence","category":"persistence_rule","stage_owner":"parallel_risk_lane","maps_to_contract":"ParallelRiskObservationStore.append_observation","raw_or_derived":"not_applicable","allowed_aliases":["write-only observation persistence"],"disallowed_phrases":["durable persistence","no audit access ever","fire-and-forget decision","append-only record"],"semantic_decision_refs":["PM-009:PRP-006"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["write only"]}

### Append-only Observation Record
Definition: Governed immutable observation record linking one observation identity to input/output packet identities, execution-context identities, lineage and bounded observation payload. Scope: one recorded lane occurrence.
Scope: observation record; Has no direct runtime influence; it preserves what happened so later review/replay can compare without rewriting original decisions.
Owner: parallel-risk observation persistence authority for record form; source/lane owners retain field meaning
Relationships: Stored by Parallel-risk Observation Store; append receipt confirms accepted identity; distinct from mutable lane state, decision output or review summary.
Aliases: parallel-risk observation record; PRL append record
Disallowed or misleading uses: updatable observation row; current lane state; capital receipt; review record
Lifecycle: active_alpha_record_contract
Projection metadata: {"projection_status":"canonical","canonical_label":"Append-only Observation Record","canonical_slug":"append_only_observation_record","category":"persistence_surface","stage_owner":"parallel_risk_lane","maps_to_contract":"ParallelRiskObservationRecord","raw_or_derived":"not_applicable","allowed_aliases":["parallel-risk observation record","PRL append record"],"disallowed_phrases":["updatable observation row","current lane state","capital receipt","review record"],"semantic_decision_refs":["PM-009:PRP-007"],"machine_projection_omissions":[],"audit_noncanonical_phrases":["append only observation record json"]}

### Review Layer
Definition: Governed post-runtime evidence, trace and replay-comparison surface that assembles review records and audit summaries from preserved packets, receipts, decisions and proof outputs. Scope: review and comparison, not decision execution.
Scope: review authority; No live influence on the serial spine or capital decision. Findings may inform later human-governed changes only through new normative/change authority, never retroactively.
Owner: review authority
Relationships: Consumes lane/serial/capital/downstream/persistence evidence; may produce Explanation Layer inputs; distinct from runtime owner, observation store and playbook authority.
Aliases: trace review layer; runtime review layer
Disallowed or misleading uses: runtime arbiter; decision override; risk lane; explanation as exact synonym
Lifecycle: locked_thin_seam_post_runtime
Projection metadata: {"projection_status":"canonical","canonical_label":"Review Layer","canonical_slug":"review_layer","category":"review_surface","stage_owner":"review_explanation","maps_to_contract":"ReviewTrace","raw_or_derived":"not_applicable","allowed_aliases":["trace review layer","runtime review layer"],"disallowed_phrases":["runtime arbiter","decision override","risk lane","explanation as exact synonym"],"semantic_decision_refs":["PM-009:PRP-008"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Explanation Layer
Definition: Governed post-runtime explanatory surface that translates cited review/runtime evidence into bounded human-readable text or explanation packets. Scope: explanation and trace communication only.
Scope: explanation authority; No live influence on serial or capital. Explanation may expose limitations or contradictions but cannot change historical or current authority.
Owner: explanation authority
Relationships: Consumes Review Layer records and/or preserved owner outputs; distinct from the review comparison itself, free-form generation, runtime decisions and playbook definitions.
Aliases: runtime explanation layer; human-readable explanation surface
Disallowed or misleading uses: trade advice; decision rationale owner; review layer as exact synonym; free-form generation
Lifecycle: locked_thin_seam_post_runtime
Projection metadata: {"projection_status":"canonical","canonical_label":"Explanation Layer","canonical_slug":"explanation_layer","category":"review_surface","stage_owner":"review_explanation","maps_to_contract":"ExplanationTrace","raw_or_derived":"not_applicable","allowed_aliases":["runtime explanation layer","human-readable explanation surface"],"disallowed_phrases":["trade advice","decision rationale owner","review layer as exact synonym","free-form generation"],"semantic_decision_refs":["PM-009:PRP-009"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Playbook Library
Definition: Governed registry/library architecture for playbook definitions, setup families/variants, eligibility constraints, selection metadata and proofable metadata receipts. Scope: playbook-owned content and registry meaning.
Scope: playbook authority; May constrain which playbook families/variants can be evaluated by the serial eligibility stage. It cannot directly alter serial outputs or capital decisions.
Owner: playbook library authority
Relationships: Consumed by Playbook Eligibility through explicit contracts; outputs definitions/candidates/metadata receipts but does not itself decide runtime eligibility, capital, broker, exit or close.
Aliases: playbook registry; governed playbook library
Disallowed or misleading uses: Playbook Eligibility; strategy engine; capital/playbook selector; execution playbook authority
Lifecycle: provisional_thin_seam
Projection metadata: {"projection_status":"canonical","canonical_label":"Playbook Library","canonical_slug":"playbook_library","category":"authority_surface","stage_owner":"playbook_library","maps_to_contract":"PlaybookRegistry","raw_or_derived":"not_applicable","allowed_aliases":["playbook registry","governed playbook library"],"disallowed_phrases":["strategy engine","capital/playbook selector","execution playbook authority"],"semantic_decision_refs":["PM-009:PRP-010"],"machine_projection_omissions":["Playbook Eligibility [canonical-token:playbook_eligibility]"],"audit_noncanonical_phrases":[]}

### Financial-calendar Architecture
Definition: Governed four-layer calendar architecture and reference/projection path that preserves market-session reference, financial-event reference, operational calendar state and derived runtime calendar context for later governed steps.
Scope: financial-calendar architecture umbrella
Owner: Financial-calendar domain authority
Relationships: Broader than Financial Calendar Crosswalk and each layer-specific record; owns architectural separation and projection path, not candidate formation, parallel risk or capital deployment.
Aliases: financial calendar; financial-calendar reference and projection; financial-calendar reference and projection path
Disallowed or misleading use: Financial Calendar Crosswalk as umbrella synonym; event calendar as complete architecture; calendar authority as candidate or capital authority
Lifecycle: active_normative_architecture
Projection metadata: {"projection_status":"canonical","canonical_label":"Financial-calendar Architecture","canonical_slug":"financial_calendar_architecture","category":"authority_surface","stage_owner":"financial_calendar","maps_to_contract":"docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:96-156","raw_or_derived":"not_applicable","allowed_aliases":["financial calendar","financial-calendar reference and projection","financial-calendar reference and projection path"],"disallowed_phrases":["Financial Calendar Crosswalk as umbrella synonym","event calendar as complete architecture","calendar authority as candidate or capital authority"],"semantic_decision_refs":["PM-005:CTP-031"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Capital Deployment Authority
Definition: Downstream authority surface that, after serial candidate formation, independent parallel-risk output and pre-deployment gating, decides whether and in what bounded way fresh capital may be deployed.
Scope: downstream fresh-capital authority
Owner: downstream capital deployment authority
Relationships: Owns and emits Capital Deployment Decision; downstream of Serial Desk-cognition Spine, Parallel Risk Lane and pre-deployment gate; upstream of opening architecture.
Aliases: capital deployment; downstream capital deployment authority
Disallowed or misleading use: candidate formation; serial execution stage; parallel risk generation; opening placement mechanics
Lifecycle: locked_placeholder_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"Capital Deployment Authority","canonical_slug":"capital_deployment_authority","category":"authority_surface","stage_owner":"downstream_capital_deployment","maps_to_contract":"docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:305-320","raw_or_derived":"not_applicable","allowed_aliases":["capital deployment","downstream capital deployment authority"],"disallowed_phrases":["candidate formation","serial execution stage","parallel risk generation","opening placement mechanics"],"semantic_decision_refs":["PM-007:SSC-014"],"machine_projection_omissions":["Capital Deployment Decision [canonical-token:capital_deployment_decision]"],"audit_noncanonical_phrases":[]}

### State Kernel
Definition: Shared `M13` mechanism for owner-declared transaction boundaries, scoped idempotency, atomic state-plus-receipt commit and storage ports.
Scope: alpha transaction mechanism and journal only
Owner: M13 state-kernel authority
Relationships: Used through State/Transaction Participation by domain-owning modules; supplies Unit of Work and Repository Port contracts; does not own positions, capital, calendar facts, risk observations or other domain meaning.
Aliases: M13 state kernel; transaction state kernel
Disallowed or misleading use: global transaction manager; owner of all state; persistence proves durability; production database
Lifecycle: accepted_m13_contract_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"State Kernel","canonical_slug":"state_kernel","category":"persistence_surface","stage_owner":"state_kernel","maps_to_contract":"docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:11.10","raw_or_derived":"not_applicable","allowed_aliases":["M13 state kernel","transaction state kernel"],"disallowed_phrases":["global transaction manager","owner of all state","production database"],"semantic_decision_refs":["M13-PROOF:MLC-A"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Unit of Work
Definition: One transaction execution boundary that validates a typed command, operates on an isolated working state and either atomically publishes the resulting state and receipt or publishes neither.
Scope: one owner-declared consistency unit per execution
Owner: State Kernel
Relationships: Consumes Transaction Command; emits Atomic Receipt; applies through a Repository Port or bounded in-memory adapter; remains separate from a cross-domain workflow.
Aliases: transaction unit of work
Disallowed or misleading use: repository-wide transaction; workflow transaction across all domains; receipt append helper; durability guarantee
Lifecycle: accepted_m13_contract_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"Unit of Work","canonical_slug":"unit_of_work","category":"persistence_surface","stage_owner":"state_kernel","maps_to_contract":"docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:17-76","raw_or_derived":"not_applicable","allowed_aliases":["transaction unit of work"],"disallowed_phrases":["repository-wide transaction","workflow transaction across all domains","receipt append helper","durability guarantee"],"semantic_decision_refs":["M13-PROOF:MLC-A"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Idempotency Key
Definition: Caller-supplied stable key scoped by command type and consistency-unit identity and atomically bound to command identity, semantic input fingerprint, committed result, state version/sequence and receipt.
Scope: one named command type and one consistency unit
Owner: command owner for issuance; State Kernel for binding and conflict enforcement
Relationships: Carried by Transaction Command and retained by Atomic Receipt; exact same-key/same-input replay returns original committed truth, while conflicting reuse fails.
Aliases: scoped idempotency key
Disallowed or misleading use: receipt ID as complete idempotency; globally unique transaction key; duplicate suppression without input fingerprint; retry counter
Lifecycle: accepted_m13_contract_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"Idempotency Key","canonical_slug":"idempotency_key","category":"protocol_field","stage_owner":"state_kernel","maps_to_contract":"docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:52-58","raw_or_derived":"not_applicable","allowed_aliases":["scoped idempotency key"],"disallowed_phrases":["receipt ID as complete idempotency","globally unique transaction key","duplicate suppression without input fingerprint","retry counter"],"semantic_decision_refs":["M13-PROOF:MLC-A"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Atomic Receipt
Definition: Immutable success attestation published in the same admitted commit as the state transition it describes and carrying command, idempotency, result and state-version lineage.
Scope: one committed owner-declared transaction result
Owner: State Kernel for atomic publication; domain owner for result meaning
Relationships: Emitted by Unit of Work; references Transaction Command and resulting state sequence; absent on failed or rolled-back transactions.
Aliases: atomic commit receipt; transaction receipt
Disallowed or misleading use: separately appended success claim; failure attempt record; evidence of external completion; receipt ID only
Lifecycle: accepted_m13_contract_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"Atomic Receipt","canonical_slug":"atomic_receipt","category":"persistence_surface","stage_owner":"state_kernel","maps_to_contract":"docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:29-46","raw_or_derived":"not_applicable","allowed_aliases":["atomic commit receipt","transaction receipt"],"disallowed_phrases":["separately appended success claim","failure attempt record","evidence of external completion","receipt ID only"],"semantic_decision_refs":["M13-PROOF:MLC-A"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Repository Port
Definition: Module-owned storage interface exposing the transaction participation, expected-version and atomic commit semantics required by its owning domain contract.
Scope: replaceable persistence interface used by State Kernel transactions
Owner: owning domain module for record meaning; State Kernel for transaction protocol requirements
Relationships: A memory or future durable adapter implements the same port; use does not transfer semantic ownership to M13.
Aliases: state repository port; transaction repository port
Disallowed or misleading use: database implementation; shared domain owner; generic CRUD repository; durability claim
Lifecycle: accepted_m13_contract_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"Repository Port","canonical_slug":"repository_port","category":"persistence_surface","stage_owner":"state_kernel","maps_to_contract":"docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:64-68","raw_or_derived":"not_applicable","allowed_aliases":["state repository port","transaction repository port"],"disallowed_phrases":["database implementation","shared domain owner","generic CRUD repository","durability claim"],"semantic_decision_refs":["M13-PROOF:MLC-A"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Transaction Command
Definition: Typed request carrying command identity, scoped Idempotency Key, semantic input fingerprint, expected prior state version and governing policy or configuration version.
Scope: input to one Unit of Work execution
Owner: issuing domain module for business meaning; State Kernel for transaction-contract validation
Relationships: Supplies deterministic identity and preconditions to Unit of Work; retained by Atomic Receipt and replay evidence; does not itself mutate state.
Aliases: transaction command contract
Disallowed or misleading use: business decision result; untyped mutation dictionary; global workflow command; receipt
Lifecycle: accepted_m13_contract_authority
Projection metadata: {"projection_status":"canonical","canonical_label":"Transaction Command","canonical_slug":"transaction_command","category":"carrier","stage_owner":"state_kernel","maps_to_contract":"docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:29-40","raw_or_derived":"not_applicable","allowed_aliases":["transaction command contract"],"disallowed_phrases":["business decision result","untyped mutation dictionary","global workflow command"],"semantic_decision_refs":["M13-PROOF:MLC-A"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### PM-controlled Parallel Workflow
Definition: One Project Manager-controlled execution mode in which multiple independent bounded assignments may be worked or tested concurrently while canonical acceptance, integration and checkpoint publication remain serial.
Scope: programme execution and integration control
Owner: Master Project Manager
Relationships: Contains Parallel Execution Lanes and Lane Assignments; preserves one canonical repository and one serial PM integration front.
Aliases: parallel workflow
Disallowed or misleading use: parallel canonical state; autonomous worker programme; concurrent PM acceptance
Lifecycle: active_programme_control
Projection metadata: {"projection_status":"canonical","canonical_label":"PM-controlled Parallel Workflow","canonical_slug":"pm_controlled_parallel_workflow","category":"workflow","stage_owner":"canonical_project_manager","maps_to_contract":"project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md","raw_or_derived":"not_applicable","allowed_aliases":["parallel workflow"],"disallowed_phrases":[],"semantic_decision_refs":["USER-20260728:PM-CONTROLLED-PARALLEL-WORKFLOW","PM-20260729:PARALLEL-CONTROL-REPAIR-1"],"machine_projection_omissions":["Contextual disallowed-use prose and lane lifecycle tokens remain governed in the human record."],"audit_noncanonical_phrases":[]}

### Parallel Execution Lane
Definition: Numbered execution-capacity slot that may hold at most one current Lane Assignment and does not own a module, canonical branch or follow-on queue.
Scope: parallel scheduling capacity
Owner: Master Project Manager
Relationships: Hosts one worker/tester assignment pair when allocated; may be held without a branch or filler task.
Aliases: PM-controlled lane; execution lane; permanent lane
Disallowed or misleading use: module owner; long-lived branch; autonomous queue
Lifecycle: active_programme_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Parallel Execution Lane","canonical_slug":"parallel_execution_lane","category":"workflow","stage_owner":"canonical_project_manager","maps_to_contract":"project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md","raw_or_derived":"not_applicable","allowed_aliases":["PM-controlled lane","execution lane","permanent lane"],"disallowed_phrases":[],"semantic_decision_refs":["USER-20260728:PM-CONTROLLED-PARALLEL-WORKFLOW","PM-20260729:PARALLEL-CONTROL-REPAIR-1"],"machine_projection_omissions":["Contextual disallowed-use prose and lane lifecycle tokens remain governed in the human record."],"audit_noncanonical_phrases":[]}

### Lane Assignment
Definition: One revisioned, dependency-ready semantic leaf or bounded implementation slice allocated to one worker/tester pair from one named canonical checkpoint with exact reads, writes, locks and return states.
Scope: one bounded parallel execution unit
Owner: Master Project Manager
Relationships: Uses one Parallel Execution Lane, one Worker Candidate Archive and one tester verdict; lifecycle and exceptional states are governed by the parallel workflow architecture.
Aliases: parallel assignment
Disallowed or misleading use: whole programme; automatic next task; module ownership
Lifecycle: active_programme_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Lane Assignment","canonical_slug":"lane_assignment","category":"workflow","stage_owner":"canonical_project_manager","maps_to_contract":"project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md","raw_or_derived":"not_applicable","allowed_aliases":["parallel assignment"],"disallowed_phrases":[],"semantic_decision_refs":["USER-20260728:PM-CONTROLLED-PARALLEL-WORKFLOW","PM-20260729:PARALLEL-CONTROL-REPAIR-1"],"machine_projection_omissions":["Contextual disallowed-use prose and lane lifecycle tokens remain governed in the human record."],"audit_noncanonical_phrases":[]}

### Material Read Set
Definition: Subset of authority and evidence whose canonical change may invalidate a prior worker or tester conclusion and require stale-base revalidation.
Scope: assignment stale-base control
Owner: Master Project Manager
Relationships: Recorded per Lane Assignment; distinct from the complete required full-read list and from the exact write set.
Aliases: stale-base read set
Disallowed or misleading use: all files read; write set; general dependency list
Lifecycle: active_programme_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Material Read Set","canonical_slug":"material_read_set","category":"authority_surface","stage_owner":"canonical_project_manager","maps_to_contract":"project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md","raw_or_derived":"not_applicable","allowed_aliases":["stale-base read set"],"disallowed_phrases":[],"semantic_decision_refs":["USER-20260728:PM-CONTROLLED-PARALLEL-WORKFLOW","PM-20260729:PARALLEL-CONTROL-REPAIR-1"],"machine_projection_omissions":["Contextual disallowed-use prose and lane lifecycle tokens remain governed in the human record."],"audit_noncanonical_phrases":[]}

### Worker Candidate Archive
Definition: Exact-named Git-preserving full-history return from a lane worker containing unaccepted candidate changes and worker-owned evidence.
Scope: worker-to-tester transfer
Owner: Lane worker under PM assignment
Relationships: Preserves PM-source ancestry and feeds the matching independent tester; never establishes canonical acceptance.
Aliases: worker candidate; candidate repository archive
Disallowed or misleading use: accepted checkpoint; tester result; canonical integration
Lifecycle: active_programme_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Worker Candidate Archive","canonical_slug":"worker_candidate_archive","category":"carrier","stage_owner":"canonical_project_manager","maps_to_contract":"project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md","raw_or_derived":"not_applicable","allowed_aliases":["worker candidate","candidate repository archive"],"disallowed_phrases":[],"semantic_decision_refs":["USER-20260728:PM-CONTROLLED-PARALLEL-WORKFLOW","PM-20260729:PARALLEL-CONTROL-REPAIR-1"],"machine_projection_omissions":["Contextual disallowed-use prose and lane lifecycle tokens remain governed in the human record."],"audit_noncanonical_phrases":[]}

### Tester-approved Portability Artefact
Definition: Exact-named reconstructable package containing verified Git changes, worker claim, tester verdict, manifests, hashes and validation evidence suitable for PM integration review but not canonical acceptance.
Scope: tester-to-PM transfer
Owner: Independent lane tester under PM assignment
Relationships: Contains a verified Git bundle and reconstruction proof; PASS remains provisional until PM acceptance and serial integration.
Aliases: tester-approved artefact; approved portability artefact
Disallowed or misleading use: canonical checkpoint; PM acceptance; worker repair package
Lifecycle: active_programme_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Tester-approved Portability Artefact","canonical_slug":"tester_approved_portability_artefact","category":"carrier","stage_owner":"canonical_project_manager","maps_to_contract":"project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md","raw_or_derived":"not_applicable","allowed_aliases":["tester-approved artefact","approved portability artefact"],"disallowed_phrases":[],"semantic_decision_refs":["USER-20260728:PM-CONTROLLED-PARALLEL-WORKFLOW","PM-20260729:PARALLEL-CONTROL-REPAIR-1"],"machine_projection_omissions":["Contextual disallowed-use prose and lane lifecycle tokens remain governed in the human record."],"audit_noncanonical_phrases":[]}

### Independent Control Test
Definition: Review by a separate control-tester thread of a newly authored or materially repaired workflow-control checkpoint before PM acceptance or lane launch.
Scope: parallel-control checkpoint review
Owner: Independent control tester
Relationships: Tests control law, briefs, vocabulary, manifests, artefacts and launch boundaries; may add evidence only and cannot repair or accept the checkpoint.
Aliases: control tester review; independent control review
Disallowed or misleading use: self-acceptance; lane test; PM acceptance
Lifecycle: active_programme_control
Projection metadata: {"projection_status":"canonical","canonical_label":"Independent Control Test","canonical_slug":"independent_control_test","category":"promotion_surface","stage_owner":"canonical_project_manager","maps_to_contract":"project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md","raw_or_derived":"not_applicable","allowed_aliases":["control tester review","independent control review"],"disallowed_phrases":[],"semantic_decision_refs":["USER-20260728:PM-CONTROLLED-PARALLEL-WORKFLOW","PM-20260729:PARALLEL-CONTROL-REPAIR-1"],"machine_projection_omissions":["Contextual disallowed-use prose and lane lifecycle tokens remain governed in the human record."],"audit_noncanonical_phrases":[]}

### Reference Packet
Definition: DMPV3 carriage of one identified and versioned reference product under an explicit reference acquisition, import, publication or replay execution context.
Scope: reference-product packet carriage only
Owner: reference-data owner for payload meaning; M04 packet protocol for carriage validation
Relationships: Carries a reference product and its retrievable source artefacts; distinct from the underlying reference artefact, source truth and any runtime decision.
Aliases: DMPV3 reference packet role
Disallowed or misleading use: reference artefact as packet occurrence; reference packet without owner-supplied execution context
Lifecycle: accepted_k07_packet_role
Projection metadata: {"projection_status":"canonical","namespace":"m04","canonical_label":"Reference Packet","canonical_slug":"reference_packet","category":"protocol_field","stage_owner":"packet_protocol","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:9.10","raw_or_derived":"not_applicable","allowed_aliases":["DMPV3 reference packet role"],"disallowed_phrases":["reference artefact as packet occurrence","reference packet without owner-supplied execution context"],"semantic_decision_refs":["M04-K07-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Prepared Context Packet
Definition: DMPV3 carriage of one identified prepared-runtime substrate with source/capture lineage, preparation meaning and prepared fingerprint preserved.
Scope: prepared-runtime-context handoff
Owner: preparation owner for payload meaning; M04 packet protocol for carriage validation
Relationships: Carries prepared authority into lawful consumers; distinct from raw ingress, serial-stage output and packet occurrence identity.
Aliases: prepared runtime context packet
Disallowed or misleading use: raw input packet; generic prepared dictionary; preparation as trading decision
Lifecycle: accepted_k07_packet_role
Projection metadata: {"projection_status":"canonical","namespace":"m04","canonical_label":"Prepared Context Packet","canonical_slug":"prepared_context_packet","category":"protocol_field","stage_owner":"packet_protocol","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:9.10","raw_or_derived":"derived","allowed_aliases":["prepared runtime context packet"],"disallowed_phrases":["raw input packet","generic prepared dictionary","preparation as trading decision"],"semantic_decision_refs":["M04-K07-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Stage Packet
Definition: DMPV3 carriage of one named serial desk-cognition stage output with ordered parentage, material dependencies and stage-domain identity preserved.
Scope: serial stage output carriage
Owner: named serial stage for payload meaning; M04 packet protocol for carriage validation
Relationships: Follows prepared or prior-stage packets; distinct from Parallel Risk Packet and capital deployment authority.
Aliases: serial stage packet
Disallowed or misleading use: parallel-risk output; capital decision packet; unowned omnibus stage
Lifecycle: accepted_k07_packet_role
Projection metadata: {"projection_status":"canonical","namespace":"m04","canonical_label":"Stage Packet","canonical_slug":"stage_packet","category":"protocol_field","stage_owner":"packet_protocol","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:9.10","raw_or_derived":"derived","allowed_aliases":["serial stage packet"],"disallowed_phrases":["parallel-risk output as stage packet","capital decision packet as stage packet","unowned omnibus stage packet"],"semantic_decision_refs":["M04-K07-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Parallel Risk Packet
Definition: DMPV3 carriage of one independent parallel-risk assessment with lawful input lineage and bounded risk-output identity.
Scope: independent parallel-risk output carriage
Owner: parallel-risk authority for payload meaning; M04 packet protocol for carriage validation
Relationships: Consumes lawful prepared/stage inputs while remaining separate from serial candidate formation and capital deployment.
Aliases: independent risk packet
Disallowed or misleading use: serial candidate packet; capital sizing instruction; merged serial-risk output
Lifecycle: accepted_k07_packet_role
Projection metadata: {"projection_status":"canonical","namespace":"m04","canonical_label":"Parallel Risk Packet","canonical_slug":"parallel_risk_packet","category":"protocol_field","stage_owner":"packet_protocol","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:9.10","raw_or_derived":"derived","allowed_aliases":["independent risk packet"],"disallowed_phrases":["serial candidate packet","capital sizing instruction packet","merged serial-risk output packet"],"semantic_decision_refs":["M04-K07-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Review Explanation Packet
Definition: DMPV3 review-only carriage of a deterministic human-facing explanation derived from identified packets, decisions, receipts or evidence.
Scope: post-runtime review and explanation carriage
Owner: review/explanation owner for payload meaning; M04 packet protocol for carriage validation
Relationships: Requires a governed review trace and cited evidence; distinct from runtime decision, replay result and free-form advice.
Aliases: review-only explanation packet
Disallowed or misleading use: runtime decision packet; trade advice packet; uncited explanation
Lifecycle: accepted_k07_packet_role
Projection metadata: {"projection_status":"canonical","namespace":"m04","canonical_label":"Review Explanation Packet","canonical_slug":"review_explanation_packet","category":"protocol_field","stage_owner":"packet_protocol","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:9.10","raw_or_derived":"derived","allowed_aliases":["review-only explanation packet"],"disallowed_phrases":["runtime decision packet as explanation","trade advice packet","uncited explanation packet"],"semantic_decision_refs":["M04-K07-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Replay Request Packet
Definition: DMPV3 non-side-effecting request to replay one identified authoritative target using a declared evidence and material-version set.
Scope: replay request carriage
Owner: replay authority for request meaning; M04 packet protocol for carriage validation
Relationships: Names a replay target and replay trace; precedes Replay Result Packet; does not itself reconstruct or execute live effects.
Aliases: governed replay request packet
Disallowed or misleading use: live execution request; proof that replay succeeded; anonymous replay target
Lifecycle: accepted_k07_packet_role
Projection metadata: {"projection_status":"canonical","namespace":"m04","canonical_label":"Replay Request Packet","canonical_slug":"replay_request_packet","category":"protocol_field","stage_owner":"packet_protocol","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:9.10","raw_or_derived":"not_applicable","allowed_aliases":["governed replay request packet"],"disallowed_phrases":["live execution request packet","replay success claim in request","anonymous replay target packet"],"semantic_decision_refs":["M04-K07-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Replay Result Packet
Definition: Newly emitted DMPV3 carriage of an isolated replay result that identifies the original target, consumed authoritative evidence and authoritative-or-incomplete outcome.
Scope: replay result carriage
Owner: replay authority for result meaning; M04 packet protocol for carriage validation
Relationships: Responds to Replay Request Packet; references rather than impersonates the original occurrence; may feed Replay Comparison Packet.
Aliases: governed replay output packet
Disallowed or misleading use: original preserved packet; live side-effect result; current-code comparison as authoritative replay
Lifecycle: accepted_k07_packet_role
Projection metadata: {"projection_status":"canonical","namespace":"m04","canonical_label":"Replay Result Packet","canonical_slug":"replay_result_packet","category":"protocol_field","stage_owner":"packet_protocol","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:9.10","raw_or_derived":"derived","allowed_aliases":["governed replay output packet"],"disallowed_phrases":["new replay result as original packet","live side-effect replay result","current-code comparison as authoritative replay"],"semantic_decision_refs":["M04-K07-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Replay Comparison Packet
Definition: DMPV3 carriage of a deterministic comparison between identified original and replay-result evidence, including visible matches, mismatches and limitations.
Scope: replay comparison carriage
Owner: replay/review authority for comparison meaning; M04 packet protocol for carriage validation
Relationships: Consumes original and Replay Result Packet evidence; distinct from reconstruction authority and Review Explanation Packet.
Aliases: replay evidence comparison packet
Disallowed or misleading use: comparison proves reconstruction; hidden mismatch packet; arbitrary mapping comparison
Lifecycle: accepted_k07_packet_role
Projection metadata: {"projection_status":"canonical","namespace":"m04","canonical_label":"Replay Comparison Packet","canonical_slug":"replay_comparison_packet","category":"protocol_field","stage_owner":"packet_protocol","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:9.10","raw_or_derived":"derived","allowed_aliases":["replay evidence comparison packet"],"disallowed_phrases":["comparison proves reconstruction","hidden mismatch comparison packet","arbitrary mapping comparison packet"],"semantic_decision_refs":["M04-K07-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Diagnostic Packet
Definition: Separately admitted, non-binding DMPV3 carriage of identified validation, processing or authority-boundary failure facts.
Scope: non-binding diagnostic carriage
Owner: failing boundary for diagnostic meaning; M04 packet protocol for carriage validation
Relationships: May describe a rejected target but never substitutes for that target's binding role or payload.
Aliases: DMPV3 diagnostic role
Disallowed or misleading use: degraded binding output; unidentified failure packet; diagnostic as domain decision
Lifecycle: accepted_k07_packet_role
Projection metadata: {"projection_status":"canonical","namespace":"m04","canonical_label":"Diagnostic Packet","canonical_slug":"diagnostic_packet","category":"protocol_field","stage_owner":"packet_protocol","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:9.10","raw_or_derived":"derived","allowed_aliases":["DMPV3 diagnostic role"],"disallowed_phrases":["degraded binding output as diagnostic","unidentified failure packet","diagnostic packet as domain decision"],"semantic_decision_refs":["M04-K07-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}

### Rejection Packet
Definition: Separately admitted, non-binding DMPV3 carriage recording rejection of an identified proposed packet, request or input and the exact failed authority facts.
Scope: non-binding rejection carriage
Owner: rejecting boundary for rejection meaning; M04 packet protocol for carriage validation
Relationships: A specialised diagnostic role with an identified rejected target; does not become the rejected domain output.
Aliases: DMPV3 rejection role
Disallowed or misleading use: successful binding output; anonymous rejection; rejected payload made authoritative
Lifecycle: accepted_k07_packet_role
Projection metadata: {"projection_status":"canonical","namespace":"m04","canonical_label":"Rejection Packet","canonical_slug":"rejection_packet","category":"protocol_field","stage_owner":"packet_protocol","maps_to_contract":"docs/09.1_DMPV3_PROTOCOL_WORKING.md:9.10","raw_or_derived":"derived","allowed_aliases":["DMPV3 rejection role"],"disallowed_phrases":["successful binding output as rejection","anonymous rejection packet","rejected payload made authoritative"],"semantic_decision_refs":["M04-K07-NORMATIVE-AUTHORITY-V1"],"machine_projection_omissions":[],"audit_noncanonical_phrases":[]}
