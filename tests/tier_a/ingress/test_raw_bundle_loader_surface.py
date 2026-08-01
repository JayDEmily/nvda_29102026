from __future__ import annotations

import importlib
from datetime import datetime

import pytest


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_raw_bundle_loader_surface_is_present() -> None:
    ingress_module = _require_module("nvda_desk.ingress.raw_bundle_loader")
    assert ingress_module.__name__ == "nvda_desk.ingress.raw_bundle_loader"

    assert _require_attr(ingress_module, "RawBundleLoader") is getattr(
        ingress_module, "RawBundleLoader"
    )
    assert _require_attr(ingress_module, "RawBundleProvenance") is getattr(
        ingress_module, "RawBundleProvenance"
    )
    assert _require_attr(ingress_module, "RealDataBundle") is getattr(
        ingress_module, "RealDataBundle"
    )
    assert _require_attr(ingress_module, "load_api_payload") is getattr(
        ingress_module, "load_api_payload"
    )
    assert _require_attr(ingress_module, "load_json_bundle") is getattr(
        ingress_module, "load_json_bundle"
    )


def test_raw_bundle_loader_preserves_ingress_preparation_and_reference_boundaries() -> None:
    ingress_module = _require_module("nvda_desk.ingress.raw_bundle_loader")
    assert ingress_module.__name__ == "nvda_desk.ingress.raw_bundle_loader"
    market_wrapper = _require_module("nvda_desk.adapters.ingress.market_snapshot_feed")
    assert market_wrapper.__name__ == "nvda_desk.adapters.ingress.market_snapshot_feed"
    options_wrapper = _require_module("nvda_desk.adapters.ingress.options_surface_feed")
    assert options_wrapper.__name__ == "nvda_desk.adapters.ingress.options_surface_feed"
    calendar_wrapper = _require_module("nvda_desk.adapters.ingress.calendar_feed")
    assert calendar_wrapper.__name__ == "nvda_desk.adapters.ingress.calendar_feed"

    source_time_utc = datetime(2026, 4, 21, 9, 31, 45)
    loader = _require_attr(ingress_module, "RawBundleLoader")()
    bundle = loader.load_api_payload(
        {
            "snapshot_id": "snap-1",
            "source_time_utc": source_time_utc,
            "market_snapshot": {"spot_price": 100.0, "nvda_return_pct": 0.4},
            "options_surface": {"spot_price": 101.0, "front_dte": 1, "next_dte": 5},
        }
    )
    assert bundle.provenance.source_kind == "api_payload"
    assert bundle.market_snapshot["spot_price"] == 100.0
    assert bundle.options_surface["spot_price"] == 101.0

    prepared = _require_attr(market_wrapper, "adapt_market_snapshot")(
        {
            "snapshot_id": "snap-1",
            "source_time_utc": source_time_utc,
            "market_snapshot": {"spot_price": 100.0, "nvda_return_pct": 0.4},
        }
    )
    assert prepared.snapshot_id == "snap-1"
    assert prepared.lineage.source_kind == "api_payload"
    assert prepared.payload["source_time_utc"] == source_time_utc
    assert prepared.payload["runtime_bar_time_utc"] == source_time_utc.replace(
        second=0, microsecond=0
    )
    assert prepared.payload["spot_price"] == 100.0
    assert prepared.payload["market_spot_price"] == 100.0
    assert prepared.payload["nvda_return_pct"] == 0.4
    assert prepared.missing_optional_enrichments == [
        "window_count:windows",
        "minutes_to_next_event:next_event_time_utc",
        "front_to_next_dte_spread:dte_inputs",
    ]

    options_input = _require_attr(options_wrapper, "adapt_options_surface")(
        {
            "source_time_utc": source_time_utc,
            "market_snapshot": {"spot_price": 100.0},
            "options_surface": {"spot_price": 101.0, "front_dte": 1, "next_dte": 5},
        }
    )
    assert options_input.spot_price == 101.0
    assert options_input.front_dte == 1
    assert options_input.next_dte == 5

    reference_bundle = _require_attr(calendar_wrapper, "adapt_calendar_manifest")(
        {"bundle_id": "bundle-1", "artifacts": [], "layers": []}
    )
    assert reference_bundle.bundle_id == "bundle-1"


def test_raw_bundle_loader_requires_source_observation_truth_not_capture_clock_only() -> None:
    ingress_module = _require_module("nvda_desk.ingress.raw_bundle_loader")
    loader = _require_attr(ingress_module, "RawBundleLoader")()
    capture_time = datetime(2026, 4, 21, 9, 31, 45)

    with pytest.raises(
        ValueError,
        match="source temporal standard requires source_time_utc or source_date",
    ):
        loader.load_api_payload(
            {
                "snapshot_id": "snap-capture-only",
                "captured_at_utc": capture_time,
                "persisted_at_utc": capture_time,
                "market_snapshot": {"spot_price": 100.0},
                "options_surface": {"front_dte": 1, "next_dte": 5},
            }
        )
