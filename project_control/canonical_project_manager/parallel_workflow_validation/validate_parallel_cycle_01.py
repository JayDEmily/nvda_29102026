#!/usr/bin/env python3
"""Mechanical validation for the repaired Cycle 01 parallel-control checkpoint.

The script validates structure, identifiers, manifests, vocabulary projection,
artefact contracts and collision boundaries. It does not make semantic authority,
independent-test or Project Manager acceptance decisions.
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
BRIEF_MANIFEST = PACK / "BRIEF_PACK_MANIFEST.tsv"
CONTROL_PACK = PM / "PARALLEL_CYCLE_01_CONTROL_REPAIR"
BASE = "ae7c8b05bf3742a5c0be530a26617d999313d232"
SUPERSEDED_CONTROL = "9e404df7c13f7cca170e05e4c9f76b8ec4548ffa"

EXPECTED = {
    "1A": {
        "worker_thread": "Lane 1AW",
        "tester_thread": "Lane 1AT",
        "unit": "M01-PROOF-MLC-R-V1",
        "worker_branch": "work/lane-1a-m01-mlc-r-v1",
        "tester_branch": "test/lane-1a-m01-mlc-r-v1",
        "name": "M01_MLC_R",
        "worker_manifest": "project_control/canonical_project_manager/modules/M01/raw_validation/mlc_r_v1/FULL_READ_MANIFEST.tsv",
        "tester_manifest": "project_control/canonical_project_manager/modules/M01/raw_validation/tester_mlc_r_v1/FULL_READ_MANIFEST.tsv",
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
        "worker_thread": "Lane 2AW", "tester_thread": "Lane 2AT",
        "unit": "M04-PROOF-MLC-A-V1",
        "worker_branch": "work/lane-2a-m04-mlc-a-v1", "tester_branch": "test/lane-2a-m04-mlc-a-v1",
        "name": "M04_MLC_A",
        "worker_manifest": "project_control/canonical_project_manager/modules/M04/raw_validation/mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "tester_manifest": "project_control/canonical_project_manager/modules/M04/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "worker_paths": {"project_control/canonical_project_manager/modules/M04/M04_AUTHORITY_WORKER_RECORD_V1.md", "project_control/canonical_project_manager/modules/M04/raw_validation/mlc_a_v1/**"},
        "tester_paths": {"project_control/canonical_project_manager/modules/M04/M04_AUTHORITY_TESTER_REVIEW_V1.md", "project_control/canonical_project_manager/modules/M04/raw_validation/tester_mlc_a_v1/**"},
    },
    "3A": {
        "worker_thread": "Lane 3AW", "tester_thread": "Lane 3AT",
        "unit": "M07-PROOF-MLC-A-V1",
        "worker_branch": "work/lane-3a-m07-mlc-a-v1", "tester_branch": "test/lane-3a-m07-mlc-a-v1",
        "name": "M07_MLC_A",
        "worker_manifest": "project_control/canonical_project_manager/modules/M07/raw_validation/mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "tester_manifest": "project_control/canonical_project_manager/modules/M07/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "worker_paths": {"project_control/canonical_project_manager/modules/M07/M07_AUTHORITY_WORKER_RECORD_V1.md", "project_control/canonical_project_manager/modules/M07/raw_validation/mlc_a_v1/**"},
        "tester_paths": {"project_control/canonical_project_manager/modules/M07/M07_AUTHORITY_TESTER_REVIEW_V1.md", "project_control/canonical_project_manager/modules/M07/raw_validation/tester_mlc_a_v1/**"},
    },
    "4A": {
        "worker_thread": "Lane 4AW", "tester_thread": "Lane 4AT",
        "unit": "M08-PROOF-MLC-A-V1",
        "worker_branch": "work/lane-4a-m08-mlc-a-v1", "tester_branch": "test/lane-4a-m08-mlc-a-v1",
        "name": "M08_MLC_A",
        "worker_manifest": "project_control/canonical_project_manager/modules/M08/raw_validation/mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "tester_manifest": "project_control/canonical_project_manager/modules/M08/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "worker_paths": {"project_control/canonical_project_manager/modules/M08/M08_AUTHORITY_WORKER_RECORD_V1.md", "project_control/canonical_project_manager/modules/M08/raw_validation/mlc_a_v1/**"},
        "tester_paths": {"project_control/canonical_project_manager/modules/M08/M08_AUTHORITY_TESTER_REVIEW_V1.md", "project_control/canonical_project_manager/modules/M08/raw_validation/tester_mlc_a_v1/**"},
    },
}

VOCAB_SLUGS = {
    "pm_controlled_parallel_workflow", "parallel_execution_lane", "lane_assignment",
    "material_read_set", "worker_candidate_archive",
    "tester_approved_portability_artefact", "independent_control_test",
}
PACKAGE_MEMBERS = {
    "MANIFEST.json", "changes.bundle", "CHANGED_PATHS.tsv", "FILE_SHA256.tsv",
    "WORKER_CLAIM.md", "TESTER_VERDICT.md", "validation/", "RECONSTRUCTION.txt", "SHA256SUMS",
}
ALLOWED_CHANGED_PREFIXES = (
    "AGENTS.md", "PLANS.md", "ROADMAP_LEDGER_V2.md",
    "docs/00_CONTROL_SURFACE_ROUTING_INDEX.md", "docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md",
    "docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md",
    "docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md",
    "docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md",
    "docs/vocabulary/vocabulary_registry.md", "data/vocabulary/canonical_vocabulary.json",
    "project_control/canonical_project_manager/EXEC_PLAN.md",
    "project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md",
    "project_control/canonical_project_manager/FULL_READ_MANIFEST.tsv",
    "project_control/canonical_project_manager/VALIDATION_LOG.md",
    "project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md",
    "project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md",
    "project_control/canonical_project_manager/PARALLEL_CYCLE_01/",
    "project_control/canonical_project_manager/PARALLEL_CYCLE_01_CONTROL_REPAIR/",
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
    return {
        token for token in re.findall(r"^- `([^`]+)`$", text[start:end], re.MULTILINE)
        if token.startswith("project_control/")
    }

def add(results: list[Result], name: str, passed: bool, detail: object) -> None:
    results.append(Result(name, bool(passed), str(detail)))

def main() -> int:
    results: list[Result] = []
    branch = git("branch", "--show-current")
    add(results, "repair branch", branch == "control/parallel-workflow-enablement-v1-repair-1", branch)
    add(results, "accepted base ancestry", git("merge-base", "HEAD", BASE) == BASE, BASE)
    add(results, "superseded control ancestry", git("merge-base", "HEAD", SUPERSEDED_CONTROL) == SUPERSEDED_CONTROL, SUPERSEDED_CONTROL)

    worker_files = sorted(PACK.glob("LANE_*/*AW_WORKER_BRIEF.md"))
    tester_files = sorted(PACK.glob("LANE_*/*AT_TESTER_BRIEF.md"))
    add(results, "worker brief count", len(worker_files) == 4, len(worker_files))
    add(results, "tester brief count", len(tester_files) == 4, len(tester_files))

    all_threads: set[str] = set()
    all_branches: set[str] = set()
    all_write_paths: list[tuple[str, str]] = []
    for assignment, exp in EXPECTED.items():
        folder = next(PACK.glob(f"LANE_{assignment}_*"), None)
        if not folder:
            add(results, f"{assignment} folder", False, "missing")
            continue
        wf = next(folder.glob("*AW_WORKER_BRIEF.md")); tf = next(folder.glob("*AT_TESTER_BRIEF.md"))
        wt, tt = wf.read_text(), tf.read_text()
        try:
            identity = {
                "worker_thread": field(wt, "Worker thread"), "tester_thread": field(tt, "Tester thread"),
                "worker_unit": field(wt, "Unit"), "tester_unit": field(tt, "Unit"),
                "worker_branch": field(wt, "Worker branch"), "tester_branch": field(tt, "Tester branch"),
                "worker_revision": field(wt, "Revision"), "tester_revision": field(tt, "Revision"),
            }
        except ValueError as exc:
            add(results, f"{assignment} identity parse", False, exc); continue
        expected_identity = {
            "worker_thread": exp["worker_thread"], "tester_thread": exp["tester_thread"],
            "worker_unit": exp["unit"], "tester_unit": exp["unit"],
            "worker_branch": exp["worker_branch"], "tester_branch": exp["tester_branch"],
            "worker_revision": "R1", "tester_revision": "R1",
        }
        add(results, f"{assignment} identity", identity == expected_identity, identity)
        for token in (identity["worker_thread"], identity["tester_thread"]):
            add(results, f"unique thread {token}", token not in all_threads, token); all_threads.add(token)
        for token in (identity["worker_branch"], identity["tester_branch"]):
            add(results, f"unique branch {token}", token not in all_branches, token); all_branches.add(token)

        wp = bullet_paths(wt, "## Exact writable paths", "## Global and cross-lane locks")
        tp = bullet_paths(tt, "The tester may add only:", "All source")
        add(results, f"{assignment} worker write set", wp == exp["worker_paths"], sorted(wp))
        add(results, f"{assignment} tester write set", tp == exp["tester_paths"], sorted(tp))
        for p in wp | tp:
            normal = p.removesuffix("/**")
            for other, owner in all_write_paths:
                if owner != assignment and (normal.startswith(other) or other.startswith(normal)):
                    add(results, "cross-lane write collision", False, f"{assignment}:{normal} vs {owner}:{other}")
            all_write_paths.append((normal, assignment))

        add(results, f"{assignment} worker local manifest", exp["worker_manifest"] in wt, exp["worker_manifest"])
        add(results, f"{assignment} tester local manifest", exp["tester_manifest"] in tt, exp["tester_manifest"])
        add(results, f"{assignment} no global registry read", "MASTER_WORKFLOW_REGISTRY.md" not in wt and "MASTER_WORKFLOW_REGISTRY.md" not in tt, "assignment-local context")
        add(results, f"{assignment} worker stop rule", "Complete this one leaf and return" in wt, "bounded worker")
        add(results, f"{assignment} tester no repair", "Do not repair worker output" in tt, "independent tester")

        worker_archive = f"NVDA_LANE_{assignment}_{exp['name']}_WORKER_CANDIDATE_R1_FULL_HISTORY.tar.gz"
        pass_archive = f"NVDA_LANE_{assignment}_{exp['name']}_TESTER_APPROVED_R1.tar.gz"
        add(results, f"{assignment} worker archive name", worker_archive in wt, worker_archive)
        add(results, f"{assignment} tester PASS archive name", pass_archive in tt, pass_archive)
        missing_members = sorted(member for member in PACKAGE_MEMBERS if f"`{member}`" not in tt)
        add(results, f"{assignment} portability members", not missing_members, missing_members)
        add(results, f"{assignment} bundle verification", "git bundle verify" in tt, "required")

    lane1 = (PACK / "LANE_1A_M01_MLC_R/LANE_1AW_WORKER_BRIEF.md").read_text() + (PACK / "LANE_1A_M01_MLC_R/LANE_1AT_TESTER_BRIEF.md").read_text()
    lane1_tokens = [
        "tests/AGENTS.override.md", "docs/01_NORMATIVE_CORE.md", "docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md",
        "docs/vocabulary/vocabulary_registry.md", "docs/08_TESTING_AND_PROMOTION_CORE.md",
        "docs/08.1_TESTING_AND_PROMOTION_WORKING.md", "config/retained_test_registry.yaml", "config/proof_blocks.yaml",
    ]
    add(results, "Lane 1 test override route", all(lane1.count(token) >= 2 for token in lane1_tokens), lane1_tokens)

    with BRIEF_MANIFEST.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    add(results, "brief manifest row count", len(rows) == 8, len(rows))
    for row in rows:
        path = ROOT / row["brief_path"]
        add(results, f"brief hash {row['thread_name']}", path.is_file() and sha256(path) == row["sha256"], row["sha256"])

    future_outputs = set().union(*(set(exp["worker_paths"]) | set(exp["tester_paths"]) for exp in EXPECTED.values()))
    exact_missing: list[str] = []
    for brief in worker_files + tester_files:
        for token in re.findall(r"`([^`]+)`", brief.read_text()):
            if not token.startswith(("00_TASK/", "docs/", "project_control/", "config/", "tests/")):
                continue
            if token in future_outputs:
                continue
            if "*" in token or "<" in token or token.endswith("FULL_READ_MANIFEST.tsv") or "raw_validation/" in token:
                continue
            if not (ROOT / token).exists():
                exact_missing.append(f"{brief.relative_to(ROOT)} -> {token}")
    add(results, "brief exact existing references", not exact_missing, exact_missing)

    control_brief = CONTROL_PACK / "PARALLEL_CONTROL_T1_INDEPENDENT_TESTER_BRIEF.md"
    ctext = control_brief.read_text() if control_brief.exists() else ""
    add(results, "independent control tester brief", control_brief.exists(), control_brief.relative_to(ROOT))
    for token in ("Parallel Control T1", "test/parallel-workflow-enablement-v1-repair-1", "NVDA_PARALLEL_WORKFLOW_CYCLE_01_CONTROL_REPAIR_1_20260729_FULL_HISTORY.tar.gz", "SUITABLE_FOR_PM_PARALLEL_CONTROL_ACCEPTANCE_REVIEW", "Do not repair the package"):
        add(results, f"control tester token {token}", token in ctext, token)
    control_test_tokens = ["tests/AGENTS.override.md", "docs/08_TESTING_AND_PROMOTION_CORE.md", "docs/08.1_TESTING_AND_PROMOTION_WORKING.md", "config/retained_test_registry.yaml", "config/proof_blocks.yaml"]
    add(results, "control tester test-override route", all(token in ctext for token in control_test_tokens), control_test_tokens)

    registry = (PM / "MASTER_WORKFLOW_REGISTRY.md").read_text()
    roadmap = (ROOT / "ROADMAP_LEDGER_V2.md").read_text()
    exec_plan = (PM / "EXEC_PLAN.md").read_text()
    gate = (PM / "GATE_C_COMPLETION_PROTOCOL.md").read_text()
    architecture = (PM / "PARALLEL_WORKFLOW_ARCHITECTURE.md").read_text()
    status_tokens = [
        (registry, "PARALLEL_CONTROL_REPAIR_1_AWAITING_INDEPENDENT_CONTROL_TEST"),
        (roadmap, "parallel_control_repair_1_awaiting_independent_control_test"),
        (exec_plan, "parallel_control_repair_1_awaiting_independent_control_test"),
        (gate, "PARALLEL_CONTROL_REPAIR_1_AWAITING_INDEPENDENT_CONTROL_TEST"),
    ]
    add(results, "control repair status agreement", all(token in text for text, token in status_tokens), "awaiting independent control test")
    add(results, "worker launch blocked", all("Parallel Control T1" in text and ("blocked" in text.lower() or "do not launch" in text.lower() or "not launch" in text.lower()) for text in (registry, roadmap, exec_plan, gate, architecture, (PACK / "README.md").read_text())), "six live controls")
    add(results, "held lanes", all(text.count("HELD_BLOCKED_DEPENDENCY") >= 2 for text in (registry, roadmap, architecture)), "Lanes 5 and 6")

    required_registry_fields = ["Worker commit", "Tester evidence commit", "Approved portability artefact", "Artefact SHA-256", "PM disposition", "Queue position", "Integration commit", "Aggregate validation", "Repair revision"]
    add(results, "registry lineage fields", all(token in registry for token in required_registry_fields), required_registry_fields)
    add(results, "registry exact artefact table", all(f"NVDA_LANE_{a}_{e['name']}_WORKER_CANDIDATE_R1_FULL_HISTORY.tar.gz" in registry for a,e in EXPECTED.items()), "four assignments")

    registry_human = (ROOT / "docs/vocabulary/vocabulary_registry.md").read_text()
    projection = json.loads((ROOT / "data/vocabulary/canonical_vocabulary.json").read_text())
    projection_slugs = {row["canonical_slug"] for row in projection["entries"]}
    add(results, "human vocabulary admissions", all(f'"canonical_slug":"{slug}"' in registry_human for slug in VOCAB_SLUGS), sorted(VOCAB_SLUGS))
    add(results, "generated vocabulary admissions", VOCAB_SLUGS <= projection_slugs, sorted(VOCAB_SLUGS - projection_slugs))
    add(results, "vocabulary overlay admission", "## 10.13 PM-controlled parallel-workflow admissions" in (ROOT / "docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md").read_text(), "10.13")

    current_manifest = PM / "parallel_workflow_validation/PARALLEL_CONTROL_REPAIR_FULL_READ_MANIFEST.tsv"
    add(results, "control current-target read manifest", current_manifest.is_file() and current_manifest.read_text().startswith("path\tevidence_class\tread_status"), current_manifest.relative_to(ROOT))

    repair_hash_manifest = PM / "parallel_workflow_validation/repair_1/FILE_SHA256.tsv"
    hash_manifest_failures: list[str] = []
    if repair_hash_manifest.is_file():
        with repair_hash_manifest.open(newline="") as handle:
            hash_rows = list(csv.DictReader(handle, delimiter="\t"))
        for row in hash_rows:
            rel = row["path"]
            expected = row["sha256"]
            if rel == str(repair_hash_manifest.relative_to(ROOT)) and expected == "SELF_NOT_HASHED":
                continue
            if rel == str(current_manifest.relative_to(ROOT)) and expected == "CROSS_REFERENTIAL_NOT_HASHED":
                continue
            target = ROOT / rel
            if not target.is_file():
                hash_manifest_failures.append(f"missing:{rel}")
                continue
            if sha256(target) != expected:
                hash_manifest_failures.append(f"sha256:{rel}")
                continue
            if row["bytes"] != str(target.stat().st_size):
                hash_manifest_failures.append(f"bytes:{rel}")
    else:
        hash_manifest_failures.append("missing:FILE_SHA256.tsv")
    add(results, "repair evidence file hashes", not hash_manifest_failures, hash_manifest_failures)

    read_manifest_failures: list[str] = []
    if current_manifest.is_file():
        with current_manifest.open(newline="") as handle:
            read_rows = list(csv.DictReader(handle, delimiter="\t"))
        for row in read_rows:
            rel = row["path"]
            expected = row["sha256_after_repair"]
            if rel == str(current_manifest.relative_to(ROOT)) and expected == "SELF_REFERENTIAL_NOT_RECORDED":
                continue
            target = Path(rel) if Path(rel).is_absolute() else ROOT / rel
            if not target.is_file():
                read_manifest_failures.append(f"missing:{rel}")
                continue
            if sha256(target) != expected:
                read_manifest_failures.append(f"sha256:{rel}")
    else:
        read_manifest_failures.append("missing:FULL_READ_MANIFEST.tsv")
    add(results, "control read-manifest current hashes", not read_manifest_failures, read_manifest_failures)

    original_review = (PM / "parallel_workflow_validation/PARALLEL_CONTROL_PM_REVIEW_V1.md").read_text()
    add(results, "original PM acceptance superseded", original_review.startswith("> **SUPERSEDED AND REJECTED BEFORE LAUNCH:**"), "historical only")

    changed = set(filter(None, git("diff", "--name-only", BASE).splitlines())) | set(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    forbidden = [p for p in sorted(changed) if not any(p == allowed or p.startswith(allowed) for allowed in ALLOWED_CHANGED_PREFIXES)]
    add(results, "control repair changed-path boundary", not forbidden, f"count={len(changed)} forbidden={forbidden}")
    behaviour = [p for p in sorted(changed) if p.startswith(("src/", "tests/", "config/", "migrations/"))]
    add(results, "no behavioural mutation", not behaviour, behaviour)
    add(results, "generated vocabulary only under data", not [p for p in changed if p.startswith("data/") and p != "data/vocabulary/canonical_vocabulary.json"], "canonical projection")

    machine = json.loads((PM / "architecture/Atlas_Architecture_Machine_Readable.json").read_text())
    contracts = {row["contract_id"]: row for row in machine["contracts"]}
    owner_ok = all(contracts[k]["owner_module"] == m for k,m in {"K01":"M01","K02":"M01","K03":"M01","K07":"M04","K12":"M07","K13":"M08"}.items())
    add(results, "Cycle 1 contract ownership", owner_ok, "K01–K03/K07/K12/K13")
    add(results, "M07 positive obligation", any(o.get("obligation_id") == "OBL-M07-POSITIVE" and o.get("module_id") == "M07" for o in machine.get("mandatory_module_obligations", [])), "OBL-M07-POSITIVE")

    blueprint = (ROOT / "docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md").read_text()
    heads = re.findall(r"^### (11\.10\.\d+)", blueprint, re.MULTILINE)
    add(results, "11.10 heading order", heads == ["11.10.1","11.10.2","11.10.3","11.10.4","11.10.5"], heads)

    failed = [r for r in results if not r.passed]
    print("PARALLEL CYCLE 01 REPAIR STRUCTURAL VALIDATION")
    for result in results:
        print(f"{'PASS' if result.passed else 'FAIL'}\t{result.name}\t{result.detail}")
    print(f"SUMMARY\tchecks={len(results)}\tpassed={len(results)-len(failed)}\tfailed={len(failed)}")
    if failed:
        print("NOTE\tMechanical validation failed; no independent or PM acceptance is inferred.")
        return 1
    print("NOTE\tMechanical validation passed; independent control testing and PM acceptance remain mandatory before lane launch.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
