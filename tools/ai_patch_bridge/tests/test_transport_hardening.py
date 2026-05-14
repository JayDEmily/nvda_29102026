from __future__ import annotations

import base64
import gzip
import json
import tempfile
from pathlib import Path

from ai_patch_bridge import core
from ai_patch_bridge import transport_hardening as hardening


def sample_patch(label: str = "blob") -> bytes:
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


def test_inline_payload_still_uses_legacy_parser_path() -> None:
    raw_patch = sample_patch("inline")
    body = hardening.make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/inline-round-trip",
        scope="inline round trip",
        raw_patch=raw_patch,
    )

    def forbidden_runner(command, cwd=None, input_text=None):
        raise AssertionError("inline parsing must not fetch a GitHub blob")

    parsed = hardening.parse_ai_patch_body(body, runner=forbidden_runner)

    assert parsed.raw_patch == raw_patch
    assert parsed.target_branch == "work/inline-round-trip"
    assert "payload_transport:" not in body


def test_auto_transport_keeps_inline_below_threshold() -> None:
    raw_patch = sample_patch("auto_inline")

    def forbidden_runner(command, cwd=None, input_text=None):
        raise AssertionError("small auto payload must not create a GitHub blob")

    body, transport, blob_sha = hardening.build_transport_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/auto-inline",
        scope="auto inline",
        raw_patch=raw_patch,
        inline_gzip_byte_limit=100000,
        runner=forbidden_runner,
    )

    assert transport == "inline"
    assert blob_sha is None
    assert "PAYLOAD_BEGIN" in body
    assert "payload_transport:" not in body
    assert hardening.parse_ai_patch_body(body).raw_patch == raw_patch


def test_github_blob_payload_round_trip() -> None:
    raw_patch = sample_patch()
    gzip_bytes = gzip.compress(raw_patch, mtime=0)
    blob_content = base64.b64encode(gzip_bytes).decode("ascii")
    body = hardening.make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/blob-round-trip",
        scope="blob round trip",
        raw_patch=raw_patch,
        payload_transport="github_blob",
        payload_blob_sha="blob123",
    )

    def fake_runner(command, cwd=None, input_text=None):
        assert command == ["gh", "api", "repos/JayDEmily/NVDAV6/git/blobs/blob123"]
        return completed(list(command), json.dumps({
            "sha": "blob123",
            "encoding": "base64",
            "content": blob_content,
        }))

    parsed = hardening.parse_ai_patch_body(body, runner=fake_runner)

    assert parsed.raw_patch == raw_patch
    assert parsed.metadata["payload_transport"] == "github_blob"
    assert parsed.metadata["payload_blob_sha"] == "blob123"


def test_auto_transport_uses_blob_above_threshold() -> None:
    created: dict[str, bytes] = {}
    raw_patch = sample_patch("auto_blob")

    def fake_runner(command, cwd=None, input_text=None):
        if command == ["gh", "api", "repos/JayDEmily/NVDAV6/git/blobs", "--method", "POST", "--input", "-"]:
            request = json.loads(input_text or "{}")
            created["gzip_bytes"] = base64.b64decode(request["content"])
            return completed(list(command), json.dumps({"sha": "createdblob"}))
        if command == ["gh", "api", "repos/JayDEmily/NVDAV6/git/blobs/createdblob"]:
            return completed(list(command), json.dumps({
                "sha": "createdblob",
                "encoding": "base64",
                "content": base64.b64encode(created["gzip_bytes"]).decode("ascii"),
            }))
        raise AssertionError(command)

    body, transport, blob_sha = hardening.build_transport_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/auto-blob",
        scope="auto blob",
        raw_patch=raw_patch,
        inline_gzip_byte_limit=1,
        runner=fake_runner,
    )

    assert transport == "github_blob"
    assert blob_sha == "createdblob"
    assert "payload_transport: github_blob" in body
    assert hardening.parse_ai_patch_body(body, runner=fake_runner).raw_patch == raw_patch


def test_blob_payload_rejects_hash_mismatch() -> None:
    body = hardening.make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/blob-mismatch",
        scope="blob mismatch",
        raw_patch=sample_patch("expected"),
        payload_transport="github_blob",
        payload_blob_sha="blob123",
    )
    wrong_gzip = gzip.compress(sample_patch("wrong"), mtime=0)

    def fake_runner(command, cwd=None, input_text=None):
        return completed(list(command), json.dumps({
            "sha": "blob123",
            "encoding": "base64",
            "content": base64.b64encode(wrong_gzip).decode("ascii"),
        }))

    assert_raises_regex(
        core.AiPatchError,
        "payload_gzip_sha256 mismatch",
        lambda: hardening.parse_ai_patch_body(body, runner=fake_runner),
    )


def test_transport_equivalence_detects_metadata_mismatch() -> None:
    expected = core.parse_ai_patch_body(core.make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/expected",
        scope="expected",
        raw_patch=sample_patch("expected"),
    ))
    observed = core.parse_ai_patch_body(core.make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/observed",
        scope="expected",
        raw_patch=sample_patch("expected"),
    ))

    assert_raises_regex(
        core.AiPatchError,
        "fetched payload metadata mismatch: target_branch",
        lambda: hardening.assert_transport_equivalent(expected, observed),
    )


def test_submit_patch_and_wait_detects_fetched_comment_mismatch() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        patch_path = Path(tmp_dir_name) / "incoming.patch"
        patch_path.write_bytes(sample_patch("submit_mismatch"))
        posted_bodies: list[str] = []

        def fake_post(repo, issue_number, body, runner=None):
            posted_bodies.append(body)
            return hardening.PostedComment(comment_id=123, body=body)

        def fake_fetch(repo, issue_number, comment_id, runner=None):
            mismatched = posted_bodies[-1].replace(
                "target_branch: work/submit-mismatch",
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
                "fetched payload metadata mismatch: target_branch",
                lambda: hardening.submit_patch_and_wait(
                    repo="JayDEmily/NVDAV6",
                    issue_number=1,
                    base_branch="main",
                    target_branch="work/submit-mismatch",
                    scope="submit mismatch",
                    patch_file=patch_path,
                    executor="local-codex",
                    mode="local_patch_fit_test_commit_push",
                    commit_policy="single_commit",
                    test_policy="required",
                    transport="inline",
                    inline_gzip_byte_limit=100000,
                    timeout_seconds=0,
                    poll_seconds=0,
                ),
            )
        finally:
            hardening.post_issue_comment = old_post  # type: ignore[assignment]
            hardening.fetch_comment_by_id = old_fetch  # type: ignore[assignment]


def test_find_receipt_matches_source_comment_id() -> None:
    comments = [
        core.IssueComment(10, "LOCAL_CODEX_RECEIPT_V1\nsource_comment_id: 99\nstatus: pushed\n"),
        core.IssueComment(11, "LOCAL_CODEX_RECEIPT_V1\nsource_comment_id: 100\nstatus: failed\nreason: no\n"),
    ]

    receipt = hardening.find_receipt(comments, 100)

    assert receipt is not None
    assert receipt.status == "failed"
    assert receipt.receipt_comment_id == 11
    assert receipt.reason == "no"


def test_poll_for_receipt_reports_timeout() -> None:
    def fake_runner(command, cwd=None, input_text=None):
        return completed(list(command), "[]")

    result = hardening.poll_for_receipt(
        "JayDEmily/NVDAV6",
        1,
        123,
        timeout_seconds=0,
        poll_seconds=0,
        runner=fake_runner,
        sleep=lambda seconds: None,
    )

    assert result.status == "timeout"
    assert result.source_comment_id == 123


def test_post_verified_receipt_checks_visibility() -> None:
    posted_bodies: list[str] = []

    def fake_post(repo, issue_number, body, runner=None):
        posted_bodies.append(body)
        return hardening.PostedComment(comment_id=777, body=body)

    def fake_fetch(repo, issue_number, comment_id, runner=None):
        return core.IssueComment(comment_id, posted_bodies[-1])

    old_post = hardening.post_issue_comment
    old_fetch = hardening.fetch_comment_by_id
    try:
        hardening.post_issue_comment = fake_post  # type: ignore[assignment]
        hardening.fetch_comment_by_id = fake_fetch  # type: ignore[assignment]
        hardening.post_verified_receipt(
            core.BridgeConfig(repo="JayDEmily/NVDAV6", issue_number=1),
            456,
            status="pushed",
            body_lines=["target_branch: work/demo"],
        )
    finally:
        hardening.post_issue_comment = old_post  # type: ignore[assignment]
        hardening.fetch_comment_by_id = old_fetch  # type: ignore[assignment]

    assert "source_comment_id: 456" in posted_bodies[-1]
    assert "status: pushed" in posted_bodies[-1]


def test_post_verified_receipt_raises_when_fetched_receipt_mismatches() -> None:
    def fake_post(repo, issue_number, body, runner=None):
        return hardening.PostedComment(comment_id=777, body=body)

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
