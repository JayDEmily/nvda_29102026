from __future__ import annotations

from pathlib import Path


def test_proof_executor_control_surfaces_are_present() -> None:
    assert Path("scripts/run_proof_block.py").exists()
    assert Path("config/proof_blocks.yaml").exists()
    assert Path("Makefile").exists()


def test_proof_executor_control_surfaces_stay_manifest_driven() -> None:
    script = Path("scripts/run_proof_block.py").read_text(encoding="utf-8")
    makefile = Path("Makefile").read_text(encoding="utf-8")
    manifest = Path("config/proof_blocks.yaml").read_text(encoding="utf-8")

    assert "--block" in script
    assert "proof_blocks.yaml" in script
    assert "proof-block:" in makefile
    assert "proof-executor-check:" in makefile
    assert "run_proof_block.py" in makefile
    assert "--check-all" in script
    assert "proof_block_id: proof_executor_contract" in manifest


def test_proof_executor_describe_returns_manifest_summary() -> None:
    import json
    import subprocess
    import sys

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_proof_block.py",
            "--describe",
            "vocabulary_governance_conformance_candidate",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["proof_block_id"] == "vocabulary_governance_conformance_candidate"
    assert payload["tier"] == "Tier A"
    assert (
        "tests/tier_a/vocabulary/test_vocabulary_candidate_admission_plan_contracts.py"
        in payload["owns"]
    )
    assert "python -m pytest" in payload["command"]


def test_proof_executor_validates_owned_paths_before_running() -> None:
    script = Path("scripts/run_proof_block.py").read_text(encoding="utf-8")

    assert "_validate_owned_paths(block)" in script
    assert "proof block owns missing paths" in script
    assert "Path(str(path)).exists()" in script


def test_proof_executor_check_validates_manifest_without_running_block() -> None:
    import subprocess
    import sys

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_proof_block.py",
            "--check",
            "vocabulary_governance_conformance_candidate",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert completed.stdout.strip() == (
        "proof_block_check=PASS vocabulary_governance_conformance_candidate"
    )


def test_proof_executor_check_all_validates_manifest_without_running_blocks() -> None:
    import subprocess
    import sys

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_proof_block.py",
            "--check-all",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert completed.stdout.strip().startswith("proof_blocks_check_all=PASS count=")


def test_proof_executor_check_all_can_write_json_receipt(tmp_path: Path) -> None:
    import json
    import subprocess
    import sys

    receipt = tmp_path / "proof_check_all_receipt.json"

    subprocess.run(
        [
            sys.executable,
            "scripts/run_proof_block.py",
            "--check-all",
            "--receipt",
            str(receipt),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert payload["mode"] == "check_all"
    assert payload["status"] == "PASS"
    assert payload["exit_code"] == 0
    assert payload["block_count"] >= 4
    assert "proof_executor_contract" in payload["proof_block_ids"]
    proof_executor = {item["proof_block_id"]: item for item in payload["checked_blocks"]}[
        "proof_executor_contract"
    ]
    assert proof_executor["command"] == (
        "python -m pytest tests/tier_b/proof_model/test_proof_executor_contract.py"
    )
    assert "scripts/run_proof_block.py" in proof_executor["owns"]


def test_proof_executor_exposes_check_mode_in_cli_surface() -> None:
    script = Path("scripts/run_proof_block.py").read_text(encoding="utf-8")

    assert "--check" in script
    assert "--check-all" in script
    assert "--receipt" in script
    assert "--json" in script
    assert "proof_block_check=PASS" in script
    assert "proof_blocks_check_all=PASS" in script
    assert "_write_receipt" in script
    assert "_validate_all_blocks" in script


def test_proof_executor_check_mode_can_write_json_receipt(tmp_path: Path) -> None:
    import json
    import subprocess
    import sys

    receipt = tmp_path / "proof_check_receipt.json"

    subprocess.run(
        [
            sys.executable,
            "scripts/run_proof_block.py",
            "--check",
            "vocabulary_governance_conformance_candidate",
            "--receipt",
            str(receipt),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert payload["mode"] == "check"
    assert payload["status"] == "PASS"
    assert payload["exit_code"] == 0
    assert payload["proof_block_id"] == "vocabulary_governance_conformance_candidate"
    assert (
        "tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py"
        in payload["owns"]
    )


def test_proof_executor_list_can_emit_json() -> None:
    import json
    import subprocess
    import sys

    completed = subprocess.run(
        [sys.executable, "scripts/run_proof_block.py", "--list", "--json"],
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout)
    assert "vocabulary_governance_conformance_candidate" in payload["proof_blocks"]
    assert "vocabulary_synonym_audit_clean_check" in payload["proof_blocks"]
    assert "proof_executor_contract" in payload["proof_blocks"]


def test_proof_block_list_json_detailed_includes_block_summaries() -> None:
    import json
    import subprocess
    import sys

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_proof_block.py",
            "--list",
            "--json",
            "--detailed",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout)
    assert "vocabulary_governance_conformance_candidate" in payload["proof_blocks"]
    summaries = {item["proof_block_id"]: item for item in payload["proof_block_summaries"]}
    summary = summaries["vocabulary_governance_conformance_candidate"]
    assert summary["command"].startswith("python -m pytest")
    assert "src/nvda_desk/schemas/vocabulary.py" in summary["owns"]
    assert "proof_executor_contract" in summaries
    assert summaries["proof_executor_contract"]["tier"] == "Tier B"


def test_proof_block_runner_resolves_python_to_current_interpreter() -> None:
    import sys

    import scripts.run_proof_block as runner

    assert runner._resolve_command("python -m pytest tests")[:3] == [
        sys.executable,
        "-m",
        "pytest",
    ]
    assert runner._resolve_command("echo hello") == ["echo", "hello"]
    assert runner._resolve_command("env PYTHONPATH=src:. python -m pytest tests")[:4] == [
        "env",
        "PYTHONPATH=src:.",
        sys.executable,
        "-m",
    ]


def test_candidate_review_clean_check_proof_block_is_manifest_owned() -> None:
    import json
    import subprocess
    import sys

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_proof_block.py",
            "--describe",
            "vocabulary_candidate_review_clean_check",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["proof_block_id"] == "vocabulary_candidate_review_clean_check"
    assert "tests/fixtures/vocabulary_candidate_review/clean_candidates.json" in payload["owns"]
    assert "--check-clean" in payload["command"]


def test_proof_executor_contract_block_is_manifest_owned() -> None:
    import json
    import subprocess
    import sys

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_proof_block.py",
            "--describe",
            "proof_executor_contract",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["proof_block_id"] == "proof_executor_contract"
    assert payload["tier"] == "Tier B"
    assert payload["command"] == (
        "python -m pytest tests/tier_b/proof_model/test_proof_executor_contract.py"
    )
    assert "scripts/run_proof_block.py" in payload["owns"]
    assert "Makefile" in payload["owns"]


def _write_temp_proof_manifest(tmp_path: Path, blocks: list[dict[str, object]]) -> None:
    import yaml

    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "proof_blocks.yaml").write_text(
        yaml.safe_dump(
            {"schema_version": "v1", "proof_blocks": blocks},
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def _run_temp_proof_executor(tmp_path: Path, *args: str):
    import subprocess
    import sys

    runner = Path(__file__).resolve().parents[3] / "scripts" / "run_proof_block.py"
    return subprocess.run(
        [sys.executable, str(runner), *args],
        cwd=tmp_path,
        check=False,
        text=True,
        capture_output=True,
    )


def test_proof_executor_rejects_unknown_block_ids(tmp_path: Path) -> None:
    owned = tmp_path / "owned.txt"
    owned.write_text("owned\n", encoding="utf-8")
    _write_temp_proof_manifest(
        tmp_path,
        [
            {
                "proof_block_id": "known_block",
                "tier": "Tier B",
                "lifecycle": "test_only",
                "command": "python -c 'import sys; sys.exit(0)'",
                "owns": ["owned.txt"],
            }
        ],
    )

    completed = _run_temp_proof_executor(tmp_path, "--describe", "missing_block")

    assert completed.returncode != 0
    assert "unknown proof block 'missing_block'" in completed.stderr
    assert "available: known_block" in completed.stderr


def test_proof_executor_rejects_missing_owned_paths_before_running(tmp_path: Path) -> None:
    _write_temp_proof_manifest(
        tmp_path,
        [
            {
                "proof_block_id": "missing_owned_path_block",
                "tier": "Tier B",
                "lifecycle": "test_only",
                "command": 'python -c \'from pathlib import Path; Path("should_not_run.txt").write_text("ran")\'',
                "owns": ["does_not_exist.txt"],
            }
        ],
    )

    completed = _run_temp_proof_executor(tmp_path, "--block", "missing_owned_path_block")

    assert completed.returncode != 0
    assert "proof block owns missing paths: does_not_exist.txt" in completed.stderr
    assert not (tmp_path / "should_not_run.txt").exists()


def test_proof_executor_check_all_rejects_duplicate_block_ids(tmp_path: Path) -> None:
    owned = tmp_path / "owned.txt"
    owned.write_text("owned\n", encoding="utf-8")
    duplicate_block = {
        "proof_block_id": "duplicate_block",
        "tier": "Tier B",
        "lifecycle": "test_only",
        "command": "python -c 'import sys; sys.exit(0)'",
        "owns": ["owned.txt"],
    }
    _write_temp_proof_manifest(tmp_path, [duplicate_block, duplicate_block])

    completed = _run_temp_proof_executor(tmp_path, "--check-all")

    assert completed.returncode != 0
    assert "duplicate proof_block_id values: duplicate_block" in completed.stderr


def test_proof_executor_check_all_rejects_non_mapping_entries(tmp_path: Path) -> None:
    _write_temp_proof_manifest(tmp_path, ["not-a-proof-block-mapping"])

    completed = _run_temp_proof_executor(tmp_path, "--check-all")

    assert completed.returncode != 0
    assert "proof_blocks contains non-mapping entries: 0" in completed.stderr


def test_proof_executor_check_all_does_not_execute_manifest_commands(tmp_path: Path) -> None:
    owned = tmp_path / "owned.txt"
    marker = tmp_path / "check_all_should_not_run.txt"
    owned.write_text("owned\n", encoding="utf-8")
    _write_temp_proof_manifest(
        tmp_path,
        [
            {
                "proof_block_id": "check_all_no_run_block",
                "tier": "Tier B",
                "lifecycle": "test_only",
                "command": f"python -c 'from pathlib import Path; Path({str(marker)!r}).write_text(\"ran\")'",
                "owns": ["owned.txt"],
            }
        ],
    )

    completed = _run_temp_proof_executor(tmp_path, "--check-all")

    assert completed.returncode == 0
    assert completed.stdout.strip() == "proof_blocks_check_all=PASS count=1"
    assert not marker.exists()


def test_proof_executor_emits_block_header_before_child_output(tmp_path: Path) -> None:
    owned = tmp_path / "owned.txt"
    owned.write_text("owned\n", encoding="utf-8")
    _write_temp_proof_manifest(
        tmp_path,
        [
            {
                "proof_block_id": "ordered_output_block",
                "tier": "Tier B",
                "lifecycle": "test_only",
                "command": "python -c 'print(\"child-output\")'",
                "owns": ["owned.txt"],
            }
        ],
    )

    completed = _run_temp_proof_executor(tmp_path, "--block", "ordered_output_block")

    assert completed.returncode == 0
    assert completed.stdout.splitlines() == [
        "proof_block_id=ordered_output_block",
        "command=python -c 'print(\"child-output\")'",
        "child-output",
    ]


def test_proof_executor_runs_manifest_commands_without_shell_evaluation(tmp_path: Path) -> None:
    owned = tmp_path / "owned.txt"
    owned.write_text("owned\n", encoding="utf-8")
    _write_temp_proof_manifest(
        tmp_path,
        [
            {
                "proof_block_id": "no_shell_block",
                "tier": "Tier B",
                "lifecycle": "test_only",
                "command": "python -c 'import sys; sys.exit(0)' ; touch shell_injection_marker.txt",
                "owns": ["owned.txt"],
            }
        ],
    )

    completed = _run_temp_proof_executor(tmp_path, "--block", "no_shell_block")

    assert completed.returncode == 0
    assert not (tmp_path / "shell_injection_marker.txt").exists()
