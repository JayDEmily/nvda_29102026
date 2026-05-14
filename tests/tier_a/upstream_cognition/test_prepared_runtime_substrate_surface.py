from __future__ import annotations

import importlib
from datetime import datetime, timedelta

import pytest

from nvda_desk.ingress.raw_bundle_loader import load_api_payload


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_preparation_runtime_substrate_surface_is_present() -> None:
    preparer = _require_module("nvda_desk.preparation.runtime_preparer")
    assert preparer.__name__ == "nvda_desk.preparation.runtime_preparer"

    for attr_name in (
        "RuntimePreparationService",
        "PreparedRuntimeSnapshot",
        "PreparedRuntimeDataset",
        "prepare_runtime_dataset",
        "align_snapshot_to_bar",
        "derive_runtime_features",
    ):
        assert _require_attr(preparer, attr_name) is getattr(preparer, attr_name)


def test_preparation_runtime_dataset_exposes_alignment_lineage_derivation_and_failures() -> None:
    preparer = _require_module("nvda_desk.preparation.runtime_preparer")
    assert preparer.__name__ == "nvda_desk.preparation.runtime_preparer"
    prepare_runtime_dataset = _require_attr(preparer, "prepare_runtime_dataset")
    assert prepare_runtime_dataset is getattr(preparer, "prepare_runtime_dataset")

    source_time_utc = datetime(2026, 4, 21, 9, 31, 45)
    next_event_time_utc = source_time_utc + timedelta(minutes=45)
    bundle = load_api_payload(
        {
            "snapshot_id": "snap-1",
            "source_time_utc": source_time_utc,
            "market_snapshot": {
                "spot_price": 100.0,
                "prior_close": 90.0,
                "nq_return_pct": 0.02,
                "vix_level": 22.5,
                "next_event_time_utc": next_event_time_utc,
                "windows": [
                    {
                        "event_id": "earnings",
                        "window_start_utc": source_time_utc + timedelta(minutes=10),
                        "window_end_utc": source_time_utc + timedelta(minutes=20),
                        "tags": ["earnings"],
                    }
                ],
            },
            "options_surface": {
                "spot_price": 101.0,
                "front_dte": 1,
                "next_dte": 5,
            },
        }
    )

    dataset = prepare_runtime_dataset(bundle)
    snapshot = dataset.primary_snapshot

    assert snapshot.snapshot_id == "snap-1"
    assert snapshot.payload["source_time_utc"] == source_time_utc
    assert snapshot.payload["runtime_bar_time_utc"] == source_time_utc.replace(
        second=0, microsecond=0
    )
    assert snapshot.payload["market_spot_price"] == 100.0
    assert snapshot.payload["options_spot_price"] == 101.0
    assert snapshot.payload["spot_price"] == 101.0
    assert snapshot.payload["front_to_next_dte_spread"] == 4
    assert snapshot.payload["minutes_to_next_event"] == 45
    assert snapshot.payload["window_count"] == 1
    assert snapshot.payload["has_windows"] is True
    assert snapshot.payload["nvda_return_pct"] == pytest.approx((100.0 - 90.0) / 90.0)
    assert snapshot.lineage.source_kind == "api_payload"
    assert snapshot.lineage.transport == "mapping"
    assert snapshot.lineage.source_sections == ("market_snapshot", "options_surface")
    assert snapshot.lineage.alignment_policy == "floor_minute_from_source_time_utc"
    assert set(snapshot.lineage.derived_field_names) == {
        "front_to_next_dte_spread",
        "has_windows",
        "minutes_to_next_event",
        "nvda_return_pct",
        "window_count",
    }
    assert snapshot.failed_enrichments == []
    assert snapshot.missing_optional_enrichments == []
    assert dataset.failed_enrichments == []
    assert dataset.missing_optional_enrichments == []


def test_preparation_runtime_dataset_makes_optional_absence_explicit() -> None:
    preparer = _require_module("nvda_desk.preparation.runtime_preparer")
    assert preparer.__name__ == "nvda_desk.preparation.runtime_preparer"
    prepare_runtime_dataset = _require_attr(preparer, "prepare_runtime_dataset")
    assert prepare_runtime_dataset is getattr(preparer, "prepare_runtime_dataset")

    dataset = prepare_runtime_dataset(
        load_api_payload(
            {
                "snapshot_id": "snap-absence",
                "source_date": "2026-04-21",
                "market_snapshot": {"spot_price": 100.0},
                "options_surface": {},
            }
        )
    )
    snapshot = dataset.primary_snapshot

    assert snapshot.lineage.alignment_policy == "missing_" "source_time_utc"
    assert snapshot.payload == {
        "source_date": datetime(2026, 4, 21).date(),
        "market_spot_price": 100.0,
        "options_spot_price": 100.0,
        "spot_price": 100.0,
    }
    assert snapshot.derived_fields == {}
    assert snapshot.failed_enrichments == []
    assert snapshot.missing_optional_enrichments == [
        "window_count:windows",
        "minutes_to_next_event:next_event_time_utc",
        "front_to_next_dte_spread:dte_inputs",
        "nvda_return_pct:price_inputs",
    ]
    assert dataset.missing_optional_enrichments == [
        "snap-absence:window_count:windows",
        "snap-absence:minutes_to_next_event:next_event_time_utc",
        "snap-absence:front_to_next_dte_spread:dte_inputs",
        "snap-absence:nvda_return_pct:price_inputs",
    ]


def test_raw_bundle_loader_preserves_nested_source_temporal_truth() -> None:
    source_time_utc = datetime(2026, 4, 21, 9, 31, 45)
    bundle = load_api_payload(
        {
            "snapshot_id": "nested-temporal",
            "market_snapshot": {
                "spot_price": 100.0,
                "source_time_utc": source_time_utc,
                "source_time_raw": "2026-04-21T09:31:45-04:00",
                "source_timezone_raw": "America/New_York",
                "time_granularity": "timestamp",
            },
            "options_surface": {"front_dte": 1, "next_dte": 5},
        }
    )

    assert bundle.provenance.source_time_utc == source_time_utc
    assert bundle.provenance.source_time_raw == "2026-04-21T09:31:45-04:00"
    assert bundle.provenance.source_timezone_raw == "America/New_York"
    assert bundle.provenance.time_granularity == "timestamp"


def test_prepared_runtime_snapshot_detaches_nested_payload_from_caller() -> None:
    preparer = _require_module("nvda_desk.preparation.runtime_preparer")
    prepare_runtime_snapshot = _require_attr(preparer, "prepare_runtime_snapshot")

    caller_payload = {
        "snapshot_id": "legacy-nested",
        "source_time_utc": datetime(2026, 4, 21, 9, 31, 45),
        "raw_context": {"windows": [{"event_id": "earnings"}]},
    }

    snapshot = prepare_runtime_snapshot(snapshot_id="legacy-nested", payload=caller_payload)
    caller_payload["raw_context"]["windows"][0]["event_id"] = "mutated"

    assert snapshot.payload["raw_context"]["windows"][0]["event_id"] == "earnings"
