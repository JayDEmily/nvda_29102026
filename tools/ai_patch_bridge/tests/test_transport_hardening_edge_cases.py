from __future__ import annotations

import base64
import json
import tempfile
from pathlib import Path

from ai_patch_bridge import core
from ai_patch_bridge import transport_hardening as hardening


def sample_patch(label: str = "edge") -> bytes:
    return (
        f"diff --git a/{label}.txt b/{label}.txt\n"
        f"--- a/{label}.txt\n"
        f"+++ b/{label}.txt\n"
        "@@ -1 +1 @@\n"
        "-old\n"
        "+new\n"
    ).encode("utf-8")


def completed(command: list[str], stdout: str):
    return core.subprocess.CompletedProcess(command, 0, stdout, "")


def assert_raises_regex(exc_type: type[BaseException], pattern: str, func):
    try:
        func()
    except exc_type as exc:
        if pattern not in str(exc):
            raise AssertionError(f"expected {pattern!r} in {exc!r}") from exc
        return
    raise AssertionError(f"expected {exc_type.__name__}")


def test_invalid_transport_is_rejected() -> None:
    assert_raises_regex(
        core.AiPatchError,
        "unsupported payload_transport",
        lambda: hardening.build_transport_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="work/bad-transport",
            scope="bad transport",
            raw_patch=sample_patch(),
            transport="carrier-pigeon",
        ),
    )


def test_missing_blob_sha_is_rejected() -> None:
    assert_raises_regex(
        core.AiPatchError,
        "payload_blob_sha is required",
        lambda: hardening.make_ai_patch_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="work/missing-blob-sha",
            scope="missing blob sha",
            raw_patch=sample_patch(),
            payload_transport="github_blob",
        ),
    )


def test_blob_fetch_rejects_wrong_sha() -> None:
    def fake_runner(command, cwd=None, input_text=None):
        return completed(list(command), json.dumps({
            "sha": "wrong-sha",
            "encoding": "base64",
            "content": base64.b64encode(b"payload").decode("ascii"),
        }))

    assert_raises_regex(
        core.AiPatchError,
        "GitHub blob SHA mismatch",
        lambda: hardening.fetch_github_blob_payload("JayDEmily/NVDAV6", "expected-sha", fake_runner),
    )


def test_blob_fetch_rejects_wrong_encoding() -> None:
    def fake_runner(command, cwd=None, input_text=None):
        return completed(list(command), json.dumps({
            "sha": "blob-sha",
            "encoding": "utf-8",
            "content": "not the expected encoding",
        }))

    assert_raises_regex(
        core.AiPatchError,
        "GitHub blob encoding must be base64",
        lambda: hardening.fetch_github_blob_payload("JayDEmily/NVDAV6", "blob-sha", fake_runner),
    )


def test_find_receipt_ignores_wrong_source_and_returns_newest_match() -> None:
    comments = [
        core.IssueComment(10, "LOCAL_CODEX_RECEIPT_V1\nsource_comment_id: 99\nstatus: pushed\n"),
        core.IssueComment(11, "LOCAL_CODEX_RECEIPT_V1\nsource_comment_id: 100\nstatus: failed\n"),
        core.IssueComment(12, "LOCAL_CODEX_RECEIPT_V1\nsource_comment_id: 100\nstatus: pushed\n"),
    ]

    receipt = hardening.find_receipt(comments, 100)

    assert receipt is not None
    assert receipt.status == "pushed"
    assert receipt.receipt_comment_id == 12


def test_submit_patch_and_wait_returns_timeout_distinctly() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        patch_path = Path(tmp_dir_name) / "incoming.patch"
        patch_path.write_bytes(sample_patch("submit_timeout"))
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
            result = hardening.submit_patch_and_wait(
                repo="JayDEmily/NVDAV6",
                issue_number=1,
                base_branch="main",
                target_branch="work/submit-timeout",
                scope="submit timeout",
                patch_file=patch_path,
                executor="local-codex",
                mode="local_patch_fit_test_commit_push",
                commit_policy="single_commit",
                test_policy="required",
                transport="inline",
                inline_gzip_byte_limit=100000,
                timeout_seconds=0,
                poll_seconds=0,
                runner=fake_runner,
                sleep=lambda seconds: None,
            )
        finally:
            hardening.post_issue_comment = old_post  # type: ignore[assignment]
            hardening.fetch_comment_by_id = old_fetch  # type: ignore[assignment]

    assert result["transport_verified"] is True
    assert result["receipt_status"] == "timeout"
    assert result["receipt_comment_id"] is None


def test_post_verified_receipt_retries_before_failure() -> None:
    attempts = 0

    def fake_post(repo, issue_number, body, runner=None):
        nonlocal attempts
        attempts += 1
        return hardening.PostedComment(comment_id=attempts, body=body)

    def fake_fetch(repo, issue_number, comment_id, runner=None):
        return core.IssueComment(
            comment_id,
            "LOCAL_CODEX_RECEIPT_V1\nsource_comment_id: 456\nstatus: stopped\n",
        )

    old_post = hardening.post_issue_comment
    old_fetch = hardening.fetch_comment_by_id
    old_sleep = hardening.time.sleep
    try:
        hardening.post_issue_comment = fake_post  # type: ignore[assignment]
        hardening.fetch_comment_by_id = fake_fetch  # type: ignore[assignment]
        hardening.time.sleep = lambda seconds: None  # type: ignore[assignment]
        assert_raises_regex(
            core.AiPatchError,
            "receipt_post_failed",
            lambda: hardening.post_verified_receipt(
                core.BridgeConfig(repo="JayDEmily/NVDAV6", issue_number=1),
                456,
                status="pushed",
                body_lines=["target_branch: work/demo"],
            ),
        )
    finally:
        hardening.post_issue_comment = old_post  # type: ignore[assignment]
        hardening.fetch_comment_by_id = old_fetch  # type: ignore[assignment]
        hardening.time.sleep = old_sleep  # type: ignore[assignment]

    assert attempts == hardening.RECEIPT_POST_ATTEMPTS


def test_cli_submit_and_wait_route_delegates_to_submitter() -> None:
    calls = []

    def fake_submit_patch_and_wait(**kwargs):
        calls.append(kwargs)
        return {
            "submitted": True,
            "transport_verified": True,
            "transport": kwargs["transport"],
            "payload_blob_sha": None,
            "comment_id": 123,
            "target_branch": kwargs["target_branch"],
            "receipt_status": "timeout",
            "receipt_comment_id": None,
            "receipt_reason": "test timeout",
        }

    old_submit = hardening.submit_patch_and_wait
    try:
        hardening.submit_patch_and_wait = fake_submit_patch_and_wait  # type: ignore[assignment]
        rc = hardening.main([
            "submit-and-wait",
            "--repo",
            "JayDEmily/NVDAV6",
            "--issue-number",
            "1",
            "--target-branch",
            "work/cli-submit",
            "--scope",
            "cli submit",
            "--patch-file",
            __file__,
            "--transport",
            "inline",
            "--timeout-seconds",
            "0",
        ])
    finally:
        hardening.submit_patch_and_wait = old_submit  # type: ignore[assignment]

    assert rc == 1
    assert calls[0]["target_branch"] == "work/cli-submit"
    assert calls[0]["transport"] == "inline"
