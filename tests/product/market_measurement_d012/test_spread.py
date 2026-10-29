"""D012-P01-P06: literal signed spread through public, versioned durable paths."""

import base64
import hashlib
import importlib
import io
import json
import pickle
import re
import sqlite3
import subprocess
import sys
import tarfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal, Inexact, Rounded, localcontext
from pathlib import Path
from threading import Event

import pytest
from _support import (
    ASOF,
    BRIEF,
    NOW,
    OLD_BRIEF,
    ROOT,
    child_env,
    configuration,
    f,
    fresh_bundle,
    history,
    mapping,
    observation,
    raw_api,
    raw_source,
    request,
)


def inputs(tmp_path, bid="100", ask="102"):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side, value in (("bid", bid), ("ask", ask)):
        raw.commands.admit_raw_observation_occurrence(observation(side, value=Decimal(value)))
    return raw


@pytest.mark.parametrize(
    "bid,ask,expected",
    [
        ("100", "102", "2"),
        ("102", "100", "-2"),
        ("100", "100", "0"),
        ("-2", "-1", "1"),
        ("0", "0", "0"),
    ],
)
def test_d012_public_spread_exact_lineage(tmp_path, bid, ask, expected):
    raw = inputs(tmp_path, bid, ask)
    config = configuration(raw.reads, tmp_path / "measurement.sqlite")
    owner = f.create_owner(**config)
    req = request()
    result = owner.materialise(req)
    assert result is not None and type(result.result) is Decimal
    assert result.result.as_tuple() == Decimal(expected).as_tuple()
    assert result.derived_signal_id == "D012" and result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/v1"
    assert result.implementation_brief_sha256 == BRIEF
    assert result.calculation_definition_version == "D012-SPREAD-1"
    assert re.fullmatch(r"mmt1:[0-9a-f]{64}", result.derived_occurrence_id)
    assert result.units == "price" and result.result_shape == "scalar_decimal"
    assert result.effective_as_of_utc == result.knowledge_cutoff_utc == ASOF
    assert result.calculated_at_utc == NOW and result.subject_instrument == "NVDA"
    assert result.parameter_context_refs == (req.parameter_set_ref, req.input_selection_policy_ref)
    assert result.convention_refs == (f.VersionRefV1("mmt-pilot-price", 1),)
    assert result.predecessor_occurrence_ids == ()
    assert result.universe is result.window is result.supersedes_derived_occurrence_id is None
    assert len(result.raw_input_lineage) == 2
    for item, side, rid, value, seconds in zip(
        result.raw_input_lineage,
        ("bid", "ask"),
        ("R034", "R035"),
        (bid, ask),
        (2, 1),
        strict=True,
    ):
        assert item.raw_signal_id == rid
        assert item.observation_occurrence_id == f"mmt-pilot-{side}-001"
        assert item.event_time_utc == ASOF - timedelta(seconds=seconds)
        assert item.canonical_value.as_tuple() == Decimal(value).as_tuple()
        assert item.projection_mapping_ref == f.VersionRefV1("mmt-pilot-" + side, 1)
        assert item.unit_convention_ref == f.VersionRefV1("mmt-pilot-price", 1)
        assert item.projection == raw.reads.project_raw_value(
            raw_api.RawSignalCatalogueId(rid),
            raw_api.observation_occurrence_id(f"mmt-pilot-{side}-001"),
            mappings=(mapping(side),),
        )
    reads = owner.reads
    assert reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert (
        reads.get_calculation_definition(
            derived_signal_id="D012", calculation_definition_version="D012-SPREAD-1"
        )
        == config["definitions"][0]
    )
    assert history(reads) == (result,)


@pytest.mark.parametrize(
    "mode",
    [
        "missing",
        "subject",
        "provider",
        "units",
        "nonfinite",
        "float",
        "future",
        "receipt",
        "stale",
        "skew",
        "temporal",
        "revision",
        "version",
        "context",
        "unenabled",
        "field",
        "variant",
        "scope",
        "mapping-mismatch",
        "missing-mapping",
        "mapping-version",
        "field-mismatch",
        "variant-mismatch",
        "scope-mismatch",
        "provider-mismatch",
    ],
)
def test_d012_selection_refusal_and_scope(tmp_path, mode):
    raw = raw_source(tmp_path / "raw.sqlite")
    change = {
        "subject": {"subject_instrument": "OTHER"},
        "provider": {"source_provider": raw_api.provider_id("other")},
        "nonfinite": {"value": Decimal("NaN")},
        "float": {"value": 100.0},
        "future": {"event": NOW},
        "receipt": {"receipt": NOW},
        "stale": {"event": ASOF - timedelta(seconds=60, microseconds=1)},
        "skew": {"event": ASOF - timedelta(seconds=11, microseconds=1)},
        "temporal": {"source_temporal_kind": "date_only", "source_timestamp_raw": "2026-10-16"},
        "revision": {"revision_vintage_native": "revision"},
        "field": {"native_record": {"quote": {"other": Decimal("100")}}},
        "variant": {"source_variant": "other"},
        "scope": {"ingestion_sequence_scope": raw_api.ingestion_sequence_scope("other")},
    }.get(mode, {})
    if mode != "missing":
        raw.commands.admit_raw_observation_occurrence(observation("bid", **change))
    raw.commands.admit_raw_observation_occurrence(observation("ask"))

    class Reader:
        def list_projected_raw_history(self, rid, **kwargs):
            page = raw.reads.list_projected_raw_history(rid, **kwargs)
            if mode == "units" and rid.value == "R034":
                return replace(
                    page, items=tuple(replace(x, native_units="shares") for x in page.items)
                )
            if mode == "mapping-mismatch" and rid.value == "R034":
                return replace(
                    page, items=tuple(replace(x, projection_mapping_id="other") for x in page.items)
                )
            metadata = {
                "mapping-version": {"projection_mapping_version": 2},
                "field-mismatch": {"native_field_path": ("quote", "other")},
                "variant-mismatch": {"source_variant": "other"},
                "scope-mismatch": {
                    "ingestion_sequence_scope": raw_api.ingestion_sequence_scope("other")
                },
                "provider-mismatch": {"source_provider": "other"},
            }.get(mode)
            if metadata is not None and rid.value == "R034":
                return replace(page, items=tuple(replace(x, **metadata) for x in page.items))
            return page

    owner = f.create_owner(**configuration(Reader(), tmp_path / "measurement.sqlite"))
    req = request(2) if mode == "version" else request()
    if mode == "context":
        req = request(context_refs=(f.VersionRefV1("strategy", 1),))
    if mode == "missing-mapping":
        req = replace(
            req,
            raw_input_bindings=(
                replace(
                    req.raw_input_bindings[0], projection_mapping_ref=f.VersionRefV1("absent", 1)
                ),
                req.raw_input_bindings[1],
            ),
        )
    identities = [f"D{i:03d}" for i in range(1, 210) if i not in (11, 12)]
    if mode == "unenabled":
        for identity in identities:
            assert owner.materialise(replace(req, derived_signal_id=identity)) is None
    else:
        assert owner.materialise(req) is None
    assert history(owner.reads) == ()


@pytest.mark.parametrize(
    "bid_seconds,ask_seconds,expected",
    [
        (60, 50, "2"),
        (11, 1, "2"),
        (60.000001, 50, None),
        (11.000001, 1, None),
    ],
)
def test_d012_inclusive_time_boundaries(tmp_path, bid_seconds, ask_seconds, expected):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side, seconds in (("bid", bid_seconds), ("ask", ask_seconds)):
        raw.commands.admit_raw_observation_occurrence(
            observation(side, event=ASOF - timedelta(seconds=seconds))
        )
    owner = f.create_owner(**configuration(raw.reads, tmp_path / "measurement.sqlite"))
    result = owner.materialise(request())
    if expected is None:
        assert result is None and history(owner.reads) == ()
    else:
        assert result.result == Decimal(expected)


def test_d012_latest_eligible_real_multipage_history(tmp_path):
    raw = raw_source(tmp_path / "raw.sqlite")
    raw.commands.admit_raw_observation_occurrence(observation("ask", sequence=0))
    for index in range(1, 103):
        raw.commands.admit_raw_observation_occurrence(
            observation(
                "bid",
                identity=f"history-{index}",
                sequence=index,
                event=ASOF - timedelta(seconds=3 if index < 101 else 2),
                value=Decimal("100") if index < 102 else 999.0,
            )
        )
    raw.commands.admit_raw_observation_occurrence(
        observation(
            "bid",
            identity="late-after",
            sequence=103,
            event=ASOF - timedelta(seconds=1),
            receipt=NOW,
            value=Decimal("999"),
        )
    )
    calls = []

    class Reader:
        def list_projected_raw_history(self, rid, **kwargs):
            calls.append((rid.value, kwargs["cursor"]))
            return raw.reads.list_projected_raw_history(rid, **kwargs)

    owner = f.create_owner(**configuration(Reader(), tmp_path / "measurement.sqlite"))
    result = owner.materialise(request())
    assert result.result == Decimal("2")
    assert result.raw_input_lineage[0].observation_occurrence_id == "history-101"
    assert [cursor for rid, cursor in calls if rid == "R034"] == [None, "100"]
    raw.commands.admit_raw_observation_occurrence(
        observation(
            "bid",
            identity="late-before",
            sequence=104,
            event=ASOF - timedelta(seconds=1),
            receipt=ASOF,
            value=Decimal("104"),
        )
    )
    assert owner.materialise(request()).result == Decimal("-2")


@pytest.mark.parametrize(
    "mode",
    [
        "identical",
        "unrelated",
        "units",
        "nonfinite",
        "stale",
        "receipt",
        "representation",
        "repeat",
    ],
)
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("cross_page", [False, True])
def test_d012_duplicate_consistency_and_pagination(tmp_path, mode, reverse, cross_page):
    raw = inputs(tmp_path)

    class Reader:
        def list_projected_raw_history(self, rid, **kwargs):
            page = raw.reads.list_projected_raw_history(rid, **(kwargs | {"cursor": None}))
            if rid.value == "R035":
                return page
            good = page.items[0]
            other = good
            if mode in {"units", "unrelated"}:
                other = replace(good, native_units="shares")
            if mode == "nonfinite":
                other = replace(good, native_value=Decimal("NaN"))
            if mode == "stale":
                other = replace(good, source_timestamp_raw="2026-10-16T00:58:00Z")
            if mode == "receipt":
                other = replace(good, received_ts_utc=NOW)
            if mode == "representation":
                other = replace(good, native_value=Decimal("100.0"))
            if mode == "unrelated":
                other = replace(
                    other, observation_occurrence_id=raw_api.observation_occurrence_id("unrelated")
                )
            pair = (other, good) if reverse else (good, other)
            if mode == "repeat":
                return replace(page, next_cursor="1")
            if cross_page:
                return raw_api.ProjectedRawHistoryPageV1(
                    pair[:1] if kwargs["cursor"] is None else pair[1:],
                    "1" if kwargs["cursor"] is None else None,
                )
            return raw_api.ProjectedRawHistoryPageV1(pair, None)

    owner = f.create_owner(**configuration(Reader(), tmp_path / "measurement.sqlite"))
    result = owner.materialise(request())
    if mode in {"identical", "unrelated"}:
        assert result.result == Decimal("2")
    else:
        assert result is None and history(owner.reads) == ()


@pytest.mark.parametrize(
    "bid,ask,expected",
    [
        ("100.00", "102.0", "2.00"),
        ("-2.00", "-1.0", "1.00"),
        ("-0.000", "0.00", "0.000"),
        ("1E+10", "0.001", "-9999999999.999"),
        (
            "100.123456789012345678901234567890",
            "102.000000000000000000000000000000",
            "1.876543210987654321098765432110",
        ),
    ],
)
def test_d012_exact_decimal_context_independence(tmp_path, bid, ask, expected):
    raw = inputs(tmp_path, bid, ask)
    owner = f.create_owner(**configuration(raw.reads, tmp_path / "measurement.sqlite"))
    with localcontext() as context:
        context.prec = 2
        context.traps[Inexact] = context.traps[Rounded] = True
        result = owner.materialise(request())
    assert result.result.as_tuple() == Decimal(expected).as_tuple()
    assert result.raw_input_lineage[0].canonical_value.as_tuple() == Decimal(bid).as_tuple()
    assert owner.materialise(request()) == result


def test_d012_identity_versions_and_later_clock_retry(tmp_path):
    raw = inputs(tmp_path)
    clock = [NOW]
    config = configuration(
        raw.reads,
        tmp_path / "measurement.sqlite",
        versions=(1, 2),
        identities=("D011", "D012"),
        now=lambda: clock[0],
    )
    owner = f.create_owner(**config)
    first = owner.materialise(request())
    clock[0] += timedelta(days=1)
    assert owner.materialise(request()) == first
    assert first.calculated_at_utc == NOW
    second = owner.materialise(request(2))
    cutoff = owner.materialise(request(knowledge_cutoff_utc=NOW))
    midpoint = owner.materialise(request(identity="D011"))
    assert first.result == second.result == cutoff.result == Decimal("2")
    assert midpoint.result == Decimal("101")
    assert len({x.derived_occurrence_id for x in (first, second, cutoff, midpoint)}) == 4
    # Change each version dimension alone; combined v2 cannot prove all members.
    base = request()
    variants = (
        replace(base, calculation_definition_version="D012-SPREAD-2"),
        replace(base, parameter_set_ref=f.VersionRefV1("mmt-pilot-basic", 2)),
        replace(base, input_selection_policy_ref=f.VersionRefV1("mmt-pilot-selection", 2)),
        replace(
            base,
            raw_input_bindings=(
                replace(
                    base.raw_input_bindings[0],
                    projection_mapping_ref=f.VersionRefV1("mmt-pilot-bid", 2),
                ),
                base.raw_input_bindings[1],
            ),
        ),
        replace(
            base,
            raw_input_bindings=(
                base.raw_input_bindings[0],
                replace(
                    base.raw_input_bindings[1],
                    projection_mapping_ref=f.VersionRefV1("mmt-pilot-ask", 2),
                ),
            ),
        ),
        replace(
            base,
            raw_input_bindings=tuple(
                replace(binding, unit_convention_ref=f.VersionRefV1("mmt-pilot-price", 2))
                for binding in base.raw_input_bindings
            ),
        ),
    )
    isolated = tuple(owner.materialise(req) for req in variants)
    assert all(item.result == Decimal("2") for item in isolated)
    assert (
        len({x.derived_occurrence_id for x in (first, second, cutoff, midpoint, *isolated)}) == 10
    )
    for req, item in zip(variants, isolated, strict=True):
        assert item.calculation_definition_version == req.calculation_definition_version
        assert item.parameter_context_refs == (
            req.parameter_set_ref,
            req.input_selection_policy_ref,
        )
        assert tuple(x.projection_mapping_ref for x in item.raw_input_lineage) == tuple(
            x.projection_mapping_ref for x in req.raw_input_bindings
        )
        assert tuple(x.unit_convention_ref for x in item.raw_input_lineage) == tuple(
            x.unit_convention_ref for x in req.raw_input_bindings
        )
        assert owner.reads.get_derived_occurrence(item.derived_occurrence_id) == item
    raw.commands.admit_raw_observation_occurrence(
        observation(
            "bid", identity="changed", sequence=3, event=ASOF, receipt=ASOF, value=Decimal("104")
        )
    )
    changed = owner.materialise(request())
    assert (
        changed.result == Decimal("-2")
        and changed.derived_occurrence_id != first.derived_occurrence_id
    )
    for item in (first, second, cutoff, changed):
        assert owner.reads.get_derived_occurrence(item.derived_occurrence_id) == item
    assert len(history(owner.reads)) == 10 and len(history(owner.reads, "D011")) == 1
    assert owner.reads.get_derived_occurrence("unknown") is None
    assert owner.reads.get_parameter_set(f.VersionRefV1("absent", 1)) is None
    bad = config | {
        "storage": f.SQLiteStorageV1(str(tmp_path / "measurement.sqlite"), False),
        "definitions": (replace(config["definitions"][-1], equation="abs(R035-R034)"),),
    }
    with pytest.raises(ValueError):
        f.create_owner(**bad)
    old = configuration(raw.reads, tmp_path / "old.sqlite", identities=("D011",), brief=OLD_BRIEF)
    legacy = f.create_owner(**old)
    assert legacy.materialise(request()) is None
    with pytest.raises(ValueError):
        f.create_owner(
            **(old | {"storage": f.MemoryStorageV1(), "definitions": (config["definitions"][2],)})
        )


def test_d012_sqlite_fresh_process_and_failure_recovery(tmp_path, monkeypatch):
    raw = inputs(tmp_path)
    path = tmp_path / "measurement.sqlite"
    config = configuration(raw.reads, path)
    owner = f.create_owner(**config)
    mechanism = importlib.import_module("nvda_desk.market_measurement_truth._sqlite")
    real_connect = sqlite3.connect
    mode = ["before"]
    reached = []

    class Fault(sqlite3.Connection):
        wrote = False

        def execute(self, sql, *args, **kwargs):
            statement = sql.strip().upper()
            if statement == "COMMIT" and self.wrote and mode[0] == "before":
                reached.append("before")
                raise sqlite3.OperationalError("precommit fault")
            result = super().execute(sql, *args, **kwargs)
            if statement.startswith("INSERT") and "MMT_OCCURRENCE_V1" in statement:
                self.wrote = True
            if statement == "COMMIT" and self.wrote and mode[0] == "after":
                reached.append("after")
                raise sqlite3.OperationalError("lost acknowledgement")
            return result

    def connect(*args, **kwargs):
        if str(args[0]).startswith(path.as_uri() + "?"):
            kwargs["factory"] = Fault
        return real_connect(*args, **kwargs)

    monkeypatch.setattr(mechanism.sqlite3, "connect", connect)
    with pytest.raises(f.PersistenceFailureV1) as failed:
        owner.materialise(request())
    assert failed.value.outcome_uncertain is False and reached == ["before"]
    mode[0] = "none"
    assert history(owner.reads) == ()
    mode[0] = "after"
    with pytest.raises(f.PersistenceFailureV1) as uncertain:
        owner.materialise(request())
    assert uncertain.value.outcome_uncertain is True and reached == ["before", "after"]
    mode[0] = "none"
    committed = history(owner.reads)[0]
    assert committed.result == Decimal("2") and owner.materialise(request()) == committed
    monkeypatch.undo()
    # A separate public writer process creates its own store and exits before
    # the read-only child receives just the durable path, digest and identity.
    writer_code = """
import base64,pickle,sys
from _support import configuration,f,raw_api,request
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence
raw=raw_api.create_owner(durability_port=create_sqlite_persistence(sys.argv[1]))
o=f.create_owner(**configuration(raw.reads,sys.argv[2]))
r=o.materialise(request())
print(base64.b64encode(pickle.dumps(r)).decode())
"""
    exited_path = tmp_path / "writer-exited.sqlite"
    writer = subprocess.run(
        [sys.executable, "-c", writer_code, str(tmp_path / "raw.sqlite"), str(exited_path)],
        env=child_env(),
        text=True,
        capture_output=True,
        timeout=20,
    )
    assert writer.returncode == 0, writer.stderr
    exited = pickle.loads(base64.b64decode(writer.stdout))
    assert exited.result == Decimal("2")
    assert fresh_bundle(exited_path, exited.derived_occurrence_id)["occurrence"] == exited
    bundle = fresh_bundle(path, committed.derived_occurrence_id)
    assert bundle == dict(
        occurrence=committed,
        definition=config["definitions"][0],
        parameter=config["parameter_sets"][0],
        selection=config["input_selection_policies"][0],
        units=config["unit_conventions"],
        mappings=config["raw_projection_mappings"],
        history=(committed,),
    )
    contender = f.create_owner(**configuration(raw.reads, path, create=False))
    lock = real_connect(path, isolation_level=None, timeout=0)
    lock.execute("BEGIN IMMEDIATE")
    try:
        with pytest.raises(f.PersistenceFailureV1) as busy:
            contender.materialise(request())
        assert busy.value.outcome_uncertain is False
    finally:
        lock.execute("ROLLBACK")
        lock.close()
    assert contender.materialise(request()) == committed and len(history(contender.reads)) == 1
    # Rehash wrong-equation content: integrity must include meaning, not just a digest.
    with real_connect(path) as c:
        name, trigger = c.execute(
            "SELECT name,sql FROM sqlite_schema WHERE type='trigger' "
            "AND tbl_name='mmt_occurrence_v1' AND upper(sql) LIKE '%BEFORE UPDATE%'"
        ).fetchone()
        c.execute('DROP TRIGGER "' + name + '"')
        doc = json.loads(c.execute("SELECT payload FROM mmt_occurrence_v1").fetchone()[0])
        doc["result"] = {"kind": "decimal", "sign": 0, "digits": "101", "exponent": 0}
        payload = json.dumps(doc, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()
        c.execute(
            "UPDATE mmt_occurrence_v1 SET payload=?,content_sha256=?",
            (payload, hashlib.sha256(payload).hexdigest()),
        )
        c.execute(trigger)
    with pytest.raises((ValueError, f.PersistenceFailureV1)):
        f.create_reader(admission=config["admission"], storage=f.SQLiteReadStorageV1(str(path)))


def test_d012_competing_identical_first_public_writes(tmp_path, monkeypatch):
    raw = inputs(tmp_path)
    path = tmp_path / "measurement.sqlite"
    first = f.create_owner(**configuration(raw.reads, path))
    second = f.create_owner(
        **configuration(raw.reads, path, create=False, now=lambda: NOW + timedelta(days=1))
    )
    inserted, release = Event(), Event()
    original = sqlite3.connect
    mechanism = importlib.import_module("nvda_desk.market_measurement_truth._sqlite")

    class Barrier(sqlite3.Connection):
        def execute(self, sql, *args, **kwargs):
            value = super().execute(sql, *args, **kwargs)
            if sql.upper().startswith("INSERT INTO MMT_OCCURRENCE_V1"):
                inserted.set()
                assert release.wait(timeout=10), "public first writer was not released"
            return value

    def connect(*args, **kwargs):
        if str(args[0]).startswith(path.as_uri() + "?"):
            kwargs["factory"] = Barrier
        return original(*args, **kwargs)

    monkeypatch.setattr(mechanism.sqlite3, "connect", connect)
    assert history(first.reads) == ()
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(first.materialise, request())
        try:
            assert inserted.wait(timeout=10), "first public call did not reach native INSERT"
            assert history(second.reads) == ()  # first tentative fact is still uncommitted
            with pytest.raises(f.PersistenceFailureV1) as contention:
                second.materialise(request())
            assert contention.value.outcome_uncertain is False
        finally:
            release.set()
        committed = pending.result(timeout=20)
    monkeypatch.undo()
    assert committed.result == Decimal("2") and committed.calculated_at_utc == NOW
    assert second.materialise(request()) == committed
    assert history(second.reads) == (committed,)


@pytest.mark.parametrize("mode", ["payload", "hash", "index", "owner"])
def test_d012_separate_durable_integrity_falsifiers(tmp_path, mode):
    raw = inputs(tmp_path)
    path = tmp_path / "measurement.sqlite"
    config = configuration(raw.reads, path)
    owner = f.create_owner(**config)
    fact = owner.materialise(request())
    assert fact.result == Decimal("2")
    with sqlite3.connect(path) as connection:
        if mode == "owner":
            connection.execute("PRAGMA application_id=1314258945")
        else:
            name, sql = connection.execute(
                "SELECT name,sql FROM sqlite_schema WHERE type='trigger' "
                "AND tbl_name='mmt_occurrence_v1' AND upper(sql) LIKE '%BEFORE UPDATE%'"
            ).fetchone()
            connection.execute('DROP TRIGGER "' + name + '"')
            if mode == "payload":
                payload = connection.execute("SELECT payload FROM mmt_occurrence_v1").fetchone()[0]
                connection.execute("UPDATE mmt_occurrence_v1 SET payload=?", (payload + b" ",))
            elif mode == "hash":
                connection.execute("UPDATE mmt_occurrence_v1 SET content_sha256=?", ("0" * 64,))
            else:
                connection.execute("UPDATE mmt_occurrence_v1 SET subject_instrument='OTHER'")
            connection.execute(sql)
    with pytest.raises((ValueError, f.PersistenceFailureV1)):
        f.create_reader(admission=config["admission"], storage=f.SQLiteReadStorageV1(str(path)))


def test_d012_legacy_d011_and_public_type_compatibility(tmp_path):
    folder = Path(__file__).parent / "typing"
    config = tmp_path / "mypy.ini"
    config.write_text("[mypy]\npython_version=3.12\nfollow_untyped_imports=True\n")
    command = [
        sys.executable,
        "-m",
        "mypy",
        "--config-file",
        str(config),
        "--strict",
        "--disallow-any-expr",
        "--cache-dir",
        str(tmp_path / "type-cache"),
    ]
    good = subprocess.run(
        [*command, str(folder / "valid_seam.py")], text=True, capture_output=True, timeout=60
    )
    assert good.returncode == 0, good.stdout + good.stderr
    bad_path = folder / "invalid_seam.py"
    expected = {
        (line, re.search(r"MISUSE\[([^]]+)\]", text)[1])
        for line, text in enumerate(bad_path.read_text().splitlines(), 1)
        if "MISUSE[" in text
    }
    bad = subprocess.run([*command, str(bad_path)], text=True, capture_output=True, timeout=60)
    observed = re.findall(r"invalid_seam.py:(\d+): error: .* \[([^]]+)\]", bad.stdout)
    assert bad.returncode == 1 and not bad.stderr
    assert {(int(line), code) for line, code in observed} == expected and len(observed) == 4
    assert bad.stdout.count("error:") == 4
    # Construct isolated old store using exact predecessor source, then public read from new source.
    baseline = "b83a1a071153d3bdff7f0aa1b6b49bcd3c90ceb2"
    archive = subprocess.run(
        ["git", "archive", "--format=tar", baseline, "src"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    previous = tmp_path / "predecessor"
    previous.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
        stream.extractall(previous, filter="data")
    code = """
import base64,pickle,sys
from _support import OLD_BRIEF,configuration,observation,raw_api,f,request
raw=raw_api.create_owner()
for side in ('bid','ask'): raw.commands.admit_raw_observation_occurrence(observation(side))
o=f.create_owner(**configuration(raw.reads,sys.argv[1],identities=('D011',),brief=OLD_BRIEF))
r=o.materialise(request(identity='D011'))
print(base64.b64encode(pickle.dumps(r)).decode())
"""
    old_path = tmp_path / "old.sqlite"
    proc = subprocess.run(
        [sys.executable, "-c", code, str(old_path)],
        env=child_env(previous),
        text=True,
        capture_output=True,
        timeout=20,
    )
    assert proc.returncode == 0, proc.stderr
    old = pickle.loads(base64.b64decode(proc.stdout))
    assert old.result == Decimal("101") and old.implementation_brief_sha256 == OLD_BRIEF
    recovered = fresh_bundle(old_path, old.derived_occurrence_id, brief=OLD_BRIEF)
    assert recovered["occurrence"] == old and recovered["history"] == (old,)
