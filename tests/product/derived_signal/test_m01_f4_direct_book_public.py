"""F4 RC12: public direct-venue concentration and SMART/direct book divergence.

Controlled native event records enter through M00 projections; they do not prove
any particular live data provider or its field names.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 9, tzinfo=UTC)
SMART = ("R185", "R187", "R188", "R189", "R190")
DIRECT = ("R192", "R193", "R194", "R195", "R196", "R197")
SMART_KEYS = ("position", "operation", "side", "price", "size")
DIRECT_KEYS = ("position", "venue", "operation", "side", "price", "size")
NATIVE: tuple[tuple[str, dict[str, object]], ...] = (
    (
        "smart-bid",
        {
            "position": 1,
            "operation": "insert",
            "side": "bid",
            "price": Decimal(100),
            "size": Decimal(10),
        },
    ),
    (
        "smart-ask",
        {
            "position": 1,
            "operation": "insert",
            "side": "ask",
            "price": Decimal(101),
            "size": Decimal(6),
        },
    ),
    (
        "x-bid",
        {
            "position": 1,
            "venue": "X",
            "operation": "insert",
            "side": "bid",
            "price": Decimal("99.5"),
            "size": Decimal(4),
        },
    ),
    (
        "y-bid",
        {
            "position": 1,
            "venue": "Y",
            "operation": "insert",
            "side": "bid",
            "price": Decimal("99.5"),
            "size": Decimal(6),
        },
    ),
    (
        "x-ask",
        {
            "position": 1,
            "venue": "X",
            "operation": "insert",
            "side": "ask",
            "price": Decimal("101.5"),
            "size": Decimal(2),
        },
    ),
    (
        "y-ask",
        {
            "position": 1,
            "venue": "Y",
            "operation": "insert",
            "side": "ask",
            "price": Decimal("101.5"),
            "size": Decimal(4),
        },
    ),
)


def _public_books(
    *, incomplete_venue: bool = False, rows: tuple[tuple[str, dict[str, object]], ...] = NATIVE
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for seq, (tag, record) in enumerate(rows, 1):
        direct = tag[0] in ("x", "y")
        fields = DIRECT if direct else SMART
        native_record = dict(record)
        if incomplete_venue and tag == "y-ask":
            del native_record["venue"]
        moment = NOW - timedelta(seconds=len(rows) + 1 - seq)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("delivery-" + tag),
                source_provider=raw.provider_id("controlled-book"),
                native_record={"book": native_record},
                received_ts_utc=moment,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope(
                    "controlled-book:" + ("direct" if direct else "smart")
                ),
                source_temporal_kind="true_instant",
                source_timestamp_raw=moment.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in fields),
                source_variant="direct" if direct else "smart",
                subject_instrument="NVDA",
                native_units="book_record",
                revision_vintage_native="v1",
            )
        )
    items = (*zip(SMART, SMART_KEYS, strict=True), *zip(DIRECT, DIRECT_KEYS, strict=True))
    mapped: list[raw.RawSignalProjectionMappingV1] = []
    unit_ref: list[api.UnitConventionVersionV1] = []
    bindings: list[api.RawInputBindingV1] = []
    for rid, key in items:
        group = "direct" if rid in DIRECT else "smart"
        unit = "price" if key == "price" else "quantity" if key == "size" else "native"
        mapped.append(
            raw.RawSignalProjectionMappingV1(
                "map-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-book",
                group,
                ("book", key),
                unit,
            )
        )
        unit_ref.append(
            api.UnitConventionVersionV1("unit-" + rid, 1, unit, unit, Decimal(1), Decimal(0))
        )
        bindings.append(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("map-" + rid, 1),
                api.VersionRefV1("unit-" + rid, 1),
                "NVDA",
                None,
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(mapped),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "f4-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "f4-book",
                1,
                ("subject_instrument",),
                timedelta(minutes=1),
                timedelta(minutes=1),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=tuple(unit_ref),
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=1),
    )
    request = api.CalculationRequestV1(
        "D143",
        "NVDA",
        NOW,
        NOW,
        "f4-direct-book",
        "f4-basic",
        1,
        "f4-book",
        1,
        (),
        raw_input_bindings=tuple(bindings),
    )
    return owner, request


def test_d143_public_concentration_uses_true_venue_partition() -> None:
    owner, request = _public_books()
    result = owner.materialise(request)
    assert result is not None
    assert result.result == Decimal(17) / Decimal(32)
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {
        "x-bid",
        "y-bid",
        "x-ask",
        "y-ask",
    }
    assert owner.materialise(request) == result


def test_d144_public_compares_both_sides_and_venues() -> None:
    owner, request = _public_books()
    result = owner.materialise(replace(request, derived_signal_id="D144"))
    assert result is not None
    gaps = {name: dict(values) for name, values in result.result}
    assert gaps == {
        "bid:1:X": {"price_difference": Decimal("0.5"), "depth_difference": Decimal(6)},
        "bid:1:Y": {"price_difference": Decimal("0.5"), "depth_difference": Decimal(4)},
        "ask:1:X": {"price_difference": Decimal("-0.5"), "depth_difference": Decimal(4)},
        "ask:1:Y": {"price_difference": Decimal("-0.5"), "depth_difference": Decimal(2)},
    }
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {x[0] for x in NATIVE}


def test_d143_d144_refuse_missing_native_venue_instead_of_collapsing_venues() -> None:
    owner, request = _public_books(incomplete_venue=True)
    assert owner.materialise(request) is None
    assert owner.materialise(replace(request, derived_signal_id="D144")) is None


def test_public_direct_and_smart_insertions_shift_existing_levels_without_merging_venues() -> None:
    rows = (
        *NATIVE,
        (
            "smart-new-bid",
            {
                "position": 1,
                "operation": "insert",
                "side": "bid",
                "price": Decimal(100),
                "size": Decimal(7),
            },
        ),
        (
            "x-new-bid",
            {
                "position": 1,
                "venue": "X",
                "operation": "insert",
                "side": "bid",
                "price": Decimal(99),
                "size": Decimal(8),
            },
        ),
    )
    owner, request = _public_books(rows=rows)
    concentration = owner.materialise(request)
    assert concentration is not None
    # After shifting, X has 8+4+2=14, Y has 6+4=10.
    assert (
        concentration.result == (Decimal(14) / Decimal(24)) ** 2 + (Decimal(10) / Decimal(24)) ** 2
    )
    divergence = owner.materialise(replace(request, derived_signal_id="D144"))
    assert divergence is not None
    gaps = {name: dict(values) for name, values in divergence.result}
    assert gaps["bid:1:X"] == {"price_difference": Decimal(1), "depth_difference": Decimal(-1)}
    assert gaps["bid:2:X"] == {"price_difference": Decimal("0.5"), "depth_difference": Decimal(6)}
    assert gaps["bid:1:Y"] == {"price_difference": Decimal("0.5"), "depth_difference": Decimal(1)}
    assert {item.observation_occurrence_id for item in concentration.raw_input_lineage} == {
        tag for tag, record in rows if "venue" in record
    }
    assert {item.observation_occurrence_id for item in divergence.raw_input_lineage} == {
        tag for tag, _ in rows
    }


def test_public_direct_update_then_delete_uses_predecessor_and_compacts_side() -> None:
    rows = (
        *NATIVE,
        (
            "x-bid-update",
            {
                "position": 1,
                "venue": "X",
                "operation": "update",
                "side": "bid",
                "price": Decimal("99.5"),
                "size": Decimal(7),
            },
        ),
        (
            "x-ask-delete",
            {
                "position": 1,
                "venue": "X",
                "operation": "delete",
                "side": "ask",
                "price": Decimal("101.5"),
                "size": Decimal(0),
            },
        ),
    )
    owner, request = _public_books(rows=rows)
    concentration = owner.materialise(request)
    assert concentration is not None
    # X: bid 7, ask removed; Y: bid 6, ask 4.
    assert concentration.result == Decimal(149) / Decimal(289)
    divergence = owner.materialise(replace(request, derived_signal_id="D144"))
    assert divergence is not None
    gaps = {name: dict(values) for name, values in divergence.result}
    assert "ask:1:X" not in gaps
    assert gaps["bid:1:X"]["depth_difference"] == Decimal(3)
    assert gaps["bid:1:Y"]["depth_difference"] == Decimal(4)
    assert gaps["ask:1:Y"]["depth_difference"] == Decimal(2)
    assert {item.observation_occurrence_id for item in concentration.raw_input_lineage} == {
        tag for tag, record in rows if "venue" in record
    }
