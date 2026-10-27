"""Actual isolated negative replays; no expected output row constructs actual facts."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from typing import Any

from m00_fixture_io import (
    ART,
    ROOT,
    control_observation,
    decode,
    dump_observation,
    encode,
    fresh_discovery,
    fresh_history,
    fresh_rows,
    inputs,
    jsonl,
    observation,
    owner,
    queries,
    utc,
)
from nvda_desk.architecture.schema import validate_instance
from nvda_desk.raw_signal_occurrence_truth import api as r


class NegativeReplayFailure(ValueError):
    """Structured observed requirement failure, retained by the export manifest."""

    def __init__(self, detail: str) -> None:
        self.details = {"check_detail": detail, "expected": True, "actual": False}
        super().__init__("negative replay invariant: " + detail)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise NegativeReplayFailure(detail)


def exact(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def query(item: dict[str, Any], role: str = "R190") -> dict[str, Any]:
    obs = item["observation"]
    identity = decode(obs["native_record"])["_collector"]
    return dict(
        group=item["mapping_group"],
        raw_id=role,
        subject=obs["subject_instrument"],
        cutoff="2026-10-26T14:00:10Z" if item["family"] == "B" else "2026-10-20T12:40:01Z",
        selection={
            key: identity[key]
            for key in ("subject", "request", "generation", "requested_exchange", "scenario_id")
        },
    )


def retained(path: Path, values: list[Any], template: dict[str, Any]) -> list[dict[str, Any]]:
    requests = []
    for value in values:
        matched = next(
            (
                item
                for item in inputs()
                if item["observation"]["observation_occurrence_id"]
                == value.observation_occurrence_id.value
            ),
            template,
        )
        requests.append({**queries([matched])[0], "id": value.observation_occurrence_id.value})
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    rows = fresh_rows(path, requests)
    schema = json.loads((ART / "output_schema_v1.json").read_text())
    for row in rows:
        validate_instance(row, schema)
    actual = {
        row["value"]["observation_occurrence_id"]: row["value"]
        for row in rows
        if row["kind"] == "observation"
    }
    wanted = {value.observation_occurrence_id.value: dump_observation(value) for value in values}
    require(exact(actual) == exact(wanted), "complete typed fresh retained observations")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == before, "fresh reads changed SQLite")
    return rows


def special_read(path: Path, ids: list[str], mapping: dict[str, Any] | None = None) -> Any:
    code = """
import json,sys
from pathlib import Path
from m00_fixture_io import owner,dump_observation,dump_projection
from nvda_desk.raw_signal_occurrence_truth import api as r
p=json.loads(sys.argv[2]); raw=owner(Path(sys.argv[1])); out=[]
for identifier in p['ids']:
 value=raw.reads.get_raw_observation_occurrence(r.observation_occurrence_id(identifier))
 item={'observation':dump_observation(value) if value is not None else None}
 if p['mapping'] is not None:
  m=dict(p['mapping']);m['raw_signal_catalogue_id']=r.RawSignalCatalogueId(m['raw_signal_catalogue_id']);m['native_field_path']=tuple(m['native_field_path'])
  result=raw.reads.project_raw_value(m['raw_signal_catalogue_id'],r.observation_occurrence_id(identifier),mappings=(r.RawSignalProjectionMappingV1(**m),))
  item['projection']=dump_projection(result) if result is not None else None
 out.append(item)
print(json.dumps(out,sort_keys=True))
"""
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    result = subprocess.run(
        [sys.executable, "-c", code, str(path), json.dumps({"ids": ids, "mapping": mapping})],
        env=dict(os.environ, PYTHONPATH=os.pathsep.join((str(ROOT / "tools"), str(ROOT / "src")))),
        text=True,
        capture_output=True,
        check=True,
    )
    require(hashlib.sha256(path.read_bytes()).hexdigest() == before, "special read changed SQLite")
    return json.loads(result.stdout)


def replay_negatives(fixtures: Path, workspace: Path) -> list[dict[str, Any]]:
    workspace.mkdir()
    all_inputs = [
        row for family in "ABC" for row in jsonl(fixtures / family / "synthetic_input_v1.jsonl")
    ]
    outcomes = []
    for number in range(1, 19):
        case = f"N{number:02}"
        spec = jsonl(fixtures / "negative" / f"{case}_v1.jsonl")[0]
        scenarios = spec.get("base_scenarios", [spec.get("base_scenario")])
        data = copy.deepcopy([row for row in all_inputs if row["scenario_id"] in scenarios])
        first: Any = observation(data[0])
        path = workspace / f"{case}.db"
        raw = owner(path, create=True)
        result: dict[str, Any] = {"case_id": case, "schema_version": "m00-negative-export/1"}
        values: list[Any] = []
        if case == "N03":
            try:
                replace(first, **spec["replace_envelope"])
            except ValueError as exc:
                require("receipt_only" in str(exc), "temporal rejection reason")
                result["rejection"] = {"type": type(exc).__name__, "message": str(exc)}
            else:
                raise NegativeReplayFailure("N03 invalid temporal discriminant accepted")
            del raw
            result["fresh_absence"] = special_read(path, [first.observation_occurrence_id.value])
            require(result["fresh_absence"] == [{"observation": None}], "rejected fact persisted")
        elif case in ("N08", "N09", "N15"):
            values = [observation(row) for row in data]
            controls = [
                control_observation(row)
                for row in jsonl(fixtures / "controls/control_input_v1.jsonl")
            ]
            for value in [*values, *controls]:
                raw.commands.admit_raw_observation_occurrence(value)
            del raw
            q: dict[str, Any] = dict(
                subject_instrument=first.subject_instrument,
                source_provider=first.source_provider.value,
                source_variant=first.source_variant,
                received_at_or_before_utc="2026-10-20T12:40:01Z",
                native_identity_selectors=[
                    [["_collector", "request"], "STK-SMART-R1"],
                    [["_collector", "generation"], "STK-SMART-G1"],
                ],
            )
            result["discovery"] = fresh_discovery(path, q)
            result["retained"] = retained(path, controls, data[0])
            actual = result["discovery"]["controls"]
            require(
                [v["control"]["kind"] for v in actual]
                == ["error317", "error316", "reconnect", "gap", "restart"],
                "control discovery",
            )
            require(all(v["control"]["invalidates"] is True for v in actual), "invalidity facts")
            require(actual[-1]["control"]["generation_after"] == "STK-SMART-G2", "restart link")
            require(
                not any(row["kind"] == "projection" for row in result["retained"]),
                "invented control R projection",
            )
        elif case == "N06":
            del raw
            result["omissions"] = []
            for i, (field, role) in enumerate(
                zip(spec["remove_native_fields"], spec["expected_missing_roles"], strict=True)
            ):
                subpath = workspace / f"N06-{i}.db"
                current = owner(subpath, create=True)
                native = dict(first.native_record)
                del native[field]
                value = replace(first, native_record=native)
                current.commands.admit_raw_observation_occurrence(value)
                del current
                rows = retained(subpath, [value], data[0])
                require(
                    not any(
                        row["kind"] == "projection"
                        and row["value"]["raw_signal_catalogue_id"] == role
                        for row in rows
                    ),
                    "missing role manufactured",
                )
                result["omissions"].append(dict(field=field, absent_role=role, actual=rows))
        else:
            if case == "N07":
                for i, event in enumerate(spec["mutation_events"]):
                    native = dict(first.native_record)
                    native.update(
                        operation=event["operation"],
                        position=event["position"],
                        size=Decimal(event["size"]),
                    )
                    values.append(
                        replace(
                            first,
                            native_record=native,
                            observation_occurrence_id=r.observation_occurrence_id(
                                f"export-N07-{i}"
                            ),
                            ingestion_sequence=1000 + i,
                        )
                    )
            elif case in ("N11", "N12"):
                for i, row in enumerate(data):
                    if case == "N11" and i == spec["event_index"]:
                        row["observation"].update(spec["replace_envelope"])
                        row["observation"]["native_record"]["_collector"].update(
                            {key: encode(value) for key, value in spec["replace_collector"].items()}
                        )
                    if case == "N12":
                        row["observation"].update(spec["replace_envelope"])
                    values.append(observation(row))
            elif case == "N05":
                values = [
                    first,
                    replace(
                        first, observation_occurrence_id=r.observation_occurrence_id(spec["new_id"])
                    ),
                ]
            elif case == "N13":
                values = [observation(row) for row in data]
                values.append(
                    replace(
                        first,
                        observation_occurrence_id=r.observation_occurrence_id(spec["new_id"]),
                        received_ts_utc=utc(spec["replace_envelope"]["received_ts_utc"]),
                        ingestion_sequence=1000,
                    )
                )
            elif case == "N14":
                native = dict(first.native_record)
                del native["position"]
                values = [replace(first, native_record=native)]
            elif case == "N18":
                first = replace(
                    first,
                    raw_signal_catalogue_ids=(
                        *first.raw_signal_catalogue_ids,
                        r.RawSignalCatalogueId("R001"),
                    ),
                )
                native = dict(first.native_record)
                native["time"] = {"receipt": utc(spec["valid_collector_receipt"]["value"])}
                values = [
                    first,
                    replace(
                        first,
                        native_record=native,
                        observation_occurrence_id=r.observation_occurrence_id("export-N18-valid"),
                        ingestion_sequence=1000,
                    ),
                ]
            elif case in ("N04", "N10", "N01"):
                values = [observation(row) for row in data]
            else:
                values = [first]
            for value in values:
                raw.commands.admit_raw_observation_occurrence(value)
            if case == "N10":
                for i, dimension in enumerate(spec["selector_dimensions"]):
                    native = copy.deepcopy(dict(first.native_record))
                    changes: dict[str, Any] = {}
                    if dimension == "source_provider":
                        changes[dimension] = r.provider_id("OTHER-SOURCE")
                    elif dimension == "source_variant":
                        changes[dimension] = "OTHER-VARIANT"
                    else:
                        replacement = spec["perturbations"].get(dimension, "OTHER-EXCHANGE")
                        native["_collector"][dimension] = replacement
                        if dimension == "subject":
                            changes["subject_instrument"] = replacement
                    value = replace(
                        first,
                        **changes,
                        native_record=native,
                        observation_occurrence_id=r.observation_occurrence_id(
                            "export-N10-" + dimension
                        ),
                        ingestion_sequence=1000 + i,
                    )
                    raw.commands.admit_raw_observation_occurrence(value)
                    values.append(value)
            if case == "N16":
                retry = raw.commands.admit_raw_observation_occurrence(first)
                require(exact(dump_observation(retry)) == exact(dump_observation(first)), "retry")
                native = dict(first.native_record)
                native.update(decode(spec["conflicting_native"]))
                try:
                    raw.commands.admit_raw_observation_occurrence(
                        replace(first, native_record=native)
                    )
                except ValueError as exc:
                    require("different content" in str(exc), "conflict reason")
                    result["rejection"] = {"type": type(exc).__name__, "message": str(exc)}
                else:
                    raise NegativeReplayFailure("N16 conflicting replay accepted")
            del raw
            result["retained"] = retained(path, values, data[0])
            observations = [v["value"] for v in result["retained"] if v["kind"] == "observation"]
            if case == "N01":
                require(
                    [v.native_record["side"] for v in values] == spec["expected_native_sides"],
                    "native sides",
                )
            if case in ("N02", "N04", "N05", "N10", "N13"):
                result["histories"] = []
                for row in {v["mapping_group"]: v for v in data}.values():
                    role = "R197" if row["scenario_id"] in ("C2", "C3") else "R190"
                    q = query(row, role)
                    hist = fresh_history(path, q)
                    expected_ids = {
                        v.observation_occurrence_id.value
                        for v in values
                        if v.subject_instrument == q["subject"]
                        and v.source_provider.value == row["observation"]["source_provider"]
                        and v.source_variant == row["observation"]["source_variant"]
                        and v.received_ts_utc <= utc(q["cutoff"])
                        and all(
                            v.native_record["_collector"].get(k) == val
                            for k, val in q["selection"].items()
                        )
                    }
                    require(
                        {v["observation_occurrence_id"] for v in hist} == expected_ids,
                        "selected history population",
                    )
                    result["histories"].append(hist)
                    if case == "N04":
                        excluded = fresh_history(path, {**q, "event_cutoff": q["cutoff"]})
                        require(excluded == [], "receipt-only event cutoff")
                        result.setdefault("event_cutoff_absences", []).append(excluded)
            if case == "N05":
                clocks = {
                    (v["received_ts_utc"], v["ingestion_sequence_scope"], v["ingestion_sequence"])
                    for v in observations
                }
                require(len(clocks) == 1 and len(observations) == 2, "distinct tied facts")
                result["causal_order"] = "UNKNOWN_TIED_RECEIPT_SCOPE_SEQUENCE"
            if case == "N11":
                require(
                    len(observations) == 4
                    and len({v["subject_instrument"] for v in observations}) == 2,
                    "asynchronous foreign contract",
                )
            if case == "N12":
                require(
                    len(observations) == 4
                    and len({v["received_ts_utc"] for v in observations}) == 1,
                    "distinct callbacks share batch receipt",
                )
            if case == "N14":
                require(
                    not any(
                        v["kind"] == "projection"
                        and v["value"]["raw_signal_catalogue_id"] == "R185"
                        for v in result["retained"]
                    ),
                    "position absence",
                )
                result["standing_book_completeness"] = "NOT_ASSERTED"
            if case == "N17":
                require(
                    encode(values[0].native_record["marketMaker"]) == encode(spec["expected_mpid"])
                    and values[0].native_record["_collector"]["requested_exchange"]
                    == spec["expected_requested_exchange"],
                    "MPID versus requested exchange",
                )
            if case == "N18":
                mapping = dict(
                    mapping_id="export-collector-receipt/1",
                    version=1,
                    raw_signal_catalogue_id="R001",
                    source_provider=first.source_provider.value,
                    source_variant=first.source_variant,
                    native_field_path=["time", "receipt"],
                    native_units="UTC-datetime",
                )
                readback = special_read(
                    path, [v.observation_occurrence_id.value for v in values], mapping
                )
                require(readback[0]["projection"] is None, "missing receipt carrier")
                projected = readback[1]["projection"]
                require(
                    projected["native_value"] == encode(values[1].received_ts_utc)
                    and projected["source_timestamp_raw"] is None,
                    "typed collector receipt",
                )
                result["receipt_carrier"] = readback
        result["verified"] = True
        outcomes.append(result)
    return outcomes
