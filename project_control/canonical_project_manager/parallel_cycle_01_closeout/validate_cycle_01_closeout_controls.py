#!/usr/bin/env python3
"""Mechanical consistency checks for the Parallel Cycle 01 PM closeout controls."""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INTEGRATED_BASE = "d6cfff9ab00cb5772baad26b14a8d388b08a241a"
ALLOWED_EXACT = {
    "ROADMAP_LEDGER_V2.md",
    "project_control/canonical_project_manager/EXEC_PLAN.md",
    "project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md",
    "project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md",
    "project_control/canonical_project_manager/PARALLEL_CYCLE_01/README.md",
    "project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md",
    "project_control/canonical_project_manager/VALIDATION_LOG.md",
}
ALLOWED_PREFIX = "project_control/canonical_project_manager/parallel_cycle_01_closeout/"

results: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    results.append((name, ok, detail))


def git(*args: str) -> tuple[int, str, str]:
    cp = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    return cp.returncode, cp.stdout.strip(), cp.stderr.strip()


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


branch = git("branch", "--show-current")[1]
record("branch", branch == "integration/parallel-cycle-01", branch)

live = {
    "exec": read("project_control/canonical_project_manager/EXEC_PLAN.md"),
    "roadmap": read("ROADMAP_LEDGER_V2.md"),
    "gate": read("project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md"),
    "registry": read("project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md"),
    "architecture": read("project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md"),
    "cycle_readme": read("project_control/canonical_project_manager/PARALLEL_CYCLE_01/README.md"),
}
expected = {
    "exec": "`parallel_cycle_01_aggregate_validated_closed`",
    "roadmap": "`parallel_cycle_01_aggregate_validated_closed`",
    "gate": "**Status:** `PARALLEL_CYCLE_01_AGGREGATE_VALIDATED_CLOSED`",
    "registry": "`PARALLEL_CYCLE_01_AGGREGATE_VALIDATED_CLOSED`",
    "architecture": "**Status:** `ACTIVE:PARALLEL_CYCLE_01_AGGREGATE_VALIDATED`",
    "cycle_readme": "`AGGREGATE_VALIDATED_CLOSED`",
}
for name, marker in expected.items():
    record(f"{name}_live_status", marker in live[name], marker)

# Registry allocation table has exactly 19 columns in header, separator and every row.
lines = live["registry"].splitlines()
start = lines.index("## Cycle 01 allocation and lineage")
table = []
for line in lines[start + 2 :]:
    if not line.startswith("|"):
        break
    table.append(line)
column_counts = [len(line.split("|")[1:-1]) for line in table]
record("registry_allocation_table_columns", bool(column_counts) and len(set(column_counts)) == 1 and column_counts[0] == 19, repr(column_counts))
record("registry_four_pass_rows", live["registry"].count("| `PASS` | `NVDA_LANE_") == 4, "expected four populated PASS package rows")

# Closeout files exist and accepted outputs contain exact summaries.
required = {
    "project_control/canonical_project_manager/parallel_cycle_01_closeout/CYCLE_01_PM_AGGREGATE_CLOSEOUT.md": "PASS:PARALLEL_CYCLE_01_AGGREGATE_VALIDATED_CLOSED",
    "project_control/canonical_project_manager/parallel_cycle_01_closeout/CYCLE_01_AGGREGATE_MECHANICAL_VALIDATION.txt": "SUMMARY\tchecks=28\tpass=28\tfail=0",
    "project_control/canonical_project_manager/parallel_cycle_01_closeout/CYCLE_01_M04_EXACT_LOCATOR_REVALIDATION.txt": "locator_validation_failures=0",
    "project_control/canonical_project_manager/parallel_cycle_01_closeout/CYCLE_01_AGGREGATE_VALIDATOR_REPAIR_NOTE.md": "f13ed3bf551f6c9ca25b522e9a17b23c5ed0528c",
}
for rel, marker in required.items():
    path = ROOT / rel
    ok = path.is_file() and path.stat().st_size > 0 and marker in path.read_text(encoding="utf-8")
    record("required_" + path.name, ok, f"size={path.stat().st_size if path.exists() else 0}")

# Full-read manifest has unique paths and current required controls.
manifest = ROOT / "project_control/canonical_project_manager/parallel_cycle_01_closeout/CYCLE_01_PM_CLOSEOUT_FULL_READ_MANIFEST.tsv"
with manifest.open(encoding="utf-8", newline="") as fh:
    rows = list(csv.DictReader(fh, delimiter="\t"))
paths = [row["path"] for row in rows]
record("closeout_manifest_unique", len(paths) == len(set(paths)), f"rows={len(paths)} unique={len(set(paths))}")
for rel in ALLOWED_EXACT:
    record("manifest_routes_" + Path(rel).name, rel in set(paths), rel)

# Closeout mutation boundary relative to the integrated state, including an uncommitted run.
rc, committed, err = git("diff", "--name-only", f"{INTEGRATED_BASE}..HEAD")
committed_paths = set(committed.splitlines()) if rc == 0 and committed else set()
worktree_paths = set(filter(None, git("diff", "--name-only")[1].splitlines()))
untracked = set(filter(None, git("ls-files", "--others", "--exclude-standard")[1].splitlines()))
all_paths = committed_paths | worktree_paths | untracked
out_of_scope = sorted(p for p in all_paths if p not in ALLOWED_EXACT and not p.startswith(ALLOWED_PREFIX))
record("pm_closeout_write_set", not out_of_scope, f"paths={len(all_paths)} out_of_scope={out_of_scope}")

# No behavioural path enters the PM closeout unit.
forbidden_prefixes = ("src/", "tests/", "config/", "configs/", "fixtures/", "migrations/", "nvda_desk/")
forbidden = sorted(p for p in all_paths if p.startswith(forbidden_prefixes))
record("no_behavioral_closeout_mutation", not forbidden, repr(forbidden))

# Git structural checks.
rc, out, err = git("diff", "--check")
record("git_diff_check", rc == 0, out or err or "clean")
rc, out, err = git("fsck", "--full", "--no-dangling")
record("git_fsck", rc == 0, out or err or "clean")
rc, out, err = git("rev-parse", "--is-shallow-repository")
record("repository_non_shallow", rc == 0 and out == "false", out or err)

print("CYCLE_01_CLOSEOUT_CONTROL_VALIDATION")
for name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{detail}")
failures = [name for name, ok, _ in results if not ok]
print(f"SUMMARY\tchecks={len(results)}\tpass={len(results)-len(failures)}\tfail={len(failures)}")
if failures:
    print("FAILED_CHECKS\t" + ",".join(failures))
    sys.exit(1)
