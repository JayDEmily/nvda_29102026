"""Expose the benchmark-owned API app cut without widening the current web shell."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any, Iterable, Mapping

from nvda_desk.adapters.egress.api_dto_adapter import ApiDtoAdapter
from nvda_desk.adapters.ingress.market_snapshot_feed import adapt_market_snapshot
from nvda_desk.adapters.ingress.options_surface_feed import adapt_options_surface
from nvda_desk.analysis.replay.walk_forward import run_slv_batch_rank_from_market
from nvda_desk.api.deps import (
    get_api_dto_adapter,
    get_carry_handoff_service,
    get_config_surface,
    get_daily_pnl_report_service,
    get_evaluation_log_service,
    get_events_service,
    get_execution_records_service,
    get_module_registry_service,
    get_overnight_carry_market_service,
    get_overnight_carry_replay_service,
    get_paper_broker_execution_service,
    get_promotion_service,
    get_research_service,
    get_risk_gateway_service,
    get_runtime_orchestrator,
    get_session_calendar_service,
    get_session_clock_classifier,
    get_settings_cached,
    get_strategic_ladder_experiment_service,
    get_strategic_ladder_market_service,
    get_strategic_ladder_replay_service,
)
from nvda_desk.calendar.operational.events import (
    MarketEventDTO,
    RuntimeCalendarQuery,
    SessionCalendarDTO,
)
from nvda_desk.config import ConfigSurface
from nvda_desk.contracts.broker_execution import BrokerOrderIntent
from nvda_desk.contracts.daily_pnl import DailyPnlReport
from nvda_desk.contracts.exit_close import ExitCloseInputTrace
from nvda_desk.contracts.strategic_ladder import StrategicLadderValidationRequest
from nvda_desk.downstream.exit_close import evaluate_exit_close_policy
from nvda_desk.review.packet_service import ReviewPacketService
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator


class HttpApp:
    """Small boundary app shell around bounded dependency and runtime composition."""

    def __init__(
        self,
        *,
        orchestrator: DeskRuntimeOrchestrator | None = None,
        config_surface: ConfigSurface | None = None,
        dto_adapter: ApiDtoAdapter | None = None,
    ) -> None:
        self.orchestrator = orchestrator or get_runtime_orchestrator()
        self.config_surface = config_surface or get_config_surface()
        self.dto_adapter = dto_adapter or get_api_dto_adapter()
        self.route_handlers: dict[str, Any] = {}
        self.events_service = get_events_service()
        self.session_calendar_service = get_session_calendar_service()
        self.module_registry_service = get_module_registry_service()
        self.execution_records_service = get_execution_records_service()
        self.research_service = get_research_service()
        self.promotion_service = get_promotion_service()
        self.evaluation_service = get_evaluation_log_service()
        self.experiment_service = get_strategic_ladder_experiment_service()
        self.strategic_ladder_market_service = get_strategic_ladder_market_service()
        self.strategic_ladder_replay_service = get_strategic_ladder_replay_service()
        self.risk_gateway_service = get_risk_gateway_service()
        self.paper_broker_execution_service = get_paper_broker_execution_service()
        self.daily_pnl_report_service = get_daily_pnl_report_service()
        self.carry_handoff_service = get_carry_handoff_service()
        self.overnight_carry_market_service = get_overnight_carry_market_service()
        self.overnight_carry_replay_service = get_overnight_carry_replay_service()
        self.review_packet_service = ReviewPacketService(
            execution_records=self.execution_records_service,
            daily_pnl_service=self.daily_pnl_report_service,
        )

    def healthcheck(self) -> dict[str, str]:
        """Return the bounded health surface supported by the rebuild-phase shell."""

        return self.dto_adapter.to_state_dto({"status": "ok"})

    def run_once(self, stage_inputs: dict[str, Any]) -> dict[str, Any]:
        """Run one bounded runtime pass from already-typed stage inputs."""

        return self.dto_adapter.to_runtime_dto(self.orchestrator.run_once(stage_inputs))

    def get_runtime_settings(self) -> dict[str, Any]:
        return get_settings_cached().model_dump(mode="json")

    def list_coefficients(self) -> list[dict[str, Any]]:
        authority_payload = self.config_surface.coefficient_authority_service().load_document()
        return [record.model_dump(mode="json") for record in authority_payload.records]

    def get_coefficient_group(self, owner_stage: str) -> dict[str, Any]:
        return {
            "owner_stage": owner_stage,
            "coefficients": [
                record.model_dump(mode="json")
                for record in self.config_surface.coefficient_authority_service()
                .record_map(owner_stage=owner_stage)
                .values()
            ],
        }

    def list_strategy_variants(self) -> list[dict[str, Any]]:
        return [
            playbook.model_dump(mode="json")
            for playbook in self.config_surface.playbook_registry().playbooks
        ]

    def get_strategy_variant(self, playbook_id: str) -> dict[str, Any]:
        for playbook in self.config_surface.playbook_registry().playbooks:
            if playbook.playbook_id == playbook_id:
                return playbook.model_dump(mode="json")
        raise KeyError(f"unknown playbook_id: {playbook_id}")

    def market_temporal_state(
        self, source_time_utc: datetime, *, source_timezone_raw: str | None = None
    ) -> dict[str, str]:
        classifier = get_session_clock_classifier()
        return {
            "session_state": classifier(source_time_utc, source_timezone_raw=source_timezone_raw)
        }

    def market_session_clock(
        self, source_time_utc: datetime, *, source_timezone_raw: str | None = None
    ) -> dict[str, str]:
        return self.market_temporal_state(source_time_utc, source_timezone_raw=source_timezone_raw)

    def market_snapshot(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        return _to_plain_dict(adapt_market_snapshot(payload))

    def market_intraday(self, rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
        row_list = [dict(row) for row in rows]
        return {"rows": row_list, "row_count": len(row_list)}

    def market_option_surface(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        return _to_plain_dict(adapt_options_surface(payload))

    def create_session_calendar(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        session = SessionCalendarDTO(
            session_id=str(payload["session_id"]),
            trade_date=str(payload["trade_date"]),
            session_state=str(payload["session_state"]),
            tags=list(payload.get("tags", [])),
        )
        return asdict(self.session_calendar_service.create_session(session))

    def list_session_calendars(self) -> list[dict[str, Any]]:
        return [asdict(session) for session in self.session_calendar_service.list_sessions()]

    def create_market_event(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        event = MarketEventDTO(
            event_id=str(payload["event_id"]),
            event_type=str(payload["event_type"]),
            starts_at=payload.get("starts_at"),
            ends_at=payload.get("ends_at"),
            tags=list(payload.get("tags", [])),
            symbol=payload.get("symbol"),
            materiality=str(payload.get("materiality", "low")),
            lineage_ids=list(payload.get("lineage_ids", [])),
        )
        return asdict(self.events_service.create_event(event))

    def list_market_events(self) -> list[dict[str, Any]]:
        return [asdict(event) for event in self.events_service.list_events()]

    def query_event_proximity(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        query = RuntimeCalendarQuery(
            symbol=payload.get("symbol"),
            window_start_utc=payload["window_start_utc"],
            window_end_utc=payload["window_end_utc"],
            minimum_materiality=str(payload.get("minimum_materiality", "low")),
            observed_at=payload.get("observed_at"),
        )
        return _to_plain_dict(self.events_service.build_runtime_calendar_snapshot(query))

    def validate_strategic_ladder_market(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        request = StrategicLadderValidationRequest.model_validate(dict(payload))
        return _to_plain_dict(self.strategic_ladder_market_service.validate_market_ladder(request))

    def evaluate_risk_policy(
        self,
        policy_id: str,
        *,
        candidate_id: str | None = None,
        semantic_tags: list[str] | None = None,
    ) -> dict[str, Any]:
        return _to_plain_dict(
            self.risk_gateway_service.evaluate_risk_policy(
                policy_id, candidate_id=candidate_id, semantic_tags=semantic_tags
            )
        )

    def list_risk_decisions(self) -> list[dict[str, Any]]:
        return _to_plain_dict(self.risk_gateway_service.list_risk_decisions())

    def replay_session_phases(self, phases: Iterable[str]) -> dict[str, Any]:
        return {"phases": [str(phase) for phase in phases]}

    def create_research_note(self, note_id: str, *, title: str, body: str) -> dict[str, Any]:
        return self.research_service.create_research_note(note_id, title=title, body=body)

    def list_research_notes(self) -> list[dict[str, Any]]:
        return self.research_service.list_research_notes()

    def create_promotion_decision(
        self, decision_id: str, *, candidate_id: str, decision: str, rationale: str
    ) -> dict[str, Any]:
        return self.promotion_service.create_promotion_decision(
            decision_id, candidate_id=candidate_id, decision=decision, rationale=rationale
        )

    def list_promotion_decisions(self) -> list[dict[str, Any]]:
        return self.promotion_service.list_promotion_decisions()

    def create_module_spec(self, module_id: str, record: Mapping[str, Any]) -> dict[str, Any]:
        self.module_registry_service.write_record(module_id, dict(record))
        return {"module_id": module_id, **dict(record)}

    def list_module_specs(self) -> list[dict[str, Any]]:
        records = []
        for module_id, record in sorted(self.module_registry_service._records.items()):
            records.append({"module_id": module_id, **dict(record)})
        return records

    def replay_strategic_ladder_from_market(
        self, rows: Iterable[Mapping[str, Any]]
    ) -> dict[str, Any]:
        report = run_slv_batch_rank_from_market(rows, report_id="api_strategic_ladder")
        payload = _to_plain_dict(report)
        payload["best_stack_id"] = report.best_stack_id
        return payload

    def record_strategic_ladder_evaluation(
        self, run_id: str, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        return self.evaluation_service.record_evaluation_run(
            run_id, kind="strategic_ladder", payload=dict(payload)
        )

    def place_paper_order(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        intent = BrokerOrderIntent.model_validate(dict(payload))
        return _to_plain_dict(self.paper_broker_execution_service.place_paper_order(intent))

    def list_broker_order_events(self) -> list[dict[str, Any]]:
        return _to_plain_dict(self.paper_broker_execution_service.list_order_events().events)

    def list_broker_fill_events(self) -> list[dict[str, Any]]:
        return _to_plain_dict(self.paper_broker_execution_service.list_fill_events().fills)

    def list_broker_positions(self) -> list[dict[str, Any]]:
        return _to_plain_dict(self.paper_broker_execution_service.list_positions().positions)

    def get_broker_account_state(self) -> dict[str, Any]:
        return _to_plain_dict(self.paper_broker_execution_service.get_account_state())

    def record_daily_pnl_report(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        report_payload = dict(payload)
        report_payload.pop("total_pnl_usd", None)
        report = DailyPnlReport.model_validate(report_payload)
        return _to_plain_dict(self.daily_pnl_report_service.record_report(report))

    def list_daily_pnl_reports(self) -> list[dict[str, Any]]:
        return _to_plain_dict(self.daily_pnl_report_service.list_reports().reports)

    def _carry_decision_from_payload(self, payload: Mapping[str, Any]):
        trace_payload = payload.get("input_trace")
        if not isinstance(trace_payload, Mapping) or not trace_payload:
            raise ValueError("input_trace_required")
        decision_id = payload.get("decision_id")
        if not isinstance(decision_id, str) or not decision_id.strip():
            raise ValueError("decision_id_required")
        trace = ExitCloseInputTrace.model_validate(dict(trace_payload))
        return evaluate_exit_close_policy(
            input_trace=trace,
            requested_action=str(payload.get("requested_action", "hold")),
            trigger_ids=tuple(payload.get("trigger_ids", ())),
            decision_id=decision_id,
        )

    def evaluate_overnight_carry(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        decision = self._carry_decision_from_payload(payload)
        handoff = self.carry_handoff_service.build_carry_handoff(
            decision=decision,
            horizon=str(payload.get("horizon", "overnight")),
            lifecycle_ceiling=str(payload.get("lifecycle_ceiling", "close")),
            next_session_open_utc=payload.get("next_session_open_utc"),
            configured_next_session_open_utc=payload.get("configured_next_session_open_utc"),
        )
        return _to_plain_dict(handoff)

    def evaluate_overnight_carry_from_market(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        decision = self._carry_decision_from_payload(payload)
        handoff = self.carry_handoff_service.build_carry_handoff(
            decision=decision,
            horizon=str(payload.get("horizon", "overnight")),
            lifecycle_ceiling=str(payload.get("lifecycle_ceiling", "close")),
        )
        evaluation_id = payload.get("evaluation_id")
        if not isinstance(evaluation_id, str) or not evaluation_id.strip():
            raise ValueError("evaluation_id_required")
        evaluation = self.overnight_carry_market_service.evaluate_from_market(
            evaluation_id=evaluation_id,
            market_state=dict(payload.get("market_state", {})),
            handoff=handoff,
        )
        return _to_plain_dict(evaluation)

    def record_overnight_carry_evaluation(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        evaluation_payload = self.evaluate_overnight_carry_from_market(payload)
        from nvda_desk.downstream.overnight_carry import OvernightCarryEvaluation

        evaluation = OvernightCarryEvaluation.model_validate(evaluation_payload)
        return _to_plain_dict(self.overnight_carry_replay_service.record_evaluation(evaluation))

    def record_overnight_carry_market_evaluation(
        self, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        return self.record_overnight_carry_evaluation(payload)

    def replay_overnight_carry_from_market(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        from nvda_desk.downstream.overnight_carry import OvernightCarryEvaluation

        evaluation_payload = payload.get("evaluation") or self.evaluate_overnight_carry_from_market(
            payload
        )
        evaluation = OvernightCarryEvaluation.model_validate(evaluation_payload)
        replay_id = payload.get("replay_id")
        if not isinstance(replay_id, str) or not replay_id.strip():
            raise ValueError("replay_id_required")
        next_session_source_id = payload.get("next_session_source_id")
        if not isinstance(next_session_source_id, str) or not next_session_source_id.strip():
            raise ValueError("next_session_source_id_required")
        replay = self.overnight_carry_replay_service.replay_evaluation(
            replay_id=replay_id,
            evaluation=evaluation,
            next_session_source_id=next_session_source_id,
            next_session_reference=dict(payload.get("next_session_reference", {})),
        )
        return _to_plain_dict(replay)

    def get_overnight_verdict_and_score(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        evaluation = self.evaluate_overnight_carry_from_market(payload)
        score = {"hold": 0.0, "trim": 0.5, "close": 1.0}[evaluation["recommendation"]]
        return {"verdict": evaluation["recommendation"], "score": score, "evaluation": evaluation}

    def get_module_health_packet(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        packet = self.review_packet_service.build_module_health_packet(
            packet_id=str(payload.get("packet_id", "module-health"))
        )
        return _to_plain_dict(packet)

    def get_daily_review_packet(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        packet = self.review_packet_service.build_daily_review_packet(
            packet_id=str(payload.get("packet_id", "daily-review")),
            symbol=str(payload.get("symbol", "NVDA")),
            trade_date=str(payload.get("trade_date")),
        )
        return _to_plain_dict(packet)


def register_routes(app: HttpApp) -> HttpApp:
    """Attach the bounded route table supported by the current shell."""

    route_names = [
        "healthcheck",
        "run_once",
        "get_runtime_settings",
        "list_coefficients",
        "get_coefficient_group",
        "list_strategy_variants",
        "get_strategy_variant",
        "market_temporal_state",
        "market_session_clock",
        "market_snapshot",
        "market_intraday",
        "market_option_surface",
        "create_session_calendar",
        "list_session_calendars",
        "create_market_event",
        "list_market_events",
        "list_risk_decisions",
        "evaluate_risk_policy",
        "validate_strategic_ladder_market",
        "query_event_proximity",
        "replay_session_phases",
        "create_research_note",
        "list_research_notes",
        "create_promotion_decision",
        "list_promotion_decisions",
        "create_module_spec",
        "list_module_specs",
        "replay_strategic_ladder_from_market",
        "record_strategic_ladder_evaluation",
        "place_paper_order",
        "list_broker_order_events",
        "list_broker_fill_events",
        "list_broker_positions",
        "get_broker_account_state",
        "record_daily_pnl_report",
        "list_daily_pnl_reports",
        "evaluate_overnight_carry",
        "evaluate_overnight_carry_from_market",
        "record_overnight_carry_evaluation",
        "record_overnight_carry_market_evaluation",
        "replay_overnight_carry_from_market",
        "get_overnight_verdict_and_score",
        "get_module_health_packet",
        "get_daily_review_packet",
    ]
    app.route_handlers = {name: getattr(app, name) for name in route_names}
    return app


def create_app(
    *,
    orchestrator: DeskRuntimeOrchestrator | None = None,
    config_surface: ConfigSurface | None = None,
    dto_adapter: ApiDtoAdapter | None = None,
) -> HttpApp:
    """Create the minimal boundary app shell for entry/bootstrap callers."""

    app = HttpApp(orchestrator=orchestrator, config_surface=config_surface, dto_adapter=dto_adapter)
    return register_routes(app)


def _to_plain_dict(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {key: _to_plain_dict(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_plain_dict(child) for child in value]
    return value
