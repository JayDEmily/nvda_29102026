"""Bounded API dependency composition for the rebuild-phase boundary shell."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from nvda_desk.adapters.egress.api_dto_adapter import ApiDtoAdapter
from nvda_desk.analysis.replay.sidecar import (
    EvaluationRunService,
    PromotionDecisionService,
    ResearchNoteService,
)
from nvda_desk.analysis.replay.walk_forward import StrategicLadderExperimentService
from nvda_desk.calendar.operational.events import (
    OperationalEventRepository,
    OperationalSessionRepository,
)
from nvda_desk.calendar.reference.projection import MarketStateService
from nvda_desk.config import ConfigSurface, RuntimeSettingsDocument, load_runtime_settings
from nvda_desk.config.bundle_loader import DEFAULT_CONFIG_DIR
from nvda_desk.domain.temporal.session_clock import classify_session_state
from nvda_desk.downstream.broker_execution import PaperBrokerExecutionService
from nvda_desk.downstream.daily_pnl import DailyPnlReportService
from nvda_desk.downstream.overnight_carry import (
    CarryHandoffService,
    OvernightCarryMarketService,
    OvernightCarryReplayService,
)
from nvda_desk.persistence.durable_sql import DurableSqliteStore
from nvda_desk.persistence.execution_records import ExecutionRecordsRepository
from nvda_desk.persistence.import_registry import ImportRegistryService
from nvda_desk.repositories.module_registry import ModuleRegistryRepository
from nvda_desk.repositories.position_repository import PositionRepository
from nvda_desk.review.packet_service import ReviewPacketService
from nvda_desk.review.strategic_ladder_replay import StrategicLadderReplayService
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator
from nvda_desk.services.parallel_risk_lane_service import ParallelRiskLaneService
from nvda_desk.upstream.strategic_ladder import StrategicLadderMarketService


def get_config_surface(config_dir: Path | str = DEFAULT_CONFIG_DIR) -> ConfigSurface:
    """Return the bounded config surface used by boundary bootstrap shells."""

    return ConfigSurface(config_dir)


@lru_cache(maxsize=1)
def get_settings_cached() -> RuntimeSettingsDocument:
    """Return one cached runtime-settings document for API dependency consumers."""

    return load_runtime_settings()


def get_runtime_orchestrator() -> DeskRuntimeOrchestrator:
    """Return the bounded runtime orchestrator used by the boundary app shell."""

    return DeskRuntimeOrchestrator()


def get_api_dto_adapter() -> ApiDtoAdapter:
    """Return the admitted DTO projection owner used by the bounded API shell."""

    return ApiDtoAdapter()


@lru_cache(maxsize=1)
def get_session_clock_classifier():
    return classify_session_state


@lru_cache(maxsize=1)
def get_market_state_service() -> MarketStateService:
    return MarketStateService()


@lru_cache(maxsize=1)
def get_module_registry_service() -> ModuleRegistryRepository:
    return ModuleRegistryRepository()


@lru_cache(maxsize=1)
def get_events_service() -> OperationalEventRepository:
    return OperationalEventRepository()


@lru_cache(maxsize=1)
def get_session_calendar_service() -> OperationalSessionRepository:
    return OperationalSessionRepository()


@lru_cache(maxsize=1)
def get_execution_records_service() -> ExecutionRecordsRepository:
    return ExecutionRecordsRepository()


@lru_cache(maxsize=1)
def get_research_service() -> ResearchNoteService:
    return ResearchNoteService()


@lru_cache(maxsize=1)
def get_promotion_service() -> PromotionDecisionService:
    return PromotionDecisionService()


@lru_cache(maxsize=1)
def get_evaluation_log_service() -> EvaluationRunService:
    return EvaluationRunService()


def get_experiment_log_service() -> EvaluationRunService:
    return get_evaluation_log_service()


@lru_cache(maxsize=1)
def get_strategic_ladder_experiment_service() -> StrategicLadderExperimentService:
    return StrategicLadderExperimentService()


@lru_cache(maxsize=1)
def get_import_registry_service() -> ImportRegistryService:
    return ImportRegistryService()


@lru_cache(maxsize=1)
def get_db_session_factory() -> DurableSqliteStore:
    return DurableSqliteStore(Path("var/runtime/api_dependency.sqlite3"))


@lru_cache(maxsize=1)
def get_strategic_ladder_market_service() -> StrategicLadderMarketService:
    return StrategicLadderMarketService()


@lru_cache(maxsize=1)
def get_risk_gateway_service() -> ParallelRiskLaneService:
    return ParallelRiskLaneService()


def get_paper_broker_execution_service() -> PaperBrokerExecutionService:
    return PaperBrokerExecutionService(
        starting_cash=100_000.0, execution_records=get_execution_records_service()
    )


def get_daily_pnl_report_service() -> DailyPnlReportService:
    return DailyPnlReportService()


def get_position_repository() -> PositionRepository:
    return PositionRepository()


@lru_cache(maxsize=1)
def get_carry_handoff_service() -> CarryHandoffService:
    return CarryHandoffService()


@lru_cache(maxsize=1)
def get_overnight_carry_market_service() -> OvernightCarryMarketService:
    return OvernightCarryMarketService()


@lru_cache(maxsize=1)
def get_overnight_carry_replay_service() -> OvernightCarryReplayService:
    return OvernightCarryReplayService()


def get_review_packet_service() -> ReviewPacketService:
    return ReviewPacketService(
        execution_records=get_execution_records_service(),
        position_repository=get_position_repository(),
        daily_pnl_service=get_daily_pnl_report_service(),
    )


@lru_cache(maxsize=1)
def get_strategic_ladder_replay_service() -> StrategicLadderReplayService:
    return StrategicLadderReplayService()
