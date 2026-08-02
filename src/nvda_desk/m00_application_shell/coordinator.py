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
from nvda_desk.m01_source_admission import SourceAdmissionService
from nvda_desk.m02_financial_calendar import CalendarResolver
from nvda_desk.m03_preparation import (
    CalendarProjectionReference,
    PreparedDataBuilder,
    SourceCaptureReference,
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

from .contracts import (
    ApplicationCommand,
    ApplicationQuery,
    ApplicationRunReceipt,
    UpstreamPreparationCommand,
    UpstreamPreparationReceipt,
)

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
        source_admission: SourceAdmissionService | None = None,
        calendar_resolver: CalendarResolver | None = None,
        prepared_data_builder: PreparedDataBuilder | None = None,
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
        self._source_admission = source_admission
        self._calendar_resolver = calendar_resolver
        self._prepared_data_builder = prepared_data_builder

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
    def _upstream_command(value: UpstreamPreparationCommand) -> UpstreamPreparationCommand:
        if not isinstance(value, UpstreamPreparationCommand):
            raise TypeError("typed_upstream_preparation_command_required")
        try:
            return UpstreamPreparationCommand.model_validate(value.model_dump(mode="python"))
        except (ValidationError, ValueError, TypeError) as exc:
            raise ValueError("upstream_preparation_command_contract_invalid") from exc

    def prepare(self, command: UpstreamPreparationCommand) -> UpstreamPreparationReceipt:
        """Delegate exact M01, M02 and M03 work without acquiring owner semantics."""

        missing = tuple(
            name
            for name, value in (
                ("source_admission", self._source_admission),
                ("calendar_resolver", self._calendar_resolver),
                ("prepared_data_builder", self._prepared_data_builder),
            )
            if value is None
        )
        if missing:
            raise ValueError(f"m00_upstream_dependency_missing:{','.join(missing)}")
        governed = self._upstream_command(command)
        source_service = self._source_admission
        calendar_resolver = self._calendar_resolver
        prepared_builder = self._prepared_data_builder
        assert source_service is not None
        assert calendar_resolver is not None
        assert prepared_builder is not None

        source_results = tuple(source_service.admit(item) for item in governed.source_requests)
        non_admissions = tuple(item for item in source_results if item.status == "not_admitted")
        if non_admissions:
            return UpstreamPreparationReceipt.create(
                command_id=governed.command_id,
                status="source_not_admitted",
                source_results=source_results,
                failure_stage="M01",
                failure_reason=non_admissions[0].reason,
            )

        calendar_projections = tuple(
            calendar_resolver.project(
                item.snapshot,
                item.policy,
                projection_id=item.projection_id,
            )
            for item in governed.calendar_requests
        )
        unusable = tuple(
            item for item in calendar_projections if item.status in {"withheld", "rejected"}
        )
        if unusable:
            reason_parts = (
                *unusable[0].missing_mandatory_authority,
                *unusable[0].unresolved_conflicts,
            )
            return UpstreamPreparationReceipt.create(
                command_id=governed.command_id,
                status="calendar_withheld",
                source_results=source_results,
                calendar_projections=calendar_projections,
                failure_stage="M02",
                failure_reason=":".join(reason_parts) or unusable[0].status,
            )

        accepted = tuple(item for item in source_results if item.status == "accepted")
        admitted_ids = {item.source_artifact.source_artifact_id for item in accepted}
        source_refs = tuple(
            SourceCaptureReference(
                capture_id=item.source_artifact.capture_receipt.capture_id,
                source_artifact_id=item.source_artifact.source_artifact_id,
                family_id=item.source_artifact.family_id,
                contract_id=item.source_artifact.contract_id,
                schema_version=item.source_artifact.schema_version,
                source_owner=(
                    item.source_artifact.source_identifier.owner or item.source_artifact.provider_id
                ),
                effective_at_utc=(
                    item.source_artifact.observed_at_utc
                    or item.source_artifact.capture_receipt.captured_at_utc
                ),
                source_time_utc=item.source_artifact.observed_at_utc,
                source_date=item.source_artifact.source_date,
                temporal_precision=item.source_artifact.source_time_precision.value,
                input_fingerprint=item.source_artifact.content_sha256,
                validation_state=(
                    "valid" if item.source_artifact.validation_status == "admitted" else "degraded"
                ),
                limitations=item.source_artifact.limitations,
                semantic_fields=tuple(sorted(item.source_artifact.typed_payload.model_dump())),
                provider_id=item.source_artifact.provider_id,
                acquisition_method=item.source_artifact.acquisition_channel,
            )
            for item in accepted
        )
        projection_refs = []
        for projection in calendar_projections:
            source_refs_for_projection = tuple(
                sorted(
                    {
                        source_ref
                        for selected in projection.selected_fields
                        for source_ref in selected.source_refs
                    }
                )
            )
            foreign = tuple(
                source_id
                for source_id, _ in source_refs_for_projection
                if source_id not in admitted_ids
            )
            if foreign:
                raise ValueError(
                    "calendar_projection_source_lineage_not_admitted:" + ",".join(foreign)
                )
            projection_refs.append(
                CalendarProjectionReference(
                    projection_id=projection.projection_id,
                    snapshot_id=projection.snapshot_id,
                    snapshot_version=projection.snapshot_version,
                    projection_policy_version=projection.projection_policy_version,
                    status=projection.status,
                    semantic_fingerprint=projection.semantic_fingerprint,
                    source_refs=source_refs_for_projection,
                )
            )

        spec = governed.preparation
        prepared = prepared_builder.build(
            source_capture_refs=source_refs,
            calendar_projection_refs=tuple(projection_refs),
            input_schema_versions=dict(spec.input_schema_versions),
            schema_version=spec.schema_version,
            preparation_policy_version=spec.preparation_policy_version,
            alignment_policy_version=spec.alignment_policy_version,
            fingerprint_policy_version=spec.fingerprint_policy_version,
            canonicalisation_version=spec.canonicalisation_version,
            derivation_versions=dict(spec.derivation_versions),
            effective_at_utc=spec.effective_at_utc,
            payload=spec.payload,
            payload_schema_version=spec.payload_schema_version,
            field_resolution_receipts=spec.field_resolution_receipts,
            derivation_receipts=spec.derivation_receipts,
            validation_state=spec.validation_state,
            completeness_state=spec.completeness_state,
            limitations=spec.limitations,
            failed_mandatory_transformations=spec.failed_mandatory_transformations,
            missing_optional_enrichments=spec.missing_optional_enrichments,
            parent_prepared_ids=spec.parent_prepared_ids,
        )
        return UpstreamPreparationReceipt.create(
            command_id=governed.command_id,
            status="prepared",
            source_results=source_results,
            calendar_projections=calendar_projections,
            prepared_data=prepared,
        )

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
