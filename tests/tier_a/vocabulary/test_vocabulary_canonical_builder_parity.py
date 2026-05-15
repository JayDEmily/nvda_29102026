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


def test_governed_source_hashes_cover_authoritative_vocabulary_surfaces() -> None:
    native_builder = _require_module("nvda_desk.vocabulary_builder")
    governed_paths = {str(path) for path in _require_attr(native_builder, "GOVERNED_SOURCE_PATHS")}

    required_hash_sources = {
        "docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md",
        "docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md",
        "docs/vocabulary/README.md",
        "docs/vocabulary/CONSOLIDATION_WORKFLOW.md",
        "docs/vocabulary/vocabulary_registry.md",
        "scripts/build_canonical_vocabulary.py",
        "src/nvda_desk/schemas/vocabulary.py",
        "src/nvda_desk/vocabulary_builder.py",
        "src/nvda_desk/vocabulary_synonym_audit.py",
        "data/vocabulary/canonical_vocabulary.json",
    }
    assert required_hash_sources <= governed_paths
    assert "var/vocabulary/synonym_candidates.json" not in governed_paths

    hashes = native_builder.governed_source_hashes()
    assert required_hash_sources <= set(hashes)
    assert "var/vocabulary/synonym_candidates.json" not in hashes


def test_durable_row_terms_are_governed_exactly_or_by_alias() -> None:
    native_builder = _require_module("nvda_desk.vocabulary_builder")
    payload = native_builder.build_canonical_payload()

    governed_terms = set()
    for entry in payload["entries"]:
        governed_terms.add(entry["canonical_label"].casefold())
        governed_terms.add(entry["canonical_slug"].replace("_", " ").casefold())
        governed_terms.update(alias.casefold() for alias in entry.get("allowed_aliases", []))

    required_terms = {
        "opening architecture",
        "placement readiness",
        "placement handoff",
        "downstream opening",
        "broker protocol",
        "capital deployment decision",
        "serial candidate",
        "live position",
        "inventory architecture",
        "exit architecture",
        "close architecture",
        "review layer",
        "explanation layer",
        "parallel risk lane",
        "serial desk-cognition",
        "dynamic coefficient",
        "modifier authority",
        "playbook library",
        "prepared ingress",
        "runtime context",
        "raw signal families",
        "event calendar",
        "dmpv3 packet",
    }
    assert required_terms <= governed_terms

    registry_text = Path("docs/vocabulary/vocabulary_registry.md").read_text(encoding="utf-8").casefold()
    registry_required_terms = required_terms - {"dynamic coefficient", "dmpv3 packet"}
    assert {f"### {term}" for term in registry_required_terms} <= set(
        f"### {line.strip().removeprefix('### ').casefold()}"
        for line in registry_text.splitlines()
        if line.startswith("### ")
    )


def test_disallowed_phrase_guardrails_and_evidence_appendix() -> None:
    native_builder = _require_module("nvda_desk.vocabulary_builder")
    payload = native_builder.build_canonical_payload()

    disallowed: list[str] = []
    governed_terms: set[str] = set()
    for entry in payload["entries"]:
        governed_terms.add(entry["canonical_label"].casefold())
        governed_terms.update(alias.casefold() for alias in entry.get("allowed_aliases", []))
        disallowed.extend(entry.get("disallowed_phrases", []))

    normalised_disallowed = [phrase.casefold() for phrase in disallowed]
    assert len(normalised_disallowed) == len(set(normalised_disallowed))
    assert not (set(normalised_disallowed) & governed_terms)

    appendix_path = Path(
        "var/audit/active_code_atlas_001/"
        "vocabulary_candidate_adjudication_evidence_hardening_before_fwd016_20260515/"
        "VOCABULARY_CANDIDATE_ADJUDICATION_APPENDIX.json"
    )
    if not appendix_path.exists():
        pytest.fail(f"Required adjudication evidence artefact missing: {appendix_path}")
    appendix = json.loads(appendix_path.read_text(encoding="utf-8"))
    represented_disallowed = {
        record["normalised_phrase"]
        for record in appendix["records"]
        if record["decision"] == "disallowed_non_term_phrase"
    }
    fragment_like_disallowed = {
        "ithout runtime context",
        "pared runtime context",
        "stream opening architecture",
        "and close architecture",
    }
    assert fragment_like_disallowed <= represented_disallowed
