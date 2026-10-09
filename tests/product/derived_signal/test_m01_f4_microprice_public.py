"""F4 RC12 public M00 quote-size co-reference for canonical D137 microprice."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 14, tzinfo=UTC)
FIELDS = ("R034", "R035", "R033", "R036")
FIELD_PATHS = ("bid_price", "ask_price", "bid_size", "ask_size")
NATIVE_UNITS = ("price", "price", "contracts", "contracts")


def owner_with_quotes(
    *, no_ask_size: bool = False, later_ask: bool = False
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    bid_quote = {"bid_price": Decimal(100), "bid_size": Decimal(8)}
    ask_quote = {"ask_price": Decimal(102), "ask_size": Decimal(2)}
    if no_ask_size:
        ask_quote.pop("ask_size")
    for seq, (tag, obs, field_ids) in enumerate(
        (
            ("quote-bid", bid_quote, ("R034", "R033")),
            ("quote-ask", ask_quote, ("R035", "R036")),
        ),
        1,
    ):
        moment = (
            NOW + timedelta(seconds=1) if later_ask and seq == 2 else NOW - timedelta(seconds=seq)
        )
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("f4-" + tag),
                source_provider=raw.provider_id("controlled-microprice"),
                native_record={"quote": obs},
                received_ts_utc=moment,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope(
                    "controlled-microprice:quote"
                ),
                source_temporal_kind="true_instant",
                source_timestamp_raw=moment.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in field_ids),
                source_variant="quote",
                subject_instrument="NVDA",
                native_units="quote",
                revision_vintage_native="v1",
            )
        )
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "mp-map-" + rid,
            1,
            raw.RawSignalCatalogueId(rid),
            "controlled-microprice",
            "quote",
            ("quote", path),
            unit,
        )
        for rid, path, unit in zip(FIELDS, FIELD_PATHS, NATIVE_UNITS, strict=True)
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "mp-params", 1, "P_BASIC", (("subject_instrument", "NVDA"),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "mp-selection",
                1,
                ("subject_instrument",),
                timedelta(seconds=10),
                timedelta(seconds=10),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=tuple(
            api.UnitConventionVersionV1("mp-unit-" + rid, 1, unit, unit, Decimal(1), Decimal(0))
            for rid, unit in zip(FIELDS, NATIVE_UNITS, strict=True)
        ),
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=2),
    )
    request = api.CalculationRequestV1(
        "D137",
        "NVDA",
        NOW,
        NOW,
        "f4-microprice",
        "mp-params",
        1,
        "mp-selection",
        1,
        (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("mp-map-" + rid, 1),
                api.VersionRefV1("mp-unit-" + rid, 1),
                "NVDA",
                None,
            )
            for rid in FIELDS
        ),
    )
    return owner, request


def test_d137_microprice_m00_public_size_weighting_exact_lineage_and_retry() -> None:
    owner, request = owner_with_quotes()
    result = owner.materialise(request)
    assert result is not None
    assert result.result == Decimal("101.6")
    assert {item.raw_signal_id for item in result.raw_input_lineage} == set(FIELDS)
    assert {item.observation_occurrence_id for item in result.raw_input_lineage} == {
        "quote-bid",
        "quote-ask",
    }
    assert owner.materialise(request) == result


def test_d137_refuses_missing_size_and_ineligible_future_quote() -> None:
    missing_owner, missing_request = owner_with_quotes(no_ask_size=True)
    assert missing_owner.materialise(missing_request) is None
    future_owner, future_request = owner_with_quotes(later_ask=True)
    assert future_owner.materialise(future_request) is None
