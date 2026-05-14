from __future__ import annotations

import importlib
from datetime import date, datetime, timedelta

import pytest

from nvda_desk.preparation.runtime_preparer import PreparedRuntimeLineage, PreparedRuntimeSnapshot


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_cognition_ingress_mapping_surfaces_are_present() -> None:
    temporal_mapper = _require_module("nvda_desk.cognition.ingress.temporal_mapper")
    assert temporal_mapper.__name__ == "nvda_desk.cognition.ingress.temporal_mapper"
    regime_mapper = _require_module("nvda_desk.cognition.ingress.regime_mapper")
    assert regime_mapper.__name__ == "nvda_desk.cognition.ingress.regime_mapper"
    options_mapper = _require_module("nvda_desk.cognition.ingress.options_mapper")
    assert options_mapper.__name__ == "nvda_desk.cognition.ingress.options_mapper"

    assert _require_attr(temporal_mapper, "build_temporal_input") is getattr(temporal_mapper, "build_temporal_input")
    assert _require_attr(regime_mapper, "build_regime_input") is getattr(regime_mapper, "build_regime_input")
    assert _require_attr(options_mapper, "build_options_flow_input") is getattr(options_mapper, "build_options_flow_input")


def test_cognition_ingress_mappers_consume_prepared_runtime_snapshot() -> None:
    temporal_mapper = _require_module("nvda_desk.cognition.ingress.temporal_mapper")
    assert temporal_mapper.__name__ == "nvda_desk.cognition.ingress.temporal_mapper"
    regime_mapper = _require_module("nvda_desk.cognition.ingress.regime_mapper")
    assert regime_mapper.__name__ == "nvda_desk.cognition.ingress.regime_mapper"
    options_mapper = _require_module("nvda_desk.cognition.ingress.options_mapper")
    assert options_mapper.__name__ == "nvda_desk.cognition.ingress.options_mapper"

    source_time_utc = datetime(2026, 4, 21, 9, 31)
    next_event_time_utc = source_time_utc + timedelta(minutes=30)
    snapshot = PreparedRuntimeSnapshot(
        snapshot_id="snap-1",
        payload={
            "source_time_utc": source_time_utc,
            "next_event_time_utc": next_event_time_utc,
            "windows": [
                {
                    "event_id": "event-1",
                    "window_start_utc": source_time_utc + timedelta(minutes=5),
                    "window_end_utc": source_time_utc + timedelta(minutes=10),
                    "tags": ["macro"],
                }
            ],
            "nvda_return_pct": 0.12,
            "nq_return_pct": 0.03,
            "vix_level": 19.5,
            "spot_price": 101.0,
            "front_dte": 1,
            "next_dte": 5,
        },
        lineage=PreparedRuntimeLineage(source_kind="api_payload", transport="mapping"),
    )

    temporal_input = _require_attr(temporal_mapper, "build_temporal_input")(snapshot)
    regime_input = _require_attr(regime_mapper, "build_regime_input")(snapshot)
    options_input = _require_attr(options_mapper, "build_options_flow_input")(snapshot)

    assert temporal_input.source_time_utc == source_time_utc
    assert temporal_input.next_event_time_utc == next_event_time_utc
    assert len(temporal_input.windows) == 1
    assert temporal_input.windows[0].event_id == "event-1"
    assert regime_input.nvda_return_pct == 0.12
    assert regime_input.nq_return_pct == 0.03
    assert regime_input.vix_level == 19.5
    assert regime_input.missing_fields == []
    assert options_input.spot_price == 101.0
    assert options_input.front_dte == 1
    assert options_input.next_dte == 5
    assert options_input.missing_fields == []


def test_cognition_ingress_mappers_represent_absence_without_fabricating_certainty() -> None:
    temporal_mapper = _require_module("nvda_desk.cognition.ingress.temporal_mapper")
    assert temporal_mapper.__name__ == "nvda_desk.cognition.ingress.temporal_mapper"
    regime_mapper = _require_module("nvda_desk.cognition.ingress.regime_mapper")
    assert regime_mapper.__name__ == "nvda_desk.cognition.ingress.regime_mapper"
    options_mapper = _require_module("nvda_desk.cognition.ingress.options_mapper")
    assert options_mapper.__name__ == "nvda_desk.cognition.ingress.options_mapper"

    source_date = date(2026, 4, 21)
    snapshot = PreparedRuntimeSnapshot(
        snapshot_id="snap-missing",
        payload={
            "source_date": source_date,
            "windows": [],
        },
        lineage=PreparedRuntimeLineage(source_kind="api_payload", transport="mapping"),
    )

    temporal_input = _require_attr(temporal_mapper, "build_temporal_input")(snapshot)
    regime_input = _require_attr(regime_mapper, "build_regime_input")(snapshot)
    options_input = _require_attr(options_mapper, "build_options_flow_input")(snapshot)

    assert temporal_input.source_date == source_date
    assert temporal_input.next_event_time_utc is None
    assert temporal_input.windows == []
    assert regime_input.nvda_return_pct is None
    assert regime_input.nq_return_pct is None
    assert regime_input.vix_level is None
    assert regime_input.missing_fields == ["nvda_return_pct", "nq_return_pct", "vix_level"]
    assert options_input.spot_price is None
    assert options_input.front_dte is None
    assert options_input.next_dte is None
    assert options_input.missing_fields == ["spot_price", "front_dte", "next_dte"]


def test_temporal_mapper_rejects_missing_source_temporal_truth_instead_of_falling_back_to_wall_clock() -> (
    None
):
    temporal_mapper = _require_module("nvda_desk.cognition.ingress.temporal_mapper")
    assert temporal_mapper.__name__ == "nvda_desk.cognition.ingress.temporal_mapper"

    snapshot = PreparedRuntimeSnapshot(
        snapshot_id="snap-no-time",
        payload={
            "windows": [],
        },
        lineage=PreparedRuntimeLineage(source_kind="api_payload", transport="mapping"),
    )

    with pytest.raises(ValueError, match="source temporal truth"):
        _require_attr(temporal_mapper, "build_temporal_input")(snapshot)
