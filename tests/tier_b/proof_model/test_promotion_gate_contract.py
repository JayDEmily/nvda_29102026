from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.run_promotion_gate import (
    PromotionError,
    _run_block,
    build_check_summary,
    classify_pytest_result,
    require_clean_git,
    resolve_command,
    sign_receipt,
    verify_receipt,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_live_pre_m00_gate_resolves_exact_membership_without_execution() -> None:
    summary = build_check_summary("pre_m00_current", repo_root=REPO_ROOT)

    assert len(summary["proof_block_ids"]) == 13
    assert len(summary["test_family_ids"]) == 13
    assert len(summary["test_paths"]) == 15
    assert summary["test_paths"][0].startswith("tests/tier_a/")


def test_env_prefixed_python_command_uses_current_interpreter_without_shell() -> None:
    resolved, environment = resolve_command(
        "env PYTHONPATH=src:. python -m pytest tests/tier_a/example.py",
        inherited_environment={"BASE": "1"},
    )

    assert resolved[:3] == [sys.executable, "-m", "pytest"]
    assert resolved[-1] == "tests/tier_a/example.py"
    assert environment == {"BASE": "1", "PYTHONPATH": "src:."}


@pytest.mark.parametrize(
    ("exit_code", "stdout", "timed_out", "expected"),
    [
        (0, "15 passed in 1.0s", False, "PASS"),
        (0, "14 passed, 1 skipped in 1.0s", False, "FAIL_SKIPPED"),
        (1, "1 failed, 14 passed", False, "FAIL"),
        (0, "collected 0 items", False, "FAIL_NO_PASS_EVIDENCE"),
        (None, "", True, "TIMEOUT"),
    ],
)
def test_pytest_result_classification_fails_closed(
    exit_code: int | None, stdout: str, timed_out: bool, expected: str
) -> None:
    status, _ = classify_pytest_result(
        exit_code=exit_code, stdout=stdout, stderr="", timed_out=timed_out
    )
    assert status == expected


def test_receipt_hash_detects_tampering() -> None:
    receipt = sign_receipt(
        {
            "schema_version": "promotion_receipt_v1",
            "status": "PASS",
            "membership": {"proof_block_ids": ["a"]},
        }
    )
    verify_receipt(receipt)

    tampered = deepcopy(receipt)
    tampered["status"] = "FAIL"
    with pytest.raises(PromotionError, match="evidence_hash mismatch"):
        verify_receipt(tampered)


def test_dirty_git_state_is_not_promotion_evidence() -> None:
    with pytest.raises(PromotionError, match="pre-run Git state is dirty"):
        require_clean_git({"status": " M governed.py"}, stage="pre-run")


def test_block_capture_uses_files_not_subprocess_pipes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def completed(*args, **kwargs):  # type: ignore[no-untyped-def]
        assert "capture_output" not in kwargs
        assert kwargs["stdout"] is not subprocess.PIPE
        assert kwargs["stderr"] is not subprocess.PIPE
        assert kwargs["start_new_session"] is True
        assert kwargs["env"]["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] == "1"
        kwargs["stdout"].write("1 passed in 0.01s\n")
        return subprocess.CompletedProcess(args[0], 0)

    monkeypatch.setattr(subprocess, "run", completed)
    result = _run_block(
        "file_capture_block",
        "python -c 'print(1)'",
        repo_root=REPO_ROOT,
        timeout_seconds=1,
    )

    assert result["status"] == "PASS"
    assert result["pytest_counts"]["passed"] == 1


def test_block_timeout_is_recorded_as_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def timeout(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise subprocess.TimeoutExpired(cmd=args[0], timeout=1, output="partial")

    monkeypatch.setattr(subprocess, "run", timeout)
    result = _run_block(
        "timed_out_block",
        "python -c 'print(1)'",
        repo_root=REPO_ROOT,
        timeout_seconds=1,
    )

    assert result["status"] == "TIMEOUT"
    assert result["timed_out"] is True
    assert result["exit_code"] is None


def test_makefile_exposes_distinct_membership_check_and_executing_gate() -> None:
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")

    assert ".PHONY: promotion-check" in makefile
    assert ".PHONY: promotion-gate" in makefile
    assert "--check-only" in makefile
    assert "--receipt $(PROMOTION_RECEIPT)" in makefile
    assert "promotion-gate: $(INSTALL_STAMP)" in makefile
