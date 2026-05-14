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
    Path("src/nvda_desk/schemas/vocabulary.py"),
    Path("src/nvda_desk/vocabulary_builder.py"),
    Path("docs/vocabulary/CONSOLIDATION_WORKFLOW.md"),
    Path("docs/vocabulary/README.md"),
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
                allowed_aliases=["parallel lane"],
            ),
            VocabularyEntry(
                "dmp_v3",
                "DMP V3",
                "protocol",
                "cross_stage_protocol",
                "DmpV3Envelope",
                allowed_aliases=["dmpv3"],
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
            ),
            VocabularyEntry(
                "financial_calendar_import_record",
                "Financial Calendar Import Record",
                "reference_data",
                "calendar_reference",
                "FinancialCalendarImportRecord",
            ),
            VocabularyEntry(
                "coefficient_authority",
                "Coefficient Authority",
                "authority_surface",
                "posture_risk_permission",
                "CoefficientAuthorityDocument",
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
            ),
            VocabularyEntry(
                "bounded_dynamic_coefficient",
                "Bounded Dynamic Coefficient",
                "authority_class",
                "posture_risk_permission",
                "CoefficientAuthorityRecord",
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
            ),
            VocabularyEntry(
                "environment_assessment",
                "Environment Assessment",
                "parallel_risk_surface",
                "parallel_risk_lane",
                "ParallelRiskEnvironmentAssessment",
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
            ),
            VocabularyEntry(
                "dependency_packet_ids",
                "Dependency Packet IDs",
                "protocol_field",
                "cross_stage_protocol",
                "DmpV3Lineage.dependencyids",
                allowed_aliases=["dependencyids"],
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
            ),
            VocabularyEntry(
                "source_temporal_standard",
                "Source Temporal Standard",
                "authority_surface",
                "temporal_context",
                "SourceTemporalStandard",
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
