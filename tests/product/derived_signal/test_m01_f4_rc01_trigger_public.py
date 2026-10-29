"""F4 RC01 D209: public M00 next-receipt trigger fact, without external action."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, 0, tzinfo=UTC)
RECEIPT = NOW - timedelta(seconds=3)


def public_trigger(
    *,
    receipt: datetime = RECEIPT,
    subject: str = "NVDA",
    with_raw: bool = True,
    with_schedule: bool = True,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    if with_raw:
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("next-receipt"),
                delivery_artifact_ref=raw.delivery_artifact_ref("next-receipt-artifact"),
                source_provider=raw.provider_id("controlled-rc01-trigger"),
                native_record={"receipt": {"source": "market_quote"}},
                received_ts_utc=receipt,
                ingestion_sequence=1,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc01-trigger"),
                source_temporal_kind="receipt_only",
                source_timestamp_raw=None,
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId("R001"),),
                source_variant="collector",
                subject_instrument=subject,
                native_units="native_source",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=(
            raw.RawSignalProjectionMappingV1(
                "receipt-map",
                1,
                raw.RawSignalCatalogueId("R001"),
                "controlled-rc01-trigger",
                "collector",
                ("receipt", "source"),
                "native_source",
            ),
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "trigger-policy",
                1,
                "P_RULE",
                (("trigger_mode", "m00_or_schedule"),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "trigger-select",
                1,
                ("subject_instrument",),
                timedelta(seconds=30),
                timedelta(seconds=30),
                ("receipt_only",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "native-source",
                1,
                "native_source",
                "native_source",
                Decimal(1),
                Decimal(0),
            ),
        ),
        contexts=(
            api.RecalculationScheduleV1(
                "versioned-trigger",
                1,
                ("on_market_data_receipt",),
            ),
        ),
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D209",
        "NVDA",
        NOW,
        NOW,
        "trigger-definition",
        "trigger-policy",
        1,
        "trigger-select",
        1,
        (api.VersionRefV1("versioned-trigger", 1),) if with_schedule else (),
        raw_input_bindings=(
            api.RawInputBindingV1(
                "R001",
                api.VersionRefV1("receipt-map", 1),
                api.VersionRefV1("native-source", 1),
                "NVDA",
                None,
            ),
        ),
    )
    return owner, request


def test_d209_public_receipt_trigger_exact_time_lineage_and_idempotency() -> None:
    owner, req = public_trigger()
    out = owner.materialise(req)
    assert out is not None
    assert out.result == (("trigger", "m00_receipt"), ("at", RECEIPT))
    assert {lineage.raw_signal_id for lineage in out.raw_input_lineage} == {"R001"}
    assert {lineage.observation_occurrence_id for lineage in out.raw_input_lineage} == {
        "next-receipt"
    }
    assert out.predecessor_occurrence_ids == ()
    assert owner.materialise(req) == out


def test_d209_public_refuses_future_unknown_source_and_missing_schedule() -> None:
    owner, req = public_trigger(receipt=NOW + timedelta(seconds=1))
    assert owner.materialise(req) is None
    owner, req = public_trigger(subject="AMD")
    assert owner.materialise(req) is None
    owner, req = public_trigger(with_raw=False)
    assert owner.materialise(req) is None
    owner, req = public_trigger(with_schedule=False)
    assert owner.materialise(req) is None
    assert owner.materialise(replace(req, context_refs=())) is None
