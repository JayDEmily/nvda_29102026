from __future__ import annotations

import importlib
from datetime import datetime, timedelta

import pytest

from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.ingress.raw_bundle_loader import load_api_payload
from nvda_desk.preparation.runtime_preparer import prepare_runtime_dataset


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_cognition_ingress_translation_coordinator_surface_is_present() -> None:
    translator = _require_module("nvda_desk.cognition.ingress.translator")
    assert translator.__name__ == "nvda_desk.cognition.ingress.translator"

    assert _require_attr(translator, "CognitionIngressTranslator") is getattr(translator, "CognitionIngressTranslator")
    assert _require_attr(translator, "convert_snapshot") is getattr(translator, "convert_snapshot")


def test_cognition_ingress_translation_coordinator_emits_typed_stage_input_bundle() -> None:
    translator = _require_module("nvda_desk.cognition.ingress.translator")
    assert translator.__name__ == "nvda_desk.cognition.ingress.translator"
    convert_snapshot = _require_attr(translator, "convert_snapshot")
    assert convert_snapshot is getattr(translator, "convert_snapshot")

    source_time_utc = datetime(2026, 4, 21, 9, 31, 15)
    next_event_time_utc = source_time_utc + timedelta(minutes=20)
    dataset = prepare_runtime_dataset(
        load_api_payload(
            {
                "snapshot_id": "snap-2",
                "source_time_utc": source_time_utc,
                "market_snapshot": {
                    "spot_price": 100.0,
                    "nvda_return_pct": 0.15,
                    "nq_return_pct": 0.04,
                    "vix_level": 24.0,
                    "next_event_time_utc": next_event_time_utc,
                    "windows": [
                        {
                            "event_id": "event-2",
                            "window_start_utc": source_time_utc + timedelta(minutes=1),
                            "window_end_utc": source_time_utc + timedelta(minutes=2),
                            "tags": ["earnings"],
                        }
                    ],
                },
                "options_surface": {
                    "spot_price": 102.0,
                    "front_dte": 1,
                    "next_dte": 14,
                },
            }
        )
    )

    result = convert_snapshot(dataset)

    assert isinstance(result, StageInputBundle)
    assert result.temporal.source_time_utc == source_time_utc
    assert result.temporal.next_event_time_utc == next_event_time_utc
    assert len(result.temporal.windows) == 1
    assert result.regime.nvda_return_pct == 0.15
    assert result.regime.nq_return_pct == 0.04
    assert result.regime.vix_level == 24.0
    assert result.options_flow.spot_price == 102.0
    assert result.options_flow.front_dte == 1
    assert result.options_flow.next_dte == 14
