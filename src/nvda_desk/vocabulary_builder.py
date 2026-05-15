"""Build the canonical vocabulary document for the scaffold repo.

This builder is intentionally dependency-light in the scaffold pass. It seeds only
admitted architecture-level terms fixed by the migrated control stack and the
active retained Tier A shell.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from nvda_desk.schemas.vocabulary import VocabularyDocument, VocabularyEntry

OUTPUT_PATH = Path("data/vocabulary/canonical_vocabulary.json")
GOVERNED_SOURCE_PATHS = [
    Path("docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md"),
    Path("docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md"),
    Path("docs/vocabulary/README.md"),
    Path("docs/vocabulary/CONSOLIDATION_WORKFLOW.md"),
    Path("docs/vocabulary/vocabulary_registry.md"),
    Path("scripts/build_canonical_vocabulary.py"),
    Path("src/nvda_desk/schemas/vocabulary.py"),
    Path("src/nvda_desk/vocabulary_builder.py"),
    Path("src/nvda_desk/vocabulary_synonym_audit.py"),
    Path("data/vocabulary/canonical_vocabulary.json"),
]


def build_document() -> VocabularyDocument:
    document = VocabularyDocument(
        schema_version="v1",
        registry_version="2026-04-22",
        notes=[
            "Scaffold baseline. Extend only through the governed vocabulary workflow.",
            "Financial-calendar reference terms are admitted because the active Tier A shell already treats them as blocking governed names.",
            "Stage Input Bundle is admitted as the cognition-ingress-owned internal carrier at the prepared-substrate to serial-runtime seam.",
            "Module 7 admits the canonical DMPV3 packet-carriage contract surfaces and mandatory outer-envelope field terms.",
            "Module 8 admits the bootstrap parallel-risk lane and write-only persistence terms needed for the lawful Stage A runtime path.",
            "Temporal standard tranche 1 admits the source temporal standard, its governed source fields, and workbook temporal provenance terms.",
            "Temporal standard tranche 2 admits the conformance inventory and classification terms used for temporal audit receipts.",
        ],
        entries=[
            VocabularyEntry(
                "temporal_context",
                "Temporal Context",
                "stage",
                "temporal_context",
                "TemporalContextOutput",
                allowed_aliases=["temporal event context"],
                disallowed_phrases=["temporal context seq5"],
            ),
            VocabularyEntry(
                "market_regime_context",
                "Market Regime Context",
                "stage",
                "market_regime_context",
                "MarketRegimeContextOutput",
            ),
            VocabularyEntry(
                "options_flow_context",
                "Options and Flow Context",
                "stage",
                "options_flow_context",
                "OptionsFlowContextOutput",
            ),
            VocabularyEntry(
                "posture_risk_permission",
                "Posture and Risk Permission",
                "stage",
                "posture_risk_permission",
                "PostureRiskPermissionOutput",
            ),
            VocabularyEntry(
                "playbook_eligibility",
                "Playbook Eligibility",
                "stage",
                "playbook_eligibility",
                "PlaybookEligibilityOutput",
                disallowed_phrases=["playbook eligibility service"],
            ),
            VocabularyEntry(
                "expression_execution",
                "Expression and Execution",
                "stage",
                "expression_execution",
                "ExpressionExecutionOutput",
                allowed_aliases=["execution expression"],
            ),
            VocabularyEntry(
                "parallel_risk_lane",
                "Parallel Risk Lane",
                "workflow",
                "parallel_risk_lane",
                "ParallelRiskLanePacket",
                allowed_aliases=["parallel lane", "parallel risk", "risk lane"],
                disallowed_phrases=[
                    "parallel risk lane dataschema",
                    "parallel risk lane packet",
                    "parallel risk lane service",
                    "roadmap parallel risk lane",
                ],
            ),
            VocabularyEntry(
                "dmp_v3",
                "DMP V3",
                "protocol",
                "cross_stage_protocol",
                "DmpV3Envelope",
                allowed_aliases=["dmpv3"],
                disallowed_phrases=["dmp v3 root"],
            ),
            VocabularyEntry(
                "dmp_v3_envelope",
                "DmpV3Envelope",
                "protocol_surface",
                "cross_stage_protocol",
                "DmpV3Envelope",
            ),
            VocabularyEntry(
                "dmp_v3_packet",
                "DmpV3Packet",
                "protocol_surface",
                "cross_stage_protocol",
                "DmpV3Packet",
                allowed_aliases=["DMPV3 packet"],
            ),
            VocabularyEntry(
                "desk_module_packet_v3",
                "DeskModulePacketV3",
                "protocol_surface",
                "cross_stage_protocol",
                "DeskModulePacketV3",
            ),
            VocabularyEntry(
                "packetrole",
                "packetrole",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Envelope.packetrole",
            ),
            VocabularyEntry(
                "producer",
                "producer",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Envelope.producer",
            ),
            VocabularyEntry(
                "lineage",
                "lineage",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Envelope.lineage",
            ),
            VocabularyEntry(
                "validation",
                "validation",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Envelope.validation",
            ),
            VocabularyEntry(
                "summary",
                "summary",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Envelope.summary",
            ),
            VocabularyEntry(
                "dmpextensions",
                "dmpextensions",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Envelope.dmpextensions",
            ),
            VocabularyEntry(
                "module_id",
                "module_id",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Producer.module_id",
            ),
            VocabularyEntry(
                "module_version",
                "module_version",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Producer.module_version",
            ),
            VocabularyEntry(
                "module_instance_id",
                "module_instance_id",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Producer.module_instance_id",
            ),
            VocabularyEntry(
                "grammar_role",
                "grammar_role",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Producer.grammar_role",
            ),
            VocabularyEntry(
                "behaviour_class",
                "behaviour_class",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Producer.behaviour_class",
            ),
            VocabularyEntry(
                "traceid",
                "traceid",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Envelope.traceid",
            ),
            VocabularyEntry(
                "runid", "runid", "protocol_field", "cross_stage_protocol", "DmpV3Envelope.runid"
            ),
            VocabularyEntry(
                "scenarioid",
                "scenarioid",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Envelope.scenarioid",
            ),
            VocabularyEntry(
                "financial_calendar_reference_bundle",
                "Financial Calendar Reference Bundle",
                "reference_data",
                "calendar_reference",
                "ImportedReferenceBundle",
            ),
            VocabularyEntry(
                "financial_calendar_crosswalk",
                "Financial Calendar Crosswalk",
                "reference_data",
                "calendar_reference",
                "FinancialCalendarCrosswalkRecord",
                allowed_aliases=["financial calendar"],
            ),
            VocabularyEntry(
                "financial_calendar_import_record",
                "Financial Calendar Import Record",
                "reference_data",
                "calendar_reference",
                "FinancialCalendarImportRecord",
            ),
            VocabularyEntry(
                "event_calendar",
                "Event Calendar",
                "reference_data",
                "calendar_reference",
                "EventCalendarProjection",
                allowed_aliases=["event calendar architecture", "event calendar ownership"],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.4 and FWD-008 closure language."
                ],
            ),
            VocabularyEntry(
                "raw_signal_families",
                "Raw Signal Families",
                "authority_surface",
                "upstream_raw_signal",
                "RawSignalFamilyCoverage",
                allowed_aliases=["raw signal", "raw signal family"],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.3 and FWD-007 closure language."
                ],
            ),
            VocabularyEntry(
                "prepared_ingress",
                "Prepared Ingress",
                "authority_surface",
                "prepared_ingress",
                "PreparedRuntimeContextBuilder",
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.5 and FWD-009 closure language."
                ],
            ),
            VocabularyEntry(
                "runtime_context",
                "Runtime Context",
                "carrier",
                "prepared_ingress",
                "PreparedRuntimeSnapshot",
                allowed_aliases=[
                    "admitted runtime context",
                    "prepared runtime context",
                    "project runtime context",
                    "runtime context preparation",
                ],
                disallowed_phrases=["ithout runtime context", "pared runtime context"],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 as the prepared substrate consumed downstream."
                ],
            ),
            VocabularyEntry(
                "serial_desk_cognition",
                "Serial Desk-cognition",
                "workflow",
                "serial_desk_cognition",
                "SerialDeskCognitionPacket",
                allowed_aliases=[
                    "serial cognition",
                    "serial desk cognition authority",
                    "serial desk cognition behaviour",
                    "serial desk cognition output",
                    "serial desk cognition spine",
                ],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.7 and FWD-012 closure language."
                ],
            ),
            VocabularyEntry(
                "serial_candidate",
                "Serial Candidate",
                "carrier",
                "serial_desk_cognition",
                "serial_candidate_id",
                allowed_aliases=[
                    "serial candidate eligible",
                    "serial candidate formation",
                    "serial candidate id",
                    "serial candidate material",
                    "serial candidate outputs",
                    "serial candidate rebuild",
                    "serial candidate selection",
                ],
                disallowed_phrases=[
                    "serial candidate 001",
                    "serial candidate 002",
                    "serial candidate 003",
                    "serial candidate 004",
                    "serial candidate 005",
                    "serial candidate 006",
                    "serial candidate 007",
                    "serial candidate 008",
                    "serial candidate row039",
                    "serial candidate row041",
                    "serial candidate row042",
                    "serial candidate seq9",
                ],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 for the candidate material consumed by capital/opening seams."
                ],
            ),
            VocabularyEntry(
                "capital_deployment_decision",
                "Capital Deployment Decision",
                "authority_surface",
                "downstream_capital_deployment",
                "CapitalDeploymentDecision",
                allowed_aliases=["capital deployment", "fresh capital deployment decision"],
                disallowed_phrases=[
                    "capital deployment decision dataschema",
                    "capital deployment decision emitted",
                    "capital deployment decision seq9",
                    "consumes capital deployment decision",
                ],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.11 and FWD-014 closure language."
                ],
            ),
            VocabularyEntry(
                "opening_architecture",
                "Opening Architecture",
                "authority_surface",
                "downstream_opening",
                "DownstreamOpeningService",
                allowed_aliases=["downstream opening architecture"],
                disallowed_phrases=["stream opening architecture"],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.12 and FWD-015 closure language."
                ],
            ),
            VocabularyEntry(
                "downstream_opening",
                "Downstream Opening",
                "authority_surface",
                "downstream_opening",
                "DownstreamOpeningSnapshot",
                allowed_aliases=[
                    "downstream opening authorisation",
                    "downstream opening authority",
                    "downstream opening service",
                ],
                disallowed_phrases=[
                    "a downstream opening",
                    "collapsing downstream opening",
                    "preserving downstream opening",
                    "the downstream opening",
                    "what downstream opening",
                ],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 for the bounded opening seam."
                ],
            ),
            VocabularyEntry(
                "placement_readiness",
                "Placement Readiness",
                "authority_surface",
                "downstream_opening",
                "PlacementReadinessResult",
                allowed_aliases=[
                    "opening placement readiness",
                    "placement readiness id",
                    "placement readiness result",
                ],
                disallowed_phrases=[
                    "evaluate placement readiness",
                    "placement readiness 001",
                    "placement readiness tests",
                ],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 as the non-executing readiness output of the opening seam."
                ],
            ),
            VocabularyEntry(
                "placement_handoff",
                "Placement Handoff",
                "carrier",
                "downstream_opening",
                "PlacementHandoffMaterial",
                allowed_aliases=["placement handoff material"],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 as protocol-only handoff material, not broker execution."
                ],
            ),
            VocabularyEntry(
                "broker_protocol",
                "Broker Protocol",
                "protocol",
                "downstream_opening",
                "BrokerBoundaryMode",
                allowed_aliases=["broker protocol only"],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 as a protocol boundary term, not concrete broker execution."
                ],
            ),
            VocabularyEntry(
                "live_position",
                "Live Position",
                "authority_surface",
                "live_inventory",
                "LivePositionSnapshot",
                allowed_aliases=["live position management", "live position state"],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.13 terminology only; FWD-016 remains unopened."
                ],
            ),
            VocabularyEntry(
                "inventory_architecture",
                "Inventory Architecture",
                "authority_surface",
                "live_inventory",
                "LiveInventorySnapshot",
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.13 terminology only; FWD-016 remains unopened."
                ],
            ),
            VocabularyEntry(
                "exit_architecture",
                "Exit Architecture",
                "authority_surface",
                "exit_close",
                "ExitCloseDecision",
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.14 terminology only; exit/close remains unopened."
                ],
            ),
            VocabularyEntry(
                "close_architecture",
                "Close Architecture",
                "authority_surface",
                "exit_close",
                "ExitCloseDecision",
                disallowed_phrases=["and close architecture"],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.14 terminology only; exit/close remains unopened."
                ],
            ),
            VocabularyEntry(
                "review_layer",
                "Review Layer",
                "review_surface",
                "review_explanation",
                "ReviewTrace",
                allowed_aliases=["review layer outputs"],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.15 terminology only."
                ],
            ),
            VocabularyEntry(
                "explanation_layer",
                "Explanation Layer",
                "review_surface",
                "review_explanation",
                "ExplanationTrace",
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.15 terminology only."
                ],
            ),
            VocabularyEntry(
                "playbook_library",
                "Playbook Library",
                "authority_surface",
                "playbook_library",
                "PlaybookRegistry",
                allowed_aliases=[
                    "playbook library architecture",
                    "playbook library authority",
                    "playbook library ownership",
                ],
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.10 and FWD-011 closure language."
                ],
            ),
            VocabularyEntry(
                "modifier_authority",
                "Modifier Authority",
                "authority_surface",
                "posture_risk_permission",
                "ModifierPolicyRecord",
                notes=[
                    "Admitted during bounded governance remediation before FWD-016 from blueprint row 5.9 and FWD-010 closure language."
                ],
            ),
            VocabularyEntry(
                "coefficient_authority",
                "Coefficient Authority",
                "authority_surface",
                "posture_risk_permission",
                "CoefficientAuthorityDocument",
                disallowed_phrases=[
                    "coefficient authority import",
                    "coefficient authority marker",
                    "coefficient authority path",
                    "coefficient authority seq8",
                    "coefficient authority service",
                    "coefficient modifier authority",
                ],
            ),
            VocabularyEntry(
                "mutable_runtime_surface",
                "Mutable Runtime Surface",
                "authority_class",
                "posture_risk_permission",
                "CoefficientAuthorityRecord",
                allowed_aliases=["runtime mutable"],
            ),
            VocabularyEntry(
                "baseline_only_surface",
                "Baseline-only Surface",
                "authority_class",
                "posture_risk_permission",
                "CoefficientAuthorityRecord",
                allowed_aliases=["baseline only surface"],
                disallowed_phrases=["baseline only"],
            ),
            VocabularyEntry(
                "effective_coefficient_lineage",
                "Effective Coefficient Lineage",
                "review_surface",
                "posture_risk_permission",
                "ResolvedCoefficientValue",
                allowed_aliases=["effective lineage"],
            ),
            VocabularyEntry(
                "state_conditioned_modifier",
                "State-conditioned Modifier",
                "authority_surface",
                "posture_risk_permission",
                "ModifierPolicyRecord",
                allowed_aliases=["state conditioned"],
                disallowed_phrases=[
                    "state conditioned modifier surface",
                    "state conditioned modifier tests",
                ],
            ),
            VocabularyEntry(
                "bounded_dynamic_coefficient",
                "Bounded Dynamic Coefficient",
                "authority_class",
                "posture_risk_permission",
                "CoefficientAuthorityRecord",
                allowed_aliases=["bounded coefficient", "dynamic coefficient"],
            ),
            VocabularyEntry(
                "review_horizon",
                "Review Horizon",
                "promotion_surface",
                "posture_risk_permission",
                "CoefficientReviewHorizon",
            ),
            VocabularyEntry(
                "champion_challenger_evaluation",
                "Champion/Challenger Evaluation",
                "promotion_surface",
                "posture_risk_permission",
                "CoefficientPromotionEvaluation",
            ),
            VocabularyEntry(
                "live_paper_historical_evaluation_separation",
                "Live-paper / Historical Evaluation Separation",
                "promotion_rule",
                "posture_risk_permission",
                "CoefficientEvaluationSeparationRule",
            ),
            VocabularyEntry(
                "stage_input_bundle",
                "Stage Input Bundle",
                "carrier",
                "cognition_ingress",
                "StageInputBundle",
                allowed_aliases=["stageinputbundle"],
                disallowed_phrases=[
                    "sequence7 stage input bundle",
                    "specimen stage input bundle",
                    "stage input bundle json",
                ],
            ),
            VocabularyEntry(
                "environment_assessment",
                "Environment Assessment",
                "parallel_risk_surface",
                "parallel_risk_lane",
                "ParallelRiskEnvironmentAssessment",
                disallowed_phrases=[
                    "bounded environment assessment",
                    "environment assessment import",
                    "environment assessment only",
                ],
            ),
            VocabularyEntry(
                "candidate_audit",
                "Candidate Audit",
                "parallel_risk_surface",
                "parallel_risk_lane",
                "ParallelRiskCandidateAuditSurface",
                disallowed_phrases=["def audit candidate", "return audit candidate"],
            ),
            VocabularyEntry(
                "stage_read_state",
                "Stage-read State",
                "parallel_risk_surface",
                "parallel_risk_lane",
                "ParallelRiskStageReadRecord",
                allowed_aliases=["stage read state", "stage state"],
                disallowed_phrases=["bootstrap stage read state", "read state"],
            ),
            VocabularyEntry(
                "dependency_packet_ids",
                "Dependency Packet IDs",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Lineage.dependencyids",
                allowed_aliases=["dependencyids", "packet ids"],
            ),
            VocabularyEntry(
                "parallel_risk_observation_store",
                "Parallel-risk Observation Store",
                "persistence_surface",
                "parallel_risk_lane",
                "ParallelRiskObservationStore",
            ),
            VocabularyEntry(
                "write_only_persistence",
                "Write-only Persistence",
                "persistence_rule",
                "parallel_risk_lane",
                "ParallelRiskObservationStore.append_observation",
                allowed_aliases=["write only persistence"],
            ),
            VocabularyEntry(
                "append_only_observation_record",
                "Append-only Observation Record",
                "persistence_surface",
                "parallel_risk_lane",
                "ParallelRiskObservationRecord",
                allowed_aliases=["append only observation record"],
                disallowed_phrases=["append only observation record json"],
            ),
            VocabularyEntry(
                "source_temporal_standard",
                "Source Temporal Standard",
                "authority_surface",
                "temporal_context",
                "SourceTemporalStandard",
                disallowed_phrases=[
                    "source temporal standard field",
                    "source temporal standard surface",
                ],
                notes=[
                    "Repo-wide source temporal grammar admitted in docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md."
                ],
            ),
            VocabularyEntry(
                "source_time_raw",
                "source_time_raw",
                "protocol_field",
                "temporal_context",
                "SourceTemporalStandard.source_time_raw",
                disallowed_phrases=["raw source"],
                notes=["Source temporal standard field. Upstream of the DMPV3 outer envelope."],
            ),
            VocabularyEntry(
                "source_time_kind",
                "source_time_kind",
                "protocol_field",
                "temporal_context",
                "SourceTemporalStandard.source_time_kind",
                allowed_aliases=["source kind"],
                notes=["Source temporal standard field. Upstream of the DMPV3 outer envelope."],
            ),
            VocabularyEntry(
                "source_timezone_raw",
                "source_timezone_raw",
                "protocol_field",
                "temporal_context",
                "SourceTemporalStandard.source_timezone_raw",
                allowed_aliases=["source timezone"],
                notes=["Source temporal standard field. Upstream of the DMPV3 outer envelope."],
            ),
            VocabularyEntry(
                "source_time_utc",
                "source_time_utc",
                "protocol_field",
                "temporal_context",
                "SourceTemporalStandard.source_time_utc",
                notes=["Source temporal standard field. Upstream of the DMPV3 outer envelope."],
            ),
            VocabularyEntry(
                "source_date",
                "source_date",
                "protocol_field",
                "temporal_context",
                "SourceTemporalStandard.source_date",
                notes=["Source temporal standard field. Upstream of the DMPV3 outer envelope."],
            ),
            VocabularyEntry(
                "captured_at_utc",
                "captured_at_utc",
                "protocol_field",
                "temporal_context",
                "SourceTemporalStandard.captured_at_utc",
                notes=["Source temporal standard field. Distinct from source observation time."],
            ),
            VocabularyEntry(
                "persisted_at_utc",
                "persisted_at_utc",
                "protocol_field",
                "temporal_context",
                "SourceTemporalStandard.persisted_at_utc",
                notes=["Source temporal standard field. Distinct from source observation time."],
            ),
            VocabularyEntry(
                "source_provider",
                "source_provider",
                "protocol_field",
                "temporal_context",
                "SourceTemporalStandard.source_provider",
                notes=["Source temporal standard field. Upstream provider identity only."],
            ),
            VocabularyEntry(
                "source_channel",
                "source_channel",
                "protocol_field",
                "temporal_context",
                "SourceTemporalStandard.source_channel",
                notes=[
                    "Source temporal standard field. Provider-local acquisition channel or lane."
                ],
            ),
            VocabularyEntry(
                "time_granularity",
                "time_granularity",
                "protocol_field",
                "temporal_context",
                "SourceTemporalStandard.time_granularity",
                notes=[
                    "Source temporal standard field. Records admitted source observation granularity."
                ],
            ),
            VocabularyEntry(
                "next_event_time_utc",
                "next_event_time_utc",
                "protocol_field",
                "temporal_context",
                "TemporalContextInput.next_event_time_utc",
                notes=[
                    "Derived temporal-context field for the next relevant event time after source observation time."
                ],
            ),
            VocabularyEntry(
                "window_start_utc",
                "window_start_utc",
                "protocol_field",
                "temporal_context",
                "TemporalEventWindow.window_start_utc",
                notes=[
                    "Temporal event-window boundary field admitted for governed UTC window starts."
                ],
            ),
            VocabularyEntry(
                "window_end_utc",
                "window_end_utc",
                "protocol_field",
                "temporal_context",
                "TemporalEventWindow.window_end_utc",
                notes=[
                    "Temporal event-window boundary field admitted for governed UTC window ends."
                ],
            ),
            VocabularyEntry(
                "runtime_bar_time_utc",
                "runtime_bar_time_utc",
                "protocol_field",
                "temporal_context",
                "PreparedRuntimeSnapshot.runtime_bar_time_utc",
                notes=[
                    "Prepared-runtime alignment field for the bar time derived from admitted source temporal data."
                ],
            ),
            VocabularyEntry(
                "temporal_conformance_inventory",
                "Temporal Conformance Inventory",
                "audit_surface",
                "temporal_context",
                "TemporalConformanceInventory",
                notes=[
                    "Governed tranche audit inventory surface for repo-wide temporal conformance receipts."
                ],
            ),
            VocabularyEntry(
                "already_conformant",
                "Already Conformant",
                "audit_classification",
                "temporal_context",
                "TemporalConformanceClassification.already_conformant",
                allowed_aliases=["conformant"],
                notes=[
                    "Temporal conformance classification for a surface that already obeys the admitted temporal law."
                ],
            ),
            VocabularyEntry(
                "needs_proof_test_remediation_only",
                "Needs Proof/Test Remediation Only",
                "audit_classification",
                "temporal_context",
                "TemporalConformanceClassification.needs_proof_test_remediation_only",
                allowed_aliases=["needs proof remediation only"],
                notes=[
                    "Temporal conformance classification for a surface where truthful remediation is limited to proof or governor updates."
                ],
            ),
            VocabularyEntry(
                "needs_code_persistence_remediation_in_tranche_3",
                "Needs Code/Persistence Remediation in Tranche 3",
                "audit_classification",
                "temporal_context",
                "TemporalConformanceClassification.needs_code_persistence_remediation_in_tranche_3",
                allowed_aliases=["needs code remediation"],
                notes=[
                    "Temporal conformance classification for a surface that cannot become conformant without runtime or persistence changes deferred to Tranche 3."
                ],
            ),
            VocabularyEntry(
                "reserved_blocked",
                "Reserved / Blocked",
                "audit_classification",
                "temporal_context",
                "TemporalConformanceClassification.reserved_blocked",
                notes=[
                    "Temporal conformance classification for a surface that remains lawfully reserved or blocked in the current tranche."
                ],
            ),
            VocabularyEntry(
                "workbook_temporal_provenance",
                "Workbook Temporal Provenance",
                "authority_surface",
                "temporal_context",
                "SignalWorkbookTemporalProvenanceRule",
                notes=[
                    "Workbook-specific temporal provenance rule admitted in docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md."
                ],
            ),
            VocabularyEntry(
                "field_level_provenance",
                "Field-level Provenance",
                "authority_surface",
                "temporal_context",
                "SignalWorkbookTemporalProvenanceRule.field_level_provenance",
                notes=[
                    "Preserves per-field source-date truth when a workbook row blends different source dates."
                ],
            ),
        ],
    )
    document.validate()
    return document


def build_canonical_vocabulary() -> VocabularyDocument:
    return build_document()


def build_canonical_payload() -> dict:
    return build_document().to_dict()


def governed_source_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in GOVERNED_SOURCE_PATHS:
        if path.exists():
            hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def write_canonical_vocabulary() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(build_canonical_payload(), indent=2) + "\n", encoding="utf-8")
