from __future__ import annotations

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
M01 = ROOT / "src" / "nvda_desk" / "derived_signal_calculation_truth"


def _python_sources() -> list[Path]:
    if not M01.is_dir():
        pytest.fail("DS-T01 expected M01 source package to exist after DS-I01 implementation")
    sources = sorted(M01.rglob("*.py"))
    assert sources
    return sources


def test_m01_never_imports_m00_private_persistence_or_raw_observation_carrier() -> None:
    forbidden_modules = {
        "nvda_desk.raw_signal_occurrence_truth._postgres",
    }
    for path in _python_sources():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = {alias.name for alias in node.names}
                assert forbidden_modules.isdisjoint(names), (path, names)
            elif isinstance(node, ast.ImportFrom):
                assert node.module not in forbidden_modules, (path, node.module)
                if node.module == "nvda_desk.raw_signal_occurrence_truth.api":
                    imported = {alias.name for alias in node.names}
                    assert "RawObservationOccurrenceV1" not in imported, (path, imported)


def test_m01_source_contains_no_direct_m00_table_reference_or_external_effect_client() -> None:
    prohibited_text = (
        "rsot_capture_scope_policy_v1",
        "rsot_scheduled_capture_occurrence_v1",
        "rsot_raw_observation_occurrence_v1",
        "rsot_capture_receipt_presence_assessment_v1",
        "place_order",
        "cancel_order",
        "modify_order",
        "brokerage",
    )
    for path in _python_sources():
        text = path.read_text(encoding="utf-8")
        for token in prohibited_text:
            assert token not in text, (path, token)
