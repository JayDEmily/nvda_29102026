from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.vocabulary_synonym_audit import write_report


def test_vocabulary_synonym_audit_cli_bootstraps_src_import_path_without_env() -> None:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)

    completed = subprocess.run(
        [sys.executable, "scripts/vocabulary_synonym_audit.py", "--check-clean"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )

    assert completed.returncode == 0, completed.stderr
    assert "vocabulary_synonym_audit=PASS candidates=0" in completed.stdout


@pytest.mark.vocabulary_governance
def test_vocabulary_synonym_candidate_audit_writes_escalation_artefact_when_touched() -> None:
    report = write_report()
    report_path = Path("var/vocabulary/synonym_candidates.json")
    assert report_path.exists()

    committed = json.loads(report_path.read_text(encoding="utf-8"))
    assert committed == report
    assert committed["trigger"] == "vocabulary_governance"
    assert "candidate_classifications" in committed
    assert len(committed["candidate_classifications"]) == len(committed["candidates"])

    if committed["vocabulary_touched"] and committed["candidates"]:
        pytest.fail(
            "Vocabulary synonym candidates require LLM escalation. See var/vocabulary/synonym_candidates.json"
        )


def test_write_stamp_refuses_to_advance_when_escalation_candidates_exist(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    stamp_path = tmp_path / "vocabulary_touch_stamp.json"
    monkeypatch.setattr(audit, "STAMP_PATH", stamp_path)
    monkeypatch.setattr(
        audit,
        "build_report",
        lambda: {
            "fingerprint": "blocked",
            "candidates": [
                {
                    "phrase": "near alpha marker",
                    "nearest_slug": "nearalpha",
                    "nearest_label": "near alpha",
                    "score": 93,
                    "path": "src/example.py",
                    "resolution_required": "llm_escalation",
                }
            ],
        },
    )

    with pytest.raises(RuntimeError, match="cannot update vocabulary touch stamp"):
        audit.write_stamp()

    assert not stamp_path.exists()


def test_write_stamp_advances_only_after_clean_candidate_report(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    stamp_path = tmp_path / "vocabulary_touch_stamp.json"
    monkeypatch.setattr(audit, "STAMP_PATH", stamp_path)
    monkeypatch.setattr(
        audit,
        "build_report",
        lambda: {"fingerprint": "clean", "candidates": []},
    )

    audit.write_stamp()

    assert json.loads(stamp_path.read_text(encoding="utf-8")) == {"fingerprint": "clean"}


def _vocabulary_payload(entries: list[dict]) -> dict:
    return {"entries": entries}


def _expected_escalation_candidate(
    *, phrase: str, nearest_slug: str, nearest_label: str, score: int, path: str
) -> dict:
    return {
        "phrase": phrase,
        "nearest_slug": nearest_slug,
        "nearest_label": nearest_label,
        "score": score,
        "path": path,
        "resolution_required": "llm_escalation",
    }


def _entry(slug: str, label: str) -> dict:
    return {
        "canonical_slug": slug,
        "canonical_label": label,
        "allowed_aliases": [],
        "disallowed_phrases": [],
    }


def test_synonym_candidate_escalation_report_marks_near_match_as_quarantine(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload([_entry("nearalpha", "near alpha")]),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit, "_iter_candidates", lambda: iter([("src/example.py", "near alpha marker")])
    )

    report = audit.build_report()

    assert report["candidates"] == [
        _expected_escalation_candidate(
            phrase="near alpha marker",
            nearest_slug="nearalpha",
            nearest_label="near alpha",
            score=93,
            path="src/example.py",
        )
    ]
    assert report["candidate_classifications"] == [
        {
            "phrase": "near alpha marker",
            "path": "src/example.py",
            "nearest_slug": "nearalpha",
            "classification": {
                "action": "quarantine",
                "candidate_slug": "near_alpha_marker",
                "matched_slug": "nearalpha",
                "reason": "near-match synonym candidate requires LLM escalation before vocabulary admission",
            },
            "admission_review": {
                "status": "quarantined",
                "candidate_slug": "near_alpha_marker",
                "plan": {
                    "classification": {
                        "action": "quarantine",
                        "candidate_slug": "near_alpha_marker",
                        "matched_slug": "nearalpha",
                        "reason": "near-match synonym candidate requires LLM escalation before vocabulary admission",
                    },
                    "proposed_entry": None,
                    "alias_candidates": [],
                    "quarantine_reason": "near-match synonym candidate requires LLM escalation before vocabulary admission",
                },
                "error": "near-match synonym candidate requires LLM escalation before vocabulary admission",
            },
        }
    ]


def test_compact_tokenisation_variant_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload([_entry("scenarioid", "scenarioid")]),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit, "_iter_candidates", lambda: iter([("src/example.py", "scenario id")])
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_likely_synonym_candidate_is_not_globally_suppressed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload([_entry("contrivedzeta", "contrived zeta")]),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("src/example.py", "contrived zeta marker")]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        _expected_escalation_candidate(
            phrase="contrived zeta marker",
            nearest_slug="contrivedzeta",
            nearest_label="contrived zeta",
            score=93,
            path="src/example.py",
        )
    ]


def test_protocol_field_identifier_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "source_time_utc",
                    "canonical_label": "source_time_utc",
                    "category": "protocol_field",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                ("src/example.py", "return source_time_utc"),
                ("src/example.py", "source_time_utc"),
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_protocol_field_prose_variant_is_still_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "source_time_utc",
                    "canonical_label": "source_time_utc",
                    "category": "protocol_field",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    phrase = "source " + "time " + "utc marker"
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("src/example.py", phrase)]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        _expected_escalation_candidate(
            phrase=phrase,
            nearest_slug="source_time_utc",
            nearest_label="source_time_utc",
            score=93,
            path="src/example.py",
        )
    ]


def test_python_function_declaration_identifier_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "financial_calendar_crosswalk",
                    "canonical_label": "Financial Calendar Crosswalk",
                    "category": "reference_data",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("src/example.py", "def financial_calendar_crosswalk")]),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_python_function_declaration_prose_variant_is_still_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "financial_calendar_crosswalk",
                    "canonical_label": "Financial Calendar Crosswalk",
                    "category": "reference_data",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    phrase = "def " + "financial " + "calendar " + "crosswalk"
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("src/example.py", phrase)]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        _expected_escalation_candidate(
            phrase=phrase,
            nearest_slug="financial_calendar_crosswalk",
            nearest_label="Financial Calendar Crosswalk",
            score=93,
            path="src/example.py",
        )
    ]


def test_vocabulary_seed_note_relationship_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "source_temporal_standard",
                    "canonical_label": "Source Temporal Standard",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    phrase = " ".join(["Source", "temporal", "standard", "field"])
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                (
                    "src/nvda_desk/vocabulary_builder.py",
                    phrase,
                )
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_vocabulary_seed_note_relationship_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "source_temporal_standard",
                    "canonical_label": "Source Temporal Standard",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    phrase = " ".join(["Source", "temporal", "standard", "field"])
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", phrase)]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": phrase.casefold(),
            "nearest_slug": "source_temporal_standard",
            "nearest_label": "Source Temporal Standard",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_dmp_v3_fixture_root_descriptor_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "dmp_v3",
                    "canonical_label": "DMP V3",
                    "category": "protocol_contract",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                (
                    "src/nvda_desk/testing/harnesses/canonical_runtime.py",
                    "_".join(["dmp", "v3", "root"]),
                )
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_dmp_v3_fixture_root_descriptor_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "dmp_v3",
                    "canonical_label": "DMP V3",
                    "category": "protocol_contract",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", "_".join(["dmp", "v3", "root"]))]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": " ".join(["dmp", "v3", "root"]),
            "nearest_slug": "dmp_v3",
            "nearest_label": "DMP V3",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_baseline_only_surface_error_text_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "baseline_only_surface",
                    "canonical_label": "Baseline-only Surface",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                (
                    "src/nvda_desk/contracts/coefficient_authority.py",
                    "-".join(["baseline", "only"])
                    + " "
                    + "surface cannot be marked runtime_mutable",
                )
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_baseline_only_surface_error_text_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "baseline_only_surface",
                    "canonical_label": "Baseline-only Surface",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", "-".join(["baseline", "only"]) + " surface marker")]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": " ".join(["baseline", "only", "surface", "marker"]),
            "nearest_slug": "baseline_only_surface",
            "nearest_label": "Baseline-only Surface",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_coefficient_authority_import_descriptor_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "coefficient_authority",
                    "canonical_label": "Coefficient Authority",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                (
                    "src/nvda_desk/config/__init__.py",
                    "_".join(["coefficient", "authority"]) + " import",
                ),
                (
                    "src/nvda_desk/config/" + "_".join(["coefficient", "authority"]) + ".py",
                    "_".join(["coefficient", "authority"]) + " import",
                ),
                (
                    "src/nvda_desk/services/"
                    + "_".join(["coefficient", "authority"])
                    + "_service.py",
                    "_".join(["coefficient", "authority"]) + " import",
                ),
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_coefficient_authority_import_descriptor_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "coefficient_authority",
                    "canonical_label": "Coefficient Authority",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", "_".join(["coefficient", "authority"]) + " import")]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": " ".join(["coefficient", "authority", "import"]),
            "nearest_slug": "coefficient_authority",
            "nearest_label": "Coefficient Authority",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_downstream_stage_read_service_method_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "stage_read_state",
                    "canonical_label": "Stage-read State",
                    "category": "parallel_risk_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [("src/nvda_desk/services/downstream_state_service.py", "_".join(["read", "state"]))]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_downstream_stage_read_service_method_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "stage_read_state",
                    "canonical_label": "Stage-read State",
                    "category": "parallel_risk_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit, "_iter_candidates", lambda: iter([("docs/example.md", "_".join(["read", "state"]))])
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": " ".join(["read", "state"]),
            "nearest_slug": "stage_read_state",
            "nearest_label": "Stage-read State",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_coefficient_authority_service_accessor_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "coefficient_authority",
                    "canonical_label": "Coefficient Authority",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                (
                    "src/nvda_desk/cognition/modifiers/state_conditioned.py",
                    "_".join(["coefficient", "authority", "service"]),
                ),
                (
                    "src/nvda_desk/config/config_surface.py",
                    "_".join(["coefficient", "authority", "service"]),
                ),
                (
                    "src/nvda_desk/services/posture_service.py",
                    "_".join(["coefficient", "authority", "service"]),
                ),
                (
                    "src/nvda_desk/services/"
                    + "_".join(["coefficient", "authority"])
                    + "_service.py",
                    "_".join(["coefficient", "authority", "service"]),
                ),
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_coefficient_authority_service_accessor_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "coefficient_authority",
                    "canonical_label": "Coefficient Authority",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", "_".join(["coefficient", "authority", "service"]))]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": " ".join(["coefficient", "authority", "service"]),
            "nearest_slug": "coefficient_authority",
            "nearest_label": "Coefficient Authority",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_dependency_packet_ids_replay_review_identifier_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "dependency_packet_ids",
                    "canonical_label": "Dependency Packet IDs",
                    "category": "protocol_field",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    packet_identifier = "_".join(["packet", "ids"])
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                ("src/nvda_desk/analysis/replay/service.py", packet_identifier),
                ("src/nvda_desk/contracts/replay.py", packet_identifier),
                ("src/nvda_desk/contracts/review.py", packet_identifier),
                ("src/nvda_desk/services/review_explanation_service.py", packet_identifier),
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_dependency_packet_ids_replay_review_identifier_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "dependency_packet_ids",
                    "canonical_label": "Dependency Packet IDs",
                    "category": "protocol_field",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    packet_identifier = "_".join(["packet", "ids"])
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                (
                    "docs/example.md",
                    packet_identifier,
                )
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": " ".join(["packet", "ids"]),
            "nearest_slug": "dependency_packet_ids",
            "nearest_label": "Dependency Packet IDs",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_parallel_risk_lane_contract_descriptor_fragments_are_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    slug_parts = ["parallel", "risk", "lane"]
    module_slug = "_".join(slug_parts)
    contract_module = "_".join(slug_parts[:2])
    two_part = "_".join(slug_parts[:2])
    dataschema_identifier = "_".join([*slug_parts, "dataschema"])
    packet_identifier = "_".join([*slug_parts, "packet"])

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": module_slug,
                    "canonical_label": " ".join(part.title() for part in slug_parts),
                    "category": "parallel_risk_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                ("src/nvda_desk/contracts/__init__.py", two_part),
                (f"src/nvda_desk/contracts/{contract_module}.py", two_part),
                (f"src/nvda_desk/contracts/{contract_module}.py", dataschema_identifier),
                (
                    f"src/nvda_desk/persistence/{contract_module}_observations.py",
                    dataschema_identifier,
                ),
                ("src/nvda_desk/risk/parallel/evaluate.py", two_part),
                (f"src/nvda_desk/services/{module_slug}_service.py", two_part),
                (
                    f"src/nvda_desk/testing/harnesses/serial_runtime_{contract_module}_boundary_specimen.py",
                    packet_identifier,
                ),
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_parallel_risk_lane_contract_descriptor_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    slug_parts = ["parallel", "risk", "lane"]
    module_slug = "_".join(slug_parts)
    label = " ".join(part.title() for part in slug_parts)
    phrase = "_".join([*slug_parts, "packet"])
    normalised_phrase = " ".join([*slug_parts, "packet"])

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": module_slug,
                    "canonical_label": label,
                    "category": "parallel_risk_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", phrase)]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": normalised_phrase,
            "nearest_slug": module_slug,
            "nearest_label": label,
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_dependency_packet_ids_harness_fixture_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "dependency_packet_ids",
                    "canonical_label": "Dependency Packet IDs",
                    "category": "protocol_field",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    packet_identifier = "_".join(["packet", "ids"])
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                (
                    "src/nvda_desk/testing/harnesses/canonical_runtime.py",
                    packet_identifier,
                )
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_dependency_packet_ids_harness_fixture_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "dependency_packet_ids",
                    "canonical_label": "Dependency Packet IDs",
                    "category": "protocol_field",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    packet_identifier = "_".join(["packet", "ids"])
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", packet_identifier)]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": " ".join(["packet", "ids"]),
            "nearest_slug": "dependency_packet_ids",
            "nearest_label": "Dependency Packet IDs",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_testing_harness_specimen_artifact_descriptor_fragments_are_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "append_only_observation_record",
                    "canonical_label": "Append-only Observation Record",
                    "category": "parallel_risk_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
                {
                    "canonical_slug": "stage_input_bundle",
                    "canonical_label": "Stage Input Bundle",
                    "category": "protocol_contract",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    module_8_specimen = (
        "src/nvda_desk/testing/harnesses/" "module_8_parallel_risk_workbook_specimen.py"
    )
    serial_boundary_specimen = (
        "src/nvda_desk/testing/harnesses/" "serial_runtime_parallel_risk_boundary_specimen.py"
    )
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                (
                    module_8_specimen,
                    "_".join(["append", "only", "observation", "record", "json"]),
                ),
                (module_8_specimen, "_".join(["stage", "input", "bundle", "json"])),
                (
                    serial_boundary_specimen,
                    "_".join(["specimen", "stage", "input", "bundle"]),
                ),
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_testing_harness_specimen_artifact_descriptor_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "stage_input_bundle",
                    "canonical_label": "Stage Input Bundle",
                    "category": "protocol_contract",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    phrase = "_".join(["stage", "input", "bundle", "json"])
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", phrase)]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": " ".join(["stage", "input", "bundle", "json"]),
            "nearest_slug": "stage_input_bundle",
            "nearest_label": "Stage Input Bundle",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_pr_stage_environment_descriptor_fragments_are_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "stage_read_state",
                    "canonical_label": "Stage-read State",
                    "category": "_".join(["parallel", "risk", "surface"]),
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
                {
                    "canonical_slug": "environment_assessment",
                    "canonical_label": "Environment Assessment",
                    "category": "_".join(["parallel", "risk", "surface"]),
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    contract_module = "_".join(["parallel", "risk"])
    contract_path = f"src/nvda_desk/contracts/{contract_module}.py"
    domain_path = f"src/nvda_desk/domain/{contract_module}/environment_assessment.py"
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                (
                    contract_path,
                    "_".join(["bootstrap", "stage", "read", "state"]),
                ),
                (
                    contract_path,
                    "_".join(["bounded", "environment", "assessment"]),
                ),
                (
                    contract_path,
                    "_".join(["environment", "assessment", "only"]),
                ),
                (
                    domain_path,
                    "_".join(["environment", "assessment", "only"]),
                ),
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_pr_stage_environment_descriptor_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "environment_assessment",
                    "canonical_label": "Environment Assessment",
                    "category": "_".join(["parallel", "risk", "surface"]),
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    phrase = "_".join(["environment", "assessment", "only"])
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", phrase)]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": " ".join(["environment", "assessment", "only"]),
            "nearest_slug": "environment_assessment",
            "nearest_label": "Environment Assessment",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_coefficient_authority_path_field_fragment_is_not_escalated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "coefficient_authority",
                    "canonical_label": "Coefficient Authority",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    phrase = "_".join(["coefficient", "authority", "path"])
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("src/nvda_desk/config/runtime_settings.py", phrase)]),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_coefficient_authority_path_field_fragment_is_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "coefficient_authority",
                    "canonical_label": "Coefficient Authority",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    phrase = "_".join(["coefficient", "authority", "path"])
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", phrase)]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": " ".join(["coefficient", "authority", "path"]),
            "nearest_slug": "coefficient_authority",
            "nearest_label": "Coefficient Authority",
            "score": 93,
            "path": "docs/example.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_sequence8_descriptor_fragments_are_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "state_conditioned_modifier",
                    "canonical_label": "State-conditioned Modifier",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
                {
                    "canonical_slug": "coefficient_authority",
                    "canonical_label": "Coefficient Authority",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                ("config/retained_test_registry.yaml", "state conditioned"),
                (
                    "tests/fixtures/sequence8/coefficient_modifier_authority_specimen.json",
                    "coefficient modifier authority",
                ),
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_sequence8_descriptor_fragments_do_not_globally_hide_synonyms(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "coefficient_authority",
                    "canonical_label": "Coefficient Authority",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                }
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/random.md", "coefficient authority marker")]),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": "coefficient authority marker",
            "nearest_slug": "coefficient_authority",
            "nearest_label": "Coefficient Authority",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        }
    ]


def test_sequence11_part45_identifier_fragments_are_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "parallel_risk_lane",
                    "canonical_label": "Parallel Risk Lane",
                    "category": "workflow",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
                {
                    "canonical_slug": "coefficient_authority",
                    "canonical_label": "Coefficient Authority",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
                {
                    "canonical_slug": "source_timezone_raw",
                    "canonical_label": "source_timezone_raw",
                    "category": "protocol_field",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
                {
                    "canonical_slug": "temporal_context",
                    "canonical_label": "Temporal Context",
                    "category": "stage",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                ("config/retained_test_registry.yaml", "parallel_risk"),
                ("config/retained_test_registry.yaml", "parallel_risk_lane_service"),
                ("src/nvda_desk/capital/authority.py", "coefficient_modifier_authority"),
                (
                    "tests/tier_a/capital_deployment/test_capital_contract_models.py",
                    "coefficient_modifier_authority",
                ),
                (
                    "tests/tier_a/capital_deployment/test_sequence9_capital_deployment_decision_surface.py",
                    "coefficient_modifier_authority",
                ),
                ("src/nvda_desk/domain/temporal/session_clock.py", "source_timezone"),
                (
                    "tests/tier_a/capital_deployment/test_sequence9_capital_deployment_dmp_packet.py",
                    "coefficient-authority-seq8",
                ),
                (
                    "tests/tier_a/capital_deployment/test_sequence9_capital_deployment_dmp_packet.py",
                    "temporal-context-seq5",
                ),
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == []


def test_sequence11_part45_identifier_fragments_do_not_globally_hide_synonyms(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                {
                    "canonical_slug": "parallel_risk_lane",
                    "canonical_label": "Parallel Risk Lane",
                    "category": "workflow",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
                {
                    "canonical_slug": "coefficient_authority",
                    "canonical_label": "Coefficient Authority",
                    "category": "authority_surface",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
                {
                    "canonical_slug": "source_timezone_raw",
                    "canonical_label": "source_timezone_raw",
                    "category": "protocol_field",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
                {
                    "canonical_slug": "temporal_context",
                    "canonical_label": "Temporal Context",
                    "category": "stage",
                    "allowed_aliases": [],
                    "disallowed_phrases": [],
                },
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                ("docs/random.md", "parallel_risk"),
                ("docs/random.md", "parallel_risk_lane_service"),
                ("docs/random.md", "coefficient_modifier_authority"),
                ("docs/random.md", "source_timezone"),
                ("docs/random.md", "coefficient-authority-seq8"),
                ("docs/random.md", "temporal-context-seq5"),
            ]
        ),
    )

    report = audit.build_report()

    assert report["candidates"] == [
        {
            "phrase": "coefficient authority seq8",
            "nearest_slug": "coefficient_authority",
            "nearest_label": "Coefficient Authority",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "coefficient modifier authority",
            "nearest_slug": "coefficient_authority",
            "nearest_label": "Coefficient Authority",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "parallel risk",
            "nearest_slug": "parallel_risk_lane",
            "nearest_label": "Parallel Risk Lane",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "parallel risk lane service",
            "nearest_slug": "parallel_risk_lane",
            "nearest_label": "Parallel Risk Lane",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "source timezone",
            "nearest_slug": "source_timezone_raw",
            "nearest_label": "source_timezone_raw",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "temporal context seq5",
            "nearest_slug": "temporal_context",
            "nearest_label": "Temporal Context",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
    ]


def test_roadmap_control_surface_identifier_fragments_are_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                _entry("financial_calendar_crosswalk", "Financial Calendar Crosswalk"),
                _entry("parallel_risk_lane", "Parallel Risk Lane"),
                _entry("state_conditioned_modifier", "State-conditioned Modifier"),
                _entry("bounded_dynamic_coefficient", "Bounded Dynamic Coefficient"),
                _entry("coefficient_authority", "Coefficient Authority"),
                _entry("playbook_eligibility", "Playbook Eligibility"),
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                ("config/proof_blocks.yaml", "financial_calendar"),
                ("config/proof_blocks.yaml", "parallel_risk"),
                ("config/proof_blocks.yaml", "parallel_risk_lane_service"),
                ("config/proof_blocks.yaml", "state_conditioned"),
                ("config/retained_test_registry.yaml", "financial_calendar"),
                ("config/retained_test_registry.yaml", "parallel_risk"),
                (
                    "docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md",
                    "roadmap_parallel_risk_lane",
                ),
                (
                    "docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md",
                    "parallel_risk_lane_service",
                ),
                (
                    "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
                    "bounded coefficient",
                ),
                (
                    "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
                    "coefficient_authority_service",
                ),
                (
                    "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
                    "parallel risk",
                ),
                (
                    "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
                    "parallel_risk_lane_service",
                ),
                (
                    "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
                    "playbook_eligibility_service",
                ),
                (
                    "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
                    "roadmap_parallel_risk_lane",
                ),
                (
                    "docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md",
                    "state_conditioned",
                ),
                (
                    "docs/planning/2026-05-09_HELD_ROW_READ_SET_AND_PROOF_MATRIX_001.md",
                    "roadmap_parallel_risk_lane",
                ),
            ]
        ),
    )

    assert audit.build_report()["candidates"] == []


def test_roadmap_control_surface_identifier_fragments_do_not_globally_hide_synonyms(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                _entry("financial_calendar_crosswalk", "Financial Calendar Crosswalk"),
                _entry("parallel_risk_lane", "Parallel Risk Lane"),
                _entry("state_conditioned_modifier", "State-conditioned Modifier"),
                _entry("bounded_dynamic_coefficient", "Bounded Dynamic Coefficient"),
                _entry("coefficient_authority", "Coefficient Authority"),
                _entry("playbook_eligibility", "Playbook Eligibility"),
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                ("docs/random.md", "financial calendar"),
                ("docs/random.md", "parallel risk"),
                ("docs/random.md", "parallel_risk_lane_service"),
                ("docs/random.md", "state conditioned"),
                ("docs/random.md", "bounded coefficient"),
                ("docs/random.md", "coefficient_authority_service"),
                ("docs/random.md", "playbook_eligibility_service"),
            ]
        ),
    )

    assert audit.build_report()["candidates"] == [
        {
            "phrase": "bounded coefficient",
            "nearest_slug": "bounded_dynamic_coefficient",
            "nearest_label": "Bounded Dynamic Coefficient",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "coefficient authority service",
            "nearest_slug": "coefficient_authority",
            "nearest_label": "Coefficient Authority",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "financial calendar",
            "nearest_slug": "financial_calendar_crosswalk",
            "nearest_label": "Financial Calendar Crosswalk",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "parallel risk",
            "nearest_slug": "parallel_risk_lane",
            "nearest_label": "Parallel Risk Lane",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "parallel risk lane service",
            "nearest_slug": "parallel_risk_lane",
            "nearest_label": "Parallel Risk Lane",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "playbook eligibility service",
            "nearest_slug": "playbook_eligibility",
            "nearest_label": "Playbook Eligibility",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
        {
            "phrase": "state conditioned",
            "nearest_slug": "state_conditioned_modifier",
            "nearest_label": "State-conditioned Modifier",
            "score": 93,
            "path": "docs/random.md",
            "resolution_required": "llm_escalation",
        },
    ]


def test_fwd001_governance_candidate_fragments_are_path_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    def u(*parts: str) -> str:
        return "_".join(parts)

    def s(*parts: str) -> str:
        return " ".join(parts)

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                _entry("coefficient_authority", "Coefficient Authority"),
                _entry("source_temporal_standard", "Source Temporal Standard"),
                _entry("bounded_dynamic_coefficient", "Bounded Dynamic Coefficient"),
                _entry("playbook_eligibility", "Playbook Eligibility"),
                _entry("source_time_raw", "source_time_raw"),
                _entry("source_timezone_raw", "source_timezone_raw"),
                _entry("financial_calendar_crosswalk", "Financial Calendar Crosswalk"),
                _entry("parallel_risk_lane", "Parallel Risk Lane"),
                _entry("state_conditioned_modifier", "State-conditioned Modifier"),
                _entry("dependency_packet_ids", "Dependency Packet IDs"),
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                ("config/proof_blocks.yaml", u("coefficient", "authority", "service")),
                ("config/proof_blocks.yaml", u("source", "temporal", "standard", "surface")),
                (
                    "config/retained_test_registry.yaml",
                    u("coefficient", "authority", "service"),
                ),
                ("config/retained_test_registry.yaml", s("dynamic", "coefficient")),
                (
                    "config/retained_test_registry.yaml",
                    u("source", "temporal", "standard", "surface"),
                ),
                ("src/nvda_desk/contracts/playbook.py", u("playbook", "eligibility", "service")),
                ("src/nvda_desk/contracts/playbook.py", u("raw", "source")),
                (
                    "tests/tier_a/legacy_imported/test_imported_module_containment_surface.py",
                    u("financial", "calendar"),
                ),
                (
                    "tests/tier_a/legacy_imported/test_imported_module_containment_surface.py",
                    u("parallel", "risk"),
                ),
                (
                    "tests/tier_a/modifiers/test_dynamic_modifier_transform_boundary_surface.py",
                    u("coefficient", "authority", "service"),
                ),
                (
                    "tests/tier_a/modifiers/test_dynamic_modifier_transform_boundary_surface.py",
                    u("state", "conditioned"),
                ),
                (
                    "tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py",
                    u("parallel", "risk"),
                ),
                (
                    "tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py",
                    u("parallel", "risk", "lane", "service"),
                ),
                (
                    "tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py",
                    u("risk", "lane"),
                ),
                (
                    "tests/tier_a/playbook/test_playbook_transform_boundary_surface.py",
                    u("playbook", "eligibility", "service"),
                ),
                (
                    "tests/tier_a/review_runtime/test_review_explanation_service_surface.py",
                    u("packet", "ids"),
                ),
                (
                    "tests/tier_a/review_runtime/test_review_transform_boundary_surface.py",
                    u("packet", "ids"),
                ),
            ]
        ),
    )

    assert audit.build_report()["candidates"] == []


def test_fwd001_governance_candidate_fragments_do_not_globally_hide_synonyms(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    def s(*parts: str) -> str:
        return " ".join(parts)

    path = "docs/random.md"
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload(
            [
                _entry("coefficient_authority", "Coefficient Authority"),
                _entry("source_temporal_standard", "Source Temporal Standard"),
                _entry("bounded_dynamic_coefficient", "Bounded Dynamic Coefficient"),
                _entry("playbook_eligibility", "Playbook Eligibility"),
                _entry("source_time_raw", "source_time_raw"),
                _entry("source_timezone_raw", "source_timezone_raw"),
                _entry("financial_calendar_crosswalk", "Financial Calendar Crosswalk"),
                _entry("parallel_risk_lane", "Parallel Risk Lane"),
                _entry("state_conditioned_modifier", "State-conditioned Modifier"),
                _entry("dependency_packet_ids", "Dependency Packet IDs"),
            ]
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter(
            [
                (path, s("coefficient", "authority", "service")),
                (path, s("dynamic", "coefficient")),
                (path, s("financial", "calendar")),
                (path, s("packet", "ids")),
                (path, s("parallel", "risk")),
                (path, s("parallel", "risk", "lane", "service")),
                (path, s("playbook", "eligibility", "service")),
                (path, s("raw", "source")),
                (path, s("risk", "lane")),
                (path, s("source", "temporal", "standard", "surface")),
                (path, s("state", "conditioned")),
            ]
        ),
    )

    assert audit.build_report()["candidates"] == [
        _expected_escalation_candidate(
            phrase=s("coefficient", "authority", "service"),
            nearest_slug="coefficient_authority",
            nearest_label="Coefficient Authority",
            score=93,
            path=path,
        ),
        _expected_escalation_candidate(
            phrase=s("dynamic", "coefficient"),
            nearest_slug="bounded_dynamic_coefficient",
            nearest_label="Bounded Dynamic Coefficient",
            score=93,
            path=path,
        ),
        _expected_escalation_candidate(
            phrase=s("financial", "calendar"),
            nearest_slug="financial_calendar_crosswalk",
            nearest_label="Financial Calendar Crosswalk",
            score=93,
            path=path,
        ),
        _expected_escalation_candidate(
            phrase=s("packet", "ids"),
            nearest_slug="dependency_packet_ids",
            nearest_label="Dependency Packet IDs",
            score=93,
            path=path,
        ),
        _expected_escalation_candidate(
            phrase=s("parallel", "risk"),
            nearest_slug="parallel_risk_lane",
            nearest_label="Parallel Risk Lane",
            score=93,
            path=path,
        ),
        _expected_escalation_candidate(
            phrase=s("parallel", "risk", "lane", "service"),
            nearest_slug="parallel_risk_lane",
            nearest_label="Parallel Risk Lane",
            score=93,
            path=path,
        ),
        _expected_escalation_candidate(
            phrase=s("playbook", "eligibility", "service"),
            nearest_slug="playbook_eligibility",
            nearest_label="Playbook Eligibility",
            score=93,
            path=path,
        ),
        _expected_escalation_candidate(
            phrase=s("raw", "source"),
            nearest_slug="source_time_raw",
            nearest_label="source_time_raw",
            score=93,
            path=path,
        ),
        _expected_escalation_candidate(
            phrase=s("risk", "lane"),
            nearest_slug="parallel_risk_lane",
            nearest_label="Parallel Risk Lane",
            score=93,
            path=path,
        ),
        _expected_escalation_candidate(
            phrase=s("source", "temporal", "standard", "surface"),
            nearest_slug="source_temporal_standard",
            nearest_label="Source Temporal Standard",
            score=93,
            path=path,
        ),
        _expected_escalation_candidate(
            phrase=s("state", "conditioned"),
            nearest_slug="state_conditioned_modifier",
            nearest_label="State-conditioned Modifier",
            score=93,
            path=path,
        ),
    ]


def test_synonym_candidate_escalation_report_exposes_admission_review_shape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload([_entry("nearalpha", "near alpha")]),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit, "_iter_candidates", lambda: iter([("src/example.py", "near alpha marker")])
    )

    review = audit.build_report()["candidate_classifications"][0]["admission_review"]

    assert review["status"] == "quarantined"
    assert review["candidate_slug"] == "near_alpha_marker"
    assert review["plan"]["proposed_entry"] is None
    assert review["plan"]["alias_candidates"] == []
    assert review["error"] == (
        "near-match synonym candidate requires LLM escalation before vocabulary admission"
    )


def test_synonym_candidate_audit_check_clean_returns_nonzero_when_candidates_exist(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(audit, "OUTPUT_PATH", tmp_path / "synonym_candidates.json")
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload([_entry("nearalpha", "near alpha")]),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit, "_iter_candidates", lambda: iter([("src/example.py", "near alpha marker")])
    )

    status = audit.main(["--check-clean"])

    assert status == 1
    output = capsys.readouterr().out
    assert "vocabulary_synonym_audit=PASS candidates=1" in output
    assert "vocabulary_synonym_audit=BLOCKED unresolved_candidates=1" in output


def test_synonym_candidate_audit_check_clean_returns_zero_when_report_is_clean(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    monkeypatch.setattr(audit, "OUTPUT_PATH", tmp_path / "synonym_candidates.json")
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _vocabulary_payload([_entry("nearalpha", "near alpha")]),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(audit, "_iter_candidates", lambda: iter([]))

    status = audit.main(["--check-clean"])

    assert status == 0
    assert "vocabulary_synonym_audit=PASS candidates=0" in capsys.readouterr().out


def test_synonym_candidate_audit_write_stamp_mode_advances_clean_stamp(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from nvda_desk import vocabulary_synonym_audit as audit

    stamp_path = tmp_path / "vocabulary_touch_stamp.json"
    monkeypatch.setattr(audit, "STAMP_PATH", stamp_path)
    monkeypatch.setattr(
        audit,
        "build_report",
        lambda: {"fingerprint": "clean", "candidates": []},
    )

    status = audit.main(["--write-stamp"])

    assert status == 0
    assert json.loads(stamp_path.read_text(encoding="utf-8")) == {"fingerprint": "clean"}
    assert "vocabulary_touch_stamp=UPDATED" in capsys.readouterr().out
