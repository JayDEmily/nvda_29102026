"""RSQL-P11/P13: production A00 construction and direct ordered public delegation."""

import ast
import inspect
import subprocess
import sys
from pathlib import Path

import pytest
from _support import T0, observation, owner, policy, process_env

from nvda_desk.composition import create_application
from nvda_desk.raw_signal_occurrence_truth import api


def test_sqlite_a00_constructs_nonowning_store_and_public_owner(tmp_path):
    path = tmp_path / "raw.db"
    owner(path, create=True)
    app = create_application(sqlite_path=str(path))
    assert app is not None
    for kwargs in (
        {},
        {"sqlite_path": str(path), "postgres_dsn": "dsn"},
        {"sqlite_path": str(path), "raw_signal_owner_factory": api.create_owner},
        {"sqlite_path": ""},
        {"sqlite_path": ":memory:"},
    ):
        with pytest.raises((TypeError, ValueError, api.PersistenceFailureV1)):
            create_application(**kwargs)
    with pytest.raises(api.PersistenceFailureV1):
        create_application(sqlite_path=str(tmp_path / "missing.db"))
    code = """
import sys
class NoPsycopg:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {"psycopg", "psycopg_binary"}:
            raise AssertionError("SQLite path imported Psycopg")
sys.meta_path.insert(0, NoPsycopg())
from nvda_desk.composition import create_application
create_application(sqlite_path=sys.argv[1])
assert not any(n.startswith("psycopg") for n in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(path)],
        env=process_env(),
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr


def test_sqlite_a00_exact_order_arguments_and_results(tmp_path):
    path = tmp_path / "raw.db"
    actual = owner(path, create=True)
    calls = []

    class Facet:
        def __init__(self, underlying):
            self.underlying = underlying

        def __getattr__(self, name):
            def traced(*args, **kwargs):
                result = getattr(self.underlying, name)(*args, **kwargs)
                calls.append((name, args, kwargs, result))
                return result

            return traced

    class TracedOwner:
        commands = Facet(actual.commands)
        reads = Facet(actual.reads)

    app = create_application(raw_signal_owner_factory=lambda: TracedOwner())
    p, raw = policy(), observation()
    result = app.run_raw_signal_proof_sequence(
        capture_scope_policy=p,
        scope_policy_ref=api.scope_policy_ref("policy@1"),
        slot_start_utc=T0,
        capture_occurrence_id=api.capture_occurrence_id("capture"),
        raw_observation=raw,
        assessment_occurrence_id=api.assessment_occurrence_id("assessment"),
        assessment_evidence_as_of_ts_utc=T0,
        supersedes_assessment_ref=None,
    )
    assert [row[0] for row in calls] == [
        "register_capture_scope_policy",
        "realise_scheduled_capture_occurrence",
        "admit_raw_observation_occurrence",
        "derive_capture_receipt_evidence_relation",
        "append_capture_receipt_presence_assessment",
        "get_raw_observation_occurrence",
    ]
    for field, row in zip(
        ("policy", "capture", "observation", "relation", "assessment", "readback"),
        calls,
        strict=True,
    ):
        assert getattr(result, field) is row[3]
    assert calls[0][1][0] is p and calls[2][1][0] is raw
    assert calls[3][2]["observation_occurrence_ref"] is result.observation.observation_occurrence_id
    assert calls[4][2]["capture_occurrence_ref"] is result.capture.capture_occurrence_id
    assert result.assessment.outcome == "one_or_more_received"


def test_sqlite_a00_has_no_domain_decisions_or_private_bypass():
    import nvda_desk.composition as composition

    tree = ast.parse(inspect.getsource(composition))
    private = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.ImportFrom)
            and node.module
            and node.module.startswith("nvda_desk.raw_signal_occurrence_truth._")
        ):
            private.extend(node.module + "." + item.name for item in node.names)
    assert set(private) == {
        "nvda_desk.raw_signal_occurrence_truth._sqlite.create_sqlite_persistence",
        "nvda_desk.raw_signal_occurrence_truth._postgres.create_postgres_persistence",
    }
    assert "sqlite_path" in inspect.signature(create_application).parameters
    rules = Path(__file__).resolve().parents[3] / "config/architecture/dependency_rules.yaml"
    assert (
        "nvda_desk.raw_signal_occurrence_truth._sqlite.create_sqlite_persistence"
        in rules.read_text()
    )
    sequence = inspect.getsource(composition.Application.run_raw_signal_proof_sequence)
    assert "outcome=" not in sequence and "sqlite3" not in sequence
