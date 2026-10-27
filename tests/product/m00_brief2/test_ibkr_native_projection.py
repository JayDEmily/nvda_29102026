"""Literal independent oracle versus actual native M00/SQLite public behaviour."""

import copy
import hashlib
import json
from dataclasses import replace
from decimal import Decimal

import pytest

from m00_fixture_io import (
    ART,
    canonical,
    dump_observation,
    encode,
    expected,
    fresh_rows,
    inputs,
    mapping_group,
    observation,
    owner,
    queries,
    read_rows,
    utc,
)
from nvda_desk.architecture.schema import validate_instance
from nvda_desk.raw_signal_occurrence_truth import api as r


@pytest.mark.parametrize("scenario", ["A1", "A2", "A3", "A4", "A5", "A6", "B", "C1", "C2", "C3"])
def test_native_scenarios(tmp_path, scenario):
    data = [item for item in inputs() if item["scenario_id"] == scenario]
    oracle = [item for item in expected() if item["scenario_id"] == scenario]
    path = tmp_path / "native.db"
    raw = owner(path, create=True)
    for item in data:
        value = observation(item)
        assert raw.commands.admit_raw_observation_occurrence(value) is value
    actual = read_rows(raw, queries(data))
    assert actual == canonical(oracle)
    schema = json.loads((ART / "output_schema_v1.json").read_text())
    for item in actual:
        validate_instance(item, schema)
    del raw
    before = hashlib.sha256(path.read_bytes()).digest()
    assert fresh_rows(path, queries(data)) == canonical(oracle)
    assert hashlib.sha256(path.read_bytes()).digest() == before


@pytest.mark.parametrize(
    "case", ["N01", "N02", "N03", "N06", "N07", "N11", "N12", "N14", "N17", "N18"]
)
def test_native_negative(tmp_path, case):
    spec = json.loads((ART / f"fixtures/negative/{case}_v1.jsonl").read_text())
    data = copy.deepcopy([x for x in inputs() if x["scenario_id"] == spec["base_scenario"]])
    path = tmp_path / "negative.db"
    raw = owner(path, create=True)
    first = observation(data[0])
    maps = mapping_group(data[0]["mapping_group"])
    if case == "N03":
        with pytest.raises(ValueError, match="receipt_only"):
            replace(first, **spec["replace_envelope"])
        assert raw.reads.get_raw_observation_occurrence(first.observation_occurrence_id) is None
    elif case == "N06":
        for i, (field, missing) in enumerate(
            zip(spec["remove_native_fields"], spec["expected_missing_roles"], strict=True)
        ):
            current = owner(tmp_path / f"missing-{i}.db", create=True)
            native = dict(first.native_record)
            del native[field]
            value = replace(first, native_record=native)
            current.commands.admit_raw_observation_occurrence(value)
            stored = current.reads.get_raw_observation_occurrence(value.observation_occurrence_id)
            assert dump_observation(stored)["native_record"] == encode(native)
            assert field not in stored.native_record
            assert (
                current.reads.project_raw_value(
                    r.RawSignalCatalogueId(missing),
                    value.observation_occurrence_id,
                    mappings=(maps[missing],),
                )
                is None
            )
            # Other original fields remain raw facts, even when required MPID identity
            # absence also makes their fully-qualified mapping unavailable.
            for key, item in first.native_record.items():
                if key != field:
                    assert encode(stored.native_record[key]) == encode(item)
            del current
            persisted = fresh_rows(tmp_path / f"missing-{i}.db", queries(data[:1]))
            assert next(
                x["value"] for x in persisted if x["kind"] == "observation"
            ) == dump_observation(value)
    elif case == "N07":
        for i, event in enumerate(spec["mutation_events"]):
            native = dict(first.native_record)
            native.update(
                operation=event["operation"],
                position=event["position"],
                size=Decimal(event["size"]),
            )
            value = replace(
                first,
                native_record=native,
                observation_occurrence_id=r.observation_occurrence_id(f"n07-{i}"),
                ingestion_sequence=1000 + i,
            )
            raw.commands.admit_raw_observation_occurrence(value)
            stored = raw.reads.get_raw_observation_occurrence(value.observation_occurrence_id)
            assert dump_observation(stored)["native_record"] == encode(native)
            persisted = fresh_rows(path, [{**queries(data[:1])[0], "id": f"n07-{i}"}])
            assert next(
                x["value"] for x in persisted if x["kind"] == "observation"
            ) == dump_observation(value)
    elif case in ("N11", "N12"):
        for index, item in enumerate(data):
            if case == "N11" and index == spec["event_index"]:
                item["observation"].update(spec["replace_envelope"])
                item["observation"]["native_record"]["_collector"].update(
                    {key: encode(value) for key, value in spec["replace_collector"].items()}
                )
            elif case == "N12":
                item["observation"].update(spec["replace_envelope"])
            raw.commands.admit_raw_observation_occurrence(observation(item))
        stored = [
            raw.reads.get_raw_observation_occurrence(
                r.observation_occurrence_id(x["observation"]["observation_occurrence_id"])
            )
            for x in data
        ]
        assert len({x.observation_occurrence_id for x in stored}) == 4
        assert all(x.source_timestamp_raw is None for x in stored)
        if case == "N11":
            assert stored[-1].subject_instrument == "NVDA-OPT-P100-CONTROL-1"
            assert all(x.subject_instrument == "NVDA-OPT-C100-CONTROL-1" for x in stored[:-1])
        else:
            assert len({x.received_ts_utc for x in stored}) == 1
    elif case == "N18":
        receipt_map = r.RawSignalProjectionMappingV1(
            "m00b2-r001-collector-receipt",
            1,
            r.RawSignalCatalogueId("R001"),
            first.source_provider.value,
            first.source_variant,
            ("time", "receipt"),
            "UTC-datetime",
        )
        first = replace(
            first,
            raw_signal_catalogue_ids=(
                *first.raw_signal_catalogue_ids,
                r.RawSignalCatalogueId("R001"),
            ),
        )
        raw.commands.admit_raw_observation_occurrence(first)
        assert (
            raw.reads.project_raw_value(
                r.RawSignalCatalogueId("R001"),
                first.observation_occurrence_id,
                mappings=(receipt_map,),
            )
            is None
        )
        native = dict(first.native_record)
        native["time"] = {"receipt": utc(spec["valid_collector_receipt"]["value"])}
        valid = replace(
            first,
            native_record=native,
            observation_occurrence_id=r.observation_occurrence_id("n18-valid"),
            ingestion_sequence=1000,
        )
        raw.commands.admit_raw_observation_occurrence(valid)
        reopened = owner(path)
        value = reopened.reads.project_raw_value(
            r.RawSignalCatalogueId("R001"), valid.observation_occurrence_id, mappings=(receipt_map,)
        )
        assert type(value.native_value) is type(first.received_ts_utc)
        assert value.native_value == value.received_ts_utc == valid.received_ts_utc
        assert value.source_timestamp_raw is None
        persisted = fresh_rows(path, [{**queries(data[:1])[0], "id": "n18-valid"}])
        assert next(
            x["value"] for x in persisted if x["kind"] == "observation"
        ) == dump_observation(valid)
    else:
        if case == "N14":
            native = dict(first.native_record)
            del native["position"]
            first = replace(first, native_record=native)
        raw.commands.admit_raw_observation_occurrence(first)
        stored = raw.reads.get_raw_observation_occurrence(first.observation_occurrence_id)
        assert dump_observation(stored) == dump_observation(first)
        assert stored.source_timestamp_raw is None
        if case == "N01":
            assert stored.native_record["side"] == 1
            ask = observation(data[2])
            raw.commands.admit_raw_observation_occurrence(ask)
            assert (
                raw.reads.project_raw_value(
                    r.RawSignalCatalogueId("R188"),
                    ask.observation_occurrence_id,
                    mappings=(maps["R188"],),
                ).native_value
                == 0
            )
        elif case == "N02":
            assert (
                raw.reads.list_projected_raw_history(
                    r.RawSignalCatalogueId("R190"),
                    mappings=(maps["R190"],),
                    subject_instrument=first.subject_instrument,
                    received_at_or_before_utc=first.received_ts_utc,
                    event_at_or_before_utc=None,
                    limit=1,
                    cursor=None,
                )
                .items[0]
                .source_temporal_kind
                == "receipt_only"
            )
        elif case == "N17":
            assert stored.native_record["marketMaker"] == spec["expected_mpid"]
            assert (
                stored.native_record["_collector"]["requested_exchange"]
                == spec["expected_requested_exchange"]
            )
            assert stored.native_record["isSmartDepth"] is False
        else:
            assert "position" not in stored.native_record
            assert "complete" not in stored.native_record
