"""Reference-only M00 composition contract and production API loader.

The reference functions encode the admitted C-NORM ordering and fail-closed
properties without providing the production composition root.  Production
conformance is exercised only through ``production_api``.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Callable


@dataclass(frozen=True)
class ReferenceCommand:
    command_id: str = "m00.command.001"
    prepared_id: str = "prepared.001"
    prepared_fingerprint: str = "a" * 64
    trace_id: str = "trace.001"
    run_id: str = "run.001"
    scenario_id: str = "paper.alpha.001"
    prepared_packet_id: str = "packet.prepared.001"
    serial_packet_id: str = "packet.serial.001"
    parallel_packet_id: str = "packet.parallel.001"
    serial_emitted_at_utc: datetime = datetime(2026, 8, 1, 1, 0, tzinfo=UTC)
    parallel_emitted_at_utc: datetime = datetime(2026, 8, 1, 1, 0, tzinfo=UTC)
    capital_emitted_at_utc: datetime = datetime(2026, 8, 1, 1, 1, tzinfo=UTC)
    intent_at_utc: datetime = datetime(2026, 8, 1, 1, 2, tzinfo=UTC)
    executed_at_utc: datetime = datetime(2026, 8, 1, 1, 3, tzinfo=UTC)


@dataclass(frozen=True)
class ReferenceRunReceipt:
    command_id: str
    run_id: str
    outcome: str
    owner_steps: tuple[str, ...]
    scope_id: str | None
    replay_class: None = None
    live_execution_proven: bool = False
    durable_state_proven: bool = False


class RecordingOwners:
    """Deterministic owner-seam specimen used only by the C-PROOF reference tests."""

    def __init__(self, *, capital_action: str = "continue") -> None:
        self.capital_action = capital_action
        self.calls: list[str] = []
        self.scope_counter = 0

    def call(self, name: str) -> dict[str, Any]:
        self.calls.append(name)
        if name == "capital":
            return {"action": self.capital_action}
        return {"owner": name}

    def new_scope(self) -> str:
        self.scope_counter += 1
        scope_id = f"scope.{self.scope_counter}"
        self.calls.append(f"scope:{scope_id}")
        return scope_id


def _require_nonempty(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"missing_{field}")


def _require_utc(value: datetime, field: str) -> None:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError(f"{field}_must_be_utc")


def evaluate_reference(command: ReferenceCommand, owners: RecordingOwners) -> ReferenceRunReceipt:
    """Evaluate the minimal admitted M00 order with no production implementation."""

    for field in (
        "command_id",
        "prepared_id",
        "prepared_fingerprint",
        "trace_id",
        "run_id",
        "scenario_id",
        "prepared_packet_id",
        "serial_packet_id",
        "parallel_packet_id",
    ):
        _require_nonempty(getattr(command, field), field)
    if len(command.prepared_fingerprint) != 64:
        raise ValueError("invalid_prepared_fingerprint")

    times = (
        ("serial_emitted_at_utc", command.serial_emitted_at_utc),
        ("parallel_emitted_at_utc", command.parallel_emitted_at_utc),
        ("capital_emitted_at_utc", command.capital_emitted_at_utc),
        ("intent_at_utc", command.intent_at_utc),
        ("executed_at_utc", command.executed_at_utc),
    )
    for field, value in times:
        _require_utc(value, field)
    if command.capital_emitted_at_utc < max(
        command.serial_emitted_at_utc, command.parallel_emitted_at_utc
    ):
        raise ValueError("capital_time_precedes_owner_packets")
    if not (command.capital_emitted_at_utc <= command.intent_at_utc <= command.executed_at_utc):
        raise ValueError("execution_time_order_invalid")

    for name in (
        "prepared_context_packet",
        "serial",
        "parallel",
        "serial_packet",
        "parallel_packet",
        "final_risk",
    ):
        owners.call(name)
    capital = owners.call("capital")
    action = capital["action"]
    if action in {"block", "no_trade"}:
        return ReferenceRunReceipt(
            command_id=command.command_id,
            run_id=command.run_id,
            outcome=action,
            owner_steps=tuple(owners.calls),
            scope_id=None,
        )
    if action not in {"continue", "reduce"}:
        raise ValueError("unsupported_capital_action")

    scope_id = owners.new_scope()
    owners.call("paper_execution")
    owners.call("portfolio_reconciliation")
    return ReferenceRunReceipt(
        command_id=command.command_id,
        run_id=command.run_id,
        outcome="paper_filled",
        owner_steps=tuple(owners.calls),
        scope_id=scope_id,
    )


def evaluate_query_reference(*, run_calls: list[str], replay_calls: list[str]) -> str:
    """Prove that the M12 query path is separate from runtime execution."""

    replay_calls.extend(("assess", "project"))
    if run_calls:
        raise AssertionError("application_query_invoked_runtime")
    return "review_projection"


def _mutant_places_after_block(command: ReferenceCommand) -> ReferenceRunReceipt:
    owners = RecordingOwners(capital_action="block")
    receipt = evaluate_reference(command, owners)
    owners.new_scope()
    owners.call("paper_execution")
    return ReferenceRunReceipt(
        command_id=receipt.command_id,
        run_id=receipt.run_id,
        outcome="paper_filled",
        owner_steps=tuple(owners.calls),
        scope_id="scope.1",
    )


def _mutant_reuses_scope(command: ReferenceCommand) -> tuple[str | None, str | None]:
    owners = RecordingOwners()
    first = evaluate_reference(command, owners)
    # Deliberately returns the prior scope rather than creating another run scope.
    return first.scope_id, first.scope_id


def _mutant_promotes_runtime_to_replay(command: ReferenceCommand) -> dict[str, Any]:
    receipt = evaluate_reference(command, RecordingOwners())
    return {"receipt": receipt, "replay_class": "preserved_occurrence_replay"}


MUTANTS: dict[str, Callable[[ReferenceCommand], Any]] = {
    "places_after_block": _mutant_places_after_block,
    "reuses_scope": _mutant_reuses_scope,
    "promotes_runtime_to_replay": _mutant_promotes_runtime_to_replay,
}


def production_api() -> dict[str, Any]:
    module = importlib.import_module("nvda_desk.m00_application_shell")
    required = (
        "ApplicationCommand",
        "ApplicationQuery",
        "ApplicationRunReceipt",
        "RunCoordinator",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise AssertionError(f"canonical M00 package missing exports: {missing}")
    prohibited = ("DeskRuntimeOrchestrator", "HttpApp")
    leaked = [name for name in prohibited if hasattr(module, name)]
    if leaked:
        raise AssertionError(f"canonical M00 package leaked compatibility owners: {leaked}")
    return {name: getattr(module, name) for name in required}


@dataclass(frozen=True)
class TestPaperRunScope:
    scope_id: str
    trace_id: str
    run_id: str
    scenario_id: str
    execution_port: Any
    portfolio_service: Any


class RecordingPaperRunScopeFactory:
    """Create one fresh M10/M11 paper scope bound to the caller run identity."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, str]] = []
        self.scopes: list[TestPaperRunScope] = []

    def __call__(self, execution_context) -> TestPaperRunScope:
        from nvda_desk.m10_execution_gateway import PaperExecutionPort
        from nvda_desk.m11_portfolio_lifecycle import PortfolioLifecycleService

        identity = (
            execution_context.traceid,
            execution_context.runid,
            execution_context.scenarioid,
        )
        self.calls.append(identity)
        scope = TestPaperRunScope(
            scope_id=f"paper-scope:{execution_context.runid}",
            trace_id=execution_context.traceid,
            run_id=execution_context.runid,
            scenario_id=execution_context.scenarioid,
            execution_port=PaperExecutionPort(),
            portfolio_service=PortfolioLifecycleService(),
        )
        self.scopes.append(scope)
        return scope


class FixedParallelEvaluator:
    """Public-seam test double returning one already governed M06 assessment."""

    def __init__(self, assessment) -> None:
        self.assessment = assessment
        self.calls: list[str] = []

    def evaluate(self, risk_input):
        if (
            risk_input.prepared_id,
            risk_input.prepared_fingerprint,
        ) != (
            self.assessment.prepared_id,
            self.assessment.prepared_fingerprint,
        ):
            raise ValueError("parallel_test_double_prepared_lineage_mismatch")
        self.calls.append(risk_input.input_id)
        return self.assessment


class RecordingReplayService:
    """M12-shaped test double proving the query path is runtime-independent."""

    def __init__(self, *, assessment: Any, projection: Any) -> None:
        self.assessment = assessment
        self.projection = projection
        self.calls: list[str] = []

    def assess(self, envelope, **kwargs):
        del envelope, kwargs
        self.calls.append("assess")
        return self.assessment

    def project(self, *, envelope, assessment):
        del envelope, assessment
        self.calls.append("project")
        return self.projection


def _production_modifier_bundle(*, kill_switch: bool):
    """Build the exact M07 authority used by the canonical M05 service."""

    from nvda_desk.m07_coefficient_modifier_authority.contracts import (
        CoefficientMember,
        ModifierMember,
        PolicyBundle,
    )

    coefficients = tuple(
        CoefficientMember(
            coefficient_id=coefficient_id,
            coefficient_version="1.0.0",
            owner_stage="posture",
            value_type="decimal",
            units=units,
            baseline_value=Decimal(baseline),
            hard_lower_bound=Decimal(lower),
            hard_upper_bound=Decimal(upper),
            surface_class="mutable_runtime_surface",
            transform_family="bounded_decimal_algebra",
            runtime_mutability_class="runtime_mutable",
            promotion_lineage=f"authority://m07/{coefficient_id}/1.0.0",
        )
        for coefficient_id, units, baseline, lower, upper in (
            ("risk_vix_caution_threshold", "vix_points", "24", "0", "100"),
            ("risk_vix_hot_threshold", "vix_points", "32", "0", "100"),
            ("max_risk_per_trade", "fraction", "0.35", "0", "1"),
            ("hedge_required", "boolean_decimal", "0", "0", "1"),
        )
    )
    modifiers = ()
    if kill_switch:
        modifiers = (
            ModifierMember(
                modifier_id="capital_kill_switch",
                modifier_version="1.0.0",
                owner_stage="posture",
                target_coefficient_ids=("max_risk_per_trade",),
                applicability_fact_refs=("regime_normal",),
                precedence_rank=1,
                transform_operator="set",
                operand=Decimal("0"),
                combination_law="authority_ordered",
                kill_switch=True,
                restrictive_only=True,
                promotion_lineage="authority://m07/capital-kill-switch/1.0.0",
            ),
        )
    return PolicyBundle(
        bundle_id="m07.posture.runtime",
        bundle_version="1.0.0",
        schema_version="1.0.0",
        authority_id="m07.k12",
        authority_version="1.0.0",
        effective_version_selector="promoted:1.0.0",
        resolution_law_version="k12.v1",
        promotion_lineage="authority://m07/posture-runtime/1.0.0",
        owner_stage="posture",
        coefficients=coefficients,
        modifiers=modifiers,
    )


def _production_playbook_catalogue(*, eligibility_terminal: bool):
    """Build exact M08 authority whose constraint is evaluated from real M05 outputs."""

    from nvda_desk.m08_playbook_catalogue.contracts import (
        EligibilityConstraint,
        PlaybookCatalogue,
        PlaybookDefinition,
        catalogue_fingerprint,
    )

    definition = PlaybookDefinition(
        playbook_id="playbook.breakout",
        playbook_version="1.0.0",
        candidate_family_id="family.breakout",
        candidate_family_version="1.0.0",
        setup_variant_id="variant.breakout.confirmed",
        setup_variant_version="1.0.0",
        selection_priority=10,
        constraints=(
            EligibilityConstraint(
                fact_ref="gamma_state",
                operator="eq",
                expected="inactive" if eligibility_terminal else "active",
            ),
            EligibilityConstraint(
                fact_ref="spot_price",
                operator="eq",
                expected=999.0 if eligibility_terminal else 190.0,
            ),
        ),
        enabled=True,
        lifecycle_intent={
            "horizon_class": "intraday",
            "handoff_schema": "m05.expression.v1",
        },
        lifecycle_schema_version="1.0.0",
        promotion_lineage="authority://m08/playbook.breakout/1.0.0",
    )
    material = {
        "catalogue_id": "m08.nvda.playbooks",
        "catalogue_version": "1.0.0",
        "schema_version": "1.0.0",
        "authority_id": "m08.k13",
        "authority_version": "1.0.0",
        "effective_version_selector": "promoted:1.0.0",
        "eligibility_law_version": "k13.v1",
        "promotion_lineage": "authority://m08/catalogue/1.0.0",
        "definitions": (definition,),
    }
    return PlaybookCatalogue(
        **material,
        catalogue_fingerprint=catalogue_fingerprint(**material),
    )


def production_serial_cognition_request(
    prepared: Any,
    *,
    suffix: str = "001",
    kill_switch: bool = False,
    eligibility_terminal: bool = False,
    emitted_at_utc: datetime | None = None,
):
    """Build one exact M05 request from M03 and concrete M07/M08 authority."""

    import nvda_desk.m05_serial_cognition as m05

    authority_time = emitted_at_utc or max(
        datetime(2026, 8, 1, 4, 0, tzinfo=UTC),
        prepared.effective_at_utc,
    )
    return m05.SerialCognitionRequest(
        prepared_data=prepared,
        modifier_bundle=_production_modifier_bundle(kill_switch=kill_switch),
        playbook_catalogue=_production_playbook_catalogue(
            eligibility_terminal=eligibility_terminal
        ),
        modifier_receipt_id=f"m07.receipt.m00.{suffix}",
        modifier_application_id=f"m07.application.m00.{suffix}",
        modifier_receipt_emitted_at_utc=authority_time,
        eligibility_decision_id=f"m08.eligibility.m00.{suffix}",
    )


def production_runtime_fixture(
    api: dict[str, Any],
    *,
    suffix: str = "001",
    terminal_stage: str | None = None,
    kill_switch: bool = False,
    upstream_dependencies: dict[str, Any] | None = None,
    prepared_data: Any | None = None,
) -> dict[str, Any]:
    """Build one lawful M00 command using actual canonical M05 owner composition."""

    from tests.support.m06_k10_contract_harness import make_prepared
    from tests.support.m09_k11_k14_contract_harness import production_parallel_assessment

    import nvda_desk.m05_serial_cognition as m05
    import nvda_desk.m06_parallel_risk as m06
    import nvda_desk.m09_capital_authority as m09
    import nvda_desk.m10_execution_gateway as m10
    import nvda_desk.m12_evidence_replay as m12
    from nvda_desk.contracts.packets import DmpV3ExecutionContext

    if terminal_stage not in {None, "eligibility"}:
        raise ValueError(
            "production_runtime_fixture_only_supports_owner_driven_eligibility_terminal"
        )
    prepared = prepared_data if prepared_data is not None else make_prepared(vix_level=20.0)
    base_time = max(
        datetime(2026, 8, 1, 4, 0, tzinfo=UTC),
        prepared.effective_at_utc,
    )
    serial_request = production_serial_cognition_request(
        prepared,
        suffix=suffix,
        kill_switch=kill_switch,
        eligibility_terminal=terminal_stage == "eligibility",
        emitted_at_utc=base_time,
    )
    serial_cognition = m05.SerialCognitionService()
    parallel_input = m06.ParallelRiskInput.from_prepared(
        prepared,
        evaluator_policy_version="parallel-risk.compat.v1",
        aggregation_version="parallel-risk.aggregate.v1",
        threshold_authority_refs=("m07:block:v1", "m07:caution:v1"),
        vix_caution_threshold=30.0,
        vix_block_threshold=50.0,
    )
    parallel_assessment = production_parallel_assessment(vix_level=20.0, prepared_data=prepared)
    parallel_evaluator = FixedParallelEvaluator(parallel_assessment)
    execution_context = DmpV3ExecutionContext(
        traceid=f"trace.m00.{suffix}",
        runid=f"run.m00.{suffix}",
        scenarioid=f"scenario.m00.{suffix}",
    )
    capital_state = m09.CapitalState.create(
        state_id=f"capital.state.m00.{suffix}",
        account_id="paper.account.001",
        state_version=1,
        effective_at_utc=base_time,
        available_capital=Decimal("100000"),
        reserved_capital=Decimal("0"),
        max_fresh_deployable_pct=Decimal("12"),
        source_authority_ref="capital.snapshot.authority.v1",
    )
    command = api["ApplicationCommand"].model_validate(
        {
            "command_id": f"m00.command.{suffix}",
            "execution_context": execution_context,
            "prepared_data": prepared,
            "serial_cognition": serial_request,
            "parallel_input": parallel_input,
            "prepared_packet": {
                "packet_id": f"packet.m00.prepared.{suffix}",
                "emitted_at_utc": base_time,
                "module_version": "1.0.0",
                "module_instance_id": f"m03.prepared.instance.{suffix}",
            },
            "serial_packet": {
                "packet_id": f"packet.m00.serial.{suffix}",
                "emitted_at_utc": base_time.replace(minute=base_time.minute + 1),
                "module_version": "1.0.0",
                "module_instance_id": f"m05.serial.instance.{suffix}",
            },
            "parallel_packet": {
                "packet_id": f"packet.m00.parallel.{suffix}",
                "emitted_at_utc": base_time.replace(minute=base_time.minute + 1),
                "module_version": "1.0.0",
                "module_instance_id": f"m06.parallel.instance.{suffix}",
            },
            "final_risk_policy": m09.FinalRiskJoinPolicy(),
            "capital_state": capital_state,
            "capital_policy": m09.CapitalDeploymentPolicy(
                target_pct=Decimal("10"),
                hard_max_pct=Decimal("15"),
                caution_multiplier=Decimal("0.5"),
                rounding_quantum=Decimal("0.01"),
            ),
            "capital_receipt_emitted_at_utc": base_time.replace(minute=base_time.minute + 2),
            "placement_policy": m10.PlacementPolicy(quantity_quantum=Decimal("0.001")),
            "limit_price": Decimal("100"),
            "intent_at_utc": base_time.replace(minute=base_time.minute + 3),
            "executed_at_utc": base_time.replace(minute=base_time.minute + 4),
        }
    )
    scope_factory = RecordingPaperRunScopeFactory()
    coordinator = api["RunCoordinator"](
        serial_cognition=serial_cognition,
        parallel_evaluator=parallel_evaluator,
        serial_packet_adapter=m05.SerialCandidatePacketAdapter(),
        parallel_packet_adapter=m06.ParallelRiskPacketAdapter(),
        capital_authority=m09.CapitalAuthorityService(),
        execution_gateway=m10.ExecutionGateway(),
        paper_run_scope_factory=scope_factory,
        replay_service=m12.EvidenceReplayService(),
        **(upstream_dependencies or {}),
    )
    return {
        "command": command,
        "coordinator": coordinator,
        "scope_factory": scope_factory,
        "parallel_evaluator": parallel_evaluator,
        "serial_cognition": serial_cognition,
    }


def production_query(api: dict[str, Any], *, suffix: str = "001"):
    """Build one exact comparison-only M12 query for the M00 read path."""

    from nvda_desk.contracts.replay import ReplayPacketLineage
    from nvda_desk.contracts.review import ReviewPacket
    from nvda_desk.m10_execution_gateway.contracts import semantic_fingerprint
    from nvda_desk.m12_evidence_replay import EvidenceReplayService

    service = EvidenceReplayService()
    packet_content = ReplayPacketLineage(
        packet_ids=[f"packet:m00:{suffix}"],
        replay_run_id=f"source-run:m00:{suffix}",
    )
    output_content = ReviewPacket(
        packet_id=f"capital-decision:m00:{suffix}",
        summary="stand_down",
        sections=["stand_down"],
    )
    packet_material = service.build_material(
        owner_module="M04",
        contract_version="1.0.0",
        occurrence_id=f"packet-occurrence:m00:{suffix}",
        content=packet_content,
        sequence=0,
        material_time_utc=datetime(2026, 8, 1, 5, 0, tzinfo=UTC),
        material_label="packet",
    )
    output_material = service.build_material(
        owner_module="M09",
        contract_version="1.0.0",
        occurrence_id=f"decision-occurrence:m00:{suffix}",
        content=output_content,
        sequence=1,
        material_time_utc=datetime(2026, 8, 1, 5, 1, tzinfo=UTC),
        material_label="original-output",
    )
    envelope = service.build_envelope(
        replay_run_id=f"replay-run:m00:{suffix}",
        replay_class="comparison_only",
        target_id=output_content.packet_id,
        original_output_id=output_content.packet_id,
        original_output_occurrence_id=output_material.occurrence_id,
        original_output_fingerprint=semantic_fingerprint(output_content.model_dump(mode="python")),
        original_reasons=("stand_down",),
        materials=(packet_material, output_material),
        executable_versions=("m09.capital.v1",),
    )
    return api["ApplicationQuery"].model_validate(
        {
            "query_id": f"m00.query.{suffix}",
            "envelope": envelope,
            "reproduced_output_id": None,
            "reproduced_output_fingerprint": None,
            "reproduced_reasons": None,
            "executable_versions": None,
            "isolated_execution": True,
            "live_side_effects": (),
            "runtime_authority_promoted": False,
        }
    )


def dataclass_replace(value, **changes):
    """Local alias avoids shadowing the module-level reference command helper."""

    from dataclasses import replace

    return replace(value, **changes)
