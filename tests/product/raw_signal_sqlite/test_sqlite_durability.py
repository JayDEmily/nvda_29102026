"""RSQL-P04/P07-P11: native commit, failure, complete facts and actual file provenance."""

import base64
import hashlib
import json
import pickle
import secrets
import sqlite3
import subprocess
import sys
from dataclasses import replace
from decimal import Decimal

import pytest
from _support import (
    T0,
    fresh_observation,
    fresh_record,
    mechanism,
    observation,
    owner,
    policy,
    process_env,
)
from test_contract_native import representation

from nvda_desk.raw_signal_occurrence_truth import api


def require_committed_return(path, kind, identity, returned, expected):
    """One complete-fact discriminator for actual public returns and canary substitutes."""
    assert representation(returned) == representation(expected)
    assert representation(fresh_record(path, kind, identity)) == representation(expected)


def test_sqlite_environment_and_only_configured_semantic_source(tmp_path):
    assert sys.version_info[:3] == (3, 12, 14)
    assert sqlite3.sqlite_version == "3.53.1"
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    raw = observation(native={"nonce": secrets.token_hex(32)})
    o.commands.admit_raw_observation_occurrence(raw)
    with sqlite3.connect(path) as c:
        assert c.execute("PRAGMA application_id").fetchone()[0] == 0x4E560001
        assert c.execute("PRAGMA user_version").fetchone()[0] == 1
        assert c.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
        rows = c.execute("PRAGMA table_list").fetchall()
        semantic = [row for row in rows if row[1].startswith("rsot_")]
        assert len(semantic) == 4 and all(row[5] == 1 for row in semantic)
    with mechanism().create_sqlite_persistence(str(path)).transaction(write=True) as tx:
        assert tx.get_observation(raw.observation_occurrence_id) is not None
    for invalid in (
        ":memory:",
        "relative.db",
        str(tmp_path / "absent" / "raw.db"),
        "file:" + str(path),
        str(path) + "?mode=ro",
    ):
        with pytest.raises((TypeError, ValueError, api.PersistenceFailureV1)):
            mechanism().create_sqlite_persistence(invalid)
    link = tmp_path / "link.db"
    link.symlink_to(path)
    with pytest.raises((ValueError, api.PersistenceFailureV1)):
        mechanism().create_sqlite_persistence(str(link))
    for existing in (path, tmp_path / "empty.db"):
        if not existing.exists():
            existing.touch()
        before = existing.read_bytes()
        with pytest.raises(api.PersistenceFailureV1):
            mechanism().create_sqlite_persistence(str(existing), create=True)
        assert existing.read_bytes() == before
    with sqlite3.connect(path) as c:
        c.execute("PRAGMA application_id=42")
    with pytest.raises(api.PersistenceFailureV1):
        owner(path).reads.get_raw_observation_occurrence(raw.observation_occurrence_id)


@pytest.mark.parametrize("kind", ["policy", "capture", "observation", "assessment"])
def test_sqlite_public_return_requires_native_commit(tmp_path, kind):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    nonce = secrets.token_hex(32)
    p = policy(eligibility_policy_ref=api.eligibility_policy_ref(nonce))
    if kind != "policy":
        o.commands.register_capture_scope_policy(p)
    if kind == "assessment":
        capture = o.commands.realise_scheduled_capture_occurrence(
            scope_policy_ref=api.scope_policy_ref("policy@1"),
            slot_start_utc=T0,
            capture_occurrence_id=api.capture_occurrence_id("capture"),
        )
    if kind == "policy":
        expected, identity = p, "policy"

        def call():
            return o.commands.register_capture_scope_policy(expected)
    elif kind == "capture":
        expected = api.ScheduledCaptureOccurrenceV1(
            api.concept_id("raw_signal.scheduled_capture_occurrence"),
            api.contract_id("nvda.raw_signal.ScheduledCaptureOccurrence.v1"),
            "not_applicable",
            api.capture_occurrence_id(nonce),
            api.scope_policy_ref("policy@1"),
            T0,
            T0.replace(second=30),
        )
        identity = nonce

        def call():
            return o.commands.realise_scheduled_capture_occurrence(
                scope_policy_ref=expected.scope_policy_ref,
                slot_start_utc=T0,
                capture_occurrence_id=expected.capture_occurrence_id,
            )
    elif kind == "observation":
        expected, identity = observation(native={"nonce": nonce}), "obs"

        def call():
            return o.commands.admit_raw_observation_occurrence(expected)
    else:
        expected = api.CaptureReceiptPresenceAssessmentV1(
            api.concept_id("raw_signal.capture_receipt_presence_assessment"),
            api.contract_id("nvda.raw_signal.CaptureReceiptPresenceAssessment.v1"),
            "not_applicable",
            api.assessment_occurrence_id(nonce),
            capture.capture_occurrence_id,
            "zero_received",
            T0,
        )
        identity = nonce

        def call():
            return o.commands.append_capture_receipt_presence_assessment(
                assessment_occurrence_id=expected.assessment_occurrence_id,
                capture_occurrence_ref=expected.capture_occurrence_ref,
                evidence_as_of_ts_utc=T0,
                supersedes_assessment_ref=None,
            )

    # First prove the independent barrier rejects an ordinary native COMMIT.
    reader = sqlite3.connect(path, isolation_level=None)
    reader.execute("BEGIN")
    reader.execute("SELECT * FROM rsot_raw_observation_occurrence_v1").fetchall()
    canary = sqlite3.connect(path, isolation_level=None, timeout=0)
    canary.execute("BEGIN IMMEDIATE")
    with pytest.raises(sqlite3.OperationalError, match="locked"):
        canary.execute("COMMIT")
    canary.execute("ROLLBACK")
    canary.close()
    try:
        with pytest.raises(api.PersistenceFailureV1) as failure:
            call()
        assert failure.value.outcome_uncertain is False
    finally:
        reader.execute("ROLLBACK")
        reader.close()
    assert fresh_record(path, kind, identity) is None
    # A separate writer stays alive immediately after public return; kill it there.
    code = """
import base64, pickle, sys
from _support import owner
o = owner(sys.argv[1])
kind = sys.argv[2]
v = pickle.loads(base64.b64decode(sys.argv[3]))
if kind == "policy":
    result = o.commands.register_capture_scope_policy(v)
elif kind == "observation":
    result = o.commands.admit_raw_observation_occurrence(v)
elif kind == "capture":
    result = o.commands.realise_scheduled_capture_occurrence(scope_policy_ref=v.scope_policy_ref,
        slot_start_utc=v.slot_start_utc, capture_occurrence_id=v.capture_occurrence_id)
else:
    result = o.commands.append_capture_receipt_presence_assessment(
        assessment_occurrence_id=v.assessment_occurrence_id,
        capture_occurrence_ref=v.capture_occurrence_ref,
        evidence_as_of_ts_utc=v.evidence_as_of_ts_utc,
        supersedes_assessment_ref=v.supersedes_assessment_ref)
print(base64.b64encode(pickle.dumps(result)).decode("ascii"), flush=True)
sys.stdin.read()
"""
    proc = subprocess.Popen(
        [
            sys.executable,
            "-u",
            "-c",
            code,
            str(path),
            kind,
            base64.b64encode(pickle.dumps(expected)).decode("ascii"),
        ],
        env=process_env(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        returned = pickle.loads(base64.b64decode(proc.stdout.readline().strip()))
        require_committed_return(path, kind, identity, returned, expected)
    finally:
        proc.kill()
        proc.communicate(timeout=10)
    assert representation(fresh_record(path, kind, identity)) == representation(expected)


def test_sqlite_failed_write_and_killed_writer_nonfabrication(tmp_path):
    path = tmp_path / "raw.db"
    owner(path, create=True)
    # A real uncommitted semantic row, not a marker, is killed with no context exit.
    code = """
import os, sys
from _support import mechanism, observation
p = mechanism().create_sqlite_persistence(sys.argv[1])
with p.transaction(write=True) as tx:
    tx.append_observation(observation("uncommitted", native={"nonce":sys.argv[2]}))
    os._exit(27)
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(path), secrets.token_hex(32)],
        env=process_env(),
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 27, result.stderr
    # Permitted writer reopen performs any required journal recovery before reader proof.
    o = owner(path)
    assert (
        o.reads.get_raw_observation_occurrence(api.observation_occurrence_id("uncommitted")) is None
    )
    assert fresh_observation(path, "uncommitted") is None
    port = mechanism().create_sqlite_persistence(str(path))
    with pytest.raises(RuntimeError, match="before commit"), port.transaction(write=True) as tx:
        tx.append_observation(observation("rolled-back"))
        raise RuntimeError("before commit")
    assert fresh_observation(path, "rolled-back") is None


def test_sqlite_uncertain_commit_and_concurrent_identity(tmp_path, monkeypatch):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    raw = observation(native={"nonce": secrets.token_hex(32)})
    original_connect = sqlite3.connect
    lost = []

    class LostAcknowledgement(sqlite3.Connection):
        def execute(self, sql, parameters=()):
            result = super().execute(sql, parameters)
            if sql.strip().upper() == "COMMIT" and not lost:
                lost.append(True)
                raise sqlite3.OperationalError("deliberately lost commit acknowledgement")
            return result

    def connect(*args, **kwargs):
        return original_connect(*args, **dict(kwargs, factory=LostAcknowledgement))

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", connect)
        with pytest.raises(api.PersistenceFailureV1) as failure:
            o.commands.admit_raw_observation_occurrence(raw)
        assert failure.value.outcome_uncertain is True
    assert lost
    assert representation(fresh_observation(path, "obs")) == representation(raw)
    assert o.commands.admit_raw_observation_occurrence(raw) == raw
    with pytest.raises(ValueError):
        o.commands.admit_raw_observation_occurrence(replace(raw, native_record={"nonce": "wrong"}))
    # An overlapping independent connection cannot silently enter a writer transaction.
    with mechanism().create_sqlite_persistence(str(path)).transaction(write=True):
        code = """
import sys
from _support import owner, observation
from nvda_desk.raw_signal_occurrence_truth.api import PersistenceFailureV1
try:
    owner(sys.argv[1]).commands.admit_raw_observation_occurrence(observation("competing", 2))
except PersistenceFailureV1 as exc:
    assert not exc.outcome_uncertain
    print("CONTENTION")
else:
    raise AssertionError("concurrent write unexpectedly succeeded")
"""
        result = subprocess.run(
            [sys.executable, "-c", code, str(path)],
            env=process_env(),
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 0 and result.stdout.strip() == "CONTENTION", result.stderr
    other = observation("competing", 2)
    assert owner(path).commands.admit_raw_observation_occurrence(other) == other
    assert owner(path).commands.admit_raw_observation_occurrence(other) == other


def test_sqlite_native_roundtrip_and_consistent_backup(tmp_path):
    path, clone = tmp_path / "raw.db", tmp_path / "clone.db"
    raw = observation(native={"nonce": secrets.token_hex(32), "precision": Decimal("-0.000")})
    o = owner(path, create=True)
    o.commands.admit_raw_observation_occurrence(raw)
    with sqlite3.connect(path) as source, sqlite3.connect(clone) as destination:
        source.backup(destination)
    path.rename(tmp_path / "unavailable.db")
    assert representation(fresh_observation(clone, "obs")) == representation(raw)
    with pytest.raises(api.PersistenceFailureV1):
        o.reads.get_raw_observation_occurrence(raw.observation_occurrence_id)
    assert not path.exists()
    # Corrupt complete content and matching index: fail closed on its immutable digest.
    with sqlite3.connect(clone) as c:
        for (name,) in c.execute("SELECT name FROM sqlite_schema WHERE type='trigger'").fetchall():
            c.execute('DROP TRIGGER "' + name + '"')
        c.execute("UPDATE rsot_raw_observation_occurrence_v1 SET payload=?", (b"{}",))
    with pytest.raises(api.PersistenceFailureV1):
        owner(clone).reads.get_raw_observation_occurrence(raw.observation_occurrence_id)


def test_sqlite_port_is_nonsemantic_and_record_only(tmp_path):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    o.commands.register_capture_scope_policy(policy())
    capture = o.commands.realise_scheduled_capture_occurrence(
        scope_policy_ref=api.scope_policy_ref("policy@1"),
        slot_start_utc=T0,
        capture_occurrence_id=api.capture_occurrence_id("capture"),
    )
    counterfactual = api.CaptureReceiptPresenceAssessmentV1(
        concept_id=api.concept_id("raw_signal.capture_receipt_presence_assessment"),
        contract_id=api.contract_id("nvda.raw_signal.CaptureReceiptPresenceAssessment.v1"),
        units="not_applicable",
        assessment_occurrence_id=api.assessment_occurrence_id("decided"),
        capture_occurrence_ref=capture.capture_occurrence_id,
        outcome="one_or_more_received",
        evidence_as_of_ts_utc=T0,
    )
    port = mechanism().create_sqlite_persistence(str(path))
    assert {name for name in dir(port) if not name.startswith("_")} == {"transaction"}
    with port.transaction(write=True) as tx:
        tx.append_assessment(counterfactual)
    assert (
        owner(path).reads.get_receipt_presence_assessment(counterfactual.assessment_occurrence_id)
        == counterfactual
    )
    with (
        port.transaction(write=False) as tx,
        pytest.raises((RuntimeError, api.PersistenceFailureV1)),
    ):
        tx.append_observation(observation())


def test_sqlite_proof_rejects_surrogate_commit_and_payload(tmp_path):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    nonce = secrets.token_hex(32)
    expected = observation("target", native={"nonce": nonce, "complete": [None, Decimal("2.000")]})

    def correspondence(operation):
        returned = operation()
        require_committed_return(path, "observation", "target", returned, expected)

    def setup_only():
        o.commands.register_capture_scope_policy(policy())
        return expected

    # Actual native commits to marker/setup state must not pass the real correspondence check.
    with pytest.raises(AssertionError):
        correspondence(setup_only)

    pending = mechanism().create_sqlite_persistence(str(path)).transaction(write=True)

    def split_commit():
        # Return actual expected content while its semantic transaction remains uncommitted.
        # A distinct setup transaction above has committed; that commit cannot certify this row.
        tx = pending.__enter__()
        tx.append_observation(expected)
        return expected

    try:
        with pytest.raises(AssertionError):
            correspondence(split_commit)
    finally:
        rollback = RuntimeError("deliberately roll back split-commit canary")
        pending.__exit__(RuntimeError, rollback, None)
    assert fresh_record(path, "observation", "target") is None

    def subset_commit():
        o.commands.admit_raw_observation_occurrence(
            replace(expected, native_record={"nonce": nonce})
        )
        return expected

    with pytest.raises(AssertionError):
        correspondence(subset_commit)


def test_sqlite_schema_settings_canonical_payload_and_index_integrity(tmp_path, monkeypatch):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    observed = []
    original = sqlite3.connect

    class ObservedConnection(sqlite3.Connection):
        def execute(self, sql, parameters=()):
            if sql.strip().upper().startswith("BEGIN"):
                settings = {
                    key: super(ObservedConnection, self).execute("PRAGMA " + key).fetchone()[0]
                    for key in (
                        "foreign_keys",
                        "synchronous",
                        "busy_timeout",
                        "query_only",
                        "journal_mode",
                    )
                }
                observed.append((sql.upper(), settings))
            return super().execute(sql, parameters)

    def connect(*args, **kwargs):
        return original(*args, **dict(kwargs, factory=ObservedConnection))

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", connect)
        o.commands.admit_raw_observation_occurrence(observation())
        o.reads.get_raw_observation_occurrence(api.observation_occurrence_id("obs"))
    assert any(
        sql == "BEGIN IMMEDIATE"
        and settings
        == {
            "foreign_keys": 1,
            "synchronous": 3,
            "busy_timeout": 0,
            "query_only": 0,
            "journal_mode": "delete",
        }
        for sql, settings in observed
    )
    assert any(
        sql == "BEGIN"
        and settings["query_only"] == 1
        and settings["foreign_keys"] == 1
        and settings["busy_timeout"] == 0
        for sql, settings in observed
    )
    columns = {
        "rsot_capture_scope_policy_v1": {
            "scope_policy_id",
            "scope_policy_version",
            "scope_policy_ref",
            "activation_ts_utc",
            "deactivation_ts_utc",
            "eligibility_policy_ref",
        },
        "rsot_scheduled_capture_occurrence_v1": {
            "capture_occurrence_id",
            "scope_policy_ref",
            "slot_start_utc",
            "slot_end_utc",
        },
        "rsot_raw_observation_occurrence_v1": {
            "observation_occurrence_id",
            "received_ts_utc",
            "ingestion_sequence_scope",
            "ingestion_sequence",
            "ingestion_sort_key",
        },
        "rsot_capture_receipt_presence_assessment_v1": {
            "assessment_occurrence_id",
            "capture_occurrence_ref",
            "outcome",
            "evidence_as_of_ts_utc",
            "supersedes_assessment_ref",
        },
    }
    with sqlite3.connect(path) as c:
        assert {
            row[0]
            for row in c.execute("SELECT name FROM sqlite_schema WHERE type='table'")
            if not row[0].startswith("sqlite_")
        } == set(columns)
        for table, names in columns.items():
            info = c.execute("PRAGMA table_info(" + table + ")").fetchall()
            assert {row[1] for row in info} == names | {"payload", "content_sha256"}
            for row in info:
                if row[1] not in {"deactivation_ts_utc", "supersedes_assessment_ref"}:
                    assert row[3] == 1
            triggers = [
                row[0].upper()
                for row in c.execute(
                    "SELECT sql FROM sqlite_schema WHERE type='trigger' AND tbl_name=?", (table,)
                )
            ]
            assert any("BEFORE UPDATE" in sql for sql in triggers)
            assert any("BEFORE DELETE" in sql for sql in triggers)
        assert c.execute("PRAGMA foreign_key_list(rsot_scheduled_capture_occurrence_v1)").fetchall()
        assert (
            len(
                c.execute(
                    "PRAGMA foreign_key_list(rsot_capture_receipt_presence_assessment_v1)"
                ).fetchall()
            )
            == 2
        )
        payload, digest, key = c.execute(
            "SELECT payload,content_sha256,ingestion_sort_key "
            "FROM rsot_raw_observation_occurrence_v1"
        ).fetchone()
        assert hashlib.sha256(payload).hexdigest() == digest
        decoded = json.loads(payload)
        assert (
            json.dumps(decoded, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()
            == payload
        )
        expected_native = (
            b"NVDA-NATIVE-V1\0m"
            + (1).to_bytes(8, "big")
            + (5).to_bytes(8, "big")
            + b"value"
            + b"d\0"
            + (3).to_bytes(8, "big")
            + b"\1\0\0"
            + (2).to_bytes(8, "big")
            + b"-2"
        )
        assert decoded["native_record"] == expected_native.hex()
        assert decoded["observation_occurrence_id"] == {
            "kind": "observation_occurrence_id",
            "value": "obs",
        }
        assert decoded["received_ts_utc"] == "2026-09-20T12:00:00.000000Z"
        assert key == b"\1" + (1).to_bytes(8, "big") + b"1"
        # Retain valid payload/hash but corrupt the searchable metadata: decoding must reject.
        trigger_sql = c.execute(
            "SELECT name,sql FROM sqlite_schema WHERE type='trigger'"
        ).fetchall()
        for name, _sql in trigger_sql:
            c.execute('DROP TRIGGER "' + name + '"')
        c.execute("UPDATE rsot_raw_observation_occurrence_v1 SET ingestion_sequence='2'")
        for _name, sql in trigger_sql:
            c.execute(sql)
    with pytest.raises(api.PersistenceFailureV1):
        owner(path).reads.get_raw_observation_occurrence(api.observation_occurrence_id("obs"))


def test_sqlite_competing_same_identity_converges_and_conflict_refuses(tmp_path):
    path = tmp_path / "raw.db"
    owner(path, create=True)
    raw = observation(native={"nonce": secrets.token_hex(32)})
    # First same-ID writer holds a genuine uncommitted row, while child attempts same ID.
    port = mechanism().create_sqlite_persistence(str(path))
    with port.transaction(write=True) as tx:
        tx.append_observation(raw)
        code = """
import base64, pickle, sys
from _support import owner
from nvda_desk.raw_signal_occurrence_truth.api import PersistenceFailureV1
raw = pickle.loads(base64.b64decode(sys.argv[2]))
try:
    owner(sys.argv[1]).commands.admit_raw_observation_occurrence(raw)
except PersistenceFailureV1 as exc:
    assert not exc.outcome_uncertain
    print("RETRY_REQUIRED")
else:
    raise AssertionError("competing uncommitted same-ID call returned success")
"""
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                code,
                str(path),
                base64.b64encode(pickle.dumps(raw)).decode("ascii"),
            ],
            env=process_env(),
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 0 and result.stdout.strip() == "RETRY_REQUIRED", result.stderr
    assert owner(path).commands.admit_raw_observation_occurrence(raw) == raw
    with pytest.raises(ValueError):
        owner(path).commands.admit_raw_observation_occurrence(
            replace(raw, native_record={"nonce": "conflicting"})
        )
    assert representation(fresh_observation(path, "obs")) == representation(raw)
