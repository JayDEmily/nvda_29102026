"""F4 RC12: public coherent three-field book slope and D011 midpoint lineage."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 15, tzinfo=UTC)
ROWS = (
    ("b1", Decimal(99), Decimal(10), "bid"),
    ("b2", Decimal(98), Decimal(5), "bid"),
    ("b3", Decimal(97), Decimal(20), "bid"),
    ("a1", Decimal(101), Decimal(8), "ask"),
    ("a2", Decimal(102), Decimal(12), "ask"),
    ("a3", Decimal(103), Decimal(12), "ask"),
)
FIELDS = ("R034", "R035", "R189", "R190", "R188")
NAMES = ("bid_price", "ask_price", "price", "size", "side")
UNITS = ("price", "price", "price", "contracts", "side")


def _owner(
    *, missing_side_at: str | None = None, unknown_side_at: str | None = None
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    quote_ts = NOW - timedelta(seconds=3)
    m00.commands.admit_raw_observation_occurrence(
        raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id("slope-quote"),
            delivery_artifact_ref=raw.delivery_artifact_ref("f4-slope-quote"),
            source_provider=raw.provider_id("slope-quotes"),
            native_record={"bid_price": Decimal(99), "ask_price": Decimal(101)},
            received_ts_utc=quote_ts,
            ingestion_sequence=1,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("slope-quotes:q"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=quote_ts.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=(
                raw.RawSignalCatalogueId("R034"),
                raw.RawSignalCatalogueId("R035"),
            ),
            source_variant="quote",
            subject_instrument="NVDA",
            native_units="quote",
            revision_vintage_native="v1",
        )
    )
    for seq, (tag, price, size, side) in enumerate(ROWS, 1):
        moment = NOW - timedelta(seconds=2)
        native = {"price": price, "size": size, "side": side}
        if tag == missing_side_at:
            del native["side"]
        if tag == unknown_side_at:
            native["side"] = "unknown"
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("slope-" + tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("f4-slope-" + tag),
                source_provider=raw.provider_id("slope-book"),
                native_record=native,
                received_ts_utc=moment,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("slope-book:depth"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=moment.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(x) for x in FIELDS[2:]),
                source_variant="depth_snapshot",
                subject_instrument="NVDA",
                native_units="displayed_depth",
                revision_vintage_native="v1",
            )
        )
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "slope-map-" + rid,
            1,
            raw.RawSignalCatalogueId(rid),
            "slope-quotes" if index < 2 else "slope-book",
            "quote" if index < 2 else "depth_snapshot",
            (key,),
            unit,
        )
        for index, (rid, key, unit) in enumerate(zip(FIELDS, NAMES, UNITS, strict=True))
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "slope-regression", 1, "P_REGRESSION", (("minimum_sample", 2),)
            ),
            api.CalculationParameterSetV1(
                "slope-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "slope-policy",
                1,
                ("subject_instrument",),
                timedelta(seconds=30),
                timedelta(seconds=30),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=tuple(
            api.UnitConventionVersionV1("slope-unit-" + rid, 1, unit, unit, Decimal(1), Decimal(0))
            for rid, unit in zip(FIELDS, UNITS, strict=True)
        ),
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=1),
    )
    request = api.CalculationRequestV1(
        "D138",
        "NVDA",
        NOW,
        NOW,
        "f4-slope",
        "slope-regression",
        1,
        "slope-policy",
        1,
        (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_REGRESSION", "slope-regression", 1),
            api.ParameterProfileRefV1("P_BASIC", "slope-basic", 1),
        ),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("slope-map-" + rid, 1),
                api.VersionRefV1("slope-unit-" + rid, 1),
                "NVDA",
                None,
            )
            for rid in FIELDS
        ),
    )
    return owner, request


def test_d138_public_per_side_ols_and_midpoint_lineage() -> None:
    owner, request = _owner()
    result = owner.materialise(request)
    assert result is not None
    assert dict(result.result) == {"bid_slope": Decimal("12.5"), "ask_slope": Decimal(12)}
    assert {x.raw_signal_id for x in result.raw_input_lineage} == set(FIELDS)
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {
        "slope-quote",
        *("slope-" + x[0] for x in ROWS),
    }
    assert result.predecessor_occurrence_ids
    assert owner.materialise(request) == result


def test_d138_refuses_incomplete_or_contradictory_row_instead_of_fitting_shortened_book() -> None:
    absent_owner, absent_request = _owner(missing_side_at="b3")
    assert absent_owner.materialise(absent_request) is None
    invalid_owner, invalid_request = _owner(unknown_side_at="b3")
    assert invalid_owner.materialise(invalid_request) is None
