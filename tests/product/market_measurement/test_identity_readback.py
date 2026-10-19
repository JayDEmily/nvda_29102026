"""FND-P05: independently encoded logical identity and immutable typed content."""

import hashlib
import json
from dataclasses import fields, is_dataclass, replace
from datetime import datetime, timedelta
from decimal import Decimal, localcontext

import pytest
from _support import ASOF, NOW, configuration, foundation, observation, request

from nvda_desk.raw_signal_occurrence_truth import api as raw_api


def tagged(value):
    if type(value) is Decimal:
        t = value.as_tuple()
        return {
            "kind": "decimal",
            "sign": t.sign,
            "digits": "".join(map(str, t.digits)),
            "exponent": t.exponent,
        }
    if type(value) is datetime:
        return value.strftime("%Y-%m-%dT%H:%M:%S.") + f"{value.microsecond:06d}Z"
    if type(value) is timedelta:
        return (value.days * 86400 + value.seconds) * 1000000 + value.microseconds
    for factory in (
        raw_api.RawSignalCatalogueId,
        raw_api.observation_occurrence_id,
        raw_api.ingestion_sequence_scope,
    ):
        witness = factory("R034" if factory is raw_api.RawSignalCatalogueId else "identity")
        if type(value) is type(witness):
            return {"kind": factory.__name__, "value": value.value}
    if is_dataclass(value):
        return {field.name: tagged(getattr(value, field.name)) for field in fields(value)}
    if type(value) is tuple:
        return [tagged(item) for item in value]
    if type(value) is dict:
        return {key: tagged(item) for key, item in value.items()}
    assert value is None or type(value) in (str, int, bool)
    return value


def canonical(value):
    return json.dumps(
        tagged(value), ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode()


def test_retry_recalculation_and_definition_readback():
    raw = raw_api.create_owner()
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    f = foundation()
    clock = [NOW]
    config = configuration(f, raw.reads, now=lambda: clock[0], versions=(1, 2))
    o = f.create_owner(**config)
    req = request(f)
    result = o.materialise(req)
    definition = config["definitions"][0]
    digest = hashlib.sha256(canonical(definition)).hexdigest()
    expected = dict(
        owner_object_id="M02",
        owner_namespace="neutral_market_measurement_truth/v1",
        implementation_brief_sha256=config["admission"].implementation_brief_sha256,
        request=req,
        definition_content_sha256=digest,
        parameter_set=config["parameter_sets"][0],
        input_selection_policy=config["input_selection_policies"][0],
        unit_conventions=(config["unit_conventions"][0],),
        projection_mappings=config["raw_projection_mappings"][:2],
        raw_input_lineage=result.raw_input_lineage,
    )
    assert result.definition_content_sha256 == digest
    assert result.derived_occurrence_id == "mmt1:" + hashlib.sha256(canonical(expected)).hexdigest()
    clock[0] += timedelta(days=1)
    assert canonical(o.materialise(req)) == canonical(result)
    assert o.reads.get_parameter_set(req.parameter_set_ref) == config["parameter_sets"][0]
    assert (
        o.reads.get_input_selection_policy(req.input_selection_policy_ref)
        == config["input_selection_policies"][0]
    )
    assert (
        o.reads.get_unit_convention(f.VersionRefV1("mmt-pilot-price", 1))
        == config["unit_conventions"][0]
    )
    assert (
        o.reads.get_projection_mapping(f.VersionRefV1("mmt-pilot-bid", 1))
        == config["raw_projection_mappings"][0]
    )
    variants = [
        o.materialise(request(f, version=2)),
        o.materialise(request(f, knowledge_cutoff_utc=ASOF + timedelta(microseconds=1))),
        o.materialise(request(f, as_of_utc=ASOF - timedelta(microseconds=1))),
    ]
    assert all(
        item is not None and item.derived_occurrence_id != result.derived_occurrence_id
        for item in variants
    )
    assert len({item.derived_occurrence_id for item in variants}) == 3
    raw.commands.admit_raw_observation_occurrence(
        observation(
            "bid", identity="changed", sequence=3, event=ASOF, receipt=ASOF, value=Decimal("104")
        )
    )
    changed = o.materialise(req)
    assert (
        changed.result == Decimal("103")
        and changed.derived_occurrence_id != result.derived_occurrence_id
    )
    assert o.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    all_values = [result, *variants, changed]
    history = o.reads.list_derived_history(
        derived_signal_id="D011",
        subject_instrument="NVDA",
        effective_at_or_before_utc=ASOF,
        knowledge_at_or_before_utc=clock[0],
        limit=100,
    )
    assert history == tuple(
        sorted(
            all_values,
            key=lambda x: (x.effective_as_of_utc, x.knowledge_cutoff_utc, x.derived_occurrence_id),
            reverse=True,
        )
    )
    assert o.reads.get_derived_occurrence("unknown") is None
    assert o.reads.get_parameter_set(f.VersionRefV1("absent", 1)) is None
    assert (
        o.reads.get_calculation_definition(
            derived_signal_id="D006", calculation_definition_version="unknown"
        )
        is None
    )
    assert (
        o.reads.list_derived_history(
            derived_signal_id="D006",
            subject_instrument="NVDA",
            effective_at_or_before_utc=ASOF,
            knowledge_at_or_before_utc=ASOF,
            limit=1,
        )
        == ()
    )
    for bad in (0, 1001, -1):
        with pytest.raises(ValueError):
            o.reads.list_derived_history(
                derived_signal_id="D011",
                subject_instrument="NVDA",
                effective_at_or_before_utc=ASOF,
                knowledge_at_or_before_utc=ASOF,
                limit=bad,
            )
    with pytest.raises(TypeError):
        o.reads.list_derived_history(
            derived_signal_id="D011",
            subject_instrument="NVDA",
            effective_at_or_before_utc=ASOF,
            knowledge_at_or_before_utc=ASOF,
            limit=True,
        )


@pytest.mark.parametrize(
    "bid,ask,expected",
    [
        ("0", "0", "0"),
        ("-4", "-2", "-3"),
        ("104", "100", "102"),
        ("100", "100", "100"),
        (
            "100.123456789012345678901234567890",
            "102.000000000000000000000000000000",
            "101.061728394506172839450617283945",
        ),
        ("-0.000", "0.000", "0.000"),
    ],
)
def test_exact_equation_independent_of_ambient_context(bid, ask, expected):
    raw = raw_api.create_owner()
    for side, value in (("bid", bid), ("ask", ask)):
        raw.commands.admit_raw_observation_occurrence(observation(side, value=Decimal(value)))
    f = foundation()
    o = f.create_owner(**configuration(f, raw.reads))
    with localcontext() as ambient:
        ambient.prec = 2
        result = o.materialise(request(f))
    assert result.result == Decimal(expected)
    assert result.raw_input_lineage[0].canonical_value.as_tuple() == Decimal(bid).as_tuple()
    assert result.raw_input_lineage[1].canonical_value.as_tuple() == Decimal(ask).as_tuple()
    assert o.materialise(request(f)).derived_occurrence_id == result.derived_occurrence_id


def test_registration_shape_and_immutable_conflicts():
    f = foundation()
    raw = raw_api.create_owner()
    config = configuration(f, raw.reads)
    definition = config["definitions"][0]
    o = f.create_owner(**(config | {"definitions": (definition, definition)}))
    assert (
        o.reads.get_calculation_definition(
            derived_signal_id="D011", calculation_definition_version="D011-MIDPOINT-1"
        )
        == definition
    )
    with pytest.raises(ValueError):
        f.create_owner(
            **(config | {"definitions": (definition, replace(definition, equation="different"))})
        )
