"""FND-P07: separate real owner files, native commit, losslessness and recovery."""

import base64
import hashlib
import importlib
import json
import pickle
import secrets
import sqlite3
import subprocess
import sys
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal

import pytest
from _support import (
    ASOF,
    BRIEF,
    NOW,
    configuration,
    foundation,
    fresh_read,
    observation,
    process_env,
    request,
)
from test_identity_readback import canonical

from nvda_desk.raw_signal_occurrence_truth import api as raw_api
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence


def raw_source(tmp_path):
    path = tmp_path / "raw.sqlite"
    raw = raw_api.create_owner(durability_port=create_sqlite_persistence(str(path), create=True))
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    return raw, path


def committed_fact(path, returned, expected):
    assert canonical(returned) == canonical(expected)
    assert canonical(fresh_read(path, expected.derived_occurrence_id)) == canonical(expected)


def test_d011_sqlite_commit_and_fresh_readback(tmp_path):
    assert sys.version_info[:3] == (3, 12, 14) and sqlite3.sqlite_version == "3.53.1"
    raw, raw_path = raw_source(tmp_path)
    f = foundation()
    path = tmp_path / "foundation.sqlite"
    config = configuration(f, raw.reads, storage=f.SQLiteStorageV1(str(path), True))
    o = f.create_owner(**config)
    # Independent native read-lock canary proves COMMIT cannot succeed under this barrier.
    barrier = sqlite3.connect(path, isolation_level=None)
    barrier.execute("BEGIN")
    barrier.execute("SELECT * FROM mmt_occurrence_v1").fetchall()
    canary = sqlite3.connect(path, isolation_level=None, timeout=0)
    canary.execute("BEGIN IMMEDIATE")
    with pytest.raises(sqlite3.OperationalError, match="locked"):
        canary.execute("COMMIT")
    canary.execute("ROLLBACK")
    canary.close()
    try:
        with pytest.raises(f.PersistenceFailureV1) as failure:
            o.materialise(request(f))
        assert failure.value.outcome_uncertain is False
    finally:
        barrier.execute("ROLLBACK")
        barrier.close()
    assert (
        o.reads.list_derived_history(
            derived_signal_id="D011",
            subject_instrument="NVDA",
            effective_at_or_before_utc=ASOF,
            knowledge_at_or_before_utc=ASOF,
            limit=100,
        )
        == ()
    )
    # High-entropy authoritative decimal input is fixed before the writer begins.
    digits = secrets.randbelow(10**25) + 10**25
    literal = Decimal(digits)
    raw.commands.admit_raw_observation_occurrence(
        observation(
            "bid", identity="nonce-bid", sequence=3, event=ASOF, receipt=ASOF, value=literal
        )
    )
    # Child reconstructs only public construction inputs; it stays alive immediately after return.
    code = """
import base64,pickle,sys
from _support import configuration,foundation,request
from nvda_desk.raw_signal_occurrence_truth import api as raw_api
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence
f=foundation()
raw=raw_api.create_owner(durability_port=create_sqlite_persistence(sys.argv[1]))
o=f.create_owner(**configuration(f,raw.reads,storage=f.SQLiteStorageV1(sys.argv[2],False)))
r=o.materialise(request(f))
print(base64.b64encode(pickle.dumps(r)).decode("ascii"),flush=True)
sys.stdin.read()
"""
    proc = subprocess.Popen(
        [sys.executable, "-u", "-c", code, str(raw_path), str(path)],
        env=process_env(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        returned = pickle.loads(base64.b64decode(proc.stdout.readline()))
        # Decimal(int) is exact; this expected average never uses the production evaluator.
        numerator = digits + 102
        expected_result = (
            Decimal(numerator // 2) if numerator % 2 == 0 else Decimal(str(numerator // 2) + ".5")
        )
        assert returned.result == expected_result
        assert returned.raw_input_lineage[0].projection.native_value == literal
        assert returned.raw_input_lineage[0].observation_occurrence_id == "nonce-bid"
        committed_fact(path, returned, returned)
        proc.kill()
        proc.wait(timeout=10)
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=10)
    committed_fact(path, returned, returned)
    for surrogate in (
        None,
        replace(returned, raw_input_lineage=()),
        replace(returned, result=Decimal("0")),
    ):
        with pytest.raises((AssertionError, TypeError)):
            committed_fact(path, surrogate, returned)
    # An uncommitted row followed by process death cannot satisfy the discriminator.
    blank = tmp_path / "blank.sqlite"
    f.create_owner(**configuration(f, raw.reads, storage=f.SQLiteStorageV1(str(blank), True)))
    with sqlite3.connect(path) as source:
        row = source.execute("SELECT * FROM mmt_occurrence_v1").fetchone()
    uncommitted_code = """
import base64,pickle,sqlite3,sys
row=pickle.loads(base64.b64decode(sys.argv[2]))
c=sqlite3.connect(sys.argv[1],isolation_level=None)
c.execute("BEGIN IMMEDIATE")
c.execute("INSERT INTO mmt_occurrence_v1 VALUES ("+",".join("?" for _ in row)+")",row)
print("INSERTED",flush=True)
sys.stdin.read()
"""
    pending = subprocess.Popen(
        [
            sys.executable,
            "-u",
            "-c",
            uncommitted_code,
            str(blank),
            base64.b64encode(pickle.dumps(row)).decode(),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        assert pending.stdout.readline().strip() == "INSERTED"
        with pytest.raises(AssertionError):
            committed_fact(blank, returned, returned)
    finally:
        pending.kill()
        pending.wait(timeout=10)
    assert fresh_read(blank, returned.derived_occurrence_id) is None
    reader = f.create_reader(
        admission=config["admission"], storage=f.SQLiteReadStorageV1(str(path))
    )
    for key in ("parameter_sets", "input_selection_policies", "unit_conventions"):
        get = {
            "parameter_sets": reader.get_parameter_set,
            "input_selection_policies": reader.get_input_selection_policy,
            "unit_conventions": reader.get_unit_convention,
        }[key]
        value = config[key][0]
        assert canonical(get(f.VersionRefV1(value.context_id, value.version))) == canonical(value)
    assert (
        reader.get_projection_mapping(f.VersionRefV1("mmt-pilot-bid", 1))
        == config["raw_projection_mappings"][0]
    )
    assert (
        reader.get_calculation_definition(
            derived_signal_id="D011", calculation_definition_version="D011-MIDPOINT-1"
        )
        == config["definitions"][0]
    )
    with sqlite3.connect(path) as connection:
        assert connection.execute("PRAGMA application_id").fetchone()[0] == 0x4E560002
        assert connection.execute("PRAGMA user_version").fetchone()[0] == 1
        assert connection.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
        tables = [
            row for row in connection.execute("PRAGMA table_list") if row[1].startswith("mmt_")
        ]
        assert len(tables) == 3 and all(row[5] == 1 for row in tables)
        clone = tmp_path / "backup.sqlite"
        with sqlite3.connect(clone) as backup:
            connection.backup(backup)
    committed_fact(clone, returned, returned)
    later = f.create_owner(
        **configuration(
            f,
            raw.reads,
            storage=f.SQLiteStorageV1(str(path), False),
            now=lambda: NOW + timedelta(days=1),
        )
    )
    assert canonical(later.materialise(request(f))) == canonical(returned)


def test_sqlite_immutable_concurrency_rollback_and_uncertain_commit(tmp_path, monkeypatch):
    raw, _ = raw_source(tmp_path)
    f = foundation()
    path = tmp_path / "foundation.sqlite"
    o = f.create_owner(**configuration(f, raw.reads, storage=f.SQLiteStorageV1(str(path), True)))
    reader = f.create_reader(
        admission=f.OwnerAdmissionV1("M02", BRIEF), storage=f.SQLiteReadStorageV1(str(path))
    )
    mechanism = importlib.import_module("nvda_desk.market_measurement_truth._sqlite")
    real_connect = sqlite3.connect
    mode = ["before"]

    class Fault(sqlite3.Connection):
        def execute(self, sql, *args, **kwargs):
            if sql.strip().upper() == "COMMIT" and mode[0] == "before":
                raise sqlite3.OperationalError("injected precommit failure")
            result = super().execute(sql, *args, **kwargs)
            if sql.strip().upper() == "COMMIT" and mode[0] == "after":
                raise sqlite3.OperationalError("injected lost commit acknowledgement")
            return result

    def connect(*args, **kwargs):
        kwargs["factory"] = Fault
        return real_connect(*args, **kwargs)

    monkeypatch.setattr(mechanism.sqlite3, "connect", connect)
    with pytest.raises(f.PersistenceFailureV1) as failure:
        o.materialise(request(f))
    assert failure.value.outcome_uncertain is False
    mode[0] = "none"
    assert (
        reader.list_derived_history(
            derived_signal_id="D011",
            subject_instrument="NVDA",
            effective_at_or_before_utc=ASOF,
            knowledge_at_or_before_utc=ASOF,
            limit=100,
        )
        == ()
    )
    mode[0] = "after"
    with pytest.raises(f.PersistenceFailureV1) as failure:
        o.materialise(request(f))
    assert failure.value.outcome_uncertain is True
    mode[0] = "none"
    committed = reader.list_derived_history(
        derived_signal_id="D011",
        subject_instrument="NVDA",
        effective_at_or_before_utc=ASOF,
        knowledge_at_or_before_utc=ASOF,
        limit=100,
    )
    assert len(committed) == 1 and committed[0].calculated_at_utc == NOW
    assert o.materialise(request(f)) == committed[0]
    monkeypatch.undo()
    lock = real_connect(path, isolation_level=None, timeout=0)
    lock.execute("BEGIN IMMEDIATE")
    try:
        with pytest.raises(f.PersistenceFailureV1) as failure:
            o.materialise(request(f, knowledge_cutoff_utc=NOW))
        assert failure.value.outcome_uncertain is False
    finally:
        lock.execute("ROLLBACK")
        lock.close()
    assert o.materialise(request(f)) == committed[0]
    config = configuration(
        f, raw.reads, storage=f.SQLiteStorageV1(str(path), False), versions=(1, 2)
    )
    bad = replace(config["parameter_sets"][0], profile="P_SCORE")
    with pytest.raises(ValueError):
        f.create_owner(**(config | {"parameter_sets": (config["parameter_sets"][1], bad)}))
    assert reader.get_parameter_set(f.VersionRefV1("mmt-pilot-basic", 2)) is None
    with real_connect(path) as connection:
        trigger_name, trigger_sql = connection.execute(
            "SELECT name,sql FROM sqlite_schema WHERE type='trigger' "
            "AND tbl_name='mmt_occurrence_v1' AND upper(sql) LIKE '%BEFORE UPDATE%'"
        ).fetchone()
        connection.execute('DROP TRIGGER "' + trigger_name.replace('"', '""') + '"')
        payload = connection.execute("SELECT payload FROM mmt_occurrence_v1").fetchone()[0]
        document = json.loads(payload)
        document["result"] = {"kind": "decimal", "sign": 0, "digits": "999", "exponent": 0}
        poisoned = json.dumps(
            document, ensure_ascii=True, sort_keys=True, separators=(",", ":")
        ).encode()
        connection.execute(
            "UPDATE mmt_occurrence_v1 SET payload=?,content_sha256=?",
            (poisoned, hashlib.sha256(poisoned).hexdigest()),
        )
        connection.execute(trigger_sql)
    with pytest.raises((ValueError, f.PersistenceFailureV1)):
        o.materialise(request(f))


def test_sqlite_actual_competing_identical_materialisations(tmp_path):
    raw, raw_path = raw_source(tmp_path)
    f = foundation()
    path = tmp_path / "foundation.sqlite"
    second = f.create_owner(
        **configuration(f, raw.reads, storage=f.SQLiteStorageV1(str(path), True))
    )
    code = """
import base64,pickle,sqlite3,sys
from _support import configuration,foundation,request
from nvda_desk.raw_signal_occurrence_truth import api as raw_api
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence
f=foundation()
raw=raw_api.create_owner(durability_port=create_sqlite_persistence(sys.argv[1]))
o=f.create_owner(**configuration(f,raw.reads,storage=f.SQLiteStorageV1(sys.argv[2],False)))
real=sqlite3.connect
class Gate(sqlite3.Connection):
    def execute(self,sql,*args,**kwargs):
        result=super().execute(sql,*args,**kwargs)
        if sql.strip().upper()=="BEGIN IMMEDIATE":
            print("LOCKED",flush=True)
            sys.stdin.readline()
        return result
def connect(*args,**kwargs):
    kwargs["factory"]=Gate
    return real(*args,**kwargs)
sqlite3.connect=connect
result=o.materialise(request(f))
print(base64.b64encode(pickle.dumps(result)).decode(),flush=True)
"""
    child = subprocess.Popen(
        [sys.executable, "-u", "-c", code, str(raw_path), str(path)],
        env=process_env(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        assert child.stdout.readline().strip() == "LOCKED"
        with pytest.raises(f.PersistenceFailureV1) as failure:
            second.materialise(request(f))
        assert failure.value.outcome_uncertain is False
        child.stdin.write("release\n")
        child.stdin.flush()
        first = pickle.loads(base64.b64decode(child.stdout.readline()))
        child.wait(timeout=20)
        assert child.returncode == 0, child.stderr.read()
    finally:
        if child.poll() is None:
            child.kill()
            child.wait(timeout=10)
    assert second.materialise(request(f)) == first
    assert second.reads.list_derived_history(
        derived_signal_id="D011",
        subject_instrument="NVDA",
        effective_at_or_before_utc=ASOF,
        knowledge_at_or_before_utc=ASOF,
        limit=100,
    ) == (first,)


@pytest.mark.parametrize("mutation", ["hash", "index", "owner", "version", "schema", "deleted"])
def test_sqlite_integrity_failure_is_not_missing_input(tmp_path, mutation):
    raw, _ = raw_source(tmp_path)
    f = foundation()
    path = tmp_path / "foundation.sqlite"
    config = configuration(f, raw.reads, storage=f.SQLiteStorageV1(str(path), True))
    o = f.create_owner(**config)
    result = o.materialise(request(f))
    if mutation == "deleted":
        path.unlink()
    else:
        with sqlite3.connect(path) as c:
            if mutation == "owner":
                c.execute("PRAGMA application_id=42")
            elif mutation == "version":
                c.execute("PRAGMA user_version=2")
            elif mutation == "schema":
                c.execute("CREATE TABLE alien(value TEXT)")
            else:
                trigger_name, trigger_sql = c.execute(
                    "SELECT name,sql FROM sqlite_schema WHERE type='trigger' "
                    "AND tbl_name='mmt_occurrence_v1' AND upper(sql) LIKE '%BEFORE UPDATE%'"
                ).fetchone()
                c.execute('DROP TRIGGER "' + trigger_name.replace('"', '""') + '"')
                if mutation == "hash":
                    c.execute("UPDATE mmt_occurrence_v1 SET content_sha256=?", ("0" * 64,))
                else:
                    c.execute("UPDATE mmt_occurrence_v1 SET subject_instrument='OTHER'")
                c.execute(trigger_sql)
    with pytest.raises(f.PersistenceFailureV1):
        o.reads.get_derived_occurrence(result.derived_occurrence_id)
    if mutation == "deleted":
        assert not path.exists()


def test_sqlite_read_facet_and_owner_file_binding(tmp_path):
    raw, raw_path = raw_source(tmp_path)
    f = foundation()
    path = tmp_path / "foundation.sqlite"
    config = configuration(f, raw.reads, storage=f.SQLiteStorageV1(str(path), True))
    o = f.create_owner(**config)
    result = o.materialise(request(f))
    reads = f.create_reader(admission=config["admission"], storage=f.SQLiteReadStorageV1(str(path)))
    assert not any(
        hasattr(reads, name) for name in ("materialise", "register", "execute", "transaction")
    )
    assert reads.get_derived_occurrence(result.derived_occurrence_id) == result
    with pytest.raises(TypeError):
        f.create_owner(**(config | {"storage": f.SQLiteReadStorageV1(str(path))}))
    for bad in (raw_path, tmp_path / "missing.sqlite"):
        with pytest.raises(f.PersistenceFailureV1):
            f.create_reader(admission=config["admission"], storage=f.SQLiteReadStorageV1(str(bad)))
    for bad in (":memory:", "relative.sqlite", "file:" + str(path), str(path) + "?mode=ro"):
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_reader(admission=config["admission"], storage=f.SQLiteReadStorageV1(bad))
    with pytest.raises(f.PersistenceFailureV1):
        f.create_owner(
            **configuration(f, raw.reads, storage=f.SQLiteStorageV1(str(raw_path), False))
        )
    before = path.read_bytes()
    with pytest.raises(f.PersistenceFailureV1):
        f.create_owner(**config)
    assert path.read_bytes() == before
    read_only = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, isolation_level=None)
    read_only.execute("PRAGMA query_only=1")
    with pytest.raises(sqlite3.OperationalError):
        read_only.execute("INSERT INTO mmt_definition_v1 VALUES ('a','b','c',X'00','bad')")
    read_only.close()
