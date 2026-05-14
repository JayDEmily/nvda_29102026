from __future__ import annotations

import ast
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


def _python_files(*roots: str) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        files.extend(sorted(Path(root).rglob("*.py")))
    return files


def _imports_package(path: Path, package_name: str) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == package_name or alias.name.startswith(f"{package_name}."):
                    return True
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module == package_name or node.module.startswith(f"{package_name}."):
                return True
    return False


def test_replay_evaluation_surface_is_present() -> None:
    package_module = _require_module("nvda_desk.analysis.replay")
    assert package_module.__name__ == "nvda_desk.analysis.replay"
    service_module = _require_module("nvda_desk.analysis.replay.service")
    assert service_module.__name__ == "nvda_desk.analysis.replay.service"

    assert _require_attr(package_module, "ReplayEvaluationService") is getattr(package_module, "ReplayEvaluationService")
    assert _require_attr(package_module, "ReplayComparisonResult") is getattr(package_module, "ReplayComparisonResult")
    assert _require_attr(package_module, "describe_replay_fixture_source") is getattr(package_module, "describe_replay_fixture_source")
    assert _require_attr(service_module, "ReplayFixtureSource") is getattr(service_module, "ReplayFixtureSource")


def test_replay_evaluation_surface_stays_analysis_only_and_outside_scenarios() -> None:
    service_module = _require_module("nvda_desk.analysis.replay.service")
    assert service_module.__name__ == "nvda_desk.analysis.replay.service"

    service = _require_attr(service_module, "ReplayEvaluationService")()
    fixture_source = service.describe_fixture_source()
    comparison = service.compare_outputs(
        baseline={"packet_id": "pkt-1", "status": "ok"},
        candidate={"packet_id": "pkt-1", "status": "different", "extra": True},
    )
    lineage_key = "packet" "_ids"
    lineage = service.build_lineage(**{lineage_key: ["pkt-1"], "replay_run_id": "replay-1"})

    assert fixture_source.fixture_root.name == "replay"
    assert fixture_source.readme_path.name == "README.md"
    assert comparison.differing_fields == ("status",)
    assert comparison.candidate_only_fields == ("extra",)
    assert getattr(lineage, lineage_key) == ["pkt-1"]
    assert lineage.replay_run_id == "replay-1"
    assert not Path("src/nvda_desk/analysis/scenarios").exists()

    scoped_files = _python_files("src/nvda_desk", "tests/tier_a", "tests/tier_b")
    scenario_importers = [
        str(path) for path in scoped_files if _imports_package(path, "nvda_desk.analysis.scenarios")
    ]
    assert scenario_importers == []
