from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone

import pytest

from nvda_desk.calendar.reference.importer import load_manifest
from nvda_desk.calendar.reference.projection import project_runtime_context


def _manifest() -> dict:
    return {
        "bundle_id": "calendar-bundle-001",
        "version": "2026.05",
        "artifacts": [
            {
                "artifact_id": "nyse-calendar",
                "kind": "calendar_bundle",
                "source_path": "data/reference/calendar/nyse.json",
                "version": "2026.05",
            },
            {
                "artifact_id": "event-crosswalk",
                "kind": "crosswalk",
                "source_path": "data/reference/calendar/crosswalk.json",
                "version": "2026.05",
            },
        ],
        "layers": [
            {
                "layer_id": "checked-calendar-reference",
                "artifact_ids": ["nyse-calendar", "event-crosswalk"],
            }
        ],
    }


def test_calendar_manifest_rejects_duplicate_artifacts_and_unknown_layer_refs() -> None:
    duplicate_payload = _manifest()
    duplicate_payload["artifacts"].append(deepcopy(duplicate_payload["artifacts"][0]))
    with pytest.raises(ValueError, match="duplicate reference artifact_id"):
        load_manifest(duplicate_payload)

    unknown_layer_payload = _manifest()
    unknown_layer_payload["layers"][0]["artifact_ids"].append("not-present")
    with pytest.raises(ValueError, match="unknown artifacts"):
        load_manifest(unknown_layer_payload)


def test_calendar_manifest_rejects_runtime_decision_keys() -> None:
    payload = _manifest()
    payload["capital_sizing"] = {"pct": 10}

    with pytest.raises(ValueError, match="forbidden runtime authority keys"):
        load_manifest(payload)


def test_calendar_projection_emits_checked_reference_trace_without_trading_authority() -> None:
    bundle = load_manifest(_manifest())
    effective_at = datetime(2026, 5, 9, tzinfo=timezone.utc)

    packet = project_runtime_context(
        bundle=bundle,
        context_id="ctx-calendar-001",
        effective_at=effective_at,
        event_rows=[
            {
                "event_id": "evt-fomc-001",
                "event_type": "fomc_window",
                "source_artifact_id": "nyse-calendar",
                "observed_at": effective_at,
            }
        ],
    )

    assert packet.projection_trace is not None
    assert packet.projection_trace.bundle_id == "calendar-bundle-001"
    assert packet.projection_trace.artifact_ids == ["event-crosswalk", "nyse-calendar"]
    assert packet.projection_trace.event_ids == ["evt-fomc-001"]
    assert packet.projection_trace.projection_mode == "checked_reference_projection"
    assert packet.projection_trace.online_mutation_allowed is False
    assert packet.projection_trace.candidate_formation_allowed is False
    assert packet.projection_trace.capital_sizing_allowed is False
    assert packet.events[0].evaluation_tags == ["event_risk"]


def test_calendar_projection_rejects_unknown_source_and_forbidden_runtime_keys() -> None:
    bundle = load_manifest(_manifest())
    effective_at = datetime(2026, 5, 9, tzinfo=timezone.utc)

    with pytest.raises(ValueError, match="unknown source_artifact_id"):
        project_runtime_context(
            bundle=bundle,
            context_id="ctx-calendar-002",
            effective_at=effective_at,
            event_rows=[
                {
                    "event_id": "evt-unknown",
                    "event_type": "market_holiday",
                    "source_artifact_id": "not-present",
                }
            ],
        )

    with pytest.raises(ValueError, match="forbidden runtime authority keys"):
        project_runtime_context(
            bundle=bundle,
            context_id="ctx-calendar-003",
            effective_at=effective_at,
            event_rows=[
                {
                    "event_id": "evt-order",
                    "event_type": "market_holiday",
                    "source_artifact_id": "nyse-calendar",
                    "trading_instruction": "buy",
                }
            ],
        )


def test_calendar_manifest_rejects_duplicate_layer_ids() -> None:
    payload = _manifest()
    payload["layers"].append(deepcopy(payload["layers"][0]))

    with pytest.raises(ValueError, match="duplicate calendar layer_id"):
        load_manifest(payload)


def test_calendar_projection_rejects_duplicate_event_ids() -> None:
    bundle = load_manifest(_manifest())
    effective_at = datetime(2026, 5, 9, tzinfo=timezone.utc)

    with pytest.raises(ValueError, match="duplicate calendar event_id"):
        project_runtime_context(
            bundle=bundle,
            context_id="ctx-calendar-duplicate-events",
            effective_at=effective_at,
            event_rows=[
                {
                    "event_id": "evt-duplicate",
                    "event_type": "market_holiday",
                    "source_artifact_id": "nyse-calendar",
                },
                {
                    "event_id": "evt-duplicate",
                    "event_type": "fomc_window",
                    "source_artifact_id": "event-crosswalk",
                },
            ],
        )


def test_calendar_manifest_rejects_nested_runtime_decision_keys() -> None:
    artifact_payload = _manifest()
    artifact_payload["artifacts"][0]["candidate_formation"] = {"from_calendar": True}
    with pytest.raises(ValueError, match="forbidden runtime authority keys"):
        load_manifest(artifact_payload)

    layer_payload = _manifest()
    layer_payload["layers"][0]["capital_sizing"] = {"pct": 10}
    with pytest.raises(ValueError, match="forbidden runtime authority keys"):
        load_manifest(layer_payload)
