"""F4 RC02 D018: independent provider VWAP vs M00-sourced per-trade D017.

D017 is evaluated recursively by the actual M01 public owner, never inserted
into the fixture as a synthetic pre-calculated kernel result.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 14, tzinfo=UTC)


def public_vwap_gap(
    *, missing_r137: bool = False, missing_size_second: bool = False,
    future_r137: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for seq, (oid, price, size, sec) in enumerate(
        (("trade-a", Decimal(6), Decimal(2), 5), ("trade-b", Decimal(4), Decimal(3), 2)), 1
    ):
        stamp = NOW - timedelta(seconds=sec)
        field_ids = ("R120",) if missing_size_second and seq == 2 else ("R120", "R121")
        fields = {"price": price, **({"size": size} if "R121" in field_ids else {})}
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("rc02-" + oid),
                source_provider=raw.provider_id("controlled-rc02-vwap"),
                native_record={"trade": fields},
                received_ts_utc=stamp,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc02-vwap:trade"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in field_ids),
                source_variant="trade",
                subject_instrument="NVDA",
                native_units="trade",
                revision_vintage_native="v1",
            )
        )
    if not missing_r137:
        stamp = NOW + timedelta(seconds=1) if future_r137 else NOW - timedelta(seconds=1)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("vwap-provider"),
                delivery_artifact_ref=raw.delivery_artifact_ref("rc02-vwap-provider"),
                source_provider=raw.provider_id("controlled-rc02-vwap"),
                native_record={"quote": {"vwap": Decimal(5)}},
                received_ts_utc=stamp,
                ingestion_sequence=3,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc02-vwap:quote"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId("R137"),),
                source_variant="quote",
                subject_instrument="NVDA",
                native_units="price",
                revision_vintage_native="v1",
            )
        )
    specs = (
        ("R120", "trade", "price", "price"),
        ("R121", "trade", "size", "shares"),
        ("R137", "quote", "vwap", "price"),
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "vwap-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc02-vwap", variant, (variant, field), units,
            )
            for rid, variant, field, units in specs
        ),
        parameter_sets=(api.CalculationParameterSetV1(
            "vwap-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),)
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "vwap-select", 1, ("subject_instrument",),
            timedelta(seconds=10), timedelta(seconds=10), ("true_instant",), (),
        ),),
        unit_conventions=tuple(
            api.UnitConventionVersionV1(
                "vwap-unit-" + rid, 1, units, units, Decimal(1), Decimal(0)
            ) for rid, _, _, units in specs
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D018", "NVDA", NOW, NOW, "vwap-gap", "vwap-basic", 1,
        "vwap-select", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("vwap-map-" + rid, 1),
                api.VersionRefV1("vwap-unit-" + rid, 1), "NVDA", None,
            ) for rid, _, _, _ in specs
        ),
    )
    return owner, request


def test_d018_public_gap_exact_arithmetic_predecessor_raw_lineage_and_retry() -> None:
    owner, request = public_vwap_gap()
    result = owner.materialise(request)
    assert result is not None
    assert dict(result.result) == {
        "price_difference": Decimal("0.2"),
        "bps_difference": Decimal(10000) * Decimal("0.2") / Decimal("4.8"),
    }
    assert {x.raw_signal_id for x in result.raw_input_lineage} == {"R120", "R121", "R137"}
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {
        "trade-a", "trade-b", "vwap-provider"
    }
    assert len(result.predecessor_occurrence_ids) == 1
    prior = owner.reads.get_derived_occurrence(result.predecessor_occurrence_ids[0])
    assert prior is not None and prior.derived_signal_id == "D017"
    assert prior.result == Decimal("4.8")
    assert owner.materialise(request) == result


def test_d018_public_refuses_missing_provider_or_unmatched_trade_size() -> None:
    owner, request = public_vwap_gap(missing_r137=True)
    assert owner.materialise(request) is None
    owner, request = public_vwap_gap(missing_size_second=True)
    assert owner.materialise(request) is None


def test_d018_public_refuses_future_provider_quote() -> None:
    owner, request = public_vwap_gap(future_r137=True)
    assert owner.materialise(request) is None
