"""Disposable public A00/M00 sequence in the installed runtime-only profile."""
import importlib.metadata
import importlib.util
import sqlite3
import sys
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from nvda_desk import composition
from nvda_desk.raw_signal_occurrence_truth import api
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

assert sys.version_info[:3] == (3, 12, 14)
assert "site-packages" in composition.__file__
assert importlib.util.find_spec("psycopg") is None
assert importlib.util.find_spec("psycopg_binary") is None
now = datetime(2026, 10, 19, tzinfo=UTC)
policy = api.CaptureScopePolicyV1(
    concept_id=api.concept_id("raw_signal.capture_scope_policy"),
    contract_id=api.contract_id("nvda.raw_signal.CaptureScopePolicy.v1"),
    units="not_applicable", scope_policy_id=api.scope_policy_id("runtime"),
    scope_policy_version=1, activation_ts_utc=now,
    eligibility_policy_ref=api.eligibility_policy_ref("runtime/v1"),
)
raw = api.RawObservationOccurrenceV1(
    concept_id=api.concept_id("raw_signal.raw_observation_occurrence"),
    contract_id=api.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
    observation_occurrence_id=api.observation_occurrence_id("runtime-observation"),
    delivery_artifact_ref=api.delivery_artifact_ref("runtime-delivery"),
    source_provider=api.provider_id("controlled-runtime"),
    native_record={"price": 123.45, "size": Decimal("3.2500"), "contract_integer": 10**5000},
    received_ts_utc=now, ingestion_sequence=10**5000,
    ingestion_sequence_scope=api.ingestion_sequence_scope("runtime-scope"),
    source_temporal_kind="receipt_only",
)
with TemporaryDirectory(prefix="nvda-g51-runtime-") as temporary:
    path = str(Path(temporary) / "m00.sqlite")
    create_sqlite_persistence(path, create=True)
    app = composition.create_application(
        sqlite_path=path, raw_signal_eligibility_resolver=lambda observation, policy: True
    )
    result = app.run_raw_signal_proof_sequence(
        capture_scope_policy=policy, scope_policy_ref=api.scope_policy_ref("runtime@1"),
        slot_start_utc=now, capture_occurrence_id=api.capture_occurrence_id("runtime-capture"),
        raw_observation=raw, assessment_occurrence_id=api.assessment_occurrence_id("runtime-a"),
        assessment_evidence_as_of_ts_utc=now, supersedes_assessment_ref=None,
    )
    assert result.readback == raw
    assert result.assessment.outcome == "one_or_more_received"
    restarted = api.create_owner(durability_port=create_sqlite_persistence(path))
    restored = restarted.reads.get_raw_observation_occurrence(raw.observation_occurrence_id)
    assert restored == raw
    assert type(restored.native_record["price"]) is float
    assert restored.native_record["size"].as_tuple() == (0, (3, 2, 5, 0, 0), -4)
    assert restored.ingestion_sequence == 10**5000
assert not any(name.startswith("psycopg") for name in sys.modules)
print("PASS: installed production A00 SQLite sequence, reopened exact public M00 read, native types")
print("Python:", sys.version.split()[0], "SQLite:", sqlite3.sqlite_version)
print("Installed:", sorted((d.metadata["Name"], d.version) for d in importlib.metadata.distributions()))
print("Module:", composition.__file__)
