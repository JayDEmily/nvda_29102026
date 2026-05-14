from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query

from nvda_desk.api.deps import (
    get_capital_allocator_service,
    get_config_surface_service,
    get_evaluation_log_service,
    get_events_service,
    get_execution_records_service,
    get_experiment_log_service,
    get_market_state_service,
    get_module_registry_service,
    get_overnight_carry_market_service,
    get_overnight_carry_replay_service,
    get_promotion_service,
    get_replay_service,
    get_research_service,
    get_review_packet_service,
    get_risk_gateway_service,
    get_strategic_ladder_experiment_service,
    get_strategic_ladder_market_service,
    get_strategic_ladder_replay_service,
)
from nvda_desk.config_models import EvaluationConfigDocument, RuntimeSettingsDocument
from nvda_desk.schemas.allocation import (
    ModuleRegimeCapitalAllocationInput,
    ModuleRegimeCapitalAllocationOutput,
)
from nvda_desk.schemas.config import (
    CoefficientGroupListResponse,
    CoefficientGroupPayload,
    StrategyVariantListResponse,
    StrategyVariantPayload,
)
from nvda_desk.schemas.eval import (
    EvaluationRunListResponse,
    EvaluationRunPayload,
    EvalVerdict,
    ExperimentRunListResponse,
    ExperimentType,
    StrategicLadderBatchRankingInput,
    StrategicLadderBatchRankingOutput,
    StrategicLadderFragilityInput,
    StrategicLadderFragilityOutput,
    StrategicLadderWalkForwardInput,
    StrategicLadderWalkForwardOutput,
)
from nvda_desk.schemas.events import (
    EventProximityResponse,
    MarketEventCreate,
    MarketEventListResponse,
    MarketEventPayload,
    SessionCalendarCreate,
    SessionCalendarListResponse,
    SessionCalendarPayload,
)
from nvda_desk.schemas.execution_records import (
    BrokerFillEventListResponse,
    BrokerOrderEventListResponse,
    BrokerOrderPayload,
    BrokerPaperOrderInput,
    CapitalStateSnapshotPayload,
    DailyPnlReportCreate,
    DailyPnlReportListResponse,
    DailyPnlReportPayload,
    ModuleSignalEventCreate,
    ModuleSignalEventListResponse,
    ModuleSignalEventPayload,
    ModuleVetoEventCreate,
    ModuleVetoEventListResponse,
    ModuleVetoEventPayload,
    PositionInstanceSnapshotListResponse,
    PositionSnapshotListResponse,
    RiskBlockEventCreate,
    RiskBlockEventListResponse,
    RiskBlockEventPayload,
)
from nvda_desk.schemas.market import IntradayBarsResponse, MarketSnapshotResponse
from nvda_desk.schemas.module import (
    ModuleSpecCreate,
    ModuleSpecListResponse,
    ModuleSpecPayload,
    PromotionDecisionCreate,
    PromotionDecisionListResponse,
    PromotionDecisionPayload,
)
from nvda_desk.schemas.options import OptionSurfaceResponse, OptionType
from nvda_desk.schemas.overnight import (
    CarryRecommendation,
    OvernightCarryEvaluatorInput,
    OvernightCarryEvaluatorOutput,
    OvernightCarryMarketInput,
    OvernightCarryMarketOutput,
    OvernightCarryReplayFromMarketInput,
    OvernightCarryReplayFromMarketOutput,
)
from nvda_desk.schemas.replay import ReplaySessionResponse
from nvda_desk.schemas.research import (
    ResearchNoteCreate,
    ResearchNoteListResponse,
    ResearchNotePayload,
)
from nvda_desk.schemas.review import DailyReviewPacket, ModuleHealthPacket
from nvda_desk.schemas.risk import (
    RiskDecisionListResponse,
    RiskDecisionPayload,
    RiskPolicyInput,
)
from nvda_desk.schemas.session_clock import SessionClockFeaturePayload
from nvda_desk.schemas.slv import (
    LadderOverallDecision,
    StrategicLadderReplayInput,
    StrategicLadderReplayOutput,
    StrategicLadderValidatorInput,
    StrategicLadderValidatorMarketInput,
    StrategicLadderValidatorMarketOutput,
    StrategicLadderValidatorOutput,
)
from nvda_desk.schemas.temporal_surface import TemporalStateFeaturePayload
from nvda_desk.services.capital_allocator import CapitalAllocatorService
from nvda_desk.services.carry_market import OvernightCarryMarketService
from nvda_desk.services.carry_replay import OvernightCarryReplayService
from nvda_desk.services.config_surface import (
    ConfigSurfaceLookupError,
    ConfigSurfaceService,
)
from nvda_desk.services.evaluation_log import EvaluationLogService
from nvda_desk.services.events import EventsService
from nvda_desk.services.execution_records import ExecutionRecordsService
from nvda_desk.services.experiment_log import ExperimentLogService
from nvda_desk.services.market_state import MarketStateService
from nvda_desk.services.module_evaluators import (
    OvernightCarryEvaluatorService,
    StrategicLadderValidatorService,
)
from nvda_desk.services.module_registry import ModuleRegistryService
from nvda_desk.services.promotion import PromotionService
from nvda_desk.services.replay import ReplayService
from nvda_desk.services.research import ResearchService
from nvda_desk.services.review_packets import ReviewPacketService
from nvda_desk.services.risk_gateway import RiskGatewayService
from nvda_desk.services.slv_experiments import StrategicLadderExperimentService
from nvda_desk.services.slv_market import StrategicLadderMarketService
from nvda_desk.services.slv_replay import StrategicLadderReplayService

app = FastAPI(title="NVDA Desk API", version="0.1.0")
MarketStateDep = Annotated[MarketStateService, Depends(get_market_state_service)]
ResearchDep = Annotated[ResearchService, Depends(get_research_service)]
EvalLogDep = Annotated[EvaluationLogService, Depends(get_evaluation_log_service)]
ExperimentLogDep = Annotated[ExperimentLogService, Depends(get_experiment_log_service)]
EventsDep = Annotated[EventsService, Depends(get_events_service)]
ExecutionRecordsDep = Annotated[ExecutionRecordsService, Depends(get_execution_records_service)]
ReplayDep = Annotated[ReplayService, Depends(get_replay_service)]
ModuleRegistryDep = Annotated[ModuleRegistryService, Depends(get_module_registry_service)]
PromotionDep = Annotated[PromotionService, Depends(get_promotion_service)]
SLVMarketDep = Annotated[StrategicLadderMarketService, Depends(get_strategic_ladder_market_service)]
SLVReplayDep = Annotated[StrategicLadderReplayService, Depends(get_strategic_ladder_replay_service)]
SLVExperimentDep = Annotated[
    StrategicLadderExperimentService,
    Depends(get_strategic_ladder_experiment_service),
]
CarryMarketDep = Annotated[OvernightCarryMarketService, Depends(get_overnight_carry_market_service)]
CarryReplayDep = Annotated[OvernightCarryReplayService, Depends(get_overnight_carry_replay_service)]
RiskGatewayDep = Annotated[RiskGatewayService, Depends(get_risk_gateway_service)]
CapitalAllocatorDep = Annotated[CapitalAllocatorService, Depends(get_capital_allocator_service)]
ConfigSurfaceDep = Annotated[ConfigSurfaceService, Depends(get_config_surface_service)]
ReviewPacketDep = Annotated[ReviewPacketService, Depends(get_review_packet_service)]
TimestampQuery = Annotated[datetime | None, Query(description="UTC or timezone-aware timestamp")]
StartTimestampQuery = Annotated[
    datetime, Query(description="Inclusive UTC or timezone-aware start timestamp")
]
EndTimestampQuery = Annotated[
    datetime, Query(description="Inclusive UTC or timezone-aware end timestamp")
]
SymbolQuery = Annotated[str, Query(description="Requested symbol", min_length=1)]
LimitQuery = Annotated[int, Query(description="Maximum bars to return", ge=1, le=390)]
OptionTypeQuery = Annotated[OptionType | None, Query(description="Optional option side filter")]
ResearchLimitQuery = Annotated[int, Query(description="Maximum notes to return", ge=1, le=100)]
ModuleLimitQuery = Annotated[
    int, Query(description="Maximum specs or decisions to return", ge=1, le=100)
]
ModuleIdQuery = Annotated[str | None, Query(description="Optional module_id filter", min_length=1)]
ExperimentTypeQuery = Annotated[
    ExperimentType | None, Query(description="Optional experiment type filter")
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/config/runtime-settings")
def get_runtime_settings(
    service: ConfigSurfaceDep = None,  # type: ignore[assignment]
) -> RuntimeSettingsDocument:
    assert service is not None
    return service.runtime_settings()


@app.get("/config/evaluation-settings")
def get_evaluation_settings(
    service: ConfigSurfaceDep = None,  # type: ignore[assignment]
) -> EvaluationConfigDocument:
    assert service is not None
    return service.evaluation_config()


@app.get("/config/coefficients")
def list_coefficients(
    service: ConfigSurfaceDep = None,  # type: ignore[assignment]
) -> CoefficientGroupListResponse:
    assert service is not None
    return service.list_coefficient_groups()


@app.get("/config/coefficients/{group_key}")
def get_coefficient_group(
    group_key: str,
    service: ConfigSurfaceDep = None,  # type: ignore[assignment]
) -> CoefficientGroupPayload:
    assert service is not None
    try:
        return service.get_coefficient_group(group_key)
    except ConfigSurfaceLookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/config/strategy-variants")
def list_strategy_variants(
    service: ConfigSurfaceDep = None,  # type: ignore[assignment]
) -> StrategyVariantListResponse:
    assert service is not None
    return service.list_strategy_variants()


@app.get("/config/strategy-variants/{variant_name}")
def get_strategy_variant(
    variant_name: str,
    service: ConfigSurfaceDep = None,  # type: ignore[assignment]
) -> StrategyVariantPayload:
    assert service is not None
    try:
        return service.get_strategy_variant(variant_name)
    except ConfigSurfaceLookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/market/temporal-state")
def market_temporal_state(
    ts: TimestampQuery = None,
    service: MarketStateDep = None,  # type: ignore[assignment]
) -> TemporalStateFeaturePayload:
    effective_ts = ts or datetime.now(tz=UTC)
    assert service is not None
    return service.get_temporal_state(effective_ts)


@app.get("/market/session-clock")
def market_session_clock(
    ts: TimestampQuery = None,
    service: MarketStateDep = None,  # type: ignore[assignment]
) -> SessionClockFeaturePayload:
    effective_ts = ts or datetime.now(tz=UTC)
    assert service is not None
    return service.get_session_clock(effective_ts)


@app.get("/market/snapshot")
def market_snapshot(
    symbol: SymbolQuery = "NVDA",
    ts: TimestampQuery = None,
    service: MarketStateDep = None,  # type: ignore[assignment]
) -> MarketSnapshotResponse:
    effective_ts = ts or datetime.now(tz=UTC)
    assert service is not None
    return service.get_market_snapshot(symbol=symbol, ts=effective_ts)


@app.get("/market/intraday")
def market_intraday(
    symbol: SymbolQuery = "NVDA",
    ts: TimestampQuery = None,
    limit: LimitQuery = 30,
    service: MarketStateDep = None,  # type: ignore[assignment]
) -> IntradayBarsResponse:
    effective_ts = ts or datetime.now(tz=UTC)
    assert service is not None
    return service.get_intraday_bars(symbol=symbol, ts=effective_ts, limit=limit)


@app.get("/market/options-surface")
def market_option_surface(
    symbol: SymbolQuery = "NVDA",
    as_of_date: Annotated[
        datetime, Query(description="Date whose YYYY-MM-DD portion is used")
    ] = datetime(2025, 4, 11, tzinfo=UTC),
    expiry: Annotated[
        datetime | None,
        Query(description="Optional expiry date whose YYYY-MM-DD portion is used"),
    ] = None,
    option_type: OptionTypeQuery = None,
    service: MarketStateDep = None,  # type: ignore[assignment]
) -> OptionSurfaceResponse:
    assert service is not None
    as_of = as_of_date.date()
    expiry_date = expiry.date() if expiry is not None else None
    return service.get_option_surface(
        symbol=symbol,
        as_of_date=as_of,
        requested_at=datetime.now(tz=UTC),
        expiry=expiry_date,
        option_type=option_type,
    )


@app.post("/events/calendar")
def create_session_calendar(
    payload: SessionCalendarCreate,
    service: EventsDep = None,  # type: ignore[assignment]
) -> SessionCalendarPayload:
    assert service is not None
    return service.create_session(payload)


@app.get("/events/calendar")
def list_session_calendars(
    limit: ModuleLimitQuery = 20,
    service: EventsDep = None,  # type: ignore[assignment]
) -> SessionCalendarListResponse:
    assert service is not None
    return service.list_sessions(limit=limit)


@app.post("/events/market")
def create_market_event(
    payload: MarketEventCreate,
    service: EventsDep = None,  # type: ignore[assignment]
) -> MarketEventPayload:
    assert service is not None
    return service.create_event(payload)


@app.get("/events/market")
def list_market_events(
    symbol: SymbolQuery = "NVDA",
    limit: ModuleLimitQuery = 20,
    service: EventsDep = None,  # type: ignore[assignment]
) -> MarketEventListResponse:
    assert service is not None
    return service.list_events(symbol=symbol, limit=limit)


@app.get("/events/proximity")
def event_proximity(
    ts: TimestampQuery = None,
    symbol: SymbolQuery = "NVDA",
    service: EventsDep = None,  # type: ignore[assignment]
) -> EventProximityResponse:
    effective_ts = ts or datetime.now(tz=UTC)
    assert service is not None
    return service.get_proximity(requested_at=effective_ts, symbol=symbol)


@app.get("/replay/session-phases")
def replay_session_phases(
    symbol: SymbolQuery = "NVDA",
    start_ts: StartTimestampQuery = datetime(2026, 3, 18, 13, 30, tzinfo=UTC),
    end_ts: EndTimestampQuery = datetime(2026, 3, 18, 17, 29, tzinfo=UTC),
    service: ReplayDep = None,  # type: ignore[assignment]
) -> ReplaySessionResponse:
    assert service is not None
    return service.replay_session_phases(symbol=symbol, start_ts=start_ts, end_ts=end_ts)


@app.post("/research/notes")
def create_research_note(
    payload: ResearchNoteCreate,
    service: ResearchDep = None,  # type: ignore[assignment]
) -> ResearchNotePayload:
    assert service is not None
    return service.create_note(payload)


@app.get("/research/notes")
def list_research_notes(
    limit: ResearchLimitQuery = 20,
    service: ResearchDep = None,  # type: ignore[assignment]
) -> ResearchNoteListResponse:
    assert service is not None
    return service.list_notes(limit=limit)


@app.post("/modules/specs")
def create_module_spec(
    payload: ModuleSpecCreate,
    service: ModuleRegistryDep = None,  # type: ignore[assignment]
) -> ModuleSpecPayload:
    assert service is not None
    return service.create_spec(payload)


@app.get("/modules/specs")
def list_module_specs(
    limit: ModuleLimitQuery = 20,
    service: ModuleRegistryDep = None,  # type: ignore[assignment]
) -> ModuleSpecListResponse:
    assert service is not None
    return service.list_specs(limit=limit)


@app.post("/modules/promotions")
def create_promotion_decision(
    payload: PromotionDecisionCreate,
    service: PromotionDep = None,  # type: ignore[assignment]
) -> PromotionDecisionPayload:
    assert service is not None
    return service.record_decision(payload)


@app.get("/modules/promotions")
def list_promotion_decisions(
    module_id: ModuleIdQuery = None,
    limit: ModuleLimitQuery = 20,
    service: PromotionDep = None,  # type: ignore[assignment]
) -> PromotionDecisionListResponse:
    assert service is not None
    return service.list_decisions(module_id=module_id, limit=limit)


@app.post("/modules/strategic-ladder-validator/evaluate")
def evaluate_strategic_ladder(
    payload: StrategicLadderValidatorInput,
) -> StrategicLadderValidatorOutput:
    service = StrategicLadderValidatorService()
    return service.evaluate(payload)


@app.post("/modules/strategic-ladder-validator/evaluate-from-market")
def evaluate_strategic_ladder_from_market(
    payload: StrategicLadderValidatorMarketInput,
    service: SLVMarketDep = None,  # type: ignore[assignment]
) -> StrategicLadderValidatorMarketOutput:
    assert service is not None
    return service.evaluate_from_market(payload)


@app.post("/modules/strategic-ladder-validator/replay-from-market")
def replay_strategic_ladder_from_market(
    payload: StrategicLadderReplayInput,
    service: SLVReplayDep = None,  # type: ignore[assignment]
) -> StrategicLadderReplayOutput:
    assert service is not None
    return service.replay_from_market(payload)


@app.post("/modules/overnight-carry-evaluator/evaluate")
def evaluate_overnight_carry(
    payload: OvernightCarryEvaluatorInput,
) -> OvernightCarryEvaluatorOutput:
    service = OvernightCarryEvaluatorService()
    return service.evaluate(payload)


@app.post("/modules/overnight-carry-evaluator/evaluate-from-market")
def evaluate_overnight_carry_from_market(
    payload: OvernightCarryMarketInput,
    service: CarryMarketDep = None,  # type: ignore[assignment]
) -> OvernightCarryMarketOutput:
    assert service is not None
    return service.evaluate_from_market(payload)


@app.get("/evals/runs")
def list_evaluation_runs(
    module_id: ModuleIdQuery = None,
    limit: ModuleLimitQuery = 20,
    service: EvalLogDep = None,  # type: ignore[assignment]
) -> EvaluationRunListResponse:
    assert service is not None
    return service.list_runs(module_id=module_id, limit=limit)


@app.get("/evals/experiments")
def list_experiment_runs(
    module_id: ModuleIdQuery = None,
    experiment_type: ExperimentTypeQuery = None,
    limit: ModuleLimitQuery = 20,
    service: ExperimentLogDep = None,  # type: ignore[assignment]
) -> ExperimentRunListResponse:
    assert service is not None
    return service.list_runs(module_id=module_id, experiment_type=experiment_type, limit=limit)


@app.post("/evals/strategic-ladder-validator")
def record_strategic_ladder_evaluation(
    payload: StrategicLadderValidatorInput,
    service: EvalLogDep = None,  # type: ignore[assignment]
) -> EvaluationRunPayload:
    assert service is not None
    result = StrategicLadderValidatorService().evaluate(payload)
    verdict = _slv_verdict(result)
    return service.record(
        symbol=payload.symbol,
        descriptor=payload.descriptor,
        requested_at=datetime.now(tz=UTC),
        verdict=verdict,
        score=result.ladder_validity_score,
        input_payload=payload,
        output_payload=result,
    )


@app.post("/evals/strategic-ladder-validator/from-market")
def record_strategic_ladder_market_evaluation(
    payload: StrategicLadderValidatorMarketInput,
    service: EvalLogDep = None,  # type: ignore[assignment]
    slv_market_service: SLVMarketDep = None,  # type: ignore[assignment]
) -> EvaluationRunPayload:
    assert service is not None
    assert slv_market_service is not None
    result = slv_market_service.evaluate_from_market(payload)
    verdict = _slv_verdict(result)
    return service.record(
        symbol=payload.symbol,
        descriptor=payload.descriptor,
        requested_at=datetime.now(tz=UTC),
        verdict=verdict,
        score=result.ladder_validity_score,
        input_payload=payload,
        output_payload=result,
    )


@app.post("/evals/strategic-ladder-validator/replay-from-market")
def record_strategic_ladder_replay_evaluation(
    payload: StrategicLadderReplayInput,
    service: EvalLogDep = None,  # type: ignore[assignment]
    slv_replay_service: SLVReplayDep = None,  # type: ignore[assignment]
) -> EvaluationRunPayload:
    assert service is not None
    assert slv_replay_service is not None
    result = slv_replay_service.replay_from_market(payload)
    verdict = _slv_verdict(result)
    return service.record(
        symbol=payload.symbol,
        descriptor=payload.descriptor,
        requested_at=payload.entry_ts,
        verdict=verdict,
        score=result.replay_score,
        input_payload=payload,
        output_payload=result,
    )


@app.post("/evals/strategic-ladder-validator/walk-forward-from-market")
def run_slv_walk_forward_from_market(
    payload: StrategicLadderWalkForwardInput,
    service: SLVExperimentDep = None,  # type: ignore[assignment]
) -> StrategicLadderWalkForwardOutput:
    assert service is not None
    try:
        return service.walk_forward_from_market(payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/evals/strategic-ladder-validator/fragility-from-market")
def run_slv_fragility_from_market(
    payload: StrategicLadderFragilityInput,
    service: SLVExperimentDep = None,  # type: ignore[assignment]
) -> StrategicLadderFragilityOutput:
    assert service is not None
    try:
        return service.fragility_from_market(payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/evals/strategic-ladder-validator/batch-rank-from-market")
def run_slv_batch_rank_from_market(
    payload: StrategicLadderBatchRankingInput,
    service: SLVExperimentDep = None,  # type: ignore[assignment]
) -> StrategicLadderBatchRankingOutput:
    assert service is not None
    try:
        return service.batch_rank_from_market(payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/evals/overnight-carry-evaluator")
def record_overnight_carry_evaluation(
    payload: OvernightCarryEvaluatorInput,
    service: EvalLogDep = None,  # type: ignore[assignment]
) -> EvaluationRunPayload:
    assert service is not None
    result = OvernightCarryEvaluatorService().evaluate(payload)
    verdict, score = _overnight_verdict_and_score(result)
    return service.record(
        symbol=payload.symbol,
        descriptor=payload.descriptor,
        requested_at=datetime.now(tz=UTC),
        verdict=verdict,
        score=score,
        input_payload=payload,
        output_payload=result,
    )


@app.post("/evals/overnight-carry-evaluator/from-market")
def record_overnight_carry_market_evaluation(
    payload: OvernightCarryMarketInput,
    service: EvalLogDep = None,  # type: ignore[assignment]
    carry_market_service: CarryMarketDep = None,  # type: ignore[assignment]
) -> EvaluationRunPayload:
    assert service is not None
    assert carry_market_service is not None
    result = carry_market_service.evaluate_from_market(payload)
    verdict, score = _overnight_verdict_and_score(result)
    return service.record(
        symbol=payload.symbol,
        descriptor=payload.descriptor,
        requested_at=payload.evaluation_ts,
        verdict=verdict,
        score=score,
        input_payload=payload,
        output_payload=result,
    )


@app.post("/evals/overnight-carry-evaluator/replay-from-market")
def replay_overnight_carry_from_market(
    payload: OvernightCarryReplayFromMarketInput,
    service: CarryReplayDep = None,  # type: ignore[assignment]
) -> OvernightCarryReplayFromMarketOutput:
    assert service is not None
    return service.replay_from_market(payload)


@app.post("/risk/evaluate")
def evaluate_risk_policy(
    payload: RiskPolicyInput,
    service: RiskGatewayDep = None,  # type: ignore[assignment]
) -> RiskDecisionPayload:
    assert service is not None
    return service.record(payload)


@app.get("/risk/decisions")
def list_risk_decisions(
    module_id: ModuleIdQuery = None,
    limit: ModuleLimitQuery = 20,
    service: RiskGatewayDep = None,  # type: ignore[assignment]
) -> RiskDecisionListResponse:
    assert service is not None
    return service.list_decisions(module_id=module_id, limit=limit)


@app.post("/allocation/module-regime")
def allocate_module_capital(
    payload: ModuleRegimeCapitalAllocationInput,
    service: CapitalAllocatorDep = None,  # type: ignore[assignment]
) -> ModuleRegimeCapitalAllocationOutput:
    assert service is not None
    try:
        return service.allocate(payload)
    except ConfigSurfaceLookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/execution/signals")
def record_signal_event(
    payload: ModuleSignalEventCreate,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> ModuleSignalEventPayload:
    assert service is not None
    return service.record_signal(payload)


@app.get("/execution/signals")
def list_signal_events(
    module_id: ModuleIdQuery = None,
    limit: ModuleLimitQuery = 20,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> ModuleSignalEventListResponse:
    assert service is not None
    return service.list_signals(module_id=module_id, limit=limit)


@app.post("/execution/vetoes")
def record_veto_event(
    payload: ModuleVetoEventCreate,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> ModuleVetoEventPayload:
    assert service is not None
    return service.record_veto(payload)


@app.get("/execution/vetoes")
def list_veto_events(
    module_id: ModuleIdQuery = None,
    limit: ModuleLimitQuery = 20,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> ModuleVetoEventListResponse:
    assert service is not None
    return service.list_vetoes(module_id=module_id, limit=limit)


@app.post("/execution/risk-blocks")
def record_risk_block_event(
    payload: RiskBlockEventCreate,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> RiskBlockEventPayload:
    assert service is not None
    return service.record_risk_block(payload)


@app.get("/execution/risk-blocks")
def list_risk_block_events(
    module_id: ModuleIdQuery = None,
    limit: ModuleLimitQuery = 20,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> RiskBlockEventListResponse:
    assert service is not None
    return service.list_risk_blocks(module_id=module_id, limit=limit)


@app.post("/execution/daily-pnl")
def record_daily_pnl_report(
    payload: DailyPnlReportCreate,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> DailyPnlReportPayload:
    assert service is not None
    return service.record_daily_pnl(payload)


@app.get("/execution/daily-pnl")
def list_daily_pnl_reports(
    symbol: SymbolQuery = "NVDA",
    limit: ModuleLimitQuery = 20,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> DailyPnlReportListResponse:
    assert service is not None
    return service.list_daily_pnl(symbol=symbol, limit=limit)


@app.post("/broker/orders/paper")
def place_paper_order(
    payload: BrokerPaperOrderInput,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> BrokerOrderPayload:
    assert service is not None
    return service.place_paper_order(payload)


@app.get("/broker/order-events")
def list_broker_order_events(
    limit: ModuleLimitQuery = 20,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> BrokerOrderEventListResponse:
    assert service is not None
    return service.list_order_events(limit=limit)


@app.get("/broker/fill-events")
def list_broker_fill_events(
    limit: ModuleLimitQuery = 20,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> BrokerFillEventListResponse:
    assert service is not None
    return service.list_fill_events(limit=limit)


@app.get("/broker/positions")
def list_broker_positions(
    symbol: SymbolQuery = "NVDA",
    limit: ModuleLimitQuery = 20,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> PositionSnapshotListResponse:
    assert service is not None
    return service.list_positions(symbol=symbol, limit=limit)


@app.get("/broker/position-instances")
def list_broker_position_instances(
    symbol: SymbolQuery = "NVDA",
    position_instance_ref: str | None = None,
    limit: ModuleLimitQuery = 20,
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> PositionInstanceSnapshotListResponse:
    assert service is not None
    return service.list_position_instances(
        symbol=symbol,
        position_instance_ref=position_instance_ref,
        limit=limit,
    )


@app.get("/broker/account-state")
def get_broker_account_state(
    service: ExecutionRecordsDep = None,  # type: ignore[assignment]
) -> CapitalStateSnapshotPayload:
    assert service is not None
    return service.latest_capital_state()


@app.get("/review/module-health/{module_id}")
def get_module_health_packet(
    module_id: str,
    service: ReviewPacketDep = None,  # type: ignore[assignment]
) -> ModuleHealthPacket:
    assert service is not None
    return service.module_health(module_id)


@app.get("/review/daily-packet")
def get_daily_review_packet(
    report_date: Annotated[datetime, Query(description="Requested report date timestamp")],
    symbol: SymbolQuery = "NVDA",
    service: ReviewPacketDep = None,  # type: ignore[assignment]
) -> DailyReviewPacket:
    assert service is not None
    return service.daily_packet(report_date=report_date.date(), symbol=symbol)


def _slv_verdict(
    result: (
        StrategicLadderValidatorOutput
        | StrategicLadderValidatorMarketOutput
        | StrategicLadderReplayOutput
    ),
) -> EvalVerdict:
    if result.overall_decision is LadderOverallDecision.ACCEPT:
        return "pass"
    if result.overall_decision is LadderOverallDecision.ADJUST:
        return "review"
    return "fail"


def _overnight_verdict_and_score(
    result: OvernightCarryEvaluatorOutput | OvernightCarryMarketOutput,
) -> tuple[EvalVerdict, float]:
    if result.carry_recommendation is CarryRecommendation.INCREASE:
        return "pass", 0.8
    if result.carry_recommendation is CarryRecommendation.HOLD_SMALL:
        return "review", 0.6
    if result.carry_recommendation is CarryRecommendation.FLATTEN:
        return "review", 0.4
    return "fail", 0.1
