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


def test_research_logs_owner_surface_is_present() -> None:
    persistence_module = _require_module("nvda_desk.persistence.research_logs")
    assert persistence_module.__name__ == "nvda_desk.persistence.research_logs"
    repository_wrapper = _require_module("nvda_desk.repositories.research_logs")
    assert repository_wrapper.__name__ == "nvda_desk.repositories.research_logs"

    owner = _require_attr(persistence_module, "ResearchLogsRepository")
    assert owner is getattr(persistence_module, "ResearchLogsRepository")
    wrapper = _require_attr(repository_wrapper, "ResearchLogsRepository")
    assert wrapper is getattr(repository_wrapper, "ResearchLogsRepository")
    assert wrapper is owner


def test_research_logs_owner_stays_append_only_and_research_bounded() -> None:
    persistence_module = _require_module("nvda_desk.persistence.research_logs")
    assert persistence_module.__name__ == "nvda_desk.persistence.research_logs"
    owner = _require_attr(persistence_module, "ResearchLogsRepository")
    assert owner is getattr(persistence_module, "ResearchLogsRepository")

    repository = owner()
    repository.append_log({"run_id": "eval-1", "kind": "evaluation_run"})
    listed = repository.list_logs()
    listed[0]["kind"] = "mutated"

    assert repository.list_logs() == [{"run_id": "eval-1", "kind": "evaluation_run"}]
