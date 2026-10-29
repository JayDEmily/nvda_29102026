"""Actual public export and independent clean-checkout reproducibility."""

import copy
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from export_m00_synthetic import ART, ROOT, difference, digest


def test_export_pipeline(tmp_path):
    def run(root, name):
        output = tmp_path / name
        command = [
            sys.executable,
            str(root / "tools/export_m00_synthetic.py"),
            "--fixtures",
            str(root / "handoff/m00_brief2/fixtures"),
            "--expected",
            str(root / "handoff/m00_brief2/fixtures"),
            "--database",
            str(tmp_path / (name + ".db")),
            "--output",
            str(output),
        ]
        env = dict(os.environ, PYTHONPATH=os.pathsep.join((str(root / "tools"), str(root / "src"))))
        completed = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)
        assert completed.returncode == 0, (
            completed.stdout
            + completed.stderr
            + (
                (output / "manifest_v1.json").read_text()
                if (output / "manifest_v1.json").exists()
                else ""
            )
        )
        return output

    original_hashes = json.loads((ART / "fixture_manifest_v1.json").read_text())["hashes"]
    first = run(ROOT, "first")
    manifest = json.loads((first / "manifest_v1.json").read_text())
    assert manifest["total_positive_observations"] == 36
    assert manifest["total_positive_projections"] == 155
    assert manifest["control_count"] == 5
    assert manifest["first_mismatch"] is None
    assert manifest["read_only_sqlite_hash_unchanged"] is True
    assert manifest["source_clean_at_start"] is True
    negative = json.loads((first / "negative_outcomes_v1.json").read_text())
    assert [item["case_id"] for item in negative] == [f"N{i:02}" for i in range(1, 19)]
    assert all(item["verified"] is True for item in negative)
    rows = [
        json.loads(line) for line in (first / "actual_m00_output_v1.jsonl").read_text().splitlines()
    ]
    altered = copy.deepcopy(rows)
    probe = next(
        item
        for item in altered
        if item["kind"] == "projection"
        and item["value"]["native_value"]["native_type"] == "Decimal"
    )
    spelling = probe["value"]["native_value"]["value"]
    probe["value"]["native_value"]["value"] = spelling + ("0" if "." in spelling else ".0")
    assert difference(rows, altered) is not None
    checkout = tmp_path / "clean-checkout"
    subprocess.run(
        ["git", "clone", "--no-local", str(ROOT), str(checkout)],
        check=True,
        capture_output=True,
        text=True,
    )
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    subprocess.run(
        ["git", "checkout", "--detach", head], cwd=checkout, check=True, capture_output=True
    )
    assert subprocess.check_output(["git", "status", "--porcelain"], cwd=checkout, text=True) == ""
    second = run(checkout, "second")
    files = [
        "actual_m00_output_v1.jsonl",
        "actual_control_output_v1.jsonl",
        "negative_outcomes_v1.json",
        "actual_absence_outcomes_v1.json",
    ]
    hashes = {name: digest(first / name) for name in files}
    assert hashes == {name: digest(second / name) for name in files}
    for name, expected_hash in original_hashes.items():
        assert digest(ART / name) == expected_hash
    evidence = Path(os.environ.get("M00_EXPORT_EVIDENCE", str(tmp_path / "retained")))
    evidence.mkdir(parents=True, exist_ok=False)
    for name in [*files, "manifest_v1.json", "readback_requests_v1.json"]:
        shutil.copy2(first / name, evidence / name)
    (evidence / "reproduction_v1.json").write_text(
        json.dumps(
            {
                "candidate": head,
                "source_clean": True,
                "second_clean_checkout": True,
                "deterministic_hashes": hashes,
                "comparison": "EXACT_BYTE_HASH_EQUAL",
            },
            indent=2,
        )
        + "\n"
    )
