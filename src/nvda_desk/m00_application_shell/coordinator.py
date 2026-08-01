"""Stateless M00 coordinator for exact owner-seam composition."""

from __future__ import annotations

from typing import Any, Callable, Protocol

from pydantic import ValidationError

from nvda_desk.contracts.packets import (
    K07_COMMON_CHECKS,
    K07_ROLE_CHECKS,
    DmpV3ExecutionContext,
    PreparedContextIdentity,
)
from nvda_desk.m05_serial_cognition import (
    SerialCandidatePacketAdapter,
    SerialRunner,
)
from nvda_desk.m06_parallel_risk import (
    ParallelRiskEvaluator,
    ParallelRiskPacketAdapter,
)
from nvda_desk.m09_capital_authority import CapitalAuthorityService
from nvda_desk.m10_execution_gateway import ExecutionGateway
from nvda_desk.m12_evidence_replay import EvidenceReplayService, ReviewProjection
from nvda_desk.packets.dmp_packets import build_prepared_context_packet

from .contracts import ApplicationCommand, ApplicationQuery, ApplicationRunReceipt

_PREPARED_OWNER_CHECKS = frozenset(
    (*K07_COMMON_CHECKS, *K07_ROLE_CHECKS["prepared_context_packet"])
)


class PaperRunScope(Protocol):
    scope_id: str
    trace_id: str
    run_id: str
    scenario_id: str
    execution_port: Any
    portfolio_service: Any


class RunCoordinator:
    """Coordinate one exact prepared run or one separate read-only M12 query."""

    def __init__(
        self,
        *,
        serial_runner: SerialRunner,
        parallel_evaluator: ParallelRiskEvaluator,
        serial_packet_adapter: SerialCandidatePacketAdapter,
        parallel_packet_adapter: ParallelRiskPacketAdapter,
        capital_authority: CapitalAuthorityService,
        execution_gateway: ExecutionGateway,
        paper_run_scope_factory: Callable[[DmpV3ExecutionContext], PaperRunScope],
        replay_service: EvidenceReplayService,
    ) -> None:
        dependencies = {
            "serial_runner": serial_runner,
            "parallel_evaluator": parallel_evaluator,
            "serial_packet_adapter": serial_packet_adapter,
            "parallel_packet_adapter": parallel_packet_adapter,
            "capital_authority": capital_authority,
            "execution_gateway": execution_gateway,
            "paper_run_scope_factory": paper_run_scope_factory,
            "replay_service": replay_service,
        }
        missing = tuple(name for name, value in dependencies.items() if value is None)
        if missing:
            raise ValueError(f"m00_dependency_missing:{','.join(missing)}")
        self._serial_runner = serial_runner
        self._parallel_evaluator = parallel_evaluator
        self._serial_packet_adapter = serial_packet_adapter
        self._parallel_packet_adapter = parallel_packet_adapter
        self._capital_authority = capital_authority
        self._execution_gateway = execution_gateway
        self._paper_run_scope_factory = paper_run_scope_factory
        self._replay_service = replay_service

    @staticmethod
    def _command(value: ApplicationCommand) -> ApplicationCommand:
        if not isinstance(value, ApplicationCommand):
            raise TypeError("typed_application_command_required")
        try:
            return ApplicationCommand.model_validate(value.model_dump(mode="python"))
        except (ValidationError, ValueError, TypeError) as exc:
            raise ValueError("application_command_contract_invalid") from exc

    @staticmethod
    def _query(value: ApplicationQuery) -> ApplicationQuery:
        if not isinstance(value, ApplicationQuery):
            raise TypeError("typed_application_query_required")
        try:
            return ApplicationQuery.model_validate(value.model_dump(mode="python"))
        except (ValidationError, ValueError, TypeError) as exc:
            raise ValueError("application_query_contract_invalid") from exc

    @staticmethod
    def _prepared_packet(command: ApplicationCommand):
        prepared = command.prepared_data
        context = command.execution_context
        identity = PreparedContextIdentity(
            prepared_id=prepared.prepared_id,
            prepared_fingerprint=prepared.prepared_fingerprint,
            schema_version=prepared.schema_version,
            preparation_policy_version=prepared.preparation_policy_version,
        )
        source_ids = tuple(item.source_artifact_id for item in prepared.source_capture_refs)
        spec = command.prepared_packet
        return build_prepared_context_packet(
            packet_id=spec.packet_id,
            data=identity,
            emitted_at=spec.emitted_at_utc,
            traceid=context.traceid,
            runid=context.runid,
            scenarioid=context.scenarioid,
            module_version=spec.module_version,
            module_instance_id=spec.module_instance_id,
            derivedfrom=prepared.prepared_id,
            sourceartifactids=list(source_ids),
            inputfingerprint=prepared.prepared_fingerprint,
            source_artifact_validator=lambda value: value in source_ids,
            input_fingerprint_validator=lambda value: value == prepared.prepared_fingerprint,
            owner_check_validator=lambda name, _: name in _PREPARED_OWNER_CHECKS,
            summary_keyflags=[prepared.validation_state, prepared.completeness_state],
        )

    @staticmethod
    def _validate_scope(scope: PaperRunScope, context: DmpV3ExecutionContext) -> PaperRunScope:
        required = (
            getattr(scope, "scope_id", None),
            getattr(scope, "trace_id", None),
            getattr(scope, "run_id", None),
            getattr(scope, "scenario_id", None),
            getattr(scope, "execution_port", None),
            getattr(scope, "portfolio_service", None),
        )
        if any(value is None or value == "" for value in required):
            raise ValueError("paper_run_scope_incomplete")
        if (scope.trace_id, scope.run_id, scope.scenario_id) != (
            context.traceid,
            context.runid,
            context.scenarioid,
        ):
            raise ValueError("paper_run_scope_execution_context_mismatch")
        if not callable(getattr(scope.portfolio_service, "reconcile_fill", None)) or not callable(
            getattr(scope.portfolio_service, "snapshot", None)
        ):
            raise ValueError("paper_run_scope_portfolio_service_invalid")
        return scope

    def run(self, command: ApplicationCommand) -> ApplicationRunReceipt:
        governed = self._command(command)
        context = governed.execution_context
        steps: list[str] = []

        prepared_packet = self._prepared_packet(governed)
        steps.append("prepared_context_packet")
        serial = self._serial_runner.run(
            context=governed.serial_context,
            stage_inputs=governed.serial_stage_inputs,
        )
        steps.append("serial")
        parallel = self._parallel_evaluator.evaluate(governed.parallel_input)
        steps.append("parallel")

        base = {
            "command_id": governed.command_id,
            "trace_id": context.traceid,
            "run_id": context.runid,
            "scenario_id": context.scenarioid,
            "owner_steps": tuple(steps),
            "prepared_context_packet": prepared_packet,
            "serial_candidate": serial,
            "parallel_assessment": parallel,
        }
        if serial.status != "formed":
            return ApplicationRunReceipt.create(
                **base,
                outcome=f"serial_{serial.status}",
            )

        serial_spec = governed.serial_packet
        serial_packet = self._serial_packet_adapter.emit(
            serial,
            prepared_context_packet=prepared_packet,
            execution_context=context,
            packet_id=serial_spec.packet_id,
            emitted_at=serial_spec.emitted_at_utc,
            module_version=serial_spec.module_version,
            module_instance_id=serial_spec.module_instance_id,
        )
        steps.append("serial_packet")
        parallel_spec = governed.parallel_packet
        parallel_packet = self._parallel_packet_adapter.emit(
            parallel,
            prepared_context_packet=prepared_packet,
            execution_context=context,
            packet_id=parallel_spec.packet_id,
            emitted_at=parallel_spec.emitted_at_utc,
            module_version=parallel_spec.module_version,
            module_instance_id=parallel_spec.module_instance_id,
        )
        steps.append("parallel_packet")
        final_risk = self._capital_authority.join_final_risk(
            serial_packet,
            parallel_packet,
            governed.final_risk_policy,
        )
        steps.append("final_risk")
        capital_decision = self._capital_authority.evaluate_capital(
            final_risk,
            governed.capital_state,
            governed.modifier_receipt,
            governed.capital_policy,
        )
        capital_receipt = self._capital_authority.build_receipt(
            capital_decision,
            final_risk,
            governed.capital_state,
            governed.modifier_receipt,
            governed.capital_policy,
            emitted_at_utc=governed.capital_receipt_emitted_at_utc,
        )
        steps.append("capital")
        downstream = {
            **base,
            "owner_steps": tuple(steps),
            "serial_packet": serial_packet,
            "parallel_packet": parallel_packet,
            "final_risk_decision": final_risk,
            "capital_decision": capital_decision,
            "capital_receipt": capital_receipt,
        }
        if capital_decision.action in {"block", "no_trade"}:
            return ApplicationRunReceipt.create(
                **downstream,
                outcome=capital_decision.action,
            )

        scope = self._validate_scope(self._paper_run_scope_factory(context), context)
        steps.append("scope")
        intent = self._execution_gateway.create_intent(
            capital_receipt,
            governed.placement_policy,
            limit_price=governed.limit_price,
            intent_at_utc=governed.intent_at_utc,
        )
        execution = self._execution_gateway.execute(
            intent,
            scope.execution_port,
            executed_at_utc=governed.executed_at_utc,
        )
        steps.append("paper_execution")
        reconciliation = scope.portfolio_service.reconcile_fill(execution)
        snapshot = scope.portfolio_service.snapshot()
        steps.append("portfolio_reconciliation")
        final_material = {
            **downstream,
            "owner_steps": tuple(steps),
        }
        return ApplicationRunReceipt.create(
            **final_material,
            outcome="paper_filled",
            run_scope_id=scope.scope_id,
            placement_intent=intent,
            execution_receipt=execution,
            fill_reconciliation_receipt=reconciliation,
            portfolio_snapshot=snapshot,
        )

    def query(self, query: ApplicationQuery) -> ReviewProjection:
        governed = self._query(query)
        assessment = self._replay_service.assess(
            governed.envelope,
            reproduced_output_id=governed.reproduced_output_id,
            reproduced_output_fingerprint=governed.reproduced_output_fingerprint,
            reproduced_reasons=governed.reproduced_reasons,
            executable_versions=governed.executable_versions,
            isolated_execution=governed.isolated_execution,
            live_side_effects=governed.live_side_effects,
            runtime_authority_promoted=governed.runtime_authority_promoted,
        )
        return self._replay_service.project(
            envelope=governed.envelope,
            assessment=assessment,
        )
