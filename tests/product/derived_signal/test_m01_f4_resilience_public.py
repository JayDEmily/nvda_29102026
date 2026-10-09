"""F4 RC12: D142 public rebuilt depth shock and first dual-condition recovery."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 18, tzinfo=UTC)
BOOK = ("R185", "R187", "R188", "R189", "R190")
QUOTE = ("R034", "R035", "R001")
FIELDS = (*BOOK, *QUOTE)
NAMES = ("position", "operation", "side", "price", "size", "bid", "ask", "event_time")
UNITS = ("level", "operation", "side", "price", "quantity", "price", "price", "timestamp")
BOOK_EVENTS = (
    ("base-bid", -8, 0, "insert", "bid", 100, 10),
    ("base-ask", -7, 0, "insert", "ask", 102, 10),
    ("second-bid", -6, 1, "insert", "bid", 99, 10),
    ("deplete", -5, 0, "update", "bid", 100, 2),
    ("recover", -4, 0, "update", "bid", 100, 10),
)


def _public_resilience(
    *, missing_depletion_side: bool = False, delayed_recovery: bool = False
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for n, (tag, offset, position, operation, side, price, quantity) in enumerate(BOOK_EVENTS, 1):
        moment = NOW + timedelta(seconds=(10 if delayed_recovery and tag == "recover" else offset))
        entry: dict[str, object] = {
            "position": position,
            "operation": operation,
            "side": side,
            "price": Decimal(price),
            "size": Decimal(quantity),
        }
        if missing_depletion_side and tag == "deplete":
            del entry["side"]
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("resilience-" + tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("resilience-" + tag),
                source_provider=raw.provider_id("resilience-book"),
                native_record={"book": entry},
                received_ts_utc=moment,
                ingestion_sequence=n,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("resilience-book:smart"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=moment.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(x) for x in BOOK),
                source_variant="smart",
                subject_instrument="NVDA",
                native_units="book",
                revision_vintage_native="v1",
            )
        )
    quote_at = NOW - timedelta(seconds=4)
    m00.commands.admit_raw_observation_occurrence(
        raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id("resilience-quote"),
            delivery_artifact_ref=raw.delivery_artifact_ref("resilience-quote"),
            source_provider=raw.provider_id("resilience-quotes"),
            native_record={
                "bid": Decimal(100),
                "ask": Decimal(102),
                "event_time": quote_at.isoformat(),
            },
            received_ts_utc=quote_at,
            ingestion_sequence=1,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("resilience-quotes:q"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=quote_at.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(x) for x in QUOTE),
            source_variant="quote",
            subject_instrument="NVDA",
            native_units="quote",
            revision_vintage_native="v1",
        )
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "resilience-map-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "resilience-book" if i < len(BOOK) else "resilience-quotes",
                "smart" if i < len(BOOK) else "quote",
                ("book", field) if i < len(BOOK) else (field,),
                UNITS[i],
            )
            for i, (rid, field) in enumerate(zip(FIELDS, NAMES, strict=True))
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "resilience-rule",
                1,
                "P_RULE",
                (
                    ("depth_levels", 2),
                    ("shock_depth_fraction", Decimal("0.8")),
                    ("shock_spread_multiple", Decimal(2)),
                    ("recovery_depth_fraction", Decimal("0.9")),
                    ("recovery_spread_multiple", Decimal(1)),
                ),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "resilience-policy",
                1,
                ("subject_instrument",),
                timedelta(seconds=15),
                timedelta(seconds=15),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=tuple(
            api.UnitConventionVersionV1(
                "resilience-unit-" + rid, 1, unit, unit, Decimal(1), Decimal(0)
            )
            for rid, unit in zip(FIELDS, UNITS, strict=True)
        ),
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=30),
    )
    request = api.CalculationRequestV1(
        "D142",
        "NVDA",
        NOW,
        NOW,
        "resilience-definition",
        "resilience-rule",
        1,
        "resilience-policy",
        1,
        (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("resilience-map-" + rid, 1),
                api.VersionRefV1("resilience-unit-" + rid, 1),
                "NVDA",
                None,
            )
            for rid in FIELDS
        ),
    )
    return owner, request


def test_d142_public_first_joint_recovery_and_raw_lineage() -> None:
    owner, request = _public_resilience()
    result = owner.materialise(request)
    assert result is not None
    assert dict(result.result) == {
        "seconds": Decimal(1),
        "recovered_depth": Decimal(30),
        "recovered_spread": Decimal(2),
        "pre_shock_depth": Decimal(30),
        "pre_shock_spread": Decimal(2),
        "shock_depth": Decimal(22),
        "shock_spread": Decimal(2),
    }
    assert {r.raw_signal_id for r in result.raw_input_lineage} == set(FIELDS)
    assert {r.observation_occurrence_id for r in result.raw_input_lineage} == {
        *("resilience-" + tag for tag, *_ in BOOK_EVENTS),
        "resilience-quote",
    }
    assert owner.materialise(request) == result


def test_d142_refuses_incomplete_mutation_or_unrecovered_historical_book() -> None:
    incomplete, request = _public_resilience(missing_depletion_side=True)
    assert incomplete.materialise(request) is None
    historical, original = _public_resilience(delayed_recovery=True)
    assert historical.materialise(original) is None
