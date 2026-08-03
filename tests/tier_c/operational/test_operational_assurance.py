"""Tier C operational assurance across installed, restart and external boundaries."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict, Field
from tests.support.m00_application_shell_contract_harness import (
    production_api,
    production_runtime_fixture,
)
from tests.tier_a.m00_application_shell.test_m00_upstream_workflow_contract import (
    _coordinator as upstream_coordinator,
)
from tests.tier_a.operations.test_live_operational_boundaries import _live_intent


class _OperationalMarketPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    source_time_utc: datetime
    runtime_bar_time_utc: datetime
    spot_price: float
    front_dte: int
    next_dte: int
    next_event_time_utc: datetime
    nvda_return_pct: float
    nq_return_pct: float
    vix_level: float


def _operational_upstream_fixture() -> dict[str, Any]:
    from tests.support.m02_k04_contract_harness import (
        field_policy,
        production_policy_payload,
        production_snapshot_payload,
        valid_snapshot,
    )

    from nvda_desk import m01_source_admission as m01
    from nvda_desk import m02_financial_calendar as m02
    from nvda_desk import m03_preparation as m03
    from nvda_desk.m00_application_shell import (
        CalendarProjectionRequest,
        PreparationSpec,
        UpstreamPreparationCommand,
    )

    observed_at = datetime(2026, 7, 31, 10, 0, tzinfo=UTC)
    payload = _OperationalMarketPayload(
        symbol="NVDA",
        source_time_utc=observed_at,
        runtime_bar_time_utc=observed_at,
        spot_price=190.0,
        front_dte=5,
        next_dte=12,
        next_event_time_utc=observed_at + timedelta(days=2),
        nvda_return_pct=1.2,
        nq_return_pct=0.4,
        vix_level=20.0,
    )
    source_identifier = m01.SourceIdentifierContract(
        requirement=m01.SourceFactRequirement.REQUIRED,
        owner="recorded-provider",
        namespace="recorded-provider/operational-market",
        uniqueness_scope="recorded-provider/operational-market",
        stability_rule="stable_for_source_object_lifetime",
        generation_rule="issued_by_upstream_provider",
    )
    contract = m01.SourceFamilyContract(
        family_id="market_runtime",
        contract_id="source.market.v1",
        schema_version="1.0.0",
        payload_model=_OperationalMarketPayload,
        providers=(
            m01.SourceProviderContract(
                provider_id="recorded-provider",
                acquisition_channels=("recorded_api_response",),
            ),
        ),
        source_identifier=source_identifier,
        source_time_kind=m01.SourceTimeKind.INSTANT,
        downstream_owner=m01.SourceDownstreamOwner.M03,
        output_contract=m01.SourceOutputContract.RAW_SIGNAL_BATCH,
        signal_family_id="market_runtime",
        semantic_bindings=(
            m01.SourceSemanticBinding(
                semantic_field="source_time_utc",
                payload_field="source_time_utc",
                value_type="datetime",
                unit=None,
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
            m01.SourceSemanticBinding(
                semantic_field="runtime_bar_time_utc",
                payload_field="runtime_bar_time_utc",
                value_type="datetime",
                unit=None,
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
            m01.SourceSemanticBinding(
                semantic_field="spot_price",
                payload_field="spot_price",
                value_type="float",
                unit="USD",
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
            m01.SourceSemanticBinding(
                semantic_field="front_dte",
                payload_field="front_dte",
                value_type="int",
                unit="days",
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
            m01.SourceSemanticBinding(
                semantic_field="next_dte",
                payload_field="next_dte",
                value_type="int",
                unit="days",
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
            m01.SourceSemanticBinding(
                semantic_field="next_event_time_utc",
                payload_field="next_event_time_utc",
                value_type="datetime",
                unit=None,
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
            m01.SourceSemanticBinding(
                semantic_field="nvda_return_pct",
                payload_field="nvda_return_pct",
                value_type="float",
                unit="percent",
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
            m01.SourceSemanticBinding(
                semantic_field="nq_return_pct",
                payload_field="nq_return_pct",
                value_type="float",
                unit="percent",
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
            m01.SourceSemanticBinding(
                semantic_field="vix_level",
                payload_field="vix_level",
                value_type="float",
                unit="index_points",
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
        ),
    )
    source_service = m01.SourceAdmissionService(
        registry=m01.SourceFamilyRegistry.build([contract]),
        capture_id_factory=lambda _: "capture.market.20260731T100000Z",
        source_artifact_id_factory=lambda *_: "calendar.reference.a",
    )
    source_request = m01.SourceAdmissionRequest(
        family_id="market_runtime",
        contract_id="source.market.v1",
        schema_version="1.0.0",
        provider_id="recorded-provider",
        acquisition_channel="recorded_api_response",
        source_object_id="provider-observation-tier-c-1",
        observed_at_utc=observed_at,
        captured_at_utc=observed_at + timedelta(seconds=1),
        captured_material=payload.model_dump_json().encode(),
        typed_payload=payload,
    )
    calendar_request = CalendarProjectionRequest(
        snapshot=m02.FinancialCalendarSnapshot.model_validate(
            production_snapshot_payload(valid_snapshot())
        ),
        policy=m02.CalendarFieldResolutionPolicy.model_validate(
            production_policy_payload(field_policy())
        ),
        projection_id="projection:tier-c-operational:001",
    )
    preparation = PreparationSpec(
        field_resolution_policies=(
            m03.FieldResolutionPolicy(
                policy_id="m03.policy.source_time_utc",
                policy_version="1.0.0",
                output_contract_version="1.0.0",
                semantic_field="source_time_utc",
                mandatory=True,
                admitted_source_roles=("recorded-provider",),
                value_type="datetime",
                unit=None,
                temporal_comparison_rule="exact_effective_interval",
                comparison_rule="exact",
                authoritative_owner="recorded-provider",
                allow_degraded_candidates=False,
                unresolved_consequence="withhold",
                optional_absence_consequence="unavailable",
            ),
            m03.FieldResolutionPolicy(
                policy_id="m03.policy.runtime_bar_time_utc",
                policy_version="1.0.0",
                output_contract_version="1.0.0",
                semantic_field="runtime_bar_time_utc",
                mandatory=True,
                admitted_source_roles=("recorded-provider",),
                value_type="datetime",
                unit=None,
                temporal_comparison_rule="exact_effective_interval",
                comparison_rule="exact",
                authoritative_owner="recorded-provider",
                allow_degraded_candidates=False,
                unresolved_consequence="withhold",
                optional_absence_consequence="unavailable",
            ),
            m03.FieldResolutionPolicy(
                policy_id="m03.policy.spot_price",
                policy_version="1.0.0",
                output_contract_version="1.0.0",
                semantic_field="spot_price",
                mandatory=True,
                admitted_source_roles=("recorded-provider",),
                value_type="float",
                unit="USD",
                temporal_comparison_rule="exact_effective_interval",
                comparison_rule="exact",
                authoritative_owner="recorded-provider",
                allow_degraded_candidates=False,
                unresolved_consequence="withhold",
                optional_absence_consequence="unavailable",
            ),
            m03.FieldResolutionPolicy(
                policy_id="m03.policy.front_dte",
                policy_version="1.0.0",
                output_contract_version="1.0.0",
                semantic_field="front_dte",
                mandatory=True,
                admitted_source_roles=("recorded-provider",),
                value_type="int",
                unit="days",
                temporal_comparison_rule="exact_effective_interval",
                comparison_rule="exact",
                authoritative_owner="recorded-provider",
                allow_degraded_candidates=False,
                unresolved_consequence="withhold",
                optional_absence_consequence="unavailable",
            ),
            m03.FieldResolutionPolicy(
                policy_id="m03.policy.next_dte",
                policy_version="1.0.0",
                output_contract_version="1.0.0",
                semantic_field="next_dte",
                mandatory=True,
                admitted_source_roles=("recorded-provider",),
                value_type="int",
                unit="days",
                temporal_comparison_rule="exact_effective_interval",
                comparison_rule="exact",
                authoritative_owner="recorded-provider",
                allow_degraded_candidates=False,
                unresolved_consequence="withhold",
                optional_absence_consequence="unavailable",
            ),
            m03.FieldResolutionPolicy(
                policy_id="m03.policy.next_event_time_utc",
                policy_version="1.0.0",
                output_contract_version="1.0.0",
                semantic_field="next_event_time_utc",
                mandatory=True,
                admitted_source_roles=("recorded-provider",),
                value_type="datetime",
                unit=None,
                temporal_comparison_rule="exact_effective_interval",
                comparison_rule="exact",
                authoritative_owner="recorded-provider",
                allow_degraded_candidates=False,
                unresolved_consequence="withhold",
                optional_absence_consequence="unavailable",
            ),
            m03.FieldResolutionPolicy(
                policy_id="m03.policy.nvda_return_pct",
                policy_version="1.0.0",
                output_contract_version="1.0.0",
                semantic_field="nvda_return_pct",
                mandatory=True,
                admitted_source_roles=("recorded-provider",),
                value_type="float",
                unit="percent",
                temporal_comparison_rule="exact_effective_interval",
                comparison_rule="exact",
                authoritative_owner="recorded-provider",
                allow_degraded_candidates=False,
                unresolved_consequence="withhold",
                optional_absence_consequence="unavailable",
            ),
            m03.FieldResolutionPolicy(
                policy_id="m03.policy.nq_return_pct",
                policy_version="1.0.0",
                output_contract_version="1.0.0",
                semantic_field="nq_return_pct",
                mandatory=True,
                admitted_source_roles=("recorded-provider",),
                value_type="float",
                unit="percent",
                temporal_comparison_rule="exact_effective_interval",
                comparison_rule="exact",
                authoritative_owner="recorded-provider",
                allow_degraded_candidates=False,
                unresolved_consequence="withhold",
                optional_absence_consequence="unavailable",
            ),
            m03.FieldResolutionPolicy(
                policy_id="m03.policy.vix_level",
                policy_version="1.0.0",
                output_contract_version="1.0.0",
                semantic_field="vix_level",
                mandatory=True,
                admitted_source_roles=("recorded-provider",),
                value_type="float",
                unit="index_points",
                temporal_comparison_rule="exact_effective_interval",
                comparison_rule="exact",
                authoritative_owner="recorded-provider",
                allow_degraded_candidates=False,
                unresolved_consequence="withhold",
                optional_absence_consequence="unavailable",
            ),
        ),
        derivation_rules=(
            m03.PreparedDerivationRule(
                semantic_field="minutes_to_next_event",
                derivation_version="1.0.0",
                input_semantic_fields=(
                    "runtime_bar_time_utc",
                    "next_event_time_utc",
                ),
                operation="minutes_between",
                unit_alignment_policy="utc_minutes",
                temporal_alignment_policy="ordered_instants",
                mandatory=True,
            ),
            m03.PreparedDerivationRule(
                semantic_field="front_to_next_dte_spread",
                derivation_version="1.0.0",
                input_semantic_fields=("next_dte", "front_dte"),
                operation="difference",
                unit_alignment_policy="same_unit_days",
                temporal_alignment_policy="same_observation",
                mandatory=True,
            ),
        ),
        schema_version="1.0.0",
        preparation_policy_version="m03.preparation.v1",
        alignment_policy_version="m03.alignment.v1",
        fingerprint_policy_version="m03.fingerprint.v1",
        canonicalisation_version="m03.canonical.v1",
        effective_at_utc=observed_at,
        payload_schema_version="1.0.0",
    )

    command = UpstreamPreparationCommand(
        command_id="tier-c-upstream-command-001",
        source_requests=(source_request,),
        calendar_requests=(calendar_request,),
        preparation=preparation,
    )
    return {
        "source_service": source_service,
        "calendar_resolver": m02.CalendarResolver(),
        "prepared_data_builder": m03.PreparedDataBuilder(),
        "command": command,
        "source_payload": payload,
    }


def _run_isolated(
    code: str, *, cwd: Path, args: tuple[str, ...] = ()
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", "-c", code, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def test_installed_package_is_importable_outside_repository(tmp_path: Path) -> None:
    completed = _run_isolated(
        "from pathlib import Path; import sysconfig; import nvda_desk; "
        "module=Path(nvda_desk.__file__).resolve(); "
        "purelib=Path(sysconfig.get_paths()['purelib']).resolve(); "
        "assert module.is_relative_to(purelib), (module, purelib); print(module)",
        cwd=tmp_path,
    )

    assert completed.returncode == 0, completed.stderr
    assert "site-packages" in completed.stdout


def test_sqlite_state_survives_a_separate_python_process(tmp_path: Path) -> None:
    database = tmp_path / "tier-c-state.sqlite3"
    writer = _run_isolated(
        """
from nvda_desk.m13_state_kernel import IdempotencyKey, SqliteUnitOfWork, TransactionCommand
import sys
boundary = SqliteUnitOfWork(database_path=sys.argv[1], initial_state={"count": 0})
command = TransactionCommand(
    command_id="tier-c-command:1",
    idempotency_key=IdempotencyKey(
        value="tier-c-idempotency:1",
        command_type="tier_c_restart",
        consistency_unit_id="tier-c-unit:1",
    ),
    input_fingerprint="a" * 64,
    expected_state_version=0,
    policy_version="tier-c.restart.v1",
)
def mutate(state):
    state["count"] += 1
    return {"receipt_id": "tier-c-receipt:1", "result_id": "tier-c-result:1"}
receipt = boundary.execute(command=command, mutation=mutate)
print(receipt.receipt_id)
""",
        cwd=tmp_path,
        args=(str(database),),
    )
    assert writer.returncode == 0, writer.stderr

    reader = _run_isolated(
        """
from nvda_desk.m13_state_kernel import SqliteUnitOfWork
import json, sys
boundary = SqliteUnitOfWork(database_path=sys.argv[1], initial_state={"count": 999})
print(json.dumps({"version": boundary.state_version, "state": boundary.snapshot_state(), "receipts": len(boundary.list_receipts())}, sort_keys=True))
""",
        cwd=tmp_path,
        args=(str(database),),
    )
    assert reader.returncode == 0, reader.stderr
    assert json.loads(reader.stdout) == {
        "receipts": 1,
        "state": {"count": 1},
        "version": 1,
    }


def test_raw_source_preparation_feeds_the_exact_paper_run() -> None:
    upstream = _operational_upstream_fixture()
    prepared_receipt = upstream_coordinator(upstream).prepare(upstream["command"])
    assert prepared_receipt.status == "prepared"
    assert prepared_receipt.prepared_data is not None
    prepared = prepared_receipt.prepared_data
    source_payload = upstream["source_payload"]
    assert prepared.payload.source_time_utc == source_payload.source_time_utc
    assert prepared.payload.runtime_bar_time_utc == source_payload.runtime_bar_time_utc
    assert prepared.payload.spot_price == source_payload.spot_price
    assert prepared.payload.front_dte == source_payload.front_dte
    assert prepared.payload.next_dte == source_payload.next_dte
    assert prepared.payload.next_event_time_utc == source_payload.next_event_time_utc
    assert prepared.payload.nvda_return_pct == source_payload.nvda_return_pct
    assert prepared.payload.nq_return_pct == source_payload.nq_return_pct
    assert prepared.payload.vix_level == source_payload.vix_level
    assert prepared.payload.minutes_to_next_event == 2880
    assert prepared.payload.front_to_next_dte_spread == 7
    assert {item.semantic_field for item in prepared.field_resolution_receipts} == {
        "source_time_utc",
        "runtime_bar_time_utc",
        "spot_price",
        "front_dte",
        "next_dte",
        "next_event_time_utc",
        "nvda_return_pct",
        "nq_return_pct",
        "vix_level",
    }
    assert {item.semantic_field for item in prepared.derivation_receipts} == {
        "minutes_to_next_event",
        "front_to_next_dte_spread",
    }

    api = production_api()
    runtime = production_runtime_fixture(
        api,
        suffix="tier-c-e2e",
        prepared_data=prepared_receipt.prepared_data,
    )
    receipt = runtime["coordinator"].run(runtime["command"])
    serial_outcome = receipt.serial_cognition_outcome
    stage_facts = {
        stage_input.stage: {fact.fact_id: fact.value for fact in stage_input.carrier_facts}
        for stage_input in serial_outcome.stage_inputs
    }
    assert stage_facts["temporal"]["source_time_utc"] == source_payload.source_time_utc
    assert stage_facts["temporal"]["runtime_bar_time_utc"] == source_payload.runtime_bar_time_utc
    assert stage_facts["temporal"]["next_event_time_utc"] == source_payload.next_event_time_utc
    assert stage_facts["regime"]["nvda_return_pct"] == source_payload.nvda_return_pct
    assert stage_facts["regime"]["nq_return_pct"] == source_payload.nq_return_pct
    assert stage_facts["regime"]["vix_level"] == source_payload.vix_level
    assert stage_facts["options_flow"]["spot_price"] == source_payload.spot_price
    assert stage_facts["options_flow"]["front_dte"] == source_payload.front_dte
    assert stage_facts["options_flow"]["next_dte"] == source_payload.next_dte
    assert serial_outcome.modifier_receipt is not None
    assert serial_outcome.eligibility_decision is not None
    m08_facts = {
        item.fact_ref: item.value
        for item in serial_outcome.eligibility_decision.material_fact_lineage
    }
    assert m08_facts["spot_price"] == source_payload.spot_price
    assert m08_facts["gamma_state"] == "active"

    assert (
        runtime["command"].prepared_data.prepared_id == prepared_receipt.prepared_data.prepared_id
    )
    assert (
        receipt.prepared_context_packet.data.prepared_id
        == prepared_receipt.prepared_data.prepared_id
    )
    assert receipt.serial_candidate == serial_outcome.candidate
    assert receipt.outcome == "paper_filled"
    assert receipt.live_execution_proven is False


class _Resolver:
    def __init__(self, value: str | None) -> None:
        self.value = value
        self.calls: list[str] = []

    def resolve(self, reference: str) -> str | None:
        self.calls.append(reference)
        return self.value


class _MarketTransport:
    transport_kind = "hermetic"

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def fetch_snapshot(self, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(kwargs)
        return {
            "provider_request_id": "tier-c-provider-request:1",
            "observed_at_utc": datetime(2026, 8, 2, 0, 0, tzinfo=UTC),
            "raw_material": b'{"symbol":"NVDA","price":"123.45"}',
            "network_fetch_proven": False,
        }


class _BrokerTransport:
    transport_kind = "network"

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def submit_order(self, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(kwargs)
        raise AssertionError("broker transport must not be called without credentials")


def test_validation_provider_substitution_is_hermetic() -> None:
    from nvda_desk.operational_boundaries import (
        LiveMarketDataAdapter,
        MarketDataOperationalConfig,
        OperationalMode,
        ProviderSnapshotRequest,
    )

    resolver = _Resolver("validation-secret")
    transport = _MarketTransport()
    adapter = LiveMarketDataAdapter(
        config=MarketDataOperationalConfig(
            mode=OperationalMode.VALIDATION,
            provider_id="provider.alpha",
            environment="sandbox",
            endpoint="https://sandbox.provider.invalid/snapshot",
            credential_reference="NVDA_PROVIDER_TOKEN",
            kill_switch_engaged=False,
            live_authorisation_id="approval:tier-c-provider:1",
        ),
        credential_resolver=resolver,
        transport=transport,
    )
    receipt = adapter.fetch(
        ProviderSnapshotRequest.create(
            provider_id="provider.alpha",
            symbol="NVDA",
            requested_at_utc=datetime(2026, 8, 2, 0, 0, tzinfo=UTC),
        )
    )

    assert receipt.operational_mode == "validation"
    assert receipt.network_fetch_proven is False
    assert len(transport.calls) == 1
    assert "validation-secret" not in repr(receipt)


def test_live_broker_missing_credential_stops_before_transport() -> None:
    from nvda_desk.operational_boundaries import (
        BrokerOperationalConfig,
        LiveBrokerAdapter,
        OperationalBlocker,
        OperationalMode,
    )

    intent = _live_intent()
    transport = _BrokerTransport()
    adapter = LiveBrokerAdapter(
        config=BrokerOperationalConfig(
            mode=OperationalMode.LIVE,
            broker_id=intent.broker_id,
            environment="live",
            endpoint="https://broker.invalid/orders",
            account_id=intent.account_id,
            expected_account_id=intent.account_id,
            credential_reference="NVDA_BROKER_TOKEN",
            kill_switch_engaged=False,
            live_authorisation_id=intent.live_authorisation_id,
        ),
        credential_resolver=_Resolver(None),
        transport=transport,
    )

    with pytest.raises(OperationalBlocker, match="broker_credential_unavailable"):
        adapter.submit(intent, submitted_at_utc=datetime(2026, 8, 2, 0, 1, tzinfo=UTC))
    assert transport.calls == []
