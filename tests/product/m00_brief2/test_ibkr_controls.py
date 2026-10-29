"""N08/N09/N15: independently discover persisted controls without known IDs."""

import copy
import hashlib
import json
from dataclasses import replace
from datetime import UTC, datetime

import pytest

from m00_fixture_io import (
    ART,
    control_observation,
    discovery_rows,
    dump_observation,
    expected,
    fresh_discovery,
    fresh_rows,
    inputs,
    jsonl,
    mapping_group,
    observation,
    owner,
    queries,
    utc,
)
from nvda_desk.architecture.schema import validate_instance
from nvda_desk.raw_signal_occurrence_truth import api as r


def _exact(value):
    # Plain control callback integers/bools must not collapse under Python ==.
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _order(value):
    return (
        value["received_ts_utc"],
        value["ingestion_sequence_scope"],
        value["ingestion_sequence"],
        value["observation_occurrence_id"],
    )


def test_control_discoverability(tmp_path):
    depth = [item for item in inputs() if item["scenario_id"] == "A4"]
    specs = jsonl(ART / "fixtures/controls/control_input_v1.jsonl")
    control_oracle = [
        item["value"]
        for item in jsonl(ART / "fixtures/controls/expected_control_output_v1.jsonl")
    ]
    controls = [control_observation(spec) for spec in specs]
    path = tmp_path / "controls.db"
    raw = owner(path, create=True)
    for item in depth:
        raw.commands.admit_raw_observation_occurrence(observation(item))
    for value in controls:
        raw.commands.admit_raw_observation_occurrence(value)
    # N15 first proves known-ID reads work; discovery below receives no IDs.
    for value in controls:
        assert dump_observation(
            raw.reads.get_raw_observation_occurrence(value.observation_occurrence_id)
        ) == dump_observation(value)
        assert raw.reads.project_raw_value(
            r.RawSignalCatalogueId("R187"),
            value.observation_occurrence_id,
            mappings=(mapping_group("A4-STK")["R187"],),
        ) is None

    # Six separately retained counterfacts exercise exact public identity filters.
    counterfacts = []
    for index, dimension in enumerate(
        ("subject", "source_provider", "source_variant", "request", "generation", "exchange")
    ):
        native = copy.deepcopy(dict(controls[0].native_record))
        changes = {}
        if dimension == "subject":
            changes["subject_instrument"] = native["_collector"]["subject"] = "OTHER-SUBJECT"
        elif dimension == "source_provider":
            changes["source_provider"] = r.provider_id("OTHER-SOURCE")
        elif dimension == "source_variant":
            changes["source_variant"] = "OTHER-VARIANT"
        elif dimension == "request":
            native["_collector"]["request"] = "OTHER-REQUEST"
            native["_collector"]["control"]["request"] = "OTHER-REQUEST"
        elif dimension == "generation":
            native["_collector"]["generation"] = "OTHER-GENERATION"
            native["_collector"]["control"].update(
                generation_before="OTHER-GENERATION", generation_after="OTHER-GENERATION"
            )
        else:
            native["_collector"]["requested_exchange"] = "OTHER-EXCHANGE"
        value = replace(
            controls[0],
            **changes,
            native_record=native,
            observation_occurrence_id=r.observation_occurrence_id(f"M00B2-L04-{dimension}"),
            ingestion_sequence=1000 + index,
        )
        raw.commands.admit_raw_observation_occurrence(value)
        counterfacts.append(value)

    query = {
        "subject_instrument": "NVDA-STK-CONTROL-1",
        "source_provider": "foundation-controlled-ibkr-m00-v1",
        "source_variant": "ibkr-smart-depth/native-v1",
        "received_at_or_before_utc": "2026-10-20T12:40:01Z",
        "native_identity_selectors": [
            [["_collector", "request"], "STK-SMART-R1"],
            [["_collector", "requested_exchange"], "SMART"],
            [["_collector", "generation"], "STK-SMART-G1"],
        ],
    }
    depth_oracle = [
        item["value"]
        for item in expected()
        if item["scenario_id"] == "A4" and item["kind"] == "observation"
    ]
    wanted_observations = sorted(
        [*depth_oracle, *(dump_observation(value) for value in controls)], key=_order
    )
    # This is the first required discovery call; baseline must fail if seam absent.
    actual = discovery_rows(raw, query)
    assert _exact(actual["observations"]) == _exact(wanted_observations)
    assert _exact(actual["controls"]) == _exact(control_oracle)
    assert len({item["observation_occurrence_id"] for item in actual["observations"]}) == 9
    assert [item["control"]["kind"] for item in actual["controls"]] == [
        "error317", "error316", "reconnect", "gap", "restart"
    ]
    schema = json.loads((ART / "output_schema_v1.json").read_text())
    for item in actual["controls"]:
        validate_instance({
            "kind": "control", "fixture_id": "M00B2-CONTROLS-V1", "fixture_version": 1,
            "family": "CONTROLS", "scenario_id": "CONTROL", "mapping_group": "CONTROL",
            "value": item,
        }, schema)
    checks = [(query, actual)]
    for cutoff, count in (
        ("2026-10-20T12:39:59.400000Z", 0),
        ("2026-10-20T12:39:59.500000Z", 1),
        ("2026-10-20T12:39:59.800000Z", 4),
        ("2026-10-20T12:39:59.900000Z", 5),
    ):
        selected = {**query, "received_at_or_before_utc": cutoff}
        result = discovery_rows(raw, selected)
        assert _exact(result["controls"]) == _exact(control_oracle[:count])
        assert _exact(result["observations"]) == _exact([
            item for item in wanted_observations if utc(item["received_ts_utc"]) <= utc(cutoff)
        ])
        checks.append((selected, result))

    # G2 consumer knows subject/request/new generation, never restart ID. Union
    # ordinary generation selection and explicit after-link query, with ID dedupe.
    g2 = copy.deepcopy(query)
    g2["native_identity_selectors"][-1][1] = "STK-SMART-G2"
    linked = copy.deepcopy(g2)
    linked["native_identity_selectors"][-1][0] = ["_collector", "control", "generation_after"]
    g2_result = discovery_rows(raw, g2)
    boundary = discovery_rows(raw, linked)
    assert g2_result == {"observations": [], "controls": []}
    assert _exact(boundary["controls"]) == _exact(control_oracle[-1:])
    assert _exact(boundary["observations"]) == _exact([dump_observation(controls[-1])])
    union = {item["control_id"]: item for result in (g2_result, boundary)
             for item in result["controls"]}
    assert _exact(list(union.values())) == _exact(control_oracle[-1:])
    before_restart = {**linked, "received_at_or_before_utc": "2026-10-20T12:39:59.800000Z"}
    assert discovery_rows(raw, before_restart) == {"observations": [], "controls": []}
    checks.extend([(g2, g2_result), (linked, boundary),
                   (before_restart, {"observations": [], "controls": []})])

    # Exact proposed domain, without weakening current projected-history behaviour.
    kwargs = dict(query)
    kwargs["received_at_or_before_utc"] = utc(kwargs["received_at_or_before_utc"])
    kwargs["native_identity_selectors"] = tuple(
        (tuple(parts), value) for parts, value in kwargs["native_identity_selectors"]
    )
    with pytest.raises(ValueError):
        raw.reads.list_raw_observation_history(**kwargs, limit=0, cursor=None)
    with pytest.raises(ValueError):
        raw.reads.list_raw_observation_history(**kwargs, limit=1, cursor="invalid")
    with pytest.raises(ValueError):
        raw.reads.list_raw_observation_history(
            **{**kwargs, "received_at_or_before_utc": datetime.max.replace(tzinfo=UTC)},
            limit=1, cursor=None,
        )
    del raw
    before = hashlib.sha256(path.read_bytes()).digest()
    for selected, wanted in checks:
        assert _exact(fresh_discovery(path, selected)) == _exact(wanted)
    counter_queries = [
        {**queries(depth[:1])[0], "id": value.observation_occurrence_id.value}
        for value in counterfacts
    ]
    retained = {
        item["value"]["observation_occurrence_id"]: item["value"]
        for item in fresh_rows(path, counter_queries) if item["kind"] == "observation"
    }
    assert _exact(retained) == _exact({
        value.observation_occurrence_id.value: dump_observation(value) for value in counterfacts
    })
    assert hashlib.sha256(path.read_bytes()).digest() == before
