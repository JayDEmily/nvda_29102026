from __future__ import annotations

import importlib

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


def test_calendar_reference_import_surface_is_present() -> None:
    importer = _require_module("nvda_desk.calendar.reference.importer")
    assert importer.__name__ == "nvda_desk.calendar.reference.importer"

    assert _require_attr(importer, "FinancialCalendarImporter") is getattr(
        importer, "FinancialCalendarImporter"
    )
    for attr_name in ("load_manifest", "load_layers", "build_reference_packet"):
        assert _require_attr(importer, attr_name) is getattr(importer, attr_name)


def test_calendar_reference_projection_surface_is_present() -> None:
    projection = _require_module("nvda_desk.calendar.reference.projection")
    assert projection.__name__ == "nvda_desk.calendar.reference.projection"

    assert _require_attr(projection, "FinancialCalendarProjectionService") is getattr(
        projection, "FinancialCalendarProjectionService"
    )
    assert _require_attr(projection, "MarketStateService") is getattr(
        projection, "MarketStateService"
    )
    for attr_name in ("project_runtime_context", "stitch_precursor_context"):
        assert _require_attr(projection, attr_name) is getattr(projection, attr_name)


def test_calendar_reference_crosswalk_surface_is_present() -> None:
    projection = _require_module("nvda_desk.calendar.reference.projection")
    assert projection.__name__ == "nvda_desk.calendar.reference.projection"

    assert _require_attr(projection, "financial_calendar_crosswalk") is getattr(
        projection, "financial_calendar_crosswalk"
    )
    assert _require_attr(projection, "FinancialCalendarCrosswalkRecord") is getattr(
        projection, "FinancialCalendarCrosswalkRecord"
    )


def test_calendar_reference_crosswalk_returns_detached_records() -> None:
    projection = _require_module("nvda_desk.calendar.reference.projection")
    assert projection.__name__ == "nvda_desk.calendar.reference.projection"
    crosswalk = _require_attr(projection, "financial_calendar_crosswalk")
    assert crosswalk is getattr(projection, "financial_calendar_crosswalk")

    first = crosswalk()
    first[0].runtime_tags.append("mutated")
    first[0].projection_targets.append("mutated_target")

    second = crosswalk()
    assert "mutated" not in second[0].runtime_tags
    assert "mutated_target" not in second[0].projection_targets
