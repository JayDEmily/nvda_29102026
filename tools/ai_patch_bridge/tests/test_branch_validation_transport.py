from __future__ import annotations

import tempfile
from pathlib import Path

from ai_patch_bridge import core
from ai_patch_bridge import transport_hardening as hardening


def assert_raises_regex(exc_type: type[BaseException], pattern: str, func):
    try:
        func()
    except exc_type as exc:
        if pattern not in str(exc):
            raise AssertionError(f"expected {pattern!r} in {exc!r}") from exc
        return
    raise AssertionError(f"expected {exc_type.__name__}")


def completed(command: list[str], stdout: str):
    return core.subprocess.CompletedProcess(command, 0, stdout, "")


def test_branch_validation_comment_round_trip() -> None:
    body = hardening.make_branch_validation_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/branch-payload",
        source_pr=14,
        checks_required="make test, make lint",
    )

    parsed = hardening.parse_branch_validation_body(body)

    assert parsed.repo == "JayDEmily/NVDAV6"
    assert parsed.base_branch == "main"
    assert parsed.target_branch == "work/branch-payload"
    assert parsed.source_pr == "14"
    assert parsed.validation_mode == "branch_checkout_test_repair_receipt"
    assert parsed.checks_required == "make test, make lint"


def test_branch_validation_rejects_non_work_target_branch() -> None:
    assert_raises_regex(
        core.AiPatchError,
        "target_branch must start with work/",
        lambda: hardening.make_branch_validation_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="main",
        ),
    )


def test_branch_validation_rejects_missing_target_branch_metadata() -> None:
    body = "\n".join([
        "LOCAL_BRANCH_VALIDATE_V1",
        "repo: JayDEmily/NVDAV6",
        "base_branch: main",
        "validation_mode: branch_checkout_test_repair_receipt",
        "",
    ])

    assert_raises_regex(
        core.AiPatchError,
        "missing required metadata: target_branch",
        lambda: hardening.parse_branch_validation_body(body),
    )


def test_branch_validation_rejects_unsupported_mode() -> None:
    assert_raises_regex(
        core.AiPatchError,
        "unsupported validation_mode",
        lambda: hardening.make_branch_validation_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="work/bad-mode",
            validation_mode="just-wing-it",
        ),
    )


def test_branch_validation_equivalence_detects_fetched_mismatch() -> None:
    expected = hardening.parse_branch_validation_body(hardening.make_branch_validation_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/expected-branch",
    ))
    observed = hardening.parse_branch_validation_body(hardening.make_branch_validation_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/observed-branch",
    ))

    assert_raises_regex(
        core.AiPatchError,
        "fetched branch validation metadata mismatch: target_branch",
        lambda: hardening.assert_branch_validation_equivalent(expected, observed),
    )


def test_submit_branch_validation_and_wait_detects_fetched_mismatch() -> None:
    posted_bodies: list[str] = []

    def fake_post(repo, issue_number, body, runner=None):
        posted_bodies.append(body)
        return hardening.PostedComment(comment_id=123, body=body)

    def fake_fetch(repo, issue_number, comment_id, runner=None):
        mismatched = posted_bodies[-1].replace(
            "target_branch: work/branch-validate",
            "target_branch: work/other-branch",
        )
        return core.IssueComment(comment_id, mismatched)

    old_post = hardening.post_issue_comment
    old_fetch = hardening.fetch_comment_by_id
    try:
        hardening.post_issue_comment = fake_post  # type: ignore[assignment]
        hardening.fetch_comment_by_id = fake_fetch  # type: ignore[assignment]
        assert_raises_regex(
            core.AiPatchError,
            "fetched branch validation metadata mismatch: target_branch",
            lambda: hardening.submit_branch_validation_and_wait(
                repo="JayDEmily/NVDAV6",
                issue_number=1,
                base_branch="main",
                target_branch="work/branch-validate",
                source_pr=14,
                checks_required="default",
                timeout_seconds=0,
                poll_seconds=0,
            ),
        )
    finally:
        hardening.post_issue_comment = old_post  # type: ignore[assignment]
        hardening.fetch_comment_by_id = old_fetch  # type: ignore[assignment]


def test_submit_branch_validation_and_wait_returns_timeout_distinctly() -> None:
    posted_bodies: list[str] = []

    def fake_post(repo, issue_number, body, runner=None):
        posted_bodies.append(body)
        return hardening.PostedComment(comment_id=123, body=body)

    def fake_fetch(repo, issue_number, comment_id, runner=None):
        return core.IssueComment(comment_id, posted_bodies[-1])

    def fake_runner(command, cwd=None, input_text=None):
        return completed(list(command), "[]")

    old_post = hardening.post_issue_comment
    old_fetch = hardening.fetch_comment_by_id
    try:
        hardening.post_issue_comment = fake_post  # type: ignore[assignment]
        hardening.fetch_comment_by_id = fake_fetch  # type: ignore[assignment]
        result = hardening.submit_branch_validation_and_wait(
            repo="JayDEmily/NVDAV6",
            issue_number=1,
            base_branch="main",
            target_branch="work/branch-timeout",
            source_pr=14,
            checks_required="default",
            timeout_seconds=0,
            poll_seconds=0,
            runner=fake_runner,
            sleep=lambda seconds: None,
        )
    finally:
        hardening.post_issue_comment = old_post  # type: ignore[assignment]
        hardening.fetch_comment_by_id = old_fetch  # type: ignore[assignment]

    assert result["control_verified"] is True
    assert result["control"] == "LOCAL_BRANCH_VALIDATE_V1"
    assert result["receipt_status"] == "timeout"
    assert result["receipt_comment_id"] is None


def test_cli_validate_branch_and_wait_route_delegates_to_submitter() -> None:
    calls = []

    def fake_submit_branch_validation_and_wait(**kwargs):
        calls.append(kwargs)
        return {
            "submitted": True,
            "control_verified": True,
            "control": "LOCAL_BRANCH_VALIDATE_V1",
            "comment_id": 123,
            "target_branch": kwargs["target_branch"],
            "source_pr": kwargs["source_pr"],
            "receipt_status": "timeout",
            "receipt_comment_id": None,
            "receipt_reason": "test timeout",
        }

    old_submit = hardening.submit_branch_validation_and_wait
    try:
        hardening.submit_branch_validation_and_wait = fake_submit_branch_validation_and_wait  # type: ignore[assignment]
        rc = hardening.main([
            "validate-branch-and-wait",
            "--repo",
            "JayDEmily/NVDAV6",
            "--issue-number",
            "1",
            "--target-branch",
            "work/cli-branch-validate",
            "--source-pr",
            "14",
            "--checks-required",
            "default",
            "--timeout-seconds",
            "0",
        ])
    finally:
        hardening.submit_branch_validation_and_wait = old_submit  # type: ignore[assignment]

    assert rc == 1
    assert calls[0]["target_branch"] == "work/cli-branch-validate"
    assert calls[0]["source_pr"] == "14"


def test_watcher_consumes_branch_validation_comment_and_posts_checked_receipt() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        body = hardening.make_branch_validation_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="work/watcher-branch-validate",
            source_pr=14,
        )
        comment = core.IssueComment(501, body, user_login="JayDEmily")
        config = core.BridgeConfig(
            repo="JayDEmily/NVDAV6",
            issue_number=1,
            repo_root=tmp_dir,
            state_dir=Path("state"),
            runs_dir=Path("runs"),
            local_checks=("make check",),
            dry_run=True,
        )
        commands: list[list[str]] = []
        checks: list[str] = []

        def fake_fetch_issue_comments(repo, issue_number, runner=None):
            return [comment]

        def fake_run_command(command, cwd=None, input_text=None):
            commands.append(list(command))
            stdout = "abc123\n" if command == ["git", "rev-parse", "HEAD"] else ""
            return completed(list(command), stdout)

        def fake_subprocess_run(command, cwd=None, shell=None, text=None, capture_output=None, check=None, input=None):
            checks.append(command)
            return core.subprocess.CompletedProcess(command, 0, "ok\n", "")

        old_fetch = core.fetch_issue_comments
        old_run_command = core.run_command
        old_subprocess_run = core.subprocess.run
        try:
            hardening.install()
            core.fetch_issue_comments = fake_fetch_issue_comments  # type: ignore[assignment]
            core.run_command = fake_run_command  # type: ignore[assignment]
            core.subprocess.run = fake_subprocess_run  # type: ignore[assignment]
            assert core.run_once(config) == 0
        finally:
            core.fetch_issue_comments = old_fetch  # type: ignore[assignment]
            core.run_command = old_run_command  # type: ignore[assignment]
            core.subprocess.run = old_subprocess_run  # type: ignore[assignment]

        assert commands == [
            ["git", "fetch", "--prune", "origin"],
            ["git", "status", "--short"],
            ["git", "rev-parse", "--verify", "origin/work/watcher-branch-validate^{commit}"],
            ["git", "switch", "--detach", "origin/work/watcher-branch-validate"],
            ["git", "rev-parse", "HEAD"],
        ]
        assert checks == ["make check"]
        receipt = (tmp_dir / "runs" / "501" / "github_receipt.md").read_text(encoding="utf-8")
        assert "LOCAL_CODEX_RECEIPT_V1" in receipt
        assert "status: checked" in receipt
        assert "target_branch: work/watcher-branch-validate" in receipt
        assert "head_sha: abc123" in receipt
        assert 'checks_run: ["make check"]' in receipt
        assert "check_outcome: passed" in receipt
        assert f"run_dir: {tmp_dir / 'runs' / '501'}" in receipt
        assert "human_melbourne_minute:" in receipt


def test_branch_validation_check_failure_posts_stopped_receipt() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        body = hardening.make_branch_validation_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="work/check-fails",
        )
        comment = core.IssueComment(502, body, user_login="JayDEmily")
        config = core.BridgeConfig(
            repo="JayDEmily/NVDAV6",
            issue_number=1,
            repo_root=tmp_dir,
            state_dir=Path("state"),
            runs_dir=Path("runs"),
            local_checks=("make fail",),
            dry_run=True,
        )

        def fake_run_command(command, cwd=None, input_text=None):
            stdout = "def456\n" if command == ["git", "rev-parse", "HEAD"] else ""
            return completed(list(command), stdout)

        def fake_subprocess_run(command, cwd=None, shell=None, text=None, capture_output=None, check=None, input=None):
            return core.subprocess.CompletedProcess(command, 2, "", "no\n")

        old_run_command = core.run_command
        old_subprocess_run = core.subprocess.run
        try:
            hardening.install()
            core.run_command = fake_run_command  # type: ignore[assignment]
            core.subprocess.run = fake_subprocess_run  # type: ignore[assignment]
            hardening.process_branch_validation_comment(comment, config)
        finally:
            core.run_command = old_run_command  # type: ignore[assignment]
            core.subprocess.run = old_subprocess_run  # type: ignore[assignment]

        receipt = (tmp_dir / "runs" / "502" / "github_receipt.md").read_text(encoding="utf-8")
        assert "status: stopped" in receipt
        assert "target_branch: work/check-fails" in receipt
        assert "head_sha: def456" in receipt
        assert 'checks_run: ["make fail"]' in receipt
        assert "check_outcome: failed" in receipt
        assert "failed_check: make fail" in receipt


def test_watcher_rejects_dirty_branch_validation_worktree() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        body = hardening.make_branch_validation_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="work/dirty-rejected",
        )
        comment = core.IssueComment(503, body, user_login="JayDEmily")
        config = core.BridgeConfig(
            repo="JayDEmily/NVDAV6",
            issue_number=1,
            repo_root=tmp_dir,
            state_dir=Path("state"),
            runs_dir=Path("runs"),
            dry_run=True,
        )
        commands: list[list[str]] = []

        def fake_fetch_issue_comments(repo, issue_number, runner=None):
            return [comment]

        def fake_run_command(command, cwd=None, input_text=None):
            commands.append(list(command))
            stdout = " M dirty.txt\n" if command == ["git", "status", "--short"] else ""
            return completed(list(command), stdout)

        old_fetch = core.fetch_issue_comments
        old_run_command = core.run_command
        try:
            hardening.install()
            core.fetch_issue_comments = fake_fetch_issue_comments  # type: ignore[assignment]
            core.run_command = fake_run_command  # type: ignore[assignment]
            assert core.run_once(config) == 1
        finally:
            core.fetch_issue_comments = old_fetch  # type: ignore[assignment]
            core.run_command = old_run_command  # type: ignore[assignment]

        assert commands == [
            ["git", "fetch", "--prune", "origin"],
            ["git", "status", "--short"],
        ]
        receipt = (tmp_dir / "runs" / "503" / "github_receipt.md").read_text(encoding="utf-8")
        assert "status: failed" in receipt
        assert "reason: working tree is not clean" in receipt
