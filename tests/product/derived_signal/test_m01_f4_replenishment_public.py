"""F4 RC12: D141 depleted-size restoration through native M00 event projection."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 17, tzinfo=UTC)
BOOK = ("R185", "R187", "R188", "R189", "R190")
TRADE = ("R120", "R121")
UNITS = ("level", "operation", "side", "price", "quantity", "price", "quantity")
FIELDS = ("position", "operation", "side", "price", "size", "trade_price", "trade_size")
BOOK_EVENTS = (
    ("bid-create", -5, "insert", "bid", Decimal(100), Decimal(10)),
    ("ask-create", -4, "insert", "ask", Decimal(101), Decimal(8)),
    ("bid-deplete", -3, "update", "bid", Decimal(100), Decimal(6)),
    ("bid-restore", -2, "update", "bid", Decimal(100), Decimal(9)),
)


def _public_owner(
    *, absent_book_price: bool = False, future_restore: bool = False
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for seq, (tag, offset, operation, side, price, quantity) in enumerate(BOOK_EVENTS, 1):
        moment = NOW + timedelta(
            seconds=(10 if future_restore and tag == "bid-restore" else offset)
        )
        record = {
            "position": 1,
            "operation": operation,
            "side": side,
            "price": price,
            "size": quantity,
        }
        if absent_book_price and tag == "bid-deplete":
            record.pop("price")
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("reload-" + tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("reload-" + tag),
                source_provider=raw.provider_id("reload-book"),
                native_record={"book": record},
                received_ts_utc=moment,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("reload-book:smart"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=moment.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(f) for f in BOOK),
                source_variant="smart",
                subject_instrument="NVDA",
                native_units="depth",
                revision_vintage_native="v1",
            )
        )
    trade_moment = NOW - timedelta(seconds=2)
    m00.commands.admit_raw_observation_occurrence(
        raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id("reload-trade"),
            delivery_artifact_ref=raw.delivery_artifact_ref("reload-trade"),
            source_provider=raw.provider_id("reload-trades"),
            native_record={"trade_price": Decimal(100), "trade_size": Decimal(4)},
            received_ts_utc=trade_moment,
            ingestion_sequence=1,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("reload-trades:tape"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=trade_moment.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(f) for f in TRADE),
            source_variant="tape",
            subject_instrument="NVDA",
            native_units="trade",
            revision_vintage_native="v1",
        )
    )
    catalogue_ids = (*BOOK, *TRADE)
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "reload-map-" + rid,
            1,
            raw.RawSignalCatalogueId(rid),
            "reload-book" if i < len(BOOK) else "reload-trades",
            "smart" if i < len(BOOK) else "tape",
            ("book", field) if i < len(BOOK) else (field,),
            UNITS[i],
        )
        for i, (rid, field) in enumerate(zip(catalogue_ids, FIELDS, strict=True))
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "reload-rule",
                1,
                "P_RULE",
                (("window_seconds", 10), ("replenishment_max_seconds", 3)),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "reload-policy",
                1,
                ("subject_instrument",),
                timedelta(seconds=10),
                timedelta(seconds=10),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=tuple(
            api.UnitConventionVersionV1(
                "reload-unit-" + rid, 1, UNITS[i], UNITS[i], Decimal(1), Decimal(0)
            )
            for i, rid in enumerate(catalogue_ids)
        ),
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=30),
    )
    request = api.CalculationRequestV1(
        "D141",
        "NVDA",
        NOW,
        NOW,
        "reload-calculation",
        "reload-rule",
        1,
        "reload-policy",
        1,
        (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("reload-map-" + rid, 1),
                api.VersionRefV1("reload-unit-" + rid, 1),
                "NVDA",
                None,
            )
            for rid in catalogue_ids
        ),
    )
    return owner, request


def test_d141_public_depletion_recovery_score_and_full_lineage() -> None:
    owner, request = _public_owner()
    result = owner.materialise(request)
    assert result is not None
    assert result.result == Decimal("0.75")
    assert {r.raw_signal_id for r in result.raw_input_lineage} == set((*BOOK, *TRADE))
    assert {r.observation_occurrence_id for r in result.raw_input_lineage} == {
        *("reload-" + tag for tag, *_ in BOOK_EVENTS),
        "reload-trade",
    }
    assert owner.materialise(request) == result


def test_d141_incomplete_price_and_future_restoration_refuse_false_replenishment() -> None:
    owner, request = _public_owner(absent_book_price=True)
    assert owner.materialise(request) is None
    future_owner, future_request = _public_owner(future_restore=True)
    result = future_owner.materialise(future_request)
    assert result is not None
    assert result.result == Decimal(0)
    assert "reload-bid-restore" not in {
        r.observation_occurrence_id for r in result.raw_input_lineage
    }
