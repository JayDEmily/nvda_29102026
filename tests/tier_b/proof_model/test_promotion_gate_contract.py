from __future__ import annotations

import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
import scripts.run_promotion_gate as promotion_gate
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


def test_live_alpha_gate_resolves_exact_membership_without_execution() -> None:
    summary = build_check_summary("alpha_current", repo_root=REPO_ROOT)

    assert len(summary["proof_block_ids"]) == 17
    assert len(summary["test_family_ids"]) == 17
    assert len(summary["test_paths"]) == 19
    assert summary["test_paths"][0].startswith("tests/tier_a/")


def test_promotion_cli_default_is_current_semantic_key() -> None:
    source = (REPO_ROOT / "scripts/run_promotion_gate.py").read_text(encoding="utf-8")
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")

    assert 'default="alpha_current"' in source
    assert "PROMOTION_SET ?= alpha_current" in makefile


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


class _FakeProcess:
    def __init__(self, *, exit_code: int = 0, times_out: bool = False) -> None:
        self.pid = 2_147_000_000
        self._exit_code = exit_code
        self._times_out = times_out
        self.returncode: int | None = None

    def wait(self, timeout: int | None = None) -> int:
        if self._times_out and self.returncode is None:
            raise subprocess.TimeoutExpired(cmd="fake", timeout=timeout)
        self.returncode = self._exit_code
        return self._exit_code

    def poll(self) -> int | None:
        return self.returncode

    def kill(self) -> None:
        self.returncode = -9


def test_block_capture_uses_files_not_subprocess_pipes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def popen(*args, **kwargs):  # type: ignore[no-untyped-def]
        assert "capture_output" not in kwargs
        assert kwargs["stdout"] is not subprocess.PIPE
        assert kwargs["stderr"] is not subprocess.PIPE
        assert kwargs["start_new_session"] is True
        assert kwargs["env"]["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] == "1"
        kwargs["stdout"].write("1 passed in 0.01s\n")
        return _FakeProcess()

    monkeypatch.setattr(subprocess, "Popen", popen)
    monkeypatch.setattr(promotion_gate, "_terminate_process_group", lambda _pid: False)
    result = _run_block(
        "file_capture_block",
        "python -c 'print(1)'",
        repo_root=REPO_ROOT,
        timeout_seconds=1,
    )

    assert result["status"] == "PASS"
    assert result["pytest_counts"]["passed"] == 1
    assert result["residual_process_group_terminated"] is False


def test_block_timeout_is_recorded_as_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: _FakeProcess(times_out=True))
    monkeypatch.setattr(promotion_gate, "_terminate_process_group", lambda _pid: True)
    result = _run_block(
        "timed_out_block",
        "python -c 'print(1)'",
        repo_root=REPO_ROOT,
        timeout_seconds=1,
    )

    assert result["status"] == "TIMEOUT"
    assert result["timed_out"] is True
    assert result["residual_process_group_terminated"] is True


def test_residual_process_group_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    def popen(*args, **kwargs):  # type: ignore[no-untyped-def]
        kwargs["stdout"].write("1 passed in 0.01s\n")
        return _FakeProcess()

    monkeypatch.setattr(subprocess, "Popen", popen)
    monkeypatch.setattr(promotion_gate, "_terminate_process_group", lambda _pid: True)
    result = _run_block(
        "residual_process_block",
        "python -c 'print(1)'",
        repo_root=REPO_ROOT,
        timeout_seconds=1,
    )

    assert result["status"] == "FAIL_RESIDUAL_PROCESS"
    assert result["residual_process_group_terminated"] is True


def test_makefile_exposes_distinct_membership_check_and_executing_gate() -> None:
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")

    assert ".PHONY: promotion-check" in makefile
    assert ".PHONY: promotion-gate" in makefile
    assert "--check-only" in makefile
    assert "--receipt $(PROMOTION_RECEIPT)" in makefile
    assert "promotion-gate: $(INSTALL_STAMP)" in makefile
