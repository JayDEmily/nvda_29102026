from __future__ import annotations

import importlib
from dataclasses import is_dataclass

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


def test_reference_data_contract_exports_required_models() -> None:
    contracts = _require_module("nvda_desk.contracts.reference_data")
    assert contracts.__name__ == "nvda_desk.contracts.reference_data"

    for attr_name in (
        "ReferenceArtifactKind",
        "ReferenceArtifact",
        "BundleLayerReference",
        "ImportedReferenceBundle",
        "LiveEventSnapshot",
        "PrecursorRuntimePacket",
    ):
        assert _require_attr(contracts, attr_name) is getattr(contracts, attr_name)


def test_reference_data_contract_models_are_dataclasses() -> None:
    contracts = _require_module("nvda_desk.contracts.reference_data")
    assert contracts.__name__ == "nvda_desk.contracts.reference_data"

    for attr_name in (
        "ReferenceArtifact",
        "BundleLayerReference",
        "ImportedReferenceBundle",
        "LiveEventSnapshot",
        "PrecursorRuntimePacket",
    ):
        model = _require_attr(contracts, attr_name)
        assert is_dataclass(model), f"{attr_name} must be a dataclass"


def test_reference_data_contract_fields_expose_bundle_and_runtime_context() -> None:
    contracts = _require_module("nvda_desk.contracts.reference_data")
    assert contracts.__name__ == "nvda_desk.contracts.reference_data"

    bundle_model = _require_attr(contracts, "ImportedReferenceBundle")
    assert bundle_model is getattr(contracts, "ImportedReferenceBundle")
    snapshot_model = _require_attr(contracts, "LiveEventSnapshot")
    assert snapshot_model is getattr(contracts, "LiveEventSnapshot")
    precursor_model = _require_attr(contracts, "PrecursorRuntimePacket")
    assert precursor_model is getattr(contracts, "PrecursorRuntimePacket")

    bundle_fields = set(getattr(bundle_model, "__dataclass_fields__", {}).keys())
    snapshot_fields = set(getattr(snapshot_model, "__dataclass_fields__", {}).keys())
    precursor_fields = set(getattr(precursor_model, "__dataclass_fields__", {}).keys())

    assert {"bundle_id", "version", "artifacts"} <= bundle_fields
    assert {"event_id", "event_type", "runtime_tags"} <= snapshot_fields
    assert {"context_id", "effective_at", "events"} <= precursor_fields
