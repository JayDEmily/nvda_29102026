"""FND-P01-P03: exact controlled public boundary and complete pilot exclusion."""

import re
from dataclasses import fields, replace
from datetime import timedelta
from decimal import Decimal

import pytest
from _support import (
    ASOF,
    BRIEF,
    NOW,
    ROOT,
    configuration,
    foundation,
    mapping,
    observation,
    request,
)

from nvda_desk.raw_signal_occurrence_truth import api as raw_api


def assert_complete(result, f, raw, req, definition):
    assert result is not None and type(result) is f.DerivedSignalOccurrenceV1
    assert result.result == Decimal("101") and type(result.result) is Decimal
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/v1"
    assert result.implementation_brief_sha256 == BRIEF
    assert result.derived_signal_id == "D011"
    assert result.calculation_definition_version == "D011-MIDPOINT-1"
    assert re.fullmatch("mmt1:[0-9a-f]{64}", result.derived_occurrence_id)
    assert re.fullmatch("[0-9a-f]{64}", result.definition_content_sha256)
    assert result.parameter_context_refs == (req.parameter_set_ref, req.input_selection_policy_ref)
    assert result.subject_instrument == "NVDA"
    assert result.effective_as_of_utc == result.knowledge_cutoff_utc == ASOF
    assert result.calculated_at_utc == NOW
    assert result.units == "price" and result.result_shape == "scalar_decimal"
    assert result.universe is result.window is result.supersedes_derived_occurrence_id is None
    assert result.predecessor_occurrence_ids == ()
    assert result.convention_refs == (f.VersionRefV1("mmt-pilot-price", 1),)
    assert len(result.raw_input_lineage) == 2
    for lineage, side, rid, seconds, value in zip(
        result.raw_input_lineage,
        ("bid", "ask"),
        ("R034", "R035"),
        (2, 1),
        ("100", "102"),
        strict=True,
    ):
        assert lineage.raw_signal_id == rid
        assert lineage.observation_occurrence_id == f"mmt-pilot-{side}-001"
        assert lineage.event_time_utc == ASOF - timedelta(seconds=seconds)
        assert lineage.canonical_value.as_tuple() == Decimal(value).as_tuple()
        assert lineage.projection_mapping_ref == f.VersionRefV1("mmt-pilot-" + side, 1)
        assert lineage.unit_convention_ref == f.VersionRefV1("mmt-pilot-price", 1)
        expected = raw.reads.project_raw_value(
            raw_api.RawSignalCatalogueId(rid),
            raw_api.observation_occurrence_id(lineage.observation_occurrence_id),
            mappings=(mapping(side),),
        )
        assert lineage.projection == expected
        assert type(lineage.projection.observation_occurrence_id) is type(
            raw_api.observation_occurrence_id("x")
        )
    assert len(fields(result)) == 21


def test_d011_midpoint_public_exact_lineage():
    raw = raw_api.create_owner()
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    # Establish actual public M00 dependencies before the attributable missing-seam assertion.
    projected = raw.reads.project_raw_value(
        raw_api.RawSignalCatalogueId("R034"),
        raw_api.observation_occurrence_id("mmt-pilot-bid-001"),
        mappings=(mapping("bid"),),
    )
    assert projected.native_value.as_tuple() == Decimal("100").as_tuple()
    f = foundation()
    config = configuration(f, raw.reads)
    o = f.create_owner(**config)
    req = request(f)
    result = o.materialise(req)
    assert_complete(result, f, raw, req, config["definitions"][0])
    assert o.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert (
        o.reads.get_calculation_definition(
            derived_signal_id="D011", calculation_definition_version="D011-MIDPOINT-1"
        )
        == config["definitions"][0]
    )


@pytest.mark.parametrize(
    "change",
    [
        {"subject_instrument": "OTHER"},
        {"source_variant": "other"},
        {"native_units": "shares"},
        {"source_provider": raw_api.provider_id("other")},
        {"ingestion_sequence_scope": raw_api.ingestion_sequence_scope("other")},
        {"source_timezone_native": "EST"},
        {"source_timestamp_raw": "2026-10-16T00:59:58+00:00"},
        {"revision_vintage_native": "vintage"},
        {"value": float("nan")},
        {"value": 100.0},
        {"value": Decimal("Infinity")},
        {"native_record": {"quote": {}}},
        {"event": ASOF + timedelta(microseconds=1)},
        {"receipt": ASOF + timedelta(microseconds=1)},
        {"event": ASOF - timedelta(seconds=60, microseconds=1)},
        {"event": ASOF - timedelta(seconds=11, microseconds=1)},
        {"event": ASOF, "receipt": ASOF - timedelta(seconds=1)},
        {"source_temporal_kind": "date_only", "source_timestamp_raw": "2026-10-16"},
        {"source_temporal_kind": "receipt_only", "source_timestamp_raw": None},
    ],
)
def test_d011_refuses_missing_or_incompatible_projection(change):
    raw = raw_api.create_owner()
    # The mapping supplies projected units; the optional observation header is
    # not the foundation's units carrier. Challenge the returned public field.
    unit_change = change == {"native_units": "shares"}
    raw.commands.admit_raw_observation_occurrence(
        observation("bid", **({} if unit_change else change))
    )
    raw.commands.admit_raw_observation_occurrence(observation("ask"))

    class Reader:
        def list_projected_raw_history(self, rid, **kwargs):
            page = raw.reads.list_projected_raw_history(rid, **kwargs)
            if unit_change and rid.value == "R034":
                return replace(page, items=(replace(page.items[0], native_units="shares"),))
            return page

    f = foundation()
    o = f.create_owner(**configuration(f, Reader()))
    assert o.materialise(request(f)) is None
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


@pytest.mark.parametrize("event_seconds,ask_seconds", [(60, 50), (11, 1)])
def test_exact_inclusive_temporal_boundaries(event_seconds, ask_seconds):
    raw = raw_api.create_owner()
    raw.commands.admit_raw_observation_occurrence(
        observation("bid", event=ASOF - timedelta(seconds=event_seconds))
    )
    raw.commands.admit_raw_observation_occurrence(
        observation("ask", event=ASOF - timedelta(seconds=ask_seconds))
    )
    f = foundation()
    assert f.create_owner(**configuration(f, raw.reads)).materialise(request(f)).result == Decimal(
        "101"
    )


def test_foundation_rejects_downstream_and_unenabled_requests():
    raw = raw_api.create_owner()
    for side in ("bid", "ask"):
        raw.commands.admit_raw_observation_occurrence(observation(side))
    f = foundation()
    config = configuration(f, raw.reads)
    o = f.create_owner(**config)
    text = (
        ROOT
        / "handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md"
    ).read_text()
    foundation_ids = set(re.findall(r"^\| (D\d{3}) \|", text, re.M))
    downstream_ids = set(re.findall(r"D\d{3}", text.split("## Annex C.")[1]))
    assert len(foundation_ids) == 126 and len(downstream_ids) == 83
    assert foundation_ids.isdisjoint(downstream_ids)
    assert foundation_ids | downstream_ids == {f"D{i:03d}" for i in range(1, 210)}
    for identity in sorted((foundation_ids | downstream_ids) - {"D011"}):
        assert o.materialise(request(f, derived_signal_id=identity)) is None
    assert o.materialise(request(f, context_refs=(f.VersionRefV1("strategy", 1),))) is None
    assert (
        o.materialise(
            request(
                f,
                as_of_utc=NOW + timedelta(seconds=1),
                knowledge_cutoff_utc=NOW + timedelta(seconds=1),
            )
        )
        is None
    )
    assert o.materialise(request(f, knowledge_cutoff_utc=ASOF - timedelta(microseconds=1))) is None
    assert o.materialise(request(f, version=2)) is None
    for key in (
        "definitions",
        "parameter_sets",
        "input_selection_policies",
        "unit_conventions",
        "raw_projection_mappings",
    ):
        missing = f.create_owner(**(config | {key: ()}))
        assert missing.materialise(request(f)) is None
    for key, field, bad in (
        ("parameter_sets", "profile", "P_SCORE"),
        ("input_selection_policies", "source_provider", "unadmitted"),
        ("unit_conventions", "scale", Decimal("2")),
        ("definitions", "equation", "R034"),
    ):
        with pytest.raises(ValueError):
            f.create_owner(**(config | {key: (replace(config[key][0], **{field: bad}),)}))
    for extra in ("candidate", "portfolio", "order", "strategy"):
        with pytest.raises(TypeError):
            request(f, **{extra: {}})
    with pytest.raises(TypeError):
        f.VersionRefV1("x", True)
    with pytest.raises(ValueError):
        f.VersionRefV1("", 1)
    with pytest.raises(ValueError):
        request(f, as_of_utc=ASOF.replace(tzinfo=None))
    assert not any(hasattr(o, name) for name in ("place_order", "execute", "publish", "score"))
