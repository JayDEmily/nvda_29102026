from __future__ import annotations

import json
import tempfile
from pathlib import Path

from ai_patch_bridge import core
from ai_patch_bridge import receipt_failure_hardening as hardening
from ai_patch_bridge import transport_hardening as transport


def completed(command: list[str], stdout: str = ""):
    return core.subprocess.CompletedProcess(command, 0, stdout, "")


def test_post_verified_receipt_writes_attempted_receipt_and_failure_state() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        config = core.BridgeConfig(
            repo="JayDEmily/NVDAV6",
            issue_number=1,
            repo_root=tmp_dir,
            state_dir=Path("state"),
            runs_dir=Path("runs"),
        )

        def fake_post_issue_comment(repo, issue_number, body, runner=None):
            raise core.AiPatchError("simulated github outage")

        old_post = transport.post_issue_comment
        try:
            transport.post_issue_comment = fake_post_issue_comment  # type: ignore[assignment]
            try:
                hardening.post_verified_receipt(
                    config,
                    777,
                    status="checked",
                    body_lines=[
                        "target_branch: work/example",
                        "checks_run: [\"make scaffold-check\"]",
                        "check_outcome: passed",
                    ],
                )
            except core.AiPatchError as exc:
                assert "receipt_post_failed" in str(exc)
            else:
                raise AssertionError("expected receipt post failure")
        finally:
            transport.post_issue_comment = old_post  # type: ignore[assignment]

        run_dir = tmp_dir / "runs" / "777"
        receipt = (run_dir / "github_receipt.md").read_text(encoding="utf-8")
        state = json.loads((run_dir / "receipt_post_state.json").read_text(encoding="utf-8"))

        assert "LOCAL_CODEX_RECEIPT_V1" in receipt
        assert "source_comment_id: 777" in receipt
        assert "status: checked" in receipt
        assert "target_branch: work/example" in receipt
        assert state["status"] == "receipt_post_failed"
        assert state["ledger_status"] == "processed_receipt_post_failed"
        assert "simulated github outage" in state["reason"]


def test_run_once_marks_receipt_post_failure_as_distinct_ledger_status() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        body = transport.make_branch_validation_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="work/receipt-post-fails",
            source_pr=14,
        )
        comment = core.IssueComment(778, body, user_login="JayDEmily")
        config = core.BridgeConfig(
            repo="JayDEmily/NVDAV6",
            issue_number=1,
            repo_root=tmp_dir,
            state_dir=Path("state"),
            runs_dir=Path("runs"),
            local_checks=("make scaffold-check",),
        )

        def fake_fetch_issue_comments(repo, issue_number, runner=None):
            return [comment]

        def fake_run_command(command, cwd=None, input_text=None):
            stdout = "abc123\n" if command == ["git", "rev-parse", "HEAD"] else ""
            return completed(list(command), stdout)

        def fake_subprocess_run(command, cwd=None, shell=None, text=None, capture_output=None, check=None, input=None):
            return core.subprocess.CompletedProcess(command, 0, "repo scaffold present\n", "")

        def fake_post_issue_comment(repo, issue_number, body, runner=None):
            raise core.AiPatchError("simulated github outage")

        old_fetch = core.fetch_issue_comments
        old_run_command = core.run_command
        old_subprocess_run = core.subprocess.run
        old_post = transport.post_issue_comment
        old_core_run_once = core.run_once
        try:
            hardening.install()
            core.fetch_issue_comments = fake_fetch_issue_comments  # type: ignore[assignment]
            core.run_command = fake_run_command  # type: ignore[assignment]
            core.subprocess.run = fake_subprocess_run  # type: ignore[assignment]
            transport.post_issue_comment = fake_post_issue_comment  # type: ignore[assignment]
            assert hardening.run_once(config) == 1
        finally:
            core.fetch_issue_comments = old_fetch  # type: ignore[assignment]
            core.run_command = old_run_command  # type: ignore[assignment]
            core.subprocess.run = old_subprocess_run  # type: ignore[assignment]
            transport.post_issue_comment = old_post  # type: ignore[assignment]
            core.run_once = old_core_run_once  # type: ignore[assignment]

        processed = json.loads((tmp_dir / "state" / "processed_comments.json").read_text(encoding="utf-8"))
        state = json.loads((tmp_dir / "runs" / "778" / "receipt_post_state.json").read_text(encoding="utf-8"))

        assert processed["778"]["status"] == "processed_receipt_post_failed"
        assert "receipt_post_failed" in processed["778"]["reason"]
        assert state["ledger_status"] == "processed_receipt_post_failed"
        assert (tmp_dir / "runs" / "778" / "github_receipt.md").exists()


def test_run_once_empty_queue_mentions_both_supported_comment_types() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        config = core.BridgeConfig(
            repo="JayDEmily/NVDAV6",
            issue_number=1,
            repo_root=tmp_dir,
            state_dir=Path("state"),
            runs_dir=Path("runs"),
        )

        def fake_fetch_issue_comments(repo, issue_number, runner=None):
            return []

        old_fetch = core.fetch_issue_comments
        try:
            core.fetch_issue_comments = fake_fetch_issue_comments  # type: ignore[assignment]
            assert hardening.run_once(config) == 0
        finally:
            core.fetch_issue_comments = old_fetch  # type: ignore[assignment]
