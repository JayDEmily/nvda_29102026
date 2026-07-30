import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from nvda_desk import vocabulary_synonym_audit as audit


def _entry(
    slug: str,
    label: str,
    *,
    category: str = "stage",
    allowed_aliases: list[str] | None = None,
    disallowed_phrases: list[str] | None = None,
    namespace: str = "global",
) -> dict:
    return {
        "namespace": namespace,
        "canonical_id": f"{namespace}.{slug}",
        "canonical_slug": slug,
        "canonical_label": label,
        "category": category,
        "stage_owner": slug,
        "maps_to_contract": label.replace(" ", ""),
        "raw_or_derived": "not_applicable",
        "allowed_aliases": allowed_aliases or [],
        "disallowed_phrases": disallowed_phrases or [],
    }


def _payload(*entries: dict) -> dict:
    return {
        "schema_version": "v2_namespaced",
        "registry_version": "fixture",
        "notes": [],
        "namespaces": {
            "global": {
                "namespace": "global",
                "imports": [],
                "scan_paths": ["src", "tests", "docs", "config"],
            },
            "m04": {
                "namespace": "m04",
                "imports": ["global"],
                "scan_paths": ["m04_scope"],
            },
        },
        "entries": list(entries),
    }


def _candidate(
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


def _slug(*parts: str) -> str:
    return "_".join(parts)


def test_vocabulary_synonym_audit_cli_bootstraps_src_import_path_without_env_and_is_read_only():
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    governed_output = audit.OUTPUT_PATH
    before = governed_output.read_bytes() if governed_output.exists() else None

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/vocabulary_synonym_audit.py",
            "--namespace",
            "global",
            "--check-clean",
        ],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert "vocabulary_synonym_audit=PASS candidates=" in completed.stdout
    candidate_count = int(completed.stdout.split("candidates=", 1)[1].split()[0])
    assert completed.returncode == (1 if candidate_count else 0)
    if candidate_count:
        assert "vocabulary_synonym_audit=BLOCKED" in completed.stdout
    after = governed_output.read_bytes() if governed_output.exists() else None
    assert after == before


def test_vocabulary_synonym_candidate_audit_writes_escalation_artefact_when_touched(
    tmp_path, monkeypatch
):
    output_path = tmp_path / "synonym_candidates.json"
    stamp_path = tmp_path / "vocabulary_touch_stamp.json"
    stamp_path.write_text(json.dumps({"fingerprint": "old"}), encoding="utf-8")
    monkeypatch.setattr(audit, "OUTPUT_PATH", output_path)
    monkeypatch.setattr(audit, "STAMP_PATH", stamp_path)
    monkeypatch.setattr(audit, "_fingerprint", lambda: "new")
    phrase = " ".join(["Temporal", "Context", "draft"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context")),
    )
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", phrase)]),
    )

    report = audit.write_report()

    assert report["vocabulary_touched"] is True
    assert output_path.exists()
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["candidates"] == [
        _candidate(
            phrase=" ".join(["temporal", "context", "draft"]),
            nearest_slug="temporal_context",
            nearest_label="Temporal Context",
            score=93,
            path="docs/example.md",
        )
    ]
    assert saved["candidate_classifications"][0]["classification"] == {
        "action": "quarantine",
        "candidate_slug": _slug("temporal", "context", "draft"),
        "matched_slug": "temporal_context",
        "reason": "near-match synonym candidate requires LLM escalation before vocabulary admission",
    }


def test_write_stamp_refuses_to_advance_when_escalation_candidates_exist(tmp_path, monkeypatch):
    output_path = tmp_path / "synonym_candidates.json"
    stamp_path = tmp_path / "vocabulary_touch_stamp.json"
    monkeypatch.setattr(audit, "OUTPUT_PATH", output_path)
    monkeypatch.setattr(audit, "STAMP_PATH", stamp_path)
    monkeypatch.setattr(audit, "_fingerprint", lambda: "new")
    phrase = " ".join(["Temporal", "Context", "draft"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context")),
    )
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", phrase)]),
    )

    with pytest.raises(RuntimeError, match="cannot update vocabulary touch stamp"):
        audit.write_stamp()

    assert not stamp_path.exists()
    assert not output_path.exists()


def test_write_stamp_advances_only_after_clean_candidate_report(tmp_path, monkeypatch):
    output_path = tmp_path / "synonym_candidates.json"
    stamp_path = tmp_path / "vocabulary_touch_stamp.json"
    monkeypatch.setattr(audit, "OUTPUT_PATH", output_path)
    monkeypatch.setattr(audit, "STAMP_PATH", stamp_path)
    monkeypatch.setattr(audit, "_fingerprint", lambda: "clean-fingerprint")
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context")),
    )
    monkeypatch.setattr(audit, "_iter_candidates", lambda: iter([]))

    assert audit.write_stamp() is None

    assert json.loads(stamp_path.read_text(encoding="utf-8")) == {
        "schema_version": "v2_namespaced",
        "namespaces": {"global": "clean-fingerprint"},
    }


def test_synonym_candidate_escalation_report_marks_near_match_as_quarantine(monkeypatch):
    phrase = " ".join(["Temporal", "Context", "Draft"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context")),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(audit, "_iter_candidates", lambda: iter([("docs/example.md", phrase)]))

    report = audit.build_report()

    assert report["candidate_classifications"] == [
        {
            "phrase": " ".join(["temporal", "context", "draft"]),
            "path": "docs/example.md",
            "nearest_slug": "temporal_context",
            "classification": {
                "action": "quarantine",
                "candidate_slug": _slug("temporal", "context", "draft"),
                "matched_slug": "temporal_context",
                "reason": "near-match synonym candidate requires LLM escalation before vocabulary admission",
            },
            "admission_review": {
                "status": "quarantined",
                "candidate_slug": _slug("temporal", "context", "draft"),
                "plan": {
                    "classification": {
                        "action": "quarantine",
                        "candidate_slug": _slug("temporal", "context", "draft"),
                        "matched_slug": "temporal_context",
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


def test_compact_tokenisation_variant_is_not_escalated(monkeypatch):
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context")),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/example.md", "TemporalContext")]),
    )

    assert audit.build_report()["candidates"] == []


def test_likely_synonym_candidate_is_not_globally_suppressed(monkeypatch):
    phrase = " ".join(["Temporal", "Context", "Draft"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context")),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(audit, "_iter_candidates", lambda: iter([("docs/random.md", phrase)]))

    assert audit.build_report()["candidates"] == [
        _candidate(
            phrase=" ".join(["temporal", "context", "draft"]),
            nearest_slug="temporal_context",
            nearest_label="Temporal Context",
            score=93,
            path="docs/random.md",
        )
    ]


def test_protocol_field_identifier_fragment_is_not_escalated(monkeypatch):
    raw = _slug("dependency", "packet", "ids", "value")
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(
            _entry("dependency_packet_ids", "Dependency Packet IDs", category="protocol_field")
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("src/example.py", raw)]),
    )

    assert audit.build_report()["candidates"] == []


def test_protocol_field_prose_variant_is_still_escalated(monkeypatch):
    phrase = " ".join(["Dependency", "Packet", "IDs", "value"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(
            _entry("dependency_packet_ids", "Dependency Packet IDs", category="protocol_field")
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(audit, "_iter_candidates", lambda: iter([("docs/example.md", phrase)]))

    assert audit.build_report()["candidates"] == [
        _candidate(
            phrase=" ".join(["dependency", "packet", "ids", "value"]),
            nearest_slug="dependency_packet_ids",
            nearest_label="Dependency Packet IDs",
            score=93,
            path="docs/example.md",
        )
    ]


def test_python_function_declaration_identifier_fragment_is_not_escalated(monkeypatch):
    raw = "def " + "_".join(["temporal", "context"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context")),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(audit, "_iter_candidates", lambda: iter([("src/example.py", raw)]))

    assert audit.build_report()["candidates"] == []


def test_python_function_declaration_prose_variant_is_still_escalated(monkeypatch):
    phrase = " ".join(["def", "temporal", "context"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context")),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(audit, "_iter_candidates", lambda: iter([("docs/example.md", phrase)]))

    assert audit.build_report()["candidates"] == [
        _candidate(
            phrase=" ".join(["def", "temporal", "context"]),
            nearest_slug="temporal_context",
            nearest_label="Temporal Context",
            score=93,
            path="docs/example.md",
        )
    ]


def test_legitimate_terms_are_admitted_through_allowed_aliases(monkeypatch):
    alias = " ".join(["temporal", "event", "context"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context", allowed_aliases=[alias])),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/one.md", alias), ("docs/two.md", alias.replace(" ", "_"))]),
    )

    assert audit.build_report()["candidates"] == []


def test_disallowed_phrases_do_not_globally_suppress_new_occurrences(monkeypatch):
    rejected = " ".join(["temporal", "context", "fixture"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(
            _entry("temporal_context", "Temporal Context", disallowed_phrases=[rejected])
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(
        audit,
        "_iter_candidates",
        lambda: iter([("docs/one.md", rejected), ("docs/two.md", rejected.replace(" ", "_"))]),
    )

    assert [item["path"] for item in audit.build_report()["candidates"]] == [
        "docs/one.md",
        "docs/two.md",
    ]


def test_unresolved_candidates_remain_visible_until_governed(monkeypatch):
    unresolved = " ".join(["temporal", "context", "fixture"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context")),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(audit, "_iter_candidates", lambda: iter([("docs/one.md", unresolved)]))

    assert audit.build_report()["candidates"] == [
        _candidate(
            phrase=unresolved,
            nearest_slug="temporal_context",
            nearest_label="Temporal Context",
            score=93,
            path="docs/one.md",
        )
    ]


def test_check_clean_returns_nonzero_when_unresolved_candidates_exist(monkeypatch, capsys):
    unresolved = " ".join(["temporal", "context", "fixture"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(_entry("temporal_context", "Temporal Context")),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(audit, "_iter_candidates", lambda: iter([("docs/one.md", unresolved)]))

    assert audit.main(["--namespace", "global", "--check-clean"]) == 1
    assert "vocabulary_synonym_audit=BLOCKED unresolved_candidates=1" in capsys.readouterr().out


def test_check_clean_returns_zero_when_occurrence_is_an_allowed_alias(monkeypatch, capsys):
    governed = " ".join(["temporal", "context", "fixture"])
    monkeypatch.setattr(
        audit,
        "_load_document",
        lambda: _payload(
            _entry("temporal_context", "Temporal Context", allowed_aliases=[governed])
        ),
    )
    monkeypatch.setattr(audit, "_fingerprint", lambda: "fixture")
    monkeypatch.setattr(audit, "_iter_candidates", lambda: iter([("docs/one.md", governed)]))

    assert audit.main(["--namespace", "global", "--check-clean"]) == 0
    assert "vocabulary_synonym_audit=PASS candidates=0" in capsys.readouterr().out


def test_source_code_contains_no_path_bound_synonym_suppression_tables():
    source = Path("src/nvda_desk/vocabulary_synonym_audit.py").read_text(encoding="utf-8")

    forbidden = [
        "FWD001_GOVERNANCE_CANDIDATE_FRAGMENTS",
        "_is_fwd001_governance_candidate_fragment",
        "selected_fragments",
        "path-bound",
    ]
    for token in forbidden:
        assert token not in source


def test_module_namespace_audit_does_not_scan_unrelated_repository_paths(
    tmp_path, monkeypatch
):
    m04_scope = tmp_path / "m04_scope"
    unrelated_scope = tmp_path / "unrelated_scope"
    m04_scope.mkdir()
    unrelated_scope.mkdir()
    (m04_scope / "owned.py").write_text(
        'label = "Reference Packet Draft"\n', encoding="utf-8"
    )
    (unrelated_scope / "unrelated.py").write_text(
        'label = "Reference Packet Draft"\n', encoding="utf-8"
    )
    payload = _payload(
        _entry(
            "reference_packet",
            "Reference Packet",
            category="protocol_field",
            namespace="m04",
        )
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(audit, "_load_document", lambda: payload)
    monkeypatch.setattr(audit, "_fingerprint", lambda namespace, scan_paths: "fixture")
    monkeypatch.setattr(
        audit,
        "RESOLVED_OCCURRENCES_PATH",
        tmp_path / "missing_resolved_occurrences.tsv",
    )
    monkeypatch.setattr(audit, "STAMP_PATH", tmp_path / "missing_stamp.json")

    report = audit.build_report(namespace="m04")

    assert report["namespace"] == "m04"
    assert report["scan_paths"] == ["m04_scope"]
    assert report["scanned_file_count"] == 1
    assert [item["path"] for item in report["candidates"]] == ["m04_scope/owned.py"]
    assert report["candidates"][0]["nearest_identity"] == "m04.reference_packet"
