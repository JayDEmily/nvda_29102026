"""RSQL-P04/P07–P11: native commit, failure, complete facts and actual file provenance."""

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
    mechanism,
    observation,
    owner,
    policy,
    process_env,
    representation,
)

from nvda_desk.raw_signal_occurrence_truth import api


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


def test_sqlite_public_return_requires_native_commit(tmp_path):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
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
    raw = observation(native={"nonce": secrets.token_hex(32)})
    try:
        with pytest.raises(api.PersistenceFailureV1) as failure:
            o.commands.admit_raw_observation_occurrence(raw)
        assert failure.value.outcome_uncertain is False
    finally:
        reader.execute("ROLLBACK")
        reader.close()
    assert fresh_observation(path, "obs") is None
    # A separate writer stays alive immediately after public return; kill it there.
    nonce = secrets.token_hex(32)
    code = """
import sys
from _support import owner, observation
o = owner(sys.argv[1])
o.commands.admit_raw_observation_occurrence(observation("committed", native={"nonce":sys.argv[2]}))
print("RETURNED", flush=True)
sys.stdin.read()
"""
    proc = subprocess.Popen(
        [sys.executable, "-u", "-c", code, str(path), nonce],
        env=process_env(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        assert proc.stdout.readline().strip() == "RETURNED"
        assert fresh_observation(path, "committed")["native"] == representation({"nonce": nonce})
    finally:
        proc.kill()
        proc.communicate(timeout=10)
    assert fresh_observation(path, "committed")["native"] == representation({"nonce": nonce})


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
    assert fresh_observation(path, "obs")["native"] == representation(raw.native_record)
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
    assert fresh_observation(clone, "obs")["native"] == representation(raw.native_record)
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
    with port.transaction(write=False) as tx:
        with pytest.raises((RuntimeError, api.PersistenceFailureV1)):
            tx.append_observation(observation())


def test_sqlite_proof_rejects_surrogate_commit_and_payload(tmp_path):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    nonce = secrets.token_hex(32)
    expected = representation({"nonce": nonce, "complete": [None, Decimal("2.000")]})
    o.commands.register_capture_scope_policy(policy())
    # Setup-only committed state cannot satisfy semantic observation readback.
    assert fresh_observation(path, "target") is None
    o.commands.admit_raw_observation_occurrence(observation("target", native={"nonce": nonce}))
    surrogate = fresh_observation(path, "target")
    assert surrogate["native"] != expected
    # The correspondence oracle is demonstrably sensitive to omission/type/precision.
    for false in (
        {"nonce": nonce},
        {"nonce": nonce, "complete": [None, Decimal("2.0")]},
        {"nonce": nonce, "complete": (None, Decimal("2.000"))},
    ):
        assert representation(false) != expected
