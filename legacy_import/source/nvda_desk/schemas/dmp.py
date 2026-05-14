"""Desk Module Protocol (DMP) v3 typed packet builders.

This module is the repo-facing wrapper and builder surface for live typed
DMPV3 packets. It keeps the current DMPV3 helper names and compatibility
projections that remain valid for the active packet shape.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.dmp_envelope import DmpV3Envelope, build_dmp_v3_envelope_kwargs

from nvda_desk.schemas.calibration import (
    CoefficientAuditPacket,
    CoefficientSet,
    ComparisonReport,
    ReplayRunResult,
    StackDefinition,
)
from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    MarketRegimeContextOutput,
    OptionsFlowContextOutput,
    PlaybookEligibilityOutput,
    PostureRiskOutput,
    ReviewExplanationOutput,
    TemporalContextOutput,
)
from nvda_desk.schemas.imported_modules.context_scanners import (
    AsiaPrecursorContextFilterContractOutput,
    EngineScoreContractOutput,
    ExecutionContextScoreContractOutput,
    MacroAdaptiveWeightingFilterContractOutput,
    MacroSignalScoreContractOutput,
    OptionsBehaviourClusterContractOutput,
    VixSpreadDetectorContractOutput,
    VolCorridorContractOutput,
)
from nvda_desk.schemas.imported_modules.execution_lifecycle import (
    DynamicPartialExitModelContractOutput,
    ExecutionLogWriterContractOutput,
    ExecutionTagsContractOutput,
    FillFeedbackRouterContractOutput,
    LadderContinuityTrackerContractOutput,
    PositionBookContractOutput,
    TakeProfitContractOutput,
    TradeLoggerContractOutput,
    TradeReentryMarkerContractOutput,
    TrailingStopContractOutput,
    UnrealizedTrackerContractOutput,
)
from nvda_desk.schemas.imported_modules.execution_planning import (
    BrokerAdapterContractOutput,
    EntryPlannerContractOutput,
    OrderSimulatorContractOutput,
    PositionAllocatorContractOutput,
    RunTradingBotContractOutput,
)
from nvda_desk.schemas.imported_modules.ladder_readiness_overlays import (
    VvixLadderShaperContractOutput,
)
from nvda_desk.schemas.imported_modules.market_context_synthesis import (
    RunSignalScanContractOutput,
)
from nvda_desk.schemas.imported_modules.market_substrate import (
    MacroDataCaptureContractOutput,
    OptionsDataCaptureContractOutput,
    OptionsMetadataCaptureContractOutput,
    PeerEquityCaptureContractOutput,
    SpotDataCaptureContractOutput,
    VwapAccumulatorContractOutput,
    VwapRocContractOutput,
)
from nvda_desk.schemas.imported_modules.posture_enrichers import (
    ArchetypeTaggerContractOutput,
    CompressionRegimeDetectorContractOutput,
    FillBiasAdjusterContractOutput,
    ObvViFlowConfirmationContractOutput,
    TailHedgeInjectorContractOutput,
    VolatilitySentimentIndexContractOutput,
)
from nvda_desk.schemas.imported_modules.review_attribution import (
    ConfidenceDivergenceLoggerContractOutput,
    DailySummaryContractOutput,
    FeedbackSummaryWriterContractOutput,
    MacroAlignmentCheckerContractOutput,
    ModuleScoreAttributorContractOutput,
    ModuleTraceAttributionContractOutput,
    ProfitLossLedgerContractOutput,
    VariantPerformanceTrackerContractOutput,
    VariantTraceLoggerContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ArchetypeMatcherContractOutput,
    ConvictionTierAllocatorContractOutput,
    EntryGateContractOutput,
    EventFlagCaptureContractOutput,
    GammaPressureContractOutput,
    IvVsRvAnalysisContractOutput,
    LadderConstructorContractOutput,
    ModelConfidenceScorerContractOutput,
    PeerDivergenceContractOutput,
    RealizedVolatilityEngineContractOutput,
    SignalConflictDetectorContractOutput,
    SkewInflectionContractOutput,
    VolumeSpikeFilterContractOutput,
)


class DmpGrammarRole(StrEnum):
    """Bounded repo-native grammar roles that live DMP packets may carry."""

    TEMPORAL_CONTEXT = "temporal_context"
    MARKET_REGIME_CONTEXT = "market_regime_context"
    OPTIONS_FLOW_CONTEXT = "options_flow_context"
    POSTURE_RISK_PERMISSION = "posture_risk_permission"
    PLAYBOOK_ELIGIBILITY = "playbook_eligibility"
    EXPRESSION_EXECUTION = "expression_execution"
    REVIEW_EXPLANATION = "review_explanation"
    STACK_DEFINITION = "stack_definition"
    COEFFICIENT_SET = "coefficient_set"
    COEFFICIENT_AUDIT = "coefficient_audit"
    REPLAY_RUN_RESULT = "replay_run_result"
    COMPARISON_REPORT = "comparison_report"


class DmpBehaviourClass(StrEnum):
    """High-level behaviour families allowed in live DMP packets."""

    STAGE_OUTPUT = "stage_output"
    MODULE_OUTPUT = "module_output"
    REPLAY_ARTEFACT = "replay_artefact"
    REVIEW_PACKET = "review_packet"


class DmpPacketIdentity(BaseModel):
    """Minimal deterministic identity for one DMP packet."""

    model_config = ConfigDict(extra="forbid")

    packet_id: str = Field(min_length=1)
    emitted_at: datetime


class DmpSchemaIdentifiers(BaseModel):
    """Live schema names attached to one DMP packet."""

    model_config = ConfigDict(extra="forbid")

    payload_model_name: str = Field(min_length=1)
    payload_module_path: str = Field(min_length=1)
    input_model_name: str | None = None
    output_model_name: str | None = None


class DmpTraceReferences(BaseModel):
    """Optional lineage pointers for review and replay attachment later."""

    model_config = ConfigDict(extra="forbid")

    parent_packet_id: str | None = None
    upstream_packet_ids: list[str] = Field(default_factory=list)
    review_trace_id: str | None = None
    replay_trace_id: str | None = None


CognitionStagePayload = (
    TemporalContextOutput
    | MarketRegimeContextOutput
    | OptionsFlowContextOutput
    | PostureRiskOutput
    | PlaybookEligibilityOutput
    | ExecutionExpressionOutput
    | ReviewExplanationOutput
)

CalibrationPayload = (
    StackDefinition | CoefficientSet | CoefficientAuditPacket | ReplayRunResult | ComparisonReport
)

ImportedModulePayload = (
    EventFlagCaptureContractOutput
    | RealizedVolatilityEngineContractOutput
    | VolumeSpikeFilterContractOutput
    | PeerDivergenceContractOutput
    | GammaPressureContractOutput
    | IvVsRvAnalysisContractOutput
    | SkewInflectionContractOutput
    | SignalConflictDetectorContractOutput
    | ModelConfidenceScorerContractOutput
    | ConvictionTierAllocatorContractOutput
    | EntryGateContractOutput
    | LadderConstructorContractOutput
    | ArchetypeMatcherContractOutput
    | SpotDataCaptureContractOutput
    | PeerEquityCaptureContractOutput
    | OptionsDataCaptureContractOutput
    | OptionsMetadataCaptureContractOutput
    | MacroDataCaptureContractOutput
    | VwapAccumulatorContractOutput
    | VwapRocContractOutput
    | MacroSignalScoreContractOutput
    | ExecutionContextScoreContractOutput
    | VixSpreadDetectorContractOutput
    | VolCorridorContractOutput
    | OptionsBehaviourClusterContractOutput
    | AsiaPrecursorContextFilterContractOutput
    | MacroAdaptiveWeightingFilterContractOutput
    | EngineScoreContractOutput
    | RunSignalScanContractOutput
    | VvixLadderShaperContractOutput
    | FillBiasAdjusterContractOutput
    | ArchetypeTaggerContractOutput
    | CompressionRegimeDetectorContractOutput
    | ObvViFlowConfirmationContractOutput
    | TailHedgeInjectorContractOutput
    | VolatilitySentimentIndexContractOutput
    | BrokerAdapterContractOutput
    | EntryPlannerContractOutput
    | PositionAllocatorContractOutput
    | OrderSimulatorContractOutput
    | RunTradingBotContractOutput
    | DynamicPartialExitModelContractOutput
    | TakeProfitContractOutput
    | TrailingStopContractOutput
    | UnrealizedTrackerContractOutput
    | PositionBookContractOutput
    | TradeReentryMarkerContractOutput
    | LadderContinuityTrackerContractOutput
    | FillFeedbackRouterContractOutput
    | ExecutionLogWriterContractOutput
    | ExecutionTagsContractOutput
    | TradeLoggerContractOutput
    | ProfitLossLedgerContractOutput
    | ModuleTraceAttributionContractOutput
    | DailySummaryContractOutput
    | FeedbackSummaryWriterContractOutput
    | ModuleScoreAttributorContractOutput
    | VariantTraceLoggerContractOutput
    | VariantPerformanceTrackerContractOutput
    | ConfidenceDivergenceLoggerContractOutput
    | MacroAlignmentCheckerContractOutput
)

DeskModulePayload = CognitionStagePayload | CalibrationPayload | ImportedModulePayload

class DmpV3Packet[PayloadT: BaseModel](DmpV3Envelope[PayloadT]):
    """DMPV3 packet envelope for one typed repo-native payload."""

    @property
    def packet_identity(self) -> DmpPacketIdentity:
        return DmpPacketIdentity(packet_id=self.packet_id, emitted_at=self.time)

    @property
    def grammar_role(self) -> DmpGrammarRole:
        return DmpGrammarRole(self.producer.grammar_role)

    @property
    def behaviour_class(self) -> DmpBehaviourClass:
        return DmpBehaviourClass(self.producer.behaviour_class)

    @property
    def schema_identifiers(self) -> DmpSchemaIdentifiers:
        compat = self.dmpextensions.get("nvda", {}).get("schema_identifiers", {})
        if isinstance(compat, dict) and {"payload_model_name", "payload_module_path"} <= compat.keys():
            return DmpSchemaIdentifiers.model_validate(compat)
        payload_model = self.data.__class__
        return DmpSchemaIdentifiers(
            payload_model_name=payload_model.__name__,
            payload_module_path=payload_model.__module__,
            output_model_name=payload_model.__name__,
        )

    @property
    def trace_references(self) -> DmpTraceReferences:
        parent_packet_id = self.lineage.parentids[-1] if self.lineage.parentids else None
        return DmpTraceReferences(
            parent_packet_id=parent_packet_id,
            upstream_packet_ids=list(self.lineage.dependencyids),
            review_trace_id=self.lineage.reviewtraceid,
            replay_trace_id=self.lineage.replaytraceid,
        )


DeskModulePacketV3 = DmpV3Packet[DeskModulePayload]


def build_dmp_v3_packet_from_payload(
    *,
    packet_id: str,
    emitted_at: datetime,
    grammar_role: DmpGrammarRole | str,
    behaviour_class: DmpBehaviourClass | str,
    payload: DeskModulePayload,
    trader_summary: str,
    stack_id: str | None = None,
    coefficient_set_id: str | None = None,
    dependencies: list[str] | None = None,
    input_model_name: str | None = None,
    output_model_name: str | None = None,
    parent_packet_ids: list[str] | None = None,
    dependency_packet_ids: list[str] | None = None,
    review_trace_id: str | None = None,
    replay_trace_id: str | None = None,
    decision_trace_id: str | None = None,
    trace_id: str | None = None,
    run_id: str | None = None,
    scenario_id: str | None = None,
    module_id: str | None = None,
    module_version: str = "1.0.0",
    module_instance_id: str | None = None,
    stage_name: str | None = None,
    registry_version: str | None = None,
    environment_tag: str | None = None,
    dmpextensions: dict[str, Any] | None = None,
) -> DeskModulePacketV3:
    """Build one DMPV3 packet directly from a typed payload model."""

    grammar_role_value = (
        grammar_role.value if isinstance(grammar_role, DmpGrammarRole) else str(grammar_role)
    )
    behaviour_class_value = (
        behaviour_class.value
        if isinstance(behaviour_class, DmpBehaviourClass)
        else str(behaviour_class)
    )
    return DeskModulePacketV3(
        **build_dmp_v3_envelope_kwargs(
            packet_id=packet_id,
            emitted_at=emitted_at,
            grammar_role=grammar_role_value,
            behaviour_class=behaviour_class_value,
            payload=payload,
            trader_summary=trader_summary,
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=dependencies,
            input_model_name=input_model_name,
            output_model_name=output_model_name,
            parent_packet_ids=parent_packet_ids,
            dependency_packet_ids=dependency_packet_ids,
            review_trace_id=review_trace_id,
            replay_trace_id=replay_trace_id,
            decision_trace_id=decision_trace_id,
            trace_id=trace_id,
            run_id=run_id,
            scenario_id=scenario_id,
            module_id=module_id,
            module_version=module_version,
            module_instance_id=module_instance_id,
            stage_name=stage_name,
            registry_version=registry_version,
            environment_tag=environment_tag,
            dmpextensions=dmpextensions,
            summary_keyflags=[],
        )
    )

