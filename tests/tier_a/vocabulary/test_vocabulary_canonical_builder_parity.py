from __future__ import annotations

import importlib
import json
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


def test_canonical_vocabulary_matches_builder_output_via_both_import_paths() -> None:
    wrapper_builder = _require_module("scripts.build_canonical_vocabulary")
    assert wrapper_builder.__name__ == "scripts.build_canonical_vocabulary"
    native_builder = _require_module("nvda_desk.vocabulary_builder")
    assert native_builder.__name__ == "nvda_desk.vocabulary_builder"

    wrapper_build_document = _require_attr(wrapper_builder, "build_document")
    assert wrapper_build_document is getattr(wrapper_builder, "build_document")
    native_build_document = _require_attr(native_builder, "build_document")
    assert native_build_document is getattr(native_builder, "build_document")

    vocab_path = Path("data/vocabulary/canonical_vocabulary.json")
    if not vocab_path.exists():
        pytest.fail(
            "Required vocabulary artefact is not implemented: data/vocabulary/canonical_vocabulary.json"
        )

    committed = json.loads(vocab_path.read_text(encoding="utf-8"))
    assert committed == wrapper_build_document().to_dict()
    assert committed == native_build_document().to_dict()
