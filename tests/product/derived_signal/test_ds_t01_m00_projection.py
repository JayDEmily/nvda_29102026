from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

from ._support import projection_mapping, raw_observation


def test_exact_mapping_is_required_and_catalogue_provenance_never_guesses_field() -> None:
    owner = raw_api.create_owner()
    observation = raw_observation(
        "1", native_value=Decimal("5"), received_ts_utc=datetime(2026, 10, 4, 1, tzinfo=UTC)
    )
    owner.commands.admit_raw_observation_occurrence(observation)

    assert (
        owner.reads.project_raw_value(
            raw_api.RawSignalCatalogueId("R001"),
            observation.observation_occurrence_id,
            mappings=(),
        )
        is None
    )

    bid_mapping = projection_mapping(field_path=("quote", "bid"))
    ask_mapping = projection_mapping(field_path=("quote", "ask"), version=2)
    assert (
        owner.reads.project_raw_value(
            raw_api.RawSignalCatalogueId("R001"),
            observation.observation_occurrence_id,
            mappings=(bid_mapping, ask_mapping),
        )
        is None
    )


def test_exact_projection_preserves_native_value_units_and_required_lineage_metadata() -> None:
    owner = raw_api.create_owner()
    observation = raw_observation(
        "2", native_value=Decimal("5"), received_ts_utc=datetime(2026, 10, 4, 1, 0, 1, tzinfo=UTC)
    )
    owner.commands.admit_raw_observation_occurrence(observation)
    mapping = projection_mapping()

    projected = owner.reads.project_raw_value(
        raw_api.RawSignalCatalogueId("R001"),
        observation.observation_occurrence_id,
        mappings=(mapping,),
    )
    assert projected is not None
    assert projected.raw_signal_catalogue_id == raw_api.RawSignalCatalogueId("R001")
    assert projected.observation_occurrence_id == observation.observation_occurrence_id
    assert projected.projection_mapping_id == mapping.mapping_id
    assert projected.projection_mapping_version == mapping.version
    assert projected.source_provider == "provider-a"
    assert projected.source_variant == "snapshot"
    assert projected.native_field_path == ("quote", "bid")
    assert projected.native_value == Decimal("5")
    assert projected.native_units == "percent"
    assert projected.subject_instrument == "NVDA"
    assert projected.source_temporal_kind == "true_instant"
    assert projected.source_timestamp_raw == observation.source_timestamp_raw
    assert projected.source_timezone_native == "UTC"
    assert projected.received_ts_utc == observation.received_ts_utc
    assert projected.ingestion_sequence == observation.ingestion_sequence
    assert projected.ingestion_sequence_scope == observation.ingestion_sequence_scope
    assert projected.revision_vintage_native == "rev-2"


def test_mapping_with_missing_native_field_or_units_produces_no_projection() -> None:
    owner = raw_api.create_owner()
    observation = raw_observation(
        "3", native_value=Decimal("5"), received_ts_utc=datetime(2026, 10, 4, 1, 0, 2, tzinfo=UTC)
    )
    owner.commands.admit_raw_observation_occurrence(observation)

    missing_field = projection_mapping(field_path=("quote", "missing"))
    assert (
        owner.reads.project_raw_value(
            raw_api.RawSignalCatalogueId("R001"),
            observation.observation_occurrence_id,
            mappings=(missing_field,),
        )
        is None
    )

    mapping_type = type(projection_mapping())
    with pytest.raises(ValueError, match="native_units"):
        mapping_type(
            mapping_id="invalid-units",
            version=1,
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R001"),
            source_provider="provider-a",
            source_variant="snapshot",
            native_field_path=("quote", "bid"),
            native_units="",
        )


def test_projected_history_is_bounded_repeatably_ordered_and_paginates_without_duplication(
) -> None:
    owner = raw_api.create_owner()
    base = datetime(2026, 10, 4, 1, tzinfo=UTC)
    observations = (
        raw_observation(
            "1", native_value=Decimal("1"), received_ts_utc=base + timedelta(seconds=3)
        ),
        raw_observation(
            "2", native_value=Decimal("2"), received_ts_utc=base + timedelta(seconds=1)
        ),
        raw_observation(
            "3", native_value=Decimal("3"), received_ts_utc=base + timedelta(seconds=2)
        ),
        raw_observation(
            "4",
            native_value=Decimal("4"),
            received_ts_utc=base + timedelta(seconds=4),
            subject="AMD",
        ),
    )
    for observation in observations:
        owner.commands.admit_raw_observation_occurrence(observation)
    mapping = projection_mapping()

    first = owner.reads.list_projected_raw_history(
        raw_api.RawSignalCatalogueId("R001"),
        mappings=(mapping,),
        subject_instrument="NVDA",
        received_at_or_before_utc=base + timedelta(seconds=10),
        limit=2,
        cursor=None,
    )
    repeated = owner.reads.list_projected_raw_history(
        raw_api.RawSignalCatalogueId("R001"),
        mappings=(mapping,),
        subject_instrument="NVDA",
        received_at_or_before_utc=base + timedelta(seconds=10),
        limit=2,
        cursor=None,
    )
    assert first == repeated
    assert len(first.items) == 2
    assert first.next_cursor is not None

    second = owner.reads.list_projected_raw_history(
        raw_api.RawSignalCatalogueId("R001"),
        mappings=(mapping,),
        subject_instrument="NVDA",
        received_at_or_before_utc=base + timedelta(seconds=10),
        limit=2,
        cursor=first.next_cursor,
    )
    ids = [item.observation_occurrence_id for item in (*first.items, *second.items)]
    assert len(ids) == 3
    assert len(set(ids)) == 3
    assert second.next_cursor is None

    with pytest.raises(ValueError, match="limit"):
        owner.reads.list_projected_raw_history(
            raw_api.RawSignalCatalogueId("R001"),
            mappings=(mapping,),
            subject_instrument="NVDA",
            received_at_or_before_utc=None,
            limit=0,
            cursor=None,
        )


def test_projection_exposes_exact_mapped_selection_identity_and_refuses_missing_dimension() -> None:
    owner = raw_api.create_owner()
    base = raw_observation(
        "5", native_value=Decimal("100"), received_ts_utc=datetime(2026, 10, 4, 1, 0, 5, tzinfo=UTC)
    )
    observation = replace(
        base,
        native_identifier="provider-contract-C1",
        native_record={
            "quote": {"bid": Decimal("100")},
            "option": {
                "contract_id": "C1",
                "underlying_instrument": "NVDA",
                "expiry": "2026-12-18",
                "strike": Decimal("150"),
                "option_right": "call",
            },
        },
    )
    owner.commands.admit_raw_observation_occurrence(observation)

    mapping = raw_api.RawSignalProjectionMappingV1(
        mapping_id="provider-a:snapshot:R001:v1:quote.bid:contract-selection",
        version=1,
        raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R001"),
        source_provider="provider-a",
        source_variant="snapshot",
        native_field_path=("quote", "bid"),
        native_units="percent",
        selection_identity_field_paths=(
            ("contract_id", ("option", "contract_id")),
            ("underlying_instrument", ("option", "underlying_instrument")),
            ("expiry", ("option", "expiry")),
            ("strike", ("option", "strike")),
            ("option_right", ("option", "option_right")),
        ),
    )
    projected = owner.reads.project_raw_value(
        raw_api.RawSignalCatalogueId("R001"),
        observation.observation_occurrence_id,
        mappings=(mapping,),
    )
    assert projected is not None
    assert projected.selection_identity is not None
    assert projected.selection_identity.values == (
        ("contract_id", "C1"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal("150")),
        ("option_right", "call"),
    )

    missing_dimension_mapping = replace(
        mapping,
        mapping_id="provider-a:snapshot:R001:v2:quote.bid:contract-selection",
        version=2,
        selection_identity_field_paths=(
            ("contract_id", ("option", "missing_contract_id")),
        ),
    )
    assert (
        owner.reads.project_raw_value(
            raw_api.RawSignalCatalogueId("R001"),
            observation.observation_occurrence_id,
            mappings=(missing_dimension_mapping,),
        )
        is None
    )
