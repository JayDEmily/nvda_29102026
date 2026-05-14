from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.config import Settings, get_settings
from nvda_desk.db.session import create_session_factory
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.services.capital_allocator import CapitalAllocatorService
from nvda_desk.services.carry_market import OvernightCarryMarketService
from nvda_desk.services.carry_replay import OvernightCarryReplayService
from nvda_desk.services.config_surface import ConfigSurfaceService
from nvda_desk.services.evaluation_log import EvaluationLogService
from nvda_desk.services.events import EventsService
from nvda_desk.services.execution_records import ExecutionRecordsService
from nvda_desk.services.experiment_log import ExperimentLogService
from nvda_desk.services.market_state import MarketStateService
from nvda_desk.services.module_registry import ModuleRegistryService
from nvda_desk.services.promotion import PromotionService
from nvda_desk.services.replay import ReplayService
from nvda_desk.services.research import ResearchService
from nvda_desk.services.review_packets import ReviewPacketService
from nvda_desk.services.risk_gateway import RiskGatewayService
from nvda_desk.services.slv_experiments import StrategicLadderExperimentService
from nvda_desk.services.slv_market import StrategicLadderMarketService
from nvda_desk.services.slv_replay import StrategicLadderReplayService


@lru_cache(maxsize=1)
def get_settings_cached() -> Settings:
    return get_settings()


@lru_cache(maxsize=1)
def get_db_session_factory() -> sessionmaker[Session]:
    settings = get_settings_cached()
    return create_session_factory(settings.database_url)


@lru_cache(maxsize=1)
def get_session_clock_classifier() -> SessionClockClassifier:
    settings = get_settings_cached()
    return SessionClockClassifier(settings)


@lru_cache(maxsize=1)
def get_config_surface_service() -> ConfigSurfaceService:
    config_dir = Path(__file__).resolve().parents[3] / "config"
    return ConfigSurfaceService(config_dir)


@lru_cache(maxsize=1)
def get_market_state_service() -> MarketStateService:
    return MarketStateService(
        get_session_clock_classifier(), session_factory=get_db_session_factory()
    )


@lru_cache(maxsize=1)
def get_research_service() -> ResearchService:
    return ResearchService(get_db_session_factory())


@lru_cache(maxsize=1)
def get_evaluation_log_service() -> EvaluationLogService:
    return EvaluationLogService(get_db_session_factory())


@lru_cache(maxsize=1)
def get_replay_service() -> ReplayService:
    return ReplayService(get_session_clock_classifier(), get_db_session_factory())


@lru_cache(maxsize=1)
def get_module_registry_service() -> ModuleRegistryService:
    return ModuleRegistryService(get_db_session_factory())


@lru_cache(maxsize=1)
def get_promotion_service() -> PromotionService:
    return PromotionService(get_db_session_factory())


@lru_cache(maxsize=1)
def get_experiment_log_service() -> ExperimentLogService:
    return ExperimentLogService(get_db_session_factory())


@lru_cache(maxsize=1)
def get_events_service() -> EventsService:
    return EventsService(get_db_session_factory())


@lru_cache(maxsize=1)
def get_execution_records_service() -> ExecutionRecordsService:
    return ExecutionRecordsService(get_db_session_factory())


@lru_cache(maxsize=1)
def get_strategic_ladder_market_service() -> StrategicLadderMarketService:
    return StrategicLadderMarketService(get_db_session_factory())


@lru_cache(maxsize=1)
def get_risk_gateway_service() -> RiskGatewayService:
    return RiskGatewayService(get_db_session_factory())


@lru_cache(maxsize=1)
def get_strategic_ladder_replay_service() -> StrategicLadderReplayService:
    return StrategicLadderReplayService(
        get_db_session_factory(),
        get_session_clock_classifier(),
        get_market_state_service(),
        get_strategic_ladder_market_service(),
        get_risk_gateway_service(),
    )


@lru_cache(maxsize=1)
def get_strategic_ladder_experiment_service() -> StrategicLadderExperimentService:
    return StrategicLadderExperimentService(
        get_session_clock_classifier(),
        get_market_state_service(),
        get_strategic_ladder_replay_service(),
        get_experiment_log_service(),
        get_config_surface_service(),
    )


@lru_cache(maxsize=1)
def get_capital_allocator_service() -> CapitalAllocatorService:
    return CapitalAllocatorService(get_experiment_log_service(), get_config_surface_service())


@lru_cache(maxsize=1)
def get_overnight_carry_market_service() -> OvernightCarryMarketService:
    return OvernightCarryMarketService(
        get_db_session_factory(),
        get_session_clock_classifier(),
        get_market_state_service(),
    )


@lru_cache(maxsize=1)
def get_overnight_carry_replay_service() -> OvernightCarryReplayService:
    return OvernightCarryReplayService(
        get_db_session_factory(),
        get_overnight_carry_market_service(),
    )


@lru_cache(maxsize=1)
def get_review_packet_service() -> ReviewPacketService:
    return ReviewPacketService(
        get_db_session_factory(),
        get_execution_records_service(),
        get_events_service(),
    )
