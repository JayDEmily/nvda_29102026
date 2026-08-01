"""Tier-A seam proof for mandatory M05/M06 DMPV3 carriage into M09."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

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
