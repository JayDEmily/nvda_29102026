#!/usr/bin/env python3
"""Mechanical aggregate validation for the integrated Parallel Cycle 01 state.

This script validates repository topology, lane scope, recorded evidence structure,
brief integrity, and bounded machine-readable reconciliations. It does not make or
replace semantic Project Manager acceptance decisions.
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = "ee67c752d14073a959fda478f31f4466b6952cae"
LANE4_PM = "d6cfff9ab00cb5772baad26b14a8d388b08a241a"
EXPECTED_BRANCH = "integration/parallel-cycle-01"

LANES = {
    "1A": {
        "start": BASE,
        "end": "934a60752642213bdac01475ff9aaddb56fc4340",
        "prefix": "project_control/canonical_project_manager/modules/M01/",
        "tester_ref": ("refs/remotes/lane1/test", "d935f6d669e8ee7e21818d3df4ff1d6df54ca8b6"),
    },
    "2A": {
        "start": "4ff92943bc881d2a1996ea5cd54da4e7ba0bcebe",
        "end": "a085870fafa9e3df380f9d5ad8cc93455b65cf57",
        "prefix": "project_control/canonical_project_manager/modules/M04/",
        "tester_ref": ("refs/remotes/lane2/test", "23289785e154110686a146671ef3d483f8f05f0b"),
    },
    "3A": {
        "start": "a538880f14f5e47a063412714a980400b4a18c19",
        "end": "1651caff9e56264b52a3ae884be308c9f8761dd4",
        "prefix": "project_control/canonical_project_manager/modules/M07/",
        "tester_ref": ("refs/remotes/lane3/test", "a78ce0642b257b0bf3779e46cd962f95dec3781a"),
    },
    "4A": {
        "start": "391781b0f576619063b0c3dbc559a62b71fa9baa",
        "end": "c3917c33edc8da1d89751d9f8b6b305e0fd9146c",
        "prefix": "project_control/canonical_project_manager/modules/M08/",
        "tester_ref": ("refs/remotes/lane4/test", "f13ed3bf551f6c9ca25b522e9a17b23c5ed0528c"),
    },
}

results: list[tuple[str, bool, str]] = []


def run(*args: str, check: bool = True) -> str:
    cp = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if check and cp.returncode != 0:
        raise RuntimeError(f"command failed ({cp.returncode}): {' '.join(args)}\n{cp.stdout}{cp.stderr}")
    return cp.stdout.strip()


def record(name: str, ok: bool, detail: str) -> None:
    results.append((name, ok, detail))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


try:
    branch = run("git", "branch", "--show-current")
    record("branch", branch == EXPECTED_BRANCH, branch)

    shallow = run("git", "rev-parse", "--is-shallow-repository")
    record("repository_non_shallow", shallow == "false", shallow)

    base_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT
    ).returncode == 0
    record("accepted_launch_is_ancestor", base_ancestor, BASE)

    lane4_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", LANE4_PM, "HEAD"], cwd=ROOT
    ).returncode == 0
    record("lane4_pm_acceptance_is_ancestor", lane4_ancestor, LANE4_PM)

    ordered = [
        BASE,
        "4ff92943bc881d2a1996ea5cd54da4e7ba0bcebe",
        "a538880f14f5e47a063412714a980400b4a18c19",
        "391781b0f576619063b0c3dbc559a62b71fa9baa",
        LANE4_PM,
    ]
    order_ok = all(
        subprocess.run(["git", "merge-base", "--is-ancestor", a, b], cwd=ROOT).returncode == 0
        for a, b in zip(ordered, ordered[1:])
    )
    record("pm_integration_order_1A_2A_3A_4A", order_ok, " -> ".join(x[:12] for x in ordered))

    lane_paths: dict[str, set[str]] = {}
    for lane, meta in LANES.items():
        paths = set(filter(None, run("git", "diff", "--name-only", f"{meta['start']}..{meta['end']}").splitlines()))
        lane_paths[lane] = paths
        confined = bool(paths) and all(p.startswith(str(meta["prefix"])) for p in paths)
        record(f"{lane}_write_set_confined", confined, f"{len(paths)} paths under {meta['prefix']}")
        ref, expected = meta["tester_ref"]
        actual = run("git", "rev-parse", ref)
        record(f"{lane}_tester_provenance_ref", actual == expected, f"{ref}={actual}")

    overlaps: list[str] = []
    lane_names = list(lane_paths)
    for i, left in enumerate(lane_names):
        for right in lane_names[i + 1 :]:
            common = sorted(lane_paths[left] & lane_paths[right])
            if common:
                overlaps.append(f"{left}/{right}: {','.join(common)}")
    record("cross_lane_write_sets_disjoint", not overlaps, "none" if not overlaps else "; ".join(overlaps))

    lane_delta = set(filter(None, run("git", "diff", "--name-only", f"{BASE}..{LANE4_PM}").splitlines()))
    allowed_prefixes = tuple(meta["prefix"] for meta in LANES.values()) + (
        "project_control/canonical_project_manager/parallel_cycle_01_closeout/",
    )
    out_of_scope = sorted(p for p in lane_delta if not p.startswith(allowed_prefixes))
    record("cycle_lane_delta_control_evidence_only", not out_of_scope, f"{len(lane_delta)} paths; out_of_scope={out_of_scope}")

    forbidden_prefixes = (
        "src/", "tests/", "test/", "config/", "configs/", "fixtures/", "migrations/",
        "nvda_desk/", "app/", "lib/",
    )
    forbidden = sorted(p for p in lane_delta if p.startswith(forbidden_prefixes))
    record("no_behavioral_surface_mutation", not forbidden, "none" if not forbidden else ",".join(forbidden))

    # Cycle brief pack integrity.
    brief_manifest = ROOT / "project_control/canonical_project_manager/PARALLEL_CYCLE_01/BRIEF_PACK_MANIFEST.tsv"
    brief_rows = tsv_rows(brief_manifest)
    brief_bad = []
    for row in brief_rows:
        path = ROOT / row["brief_path"]
        actual = sha256(path) if path.is_file() else "MISSING"
        if actual != row["sha256"]:
            brief_bad.append(f"{row['brief_path']} expected={row['sha256']} actual={actual}")
    record("brief_pack_sha256", len(brief_rows) == 8 and not brief_bad, f"rows={len(brief_rows)} bad={brief_bad}")

    # M01 complete routing inventory reconciliation.
    inv = tsv_rows(ROOT / "project_control/canonical_project_manager/modules/M01/raw_validation/mlc_r_v1/PHYSICAL_TEST_ROUTING_INVENTORY.tsv")
    chains = tsv_rows(ROOT / "project_control/canonical_project_manager/modules/M01/raw_validation/mlc_r_v1/M01_CURRENT_CLAIM_ROUTE_CHAINS.tsv")
    inv_paths = [r["test_path"] for r in inv]
    route_paths = {r["test_path"] for r in inv if r["m01_route_classification"] == "M01_CURRENT_CLAIM_ROUTE"}
    shadow_paths = {r["test_path"] for r in inv if r["m01_route_classification"] == "LEGACY_SHADOW_UNADMITTED"}
    chain_paths = {r["test_path"] for r in chains}
    m01_ok = (
        len(inv) == 179
        and len(set(inv_paths)) == 179
        and len(route_paths) == 20
        and len(shadow_paths) == 159
        and not (route_paths & shadow_paths)
        and route_paths | shadow_paths == set(inv_paths)
        and len(chains) == 20
        and chain_paths == route_paths
    )
    record("m01_routing_reconciliation", m01_ok, f"inventory={len(inv)} unique={len(set(inv_paths))} route={len(route_paths)} shadow={len(shadow_paths)} chains={len(chains)}")

    # Required semantic outcome markers (mechanical presence only).
    marker_checks = {
        "m01_tester_pass": (
            "project_control/canonical_project_manager/modules/M01/M01_RELEVANT_TEST_ROUTING_TESTER_REVIEW_V1.md",
            ["`PASS`", "SUITABLE_FOR_PM_M01_MLC_R_INTEGRATION_REVIEW"],
        ),
        "m04_authority_block_and_pass": (
            "project_control/canonical_project_manager/modules/M04/M04_AUTHORITY_TESTER_REVIEW_V1.md",
            ["`PASS`", "SUITABLE_FOR_PM_M04_MLC_A_INTEGRATION_REVIEW", "role-specific authority gap"],
        ),
        "m07_authority_block_and_positive_obligation": (
            "project_control/canonical_project_manager/modules/M07/M07_AUTHORITY_WORKER_RECORD_V1.md",
            ["BLOCKED_MISSING_NORMATIVE_AUTHORITY", "OBL-M07-POSITIVE", "ModifierApplicationReceipt"],
        ),
        "m07_tester_pass": (
            "project_control/canonical_project_manager/modules/M07/M07_AUTHORITY_TESTER_REVIEW_V1.md",
            ["`PASS`", "SUITABLE_FOR_PM_M07_MLC_A_INTEGRATION_REVIEW"],
        ),
        "m08_authority_block": (
            "project_control/canonical_project_manager/modules/M08/M08_AUTHORITY_WORKER_RECORD_V1.md",
            ["BLOCKED_MISSING_NORMATIVE_AUTHORITY", "deterministic", "tie-break"],
        ),
        "m08_tester_pass": (
            "project_control/canonical_project_manager/modules/M08/M08_AUTHORITY_TESTER_REVIEW_V1.md",
            ["`PASS`", "SUITABLE_FOR_PM_M08_MLC_A_INTEGRATION_REVIEW"],
        ),
    }
    for name, (rel, markers) in marker_checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        missing = [m for m in markers if m not in text]
        record(name, not missing, "missing=" + repr(missing))

    # Worker/tester manifests are independently present and non-empty.
    manifests = [
        "modules/M01/raw_validation/mlc_r_v1/FULL_READ_MANIFEST.tsv",
        "modules/M01/raw_validation/tester_mlc_r_v1/FULL_READ_MANIFEST.tsv",
        "modules/M04/raw_validation/mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "modules/M04/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "modules/M07/raw_validation/mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "modules/M07/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "modules/M08/raw_validation/mlc_a_v1/FULL_READ_MANIFEST.tsv",
        "modules/M08/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv",
    ]
    manifest_root = ROOT / "project_control/canonical_project_manager"
    bad_manifests = []
    for rel in manifests:
        path = manifest_root / rel
        rows = tsv_rows(path) if path.is_file() else []
        if not rows:
            bad_manifests.append(rel)
    record("independent_worker_tester_read_manifests", not bad_manifests, f"8 expected; bad={bad_manifests}")

    # Accepted machine-readable contract ownership.
    atlas = json.loads((ROOT / "project_control/canonical_project_manager/architecture/Atlas_Architecture_Machine_Readable.json").read_text(encoding="utf-8"))
    owners = {r["contract_id"]: r["owner_module"] for r in atlas["contracts"]}
    expected_owners = {"K01": "M01", "K02": "M01", "K03": "M01", "K07": "M04", "K12": "M07", "K13": "M08"}
    owner_bad = {k: (owners.get(k), v) for k, v in expected_owners.items() if owners.get(k) != v}
    record("atlas_contract_ownership", not owner_bad, repr(expected_owners if not owner_bad else owner_bad))

    # Git structural checks.
    diff_check = subprocess.run(["git", "diff", "--check"], cwd=ROOT, text=True, capture_output=True)
    record("git_diff_check", diff_check.returncode == 0, (diff_check.stdout + diff_check.stderr).strip() or "clean")
    fsck = subprocess.run(["git", "fsck", "--full", "--no-dangling"], cwd=ROOT, text=True, capture_output=True)
    record("git_fsck", fsck.returncode == 0, (fsck.stdout + fsck.stderr).strip() or "clean")

except Exception as exc:  # fail closed with a readable result
    record("validator_exception", False, str(exc))

print("CYCLE_01_AGGREGATE_MECHANICAL_VALIDATION")
for name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{detail}")
failures = [name for name, ok, _ in results if not ok]
print(f"SUMMARY\tchecks={len(results)}\tpass={len(results)-len(failures)}\tfail={len(failures)}")
if failures:
    print("FAILED_CHECKS\t" + ",".join(failures))
    sys.exit(1)
