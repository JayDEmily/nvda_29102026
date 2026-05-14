"""Gate 21 execution-planning and broker-abstraction contract services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from nvda_desk.schemas.dmp import (
    DmpBehaviourClass,
    DmpGrammarRole,
    DeskModulePacketV3,
    build_dmp_v3_packet_from_payload,
)
from nvda_desk.schemas.imported_modules.execution_planning import (
    BrokerAdapterContractOutput,
    EntryPlannerContractOutput,
    ExecutionPlanningContext,
    ExecutionPlanningPayload,
    OrderSimulatorContractOutput,
    PositionAllocatorContractOutput,
    RunTradingBotContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    ContractDependencyStatus,
)


@dataclass(frozen=True)
class ExecutionPlanningContractEmission:
    """One typed execution-planning contract output plus its DMP packets."""

    output: ExecutionPlanningPayload
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


class ExecutionPlanningContractService:
    """Emit Gate-21 execution-planning contracts in frozen order."""

    def evaluate(
        self, context: ExecutionPlanningContext
    ) -> list[ExecutionPlanningContractEmission]:
        outputs: list[ExecutionPlanningPayload] = [
            self._broker_adapter(context),
            self._entry_planner(context),
            self._position_allocator(context),
            self._order_simulator(context),
            self._run_trading_bot(context),
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
        output: ExecutionPlanningPayload,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> ExecutionPlanningContractEmission:
        packet = build_dmp_v3_packet_from_payload(
            packet_id=f"dmp::execution_planning::{output.canonical_slug}::{emitted_at.isoformat()}",
            emitted_at=emitted_at,
            grammar_role=DmpGrammarRole(output.grammar_role),
            behaviour_class=DmpBehaviourClass.MODULE_OUTPUT,
            payload=output,
            trader_summary=f"{output.canonical_slug} / {output.computation_mode.value}",
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=[fence.dependency for fence in output.dependency_fences],
            input_model_name="ExecutionPlanningContext",
            output_model_name=output.__class__.__name__,
            trace_id=f"trace::execution_planning::{emitted_at.isoformat()}",
            run_id=f"run::execution_planning::{emitted_at.isoformat()}",
            module_instance_id=f"execution_planning::{output.canonical_slug}",
            registry_version="execution_planning_v1",
            environment_tag="research",
        )
        return ExecutionPlanningContractEmission(output=output, packet=packet)

    def _broker_adapter(self, context: ExecutionPlanningContext) -> BrokerAdapterContractOutput:
        return BrokerAdapterContractOutput(
            canonical_id="archive-module-054",
            canonical_slug="broker_adapter",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.FENCED_CONTRACT_ONLY,
            dependency_fences=_dependency_fences(["broker_requests", "runtime_translation"]),
            upstream_contract_slugs=[],
            contract_notes=[
                "Gate 21 preserves the broker boundary as an explicit dry-run contract only.",
                "No live routing, credentials, or fill acknowledgements exist inside the deterministic runtime.",
            ],
            adapter_mode="paper_broker_boundary",
            supported_actions=["preview_order", "cancel_preview", "flatten_preview"],
            routing_state="fenced_no_broker_bridge",
        )

    def _entry_planner(self, context: ExecutionPlanningContext) -> EntryPlannerContractOutput:
        active_playbook = (
            context.execution.active_playbook_ids[0]
            if context.execution.active_playbook_ids
            else None
        )
        if not active_playbook or context.posture.permission_state.value == "block":
            return EntryPlannerContractOutput(
                canonical_id="archive-module-027",
                canonical_slug="entry_planner",
                grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
                computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
                dependency_fences=_dependency_fences(
                    ["fill_bias_adjuster", "ladder_constructor", "slv_validator"],
                    satisfied={"fill_bias_adjuster", "ladder_constructor"},
                ),
                upstream_contract_slugs=[
                    "fill_bias_adjuster",
                    "ladder_constructor",
                    "entry_gate",
                ],
                contract_notes=[
                    "Entry planning remains suppressed when no active playbook exists or posture permission is fully blocked.",
                ],
                planned_playbook=active_playbook,
                order_style=context.execution.entry_style,
                planned_limit_price=None,
                planned_scale_steps=[],
                planned_ladder_strikes=[],
                planner_state="suppressed_by_gate",
            )

        spot_price = context.spot_data_capture.spot_price or 100.0
        if context.fill_bias_adjuster.fill_bias == "passive_improve":
            planned_limit_price = round(spot_price - 0.08, 2)
        else:
            planned_limit_price = round(spot_price + 0.05, 2)
        return EntryPlannerContractOutput(
            canonical_id="archive-module-027",
            canonical_slug="entry_planner",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["fill_bias_adjuster", "ladder_constructor", "slv_validator"],
                satisfied={"fill_bias_adjuster", "ladder_constructor"},
            ),
            upstream_contract_slugs=[
                "fill_bias_adjuster",
                "ladder_constructor",
                "entry_gate",
            ],
            contract_notes=[
                "SLV validation remains fenced; Gate 21 only preserves a deterministic execution-planning shape.",
                "A temporal or entry-gate veto may still block dispatch even when a preview plan exists.",
            ],
            planned_playbook=active_playbook,
            order_style=context.execution.entry_style,
            planned_limit_price=planned_limit_price,
            planned_scale_steps=[round(step, 2) for step in context.execution.scaling_plan],
            planned_ladder_strikes=[
                round(level, 2) for level in context.ladder_constructor.ladder_strikes
            ],
            planner_state="advisory_plan_ready",
        )

    def _position_allocator(
        self, context: ExecutionPlanningContext
    ) -> PositionAllocatorContractOutput:
        planner = self._entry_planner(context)
        if planner.planner_state != "advisory_plan_ready":
            return PositionAllocatorContractOutput(
                canonical_id="archive-module-028",
                canonical_slug="position_allocator",
                grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
                computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
                dependency_fences=_dependency_fences(
                    ["engine_score", "entry_planner", "spot_prices"],
                    satisfied={"engine_score"},
                    proxied={
                        "spot_prices": "proxied from the current options-flow spot-price surface"
                    },
                ),
                upstream_contract_slugs=["engine_score", "entry_planner"],
                contract_notes=[
                    "No advisory allocation is emitted when the entry planner is suppressed."
                ],
                target_position_pct=0.0,
                tranche_sizes=[],
                conviction_band="stand_down",
                allocation_state="allocation_suppressed",
            )

        shape_sum = round(sum(context.execution.scaling_plan), 4)
        if shape_sum <= 0.0 or shape_sum > 1.0:
            return PositionAllocatorContractOutput(
                canonical_id="archive-module-028",
                canonical_slug="position_allocator",
                grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
                computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
                dependency_fences=_dependency_fences(
                    ["engine_score", "entry_planner", "spot_prices"],
                    satisfied={"engine_score", "entry_planner"},
                    proxied={
                        "spot_prices": "proxied from the current options-flow spot-price surface"
                    },
                ),
                upstream_contract_slugs=["engine_score", "entry_planner"],
                contract_notes=[
                    "The allocator suppresses preview sizing when serial scaling plan input is not a lawful normalised shape.",
                ],
                target_position_pct=0.0,
                tranche_sizes=[],
                conviction_band="stand_down",
                allocation_state="allocation_suppressed_invalid_shape",
            )
        target_position_pct = round(context.posture.fresh_deployable_capital_pct * shape_sum, 2)
        tranche_sizes = [
            round(target_position_pct * (step / shape_sum), 2)
            for step in context.execution.scaling_plan
        ]
        conviction_band = (
            "high_conviction" if context.engine_score.engine_score >= 0.75 else "medium_conviction"
        )
        return PositionAllocatorContractOutput(
            canonical_id="archive-module-028",
            canonical_slug="position_allocator",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["engine_score", "entry_planner", "spot_prices"],
                satisfied={"engine_score", "entry_planner"},
                proxied={"spot_prices": "proxied from the current options-flow spot-price surface"},
            ),
            upstream_contract_slugs=["engine_score", "entry_planner"],
            contract_notes=[
                "The allocator derives advisory target sizing from posture capacity and lawful serial ladder shape only.",
                "Capital booking still remains outside live execution.",
            ],
            target_position_pct=target_position_pct,
            tranche_sizes=tranche_sizes,
            conviction_band=conviction_band,
            allocation_state="advisory_allocation_ready",
        )

    def _order_simulator(self, context: ExecutionPlanningContext) -> OrderSimulatorContractOutput:
        planner = self._entry_planner(context)
        allocator = self._position_allocator(context)
        if planner.planner_state != "advisory_plan_ready" or allocator.target_position_pct <= 0.0:
            return OrderSimulatorContractOutput(
                canonical_id="archive-module-029",
                canonical_slug="order_simulator",
                grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
                computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
                dependency_fences=_dependency_fences(
                    [
                        "entry_planner",
                        "position_allocator",
                        "spot_prices",
                        "spot_vwap_10s",
                    ],
                    satisfied={"entry_planner", "position_allocator"},
                    proxied={
                        "spot_prices": "proxied from the current options-flow spot-price surface"
                    },
                ),
                upstream_contract_slugs=["entry_planner", "position_allocator"],
                contract_notes=["Simulation remains dormant when no advisory entry plan exists."],
                simulated_fill_price=None,
                slippage_bps=None,
                fill_probability=0.0,
                simulation_state="simulation_suppressed",
            )

        baseline_price = (
            planner.planned_limit_price or context.spot_data_capture.spot_price or 100.0
        )
        slippage_bps = 2.0 if context.fill_bias_adjuster.fill_bias == "passive_improve" else 8.0
        simulated_fill_price = round(baseline_price * (1.0 + (slippage_bps / 10000.0)), 4)
        fill_probability = round(
            max(
                0.0,
                min(1.0, 0.45 + (context.fill_bias_adjuster.adjustment_score * 0.4)),
            ),
            4,
        )
        state = (
            "advisory_fill_preview_with_vwap_gap"
            if context.vwap_accumulator.spot_vwap_10s is None
            else "advisory_fill_preview"
        )
        return OrderSimulatorContractOutput(
            canonical_id="archive-module-029",
            canonical_slug="order_simulator",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["entry_planner", "position_allocator", "spot_prices", "spot_vwap_10s"],
                satisfied={"entry_planner", "position_allocator"},
                proxied={"spot_prices": "proxied from the current options-flow spot-price surface"},
            ),
            upstream_contract_slugs=[
                "entry_planner",
                "position_allocator",
                "fill_bias_adjuster",
            ],
            contract_notes=[
                "VWAP tick accumulation remains fenced, so slippage is still a deterministic preview rather than a fill claim.",
            ],
            simulated_fill_price=simulated_fill_price,
            slippage_bps=slippage_bps,
            fill_probability=fill_probability,
            simulation_state=state,
        )

    def _run_trading_bot(self, context: ExecutionPlanningContext) -> RunTradingBotContractOutput:
        simulator = self._order_simulator(context)
        active_dispatches = (
            1 if simulator.simulation_state.startswith("advisory_fill_preview") else 0
        )
        dispatch_state = "dry_run_preview_only" if active_dispatches else "stand_down"
        start_reason = (
            "preview_contract_chain_ready"
            if active_dispatches
            else "no_execution_preview_due_to_entry_veto"
        )
        return RunTradingBotContractOutput(
            canonical_id="archive-module-053",
            canonical_slug="run_trading_bot",
            grammar_role=DmpGrammarRole.EXPRESSION_EXECUTION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["runtime_config", "order_simulator", "broker_adapter"],
                satisfied={"order_simulator", "broker_adapter"},
                proxied={
                    "runtime_config": "proxied from the current deterministic settings surface; no daemon or scheduler exists",
                },
            ),
            upstream_contract_slugs=["order_simulator", "broker_adapter"],
            contract_notes=[
                "Gate 21 stops at dry-run orchestration; it must not claim a live bot loop, order placement, or broker callback path.",
            ],
            run_mode="dry_run_only",
            active_dispatches=active_dispatches,
            dispatch_state=dispatch_state,
            start_reason=start_reason,
        )
