"""Exact independent histories through public SQLite pages and fresh owners."""

import copy
import hashlib
import json
from dataclasses import replace

import pytest

from m00_fixture_io import (
    ART,
    decode,
    dump_observation,
    expected,
    fresh_history,
    fresh_rows,
    history_rows,
    inputs,
    observation,
    owner,
    queries,
    utc,
)
from nvda_desk.raw_signal_occurrence_truth import api as r


def _query(item, raw_id):
    data = item["observation"]
    identity = decode(data["native_record"])["_collector"]
    return {
        "group": item["mapping_group"],
        "raw_id": raw_id,
        "subject": data["subject_instrument"],
        "cutoff": (
            "2026-10-26T14:00:10Z" if item["family"] == "B" else "2026-10-20T12:40:01Z"
        ),
        "selection": {
            key: identity[key]
            for key in ("subject", "request", "generation", "requested_exchange", "scenario_id")
        },
    }


def _order(value):
    return (
        value["received_ts_utc"],
        value["ingestion_sequence_scope"],
        value["ingestion_sequence"],
        value["observation_occurrence_id"],
    )


def _oracle(query):
    return sorted(
        (
            item["value"]
            for item in expected()
            if item["kind"] == "projection"
            and item["mapping_group"] == query["group"]
            and item["value"]["raw_signal_catalogue_id"] == query["raw_id"]
            and item["value"]["subject_instrument"] == query["subject"]
            and all(
                item["value"]["selection_identity"][key] == value
                for key, value in query["selection"].items()
            )
        ),
        key=_order,
    )


def _fresh_observations(path, data):
    return {
        item["value"]["observation_occurrence_id"]: item["value"]
        for item in fresh_rows(path, queries(data))
        if item["kind"] == "observation"
    }


@pytest.mark.parametrize("scenario", ["A1", "A2", "A3", "A4", "A5", "A6", "B", "C1", "C2", "C3"])
def test_history_scenarios(tmp_path, scenario):
    data = [item for item in inputs() if item["scenario_id"] == scenario]
    path = tmp_path / "history.db"
    raw = owner(path, create=True)
    for item in data:
        raw.commands.admit_raw_observation_occurrence(observation(item))
    # Separate groups include B's independent STK and option subscriptions.
    groups = {item["mapping_group"]: item for item in data}
    checks = []
    for item in groups.values():
        roles = {
            row["value"]["raw_signal_catalogue_id"]
            for row in expected()
            if row["kind"] == "projection" and row["mapping_group"] == item["mapping_group"]
        }
        for role in sorted(roles):
            query = _query(item, role)
            actual = history_rows(raw, **query)
            wanted = _oracle(query)
            assert actual == wanted
            assert len({row["observation_occurrence_id"] for row in actual}) == len(wanted)
            checks.append((query, wanted))
    del raw
    before = hashlib.sha256(path.read_bytes()).digest()
    for query, wanted in checks:
        assert fresh_history(path, query) == wanted
    assert hashlib.sha256(path.read_bytes()).digest() == before


@pytest.mark.parametrize("case", ["N04", "N05", "N10", "N13", "N16"])
def test_history_negative(tmp_path, case):
    spec = json.loads((ART / f"fixtures/negative/{case}_v1.jsonl").read_text())
    scenarios = spec.get("base_scenarios", [spec.get("base_scenario")])
    data = [item for item in inputs() if item["scenario_id"] in scenarios]
    path = tmp_path / "negative-history.db"
    raw = owner(path, create=True)
    first = observation(data[0])
    query = _query(data[0], "R190")
    if case == "N04":
        for item in data:
            raw.commands.admit_raw_observation_occurrence(observation(item))
        checks = []
        for item in {row["mapping_group"]: row for row in data}.values():
            selected = _query(item, "R190")
            wanted = _oracle(selected)
            assert history_rows(raw, **selected) == wanted
            assert wanted and all(row["source_timestamp_raw"] is None for row in wanted)
            excluded = {**selected, "event_cutoff": spec["query"]["event_at_or_before_utc"]}
            assert history_rows(raw, **excluded) == []
            checks.append((selected, wanted, excluded))
        del raw
        for selected, wanted, excluded in checks:
            assert fresh_history(path, selected) == wanted
            assert fresh_history(path, excluded) == []
    elif case == "N05":
        raw.commands.admit_raw_observation_occurrence(first)
        tied = replace(first, observation_occurrence_id=r.observation_occurrence_id(spec["new_id"]))
        raw.commands.admit_raw_observation_occurrence(tied)
        original = next(
            row for row in _oracle(query)
            if row["observation_occurrence_id"] == first.observation_occurrence_id.value
        )
        # The oracle is independent L01 literal output; the sole changed field is ID.
        wanted = sorted(
            [original, {**original, "observation_occurrence_id": spec["new_id"]}], key=_order
        )
        assert history_rows(raw, **query) == wanted
        del raw
        assert fresh_history(path, query) == wanted
        tied_row = copy.deepcopy(data[0])
        tied_row["observation"]["observation_occurrence_id"] = spec["new_id"]
        assert _fresh_observations(path, [data[0], tied_row]) == {
            first.observation_occurrence_id.value: dump_observation(first),
            spec["new_id"]: dump_observation(tied),
        }
        # Display order uses ID tie-break; equal clocks/scope/sequence establish no
        # provider causal order. Both facts survive for export ambiguity metadata.
        assert _order(wanted[0])[:3] == _order(wanted[1])[:3]
    elif case == "N10":
        for item in data:
            raw.commands.admit_raw_observation_occurrence(observation(item))
        counterfacts = []
        counterrows = []
        for index, dimension in enumerate(spec["selector_dimensions"]):
            native = copy.deepcopy(dict(first.native_record))
            changes = {}
            if dimension == "source_provider":
                changes[dimension] = r.provider_id("OTHER-SOURCE")
            elif dimension == "source_variant":
                changes[dimension] = "OTHER-VARIANT"
            else:
                replacement = spec["perturbations"].get(dimension, "OTHER-EXCHANGE")
                native["_collector"][dimension] = replacement
                if dimension == "subject":
                    changes["subject_instrument"] = replacement
            identifier = f"M00B2-N10-{dimension}"
            value = replace(
                first,
                **changes,
                native_record=native,
                observation_occurrence_id=r.observation_occurrence_id(identifier),
                ingestion_sequence=1000 + index,
            )
            raw.commands.admit_raw_observation_occurrence(value)
            counterfacts.append(value)
            extra = copy.deepcopy(data[0])
            extra["observation"]["observation_occurrence_id"] = identifier
            counterrows.append(extra)
        checks = []
        for item in {row["mapping_group"]: row for row in data}.values():
            role = "R197" if item["scenario_id"] in ("C2", "C3") else "R190"
            selected = _query(item, role)
            assert history_rows(raw, **selected) == _oracle(selected)
            checks.append(selected)
        del raw
        for selected in checks:
            assert fresh_history(path, selected) == _oracle(selected)
        assert _fresh_observations(path, counterrows) == {
            value.observation_occurrence_id.value: dump_observation(value) for value in counterfacts
        }
    elif case == "N13":
        for item in data:
            raw.commands.admit_raw_observation_occurrence(observation(item))
        future = replace(
            first,
            observation_occurrence_id=r.observation_occurrence_id(spec["new_id"]),
            received_ts_utc=utc(spec["replace_envelope"]["received_ts_utc"]),
            ingestion_sequence=spec["replace_envelope"]["ingestion_sequence"],
        )
        raw.commands.admit_raw_observation_occurrence(future)
        assert history_rows(raw, **query) == _oracle(query)
        assert dump_observation(
            raw.reads.get_raw_observation_occurrence(future.observation_occurrence_id)
        ) == dump_observation(future)
        del raw
        assert fresh_history(path, query) == _oracle(query)
        future_row = copy.deepcopy(data[0])
        future_row["observation"]["observation_occurrence_id"] = spec["new_id"]
        assert _fresh_observations(path, [future_row]) == {
            spec["new_id"]: dump_observation(future)
        }
    else:
        raw.commands.admit_raw_observation_occurrence(first)
        retried = raw.commands.admit_raw_observation_occurrence(first)
        assert dump_observation(retried) == dump_observation(first)
        native = dict(first.native_record)
        native.update(decode(spec["conflicting_native"]))
        with pytest.raises(ValueError, match="different content"):
            raw.commands.admit_raw_observation_occurrence(replace(first, native_record=native))
        wanted = [
            row for row in _oracle(query)
            if row["observation_occurrence_id"] == first.observation_occurrence_id.value
        ]
        assert history_rows(raw, **query) == wanted
        del raw
        assert _fresh_observations(path, data[:1]) == {
            first.observation_occurrence_id.value: dump_observation(first)
        }
        assert fresh_history(path, query) == wanted
