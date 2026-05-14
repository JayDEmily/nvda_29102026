"""Gate 22 execution-state, exit, and lifecycle contract services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha1

from nvda_desk.schemas.dmp import (
    DmpBehaviourClass,
    DmpGrammarRole,
    DeskModulePacketV3,
    build_dmp_v3_packet_from_payload,
)
from nvda_desk.schemas.imported_modules.execution_lifecycle import (
    DynamicPartialExitModelContractOutput,
    ExecutionLifecycleContext,
    ExecutionLifecyclePayload,
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
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    ContractDependencyStatus,
)


@dataclass(frozen=True)
class ExecutionLifecycleContractEmission:
    """One typed execution-lifecycle contract output plus its DMP packets."""

    output: ExecutionLifecyclePayload
    packet: DeskModulePacketV3


def _dependency_fences(
    dependencies: list[str],
    *,
    satisfied: set[str] | None = None,
    proxied: dict[str, str] | None = None,
) -> list[ContractDependencyFence]:
    satisfied = satisfied or set()
    proxied = proxied or {}
    fences: list[ContractDependencyFence] = []
    for dependency in dependencies:
        if dependency in proxied:
            fences.append(
                ContractDependencyFence(
                    dependency=dependency,
                    status=ContractDependencyStatus.PROXIED_FROM_RUNTIME,
                    note=proxied[dependency],
                )
            )
        elif dependency in satisfied:
            fences.append(
                ContractDependencyFence(
                    dependency=dependency,
                    status=ContractDependencyStatus.SATISFIED,
                    note="available directly inside the deterministic runtime or prior contract surface",
                )
            )
        else:
            fences.append(
                ContractDependencyFence(
                    dependency=dependency,
                    status=ContractDependencyStatus.FENCED_MISSING_SOURCE,
                    note="not available in the current deterministic runtime; kept as an explicit contract fence",
                )
            )
    return fences


class ExecutionLifecycleContractService:
    """Emit Gate-22 lifecycle contracts in frozen order."""

    def evaluate(
        self, context: ExecutionLifecycleContext
    ) -> list[ExecutionLifecycleContractEmission]:
        outputs: list[ExecutionLifecyclePayload] = [
            self._dynamic_partial_exit_model(context),
            self._take_profit(context),
            self._trailing_stop(context),
            self._unrealized_tracker(context),
            self._position_book(context),
            self._trade_reentry_marker(context),
            self._ladder_continuity_tracker(context),
            self._fill_feedback_router(context),
            self._execution_log_writer(context),
            self._execution_tags(context),
            self._trade_logger(context),
        ]
        return [
            self._emit_packet(
                output=output,
                emitted_at=context.emitted_at,
                stack_id=context.stack_id,
                coefficient_set_id=context.coefficient_set_id,
            )
            for output in outputs
        ]

    def _emit_packet(
        self,
        *,
        output: ExecutionLifecyclePayload,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> ExecutionLifecycleContractEmission:
        packet = build_dmp_v3_packet_from_payload(
            packet_id=f"dmp::execution_lifecycle::{output.canonical_slug}::{emitted_at.isoformat()}",
            emitted_at=emitted_at,
            grammar_role=DmpGrammarRole(output.grammar_role),
            behaviour_class=DmpBehaviourClass.MODULE_OUTPUT,
            payload=output,
            trader_summary=f"{output.canonical_slug} / {output.computation_mode.value}",
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=[fence.dependency for fence in output.dependency_fences],
            input_model_name="ExecutionLifecycleContext",
            output_model_name=output.__class__.__name__,
            trace_id=f"trace::execution_lifecycle::{emitted_at.isoformat()}",
            run_id=f"run::execution_lifecycle::{emitted_at.isoformat()}",
            module_instance_id=f"execution_lifecycle::{output.canonical_slug}",
            registry_version="execution_lifecycle_v1",
            environment_tag="research",
        )
        return ExecutionLifecycleContractEmission(output=output, packet=packet)

    def _dynamic_partial_exit_model(
        self, context: ExecutionLifecycleContext
    ) -> DynamicPartialExitModelContractOutput:
        if context.order_simulator.simulation_state == "simulation_suppressed":
            return DynamicPartialExitModelContractOutput(
                canonical_id="archive-module-035",
                canonical_slug="dynamic_partial_exit_model",
                grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
                computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
                dependency_fences=_dependency_fences(
                    ["position_state", "signals"],
                    proxied={"signals": "proxied from the current execution exit-plan surface"},
                ),
                upstream_contract_slugs=["order_simulator"],
                contract_notes=["No exit ladder exists while the execution preview is suppressed."],
                partial_exit_levels=[],
                partial_exit_fracs=[],
                model_state="no_exit_plan",
            )
        fill_price = (
            context.order_simulator.simulated_fill_price
            or context.spot_data_capture.spot_price
            or 100.0
        )
        levels = [round(fill_price * (1.0 + step), 4) for step in (0.01, 0.02, 0.035)]
        return DynamicPartialExitModelContractOutput(
            canonical_id="archive-module-035",
            canonical_slug="dynamic_partial_exit_model",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["position_state", "signals"],
                proxied={"signals": "proxied from the current execution exit-plan surface"},
            ),
            upstream_contract_slugs=["order_simulator", "entry_planner"],
            contract_notes=["Dynamic partial exits remain an advisory preview only."],
            partial_exit_levels=levels,
            partial_exit_fracs=[0.25, 0.35, 0.4],
            model_state="advisory_partial_exit_ready",
        )

    def _take_profit(self, context: ExecutionLifecycleContext) -> TakeProfitContractOutput:
        partial_exit = self._dynamic_partial_exit_model(context)
        return TakeProfitContractOutput(
            canonical_id="archive-module-034",
            canonical_slug="take_profit",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["market_prices", "position_state"],
                proxied={
                    "market_prices": "proxied from the current options-flow spot-price surface"
                },
            ),
            upstream_contract_slugs=["dynamic_partial_exit_model", "order_simulator"],
            contract_notes=[
                "Take-profit levels are derived from the advisory partial-exit ladder, not from live orders."
            ],
            profit_targets=partial_exit.partial_exit_levels,
            target_basis=(
                "simulated_fill_plus_extension"
                if partial_exit.partial_exit_levels
                else "no_position"
            ),
            take_profit_state=(
                "targets_ready"
                if partial_exit.partial_exit_levels
                else "suppressed_without_position"
            ),
        )

    def _trailing_stop(self, context: ExecutionLifecycleContext) -> TrailingStopContractOutput:
        fill_price = context.order_simulator.simulated_fill_price
        if fill_price is None:
            return TrailingStopContractOutput(
                canonical_id="archive-module-033",
                canonical_slug="trailing_stop",
                grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
                computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
                dependency_fences=_dependency_fences(
                    ["market_prices", "position_state"],
                    proxied={
                        "market_prices": "proxied from the current options-flow spot-price surface"
                    },
                ),
                upstream_contract_slugs=["order_simulator"],
                contract_notes=[
                    "No trailing stop preview exists when there is no simulated entry."
                ],
                trailing_stop_pct=None,
                trail_anchor=None,
                stop_state="no_trailing_stop",
            )
        stop_pct = 0.025 if context.posture.permission_state.value == "allow" else 0.015
        return TrailingStopContractOutput(
            canonical_id="archive-module-033",
            canonical_slug="trailing_stop",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["market_prices", "position_state"],
                proxied={
                    "market_prices": "proxied from the current options-flow spot-price surface"
                },
            ),
            upstream_contract_slugs=["order_simulator"],
            contract_notes=[
                "Trailing-stop distance remains advisory and is widened only by current posture permission."
            ],
            trailing_stop_pct=stop_pct,
            trail_anchor=fill_price,
            stop_state="advisory_trailing_stop_ready",
        )

    def _unrealized_tracker(
        self, context: ExecutionLifecycleContext
    ) -> UnrealizedTrackerContractOutput:
        mark_price = context.spot_data_capture.spot_price or 100.0
        fill_price = context.order_simulator.simulated_fill_price
        if fill_price is None and context.inventory.existing_inventory_pct > 0.0:
            unrealized_pnl_pct = round(context.inventory.cost_basis_gap_pct, 4)
        elif fill_price is None:
            unrealized_pnl_pct = 0.0
        else:
            unrealized_pnl_pct = round(((mark_price / fill_price) - 1.0) * 100.0, 4)
        return UnrealizedTrackerContractOutput(
            canonical_id="archive-module-032",
            canonical_slug="unrealized_tracker",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["market_prices", "open_positions"],
                proxied={
                    "market_prices": "proxied from the current options-flow spot-price surface",
                    "open_positions": "proxied from the advisory position-allocation and inventory surfaces",
                },
            ),
            upstream_contract_slugs=["position_allocator", "order_simulator"],
            contract_notes=[
                "Unrealised P&L remains a deterministic preview rather than a ledger assertion."
            ],
            mark_price=mark_price,
            unrealized_pnl_pct=unrealized_pnl_pct,
            tracker_state=(
                "flat"
                if fill_price is None and context.inventory.existing_inventory_pct <= 0.0
                else "preview_mark_to_market"
            ),
        )

    def _position_book(self, context: ExecutionLifecycleContext) -> PositionBookContractOutput:
        live_position_pct = round(
            min(
                100.0,
                context.inventory.existing_inventory_pct
                + context.position_allocator.target_position_pct,
            ),
            2,
        )
        open_order_count = context.inventory.open_orders_count + (
            1 if context.entry_planner.planner_state == "advisory_plan_ready" else 0
        )
        state = (
            "preview_position_open"
            if context.position_allocator.target_position_pct > 0.0
            else "flat_or_locked"
        )
        return PositionBookContractOutput(
            canonical_id="archive-module-031",
            canonical_slug="position_book",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["execution_log", "fills"],
                proxied={"execution_log": "proxied from the advisory execution-chain surfaces"},
            ),
            upstream_contract_slugs=["position_allocator", "order_simulator"],
            contract_notes=[
                "The position book remains a preview state built from advisory allocation plus current inventory."
            ],
            open_position_state=state,
            live_position_pct=live_position_pct,
            open_order_count=open_order_count,
            book_state=state,
        )

    def _trade_reentry_marker(
        self, context: ExecutionLifecycleContext
    ) -> TradeReentryMarkerContractOutput:
        position_book = self._position_book(context)
        if position_book.live_position_pct > 0.0:
            reentry_allowed = False
            cooldown_minutes = 30
            state = "position_still_live"
        elif context.entry_gate.entry_allowed:
            reentry_allowed = True
            cooldown_minutes = 0
            state = "reentry_available"
        else:
            reentry_allowed = False
            cooldown_minutes = 60
            state = "gated_off"
        return TradeReentryMarkerContractOutput(
            canonical_id="archive-module-036",
            canonical_slug="trade_reentry_marker",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["closed_positions", "new_signals"],
                proxied={
                    "new_signals": "proxied from the current eligibility and execution surfaces"
                },
            ),
            upstream_contract_slugs=["position_book", "entry_gate"],
            contract_notes=[
                "Re-entry gating remains advisory and depends on the preview position state only."
            ],
            reentry_allowed=reentry_allowed,
            cooldown_minutes=cooldown_minutes,
            reentry_state=state,
        )

    def _ladder_continuity_tracker(
        self, context: ExecutionLifecycleContext
    ) -> LadderContinuityTrackerContractOutput:
        ladder_bytes = repr(context.entry_planner.planned_ladder_strikes).encode("utf-8")
        ladder_hash = (
            sha1(ladder_bytes, usedforsecurity=False).hexdigest()[:12] if ladder_bytes else None
        )
        continuity_score = 1.0 if context.entry_planner.planned_ladder_strikes else 0.0
        return LadderContinuityTrackerContractOutput(
            canonical_id="archive-module-047",
            canonical_slug="ladder_continuity_tracker",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["current_ladder", "prior_ladder_history"],
                proxied={
                    "current_ladder": "proxied from the advisory entry planner ladder surface"
                },
            ),
            upstream_contract_slugs=["entry_planner"],
            contract_notes=[
                "Only current-session ladder continuity is preserved; cross-session history remains fenced."
            ],
            continuity_state=("continuous" if continuity_score > 0.0 else "no_ladder"),
            continuity_score=continuity_score,
            ladder_hash=ladder_hash,
        )

    def _fill_feedback_router(
        self, context: ExecutionLifecycleContext
    ) -> FillFeedbackRouterContractOutput:
        if context.order_simulator.fill_probability >= 0.7:
            route = "feed_back_into_entry_planner"
            confidence = 0.75
            state = "preview_feedback_ready"
        elif context.order_simulator.fill_probability > 0.0:
            route = "hold_for_manual_review"
            confidence = 0.45
            state = "preview_feedback_thin"
        else:
            route = "no_feedback_without_simulation"
            confidence = 0.0
            state = "suppressed"
        return FillFeedbackRouterContractOutput(
            canonical_id="archive-module-045",
            canonical_slug="fill_feedback_router",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["current_runtime_state", "past_fills"],
                proxied={
                    "current_runtime_state": "proxied from the advisory execution-chain packet surface"
                },
            ),
            upstream_contract_slugs=["order_simulator", "entry_planner"],
            contract_notes=[
                "Past fills remain fenced, so feedback routing stays a deterministic preview only."
            ],
            feedback_route=route,
            route_confidence=confidence,
            router_state=state,
        )

    def _execution_log_writer(
        self, context: ExecutionLifecycleContext
    ) -> ExecutionLogWriterContractOutput:
        missing_surfaces = [
            fence.dependency
            for fence in context.broker_adapter.dependency_fences
            if fence.status is ContractDependencyStatus.FENCED_MISSING_SOURCE
        ]
        event_count = 3 if context.order_simulator.fill_probability > 0.0 else 1
        return ExecutionLogWriterContractOutput(
            canonical_id="archive-module-030",
            canonical_slug="execution_log_writer",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "engine_score",
                    "entry_gate",
                    "entry_planner",
                    "order_simulator",
                    "position_allocator",
                ],
                satisfied={
                    "entry_gate",
                    "entry_planner",
                    "order_simulator",
                    "position_allocator",
                },
            ),
            upstream_contract_slugs=[
                "entry_gate",
                "entry_planner",
                "order_simulator",
                "position_allocator",
            ],
            contract_notes=[
                "The log writer emits preview events only and keeps missing broker surfaces explicit."
            ],
            log_state=("preview_events_logged" if event_count > 1 else "stand_down_logged"),
            event_count=event_count,
            missing_surfaces=missing_surfaces,
        )

    def _execution_tags(self, context: ExecutionLifecycleContext) -> ExecutionTagsContractOutput:
        position_book = self._position_book(context)
        fill_feedback_router = self._fill_feedback_router(context)
        tags = [
            context.execution.entry_style,
            position_book.book_state,
            fill_feedback_router.feedback_route,
        ]
        if context.posture.permission_state.value != "allow":
            tags.append("permission_constrained")
        return ExecutionTagsContractOutput(
            canonical_id="archive-module-050",
            canonical_slug="execution_tags",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["execution_decisions", "signals"],
                proxied={"signals": "proxied from the current execution and posture outputs"},
            ),
            upstream_contract_slugs=["position_book", "fill_feedback_router"],
            contract_notes=["Tags remain an explainability surface for preview execution only."],
            tags=tags,
            tagging_state="tagged",
        )

    def _trade_logger(self, context: ExecutionLifecycleContext) -> TradeLoggerContractOutput:
        execution_log_writer = self._execution_log_writer(context)
        last_event = (
            "preview_order_ready"
            if context.order_simulator.fill_probability > 0.0
            else "stand_down"
        )
        return TradeLoggerContractOutput(
            canonical_id="archive-module-037",
            canonical_slug="trade_logger",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["runtime_events"],
                proxied={
                    "runtime_events": "proxied from the advisory execution log and tag surfaces"
                },
            ),
            upstream_contract_slugs=["execution_log_writer", "execution_tags"],
            contract_notes=[
                "Trade logging remains a deterministic preview trail rather than a fill ledger."
            ],
            trade_log_state=(
                "preview_trade_log_ready"
                if context.order_simulator.fill_probability > 0.0
                else "idle"
            ),
            record_count=execution_log_writer.event_count,
            last_event_tag=last_event,
        )
