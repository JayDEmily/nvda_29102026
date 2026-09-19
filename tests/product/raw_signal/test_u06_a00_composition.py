from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest
import yaml
from tests.product.raw_signal._support import observation, policy

import nvda_desk.composition as composition

ROOT = Path(__file__).resolve().parents[3]


def test_architecture_runtime_edge_is_exactly_a00_to_m00() -> None:
    rules = yaml.safe_load((ROOT / "config/architecture/dependency_rules.yaml").read_text())
    assert rules["declared_owner_edges"] == [{"source": "A00", "target": "M00"}]


def test_a00_composition_source_may_import_only_the_m00_public_seam() -> None:
    imported: set[str] = set()
    for path in (ROOT / "src/nvda_desk/composition").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
            elif isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
    m00_imports = {
        name for name in imported if name.startswith("nvda_desk.raw_signal_occurrence_truth")
    }
    assert m00_imports <= {"nvda_desk.raw_signal_occurrence_truth.api"}


def test_a00_test_application_builder_exists_only_as_construction_glue() -> None:
    builder = getattr(composition, "_build_test_application", None)
    if builder is None:
        pytest.fail("A00 proof construction symbol _build_test_application is not implemented")
    source = inspect.getsource(builder).lower()
    for forbidden in ("zero_received", "one_or_more_received", "unknown_not_established"):
        assert forbidden not in source


def test_a00_sequential_path_uses_m00_command_and_read_facets_without_extra_meaning() -> None:
    builder = getattr(composition, "_build_test_application", None)
    if builder is None:
        pytest.fail("A00 proof construction symbol _build_test_application is not implemented")
    app = builder()
    result = app.run_raw_signal_proof_sequence(
        capture_scope_policy=policy(),
        slot_start_utc="2026-09-20T12:00:00Z",
        capture_occurrence_id="a00-capture-001",
        raw_observation=observation(observation_occurrence_id="a00-observation-001"),
        assessment_occurrence_id="a00-assessment-001",
    )
    assert result.capture.capture_occurrence_id == "a00-capture-001"
    assert result.observation.observation_occurrence_id == "a00-observation-001"
    assert result.assessment.outcome in {
        "unknown_not_established",
        "zero_received",
        "one_or_more_received",
    }
    assert result.readback.observation_occurrence_id == result.observation.observation_occurrence_id
    for forbidden in ("dmpv3_packet", "k01", "downstream_consumer", "exact_count"):
        assert not hasattr(result, forbidden)
