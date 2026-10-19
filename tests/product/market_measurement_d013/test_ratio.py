"""D013-P01-P06: actual producer ordering, exact ratios and independent durable truth."""

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
from datetime import datetime, timedelta
from decimal import Decimal, Inexact, Rounded, localcontext
from pathlib import Path
from threading import Event

import pytest
from _support import (
    ASOF,
    BRIEF,
    NOW,
    OLD_BRIEF,
    PREDECESSOR_BRIEF,
    ROOT,
    f,
    mapping,
    observation,
    predecessor_configuration,
    predecessor_request,
    ratio_configuration,
    ratio_request,
    raw_api,
    raw_source,
)


def ratio_seam():
    # Called only after the test establishes actual old producers. Missing new
    # behaviour is an assertion, never an import/collection/dependency failure.
    assert hasattr(f, "create_ratio_owner"), "admitted additive D013 ratio seam is absent"
    for name in (
        "create_ratio_reader",
        "ExactRatioV1",
        "RatioCalculationRequestV1",
        "RatioOccurrenceV1",
        "PredecessorEvidenceV1",
        "MeasurementRatioReadsV1",
        "MeasurementRatioOwnerV1",
    ):
        assert hasattr(f, name), name


def integer_text(number):
    """Independent canonical wire oracle, not bounded int-to-string conversion."""
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
    # Independent declared-wire oracle; no production serializer/validator import.
    identities = (
        ("RawSignalCatalogueId", raw_api.RawSignalCatalogueId("R034")),
        ("observation_occurrence_id", raw_api.observation_occurrence_id("id")),
        ("ingestion_sequence_scope", raw_api.ingestion_sequence_scope("scope")),
    )
    for kind, exemplar in identities:
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
                derived_signal_id="D013",
                subject_instrument="NVDA",
                effective_at_or_before_utc=NOW,
                knowledge_at_or_before_utc=NOW,
                limit=1000,
            )
            | changes
        )
    )


def unsafe_copy(record, **changes):
    """Adversarial public-read reply: constructors cannot conceal bad stored fields."""
    clone = object.__new__(type(record))
    for field in fields(record):
        object.__setattr__(clone, field.name, changes.get(field.name, getattr(record, field.name)))
    return clone


def snapshot(reads, occurrence):
    # Test explicitly calls producer first. This only reads already-returned fact.
    return f.PredecessorEvidenceV1(
        occurrence,
        reads.get_calculation_definition(
            derived_signal_id=occurrence.derived_signal_id,
            calculation_definition_version=occurrence.calculation_definition_version,
        ),
        reads.get_parameter_set(occurrence.parameter_context_refs[0]),
        reads.get_input_selection_policy(occurrence.parameter_context_refs[1]),
        tuple(reads.get_unit_convention(ref) for ref in occurrence.convention_refs),
        tuple(
            reads.get_projection_mapping(item.projection_mapping_ref)
            for item in occurrence.raw_input_lineage
        ),
    )


def assert_ratio(result, numerator, denominator):
    assert result is not None and type(result) is f.RatioOccurrenceV1
    assert type(result.result) is f.ExactRatioV1
    assert type(result.result.numerator) is type(result.result.denominator) is int
    assert (result.result.numerator, result.result.denominator) == (numerator, denominator)


@pytest.mark.parametrize("storage", ["sqlite", "memory"])
def test_d013_actual_predecessors_exact_ratio(tmp_path, storage):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    old_config = predecessor_configuration(raw.reads, tmp_path / "predecessors.sqlite")
    previous = f.create_owner(**old_config)
    midpoint = previous.materialise(predecessor_request(identity="D011"))
    spread = previous.materialise(predecessor_request(identity="D012"))
    assert midpoint.result.as_tuple() == Decimal("101").as_tuple()
    assert spread.result.as_tuple() == Decimal("2").as_tuple()
    assert (
        midpoint.implementation_brief_sha256
        == spread.implementation_brief_sha256
        == (PREDECESSOR_BRIEF)
    )
    ratio_seam()
    config = ratio_configuration(previous.reads, tmp_path / "ratio.sqlite")
    if storage == "memory":
        config["storage"] = f.MemoryStorageV1()
    owner = f.create_ratio_owner(**config)
    req = ratio_request(midpoint.derived_occurrence_id, spread.derived_occurrence_id)
    assert history(owner.reads) == ()
    result = owner.materialise(req)
    assert_ratio(result, 200, 101)
    evidence = (snapshot(previous.reads, midpoint), snapshot(previous.reads, spread))
    assert result.predecessor_evidence == evidence
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/exact_ratio/v1"
    assert result.implementation_brief_sha256 == BRIEF
    assert result.derived_signal_id == "D013" and result.subject_instrument == "NVDA"
    assert result.effective_as_of_utc == result.knowledge_cutoff_utc == ASOF
    assert result.calculated_at_utc == NOW
    assert result.calculation_definition_version == "D013-RELATIVE-SPREAD-1"
    assert result.units == "percent" and result.result_shape == "scalar_exact_ratio"
    assert result.raw_input_lineage == result.convention_refs == ()
    assert result.parameter_context_refs == (req.parameter_set_ref,)
    assert result.predecessor_occurrence_ids == req.predecessor_occurrence_ids
    assert result.window is result.universe is result.supersedes_derived_occurrence_id is None
    definition = config["definitions"][0]
    expected_hash = hashlib.sha256(canonical(definition)).hexdigest()
    logical = dict(
        owner_object_id="M02",
        owner_namespace=result.owner_namespace,
        implementation_brief_sha256=BRIEF,
        request=req,
        definition_content_sha256=expected_hash,
        parameter_set=config["parameter_sets"][0],
        predecessor_evidence=evidence,
    )
    assert result.definition_content_sha256 == expected_hash
    assert result.derived_occurrence_id == "mmtr1:" + hashlib.sha256(canonical(logical)).hexdigest()
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert history(owner.reads) == (result,)
    assert not hasattr(owner.reads, "materialise")
    for ev in evidence:
        assert type(ev.occurrence.result) is Decimal and len(ev.occurrence.raw_input_lineage) == 2
        assert ev.parameter_set == old_config["parameter_sets"][0]
        assert ev.input_selection_policy == old_config["input_selection_policies"][0]
        assert ev.unit_conventions == old_config["unit_conventions"]
        assert ev.projection_mappings == old_config["raw_projection_mappings"]
        for item, side in zip(ev.occurrence.raw_input_lineage, ("bid", "ask"), strict=True):
            assert item.projection == raw.reads.project_raw_value(
                raw_api.RawSignalCatalogueId("R034" if side == "bid" else "R035"),
                raw_api.observation_occurrence_id(f"mmt-pilot-{side}-001"),
                mappings=(mapping(side),),
            )
    for registered in config["definitions"]:
        assert (
            owner.reads.get_calculation_definition(
                derived_signal_id="D013",
                calculation_definition_version=registered.calculation_definition_version,
            )
            == registered
        )
    for parameter in config["parameter_sets"]:
        assert (
            owner.reads.get_parameter_set(f.VersionRefV1(parameter.context_id, parameter.version))
            == parameter
        )


REFUSALS = (
    "missing",
    "wrong-type",
    "owner",
    "namespace",
    "authority",
    "wrong-d",
    "order",
    "id",
    "definition-version",
    "definition-hash",
    "subject",
    "asof",
    "cutoff",
    "calculated-before",
    "calculated-after",
    "parameter-ref",
    "selection-ref",
    "extra-context",
    "unit-ref",
    "universe",
    "window",
    "supersedes",
    "predecessors",
    "result",
    "result-representation",
    "result-float",
    "units",
    "shape",
    "lineage-order",
    "canonical-representation",
    "lineage-event",
    "projection-provider",
    "projection-variant",
    "projection-field",
    "projection-rid",
    "projection-id",
    "projection-mapping",
    "projection-mapping-version",
    "projection-native-value",
    "projection-units",
    "projection-subject",
    "projection-temporal",
    "projection-time",
    "projection-timezone",
    "projection-receipt",
    "projection-sequence",
    "projection-scope",
    "projection-revision",
    "projection-identity",
    "missing-definition",
    "missing-parameter",
    "missing-selection",
    "missing-unit",
    "missing-mapping",
    "definition-content",
    "parameter-content",
    "selection-content",
    "unit-content",
    "mapping-content",
    "request-subject",
    "request-cutoff",
    "request-asof",
    "request-parameter",
    "request-definition",
    "unsupported-all",
    "reader-storage-failure",
)


@pytest.mark.parametrize("populated", [False, True])
@pytest.mark.parametrize("mode", REFUSALS)
def test_d013_predecessor_compatibility_and_refusal(tmp_path, populated, mode):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    previous = f.create_owner(
        **predecessor_configuration(raw.reads, tmp_path / "predecessors.sqlite", versions=(1, 2))
    )
    midpoint = previous.materialise(predecessor_request(identity="D011"))
    spread = previous.materialise(predecessor_request(identity="D012"))
    assert midpoint.result == Decimal("101") and spread.result == Decimal("2")
    ratio_seam()
    calls = []
    active = [False]

    class Reader:
        def get_derived_occurrence(self, identity):
            calls.append(identity)
            value = previous.reads.get_derived_occurrence(identity)
            if not active[0] or identity != midpoint.derived_occurrence_id:
                return value
            if mode == "missing":
                return None
            if mode == "wrong-type":
                return {"result": Decimal("101")}
            if mode == "reader-storage-failure":
                raise f.PersistenceFailureV1("truthful upstream storage failure")
            change = {
                "owner": dict(owner_object_id="M01"),
                "namespace": dict(owner_namespace="other/v1"),
                "authority": dict(implementation_brief_sha256=OLD_BRIEF),
                "wrong-d": dict(derived_signal_id="D012"),
                "id": dict(derived_occurrence_id="mmt1:" + "0" * 64),
                "definition-version": dict(calculation_definition_version="D011-MIDPOINT-2"),
                "definition-hash": dict(definition_content_sha256="0" * 64),
                "subject": dict(subject_instrument="OTHER"),
                "asof": dict(effective_as_of_utc=ASOF - timedelta(microseconds=1)),
                "cutoff": dict(knowledge_cutoff_utc=ASOF - timedelta(microseconds=1)),
                "calculated-before": dict(calculated_at_utc=ASOF - timedelta(microseconds=1)),
                "calculated-after": dict(calculated_at_utc=NOW + timedelta(microseconds=1)),
                "parameter-ref": dict(
                    parameter_context_refs=(
                        f.VersionRefV1("mmt-pilot-basic", 2),
                        value.parameter_context_refs[1],
                    )
                ),
                "selection-ref": dict(
                    parameter_context_refs=(
                        value.parameter_context_refs[0],
                        f.VersionRefV1("mmt-pilot-selection", 2),
                    )
                ),
                "extra-context": dict(
                    parameter_context_refs=(
                        *value.parameter_context_refs,
                        f.VersionRefV1("extra", 1),
                    )
                ),
                "unit-ref": dict(convention_refs=(f.VersionRefV1("mmt-pilot-price", 2),)),
                "universe": dict(universe=("NVDA",)),
                "window": dict(window="unauthorised"),
                "supersedes": dict(supersedes_derived_occurrence_id="other"),
                "predecessors": dict(predecessor_occurrence_ids=("other",)),
                "result": dict(result=Decimal("999")),
                "result-representation": dict(result=Decimal("101.0")),
                "result-float": dict(result=101.0),
                "units": dict(units="shares"),
                "shape": dict(result_shape="scalar_exact_ratio"),
                "lineage-order": dict(raw_input_lineage=tuple(reversed(value.raw_input_lineage))),
            }.get(mode, {})
            if mode in ("canonical-representation", "lineage-event") or mode.startswith(
                "projection-"
            ):
                first = value.raw_input_lineage[0]
                if mode == "canonical-representation":
                    first = unsafe_copy(first, canonical_value=Decimal("100.0"))
                elif mode == "lineage-event":
                    first = unsafe_copy(first, event_time_utc=ASOF)
                else:
                    projection = first.projection
                    changes = {
                        "projection-provider": dict(source_provider="OTHER"),
                        "projection-variant": dict(source_variant="OTHER"),
                        "projection-field": dict(native_field_path=("other",)),
                        "projection-rid": dict(
                            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R035")
                        ),
                        "projection-id": dict(
                            observation_occurrence_id=(raw_api.observation_occurrence_id("OTHER"))
                        ),
                        "projection-mapping": dict(projection_mapping_id="OTHER"),
                        "projection-mapping-version": dict(projection_mapping_version=2),
                        "projection-native-value": dict(native_value=Decimal("100.0")),
                        "projection-units": dict(native_units="shares"),
                        "projection-subject": dict(subject_instrument="OTHER"),
                        "projection-temporal": dict(source_temporal_kind="date_only"),
                        "projection-time": dict(source_timestamp_raw="2026-10-16T01:00:00Z"),
                        "projection-timezone": dict(source_timezone_native="OTHER"),
                        "projection-receipt": dict(received_ts_utc=NOW),
                        "projection-sequence": dict(ingestion_sequence=99),
                        "projection-scope": dict(
                            ingestion_sequence_scope=(raw_api.ingestion_sequence_scope("OTHER"))
                        ),
                        "projection-revision": dict(revision_vintage_native="OTHER"),
                        "projection-identity": dict(selection_identity="not-a-public-record"),
                    }[mode]
                    first = unsafe_copy(first, projection=unsafe_copy(projection, **changes))
                change = dict(raw_input_lineage=(first, value.raw_input_lineage[1]))
            return unsafe_copy(value, **change)

        def __getattr__(self, name):
            target = getattr(previous.reads, name)

            def getter(*args, **kwargs):
                value = target(*args, **kwargs)
                if not active[0]:
                    return value
                missing = {
                    "get_calculation_definition": "missing-definition",
                    "get_parameter_set": "missing-parameter",
                    "get_input_selection_policy": "missing-selection",
                    "get_unit_convention": "missing-unit",
                    "get_projection_mapping": "missing-mapping",
                }
                if mode == missing.get(name):
                    return None
                if name == "get_calculation_definition" and mode == "definition-content":
                    return replace(value, equation="abs(D012)")
                if name == "get_parameter_set" and mode == "parameter-content":
                    return replace(value, members=("OTHER",))
                if name == "get_input_selection_policy" and mode == "selection-content":
                    return replace(value, maximum_skew=timedelta(seconds=11))
                if name == "get_unit_convention" and mode == "unit-content":
                    return replace(value, scale=Decimal("2"))
                if name == "get_projection_mapping" and mode == "mapping-content":
                    return replace(value, native_field_path=("other",))
                return value

            return getter

    owner = f.create_ratio_owner(**ratio_configuration(Reader(), tmp_path / "ratio.sqlite"))
    request = ratio_request(midpoint.derived_occurrence_id, spread.derived_occurrence_id)
    if populated:
        assert_ratio(owner.materialise(request), 200, 101)
    before = history(owner.reads)
    assert len(before) == int(populated)
    calls.clear()
    active[0] = True
    if mode == "order":
        request = replace(
            request, predecessor_occurrence_ids=tuple(reversed(request.predecessor_occurrence_ids))
        )
    request = {
        "request-subject": lambda: replace(request, subject_instrument="OTHER"),
        "request-cutoff": lambda: replace(request, knowledge_cutoff_utc=NOW),
        "request-asof": lambda: replace(request, as_of_utc=ASOF - timedelta(microseconds=1)),
        "request-parameter": lambda: replace(
            request, parameter_set_ref=f.VersionRefV1("mmt-pilot-basic", 2)
        ),
        "request-definition": lambda: replace(request, calculation_definition_version="OTHER"),
    }.get(mode, lambda: request)()
    if mode == "unsupported-all":
        for number in range(1, 210):
            if number == 13:
                continue
            # Each call has its own read budget, regardless of validation order.
            calls.clear()
            assert owner.materialise(replace(request, derived_signal_id=f"D{number:03d}")) is None
            assert history(owner.reads) == before
            assert len(calls) == len(set(calls))
    elif mode == "reader-storage-failure":
        with pytest.raises(f.PersistenceFailureV1) as failed:
            owner.materialise(request)
        assert failed.value.outcome_uncertain is False
        assert history(owner.reads) == before
    else:
        assert owner.materialise(request) is None
        assert history(owner.reads) == before
    assert len(calls) == len(set(calls))


@pytest.mark.parametrize(
    "bid,ask,numerator,denominator",
    [
        ("100", "102", 200, 101),
        ("1", "3", 100, 1),
        ("102", "100", -200, 101),
        ("-3", "-1", -100, 1),
        ("100.00", "100.0", 0, 1),
        ("-0.000", "2.00", 200, 1),
        ("-1", "1", None, None),
        ("-0.000", "0.00", None, None),
        ("1E+5000", "3E+5000", 100, 1),
        ("1E-5000", "3E-5000", 100, 1),
        ("-1", "1." + "0" * 4999 + "1", 4 * 10**5002 + 200, 1),
        ("1", "1." + "0" * 4999 + "1", 200, 2 * 10**5000 + 1),
    ],
    ids=[
        "nonterminating",
        "integer",
        "crossed",
        "negative",
        "zero",
        "signed-zero-input",
        "zero-midpoint",
        "all-zero",
        "large-exponent",
        "tiny-exponent",
        "huge-numerator-wire",
        "huge-denominator-wire",
    ],
)
def test_d013_exact_ratio_canonical_domain(tmp_path, bid, ask, numerator, denominator):
    conversion_limit = sys.get_int_max_str_digits()
    raw = raw_source(tmp_path / "raw.sqlite")
    for side, literal in (("bid", bid), ("ask", ask)):
        raw.commands.admit_raw_observation_occurrence(observation(side, value=Decimal(literal)))
    previous = f.create_owner(
        **predecessor_configuration(raw.reads, tmp_path / "predecessors.sqlite")
    )
    with localcontext() as context:
        context.prec = 2
        context.traps[Inexact] = context.traps[Rounded] = True
        midpoint = previous.materialise(predecessor_request(identity="D011"))
        spread = previous.materialise(predecessor_request(identity="D012"))
    assert midpoint is not None and spread is not None
    ratio_seam()
    config = ratio_configuration(previous.reads, tmp_path / "ratio.sqlite")
    owner = f.create_ratio_owner(**config)
    request = ratio_request(midpoint.derived_occurrence_id, spread.derived_occurrence_id)
    with localcontext() as context:
        context.prec = 1
        context.traps[Inexact] = context.traps[Rounded] = True
        result = owner.materialise(request)
    if numerator is None:
        assert result is None and history(owner.reads) == ()
    else:
        assert_ratio(result, numerator, denominator)
        for evidence in result.predecessor_evidence:
            for item, literal in zip(
                evidence.occurrence.raw_input_lineage, (bid, ask), strict=True
            ):
                assert item.canonical_value.as_tuple() == Decimal(literal).as_tuple()
                assert item.projection.native_value.as_tuple() == Decimal(literal).as_tuple()
        assert owner.materialise(request) == result
        readonly = f.create_ratio_reader(
            admission=config["admission"],
            storage=f.SQLiteReadStorageV1(str(tmp_path / "ratio.sqlite")),
        )
        assert readonly.get_derived_occurrence(result.derived_occurrence_id) == result
        with sqlite3.connect(tmp_path / "ratio.sqlite") as connection:
            payload = connection.execute("SELECT payload FROM mmt_ratio_occurrence_v1").fetchone()[
                0
            ]
        wire = json.loads(payload)["result"]
        assert wire == dict(
            kind="exact_ratio",
            numerator=integer_text(numerator),
            denominator=integer_text(denominator),
        )
        if numerator == 4 * 10**5002 + 200:
            assert wire["numerator"] == "4" + "0" * 4999 + "200"
        if denominator == 2 * 10**5000 + 1:
            assert wire["denominator"] == "2" + "0" * 4999 + "1"
    assert sys.get_int_max_str_digits() == conversion_limit
    for n, d in ((0, 1), (1, 1), (-2, 3)):
        exact = f.ExactRatioV1(n, d)
        assert exact.numerator == n and exact.denominator == d
        assert not hasattr(exact, "__dict__")
        with pytest.raises(FrozenInstanceError):
            exact.numerator = 0
    for n, d in ((2, 2), (0, 2), (1, 0), (1, -2), (2, 4)):
        with pytest.raises(ValueError):
            f.ExactRatioV1(n, d)
    for n, d in ((True, 1), (1, True), (1.0, 1), (1, "1"), (Decimal("1"), 1)):
        with pytest.raises(TypeError):
            f.ExactRatioV1(n, d)


@pytest.mark.parametrize(
    "dimension",
    [
        "definition",
        "midpoint-definition",
        "spread-definition",
        "parameter",
        "selection",
        "bid-mapping",
        "ask-mapping",
        "unit",
        "observation-identity",
        "representation",
        "cutoff",
        "asof",
    ],
)
def test_d013_identity_versions_and_later_retry(tmp_path, dimension):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    previous = f.create_owner(
        **predecessor_configuration(raw.reads, tmp_path / "predecessors.sqlite", versions=(1, 2))
    )
    base_mid = predecessor_request(identity="D011")
    base_spread = predecessor_request(identity="D012")
    midpoint = previous.materialise(base_mid)
    spread = previous.materialise(base_spread)
    assert midpoint.result == Decimal("101") and spread.result == Decimal("2")
    ratio_seam()
    clock = [NOW]
    config = ratio_configuration(previous.reads, tmp_path / "ratio.sqlite", now=lambda: clock[0])
    owner = f.create_ratio_owner(**config)
    request = ratio_request(midpoint.derived_occurrence_id, spread.derived_occurrence_id)
    first = owner.materialise(request)
    assert_ratio(first, 200, 101)
    clock[0] += timedelta(days=1)
    assert owner.materialise(request) == first and first.calculated_at_utc == NOW
    next_request = request
    if dimension == "definition":
        next_request = replace(request, calculation_definition_version="D013-RELATIVE-SPREAD-2")
    else:

        def altered(req):
            if dimension in ("midpoint-definition", "spread-definition"):
                which = "D011" if dimension == "midpoint-definition" else "D012"
                if req.derived_signal_id == which:
                    label = "MIDPOINT" if which == "D011" else "SPREAD"
                    return replace(req, calculation_definition_version=f"{which}-{label}-2")
            if dimension == "parameter":
                return replace(req, parameter_set_ref=f.VersionRefV1("mmt-pilot-basic", 2))
            if dimension == "selection":
                return replace(
                    req, input_selection_policy_ref=f.VersionRefV1("mmt-pilot-selection", 2)
                )
            if dimension in ("bid-mapping", "ask-mapping"):
                index = 0 if dimension == "bid-mapping" else 1
                bindings = list(req.raw_input_bindings)
                bindings[index] = replace(
                    bindings[index],
                    projection_mapping_ref=f.VersionRefV1(
                        "mmt-pilot-bid" if index == 0 else "mmt-pilot-ask", 2
                    ),
                )
                return replace(req, raw_input_bindings=tuple(bindings))
            if dimension == "unit":
                return replace(
                    req,
                    raw_input_bindings=tuple(
                        replace(binding, unit_convention_ref=f.VersionRefV1("mmt-pilot-price", 2))
                        for binding in req.raw_input_bindings
                    ),
                )
            if dimension == "cutoff":
                return replace(req, knowledge_cutoff_utc=NOW)
            if dimension == "asof":
                return replace(req, as_of_utc=ASOF - timedelta(microseconds=1))
            return req

        if dimension in ("observation-identity", "representation"):
            raw.commands.admit_raw_observation_occurrence(
                observation(
                    "bid",
                    identity="same-source-new-identity",
                    sequence=3,
                    event=ASOF,
                    receipt=ASOF,
                    value=Decimal("100.0" if dimension == "representation" else "100"),
                )
            )
        next_mid = previous.materialise(altered(base_mid))
        next_spread = previous.materialise(altered(base_spread))
        assert next_mid.result == Decimal("101") and next_spread.result == Decimal("2")
        if dimension not in ("midpoint-definition", "spread-definition"):
            # A one-sided pair is independently refused, even though both facts
            # are lawful and the numerical answer would be the same.
            mismatched = replace(
                request,
                predecessor_occurrence_ids=(
                    next_mid.derived_occurrence_id,
                    spread.derived_occurrence_id,
                ),
            )
            assert owner.materialise(mismatched) is None
            assert history(owner.reads) == (first,)
        next_request = replace(
            request,
            predecessor_occurrence_ids=(
                next_mid.derived_occurrence_id,
                next_spread.derived_occurrence_id,
            ),
        )
        if dimension == "parameter":
            next_request = replace(
                next_request, parameter_set_ref=f.VersionRefV1("mmt-pilot-basic", 2)
            )
        if dimension == "cutoff":
            next_request = replace(next_request, knowledge_cutoff_utc=NOW)
        if dimension == "asof":
            next_request = replace(next_request, as_of_utc=ASOF - timedelta(microseconds=1))
    second = owner.materialise(next_request)
    assert_ratio(second, 200, 101)
    assert second.derived_occurrence_id != first.derived_occurrence_id
    assert second.calculated_at_utc == clock[0]
    assert owner.materialise(next_request) == second
    assert owner.reads.get_derived_occurrence(first.derived_occurrence_id) == first
    assert owner.reads.get_derived_occurrence(second.derived_occurrence_id) == second
    expected = tuple(
        sorted(
            (first, second),
            key=lambda item: (
                item.effective_as_of_utc,
                item.knowledge_cutoff_utc,
                item.derived_occurrence_id,
            ),
            reverse=True,
        )
    )
    assert history(owner.reads) == expected
    assert history(owner.reads, limit=1) == expected[:1]
    assert history(owner.reads, effective_at_or_before_utc=ASOF - timedelta(seconds=1)) == ()
    assert history(owner.reads, knowledge_at_or_before_utc=ASOF - timedelta(seconds=1)) == ()
    assert history(owner.reads, subject_instrument="OTHER") == ()
    for bad in (0, 1001):
        with pytest.raises(ValueError):
            history(owner.reads, limit=bad)
    for bad in (True, 1.0):
        with pytest.raises(TypeError):
            history(owner.reads, limit=bad)
    assert owner.reads.get_derived_occurrence("absent") is None
    assert owner.reads.get_parameter_set(f.VersionRefV1("absent", 1)) is None
    assert (
        owner.reads.get_calculation_definition(
            derived_signal_id="D013", calculation_definition_version="absent"
        )
        is None
    )
    # Identical registration is idempotent; unsupported conflicting payload
    # must not partially register the valid new second definition.
    atomic_path = tmp_path / "atomic.sqlite"
    atomic = ratio_configuration(previous.reads, atomic_path, versions=(1,))
    original = f.create_ratio_owner(**atomic)
    f.create_ratio_owner(**(atomic | {"storage": f.SQLiteStorageV1(str(atomic_path), False)}))
    changed = config["definitions"][1]
    conflict = replace(atomic["definitions"][0], equation="abs(D012)")
    with pytest.raises((ValueError, f.PersistenceFailureV1)):
        f.create_ratio_owner(
            **(
                atomic
                | {
                    "definitions": (changed, conflict),
                    "storage": f.SQLiteStorageV1(str(atomic_path), False),
                }
            )
        )
    assert (
        original.reads.get_calculation_definition(
            derived_signal_id="D013", calculation_definition_version="D013-RELATIVE-SPREAD-2"
        )
        is None
    )
    assert (
        original.reads.get_calculation_definition(
            derived_signal_id="D013", calculation_definition_version="D013-RELATIVE-SPREAD-1"
        )
        == atomic["definitions"][0]
    )

    before_parameters = tuple(
        original.reads.get_parameter_set(f.VersionRefV1("mmt-pilot-basic", version))
        for version in (1, 2)
    )
    with pytest.raises((ValueError, f.PersistenceFailureV1)):
        f.create_ratio_owner(
            **(
                atomic
                | {
                    "parameter_sets": (
                        config["parameter_sets"][1],
                        replace(atomic["parameter_sets"][0], members=("OTHER",)),
                    ),
                    "storage": f.SQLiteStorageV1(str(atomic_path), False),
                }
            )
        )
    assert (
        tuple(
            original.reads.get_parameter_set(f.VersionRefV1("mmt-pilot-basic", version))
            for version in (1, 2)
        )
        == before_parameters
    )


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
    "nested-config",
    "nested-correct-rehash-equation",
    "correct-rehash-equation",
    "wrong-owner",
    "wrong-version",
    "extra-table",
    "missing-trigger",
    "parameter-link",
    "definition-link",
)


@pytest.mark.parametrize("mode", STORAGE_CASES)
def test_d013_sqlite_recovery_faults_and_integrity(tmp_path, monkeypatch, mode):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    predecessor_path = tmp_path / "predecessors.sqlite"
    previous = f.create_owner(**predecessor_configuration(raw.reads, predecessor_path))
    midpoint = previous.materialise(predecessor_request(identity="D011"))
    spread = previous.materialise(predecessor_request(identity="D012"))
    assert midpoint.result == Decimal("101") and spread.result == Decimal("2")
    ratio_seam()
    assert importlib.util.find_spec("nvda_desk.market_measurement_truth._rational_sqlite") is not (
        None
    ), "admitted isolated ratio SQLite behaviour is absent"
    path = tmp_path / "ratio.sqlite"
    config = ratio_configuration(previous.reads, path)
    owner = f.create_ratio_owner(**config)
    request = ratio_request(midpoint.derived_occurrence_id, spread.derived_occurrence_id)
    original_connect = sqlite3.connect
    table = "mmt_ratio_occurrence_v1"
    if mode in ("precommit", "postcommit", "competing"):
        mechanism = importlib.import_module("nvda_desk.market_measurement_truth._rational_sqlite")
        reached = []
        phase = [mode]
        inserted, release = Event(), Event()

        class ControlledConnection(sqlite3.Connection):
            wrote = False

            def execute(self, sql, *args, **kwargs):
                statement = sql.strip().upper()
                if statement == "COMMIT" and self.wrote and phase[0] == "precommit":
                    reached.append("before")
                    raise sqlite3.OperationalError("deliberate native precommit failure")
                result = super().execute(sql, *args, **kwargs)
                if statement.startswith("INSERT") and table.upper() in statement:
                    self.wrote = True
                    if phase[0] == "competing":
                        inserted.set()
                        assert release.wait(timeout=10), "first public write not released"
                if statement == "COMMIT" and self.wrote and phase[0] == "postcommit":
                    reached.append("after")
                    raise sqlite3.OperationalError("deliberate lost commit acknowledgement")
                return result

        def connect(*args, **kwargs):
            if str(args[0]).startswith(path.as_uri() + "?"):
                kwargs["factory"] = ControlledConnection
            return original_connect(*args, **kwargs)

        monkeypatch.setattr(mechanism.sqlite3, "connect", connect)
        assert history(owner.reads) == ()
        if mode == "competing":
            second = f.create_ratio_owner(
                **(
                    config
                    | {
                        "storage": f.SQLiteStorageV1(str(path), False),
                        "utc_now": lambda: NOW + timedelta(days=1),
                    }
                )
            )
            with ThreadPoolExecutor(max_workers=1) as pool:
                pending = pool.submit(owner.materialise, request)
                try:
                    assert inserted.wait(timeout=10), "actual first INSERT not reached"
                    assert history(second.reads) == ()
                    with original_connect(path) as direct:
                        assert direct.execute("SELECT count(*) FROM " + table).fetchone() == (0,)
                    with pytest.raises(f.PersistenceFailureV1) as busy:
                        second.materialise(request)
                    assert busy.value.outcome_uncertain is False
                finally:
                    release.set()
                fact = pending.result(timeout=20)
            phase[0] = "none"
            assert second.materialise(request) == fact
        else:
            with pytest.raises(f.PersistenceFailureV1) as failed:
                owner.materialise(request)
            assert failed.value.outcome_uncertain is (mode == "postcommit")
            assert reached == (["before"] if mode == "precommit" else ["after"])
            phase[0] = "none"
            observed = history(owner.reads)
            assert len(observed) == int(mode == "postcommit")
            fact = owner.materialise(request)
            if mode == "postcommit":
                assert fact == observed[0]
        monkeypatch.undo()
        assert_ratio(fact, 200, 101)
        assert fact.calculated_at_utc == NOW
        assert history(owner.reads) == (fact,)
        return
    fact = owner.materialise(request)
    assert_ratio(fact, 200, 101)
    assert history(owner.reads) == (fact,)
    if mode == "profile":
        mechanism = importlib.import_module("nvda_desk.market_measurement_truth._rational_sqlite")
        observed_connections = []
        observed_policy = []

        class ObservedConnection(sqlite3.Connection):
            def execute(self, sql, *args, **kwargs):
                result = super().execute(sql, *args, **kwargs)
                if sql.strip().upper() == "BEGIN IMMEDIATE":
                    observed_policy.append(
                        (
                            "write",
                            super().execute("PRAGMA synchronous").fetchone()[0],
                            super().execute("PRAGMA foreign_keys").fetchone()[0],
                            super().execute("PRAGMA busy_timeout").fetchone()[0],
                        )
                    )
                if sql.strip().upper() == "BEGIN":
                    observed_policy.append(
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
                observed_connections.append((str(args[0]), kwargs.get("uri")))
                kwargs["factory"] = ObservedConnection
            return original_connect(*args, **kwargs)

        monkeypatch.setattr(mechanism.sqlite3, "connect", observed_connect)
        # Observe mandatory write policy on a genuinely new logical fact.
        # The subsequent original-fact retry may lawfully be read-only.
        new_request = replace(request, calculation_definition_version="D013-RELATIVE-SPREAD-2")
        new_fact = owner.materialise(new_request)
        assert_ratio(new_fact, 200, 101)
        assert new_fact.derived_occurrence_id != fact.derived_occurrence_id
        assert ("write", 3, 1, 0) in observed_policy
        assert any(url == path.as_uri() + "?mode=rw" for url, _ in observed_connections)
        assert owner.materialise(request) == fact
        independent = f.create_ratio_reader(
            admission=config["admission"], storage=f.SQLiteReadStorageV1(str(path))
        )
        assert independent.get_derived_occurrence(fact.derived_occurrence_id) == fact
        assert ("read", 1, 1, 0) in observed_policy
        assert all(uri is True for _, uri in observed_connections)
        assert any(url == path.as_uri() + "?mode=ro" for url, _ in observed_connections)
        monkeypatch.undo()
        with original_connect(path) as connection:
            assert connection.execute("PRAGMA application_id").fetchone() == (0x4E560003,)
            assert connection.execute("PRAGMA user_version").fetchone() == (1,)
            assert connection.execute("PRAGMA journal_mode").fetchone() == ("delete",)
            tables = dict(
                connection.execute(
                    "SELECT name,strict FROM pragma_table_list WHERE name NOT LIKE 'sqlite_%'"
                )
            )
            assert tables == {"mmt_ratio_definition_v1": 1, "mmt_ratio_parameter_v1": 1, table: 1}
            assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
            triggers = connection.execute(
                "SELECT tbl_name,sql FROM sqlite_schema WHERE type='trigger'"
            ).fetchall()
            assert len(triggers) == 6
            for current in tables:
                assert all(
                    row[3] == 1 for row in connection.execute("PRAGMA table_info(" + current + ")")
                )
                for operation in ("UPDATE", "DELETE"):
                    assert (
                        sum(
                            name == current and "BEFORE " + operation in sql.upper()
                            for name, sql in triggers
                        )
                        == 1
                    )
                    with pytest.raises(sqlite3.IntegrityError):
                        connection.execute(
                            ("DELETE FROM " + current)
                            if operation == "DELETE"
                            else ("UPDATE " + current + " SET payload=payload")
                        )
            assert connection.execute("SELECT count(*) FROM " + table).fetchone() == (2,)
        for other in (tmp_path / "raw.sqlite", predecessor_path):
            before = other.read_bytes()
            with pytest.raises((ValueError, f.PersistenceFailureV1)):
                f.create_ratio_reader(
                    admission=config["admission"], storage=f.SQLiteReadStorageV1(str(other))
                )
            with pytest.raises((ValueError, f.PersistenceFailureV1)):
                f.create_ratio_owner(
                    **(
                        config
                        | {
                            "storage": f.SQLiteStorageV1(str(other), False),
                        }
                    )
                )
            assert other.read_bytes() == before
        before = path.read_bytes()
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_reader(
                admission=f.OwnerAdmissionV1("M02", PREDECESSOR_BRIEF),
                storage=f.SQLiteReadStorageV1(str(path)),
            )
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_owner(**(predecessor_configuration(raw.reads, path, create=False)))
        with pytest.raises(f.PersistenceFailureV1):
            f.create_ratio_owner(**config)  # exclusive create cannot overwrite
        assert path.read_bytes() == before
        absent = tmp_path / "absent.sqlite"
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_ratio_reader(
                admission=config["admission"], storage=f.SQLiteReadStorageV1(str(absent))
            )
        assert not absent.exists()
        link = tmp_path / "link.sqlite"
        link.symlink_to(path)
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_ratio_reader(
                admission=config["admission"], storage=f.SQLiteReadStorageV1(str(link))
            )
        assert path.read_bytes() == before
        return
    if mode == "readonly-process":
        env = dict(
            os.environ, PYTHONPATH=os.pathsep.join([str(ROOT / "src"), str(Path(__file__).parent)])
        )
        writer_code = """
import base64,pickle,sys
from pathlib import Path
from _support import (raw_source,observation,predecessor_configuration,
    predecessor_request,ratio_configuration,ratio_request,f)
root=Path(sys.argv[1])
raw=raw_source(root/'child-raw.sqlite')
for side in ('bid','ask'): raw.commands.admit_raw_observation_occurrence(observation(side))
old=f.create_owner(**predecessor_configuration(raw.reads,root/'child-previous.sqlite'))
mid=old.materialise(predecessor_request(identity='D011'))
spread=old.materialise(predecessor_request(identity='D012'))
owner=f.create_ratio_owner(**ratio_configuration(old.reads,root/'child-ratio.sqlite'))
value=owner.materialise(ratio_request(mid.derived_occurrence_id,spread.derived_occurrence_id))
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
        reader_code = """
import base64,pickle,sys
from nvda_desk.market_measurement_truth import api as f
reads=f.create_ratio_reader(admission=f.OwnerAdmissionV1('M02',sys.argv[2]),
    storage=f.SQLiteReadStorageV1(sys.argv[1]))
value=reads.get_derived_occurrence(sys.argv[3])
bundle=dict(occurrence=value,
    definitions=tuple(reads.get_calculation_definition(derived_signal_id='D013',
        calculation_definition_version='D013-RELATIVE-SPREAD-'+str(v)) for v in (1,2)),
    parameters=tuple(reads.get_parameter_set(f.VersionRefV1('mmt-pilot-basic',v)) for v in (1,2)),
    history=reads.list_derived_history(derived_signal_id='D013',subject_instrument='NVDA',
        effective_at_or_before_utc=value.effective_as_of_utc,
        knowledge_at_or_before_utc=value.knowledge_cutoff_utc,limit=1000),
    has_writer=hasattr(reads,'materialise'))
print(base64.b64encode(pickle.dumps(bundle)).decode())
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
            occurrence=fact,
            definitions=config["definitions"],
            parameters=config["parameter_sets"],
            history=(fact,),
            has_writer=False,
        )
        assert child_path.read_bytes() == before
        return
    with original_connect(path) as connection:
        if mode == "wrong-owner":
            connection.execute("PRAGMA application_id=1314258945")
        elif mode == "wrong-version":
            connection.execute("PRAGMA user_version=2")
        elif mode == "extra-table":
            connection.execute("CREATE TABLE extra(value TEXT)")
        elif mode == "missing-trigger":
            name = connection.execute(
                "SELECT name FROM sqlite_schema WHERE type='trigger' LIMIT 1"
            ).fetchone()[0]
            connection.execute('DROP TRIGGER "' + name + '"')
        else:
            triggers = connection.execute(
                "SELECT name,sql FROM sqlite_schema WHERE type='trigger'"
            ).fetchall()
            for name, _ in triggers:
                connection.execute('DROP TRIGGER "' + name + '"')
            payload, logical = connection.execute(
                "SELECT payload,logical_identity_payload FROM " + table
            ).fetchone()
            doc, identity = json.loads(payload), json.loads(logical)
            if mode == "payload":
                connection.execute("UPDATE " + table + " SET payload=?", (payload + b" ",))
            elif mode == "content-hash":
                connection.execute("UPDATE " + table + " SET content_sha256=?", ("0" * 64,))
            elif mode == "logical-hash":
                connection.execute(
                    "UPDATE " + table + " SET logical_identity_sha256=?", ("0" * 64,)
                )
            elif mode == "index":
                connection.execute("UPDATE " + table + " SET subject_instrument='OTHER'")
            elif mode in ("parameter-link", "definition-link"):
                target = (
                    "mmt_ratio_parameter_v1"
                    if mode == "parameter-link"
                    else ("mmt_ratio_definition_v1")
                )
                connection.execute("DELETE FROM " + target)
            else:
                if mode == "noncanonical-ratio":
                    doc["result"]["numerator"] = "400"
                    doc["result"]["denominator"] = "202"
                elif mode == "noncanonical-integer":
                    doc["result"]["numerator"] = "+200"
                elif mode == "correct-rehash-equation":
                    doc["result"]["numerator"] = "999"
                    doc["result"]["denominator"] = "1"
                elif mode in ("nested-config", "nested-correct-rehash-equation"):
                    for current in (doc, identity):
                        evidence = current["predecessor_evidence"][0]
                        if mode == "nested-config":
                            evidence["parameter_set"]["members"] = ["OTHER"]
                        else:
                            evidence["occurrence"]["result"] = dict(
                                kind="decimal", sign=0, digits="999", exponent=0
                            )
                    if mode == "nested-correct-rehash-equation":
                        # Outer equation is correct for the forged input; only
                        # complete old-fact validation can reject this corruption.
                        doc["result"] = dict(kind="exact_ratio", numerator="200", denominator="999")
                    logical = json.dumps(
                        identity, sort_keys=True, ensure_ascii=True, separators=(",", ":")
                    ).encode()
                    digest = hashlib.sha256(logical).hexdigest()
                    doc["derived_occurrence_id"] = "mmtr1:" + digest
                    connection.execute(
                        "UPDATE "
                        + table
                        + " SET derived_occurrence_id=?,logical_identity_payload=?,"
                        "logical_identity_sha256=?",
                        (doc["derived_occurrence_id"], logical, digest),
                    )
                payload = json.dumps(
                    doc, sort_keys=True, ensure_ascii=True, separators=(",", ":")
                ).encode()
                connection.execute(
                    "UPDATE " + table + " SET payload=?,content_sha256=?",
                    (payload, hashlib.sha256(payload).hexdigest()),
                )
            for _, sql in triggers:
                connection.execute(sql)
    with pytest.raises((ValueError, f.PersistenceFailureV1)):
        f.create_ratio_reader(
            admission=config["admission"], storage=f.SQLiteReadStorageV1(str(path))
        )

    corrupted_bytes = path.read_bytes()
    with pytest.raises((ValueError, f.PersistenceFailureV1)):
        f.create_ratio_owner(**(config | {"storage": f.SQLiteStorageV1(str(path), False)}))
    assert path.read_bytes() == corrupted_bytes


def test_d013_additive_types_and_legacy_preservation(tmp_path):
    raw = raw_source(tmp_path / "raw.sqlite")
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    old_path = tmp_path / "predecessors.sqlite"
    old_config = predecessor_configuration(raw.reads, old_path, versions=(1, 2))
    previous = f.create_owner(**old_config)
    midpoint = previous.materialise(predecessor_request(identity="D011"))
    spread = previous.materialise(predecessor_request(identity="D012"))
    assert type(midpoint.result) is type(spread.result) is Decimal
    ratio_seam()
    config = ratio_configuration(previous.reads, tmp_path / "ratio.sqlite")
    owner = f.create_ratio_owner(**config)
    request = ratio_request(midpoint.derived_occurrence_id, spread.derived_occurrence_id)
    result = owner.materialise(request)
    assert_ratio(result, 200, 101)
    old_reader = f.create_reader(
        admission=old_config["admission"], storage=f.SQLiteReadStorageV1(str(old_path))
    )
    assert old_reader.get_derived_occurrence(midpoint.derived_occurrence_id) == midpoint
    assert old_reader.get_derived_occurrence(spread.derived_occurrence_id) == spread
    assert previous.materialise(predecessor_request(identity="D013")) is None
    assert not isinstance(result, f.DerivedSignalOccurrenceV1)
    assert type(result.result) is not Decimal
    original_fields = fields(f.DerivedSignalOccurrenceV1)
    new_fields = fields(f.RatioOccurrenceV1)
    assert [field.name for field in new_fields] == (
        [field.name for field in original_fields] + ["predecessor_evidence"]
    )
    for old, new in zip(original_fields, new_fields, strict=False):
        if old.name != "result":
            assert old.type == new.type
    assert not hasattr(result, "__dict__")
    with pytest.raises(FrozenInstanceError):
        result.units = "shares"
    with pytest.raises(TypeError):
        f.RatioCalculationRequestV1(
            **{
                field.name: (
                    ["bad", "ids"]
                    if field.name == "predecessor_occurrence_ids"
                    else getattr(request, field.name)
                )
                for field in fields(request)
            }
        )
    with pytest.raises(ValueError):
        replace(request, as_of_utc=ASOF.replace(tzinfo=None))
    with pytest.raises(ValueError):
        replace(request, subject_instrument="")
    with pytest.raises(TypeError):
        replace(result, result=Decimal("2"))
    # New factory admission is exact, not inherited by old/foreign authority.
    for admission in (
        f.OwnerAdmissionV1("M02", PREDECESSOR_BRIEF),
        f.OwnerAdmissionV1("M02", OLD_BRIEF),
        f.OwnerAdmissionV1("M01", BRIEF),
    ):
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_ratio_owner(
                **(
                    config
                    | {
                        "admission": admission,
                        "storage": f.MemoryStorageV1(),
                    }
                )
            )
    for key, values in (
        ("definitions", (replace(config["definitions"][0], derived_signal_id="D011"),)),
        ("definitions", (replace(config["definitions"][0], equation="D012 / D011"),)),
        ("parameter_sets", (replace(config["parameter_sets"][0], profile="STRATEGY"),)),
    ):
        with pytest.raises((ValueError, f.PersistenceFailureV1)):
            f.create_ratio_owner(**(config | {key: values, "storage": f.MemoryStorageV1()}))
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
    assert len(expected) == len(observed) == bad.stdout.count("error:") == 7
    assert {(int(line), code) for line, code in observed} == expected
    # Public original declarations remain AST-identical; adding new exports is
    # permitted, widening/changing existing Decimal declarations is not.
    api_path = "src/nvda_desk/market_measurement_truth/api.py"
    baseline = subprocess.check_output(
        ["git", "show", "5f998db9c0b9410dbb595286a5d6cdbd48c67a82:" + api_path], cwd=ROOT
    ).decode()
    original_tree = ast.parse(baseline)
    new_nodes = {
        node.name: node
        for node in ast.parse((ROOT / api_path).read_text()).body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef))
    }
    for node in original_tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and not node.name.startswith("_"):
            assert ast.dump(node) == ast.dump(new_nodes[node.name])
    exports = next(
        node
        for node in original_tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
    )
    assert set(ast.literal_eval(exports.value)) <= set(f.__all__)
