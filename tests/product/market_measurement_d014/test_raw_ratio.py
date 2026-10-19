"""D014-P01-P06: authority-derived direct-raw exact-ratio falsifiers, before behaviour."""

import ast
import base64
import hashlib
import importlib
import json
import os
import pickle
import re
import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError, fields, is_dataclass, replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal, Inexact, Rounded, localcontext
from pathlib import Path
from threading import Event

import pytest
from _support import (
    ASOF,
    AUTHORITY,
    BRIEF,
    NOW,
    ROOT,
    configuration,
    f,
    mapping,
    observation,
    raw_api,
    raw_source,
    request,
)


def seam():
    # Tests establish real public M00 readiness first; missing behaviour is an
    # assertion, not a top-level import error or a passing absence placeholder.
    assert hasattr(f, "create_raw_ratio_owner"), "admitted additive D014 raw-ratio seam is absent"
    for name in (
        "RawRatioOccurrenceV1",
        "MeasurementRawRatioReadsV1",
        "MeasurementRawRatioOwnerV1",
        "create_raw_ratio_reader",
    ):
        assert hasattr(f, name), name


def integer_text(number):
    """Independent unbounded decimal wire oracle, not production serialization."""
    if number == 0:
        return "0"
    sign = "-" if number < 0 else ""
    number = abs(number)
    digits = []
    while number:
        number, digit = divmod(number, 10)
        digits.append(chr(48 + digit))
    return sign + "".join(reversed(digits))


def tagged(value):
    for kind, exemplar in (
        ("RawSignalCatalogueId", raw_api.RawSignalCatalogueId("R033")),
        ("observation_occurrence_id", raw_api.observation_occurrence_id("id")),
        ("ingestion_sequence_scope", raw_api.ingestion_sequence_scope("scope")),
    ):
        if type(value) is type(exemplar):
            return dict(kind=kind, value=value.value)
    if type(value) is Decimal:
        part = value.as_tuple()
        return dict(
            kind="decimal",
            sign=part.sign,
            digits="".join(chr(48 + n) for n in part.digits),
            exponent=part.exponent,
        )
    if type(value) is f.ExactRatioV1:
        return dict(
            kind="exact_ratio",
            numerator=integer_text(value.numerator),
            denominator=integer_text(value.denominator),
        )
    if type(value) is datetime:
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if type(value) is timedelta:
        return (value.days * 86400 + value.seconds) * 1000000 + value.microseconds
    if is_dataclass(value):
        return {field.name: tagged(getattr(value, field.name)) for field in fields(value)}
    if type(value) is tuple:
        return [tagged(item) for item in value]
    if type(value) is dict:
        return {key: tagged(item) for key, item in value.items()}
    assert value is None or type(value) in (str, bool, int)
    return value


def canonical(value):
    return json.dumps(
        tagged(value), sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False
    ).encode()


def history(reads, **changes):
    return reads.list_derived_history(
        **(
            dict(
                derived_signal_id="D014",
                subject_instrument="NVDA",
                effective_at_or_before_utc=NOW + timedelta(days=2),
                knowledge_at_or_before_utc=NOW + timedelta(days=2),
                limit=1000,
            )
            | changes
        )
    )


def assert_ratio(fact, numerator, denominator):
    assert fact is not None and type(fact) is f.RawRatioOccurrenceV1
    assert type(fact.result) is f.ExactRatioV1
    assert type(fact.result.numerator) is type(fact.result.denominator) is int
    assert fact.result.numerator == numerator and fact.result.denominator == denominator


def unsafe_copy(record, **changes):
    clone = object.__new__(type(record))
    for field in fields(record):
        object.__setattr__(clone, field.name, changes.get(field.name, getattr(record, field.name)))
    return clone


def assert_config_reads(reads, config):
    for definition in config["definitions"]:
        assert (
            reads.get_calculation_definition(
                derived_signal_id="D014",
                calculation_definition_version=definition.calculation_definition_version,
            )
            == definition
        )
    for key, getter in (
        ("parameter_sets", reads.get_parameter_set),
        ("input_selection_policies", reads.get_input_selection_policy),
        ("unit_conventions", reads.get_unit_convention),
        ("raw_projection_mappings", reads.get_projection_mapping),
    ):
        for item in config[key]:
            identity = item.mapping_id if key == "raw_projection_mappings" else item.context_id
            assert getter(f.VersionRefV1(identity, item.version)) == item


@pytest.mark.parametrize("storage", ["memory", "sqlite"])
def test_d014_actual_raw_projections_exact_ratio(tmp_path, storage):
    # An independent real producer check precedes even the missing-seam guard.
    probe = raw_source(tmp_path / "probe.sqlite")
    for side, rid in (("bid", "R033"), ("ask", "R036")):
        item = observation(side)
        probe.commands.admit_raw_observation_occurrence(item)
        projected = probe.reads.project_raw_value(
            raw_api.RawSignalCatalogueId(rid),
            item.observation_occurrence_id,
            mappings=(mapping(side),),
        )
        assert (
            projected.native_value.as_tuple() == Decimal("2" if side == "bid" else "1").as_tuple()
        )
    seam()
    # No fixture has pre-satisfied this owner's absence→admission transition.
    raw = raw_source(tmp_path / "raw.sqlite")
    config = configuration(raw.reads, tmp_path / "ratio.sqlite")
    if storage == "memory":
        config["storage"] = f.MemoryStorageV1()
    owner = f.create_raw_ratio_owner(**config)
    req = request()
    assert history(owner.reads) == ()
    assert owner.materialise(req) is None
    assert history(owner.reads) == ()
    assert (
        raw.reads.project_raw_value(
            raw_api.RawSignalCatalogueId("R033"),
            raw_api.observation_occurrence_id("mmt-size-bid-001"),
            mappings=(mapping("bid"),),
        )
        is None
    )
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    fact = owner.materialise(req)
    assert_ratio(fact, 1, 3)
    assert fact.owner_object_id == "M02"
    assert fact.owner_namespace == "neutral_market_measurement_truth/raw_exact_ratio/v1"
    assert fact.implementation_brief_sha256 == BRIEF
    assert fact.derived_signal_id == "D014" and fact.subject_instrument == "NVDA"
    assert fact.calculation_definition_version == "D014-SIZE-IMBALANCE-1"
    assert fact.effective_as_of_utc == fact.knowledge_cutoff_utc == ASOF
    assert fact.calculated_at_utc == NOW
    assert fact.units == "-1 to 1" and fact.result_shape == "scalar_exact_ratio"
    assert fact.predecessor_occurrence_ids == ()
    assert fact.parameter_context_refs == (req.parameter_set_ref, req.input_selection_policy_ref)
    assert fact.convention_refs == (f.VersionRefV1("mmt-size-shares", 1),)
    assert fact.universe is fact.window is fact.supersedes_derived_occurrence_id is None
    assert len(fact.raw_input_lineage) == 2
    for lineage, side, rid, number, seconds in zip(
        fact.raw_input_lineage,
        ("bid", "ask"),
        ("R033", "R036"),
        ("2", "1"),
        (2, 1),
        strict=True,
    ):
        assert type(lineage) is f.RawInputLineageV1
        assert lineage.raw_signal_id == rid
        assert lineage.observation_occurrence_id == "mmt-size-" + side + "-001"
        assert lineage.event_time_utc == ASOF - timedelta(seconds=seconds)
        assert lineage.canonical_value == Decimal(number)
        assert lineage.projection.native_value.as_tuple() == Decimal(number).as_tuple()
        assert lineage.projection_mapping_ref == f.VersionRefV1("mmt-size-" + side, 1)
        assert lineage.unit_convention_ref == f.VersionRefV1("mmt-size-shares", 1)
        assert lineage.projection == raw.reads.project_raw_value(
            raw_api.RawSignalCatalogueId(rid),
            raw_api.observation_occurrence_id(lineage.observation_occurrence_id),
            mappings=(mapping(side),),
        )
    definition_hash = hashlib.sha256(canonical(config["definitions"][0])).hexdigest()
    logical = dict(
        owner_object_id="M02",
        owner_namespace=fact.owner_namespace,
        implementation_brief_sha256=BRIEF,
        request=req,
        definition_content_sha256=definition_hash,
        parameter_set=config["parameter_sets"][0],
        input_selection_policy=config["input_selection_policies"][0],
        unit_conventions=(config["unit_conventions"][0],),
        projection_mappings=tuple(mapping(side) for side in ("bid", "ask")),
        raw_input_lineage=fact.raw_input_lineage,
    )
    assert fact.definition_content_sha256 == definition_hash
    assert fact.derived_occurrence_id == "mmtraw1:" + hashlib.sha256(canonical(logical)).hexdigest()
    assert owner.reads.get_derived_occurrence(fact.derived_occurrence_id) == fact
    assert history(owner.reads) == (fact,)
    assert_config_reads(owner.reads, config)
    assert not hasattr(owner.reads, "materialise")


REFUSALS = (
    "missing",
    "wrong-page",
    "wrong-items",
    "wrong-type",
    "provider",
    "variant",
    "subject",
    "units",
    "field",
    "mapping",
    "mapping-version",
    "rid",
    "float",
    "nonfinite",
    "scope",
    "sequence-bool",
    "identity-type",
    "selection-identity",
    "revision",
    "temporal",
    "timezone",
    "timestamp-type",
    "timestamp-format",
    "future",
    "receipt",
    "event-after-receipt",
    "stale",
    "skew",
    "ambiguous",
    "duplicate-content",
    "cursor",
    "repeated-cursor",
    "empty-cursor",
    "oversized-page",
    "page-cap",
    "order",
    "binding-rid",
    "binding-subject",
    "binding-mapping",
    "binding-unit",
    "binding-unit-incompatible",
    "context",
    "definition",
    "profile",
    "selection",
    "request-subject",
    "asof-after-cutoff",
    "cutoff-after-clock",
    "unsupported-all",
    "storage-error",
)
POSITIVES = (
    "duplicate-identical",
    "inclusive-freshness",
    "inclusive-skew",
    "real-multipage",
    "newer-invalid",
    "late-receipt",
    "identical-cross-page",
)
DUPLICATE_CASES = {
    "dup-provider-forward-page": ("provider", False, False),
    "dup-provider-reverse-page": ("provider", True, False),
    "dup-provider-forward-cross": ("provider", False, True),
    "dup-provider-reverse-cross": ("provider", True, True),
    "dup-representation-forward-page": ("representation", False, False),
    "dup-representation-reverse-page": ("representation", True, False),
    "dup-representation-forward-cross": ("representation", False, True),
    "dup-representation-reverse-cross": ("representation", True, True),
    "dup-stale-forward-page": ("stale", False, False),
    "dup-stale-reverse-page": ("stale", True, False),
    "dup-stale-forward-cross": ("stale", False, True),
    "dup-stale-reverse-cross": ("stale", True, True),
    "dup-receipt-forward-page": ("receipt", False, False),
    "dup-receipt-reverse-page": ("receipt", True, False),
    "dup-receipt-forward-cross": ("receipt", False, True),
    "dup-receipt-reverse-cross": ("receipt", True, True),
}


@pytest.mark.parametrize("populated", [False, True])
@pytest.mark.parametrize("mode", REFUSALS + POSITIVES + tuple(DUPLICATE_CASES))
def test_d014_selection_and_refusal(tmp_path, populated, mode):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    if mode == "real-multipage":
        for index in range(101):
            raw.commands.admit_raw_observation_occurrence(
                observation(
                    "bid",
                    identity="older-" + str(index),
                    sequence=index + 3,
                    event=ASOF - timedelta(seconds=3),
                    value=Decimal("99"),
                )
            )
    if mode in ("newer-invalid", "late-receipt"):
        raw.commands.admit_raw_observation_occurrence(
            observation(
                "bid",
                identity="newer-unavailable",
                sequence=200,
                event=ASOF,
                receipt=NOW if mode == "late-receipt" else ASOF,
                value=Decimal("99") if mode == "late-receipt" else 99.0,
            )
        )
    seam()
    active = [False]
    calls = []
    synthetic_cursor_modes = ("cursor", "repeated-cursor", "empty-cursor", "page-cap")
    page_seed = (
        raw.reads.project_raw_value(
            raw_api.RawSignalCatalogueId("R033"),
            raw_api.observation_occurrence_id("mmt-size-bid-001"),
            mappings=(mapping("bid"),),
        )
        if mode in synthetic_cursor_modes
        else None
    )

    class Reader:
        def list_projected_raw_history(self, rid, **kwargs):
            calls.append((rid.value, kwargs.get("cursor")))
            if active[0] and rid.value == "R033" and mode in synthetic_cursor_modes:
                # These are generated adversarial pages, not native offset
                # cursors. Keep their real public seed independent of exhausting
                # the one-record M00 history on the second fabricated cursor.
                assert type(page_seed) is raw_api.ProjectedRawValueV1
                cursor = kwargs.get("cursor")
                nxt = "bad" if mode == "cursor" else str(int(cursor or "0") + 1)
                if mode == "repeated-cursor":
                    nxt = "1"
                return raw_api.ProjectedRawHistoryPageV1(
                    () if mode == "empty-cursor" else (page_seed,), nxt
                )
            page = raw.reads.list_projected_raw_history(rid, **kwargs)
            if (
                active[0]
                and rid.value == "R033"
                and (mode in DUPLICATE_CASES or mode == "identical-cross-page")
            ):
                first = raw.reads.project_raw_value(
                    rid,
                    raw_api.observation_occurrence_id("mmt-size-bid-001"),
                    mappings=kwargs["mappings"],
                )
                if mode == "identical-cross-page":
                    pair, cross_page = (first, first), True
                else:
                    dimension, reverse, cross_page = DUPLICATE_CASES[mode]
                    changed = replace(
                        first,
                        **{
                            "provider": dict(source_provider="OTHER"),
                            "representation": dict(native_value=Decimal("2.0")),
                            "stale": dict(source_timestamp_raw="2026-10-16T00:58:59Z"),
                            "receipt": dict(received_ts_utc=NOW),
                        }[dimension],
                    )
                    pair = (changed, first) if reverse else (first, changed)
                if cross_page:
                    start = kwargs.get("cursor") is None
                    return replace(
                        page, items=(pair[0 if start else 1],), next_cursor="1" if start else None
                    )
                return replace(page, items=pair, next_cursor=None)
            if active[0] and mode in ("inclusive-freshness", "inclusive-skew"):
                seconds = (
                    (60 if rid.value == "R033" else 50)
                    if mode == "inclusive-freshness"
                    else (11 if rid.value == "R033" else 1)
                )
                return replace(
                    page,
                    items=tuple(
                        replace(
                            item,
                            source_timestamp_raw=(ASOF - timedelta(seconds=seconds))
                            .isoformat()
                            .replace("+00:00", "Z"),
                        )
                        for item in page.items
                    ),
                )
            if not active[0] or rid.value != "R033":
                return page
            first = page.items[0]
            changes = {
                "provider": dict(source_provider="OTHER"),
                "variant": dict(source_variant="OTHER"),
                "subject": dict(subject_instrument="OTHER"),
                "units": dict(native_units="price"),
                "field": dict(native_field_path=("quote", "ask_size")),
                "mapping": dict(projection_mapping_id="OTHER"),
                "mapping-version": dict(projection_mapping_version=2),
                "rid": dict(raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R036")),
                "float": dict(native_value=2.0),
                "nonfinite": dict(native_value=Decimal("NaN")),
                "scope": dict(ingestion_sequence_scope=raw_api.ingestion_sequence_scope("OTHER")),
                "sequence-bool": dict(ingestion_sequence=True),
                "identity-type": dict(observation_occurrence_id="mmt-size-bid-001"),
                "selection-identity": dict(selection_identity="OTHER"),
                "revision": dict(revision_vintage_native="v2"),
                "temporal": dict(source_temporal_kind="date_only"),
                "timezone": dict(source_timezone_native="OTHER"),
                "timestamp-type": dict(source_timestamp_raw=123),
                "timestamp-format": dict(source_timestamp_raw="2026-10-16 00:59:58+00:00"),
                "future": dict(source_timestamp_raw=NOW.isoformat().replace("+00:00", "Z")),
                "receipt": dict(received_ts_utc=NOW),
                "event-after-receipt": dict(received_ts_utc=ASOF - timedelta(seconds=3)),
                "stale": dict(source_timestamp_raw="2026-10-16T00:58:59.999999Z"),
                "skew": dict(source_timestamp_raw="2026-10-16T00:59:48.999999Z"),
            }.get(mode)
            if changes is not None:
                return replace(page, items=(unsafe_copy(first, **changes),))
            if mode == "missing":
                return replace(page, items=())
            if mode == "wrong-page":
                return {"items": page.items}
            if mode == "wrong-items":
                return unsafe_copy(page, items=list(page.items))
            if mode == "wrong-type":
                return replace(page, items=({"value": Decimal("2")},))
            if mode == "ambiguous":
                return replace(
                    page,
                    items=(
                        first,
                        replace(
                            first,
                            observation_occurrence_id=raw_api.observation_occurrence_id("tie"),
                        ),
                    ),
                )
            if mode == "duplicate-content":
                # Invalid newer copy cannot be filtered before duplicate-content comparison.
                return replace(page, items=(first, replace(first, source_provider="OTHER")))
            if mode == "duplicate-identical":
                return replace(page, items=(first, first))
            if mode == "oversized-page":
                return replace(page, items=(first,) * 101)
            if mode == "storage-error":
                raise f.PersistenceFailureV1("upstream persistence failed")
            return page

    owner = f.create_raw_ratio_owner(**configuration(Reader(), tmp_path / "ratio.sqlite"))
    req = request()
    before = ()
    if populated:
        first = owner.materialise(req)
        assert_ratio(first, 1, 3)
        before = (first,)
    active[0] = True
    if mode in POSITIVES:
        calls.clear()
        fact = owner.materialise(req)
        assert_ratio(fact, 1, 3)
        assert owner.reads.get_derived_occurrence(fact.derived_occurrence_id) == fact
        if mode == "real-multipage":
            assert any(rid == "R033" and cursor is not None for rid, cursor in calls)
            assert fact.raw_input_lineage[0].observation_occurrence_id == "mmt-size-bid-001"
        if mode in ("inclusive-freshness", "inclusive-skew"):
            assert fact.raw_input_lineage[0].event_time_utc == ASOF - timedelta(
                seconds=60 if mode == "inclusive-freshness" else 11
            )
        observed = history(owner.reads)
        assert len(observed) == len(before) + int(fact not in before)
        assert fact in observed and all(item in observed for item in before)
        return
    if mode == "order":
        req = replace(req, raw_input_bindings=tuple(reversed(req.raw_input_bindings)))
    changes = {
        "context": dict(context_refs=(f.VersionRefV1("strategy", 1),)),
        "definition": dict(calculation_definition_version="absent"),
        "profile": dict(parameter_set_ref=f.VersionRefV1("absent", 1)),
        "selection": dict(input_selection_policy_ref=f.VersionRefV1("absent", 1)),
        "request-subject": dict(subject_instrument="OTHER"),
        "asof-after-cutoff": dict(as_of_utc=NOW),
        "cutoff-after-clock": dict(knowledge_cutoff_utc=NOW + timedelta(microseconds=1)),
    }.get(mode)
    if changes:
        req = replace(req, **changes)
    binding_changes = {
        "binding-rid": dict(raw_signal_id="R034"),
        "binding-subject": dict(subject_instrument="OTHER"),
        "binding-mapping": dict(projection_mapping_ref=f.VersionRefV1("mmt-size-ask", 1)),
        "binding-unit": dict(unit_convention_ref=f.VersionRefV1("absent", 1)),
        "binding-unit-incompatible": dict(unit_convention_ref=f.VersionRefV1("mmt-pilot-price", 1)),
    }.get(mode)
    if binding_changes:
        req = replace(
            req,
            raw_input_bindings=(
                replace(req.raw_input_bindings[0], **binding_changes),
                req.raw_input_bindings[1],
            ),
        )
    requests = [req]
    if mode == "unsupported-all":
        requests = [replace(req, derived_signal_id=f"D{i:03d}") for i in range(1, 210) if i != 14]
        assert len(requests) == 208
    for bad in requests:
        calls.clear()  # Read-budget scope is this request, not all208 requests.
        if mode == "storage-error":
            with pytest.raises(f.PersistenceFailureV1):
                owner.materialise(bad)
        else:
            assert owner.materialise(bad) is None, mode
        assert history(owner.reads) == before
        if populated:
            assert owner.reads.get_derived_occurrence(first.derived_occurrence_id) == first


@pytest.mark.parametrize(
    "bid,ask,expected",
    [
        ("2", "1", (1, 3)),
        ("1", "2", (-1, 3)),
        ("3", "1", (1, 2)),
        ("2", "2", (0, 1)),
        ("2", "0", (1, 1)),
        ("0", "2", (-1, 1)),
        ("0", "-0.00", None),
        ("1", "-1", None),
        ("2.50", "1.25", (1, 3)),
        ("-3", "1", (2, 1)),
        ("2E+5000", "1E+5000", (1, 3)),
        ("2E-5000", "1E-5000", (1, 3)),
        ("1E+4400", "1", (10**4400 - 1, 10**4400 + 1)),
        ("-0.00", "2.000", (-1, 1)),
    ],
)
def test_d014_exact_ratio_arithmetic_domain(tmp_path, bid, ask, expected):
    # Negative fixtures are signed artificial algebra, not native displayed-size validity.
    raw = raw_source(tmp_path / "raw.sqlite")
    for side, value in (("bid", bid), ("ask", ask)):
        raw.commands.admit_raw_observation_occurrence(observation(side, value=Decimal(value)))
    seam()
    path = tmp_path / "ratio.sqlite"
    owner = f.create_raw_ratio_owner(**configuration(raw.reads, path))
    limit_before = sys.get_int_max_str_digits()
    with localcontext() as context:
        context.prec = 2
        context.traps[Inexact] = context.traps[Rounded] = True
        fact = owner.materialise(request())
    assert sys.get_int_max_str_digits() == limit_before
    if expected is None:
        assert fact is None and history(owner.reads) == ()
        return
    assert_ratio(fact, *expected)
    for lineage, value in zip(fact.raw_input_lineage, (bid, ask), strict=True):
        assert lineage.projection.native_value.as_tuple() == Decimal(value).as_tuple()
        assert lineage.canonical_value == Decimal(value)
    fresh = f.create_raw_ratio_reader(
        admission=f.OwnerAdmissionV1("M02", BRIEF), storage=f.SQLiteReadStorageV1(str(path))
    )
    assert fresh.get_derived_occurrence(fact.derived_occurrence_id) == fact
    assert sys.get_int_max_str_digits() == limit_before
    with sqlite3.connect(path) as db:
        payload = db.execute("SELECT payload FROM mmt_raw_ratio_occurrence_v1").fetchone()[0]
    assert json.loads(payload)["result"] == dict(
        kind="exact_ratio",
        numerator=integer_text(expected[0]),
        denominator=integer_text(expected[1]),
    )


@pytest.mark.parametrize(
    "dimension",
    [
        "definition",
        "parameter",
        "selection",
        "bid-unit",
        "ask-unit",
        "bid-mapping",
        "ask-mapping",
        "raw-identity",
        "native-representation",
        "asof",
        "cutoff",
    ],
)
def test_d014_identity_versions_and_later_retry(tmp_path, dimension):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    seam()
    source = [raw.reads]
    clock = [NOW]

    class Reader:
        def list_projected_raw_history(self, rid, **kwargs):
            return source[0].list_projected_raw_history(rid, **kwargs)

    config = configuration(Reader(), tmp_path / "ratio.sqlite", now=lambda: clock[0])
    owner = f.create_raw_ratio_owner(**config)
    req = request()
    first = owner.materialise(req)
    assert_ratio(first, 1, 3)
    clock[0] += timedelta(days=1)
    assert owner.materialise(req) == first
    assert first.calculated_at_utc == NOW
    changed = req
    if dimension == "definition":
        changed = replace(req, calculation_definition_version="D014-SIZE-IMBALANCE-2")
    elif dimension == "parameter":
        changed = replace(req, parameter_set_ref=f.VersionRefV1("mmt-size-basic", 2))
    elif dimension == "selection":
        changed = replace(req, input_selection_policy_ref=f.VersionRefV1("mmt-size-selection", 2))
    elif dimension.endswith("-unit") or dimension.endswith("-mapping"):
        index = 0 if dimension.startswith("bid-") else 1
        bindings = list(req.raw_input_bindings)
        updates = (
            dict(unit_convention_ref=f.VersionRefV1("mmt-size-shares", 2))
            if dimension.endswith("-unit")
            else dict(
                projection_mapping_ref=f.VersionRefV1(
                    "mmt-size-" + ("bid" if index == 0 else "ask"), 2
                )
            )
        )
        bindings[index] = replace(bindings[index], **updates)
        changed = replace(req, raw_input_bindings=tuple(bindings))
    elif dimension in ("raw-identity", "native-representation"):
        # Fresh actual M00 source differs in exactly ONE input field, not time,
        # rank, config or request. Separate files permit the same scoped sequence.
        other = raw_source(tmp_path / "other-raw.sqlite")
        for side in ("bid", "ask"):
            item = observation(side)
            if side == "bid":
                item = (
                    replace(
                        item, observation_occurrence_id=raw_api.observation_occurrence_id("new-id")
                    )
                    if dimension == "raw-identity"
                    else replace(item, native_record={"quote": {"bid_size": Decimal("2.0")}})
                )
            other.commands.admit_raw_observation_occurrence(item)
        source[0] = other.reads
    elif dimension == "asof":
        changed = replace(req, as_of_utc=ASOF - timedelta(microseconds=1))
    elif dimension == "cutoff":
        changed = replace(req, knowledge_cutoff_utc=NOW)
    second = owner.materialise(changed)
    assert_ratio(second, 1, 3)
    assert first.derived_occurrence_id != second.derived_occurrence_id
    assert second.calculated_at_utc == clock[0]
    assert owner.materialise(changed) == second
    assert owner.reads.get_derived_occurrence(first.derived_occurrence_id) == first
    assert owner.reads.get_derived_occurrence(second.derived_occurrence_id) == second
    if dimension.endswith("-unit"):
        assert second.convention_refs == (
            f.VersionRefV1("mmt-size-shares", 1),
            f.VersionRefV1("mmt-size-shares", 2),
        )
    assert_config_reads(owner.reads, config)
    ordered = tuple(
        sorted(
            (first, second),
            key=lambda fact: (
                fact.effective_as_of_utc,
                fact.knowledge_cutoff_utc,
                fact.derived_occurrence_id,
            ),
            reverse=True,
        )
    )
    assert history(owner.reads) == ordered
    assert history(owner.reads, limit=1) == ordered[:1]
    assert history(
        owner.reads, effective_at_or_before_utc=ASOF, knowledge_at_or_before_utc=ASOF
    ) == tuple(x for x in ordered if x.knowledge_cutoff_utc <= ASOF)
    assert history(owner.reads, effective_at_or_before_utc=ASOF - timedelta(seconds=1)) == ()
    assert history(owner.reads, knowledge_at_or_before_utc=ASOF - timedelta(microseconds=1)) == ()
    assert history(owner.reads, subject_instrument="OTHER") == ()
    for bad in (0, 1001):
        with pytest.raises(ValueError):
            history(owner.reads, limit=bad)
    for bad in (True, 1.0):
        with pytest.raises(TypeError):
            history(owner.reads, limit=bad)
    for getter in (
        owner.reads.get_parameter_set,
        owner.reads.get_input_selection_policy,
        owner.reads.get_unit_convention,
        owner.reads.get_projection_mapping,
    ):
        assert getter(f.VersionRefV1("absent", 1)) is None
    assert owner.reads.get_derived_occurrence("absent") is None
    assert (
        owner.reads.get_calculation_definition(
            derived_signal_id="D014", calculation_definition_version="absent"
        )
        is None
    )
    # Each conflict separately presents lawful new members BEFORE conflicting
    # content. No partially registered member may escape any failed operation.
    for key, invalid in (
        ("definitions", lambda x: replace(x, equation="R033 / R036")),
        ("parameter_sets", lambda x: replace(x, members=("OTHER",))),
        ("input_selection_policies", lambda x: replace(x, maximum_skew=timedelta(seconds=11))),
        ("unit_conventions", lambda x: replace(x, scale=Decimal("2"))),
        ("raw_projection_mappings", lambda x: replace(x, native_field_path=("other",))),
    ):
        path = tmp_path / ("atomic-" + key + ".sqlite")
        initial = configuration(raw.reads, path, versions=(1,))
        initial_owner = f.create_raw_ratio_owner(**initial)
        reopened = initial | dict(storage=f.SQLiteStorageV1(str(path), False))
        f.create_raw_ratio_owner(**reopened)  # Identical registration is lawful.
        all_versions = configuration(raw.reads, path)
        attempted = all_versions | dict(storage=f.SQLiteStorageV1(str(path), False))
        new_members = tuple(x for x in all_versions[key] if x not in initial[key])
        attempted[key] = (*new_members, invalid(initial[key][0]))
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_raw_ratio_owner(**attempted)
        assert_config_reads(initial_owner.reads, initial)
        assert (
            initial_owner.reads.get_calculation_definition(
                derived_signal_id="D014", calculation_definition_version="D014-SIZE-IMBALANCE-2"
            )
            is None
        )
        for getter, identity in (
            (initial_owner.reads.get_parameter_set, "mmt-size-basic"),
            (initial_owner.reads.get_input_selection_policy, "mmt-size-selection"),
            (initial_owner.reads.get_unit_convention, "mmt-size-shares"),
            (initial_owner.reads.get_projection_mapping, "mmt-size-bid"),
            (initial_owner.reads.get_projection_mapping, "mmt-size-ask"),
        ):
            assert getter(f.VersionRefV1(identity, 2)) is None
        assert history(initial_owner.reads) == ()


STORAGE_CASES = (
    "profile",
    "readonly-process",
    "precommit",
    "postcommit",
    "competing",
    "payload",
    "content-hash",
    "logical-hash",
    "index",
    "noncanonical-ratio",
    "noncanonical-integer",
    "native-representation",
    "configuration-content",
    "configuration-link",
    "definition-link",
    "correct-rehash-equation",
    "wrong-owner",
    "wrong-version",
    "extra-table",
    "missing-trigger",
    "altered-trigger",
    "column-schema",
    "wal-policy",
    "definition-primary-key",
    "configuration-primary-key",
    "occurrence-primary-key",
    "configuration-check",
    "occurrence-foreign-key",
)


def downgrade_constraint(db, target, mode):
    """Independent brief-derived declaration; retain every row and other property.

    No writable_schema trick or malformed B-tree stands in for a valid downgraded
    declaration. All original triggers are restored after the real table rebuild.
    """
    rows = db.execute("SELECT * FROM " + target).fetchall()
    original_info = db.execute("PRAGMA table_info(" + target + ")").fetchall()
    triggers = db.execute("SELECT name,sql FROM sqlite_schema WHERE type='trigger'").fetchall()
    for name, _ in triggers:
        db.execute('DROP TRIGGER "' + name + '"')
    columns = [name + " " + kind + " NOT NULL" for _, name, kind, *_ in original_info]
    if target.endswith("configuration_v1") and mode != "configuration-check":
        columns.append("CHECK(kind IN ('parameter','selection','unit','raw_mapping'))")
    keys = {
        "mmt_raw_ratio_definition_v1": (
            "owner_namespace,derived_signal_id,calculation_definition_version"
        ),
        "mmt_raw_ratio_configuration_v1": "owner_namespace,kind,context_id,version",
        "mmt_raw_ratio_occurrence_v1": "derived_occurrence_id",
    }
    if not mode.endswith("primary-key"):
        columns.append("PRIMARY KEY(" + keys[target] + ")")
    elif target.endswith("definition_v1"):
        # Keep the referenced columns UNIQUE so the remaining occurrence FK is
        # still a valid declaration. Missing PK must not hide behind a malformed
        # foreign-key-target error raised by SQLite itself.
        columns.append("UNIQUE(" + keys[target] + ")")
    if target.endswith("occurrence_v1") and mode != "occurrence-foreign-key":
        columns.append(
            "FOREIGN KEY(owner_namespace,derived_signal_id,calculation_definition_version) "
            "REFERENCES mmt_raw_ratio_definition_v1"
            "(owner_namespace,derived_signal_id,calculation_definition_version)"
        )
    scratch = "proof_rebuild"
    db.execute("CREATE TABLE " + scratch + " (" + ",".join(columns) + ") STRICT")
    db.execute("INSERT INTO " + scratch + " SELECT * FROM " + target)
    db.execute("DROP TABLE " + target)
    db.execute("ALTER TABLE " + scratch + " RENAME TO " + target)
    for _, sql in triggers:
        db.execute(sql)
    info = db.execute("PRAGMA table_info(" + target + ")").fetchall()
    assert [(row[1], row[2], row[3]) for row in info] == [
        (row[1], row[2], row[3]) for row in original_info
    ]
    assert sorted(db.execute("SELECT * FROM " + target).fetchall()) == sorted(rows)
    assert db.execute(
        "SELECT strict FROM pragma_table_list WHERE name=?", (target,)
    ).fetchone() == (1,)
    assert db.execute("PRAGMA application_id").fetchone() == (0x4E560004,)
    assert db.execute("PRAGMA user_version").fetchone() == (1,)
    assert db.execute("PRAGMA journal_mode").fetchone() == ("delete",)
    assert dict(db.execute("SELECT name,sql FROM sqlite_schema WHERE type='trigger'")) == dict(
        triggers
    )
    assert db.execute("PRAGMA foreign_key_check").fetchall() == []
    if mode.endswith("primary-key"):
        assert all(row[5] == 0 for row in info)
    elif mode == "configuration-check":
        sql = db.execute("SELECT sql FROM sqlite_schema WHERE name=?", (target,)).fetchone()[0]
        assert "CHECK" not in sql.upper()
    else:
        assert db.execute("PRAGMA foreign_key_list(" + target + ")").fetchall() == []


@pytest.mark.parametrize("mode", STORAGE_CASES)
def test_d014_sqlite_recovery_faults_and_integrity(tmp_path, monkeypatch, mode):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    seam()
    assert (
        importlib.util.find_spec("nvda_desk.market_measurement_truth._raw_rational_sqlite")
        is not None
    ), "admitted isolated D014 SQLite behaviour is absent"
    path = tmp_path / "ratio.sqlite"
    config = configuration(raw.reads, path)
    owner = f.create_raw_ratio_owner(**config)
    req = request()
    original_connect = sqlite3.connect
    table = "mmt_raw_ratio_occurrence_v1"
    definition_table = "mmt_raw_ratio_definition_v1"
    configuration_table = "mmt_raw_ratio_configuration_v1"
    if mode in ("precommit", "postcommit", "competing"):
        mechanism = importlib.import_module(
            "nvda_desk.market_measurement_truth._raw_rational_sqlite"
        )
        reached = []
        phase = [mode]
        inserted, release = Event(), Event()

        class ControlledConnection(sqlite3.Connection):
            wrote = False

            def execute(self, sql, *args, **kwargs):
                statement = sql.strip().upper()
                if statement == "COMMIT" and self.wrote and phase[0] == "precommit":
                    reached.append("before")
                    raise sqlite3.OperationalError("native precommit failure")
                result = super().execute(sql, *args, **kwargs)
                if statement.startswith("INSERT") and table.upper() in statement:
                    self.wrote = True
                    if phase[0] == "competing":
                        inserted.set()
                        assert release.wait(timeout=10), "first INSERT not released"
                if statement == "COMMIT" and self.wrote and phase[0] == "postcommit":
                    reached.append("after")
                    raise sqlite3.OperationalError("lost commit acknowledgement")
                return result

        def connect(*args, **kwargs):
            if str(args[0]).startswith(path.as_uri() + "?"):
                kwargs["factory"] = ControlledConnection
            return original_connect(*args, **kwargs)

        # Module-local sqlite fault injection does not forge a fact, storage
        # outcome or commit. The first public write really reaches SQLite.
        monkeypatch.setattr(mechanism.sqlite3, "connect", connect)
        assert history(owner.reads) == ()
        if mode == "competing":
            second = f.create_raw_ratio_owner(
                **(
                    config
                    | dict(
                        storage=f.SQLiteStorageV1(str(path), False),
                        utc_now=lambda: NOW + timedelta(days=1),
                    )
                )
            )
            with ThreadPoolExecutor(max_workers=1) as pool:
                pending = pool.submit(owner.materialise, req)
                try:
                    assert inserted.wait(timeout=10), "real first INSERT not reached"
                    assert history(second.reads) == ()
                    with original_connect(path) as db:
                        assert db.execute("SELECT count(*) FROM " + table).fetchone() == (0,)
                    with pytest.raises(f.PersistenceFailureV1) as busy:
                        second.materialise(req)
                    assert busy.value.outcome_uncertain is False
                finally:
                    release.set()
                fact = pending.result(timeout=20)
            phase[0] = "none"
            assert second.materialise(req) == fact
        else:
            with pytest.raises(f.PersistenceFailureV1) as failed:
                owner.materialise(req)
            assert failed.value.outcome_uncertain is (mode == "postcommit")
            assert reached == (["before"] if mode == "precommit" else ["after"])
            phase[0] = "none"
            existing = history(owner.reads)
            assert len(existing) == int(mode == "postcommit")
            fact = owner.materialise(req)
            if mode == "postcommit":
                assert fact == existing[0]
        monkeypatch.undo()
        assert_ratio(fact, 1, 3)
        assert fact.calculated_at_utc == NOW and history(owner.reads) == (fact,)
        return
    fact = owner.materialise(req)
    assert_ratio(fact, 1, 3)
    assert history(owner.reads) == (fact,)
    if mode == "profile":
        mechanism = importlib.import_module(
            "nvda_desk.market_measurement_truth._raw_rational_sqlite"
        )
        connections, policies = [], []

        class ObservedConnection(sqlite3.Connection):
            def execute(self, sql, *args, **kwargs):
                result = super().execute(sql, *args, **kwargs)
                statement = sql.strip().upper()
                if statement == "BEGIN IMMEDIATE":
                    policies.append(
                        (
                            "write",
                            super().execute("PRAGMA synchronous").fetchone()[0],
                            super().execute("PRAGMA foreign_keys").fetchone()[0],
                            super().execute("PRAGMA busy_timeout").fetchone()[0],
                        )
                    )
                if statement == "BEGIN":
                    policies.append(
                        (
                            "read",
                            super().execute("PRAGMA query_only").fetchone()[0],
                            super().execute("PRAGMA foreign_keys").fetchone()[0],
                            super().execute("PRAGMA busy_timeout").fetchone()[0],
                        )
                    )
                    with pytest.raises(sqlite3.OperationalError):
                        super().execute("CREATE TABLE prohibited(value TEXT)")
                return result

        def observed_connect(*args, **kwargs):
            if str(args[0]).startswith(path.as_uri() + "?"):
                connections.append((str(args[0]), kwargs.get("uri")))
                kwargs["factory"] = ObservedConnection
            return original_connect(*args, **kwargs)

        monkeypatch.setattr(mechanism.sqlite3, "connect", observed_connect)
        # BEGIN IMMEDIATE belongs to a new append, not necessarily a retry.
        new_fact = owner.materialise(
            replace(req, calculation_definition_version="D014-SIZE-IMBALANCE-2")
        )
        assert_ratio(new_fact, 1, 3)
        assert new_fact.derived_occurrence_id != fact.derived_occurrence_id
        assert ("write", 3, 1, 0) in policies
        assert owner.materialise(req) == fact
        independent = f.create_raw_ratio_reader(
            admission=config["admission"], storage=f.SQLiteReadStorageV1(str(path))
        )
        assert independent.get_derived_occurrence(fact.derived_occurrence_id) == fact
        assert ("read", 1, 1, 0) in policies
        assert all(uri is True for _, uri in connections)
        assert any(url == path.as_uri() + "?mode=rw" for url, _ in connections)
        assert any(url == path.as_uri() + "?mode=ro" for url, _ in connections)
        monkeypatch.undo()
        with original_connect(path) as db:
            assert db.execute("PRAGMA application_id").fetchone() == (0x4E560004,)
            assert db.execute("PRAGMA user_version").fetchone() == (1,)
            assert db.execute("PRAGMA journal_mode").fetchone() == ("delete",)
            assert dict(
                db.execute(
                    "SELECT name,strict FROM pragma_table_list WHERE name NOT LIKE 'sqlite_%'"
                )
            ) == {definition_table: 1, configuration_table: 1, table: 1}
            columns = {
                definition_table: (
                    "owner_namespace",
                    "derived_signal_id",
                    "calculation_definition_version",
                    "payload",
                    "content_sha256",
                ),
                configuration_table: (
                    "owner_namespace",
                    "kind",
                    "context_id",
                    "version",
                    "payload",
                    "content_sha256",
                ),
                table: (
                    "derived_occurrence_id",
                    "owner_object_id",
                    "owner_namespace",
                    "implementation_brief_sha256",
                    "derived_signal_id",
                    "calculation_definition_version",
                    "subject_instrument",
                    "effective_as_of_utc",
                    "knowledge_cutoff_utc",
                    "logical_identity_payload",
                    "logical_identity_sha256",
                    "payload",
                    "content_sha256",
                ),
            }
            for current, names in columns.items():
                info = db.execute("PRAGMA table_info(" + current + ")").fetchall()
                assert tuple(row[1] for row in info) == names
                assert all(row[3] == 1 for row in info)
                assert tuple(row[2] for row in info) == tuple(
                    "BLOB" if name.endswith("payload") else "TEXT" for name in names
                )
                keys = {
                    definition_table: (1, 2, 3, 0, 0),
                    configuration_table: (1, 2, 3, 4, 0, 0),
                    table: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                }
                assert tuple(row[5] for row in info) == keys[current]
            foreign = db.execute("PRAGMA foreign_key_list(" + table + ")").fetchall()
            assert sorted(foreign) == [
                (0, index, definition_table, name, name, "NO ACTION", "NO ACTION", "NONE")
                for index, name in enumerate(
                    ("owner_namespace", "derived_signal_id", "calculation_definition_version")
                )
            ]
            for current in (definition_table, configuration_table):
                assert db.execute("PRAGMA foreign_key_list(" + current + ")").fetchall() == []
            declaration = db.execute(
                "SELECT sql FROM sqlite_schema WHERE name=?", (configuration_table,)
            ).fetchone()[0]
            check = re.search(
                r"CHECK\s*\(\s*kind\s+IN\s*\(([^)]+)\)\s*\)", declaration, re.IGNORECASE
            )
            assert check is not None
            assert tuple(re.findall(r"'([^']*)'", check[1])) == (
                "parameter",
                "selection",
                "unit",
                "raw_mapping",
            )
            assert {
                row[0] for row in db.execute("SELECT DISTINCT kind FROM " + configuration_table)
            } == {"parameter", "selection", "unit", "raw_mapping"}
            with pytest.raises(sqlite3.IntegrityError, match="CHECK constraint failed"):
                db.execute(
                    "INSERT INTO " + configuration_table + " VALUES(?,?,?,?,?,?)",
                    ("probe", "forbidden", "probe", "1", b"{}", "0" * 64),
                )
            assert db.execute("PRAGMA foreign_key_check").fetchall() == []
            triggers = dict(db.execute("SELECT name,sql FROM sqlite_schema WHERE type='trigger'"))
            assert set(triggers) == {
                current + "_" + action.lower()
                for current in columns
                for action in ("UPDATE", "DELETE")
            }
            for current in columns:
                for action in ("UPDATE", "DELETE"):
                    sql = triggers[current + "_" + action.lower()]
                    assert "BEFORE " + action in sql.upper() and "immutable raw-ratio record" in sql
                    with pytest.raises(sqlite3.IntegrityError, match="immutable raw-ratio record"):
                        db.execute(
                            "DELETE FROM " + current
                            if action == "DELETE"
                            else "UPDATE " + current + " SET payload=payload"
                        )
            assert db.execute("SELECT count(*) FROM " + table).fetchone() == (2,)
        before = path.read_bytes()
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_raw_ratio_owner(**config)  # Exclusive create never overwrites.
        for bad in (
            str(path) + "?x=1",
            path.as_uri(),
            "relative.sqlite",
            str(tmp_path),
            str(tmp_path / "absent.sqlite"),
        ):
            with pytest.raises((ValueError, f.PersistenceFailureV1)):
                f.create_raw_ratio_reader(
                    admission=config["admission"], storage=f.SQLiteReadStorageV1(bad)
                )
        link = tmp_path / "link.sqlite"
        link.symlink_to(path)
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_raw_ratio_reader(
                admission=config["admission"], storage=f.SQLiteReadStorageV1(str(link))
            )
        assert not (tmp_path / "absent.sqlite").exists()
        assert path.read_bytes() == before
        # Actual raw/v1/D013 profile files are separately provisioned; no fake
        # appid-only file stands in for a valid other-owner file.
        for kind, brief in (
            ("v1", "a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393"),
            ("predecessor", "1f53d9c21c6eb4b90213137c4699a0688f994cd0ed55e54082268d8477abc148"),
        ):
            other_path = tmp_path / (kind + ".sqlite")
            if kind == "v1":
                old_owner = f.create_owner(
                    admission=f.OwnerAdmissionV1("M02", brief),
                    raw_projection_reader=raw.reads,
                    definitions=(),
                    parameter_sets=(),
                    input_selection_policies=(),
                    unit_conventions=(),
                    raw_projection_mappings=(),
                    storage=f.SQLiteStorageV1(str(other_path), True),
                    utc_now=lambda: NOW,
                )
            else:
                f.create_ratio_owner(
                    admission=f.OwnerAdmissionV1("M02", brief),
                    predecessor_reader=old_owner.reads,
                    definitions=(),
                    parameter_sets=(),
                    storage=f.SQLiteStorageV1(str(other_path), True),
                    utc_now=lambda: NOW,
                )
            old_bytes = other_path.read_bytes()
            with pytest.raises((ValueError, f.PersistenceFailureV1)):
                f.create_raw_ratio_reader(
                    admission=config["admission"], storage=f.SQLiteReadStorageV1(str(other_path))
                )
            with pytest.raises((ValueError, f.PersistenceFailureV1)):
                f.create_raw_ratio_owner(
                    **(config | dict(storage=f.SQLiteStorageV1(str(other_path), False)))
                )
            assert other_path.read_bytes() == old_bytes
            factory = f.create_reader if kind == "v1" else f.create_ratio_reader
            with pytest.raises((ValueError, f.PersistenceFailureV1)):
                factory(
                    admission=f.OwnerAdmissionV1("M02", brief),
                    storage=f.SQLiteReadStorageV1(str(path)),
                )
        raw_path = tmp_path / "raw.sqlite"
        raw_bytes = raw_path.read_bytes()
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_raw_ratio_owner(
                **(config | dict(storage=f.SQLiteStorageV1(str(raw_path), False)))
            )
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_raw_ratio_reader(
                admission=config["admission"], storage=f.SQLiteReadStorageV1(str(raw_path))
            )
        with pytest.raises(raw_api.PersistenceFailureV1):
            # Raw file constructor must refuse this different profile, too.
            from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

            create_sqlite_persistence(str(path), create=False)
        assert raw_path.read_bytes() == raw_bytes and path.read_bytes() == before
        return
    if mode == "readonly-process":
        env = dict(
            os.environ, PYTHONPATH=os.pathsep.join((str(ROOT / "src"), str(Path(__file__).parent)))
        )
        writer_code = """
import base64,pickle,sys
from pathlib import Path
from _support import raw_source,observation,configuration,request,f
root=Path(sys.argv[1]); raw=raw_source(root/'child-raw.sqlite')
for side in ('bid','ask'): raw.commands.admit_raw_observation_occurrence(observation(side))
owner=f.create_raw_ratio_owner(**configuration(raw.reads,root/'child-ratio.sqlite'))
value=owner.materialise(request())
print(base64.b64encode(pickle.dumps(value)).decode())
"""
        writer = subprocess.run(
            [sys.executable, "-c", writer_code, str(tmp_path)],
            env=env,
            text=True,
            capture_output=True,
            timeout=30,
        )
        assert writer.returncode == 0, writer.stderr
        exited = pickle.loads(base64.b64decode(writer.stdout))
        assert exited == fact
        # This process imports only the public API; inputs are path/admission/ID.
        reader_code = """
import base64,pickle,sys
from nvda_desk.market_measurement_truth import api as f
reads=f.create_raw_ratio_reader(admission=f.OwnerAdmissionV1('M02',sys.argv[2]),
    storage=f.SQLiteReadStorageV1(sys.argv[1]))
fact=reads.get_derived_occurrence(sys.argv[3])
result=dict(fact=fact,
    definitions=tuple(reads.get_calculation_definition(derived_signal_id='D014',
        calculation_definition_version='D014-SIZE-IMBALANCE-'+str(v)) for v in (1,2)),
    parameters=tuple(reads.get_parameter_set(f.VersionRefV1('mmt-size-basic',v)) for v in (1,2)),
    policies=tuple(reads.get_input_selection_policy(
        f.VersionRefV1('mmt-size-selection',v)) for v in (1,2)),
    units=tuple(reads.get_unit_convention(f.VersionRefV1('mmt-size-shares',v)) for v in (1,2)),
    mappings=tuple(reads.get_projection_mapping(f.VersionRefV1('mmt-size-'+side,v))
        for v in (1,2) for side in ('bid','ask')),
    history=reads.list_derived_history(derived_signal_id='D014',subject_instrument='NVDA',
        effective_at_or_before_utc=fact.effective_as_of_utc,
        knowledge_at_or_before_utc=fact.knowledge_cutoff_utc,limit=1000),
    has_writer=hasattr(reads,'materialise'))
print(base64.b64encode(pickle.dumps(result)).decode())
"""
        child_path = tmp_path / "child-ratio.sqlite"
        before = child_path.read_bytes()
        reader = subprocess.run(
            [
                sys.executable,
                "-c",
                reader_code,
                str(child_path),
                BRIEF,
                exited.derived_occurrence_id,
            ],
            env=env,
            text=True,
            capture_output=True,
            timeout=30,
        )
        assert reader.returncode == 0, reader.stderr
        bundle = pickle.loads(base64.b64decode(reader.stdout))
        assert bundle == dict(
            fact=fact,
            definitions=config["definitions"],
            parameters=config["parameter_sets"],
            policies=config["input_selection_policies"],
            units=config["unit_conventions"],
            mappings=config["raw_projection_mappings"],
            history=(fact,),
            has_writer=False,
        )
        assert child_path.read_bytes() == before
        return
    with original_connect(path) as db:
        if mode in (
            "definition-primary-key",
            "configuration-primary-key",
            "occurrence-primary-key",
            "configuration-check",
            "occurrence-foreign-key",
        ):
            target = (
                definition_table
                if mode.startswith("definition-")
                else configuration_table
                if mode.startswith("configuration-")
                else table
            )
            downgrade_constraint(db, target, mode)
        elif mode == "wrong-owner":
            db.execute("PRAGMA application_id=1314258946")
        elif mode == "wrong-version":
            db.execute("PRAGMA user_version=2")
        elif mode == "extra-table":
            db.execute("CREATE TABLE extra(value TEXT)")
        elif mode == "missing-trigger":
            db.execute("DROP TRIGGER " + table + "_update")
        elif mode == "altered-trigger":
            db.execute("DROP TRIGGER " + table + "_update")
            db.execute(
                "CREATE TRIGGER "
                + table
                + "_update BEFORE UPDATE ON "
                + table
                + " BEGIN SELECT 1; END"
            )
        elif mode == "column-schema":
            db.execute("ALTER TABLE " + table + " ADD COLUMN extra TEXT NOT NULL DEFAULT ''")
        elif mode == "wal-policy":
            assert db.execute("PRAGMA journal_mode=WAL").fetchone() == ("wal",)
        else:
            triggers = db.execute(
                "SELECT name,sql FROM sqlite_schema WHERE type='trigger'"
            ).fetchall()
            for name, _ in triggers:
                db.execute('DROP TRIGGER "' + name + '"')
            payload, logical = db.execute(
                "SELECT payload,logical_identity_payload FROM " + table
            ).fetchone()
            doc = json.loads(payload)
            assert hashlib.sha256(logical).hexdigest() == fact.derived_occurrence_id.removeprefix(
                "mmtraw1:"
            )
            if mode == "payload":
                db.execute("UPDATE " + table + " SET payload=?", (payload + b" ",))
            elif mode == "content-hash":
                db.execute("UPDATE " + table + " SET content_sha256=?", ("0" * 64,))
            elif mode == "logical-hash":
                db.execute("UPDATE " + table + " SET logical_identity_sha256=?", ("0" * 64,))
            elif mode == "index":
                db.execute("UPDATE " + table + " SET subject_instrument='OTHER'")
            elif mode == "configuration-link":
                db.execute(
                    "DELETE FROM " + configuration_table + " WHERE kind='unit' AND version='1'"
                )
            elif mode == "definition-link":
                db.execute(
                    "DELETE FROM "
                    + definition_table
                    + " WHERE calculation_definition_version='D014-SIZE-IMBALANCE-1'"
                )
            elif mode == "configuration-content":
                cfg = db.execute(
                    "SELECT payload FROM "
                    + configuration_table
                    + " WHERE kind='unit' AND version='1'"
                ).fetchone()[0]
                unit = json.loads(cfg)
                unit["scale"] = dict(kind="decimal", sign=0, digits="2", exponent=0)
                encoded = json.dumps(
                    unit, sort_keys=True, ensure_ascii=True, separators=(",", ":")
                ).encode()
                db.execute(
                    "UPDATE "
                    + configuration_table
                    + " SET payload=?,content_sha256=? WHERE kind='unit' AND version='1'",
                    (encoded, hashlib.sha256(encoded).hexdigest()),
                )
            else:
                if mode == "noncanonical-ratio":
                    doc["result"] = dict(kind="exact_ratio", numerator="2", denominator="6")
                elif mode == "noncanonical-integer":
                    doc["result"]["numerator"] = "+1"
                elif mode == "correct-rehash-equation":
                    # Every outer hash/index/logical byte remains valid. Only
                    # independent fixed-equation recomputation can reject999/1.
                    doc["result"] = dict(kind="exact_ratio", numerator="999", denominator="1")
                elif mode == "native-representation":
                    doc["raw_input_lineage"][0]["projection"]["native_value"] = dict(
                        kind="decimal", sign=0, digits="20", exponent=-1
                    )
                encoded = json.dumps(
                    doc, sort_keys=True, ensure_ascii=True, separators=(",", ":")
                ).encode()
                db.execute(
                    "UPDATE " + table + " SET payload=?,content_sha256=?",
                    (encoded, hashlib.sha256(encoded).hexdigest()),
                )
            for _, sql in triggers:
                db.execute(sql)
    corrupted = path.read_bytes()
    with pytest.raises((ValueError, f.PersistenceFailureV1)):
        f.create_raw_ratio_reader(
            admission=config["admission"], storage=f.SQLiteReadStorageV1(str(path))
        )
    with pytest.raises((ValueError, f.PersistenceFailureV1)):
        f.create_raw_ratio_owner(**(config | dict(storage=f.SQLiteStorageV1(str(path), False))))
    assert path.read_bytes() == corrupted


def test_d014_additive_types_and_legacy_preservation(tmp_path):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    seam()
    config = configuration(raw.reads, tmp_path / "ratio.sqlite")
    owner = f.create_raw_ratio_owner(**config)
    fact = owner.materialise(request())
    assert_ratio(fact, 1, 3)
    assert not isinstance(fact, (f.DerivedSignalOccurrenceV1, f.RatioOccurrenceV1))
    assert type(fact.result) is not Decimal and not hasattr(fact, "__dict__")
    old_fields, new_fields = fields(f.DerivedSignalOccurrenceV1), fields(f.RawRatioOccurrenceV1)
    assert len(old_fields) == len(new_fields) == 21
    assert [x.name for x in old_fields] == [x.name for x in new_fields]
    for old, new in zip(old_fields, new_fields, strict=True):
        if old.name != "result":
            assert old.type == new.type
    with pytest.raises(FrozenInstanceError):
        fact.units = "price"
    for changes in (
        dict(result=Decimal("1")),
        dict(raw_input_lineage=list(fact.raw_input_lineage)),
    ):
        with pytest.raises(TypeError):
            replace(fact, **changes)
    for changes in (
        dict(units=""),
        dict(calculated_at_utc=NOW.replace(tzinfo=None)),
        dict(calculated_at_utc=NOW.astimezone(timezone(timedelta(hours=1)))),
        dict(raw_input_lineage=tuple(reversed(fact.raw_input_lineage))),
        dict(predecessor_occurrence_ids=("forbidden",)),
    ):
        with pytest.raises(ValueError):
            replace(fact, **changes)
    for admission in (
        f.OwnerAdmissionV1("M01", BRIEF),
        f.OwnerAdmissionV1(
            "M02", "a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393"
        ),
        f.OwnerAdmissionV1(
            "M02", "1f53d9c21c6eb4b90213137c4699a0688f994cd0ed55e54082268d8477abc148"
        ),
    ):
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_raw_ratio_owner(
                **(config | dict(admission=admission, storage=f.MemoryStorageV1()))
            )
    # Actual old public producers and D013 remain reachable and exactly typed;
    # no import of another claim's proof helper or private calculation module.
    previous_brief = "a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393"
    previous_ratio_brief = "1f53d9c21c6eb4b90213137c4699a0688f994cd0ed55e54082268d8477abc148"
    previous_raw = raw_source(tmp_path / "old-raw.sqlite")
    for side, rid, number in (("bid", "R034", "100"), ("ask", "R035", "102")):
        literal = replace(
            observation(side),
            source_provider=raw_api.provider_id("foundation-pilot-fixture"),
            native_record={"quote": {side: Decimal(number)}},
            ingestion_sequence_scope=raw_api.ingestion_sequence_scope(
                "foundation-pilot-fixture/cash_quote_v1"
            ),
            raw_signal_catalogue_ids=(raw_api.RawSignalCatalogueId(rid),),
            source_variant="cash_quote_v1",
            native_units="price",
        )
        previous_raw.commands.admit_raw_observation_occurrence(literal)
    definitions = tuple(
        f.CalculationDefinitionV1(
            identity,
            identity + "-" + label + "-1",
            "K02_ALGEBRA",
            equation,
            ("R034", "R035"),
            (),
            "P_BASIC",
            "price",
            "scalar_decimal",
            tuple(f.AuthorityArtifactRefV1(*ref) for ref in AUTHORITY),
        )
        for identity, label, equation in (
            ("D011", "MIDPOINT", "(R034 + R035) / 2"),
            ("D012", "SPREAD", "R035 - R034"),
        )
    )
    parameter = f.CalculationParameterSetV1("mmt-pilot-basic", 1, "P_BASIC", "NVDA", ("NVDA",))
    policy = f.InputSelectionPolicyVersionV1(
        "mmt-pilot-selection",
        1,
        ("subject_instrument",),
        timedelta(seconds=60),
        timedelta(seconds=10),
        ("true_instant",),
        (),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        "foundation-pilot-fixture/cash_quote_v1",
        100,
        1000,
    )
    unit = f.UnitConventionVersionV1(
        "mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0")
    )
    mappings = tuple(
        raw_api.RawSignalProjectionMappingV1(
            "mmt-pilot-" + side,
            1,
            raw_api.RawSignalCatalogueId(rid),
            "foundation-pilot-fixture",
            "cash_quote_v1",
            ("quote", side),
            "price",
            (),
        )
        for side, rid in (("bid", "R034"), ("ask", "R035"))
    )
    previous = f.create_owner(
        admission=f.OwnerAdmissionV1("M02", previous_brief),
        raw_projection_reader=previous_raw.reads,
        definitions=definitions,
        parameter_sets=(parameter,),
        input_selection_policies=(policy,),
        unit_conventions=(unit,),
        raw_projection_mappings=mappings,
        storage=f.SQLiteStorageV1(str(tmp_path / "previous.sqlite"), True),
        utc_now=lambda: NOW,
    )
    old_requests = tuple(
        f.CalculationRequestV1(
            identity,
            "NVDA",
            ASOF,
            ASOF,
            identity + "-" + label + "-1",
            f.VersionRefV1("mmt-pilot-basic", 1),
            f.VersionRefV1("mmt-pilot-selection", 1),
            (),
            tuple(
                f.RawInputBindingV1(
                    rid,
                    f.VersionRefV1("mmt-pilot-" + side, 1),
                    f.VersionRefV1("mmt-pilot-price", 1),
                    "NVDA",
                )
                for side, rid in (("bid", "R034"), ("ask", "R035"))
            ),
        )
        for identity, label in (("D011", "MIDPOINT"), ("D012", "SPREAD"))
    )
    midpoint, spread = (previous.materialise(req) for req in old_requests)
    assert type(midpoint) is type(spread) is f.DerivedSignalOccurrenceV1
    assert type(midpoint.result) is type(spread.result) is Decimal
    assert midpoint.result.as_tuple() == Decimal("101").as_tuple()
    assert spread.result.as_tuple() == Decimal("2").as_tuple()
    ratio_definition = f.CalculationDefinitionV1(
        "D013",
        "D013-RELATIVE-SPREAD-1",
        "K02_ALGEBRA",
        "100 * D012 / D011",
        (),
        ("D011", "D012"),
        "P_BASIC",
        "percent",
        "scalar_exact_ratio",
        tuple(f.AuthorityArtifactRefV1(*ref) for ref in AUTHORITY),
    )
    predecessor = f.create_ratio_owner(
        admission=f.OwnerAdmissionV1("M02", previous_ratio_brief),
        predecessor_reader=previous.reads,
        definitions=(ratio_definition,),
        parameter_sets=(parameter,),
        storage=f.SQLiteStorageV1(str(tmp_path / "predecessor.sqlite"), True),
        utc_now=lambda: NOW,
    )
    predecessor_request = f.RatioCalculationRequestV1(
        "D013",
        "NVDA",
        ASOF,
        ASOF,
        "D013-RELATIVE-SPREAD-1",
        f.VersionRefV1("mmt-pilot-basic", 1),
        (midpoint.derived_occurrence_id, spread.derived_occurrence_id),
    )
    ratio_fact = predecessor.materialise(predecessor_request)
    assert type(ratio_fact) is f.RatioOccurrenceV1
    assert ratio_fact.result == f.ExactRatioV1(200, 101)
    assert len(ratio_fact.predecessor_evidence) == 2
    assert previous.materialise(request()) is None
    assert predecessor.materialise(replace(predecessor_request, derived_signal_id="D014")) is None
    assert previous.reads.get_derived_occurrence(midpoint.derived_occurrence_id) == midpoint
    assert predecessor.reads.get_derived_occurrence(ratio_fact.derived_occurrence_id) == ratio_fact
    folder = Path(__file__).parent / "typing"
    mypy_config = tmp_path / "mypy.ini"
    mypy_config.write_text("[mypy]\npython_version=3.12\nfollow_untyped_imports=True\n")
    command = [
        sys.executable,
        "-m",
        "mypy",
        "--config-file",
        str(mypy_config),
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
    assert len(expected) == len(observed) == bad.stdout.count("error:") == 10
    assert {(int(line), code) for line, code in observed} == expected
    # This accepted additive unit permits no old-body edits; this is not a
    # permanent prohibition on future independently authorised compatible work.
    api_path = "src/nvda_desk/market_measurement_truth/api.py"
    original = ast.parse(
        subprocess.check_output(
            ["git", "show", "6c37588947ce4d61d0794d0f99ebaf497c970309:" + api_path], cwd=ROOT
        ).decode()
    )
    nodes = {
        node.name: node
        for node in ast.parse((ROOT / api_path).read_text()).body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef))
    }
    for node in original.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and not node.name.startswith("_"):
            assert ast.dump(node) == ast.dump(nodes[node.name])
    exports = next(
        node
        for node in original.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
    )
    assert set(ast.literal_eval(exports.value)) <= set(f.__all__)
