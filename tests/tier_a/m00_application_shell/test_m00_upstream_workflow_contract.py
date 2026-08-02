"""Canonical M01 -> M02 -> M03 application workflow proof."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from tests.support.m00_application_shell_contract_harness import (
    production_api,
    production_runtime_fixture,
)
from tests.support.m02_k04_contract_harness import (
    field_policy,
    production_policy_payload,
    production_snapshot_payload,
    valid_snapshot,
)


class MarketSnapshotPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    value: float


def _upstream_fixture() -> dict[str, Any]:
    from nvda_desk import m01_source_admission as m01
    from nvda_desk import m02_financial_calendar as m02
    from nvda_desk import m03_preparation as m03
    from nvda_desk.m00_application_shell import (
        CalendarProjectionRequest,
        PreparationSpec,
        UpstreamPreparationCommand,
    )

    source_identifier = m01.SourceIdentifierContract(
        requirement=m01.SourceFactRequirement.REQUIRED,
        owner="recorded-provider",
        namespace="recorded-provider/market-observation",
        uniqueness_scope="recorded-provider/market-observation",
        stability_rule="stable_for_source_object_lifetime",
        generation_rule="issued_by_upstream_provider",
    )
    contract = m01.SourceFamilyContract(
        family_id="market_snapshot",
        contract_id="market_snapshot.v1",
        schema_version="1.0.0",
        payload_model=MarketSnapshotPayload,
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
        signal_family_id="market_snapshot",
        semantic_bindings=(
            m01.SourceSemanticBinding(
                semantic_field="spot_price",
                payload_field="value",
                value_type="float",
                unit="USD",
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
        ),
    )
    source_service = m01.SourceAdmissionService(
        registry=m01.SourceFamilyRegistry.build([contract]),
        capture_id_factory=lambda _: "capture::m01::upstream-001",
        source_artifact_id_factory=lambda *_: "calendar.reference.a",
    )
    source_request = m01.SourceAdmissionRequest(
        family_id="market_snapshot",
        contract_id="market_snapshot.v1",
        schema_version="1.0.0",
        provider_id="recorded-provider",
        acquisition_channel="recorded_api_response",
        source_object_id="provider-observation-17",
        observed_at_utc=datetime(2026, 7, 31, 1, 15, tzinfo=UTC),
        captured_at_utc=datetime(2026, 7, 31, 1, 16, tzinfo=UTC),
        captured_material=b'{"symbol":"NVDA","value":121.5}',
        typed_payload=MarketSnapshotPayload(symbol="NVDA", value=121.5),
    )
    calendar_request = CalendarProjectionRequest(
        snapshot=m02.FinancialCalendarSnapshot.model_validate(
            production_snapshot_payload(valid_snapshot())
        ),
        policy=m02.CalendarFieldResolutionPolicy.model_validate(
            production_policy_payload(field_policy())
        ),
        projection_id="projection:m00-upstream:001",
    )
    preparation = PreparationSpec(
        field_resolution_policies=(
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
        ),
        schema_version="1.0.0",
        preparation_policy_version="m03.preparation.v1",
        alignment_policy_version="m03.alignment.v1",
        fingerprint_policy_version="m03.fingerprint.v1",
        canonicalisation_version="m03.canonical.v1",
        effective_at_utc=datetime(2026, 7, 31, 1, 20, tzinfo=UTC),
        payload_schema_version="1.0.0",
    )
    command = UpstreamPreparationCommand(
        command_id="upstream-command-001",
        source_requests=(source_request,),
        calendar_requests=(calendar_request,),
        preparation=preparation,
    )
    return {
        "source_service": source_service,
        "calendar_resolver": m02.CalendarResolver(),
        "prepared_data_builder": m03.PreparedDataBuilder(),
        "command": command,
    }


def _coordinator(fixture: dict[str, Any]):
    api = production_api()
    case = production_runtime_fixture(
        api,
        upstream_dependencies={
            "source_admission": fixture["source_service"],
            "calendar_resolver": fixture["calendar_resolver"],
            "prepared_data_builder": fixture["prepared_data_builder"],
        },
    )
    return case["coordinator"]


def test_m00_exports_upstream_contracts() -> None:
    from nvda_desk import m00_application_shell as m00

    assert {
        "CalendarProjectionRequest",
        "PreparationSpec",
        "UpstreamPreparationCommand",
        "UpstreamPreparationReceipt",
    } <= set(m00.__all__)


def test_source_admission_issues_distinct_source_artifact_identity() -> None:
    fixture = _upstream_fixture()
    result = fixture["source_service"].admit(fixture["command"].source_requests[0])

    assert result.status == "accepted"
    envelope = result.source_artifact
    assert envelope.source_artifact_id == "calendar.reference.a"
    assert envelope.source_artifact_id not in {
        envelope.source_object_id,
        envelope.capture_receipt.capture_id,
        envelope.content_sha256,
    }


def test_upstream_command_preserves_exact_owner_outputs_and_m02_lineage() -> None:
    fixture = _upstream_fixture()
    receipt = _coordinator(fixture).prepare(fixture["command"])

    assert receipt.status == "prepared"
    assert receipt.command_id == "upstream-command-001"
    assert receipt.source_results[0].status == "accepted"
    assert receipt.calendar_projections[0].projection_id == "projection:m00-upstream:001"
    assert receipt.prepared_data is not None
    assert receipt.prepared_data.source_capture_refs[0].source_artifact_id == "calendar.reference.a"
    assert receipt.prepared_data.calendar_projection_refs[0].projection_id == (
        "projection:m00-upstream:001"
    )
    assert receipt.prepared_data.calendar_projection_refs[0].semantic_fingerprint == (
        receipt.calendar_projections[0].semantic_fingerprint
    )
    assert receipt.prepared_data.payload.spot_price == 121.5
    spot_receipt = next(
        item
        for item in receipt.prepared_data.field_resolution_receipts
        if item.semantic_field == "spot_price"
    )
    assert spot_receipt.selected_value == 121.5
    assert spot_receipt.selected_source_artifact_id == "calendar.reference.a"


def test_source_non_admission_is_terminal_before_calendar_and_preparation() -> None:
    fixture = _upstream_fixture()
    command = fixture["command"].model_copy(
        update={
            "source_requests": (
                fixture["command"]
                .source_requests[0]
                .model_copy(update={"provider_id": "unregistered-provider"}),
            )
        }
    )
    receipt = _coordinator(fixture).prepare(command)

    assert receipt.status == "source_not_admitted"
    assert receipt.failure_stage == "M01"
    assert receipt.source_results[0].reason == "unsupported_source_provider"
    assert receipt.calendar_projections == ()
    assert receipt.prepared_data is None


def test_withheld_calendar_is_terminal_before_preparation() -> None:
    fixture = _upstream_fixture()
    unavailable_policy = (
        fixture["command"]
        .calendar_requests[0]
        .policy.model_copy(update={"semantic_key": "mandatory_missing_fact"})
    )
    command = fixture["command"].model_copy(
        update={
            "calendar_requests": (
                fixture["command"]
                .calendar_requests[0]
                .model_copy(update={"policy": unavailable_policy}),
            )
        }
    )
    receipt = _coordinator(fixture).prepare(command)

    assert receipt.status == "calendar_withheld"
    assert receipt.failure_stage == "M02"
    assert receipt.calendar_projections[0].status == "withheld"
    assert receipt.prepared_data is None


def test_cli_upstream_route_translates_only_into_m00_contract() -> None:
    from nvda_desk.entry.cli import prepare_command

    fixture = _upstream_fixture()
    result = prepare_command(
        fixture["command"].model_dump(mode="json"),
        coordinator=_coordinator(fixture),
    )

    assert result["status"] == "prepared"
    assert result["prepared_data"]["prepared_id"].startswith("prepared:")


def test_unit3_m00_transport_translation_delegates_typed_payload_to_m01() -> None:
    fixture = _upstream_fixture()
    coordinator = _coordinator(fixture)

    command = coordinator.translate_upstream_command(fixture["command"].model_dump(mode="json"))

    assert isinstance(command.source_requests[0].typed_payload, MarketSnapshotPayload)
    assert command == fixture["command"]


def test_asgi_exposes_canonical_upstream_route() -> None:
    from nvda_desk.entry.asgi import _ApplicationAsgiApp

    source = _ApplicationAsgiApp.__call__.__code__.co_consts
    assert "/commands/prepare" in source or any(
        isinstance(item, tuple) and "/commands/prepare" in item for item in source
    )


def test_semantic_continuity_m00_preparation_spec_cannot_carry_prepared_values() -> None:
    from nvda_desk.m00_application_shell import PreparationSpec

    fields = set(PreparationSpec.model_fields)

    assert "payload" not in fields
    assert "input_schema_versions" not in fields
    assert "field_resolution_policies" in fields
    assert "derivation_rules" in fields
