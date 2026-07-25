from __future__ import annotations

import importlib
from pathlib import Path

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


def test_canonical_runtime_specimen_surface_is_present() -> None:
    package_module = _require_module("nvda_desk.testing.harnesses")
    assert package_module.__name__ == "nvda_desk.testing.harnesses"
    harness_module = _require_module("nvda_desk.testing.harnesses.canonical_runtime")
    assert harness_module.__name__ == "nvda_desk.testing.harnesses.canonical_runtime"

    assert _require_attr(package_module, "CanonicalRuntimeHarness") is getattr(package_module, "CanonicalRuntimeHarness")
    assert _require_attr(package_module, "CanonicalRuntimeSpecimen") is getattr(package_module, "CanonicalRuntimeSpecimen")
    assert _require_attr(package_module, "build_canonical_runtime_specimen") is getattr(package_module, "build_canonical_runtime_specimen")
    assert _require_attr(harness_module, "CanonicalRuntimeHarnessPaths") is getattr(harness_module, "CanonicalRuntimeHarnessPaths")


def test_canonical_runtime_specimen_surface_stays_test_only_and_fixture_backed() -> None:
    harness_module = _require_module("nvda_desk.testing.harnesses.canonical_runtime")
    assert harness_module.__name__ == "nvda_desk.testing.harnesses.canonical_runtime"
    build_specimen = _require_attr(harness_module, "build_canonical_runtime_specimen")
    assert build_specimen is getattr(harness_module, "build_canonical_runtime_specimen")

    dependency_key = "packet" "_ids"
    specimen = build_specimen(
        **{
            dependency_key: ["pkt-1", "pkt-2"],
            "replay_run_id": "replay-1",
            "scenario_ids": ["scenario-a"],
        }
    )
    source_text = Path("src/nvda_desk/testing/harnesses/canonical_runtime.py").read_text(
        encoding="utf-8"
    )

    assert specimen.fixture_paths.replay_root.name == "replay"
    assert specimen.fixture_paths.trace_review_root.name == "trace_review"
    assert getattr(specimen.fixture_paths, "dmp" "_v3_root").name == "dmp_v3"
    assert getattr(specimen.replay_lineage, dependency_key) == ["pkt-1", "pkt-2"]
    assert specimen.trace_review_pack.scenario_ids == ["scenario-a"]
    assert "nvda_desk.entry" not in source_text
    assert "nvda_desk.api" not in source_text
