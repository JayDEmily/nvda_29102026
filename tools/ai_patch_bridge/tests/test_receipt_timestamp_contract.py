from __future__ import annotations

from datetime import datetime, timezone

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


def test_receipt_timestamp_lines_use_melbourne_aest_after_daylight_saving_ends() -> None:
    fixed_utc = datetime(2026, 4, 30, 4, 17, 0, tzinfo=timezone.utc)

    lines = hardening.receipt_timestamp_lines(fixed_utc)

    assert lines == [
        "computer_unix_epoch_s: 1777522620",
        "computer_utc_minute: 2026-04-30T04:17Z",
        "human_melbourne_minute: 30-04-2026 14:17 AEST",
        "human_timezone: Australia/Melbourne",
        "human_utc_offset: UTC+10",
    ]


def test_receipt_timestamp_lines_use_melbourne_aedt_during_daylight_saving() -> None:
    fixed_utc = datetime(2026, 1, 15, 2, 5, 0, tzinfo=timezone.utc)

    lines = hardening.receipt_timestamp_lines(fixed_utc)

    assert "human_melbourne_minute: 15-01-2026 13:05 AEDT" in lines
    assert "human_utc_offset: UTC+11" in lines


def test_post_verified_receipt_includes_timestamp_and_check_contract_fields() -> None:
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

    body = posted_bodies[-1]
    assert "computer_unix_epoch_s: " in body
    assert "computer_utc_minute: " in body
    assert "human_melbourne_minute: " in body
    assert "human_timezone: Australia/Melbourne" in body
    assert "human_utc_offset: UTC+" in body
    assert "checks_run: unknown" in body
    assert "check_outcome: unknown" in body


def test_post_verified_receipt_requires_visible_melbourne_timezone() -> None:
    def fake_post(repo, issue_number, body, runner=None):
        return hardening.PostedComment(comment_id=777, body=body)

    def fake_fetch(repo, issue_number, comment_id, runner=None):
        return core.IssueComment(
            comment_id,
            "LOCAL_CODEX_RECEIPT_V1\nsource_comment_id: 456\nstatus: pushed\n",
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
