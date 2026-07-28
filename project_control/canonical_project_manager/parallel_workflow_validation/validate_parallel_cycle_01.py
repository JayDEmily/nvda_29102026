#!/usr/bin/env python3
"""Mechanical validation for the Cycle 01 parallel-control checkpoint.

This script validates structure, identifiers, paths, hashes and collision boundaries.
It does not make semantic authority or acceptance decisions.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PM = ROOT / "project_control/canonical_project_manager"
PACK = PM / "PARALLEL_CYCLE_01"
MANIFEST = PACK / "BRIEF_PACK_MANIFEST.tsv"

EXPECTED = {
    "1A": {
        "worker_thread": "Lane 1AW",
        "tester_thread": "Lane 1AT",
        "unit": "M01-PROOF-MLC-R-V1",
        "worker_branch": "work/lane-1a-m01-mlc-r-v1",
        "tester_branch": "test/lane-1a-m01-mlc-r-v1",
        "worker_paths": {
            "project_control/canonical_project_manager/modules/M01/M01_RELEVANT_TEST_ROUTING_WORKER_RECORD_V1.md",
            "project_control/canonical_project_manager/modules/M01/raw_validation/mlc_r_v1/**",
        },
        "tester_paths": {
            "project_control/canonical_project_manager/modules/M01/M01_RELEVANT_TEST_ROUTING_TESTER_REVIEW_V1.md",
            "project_control/canonical_project_manager/modules/M01/raw_validation/tester_mlc_r_v1/**",
        },
    },
    "2A": {
        "worker_thread": "Lane 2AW",
        "tester_thread": "Lane 2AT",
        "unit": "M04-PROOF-MLC-A-V1",
        "worker_branch": "work/lane-2a-m04-mlc-a-v1",
        "tester_branch": "test/lane-2a-m04-mlc-a-v1",
        "worker_paths": {
            "project_control/canonical_project_manager/modules/M04/M04_AUTHORITY_WORKER_RECORD_V1.md",
            "project_control/canonical_project_manager/modules/M04/raw_validation/mlc_a_v1/**",
        },
        "tester_paths": {
            "project_control/canonical_project_manager/modules/M04/M04_AUTHORITY_TESTER_REVIEW_V1.md",
            "project_control/canonical_project_manager/modules/M04/raw_validation/tester_mlc_a_v1/**",
        },
    },
    "3A": {
        "worker_thread": "Lane 3AW",
        "tester_thread": "Lane 3AT",
        "unit": "M07-PROOF-MLC-A-V1",
        "worker_branch": "work/lane-3a-m07-mlc-a-v1",
        "tester_branch": "test/lane-3a-m07-mlc-a-v1",
        "worker_paths": {
            "project_control/canonical_project_manager/modules/M07/M07_AUTHORITY_WORKER_RECORD_V1.md",
            "project_control/canonical_project_manager/modules/M07/raw_validation/mlc_a_v1/**",
        },
        "tester_paths": {
            "project_control/canonical_project_manager/modules/M07/M07_AUTHORITY_TESTER_REVIEW_V1.md",
            "project_control/canonical_project_manager/modules/M07/raw_validation/tester_mlc_a_v1/**",
        },
    },
    "4A": {
        "worker_thread": "Lane 4AW",
        "tester_thread": "Lane 4AT",
        "unit": "M08-PROOF-MLC-A-V1",
        "worker_branch": "work/lane-4a-m08-mlc-a-v1",
        "tester_branch": "test/lane-4a-m08-mlc-a-v1",
        "worker_paths": {
            "project_control/canonical_project_manager/modules/M08/M08_AUTHORITY_WORKER_RECORD_V1.md",
            "project_control/canonical_project_manager/modules/M08/raw_validation/mlc_a_v1/**",
        },
        "tester_paths": {
            "project_control/canonical_project_manager/modules/M08/M08_AUTHORITY_TESTER_REVIEW_V1.md",
            "project_control/canonical_project_manager/modules/M08/raw_validation/tester_mlc_a_v1/**",
        },
    },
}

ALLOWED_CHANGED_PREFIXES = (
    "AGENTS.md",
    "PLANS.md",
    "ROADMAP_LEDGER_V2.md",
    "docs/00_CONTROL_SURFACE_ROUTING_INDEX.md",
    "docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md",
    "docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md",
    "docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md",
    "project_control/canonical_project_manager/EXEC_PLAN.md",
    "project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md",
    "project_control/canonical_project_manager/FULL_READ_MANIFEST.tsv",
    "project_control/canonical_project_manager/VALIDATION_LOG.md",
    "project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md",
    "project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md",
    "project_control/canonical_project_manager/PARALLEL_CYCLE_01/",
    "project_control/canonical_project_manager/parallel_workflow_validation/",
)


@dataclass
class Result:
    name: str
    passed: bool
    detail: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def field(text: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}: `([^`]+)`$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"missing field {label!r}")
    return match.group(1)


def bullet_paths(text: str, heading: str, stop_heading: str | None = None) -> set[str]:
    start = text.index(heading) + len(heading)
    end = text.find(stop_heading, start) if stop_heading else len(text)
    if end == -1:
        end = len(text)
    section = text[start:end]
    return {
        token
        for token in re.findall(r"^- `([^`]+)`$", section, re.MULTILINE)
        if token.startswith("project_control/")
    }


def main() -> int:
    results: list[Result] = []

    branch = git("branch", "--show-current")
    results.append(Result("control branch", branch == "control/parallel-workflow-enablement-v1", branch))
    base = "ae7c8b05bf3742a5c0be530a26617d999313d232"
    merge_base = git("merge-base", "HEAD", base)
    results.append(Result("source ancestry", merge_base == base, f"merge-base={merge_base}"))

    worker_files = sorted(PACK.glob("LANE_*/*AW_WORKER_BRIEF.md"))
    tester_files = sorted(PACK.glob("LANE_*/*AT_TESTER_BRIEF.md"))
    results.append(Result("worker brief count", len(worker_files) == 4, str(len(worker_files))))
    results.append(Result("tester brief count", len(tester_files) == 4, str(len(tester_files))))

    parsed: dict[str, dict[str, object]] = {}
    all_branches: set[str] = set()
    all_threads: set[str] = set()
    all_cross_lane_paths: dict[str, str] = {}

    for assignment, exp in EXPECTED.items():
        folder = next(PACK.glob(f"LANE_{assignment}_*"), None)
        if folder is None:
            results.append(Result(f"{assignment} folder", False, "missing"))
            continue
        wf = next(folder.glob("*AW_WORKER_BRIEF.md"), None)
        tf = next(folder.glob("*AT_TESTER_BRIEF.md"), None)
        if wf is None or tf is None:
            results.append(Result(f"{assignment} pair", False, "worker or tester brief missing"))
            continue
        wt = wf.read_text()
        tt = tf.read_text()
        try:
            actual = {
                "worker_thread": field(wt, "Worker thread"),
                "tester_thread": field(tt, "Tester thread"),
                "unit_worker": field(wt, "Unit"),
                "unit_tester": field(tt, "Unit"),
                "worker_branch": field(wt, "Worker branch"),
                "tester_branch": field(tt, "Tester branch"),
            }
        except ValueError as exc:
            results.append(Result(f"{assignment} identity parse", False, str(exc)))
            continue
        worker_paths = bullet_paths(wt, "## Exact writable paths", "## Global and cross-lane locks")
        tester_paths = bullet_paths(tt, "The tester may add only:", "All source")
        actual["worker_paths"] = worker_paths
        actual["tester_paths"] = tester_paths
        parsed[assignment] = actual

        identity_ok = (
            actual["worker_thread"] == exp["worker_thread"]
            and actual["tester_thread"] == exp["tester_thread"]
            and actual["unit_worker"] == exp["unit"]
            and actual["unit_tester"] == exp["unit"]
            and actual["worker_branch"] == exp["worker_branch"]
            and actual["tester_branch"] == exp["tester_branch"]
        )
        detail_actual = {
            key: sorted(value) if isinstance(value, set) else value
            for key, value in actual.items()
        }
        results.append(Result(f"{assignment} identity", identity_ok, json.dumps(detail_actual, sort_keys=True)))
        results.append(Result(f"{assignment} worker write set", worker_paths == exp["worker_paths"], repr(sorted(worker_paths))))
        results.append(Result(f"{assignment} tester write set", tester_paths == exp["tester_paths"], repr(sorted(tester_paths))))

        for thread in (actual["worker_thread"], actual["tester_thread"]):
            if str(thread) in all_threads:
                results.append(Result(f"unique thread {thread}", False, "duplicate"))
            all_threads.add(str(thread))
        for branch_name in (actual["worker_branch"], actual["tester_branch"]):
            if str(branch_name) in all_branches:
                results.append(Result(f"unique branch {branch_name}", False, "duplicate"))
            all_branches.add(str(branch_name))
        for write_path in worker_paths | tester_paths:
            normalised = write_path.rstrip("/**")
            for other, owner in all_cross_lane_paths.items():
                if assignment != owner and (normalised.startswith(other) or other.startswith(normalised)):
                    results.append(Result("cross-lane write collision", False, f"{assignment}:{normalised} vs {owner}:{other}"))
            all_cross_lane_paths[normalised] = assignment

        required_tokens = (
            "Complete this one leaf and return" if "WORKER" in wf.name else "Do not repair worker output"
        )
        results.append(Result(f"{assignment} bounded stop rule", required_tokens in (wt if "WORKER" in wf.name else tt), required_tokens))
        results.append(Result(f"{assignment} worker archive rule", "Return one archive only" in wt, "one candidate archive"))
        results.append(Result(f"{assignment} tester archive rule", "Return exactly one tester-result archive" in tt, "one tester-result archive"))

    # Manifest exactness and hashes.
    with MANIFEST.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    results.append(Result("brief manifest row count", len(rows) == 8, str(len(rows))))
    for row in rows:
        p = ROOT / row["brief_path"]
        ok = p.is_file() and sha256(p) == row["sha256"]
        results.append(Result(f"manifest hash {row['thread_name']}", ok, row["sha256"]))

    # Every exact repository path in backticks must exist unless it is a declared future output.
    future_outputs = set().union(*(set(e["worker_paths"]) | set(e["tester_paths"]) for e in EXPECTED.values()))
    missing_refs: list[str] = []
    exact_refs = 0
    for p in worker_files + tester_files:
        for token in re.findall(r"`([^`]+)`", p.read_text()):
            if "/" not in token or token.startswith(("work/", "test/")):
                continue
            if "*" in token or "<" in token:
                continue
            if not token.startswith(("00_TASK/", "docs/", "project_control/")):
                continue
            exact_refs += 1
            if token in future_outputs:
                continue
            if not (ROOT / token).exists():
                missing_refs.append(f"{p.relative_to(ROOT)} -> {token}")
    results.append(Result("brief exact-path references", not missing_refs, f"checked={exact_refs}; missing={missing_refs}"))

    # Held lanes and common status.
    registry = (PM / "MASTER_WORKFLOW_REGISTRY.md").read_text()
    roadmap = (ROOT / "ROADMAP_LEDGER_V2.md").read_text()
    exec_plan = (PM / "EXEC_PLAN.md").read_text()
    gate = (PM / "GATE_C_COMPLETION_PROTOCOL.md").read_text()
    architecture = (PM / "PARALLEL_WORKFLOW_ARCHITECTURE.md").read_text()
    status_ok = all(
        token in text
        for text, token in [
            (registry, "PARALLEL_CYCLE_01_ALLOCATED_AWAITING_WORKER_LAUNCH"),
            (roadmap, "parallel_cycle_01_allocated_awaiting_worker_launch"),
            (exec_plan, "parallel_cycle_01_allocated_awaiting_worker_launch"),
            (gate, "PARALLEL_CYCLE_01_ALLOCATED_AWAITING_WORKER_LAUNCH"),
        ]
    )
    results.append(Result("control status agreement", status_ok, "Cycle 01 allocated awaiting launch"))
    held_ok = all("HELD_BLOCKED_DEPENDENCY" in text or "dependency-held" in text for text in (registry, roadmap, architecture))
    results.append(Result("lanes 5 and 6 held", held_ok, "held markers present"))
    serial_integration_ok = all(
        "integration" in text.lower()
        and ("serial" in text.lower() or "sequential" in text.lower())
        for text in (exec_plan, gate, architecture, roadmap)
    )
    results.append(Result("serial canonical integration", serial_integration_ok, "present in four controls"))

    # No unapproved placeholder vocabulary in the new pack.
    placeholder_hits: list[str] = []
    allowed_placeholder = "SUPPLIED_IN_PM_LAUNCH_BLOCK_AFTER_CHECKPOINT_PUBLICATION"
    for p in [PM / "PARALLEL_WORKFLOW_ARCHITECTURE.md", PM / "MASTER_WORKFLOW_REGISTRY.md", *sorted(PACK.rglob("*"))]:
        if not p.is_file() or p.suffix not in {".md", ".tsv"}:
            continue
        for i, line in enumerate(p.read_text().splitlines(), 1):
            if re.search(r"\b(TODO|TBD|FIXME|PLACEHOLDER)\b", line):
                placeholder_hits.append(f"{p.relative_to(ROOT)}:{i}:{line}")
            if "SUPPLIED_IN_PM_LAUNCH" in line and allowed_placeholder not in line:
                placeholder_hits.append(f"{p.relative_to(ROOT)}:{i}:{line}")
    results.append(Result("placeholder control", not placeholder_hits, repr(placeholder_hits)))
    results.append(Result("external launch placeholders", registry.count(allowed_placeholder) == 3, str(registry.count(allowed_placeholder))))

    # Changed-path boundary.
    changed = set(filter(None, git("diff", "--name-only", base).splitlines()))
    untracked = set(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    all_changed = changed | untracked
    forbidden = [p for p in sorted(all_changed) if not any(p == allowed or p.startswith(allowed) for allowed in ALLOWED_CHANGED_PREFIXES)]
    results.append(Result("control-only changed paths", not forbidden, f"count={len(all_changed)}; forbidden={forbidden}"))
    behaviour = [p for p in sorted(all_changed) if p.startswith(("src/", "tests/", "config/", "migrations/"))]
    results.append(Result("no behavioural mutation", not behaviour, repr(behaviour)))

    # Architecture source still parses and Cycle 1 roots/contract owners agree.
    machine = json.loads((PM / "architecture/Atlas_Architecture_Machine_Readable.json").read_text())
    contracts = {row["contract_id"]: row for row in machine["contracts"]}
    owner_ok = (
        contracts["K01"]["owner_module"] == "M01"
        and contracts["K02"]["owner_module"] == "M01"
        and contracts["K03"]["owner_module"] == "M01"
        and contracts["K07"]["owner_module"] == "M04"
        and contracts["K12"]["owner_module"] == "M07"
        and contracts["K13"]["owner_module"] == "M08"
    )
    results.append(Result("Cycle 1 contract ownership", owner_ok, "K01/K02/K03→M01; K07→M04; K12→M07; K13→M08"))
    obligation_ok = any(o.get("obligation_id") == "OBL-M07-POSITIVE" and o.get("module_id") == "M07" for o in machine.get("mandatory_module_obligations", []))
    results.append(Result("M07 positive obligation", obligation_ok, "OBL-M07-POSITIVE"))

    # Heading order after the architecture amendment.
    blueprint = (ROOT / "docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md").read_text()
    heads = re.findall(r"^### (11\.10\.\d+)", blueprint, re.MULTILINE)
    results.append(Result("11.10 heading order", heads == ["11.10.1", "11.10.2", "11.10.3", "11.10.4", "11.10.5"], repr(heads)))

    failed = [r for r in results if not r.passed]
    print("PARALLEL CYCLE 01 STRUCTURAL VALIDATION")
    for r in results:
        print(f"{'PASS' if r.passed else 'FAIL'}\t{r.name}\t{r.detail}")
    print(f"SUMMARY\tchecks={len(results)}\tpassed={len(results)-len(failed)}\tfailed={len(failed)}")
    if failed:
        print("NOTE\tMechanical validation failed; no semantic acceptance is inferred.")
        return 1
    print("NOTE\tMechanical validation passed; semantic authority and future lane outputs remain subject to human/PM adjudication.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
