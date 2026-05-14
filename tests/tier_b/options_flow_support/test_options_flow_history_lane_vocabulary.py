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


def test_options_flow_history_lane_vocabulary_and_schema_surfaces_are_present() -> None:
    contracts = _require_module("nvda_desk.contracts.options_flow_history")
    vocabulary_schema = _require_module("nvda_desk.schemas.vocabulary")
    vocabulary_builder = _require_module("scripts.build_canonical_vocabulary")

    _require_attr(contracts, "OptionsFlowHistoryObservationRecord")
    _require_attr(contracts, "OptionsFlowHistoryWriteResult")
    _require_attr(vocabulary_schema, "VocabularyEntry")
    _require_attr(vocabulary_builder, "build_canonical_vocabulary")


def test_options_flow_history_lane_is_not_admitted_as_a_runtime_stage() -> None:
    contracts = _require_module("nvda_desk.contracts.options_flow_history")
    observation_model = _require_attr(contracts, "OptionsFlowHistoryObservationRecord")
    write_result_model = _require_attr(contracts, "OptionsFlowHistoryWriteResult")

    assert hasattr(observation_model, "model_fields")
    assert hasattr(write_result_model, "model_fields")
    assert "derived_state" in observation_model.model_fields
    assert "lineage" in observation_model.model_fields
    assert "persisted" in write_result_model.model_fields
