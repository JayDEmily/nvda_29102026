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

    assert committed["schema_version"] == "v2_namespaced"
    assert set(committed["namespaces"]) == {"global", "m02", "m03", "m04", "m05", "m06", "m07", "m08", "m09", "m10"}
    assert committed["namespaces"]["m02"]["imports"] == ["global"]
    assert committed["namespaces"]["m03"]["imports"] == ["global"]
    assert committed["namespaces"]["m04"]["imports"] == ["global"]
    assert committed["namespaces"]["m05"]["imports"] == ["global", "m03", "m04", "m07", "m08"]
    assert committed["namespaces"]["m07"]["imports"] == ["global"]
    assert committed["namespaces"]["m08"]["imports"] == ["global"]
    assert committed["namespaces"]["m09"]["imports"] == ["global", "m05", "m06", "m07"]
    assert committed["namespaces"]["m10"]["imports"] == ["global", "m09"]
    assert "config" not in committed["namespaces"]["m02"]["scan_paths"]
    assert "config" not in committed["namespaces"]["m03"]["scan_paths"]
    assert "config" not in committed["namespaces"]["m04"]["scan_paths"]
    assert "config" not in committed["namespaces"]["m05"]["scan_paths"]
    assert "config" not in committed["namespaces"]["m07"]["scan_paths"]
    assert "config" not in committed["namespaces"]["m08"]["scan_paths"]
    assert "config" not in committed["namespaces"]["m09"]["scan_paths"]
    assert "config" not in committed["namespaces"]["m10"]["scan_paths"]

    m02_entries = [
        entry for entry in committed["entries"] if entry["namespace"] == "m02"
    ]
    assert len(m02_entries) == 3
    assert {entry["canonical_id"] for entry in m02_entries} == {
        "m02.calendar_fact_candidate",
        "m02.financial_calendar_snapshot",
        "m02.calendar_projection",
    }

    m03_entries = [
        entry for entry in committed["entries"] if entry["namespace"] == "m03"
    ]
    assert len(m03_entries) == 3
    assert {entry["canonical_id"] for entry in m03_entries} == {
        "m03.prepared_data_envelope",
        "m03.field_resolution_receipt",
        "m03.prepared_data_builder",
    }

    m04_entries = [
        entry for entry in committed["entries"] if entry["namespace"] == "m04"
    ]
    assert len(m04_entries) == 10
    assert {entry["canonical_id"] for entry in m04_entries} == {
        "m04.reference_packet",
        "m04.prepared_context_packet",
        "m04.stage_packet",
        "m04.parallel_risk_packet",
        "m04.review_explanation_packet",
        "m04.replay_request_packet",
        "m04.replay_result_packet",
        "m04.replay_comparison_packet",
        "m04.diagnostic_packet",
        "m04.rejection_packet",
    }

    m05_entries = [
        entry for entry in committed["entries"] if entry["namespace"] == "m05"
    ]
    assert len(m05_entries) == 5
    assert {entry["canonical_id"] for entry in m05_entries} == {
        "m05.stage_context",
        "m05.stage_input",
        "m05.stage_output",
        "m05.serial_candidate",
        "m05.serial_runner",
    }

    m07_entries = [
        entry for entry in committed["entries"] if entry["namespace"] == "m07"
    ]
    assert len(m07_entries) == 3
    assert {entry["canonical_id"] for entry in m07_entries} == {
        "m07.policy_bundle",
        "m07.modifier_decision",
        "m07.modifier_application_receipt",
    }

    m08_entries = [
        entry for entry in committed["entries"] if entry["namespace"] == "m08"
    ]
    assert len(m08_entries) == 3
    assert {entry["canonical_id"] for entry in m08_entries} == {
        "m08.playbook_definition",
        "m08.playbook_catalogue",
        "m08.eligibility_decision",
    }

    m09_entries = [
        entry for entry in committed["entries"] if entry["namespace"] == "m09"
    ]
    assert len(m09_entries) == 4
    assert {entry["canonical_id"] for entry in m09_entries} == {
        "m09.final_risk_decision",
        "m09.capital_state",
        "m09.capital_deployment_decision",
        "m09.capital_deployment_receipt",
    }

    m10_entries = [entry for entry in committed["entries"] if entry["namespace"] == "m10"]
    assert len(m10_entries) == 4
    assert {entry["canonical_id"] for entry in m10_entries} == {
        "m10.placement_intent",
        "m10.execution_port",
        "m10.execution_event",
        "m10.execution_receipt",
    }


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
    registry_required_terms = required_terms - {
        "dynamic coefficient",
        "dmpv3 packet",
        "serial desk-cognition",
    }
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
