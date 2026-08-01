"""Tier-A seam proof for mandatory M05/M06 DMPV3 carriage into M09."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.contracts.packets import (
    DmpV3ExecutionContext,
    dmp_v3_carriage_fingerprint,
)
from nvda_desk.m05_serial_cognition import SerialCandidatePacketAdapter
from nvda_desk.m06_parallel_risk import ParallelRiskPacketAdapter
from tests.support.m09_k11_k14_contract_harness import (
    production_api,
    production_canonical_packet_pair,
    production_modifier_receipt,
    production_parallel_assessment,
    production_serial_candidate,
)


def _domain_pair():
    parallel = production_parallel_assessment(vix_level=20.0)
    serial = production_serial_candidate(
        prepared_id=parallel.prepared_id,
        prepared_fingerprint=parallel.prepared_fingerprint,
    )
    return serial, parallel


def test_execution_context_is_caller_owned_and_rejects_placeholder_identity() -> None:
    context = DmpV3ExecutionContext(
        traceid="trace.m09.001",
        runid="run.m09.001",
        scenarioid="scenario.m09.001",
    )
    assert context.traceid == "trace.m09.001"
    for field_name, value in (
        ("traceid", ""),
        ("runid", "generated"),
        ("scenarioid", "live"),
    ):
        values = context.model_dump()
        values[field_name] = value
        with pytest.raises(ValueError):
            DmpV3ExecutionContext.model_validate(values)


def test_canonical_m09_ingress_requires_packets_and_preserves_exact_lineage() -> None:
    api = production_api()
    serial_packet, parallel_packet, prepared_packet = production_canonical_packet_pair()
    service = api["CapitalAuthorityService"]()
    policy = api["FinalRiskJoinPolicy"](
        policy_version="m09.final-risk-join.v1",
        cautions_prohibit=False,
    )

    result = service.join_final_risk(serial_packet, parallel_packet, policy)

    assert result.action == "eligible_for_capital_assessment"
    assert result.carriage_validated is True
    assert result.trace_id == serial_packet.traceid == parallel_packet.traceid
    assert result.run_id == serial_packet.runid == parallel_packet.runid
    assert result.scenario_id == serial_packet.scenarioid == parallel_packet.scenarioid
    assert result.prepared_context_packet_id == prepared_packet.id
    assert result.serial_packet_id == serial_packet.id
    assert result.parallel_packet_id == parallel_packet.id
    assert result.serial_packet_carriage_fingerprint == dmp_v3_carriage_fingerprint(serial_packet)
    assert result.parallel_packet_carriage_fingerprint == dmp_v3_carriage_fingerprint(parallel_packet)


def test_canonical_m09_ingress_rejects_unpacketised_domain_products() -> None:
    api = production_api()
    serial, parallel = _domain_pair()
    policy = api["FinalRiskJoinPolicy"](
        policy_version="m09.final-risk-join.v1",
        cautions_prohibit=False,
    )
    with pytest.raises(TypeError, match="canonical_dmpv3_packet_required"):
        api["CapitalAuthorityService"]().join_final_risk(serial, parallel, policy)


def test_canonical_m09_ingress_rejects_cross_run_and_prepared_parent_mismatch() -> None:
    api = production_api()
    serial_packet, parallel_packet, _ = production_canonical_packet_pair()
    policy = api["FinalRiskJoinPolicy"](
        policy_version="m09.final-risk-join.v1",
        cautions_prohibit=False,
    )
    service = api["CapitalAuthorityService"]()

    cross_run = parallel_packet.model_copy(update={"runid": "run.other.001"})
    with pytest.raises(ValueError, match="packet_execution_context_mismatch"):
        service.join_final_risk(serial_packet, cross_run, policy)

    extensions = parallel_packet.model_dump(mode="python")["dmpextensions"]
    extensions["nvda"]["prepared_context"]["packet_id"] = "packet.prepared.other"
    wrong_parent = parallel_packet.model_copy(update={"dmpextensions": extensions})
    with pytest.raises(ValueError, match="prepared_context_packet_mismatch"):
        service.join_final_risk(serial_packet, wrong_parent, policy)


def test_canonical_m09_ingress_rejects_wrong_role_and_producer() -> None:
    api = production_api()
    serial_packet, parallel_packet, _ = production_canonical_packet_pair()
    policy = api["FinalRiskJoinPolicy"](
        policy_version="m09.final-risk-join.v1",
        cautions_prohibit=False,
    )
    service = api["CapitalAuthorityService"]()

    wrong_role = serial_packet.model_copy(update={"packetrole": "parallel_risk_packet"})
    with pytest.raises(ValueError, match="serial_packet_role_invalid"):
        service.join_final_risk(wrong_role, parallel_packet, policy)

    producer = parallel_packet.producer.model_copy(update={"module_id": "m05_serial_cognition"})
    wrong_producer = parallel_packet.model_copy(update={"producer": producer})
    with pytest.raises(ValueError, match="parallel_packet_producer_invalid"):
        service.join_final_risk(serial_packet, wrong_producer, policy)


def test_carriage_fingerprint_ignores_occurrence_identity_but_binds_semantics() -> None:
    serial_packet, _, _ = production_canonical_packet_pair()
    shifted = serial_packet.model_copy(
        update={
            "id": "packet.m05.serial.occurrence.002",
            "time": serial_packet.time + timedelta(seconds=5),
        }
    )
    changed_context = serial_packet.model_copy(update={"runid": "run.changed.001"})

    assert dmp_v3_carriage_fingerprint(serial_packet) == dmp_v3_carriage_fingerprint(shifted)
    assert dmp_v3_carriage_fingerprint(serial_packet) != dmp_v3_carriage_fingerprint(changed_context)


def test_m05_and_m06_adapters_reject_wrong_payload_state_or_parent_context() -> None:
    serial, parallel = _domain_pair()
    serial_packet, parallel_packet, prepared_packet = production_canonical_packet_pair(
        serial=serial,
        parallel=parallel,
    )
    assert isinstance(SerialCandidatePacketAdapter(), SerialCandidatePacketAdapter)
    assert isinstance(ParallelRiskPacketAdapter(), ParallelRiskPacketAdapter)

    withheld = serial.model_copy(update={"status": "withheld", "candidate_id": None})
    with pytest.raises(ValueError, match="formed_serial_candidate_required"):
        SerialCandidatePacketAdapter().emit(
            withheld,
            prepared_context_packet=prepared_packet,
            execution_context=DmpV3ExecutionContext(
                traceid=serial_packet.traceid,
                runid=serial_packet.runid,
                scenarioid=serial_packet.scenarioid,
            ),
            packet_id="packet.m05.invalid",
            emitted_at=datetime(2026, 8, 1, 1, 0, tzinfo=UTC),
            module_version="1.0.0",
            module_instance_id="m05.instance.001",
        )

    wrong_context = DmpV3ExecutionContext(
        traceid=parallel_packet.traceid,
        runid="run.other.001",
        scenarioid=parallel_packet.scenarioid,
    )
    with pytest.raises(ValueError, match="prepared_packet_execution_context_mismatch"):
        ParallelRiskPacketAdapter().emit(
            parallel,
            prepared_context_packet=prepared_packet,
            execution_context=wrong_context,
            packet_id="packet.m06.invalid",
            emitted_at=datetime(2026, 8, 1, 1, 0, tzinfo=UTC),
            module_version="1.0.0",
            module_instance_id="m06.instance.001",
        )


def test_legacy_orchestrator_and_bootstrap_evaluator_are_explicitly_noncanonical() -> None:
    from nvda_desk.risk.parallel import evaluate as legacy_parallel
    from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator

    assert DeskRuntimeOrchestrator.canonical_runtime_route is False
    assert DeskRuntimeOrchestrator.compatibility_scope == "legacy_pre_m00_serial_runtime_specimen"
    assert legacy_parallel.CANONICAL_M06_ROUTE is False
    assert legacy_parallel.COMPATIBILITY_SCOPE == "legacy_parallel_risk_bootstrap_specimen"

    service_source = __import__(
        "inspect"
    ).getsource(production_api()["CapitalAuthorityService"])
    assert "parallel_risk_bootstrap_input" not in service_source
    assert "DeskRuntimeOrchestrator" not in service_source


def test_packet_lineage_is_bound_into_capital_decision_and_receipt() -> None:
    api = production_api()
    serial_packet, parallel_packet, _ = production_canonical_packet_pair()
    service = api["CapitalAuthorityService"]()
    join_policy = api["FinalRiskJoinPolicy"](
        policy_version="m09.final-risk-join.v1",
        cautions_prohibit=False,
    )
    final = service.join_final_risk(serial_packet, parallel_packet, join_policy)
    capital = api["CapitalState"].create(
        state_id="capital.state.packet-lineage",
        account_id="account.packet-lineage",
        state_version=1,
        effective_at_utc=datetime(2026, 8, 1, 0, 0, tzinfo=UTC),
        available_capital=Decimal("100000"),
        reserved_capital=Decimal("0"),
        max_fresh_deployable_pct=Decimal("12"),
        source_authority_ref="capital.snapshot.authority.v1",
    )
    capital_policy = api["CapitalDeploymentPolicy"](
        policy_version="m09.capital-policy.v1",
        target_pct=Decimal("10"),
        hard_max_pct=Decimal("15"),
        caution_multiplier=Decimal("0.5"),
        rounding_quantum=Decimal("0.01"),
    )
    modifier = production_modifier_receipt()
    decision = service.evaluate_capital(final, capital, modifier, capital_policy)
    receipt = service.build_receipt(
        decision, final, capital, modifier, capital_policy,
        emitted_at_utc=datetime(2026, 8, 1, 2, 0, tzinfo=UTC),
    )
    for field_name in (
        "trace_id", "run_id", "scenario_id", "prepared_context_packet_id",
        "prepared_context_carriage_fingerprint", "serial_packet_id",
        "serial_packet_carriage_fingerprint", "parallel_packet_id",
        "parallel_packet_carriage_fingerprint",
    ):
        assert getattr(decision, field_name) == getattr(final, field_name)
        assert getattr(receipt, field_name) == getattr(final, field_name)
    assert decision.carriage_validated is receipt.carriage_validated is True


def test_domain_compatibility_join_cannot_authorise_capital() -> None:
    api = production_api()
    serial, parallel = _domain_pair()
    service = api["CapitalAuthorityService"]()
    join_policy = api["FinalRiskJoinPolicy"](
        policy_version="m09.final-risk-join.v1",
        cautions_prohibit=False,
    )
    final = service.join_final_risk_domain_for_compatibility(serial, parallel, join_policy)
    assert final.carriage_validated is False
    capital = api["CapitalState"].create(
        state_id="capital.state.compatibility",
        account_id="account.compatibility",
        state_version=1,
        effective_at_utc=datetime(2026, 8, 1, 0, 0, tzinfo=UTC),
        available_capital=Decimal("100000"),
        reserved_capital=Decimal("0"),
        max_fresh_deployable_pct=Decimal("12"),
        source_authority_ref="capital.snapshot.authority.v1",
    )
    capital_policy = api["CapitalDeploymentPolicy"](
        policy_version="m09.capital-policy.v1",
        target_pct=Decimal("10"),
        hard_max_pct=Decimal("15"),
        caution_multiplier=Decimal("0.5"),
        rounding_quantum=Decimal("0.01"),
    )
    with pytest.raises(ValueError, match="canonical_packet_carriage_required"):
        service.evaluate_capital(
            final, capital, production_modifier_receipt(), capital_policy
        )
