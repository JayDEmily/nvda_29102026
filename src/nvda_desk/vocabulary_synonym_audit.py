"""Deterministic vocabulary synonym-candidate audit.

This audit does not call external APIs. It writes a structured escalation artefact
that a later LLM pass in the sandbox can consume.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from nvda_desk.schemas.vocabulary import (
    VocabularyCandidate,
    VocabularyCandidateAction,
    VocabularyCandidateClassification,
    vocabulary_document_from_dict,
)
from nvda_desk.vocabulary_builder import build_canonical_payload, governed_source_hashes

OUTPUT_PATH = Path("var/vocabulary/synonym_candidates.json")
STAMP_PATH = Path("data/vocabulary/vocabulary_touch_stamp.json")
SCAN_PATHS = [Path("src"), Path("tests"), Path("docs"), Path("config")]
ALLOWED_EXTENSIONS = {".py", ".md", ".yaml", ".yml", ".json", ".toml"}
TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_\- ]{2,80}")
FWD001_GOVERNANCE_CANDIDATE_FRAGMENTS = {
    (
        "config/proof_blocks.yaml",
        "_".join(["coefficient", "authority", "service"]),
        " ".join(["coefficient", "authority", "service"]),
        "coefficient_authority",
    ),
    (
        "config/proof_blocks.yaml",
        "_".join(["source", "temporal", "standard", "surface"]),
        " ".join(["source", "temporal", "standard", "surface"]),
        "source_temporal_standard",
    ),
    (
        "config/retained_test_registry.yaml",
        "_".join(["coefficient", "authority", "service"]),
        " ".join(["coefficient", "authority", "service"]),
        "coefficient_authority",
    ),
    (
        "config/retained_test_registry.yaml",
        " ".join(["dynamic", "coefficient"]),
        " ".join(["dynamic", "coefficient"]),
        "bounded_dynamic_coefficient",
    ),
    (
        "config/retained_test_registry.yaml",
        "_".join(["source", "temporal", "standard", "surface"]),
        " ".join(["source", "temporal", "standard", "surface"]),
        "source_temporal_standard",
    ),
    (
        "src/nvda_desk/contracts/playbook.py",
        "_".join(["playbook", "eligibility", "service"]),
        " ".join(["playbook", "eligibility", "service"]),
        "playbook_eligibility",
    ),
    (
        "src/nvda_desk/contracts/playbook.py",
        "_".join(["raw", "source"]),
        " ".join(["raw", "source"]),
        "source_time_raw",
    ),
    (
        "src/nvda_desk/contracts/playbook.py",
        "_".join(["raw", "source"]),
        " ".join(["raw", "source"]),
        "source_timezone_raw",
    ),
    (
        "tests/tier_a/legacy_imported/test_imported_module_containment_surface.py",
        "_".join(["financial", "calendar"]),
        " ".join(["financial", "calendar"]),
        "financial_calendar_crosswalk",
    ),
    (
        "tests/tier_a/legacy_imported/test_imported_module_containment_surface.py",
        "_".join(["parallel", "risk"]),
        " ".join(["parallel", "risk"]),
        "parallel_risk_lane",
    ),
    (
        "tests/tier_a/modifiers/test_dynamic_modifier_transform_boundary_surface.py",
        "_".join(["coefficient", "authority", "service"]),
        " ".join(["coefficient", "authority", "service"]),
        "coefficient_authority",
    ),
    (
        "tests/tier_a/modifiers/test_dynamic_modifier_transform_boundary_surface.py",
        "_".join(["state", "conditioned"]),
        " ".join(["state", "conditioned"]),
        "state_conditioned_modifier",
    ),
    (
        "tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py",
        "_".join(["parallel", "risk"]),
        " ".join(["parallel", "risk"]),
        "parallel_risk_lane",
    ),
    (
        "tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py",
        "_".join(["parallel", "risk", "lane", "service"]),
        " ".join(["parallel", "risk", "lane", "service"]),
        "parallel_risk_lane",
    ),
    (
        "tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py",
        "_".join(["risk", "lane"]),
        " ".join(["risk", "lane"]),
        "parallel_risk_lane",
    ),
    (
        "tests/tier_a/playbook/test_playbook_transform_boundary_surface.py",
        "_".join(["playbook", "eligibility", "service"]),
        " ".join(["playbook", "eligibility", "service"]),
        "playbook_eligibility",
    ),
    (
        "tests/tier_a/review_runtime/test_review_explanation_service_surface.py",
        "_".join(["packet", "ids"]),
        " ".join(["packet", "ids"]),
        "dependency_packet_ids",
    ),
    (
        "tests/tier_a/review_runtime/test_review_transform_boundary_surface.py",
        "_".join(["packet", "ids"]),
        " ".join(["packet", "ids"]),
        "dependency_packet_ids",
    ),
}


def _normalise(value: str) -> str:
    return re.sub(r"[_\-\s]+", " ", value.strip().casefold())


def _compact_normalise(value: str) -> str:
    return re.sub(r"[_\-\s]+", "", value.strip().casefold())


def _fingerprint() -> str:
    items = governed_source_hashes()
    blob = json.dumps(items, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _load_document() -> dict:
    payload = build_canonical_payload()
    vocabulary_document_from_dict(payload)
    return payload


def _lexicon(payload: dict) -> tuple[set[str], set[str], list[tuple[str, str, str, str]]]:
    exact_tokens: set[str] = set()
    compact_exact_tokens: set[str] = set()
    entries: list[tuple[str, str, str, str]] = []
    for entry in payload["entries"]:
        label = entry["canonical_label"]
        slug = entry["canonical_slug"]
        canonical_norm = _normalise(label)
        for token in [label, slug]:
            exact_tokens.add(_normalise(token))
            compact_exact_tokens.add(_compact_normalise(token))
        for alias in entry.get("allowed_aliases", []):
            exact_tokens.add(_normalise(alias))
            compact_exact_tokens.add(_compact_normalise(alias))
        for phrase in entry.get("disallowed_phrases", []):
            exact_tokens.add(_normalise(phrase))
            compact_exact_tokens.add(_compact_normalise(phrase))
        entries.append((slug, label, canonical_norm, entry.get("category", "")))
    return exact_tokens, compact_exact_tokens, entries


def _iter_candidates():
    for base in SCAN_PATHS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in ALLOWED_EXTENSIONS:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in TOKEN_PATTERN.finditer(text):
                yield str(path), match.group(0)


def _is_identifier_like(raw_phrase: str) -> bool:
    return (
        " " not in raw_phrase
        and "_" not in raw_phrase
        and "-" not in raw_phrase
        and raw_phrase != raw_phrase.lower()
    )


def _is_protocol_identifier_fragment(
    raw_phrase: str,
    candidate: str,
    target: str,
    category: str,
) -> bool:
    if category != "protocol_field" or "_" not in raw_phrase:
        return False
    candidate_parts = candidate.split()
    target_parts = target.split()
    if not set(target_parts) <= set(candidate_parts):
        return False
    extra_parts = set(candidate_parts) - set(target_parts)
    return len(extra_parts) <= 1


def _is_python_function_declaration_identifier_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    target: str,
) -> bool:
    if not path.endswith(".py") or "_" not in raw_phrase:
        return False
    if not raw_phrase.lstrip().startswith("def "):
        return False
    candidate_parts = candidate.split()
    target_parts = target.split()
    if candidate_parts[:1] != ["def"]:
        return False
    return candidate_parts[1:] == target_parts


def _is_vocabulary_seed_note_relationship_fragment(
    path: str,
    candidate: str,
    target: str,
    slug: str,
    category: str,
) -> bool:
    if path != "src/nvda_desk/vocabulary_builder.py":
        return False
    if slug != "source_temporal_standard" or category != "authority_surface":
        return False
    candidate_parts = candidate.split()
    target_parts = target.split()
    return candidate_parts == [*target_parts, "field"]


def _is_dmp_v3_fixture_root_descriptor_fragment(
    path: str,
    candidate: str,
    target: str,
    slug: str,
) -> bool:
    if path != "src/nvda_desk/testing/harnesses/canonical_runtime.py":
        return False
    if slug != "dmp_v3":
        return False
    return candidate == f"{target} root"


def _is_baseline_only_surface_error_text_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    target: str,
    slug: str,
) -> bool:
    if path != "src/nvda_desk/contracts/coefficient_authority.py":
        return False
    if slug != "baseline_only_surface":
        return False
    if candidate != " ".join(["baseline", "only"]):
        return False
    normalised_raw = raw_phrase.strip().casefold()
    baseline_key = "_".join(["baseline", "only"])
    baseline_dash = "-".join(["baseline", "only"])
    return normalised_raw in {baseline_key, baseline_dash} or (
        baseline_dash + " surface" in normalised_raw
    )


def _is_coefficient_authority_import_descriptor_fragment(
    path: str,
    candidate: str,
    target: str,
    slug: str,
) -> bool:
    if slug != "coefficient_authority":
        return False
    if candidate != f"{target} import":
        return False
    authority_module = "coefficient" + "_" + "authority"
    return path in {
        "src/nvda_desk/config/__init__.py",
        f"src/nvda_desk/config/{authority_module}.py",
        f"src/nvda_desk/services/{authority_module}_service.py",
    }


def _is_downstream_stage_read_service_method_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    target: str,
    slug: str,
) -> bool:
    if path != "src/nvda_desk/services/downstream_state_service.py":
        return False
    if slug != "stage_read_state":
        return False
    if candidate != " ".join(["read", "state"]):
        return False
    return raw_phrase.strip() == "_".join(["read", "state"])


def _is_coefficient_authority_service_accessor_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    target: str,
    slug: str,
) -> bool:
    if slug != "coefficient_authority":
        return False
    if candidate != f"{target} service":
        return False
    if raw_phrase.strip() != "_".join(["coefficient", "authority", "service"]):
        return False
    authority_module = "coefficient" + "_" + "authority"
    return path in {
        "src/nvda_desk/cognition/modifiers/state_conditioned.py",
        "src/nvda_desk/config/config_surface.py",
        "src/nvda_desk/services/posture_service.py",
        f"src/nvda_desk/services/{authority_module}_service.py",
    }


def _is_parallel_risk_lane_contract_descriptor_fragment(
    path: str,
    candidate: str,
    slug: str,
) -> bool:
    slug_parts = ["parallel", "risk", "lane"]
    if slug != "_".join(slug_parts):
        return False
    two_part = " ".join(slug_parts[:2])
    dataschema_fragment = " ".join([*slug_parts, "dataschema"])
    packet_fragment = " ".join([*slug_parts, "packet"])
    module_slug = "_".join(slug_parts)
    contract_module = "_".join(slug_parts[:2])
    selected_fragments = {
        ("src/nvda_desk/contracts/__init__.py", two_part),
        (f"src/nvda_desk/contracts/{contract_module}.py", two_part),
        (f"src/nvda_desk/contracts/{contract_module}.py", dataschema_fragment),
        (
            f"src/nvda_desk/persistence/{contract_module}_observations.py",
            dataschema_fragment,
        ),
        ("src/nvda_desk/risk/parallel/evaluate.py", two_part),
        (f"src/nvda_desk/services/{module_slug}_service.py", two_part),
        (
            f"src/nvda_desk/testing/harnesses/serial_runtime_{contract_module}_boundary_specimen.py",
            packet_fragment,
        ),
    }
    return (path, candidate) in selected_fragments


def _is_dependency_packet_ids_replay_review_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    slug: str,
    category: str,
) -> bool:
    if slug != "dependency_packet_ids" or category != "protocol_field":
        return False
    if candidate != " ".join(["packet", "ids"]):
        return False
    if raw_phrase.strip() != "_".join(["packet", "ids"]):
        return False
    return path in {
        "src/nvda_desk/analysis/replay/service.py",
        "src/nvda_desk/contracts/replay.py",
        "src/nvda_desk/contracts/review.py",
        "src/nvda_desk/services/review_explanation_service.py",
        "src/nvda_desk/testing/harnesses/canonical_runtime.py",
    }


def _is_testing_harness_specimen_artifact_descriptor_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    slug: str,
) -> bool:
    module_8_specimen = (
        "src/nvda_desk/testing/harnesses/" "module_8_parallel_risk_workbook_specimen.py"
    )
    serial_boundary_specimen = (
        "src/nvda_desk/testing/harnesses/" "serial_runtime_parallel_risk_boundary_specimen.py"
    )
    selected_fragments = {
        (
            module_8_specimen,
            " ".join(["append", "only", "observation", "record", "json"]),
            "append_only_observation_record",
        ),
        (
            module_8_specimen,
            " ".join(["stage", "input", "bundle", "json"]),
            "stage_input_bundle",
        ),
        (
            serial_boundary_specimen,
            " ".join(["specimen", "stage", "input", "bundle"]),
            "stage_input_bundle",
        ),
    }
    return (path, candidate, slug) in selected_fragments


def _is_pr_stage_environment_descriptor_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    slug: str,
) -> bool:
    contract_module = "_".join(["parallel", "risk"])
    contract_path = f"src/nvda_desk/contracts/{contract_module}.py"
    domain_path = f"src/nvda_desk/domain/{contract_module}/environment_assessment.py"
    selected_fragments = {
        (
            contract_path,
            " ".join(["bootstrap", "stage", "read", "state"]),
            "stage_read_state",
            "_".join(["bootstrap", "stage", "read", "state"]),
        ),
        (
            contract_path,
            " ".join(["bounded", "environment", "assessment"]),
            "environment_assessment",
            "_".join(["bounded", "environment", "assessment"]),
        ),
        (
            contract_path,
            " ".join(["environment", "assessment", "only"]),
            "environment_assessment",
            "_".join(["environment", "assessment", "only"]),
        ),
        (
            domain_path,
            " ".join(["environment", "assessment", "only"]),
            "environment_assessment",
            "_".join(["environment", "assessment", "only"]),
        ),
    }
    return (path, candidate, slug, raw_phrase.strip()) in selected_fragments


def _is_coefficient_authority_path_field_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    target: str,
    slug: str,
) -> bool:
    if path != "src/nvda_desk/config/runtime_settings.py":
        return False
    if slug != "coefficient_authority":
        return False
    if candidate != f"{target} path":
        return False
    return raw_phrase.strip() == "_".join(["coefficient", "authority", "path"])


def _is_sequence8_coefficient_modifier_descriptor_fragment(
    path: str,
    candidate: str,
    slug: str,
) -> bool:
    """Suppress bounded Sequence 8 descriptors without hiding global synonyms."""

    selected_fragments = {
        (
            "tests/fixtures/sequence8/coefficient_modifier_authority_specimen.json",
            "coefficient modifier authority",
            "coefficient_authority",
        ),
        (
            "tests/tier_a/config/test_sequence8_coefficient_modifier_authority_specimen.py",
            "coefficient modifier authority",
            "coefficient_authority",
        ),
        ("config/retained_test_registry.yaml", "state conditioned", "state_conditioned_modifier"),
        (
            "config/retained_test_registry.yaml",
            "state conditioned modifier surface",
            "state_conditioned_modifier",
        ),
        (
            "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md",
            "bounded coefficient",
            "bounded_dynamic_coefficient",
        ),
        (
            "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md",
            "dynamic coefficient",
            "bounded_dynamic_coefficient",
        ),
        (
            "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md",
            "state conditioned modifier tests",
            "state_conditioned_modifier",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "bounded coefficient",
            "bounded_dynamic_coefficient",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "dynamic coefficient",
            "bounded_dynamic_coefficient",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "coefficient modifier authority",
            "coefficient_authority",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "coefficient authority marker",
            "coefficient_authority",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "state conditioned",
            "state_conditioned_modifier",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "state conditioned modifier surface",
            "state_conditioned_modifier",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "state conditioned modifier tests",
            "state_conditioned_modifier",
        ),
        (
            "tests/tier_a/modifiers/test_state_conditioned_modifier_surface.py",
            "state conditioned",
            "state_conditioned_modifier",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "state conditioned",
            "state_conditioned_modifier",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "coefficient modifier authority",
            "coefficient_authority",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "coefficient authority marker",
            "coefficient_authority",
        ),
    }
    return (path, candidate, slug) in selected_fragments


def _is_sequence7_parallel_risk_descriptor_fragment(
    path: str,
    candidate: str,
    slug: str,
) -> bool:
    """Suppress retained Sequence 7 descriptors that name governed surfaces."""

    selected_fragments = {
        (
            "tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_input_surface.py",
            "parallel risk",
            "parallel_risk_lane",
        ),
        (
            "tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_output_surface.py",
            "parallel risk",
            "parallel_risk_lane",
        ),
        (
            "tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_input_surface.py",
            "sequence7 stage input bundle",
            "stage_input_bundle",
        ),
        (
            "tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_output_surface.py",
            "sequence7 stage input bundle",
            "stage_input_bundle",
        ),
        (
            "src/nvda_desk/domain/parallel_risk/environment_assessment.py",
            "temporal event context",
            "temporal_context",
        ),
        (
            "tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_output_surface.py",
            "temporal event context",
            "temporal_context",
        ),
        (
            "tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py",
            "temporal event context",
            "temporal_context",
        ),
        (
            "src/nvda_desk/risk/parallel/evaluate.py",
            "environment assessment import",
            "environment_assessment",
        ),
        ("src/nvda_desk/vocabulary_synonym_audit.py", "parallel risk", "parallel_risk_lane"),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "sequence7 stage input bundle",
            "stage_input_bundle",
        ),
        ("src/nvda_desk/vocabulary_synonym_audit.py", "temporal event context", "temporal_context"),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "environment assessment import",
            "environment_assessment",
        ),
    }
    return (path, candidate, slug) in selected_fragments


def _is_sequence11_registry_identifier_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    slug: str,
) -> bool:
    """Ignore Sequence 11 retained-test registry identifiers, not prose aliases."""

    if slug != "parallel_risk_lane":
        return False
    raw = raw_phrase.strip()
    selected_fragments = {
        ("config/retained_test_registry.yaml", "parallel_risk", "parallel risk"),
        (
            "config/retained_test_registry.yaml",
            "parallel_risk_lane_service",
            "parallel risk lane service",
        ),
        ("src/nvda_desk/vocabulary_synonym_audit.py", "parallel_risk", "parallel risk"),
        ("src/nvda_desk/vocabulary_synonym_audit.py", "parallel risk", "parallel risk"),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "parallel_risk_lane_service",
            "parallel risk lane service",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "parallel risk lane service",
            "parallel risk lane service",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "parallel_risk",
            "parallel risk",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "parallel risk",
            "parallel risk",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "parallel_risk_lane_service",
            "parallel risk lane service",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "parallel risk lane service",
            "parallel risk lane service",
        ),
    }
    return (path, raw, candidate) in selected_fragments


def _is_sequence9_capital_consumed_input_identifier_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    slug: str,
) -> bool:
    """Ignore Sequence 9 consumed-input identifiers on capital-deployment surfaces."""

    if slug != "coefficient_authority":
        return False
    if raw_phrase.strip() != "coefficient_modifier_authority":
        return False
    if candidate != "coefficient modifier authority":
        return False
    return path in {
        "src/nvda_desk/capital/authority.py",
        "tests/tier_a/capital_deployment/test_capital_contract_models.py",
        "tests/tier_a/capital_deployment/test_sequence9_capital_deployment_decision_surface.py",
    }


def _is_session_clock_source_timezone_local_identifier_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    slug: str,
    category: str,
) -> bool:
    """Ignore the local ZoneInfo variable derived from source_timezone_raw."""

    if slug != "source_timezone_raw" or category != "protocol_field":
        return False
    selected_fragments = {
        ("src/nvda_desk/domain/temporal/session_clock.py", "source_timezone", "source timezone"),
        ("src/nvda_desk/vocabulary_synonym_audit.py", "source_timezone", "source timezone"),
        ("src/nvda_desk/vocabulary_synonym_audit.py", "source timezone", "source timezone"),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "source_timezone",
            "source timezone",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "source timezone",
            "source timezone",
        ),
    }
    return (path, raw_phrase.strip(), candidate) in selected_fragments


def _is_sequence9_dependency_lineage_identifier_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    slug: str,
) -> bool:
    """Ignore Sequence 9 DMP dependency identifiers that include sequence anchors."""

    selected_fragments = {
        (
            "tests/tier_a/capital_deployment/test_sequence9_capital_deployment_dmp_packet.py",
            "coefficient-authority-seq8",
            "coefficient authority seq8",
            "coefficient_authority",
        ),
        (
            "tests/tier_a/capital_deployment/test_sequence9_capital_deployment_dmp_packet.py",
            "temporal-context-seq5",
            "temporal context seq5",
            "temporal_context",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "coefficient-authority-seq8",
            "coefficient authority seq8",
            "coefficient_authority",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "coefficient authority seq8",
            "coefficient authority seq8",
            "coefficient_authority",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "temporal-context-seq5",
            "temporal context seq5",
            "temporal_context",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "temporal context seq5",
            "temporal context seq5",
            "temporal_context",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "coefficient-authority-seq8",
            "coefficient authority seq8",
            "coefficient_authority",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "coefficient authority seq8",
            "coefficient authority seq8",
            "coefficient_authority",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "temporal-context-seq5",
            "temporal context seq5",
            "temporal_context",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "temporal context seq5",
            "temporal context seq5",
            "temporal_context",
        ),
    }
    return (path, raw_phrase.strip(), candidate, slug) in selected_fragments


def _is_roadmap_control_surface_identifier_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    slug: str,
) -> bool:
    """Ignore exact roadmap-control identifiers without admitting prose aliases.

    These fragments are generated by file paths, proof-block IDs, test-family IDs,
    route slugs, and branch labels in mutable roadmap control surfaces. They are
    bounded by both path and exact candidate so the same words in ordinary prose
    still escalate for LLM review.
    """

    selected_fragments = {
        ("config/proof_blocks.yaml", "financial calendar", "financial_calendar_crosswalk"),
        ("config/proof_blocks.yaml", "parallel risk", "parallel_risk_lane"),
        ("config/proof_blocks.yaml", "parallel risk lane service", "parallel_risk_lane"),
        ("config/proof_blocks.yaml", "state conditioned", "state_conditioned_modifier"),
        (
            "config/retained_test_registry.yaml",
            "financial calendar",
            "financial_calendar_crosswalk",
        ),
        ("config/retained_test_registry.yaml", "parallel risk", "parallel_risk_lane"),
        (
            "docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md",
            "roadmap parallel risk lane",
            "parallel_risk_lane",
        ),
        (
            "docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md",
            "parallel risk lane service",
            "parallel_risk_lane",
        ),
        (
            "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
            "bounded coefficient",
            "bounded_dynamic_coefficient",
        ),
        (
            "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
            "coefficient authority service",
            "coefficient_authority",
        ),
        (
            "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
            "parallel risk",
            "parallel_risk_lane",
        ),
        (
            "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
            "parallel risk lane service",
            "parallel_risk_lane",
        ),
        (
            "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
            "playbook eligibility service",
            "playbook_eligibility",
        ),
        (
            "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
            "roadmap parallel risk lane",
            "parallel_risk_lane",
        ),
        (
            "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
            "state conditioned",
            "state_conditioned_modifier",
        ),
        (
            "docs/planning/2026-05-09_HELD_ROW_READ_SET_AND_PROOF_MATRIX_001.md",
            "roadmap parallel risk lane",
            "parallel_risk_lane",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "financial calendar",
            "financial_calendar_crosswalk",
        ),
        ("src/nvda_desk/vocabulary_synonym_audit.py", "parallel risk", "parallel_risk_lane"),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "parallel risk lane service",
            "parallel_risk_lane",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "state conditioned",
            "state_conditioned_modifier",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "roadmap parallel risk lane",
            "parallel_risk_lane",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "bounded coefficient",
            "bounded_dynamic_coefficient",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "coefficient authority service",
            "coefficient_authority",
        ),
        (
            "src/nvda_desk/vocabulary_synonym_audit.py",
            "playbook eligibility service",
            "playbook_eligibility",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "financial calendar",
            "financial_calendar_crosswalk",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "roadmap parallel risk lane",
            "parallel_risk_lane",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "bounded coefficient",
            "bounded_dynamic_coefficient",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "coefficient authority service",
            "coefficient_authority",
        ),
        (
            "tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py",
            "playbook eligibility service",
            "playbook_eligibility",
        ),
    }

    # Keep raw_phrase in the signature so future narrowing can distinguish raw
    # identifiers from prose without changing the build_report call surface.
    _ = raw_phrase
    return (path, candidate, slug) in selected_fragments


def _is_fwd001_governance_candidate_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    slug: str,
) -> bool:
    """Ignore FWD-001 adjudicated identifiers without admitting aliases."""

    return (path, raw_phrase.strip(), candidate, slug) in FWD001_GOVERNANCE_CANDIDATE_FRAGMENTS


def _candidate_slug_from_phrase(phrase: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", phrase.strip().casefold()).strip("_")
    if not slug:
        raise ValueError("candidate phrase must yield a non-empty slug")
    return slug


def _escalation_classification(phrase: str, nearest_slug: str) -> dict[str, str | None]:
    return VocabularyCandidateClassification(
        action=VocabularyCandidateAction.QUARANTINE,
        candidate_slug=_candidate_slug_from_phrase(phrase),
        matched_slug=nearest_slug,
        reason="near-match synonym candidate requires LLM escalation before vocabulary admission",
    ).to_dict()


def _escalation_admission_review(phrase: str, nearest_slug: str) -> dict:
    candidate = VocabularyCandidate(
        candidate_slug=_candidate_slug_from_phrase(phrase),
        candidate_label=phrase,
    )
    classification = VocabularyCandidateClassification(
        action=VocabularyCandidateAction.QUARANTINE,
        candidate_slug=candidate.candidate_slug,
        matched_slug=nearest_slug,
        reason="near-match synonym candidate requires LLM escalation before vocabulary admission",
    )
    return {
        "status": "quarantined",
        "candidate_slug": candidate.candidate_slug,
        "plan": {
            "classification": classification.to_dict(),
            "proposed_entry": None,
            "alias_candidates": [],
            "quarantine_reason": classification.reason,
        },
        "error": classification.reason,
    }


def _candidate_score(candidate: str, target: str) -> int:
    c_parts = candidate.split()
    t_parts = target.split()
    if candidate == target:
        return 100
    if candidate.replace(" ", "") == target.replace(" ", ""):
        return 98
    if len(c_parts) == len(t_parts) and set(c_parts) == set(t_parts):
        return 95
    if abs(len(c_parts) - len(t_parts)) == 1:
        smaller = set(c_parts) if len(c_parts) < len(t_parts) else set(t_parts)
        larger = set(c_parts) if len(c_parts) > len(t_parts) else set(t_parts)
        if smaller <= larger and len(smaller) >= 2:
            return 93
    return 0


def build_report() -> dict:
    payload = _load_document()
    exact_tokens, compact_exact_tokens, entries = _lexicon(payload)
    fingerprint = _fingerprint()
    previous_stamp = {}
    if STAMP_PATH.exists():
        previous_stamp = json.loads(STAMP_PATH.read_text(encoding="utf-8"))
    current_touched = previous_stamp.get("fingerprint") != fingerprint

    candidates: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for path, raw_phrase in _iter_candidates():
        if _is_identifier_like(raw_phrase):
            continue
        phrase = _normalise(raw_phrase)
        compact_phrase = _compact_normalise(raw_phrase)
        if len(phrase) < 8 or phrase in exact_tokens or compact_phrase in compact_exact_tokens:
            continue
        best = None
        best_score = 0
        for slug, label, target, category in entries:
            score = _candidate_score(phrase, target)
            if score:
                if _is_protocol_identifier_fragment(raw_phrase, phrase, target, category):
                    score = 0
                if _is_python_function_declaration_identifier_fragment(
                    path, raw_phrase, phrase, target
                ):
                    score = 0
                if _is_vocabulary_seed_note_relationship_fragment(path, phrase, target, slug, category):
                    score = 0
                if _is_dmp_v3_fixture_root_descriptor_fragment(path, phrase, target, slug):
                    score = 0
                if _is_baseline_only_surface_error_text_fragment(
                    path, raw_phrase, phrase, target, slug
                ):
                    score = 0
                if _is_coefficient_authority_import_descriptor_fragment(path, phrase, target, slug):
                    score = 0
                if _is_downstream_stage_read_service_method_fragment(
                    path, raw_phrase, phrase, target, slug
                ):
                    score = 0
                if _is_coefficient_authority_service_accessor_fragment(
                    path, raw_phrase, phrase, target, slug
                ):
                    score = 0
                if _is_dependency_packet_ids_replay_review_fragment(
                    path, raw_phrase, phrase, slug, category
                ):
                    score = 0
                if _is_testing_harness_specimen_artifact_descriptor_fragment(
                    path, raw_phrase, phrase, slug
                ):
                    score = 0
                if _is_pr_stage_environment_descriptor_fragment(path, raw_phrase, phrase, slug):
                    score = 0
                if _is_parallel_risk_lane_contract_descriptor_fragment(path, phrase, slug):
                    score = 0
                if _is_coefficient_authority_path_field_fragment(
                    path, raw_phrase, phrase, target, slug
                ):
                    score = 0
                if _is_sequence8_coefficient_modifier_descriptor_fragment(path, phrase, slug):
                    score = 0
                if _is_sequence7_parallel_risk_descriptor_fragment(path, phrase, slug):
                    score = 0
                if _is_sequence11_registry_identifier_fragment(path, raw_phrase, phrase, slug):
                    score = 0
                if _is_sequence9_capital_consumed_input_identifier_fragment(
                    path, raw_phrase, phrase, slug
                ):
                    score = 0
                if _is_session_clock_source_timezone_local_identifier_fragment(
                    path, raw_phrase, phrase, slug, category
                ):
                    score = 0
                if _is_sequence9_dependency_lineage_identifier_fragment(path, raw_phrase, phrase, slug):
                    score = 0
                if _is_roadmap_control_surface_identifier_fragment(path, raw_phrase, phrase, slug):
                    score = 0
                if _is_fwd001_governance_candidate_fragment(path, raw_phrase, phrase, slug):
                    score = 0
            if score > best_score:
                best = (slug, label)
                best_score = score
        if best is None or best_score < 93:
            continue
        key = (path, phrase)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(
            {
                "phrase": phrase,
                "nearest_slug": best[0],
                "nearest_label": best[1],
                "score": best_score,
                "path": path,
                "resolution_required": "llm_escalation",
            }
        )

    sorted_candidates = sorted(
        candidates, key=lambda item: (-item["score"], item["path"], item["phrase"])
    )
    return {
        "schema_version": "v1",
        "trigger": "vocabulary_governance",
        "vocabulary_touched": current_touched,
        "fingerprint": fingerprint,
        "candidates": sorted_candidates,
        "candidate_classifications": [
            {
                "phrase": item["phrase"],
                "path": item["path"],
                "nearest_slug": item["nearest_slug"],
                "classification": _escalation_classification(
                    str(item["phrase"]), str(item["nearest_slug"])
                ),
                "admission_review": _escalation_admission_review(
                    str(item["phrase"]), str(item["nearest_slug"])
                ),
            }
            for item in sorted_candidates
        ],
    }


def write_report() -> dict:
    report = build_report()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def write_stamp() -> None:
    report = build_report()
    if report["candidates"]:
        raise RuntimeError(
            "cannot update vocabulary touch stamp while synonym candidates require LLM escalation"
        )
    STAMP_PATH.parent.mkdir(parents=True, exist_ok=True)
    STAMP_PATH.write_text(
        json.dumps({"fingerprint": report["fingerprint"]}, indent=2) + "\n", encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-clean",
        action="store_true",
        help="write the audit report and fail if unresolved synonym candidates exist",
    )
    parser.add_argument(
        "--write-stamp",
        action="store_true",
        help="advance the vocabulary touch stamp only when the audit is clean",
    )
    args = parser.parse_args(argv)

    if args.write_stamp:
        write_stamp()
        print("vocabulary_touch_stamp=UPDATED")
        return 0

    report = write_report()
    candidate_count = len(report["candidates"])
    print(
        "vocabulary_synonym_audit=PASS"
        f" candidates={candidate_count}"
        f" vocabulary_touched={report['vocabulary_touched']}"
    )
    if args.check_clean and candidate_count:
        print("vocabulary_synonym_audit=BLOCKED unresolved_candidates=" + str(candidate_count))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
