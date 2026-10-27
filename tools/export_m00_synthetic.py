"""Deterministic M00 Brief-2 portable public-seam replay and comparison.

No expected row is used to construct a production observation, mapping or output.
The second process receives only a database and explicit public-read selectors.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import traceback
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from m00_fixture_io import (
    ART,
    META,
    canonical,
    control_observation,
    discovery_rows,
    dump_control,
    history_rows,
    jsonl,
    observation,
    owner,
    queries,
)
from nvda_desk.architecture.schema import validate_instance

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("A1", "A2", "A3", "A4", "A5", "A6", "B", "C1", "C2", "C3")
COUNTS = {
    "A1": (1, 4), "A2": (4, 4), "A3": (4, 4), "A4": (4, 20),
    "A5": (3, 15), "A6": (2, 10), "B": (7, 35), "C1": (3, 15),
    "C2": (4, 24), "C3": (4, 24),
}
CONTROL_META = dict(
    fixture_id="M00B2-CONTROLS-V1", fixture_version=1,
    family="CONTROLS", scenario_id="CONTROL", mapping_group="CONTROL",
)
CONTROL_QUERY = {
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
NEGATIVE_OWNER = {
    **dict.fromkeys(("N01", "N02", "N03", "N06", "N07", "N11", "N12", "N14", "N17", "N18"), "L02"),
    **dict.fromkeys(("N04", "N05", "N10", "N13", "N16"), "L03"),
    **dict.fromkeys(("N08", "N09", "N15"), "L04"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("x", encoding="utf-8") as handle:
        for entry in rows:
            handle.write(json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")


def exact(value: Any) -> str:
    # JSON encoding distinguishes bool/int and str and tagged Decimal representation.
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def difference(wanted: list[dict[str, Any]], actual: list[dict[str, Any]]) -> dict[str, Any] | None:
    for index in range(max(len(wanted), len(actual))):
        a = actual[index] if index < len(actual) else None
        e = wanted[index] if index < len(wanted) else None
        if exact(a) != exact(e):
            return {"index": index, "expected": e, "actual": a, "expected_count": len(wanted), "actual_count": len(actual)}
    return None


def read_expected(directory: Path) -> tuple[list[dict[str, Any]], dict[str, str]]:
    paths = [directory / family / "expected_m00_output_v1.jsonl" for family in "ABC"]
    paths.append(directory / "controls/expected_control_output_v1.jsonl")
    return canonical([entry for path in paths for entry in jsonl(path)]), {
        str(path.relative_to(directory)): digest(path) for path in paths
    }


def load_inputs(directory: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, str]]:
    paths = [directory / family / "synthetic_input_v1.jsonl" for family in "ABC"]
    paths.append(directory / "controls/control_input_v1.jsonl")
    paths.extend(directory / "negative" / f"N{i:02}_v1.jsonl" for i in range(1, 19))
    hashes = {str(path.relative_to(directory)): digest(path) for path in paths}
    return [entry for path in paths[:3] for entry in jsonl(path)], jsonl(paths[3]), hashes


def history_queries(data: list[dict[str, Any]], expected_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # The selection is sourced from *input* collector fields, not desired output.
    from m00_fixture_io import decode

    roles: dict[str, set[str]] = defaultdict(set)
    for entry in expected_rows:
        if entry["kind"] == "projection":
            roles[entry["mapping_group"]].add(entry["value"]["raw_signal_catalogue_id"])
    representatives = {entry["mapping_group"]: entry for entry in data}
    result = []
    for group, item in sorted(representatives.items()):
        obs = item["observation"]
        collector = decode(obs["native_record"])["_collector"]
        for role in sorted(roles[group]):
            result.append({
                "group": group, "raw_id": role, "subject": obs["subject_instrument"],
                "cutoff": "2026-10-26T14:00:10Z" if item["family"] == "B" else "2026-10-20T12:40:01Z",
                "selection": {key: collector[key] for key in (
                    "subject", "request", "generation", "requested_exchange", "scenario_id"
                )},
            })
    return result


def _fresh_public_readback(database: Path, specs: Path, destination: Path) -> None:
    """Called solely in a new OS process after the writer has closed."""
    from m00_fixture_io import read_rows
    payload = json.loads(specs.read_text())
    public = owner(database, create=False)
    from m00_fixture_io import mapping_group
    from nvda_desk.raw_signal_occurrence_truth import api as r
    a4_id = payload["absence_probes"]["a4_observation_id"]
    controls = payload["absence_probes"]["control_ids"]
    absent_probes = {
        "N04_receipt_only_with_event_cutoff": history_rows(
            public, group="A4-STK", raw_id="R190",
            subject="NVDA-STK-CONTROL-1", cutoff="2026-10-20T12:40:01Z",
            selection=payload["absence_probes"]["a4_selection"],
            event_cutoff="2026-10-20T12:40:01Z",
        ),
        "N08_error317_not_R187": public.reads.project_raw_value(
            r.RawSignalCatalogueId("R187"),
            r.observation_occurrence_id(controls[0]),
            mappings=(mapping_group("A4-STK")["R187"],),
        ) is None,
        "N09_error316_not_R187": public.reads.project_raw_value(
            r.RawSignalCatalogueId("R187"),
            r.observation_occurrence_id(controls[1]),
            mappings=(mapping_group("A4-STK")["R187"],),
        ) is None,
        "N06_non_native_R193_missing": public.reads.project_raw_value(
            r.RawSignalCatalogueId("R193"),
            r.observation_occurrence_id(a4_id),
            mappings=(mapping_group("C2-STK")["R193"],),
        ) is None,
    }
    result = {
        "absence_probes": absent_probes,
        "positive_rows": read_rows(public, payload["observation_queries"]),
        "control_discovery": discovery_rows(public, payload["control_query"]),
        "histories": [history_rows(public, **query) for query in payload["history_queries"]],
    }
    write_json(destination, result)


def run_readback_subprocess(database: Path, specs: Path, destination: Path) -> None:
    env = dict(os.environ, PYTHONPATH=os.pathsep.join((str(ROOT / "src"), str(ROOT / "tools"))))
    cmd = [sys.executable, str(Path(__file__).resolve()), "--internal-readback",
           str(database), str(specs), str(destination)]
    completed = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError(f"fresh-read-only subprocess exited {completed.returncode}: {completed.stderr[:3000]}")


def run(args: argparse.Namespace) -> int:
    fixtures, expected_dir, database, output = (
        Path(args.fixtures).resolve(), Path(args.expected).resolve(),
        Path(args.database), Path(args.output).resolve(),
    )
    if not database.is_absolute() or database.exists():
        raise ValueError("--database must be an ABSENT absolute file path")
    if output.exists():
        raise ValueError("--output must be a NEW directory")
    if not database.parent.is_dir() or not output.parent.is_dir():
        raise ValueError("database and output parent directories must exist")
    if output == database or output in database.parents or database in output.parents:
        raise ValueError("output directory and SQLite file may not overlap")
    output.mkdir()
    manifest: dict[str, Any] = {
        "manifest_version": "m00-brief2-actual-export/1",
        "status": "RUNNING_NOT_VERIFIED", "independent_review": "NOT_PERFORMED",
        "backend": "SQLite", "postgres_runtime": "DEFERRED", "live_ibkr": "UNVERIFIED",
        "source_git_sha": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
            text=True, capture_output=True, check=True).stdout.strip(),
        "source_clean_at_start": subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
            text=True, capture_output=True, check=True).stdout == "",
        "environment": {"python": sys.version.split()[0], "sqlite": __import__("sqlite3").sqlite_version},
        "versions": {"fixture": 1, "oracle": 1, "output_schema": 1,
                     "mapping_manifest": 1, "control_envelope": 1},
        "replay_command": "python tools/export_m00_synthetic.py --fixtures <fixture-dir> --expected <oracle-dir> --database <ABSENT-ABSOLUTE-PATH> --output <NEW-DIR>",
        "first_mismatch": None,
    }
    try:
        data, controls, input_hashes = load_inputs(fixtures)
        wanted, oracle_hashes = read_expected(expected_dir)
        manifest["input_hashes"] = input_hashes
        manifest["oracle_hashes"] = oracle_hashes
        manifest["mapping_sha256"] = digest(ART / "mapping_manifest_v1.json")
        manifest["schema_sha256"] = digest(ART / "output_schema_v1.json")
        signed = json.loads((ART / "fixture_manifest_v1.json").read_text())["hashes"]
        for rel, h in {**input_hashes, **oracle_hashes}.items():
            if signed.get("fixtures/" + rel) != h:
                raise ValueError(f"immutable fixture/oracle hash differs from admitted fixture manifest: {rel}")
        if len(data) != 36 or len(controls) != 5 or len(wanted) != 196:
            raise ValueError("fixture cardinality differs from L01 contract")
        # Authorised raw observations are independently decoded input rows only.
        raw = owner(database, create=True)
        for input_row in data:
            raw.commands.admit_raw_observation_occurrence(observation(input_row))
        for control in controls:
            raw.commands.admit_raw_observation_occurrence(control_observation(control))
        del raw  # close writer; new process below uses public read-only owner
        writer_db_hash = digest(database)
        from m00_fixture_io import decode
        a4 = next(item for item in data if item["scenario_id"] == "A4")
        a4_collector = decode(a4["observation"]["native_record"])["_collector"]
        specs = {
            "absence_probes": {
                "a4_observation_id": a4["observation"]["observation_occurrence_id"],
                "control_ids": [item["control_id"] for item in controls],
                "a4_selection": {key: a4_collector[key] for key in (
                    "subject", "request", "generation", "requested_exchange", "scenario_id"
                )},
            },
            "observation_queries": queries(data),
            "control_query": CONTROL_QUERY,
            "history_queries": history_queries(data, wanted),
        }
        write_json(output / "readback_requests_v1.json", specs)
        run_readback_subprocess(database, output / "readback_requests_v1.json", output / "fresh_public_readback_v1.json")
        if digest(database) != writer_db_hash:
            raise AssertionError("read-only fresh process changed SQLite database bytes")
        readback = json.loads((output / "fresh_public_readback_v1.json").read_text())
        absence_probes = readback["absence_probes"]
        absence_expected = {
            "N04_receipt_only_with_event_cutoff": [],
            "N08_error317_not_R187": True,
            "N09_error316_not_R187": True,
            "N06_non_native_R193_missing": True,
        }
        write_json(output / "actual_absence_outcomes_v1.json", {
            "actual": absence_probes, "expected": absence_expected,
            "exact_match": exact(absence_probes) == exact(absence_expected),
        })
        positive = readback["positive_rows"]
        control_actual = [{"kind": "control", **CONTROL_META, "value": value}
                          for value in readback["control_discovery"]["controls"]]
        actual = canonical([*positive, *control_actual])
        write_jsonl(output / "actual_m00_output_v1.jsonl", actual)
        write_jsonl(output / "actual_control_output_v1.jsonl", canonical(control_actual))
        schema = json.loads((ART / "output_schema_v1.json").read_text())
        for entry in actual:
            validate_instance(entry, schema)
        per_scenario = {}
        for scenario in SCENARIOS:
            observed = Counter(entry["kind"] for entry in actual if entry["scenario_id"] == scenario)
            exp = Counter(entry["kind"] for entry in wanted if entry["scenario_id"] == scenario)
            expected_count = COUNTS[scenario]
            per_scenario[scenario] = {
                "observations": observed["observation"], "projections": observed["projection"],
                "expected_observations": expected_count[0], "expected_projections": expected_count[1],
                "row_counts_match": (observed["observation"], observed["projection"]) == expected_count
                     and exp["observation"] == expected_count[0] and exp["projection"] == expected_count[1],
            }
        manifest["scenarios"] = per_scenario
        manifest["total_positive_observations"] = sum(entry["kind"] == "observation" for entry in actual)
        manifest["total_positive_projections"] = sum(entry["kind"] == "projection" for entry in actual)
        manifest["control_count"] = len(control_actual)
        manifest["read_only_sqlite_hash_unchanged"] = True
        manifest["sqlite_sha256"] = writer_db_hash
        manifest["first_mismatch"] = difference(wanted, actual)
        # Histories are validated independently against the L01 literal projection oracle.
        history_checks = []
        for spec, hist in zip(specs["history_queries"], readback["histories"], strict=True):
            oracle = [entry["value"] for entry in wanted if entry["kind"] == "projection"
                      and entry["mapping_group"] == spec["group"]
                      and entry["value"]["raw_signal_catalogue_id"] == spec["raw_id"]
                      and entry["value"]["subject_instrument"] == spec["subject"]
                      and all(entry["value"]["selection_identity"].get(key) == val
                              for key, val in spec["selection"].items())]
            oracle.sort(key=lambda x: (x["received_ts_utc"], x["ingestion_sequence_scope"],
                                        x["ingestion_sequence"], x["observation_occurrence_id"]))
            history_checks.append({"mapping_group": spec["group"], "r_id": spec["raw_id"],
                                   "count": len(hist), "expected_count": len(oracle),
                                   "exact_match": exact(hist) == exact(oracle)})
        manifest["history_checks"] = history_checks
        negative = []
        for i in range(1, 19):
            case = f"N{i:02}"
            negative.append({"case": case, "fixture_sha256": input_hashes[f"negative/{case}_v1.jsonl"],
                             "owner_leaf": NEGATIVE_OWNER[case],
                             "outcome": "PRIOR_ACCEPTED_PROOF_REFERENCED_NOT_EXECUTED_BY_EXPORTER",
                             "evidence": f"handoff/m00_brief2/evidence/{NEGATIVE_OWNER[case]}/" + ("strict.log" if NEGATIVE_OWNER[case] == "L03" else "strict-green.log")})
        write_json(output / "negative_outcomes_v1.json", negative)
        manifest["absence_outcomes"] = {
            "count": len(absence_probes), "exact_match": exact(absence_probes) == exact(absence_expected),
            "file": "actual_absence_outcomes_v1.json"}
        manifest["negative_cases"] = {"count": 18, "new_negative_execution": "NOT_PERFORMED",
                                       "outcome_file": "negative_outcomes_v1.json"}
        manifest["actual_hashes"] = {file.name: digest(file) for file in (
            output / "actual_m00_output_v1.jsonl", output / "actual_control_output_v1.jsonl")}
        ok = (manifest["first_mismatch"] is None and
              all(item["row_counts_match"] for item in per_scenario.values()) and
              all(item["exact_match"] for item in history_checks) and len(control_actual) == 5
              and exact(absence_probes) == exact(absence_expected))
        manifest["status"] = ("AUTHOR_REPLAY_MATCH_INDEPENDENT_REVIEW_PENDING" if ok
                               else "FAILED_PUBLIC_OUTPUT_COMPARISON")
        manifest["pinned_python_3_12_14"] = sys.version_info[:3] == (3, 12, 14)
        manifest["acceptance_status"] = "PENDING_INDEPENDENT_REVIEW" if ok and manifest["pinned_python_3_12_14"] else "NOT_ACCEPTED"
        write_json(output / "manifest_v1.json", manifest)
        return 0 if ok and manifest["pinned_python_3_12_14"] else 2
    except BaseException as exc:
        manifest["status"] = "FAILED_EXPORT"
        manifest["first_mismatch"] = manifest["first_mismatch"] or {"failure": type(exc).__name__, "detail": str(exc)}
        write_json(output / "failure_v1.json", {"error": str(exc), "traceback": traceback.format_exc()})
        write_json(output / "manifest_v1.json", manifest)
        return 2


def main() -> int:
    if len(sys.argv) == 5 and sys.argv[1] == "--internal-readback":
        _fresh_public_readback(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", required=True, help="Immutable family/controls/negative fixture directory")
    parser.add_argument("--expected", required=True, help="Independent oracle directory with A/B/C and controls")
    parser.add_argument("--database", required=True, help="Absolute path to absent SQLite file")
    parser.add_argument("--output", required=True, help="New, non-existing output directory")
    return run(parser.parse_args())


if __name__ == "__main__":
    sys.exit(main())
