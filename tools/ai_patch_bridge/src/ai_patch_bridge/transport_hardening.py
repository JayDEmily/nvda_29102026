"""Transport and receipt hardening overlay for the AI Patch Bridge.

This module keeps the existing bridge core intact and installs a narrow runtime
overlay for safer payload transport and verified receipt posting.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import sys
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from ai_patch_bridge import core

INLINE_PAYLOAD_TRANSPORT = "inline"
GITHUB_BLOB_PAYLOAD_TRANSPORT = "github_blob"
AUTO_PAYLOAD_TRANSPORT = "auto"
DEFAULT_INLINE_GZIP_BYTE_LIMIT = 4096
RECEIPT_POST_ATTEMPTS = 3
MELBOURNE_TIMEZONE = "Australia/Melbourne"
BRANCH_VALIDATE_HEADER = "LOCAL_BRANCH_VALIDATE_V1"
BRANCH_VALIDATE_MODE = "branch_checkout_test_repair_receipt"

_CORE_PARSE_AI_PATCH_BODY = core.parse_ai_patch_body
_CORE_MAKE_AI_PATCH_COMMENT = core.make_ai_patch_comment
_CORE_PROCESS_COMMENT = core.process_comment
_CORE_SHOULD_PROCESS_COMMENT = core._should_process_comment  # type: ignore[attr-defined]
_INSTALLED = False


@dataclass(frozen=True, slots=True)
class PostedComment:
    """GitHub issue comment returned after posting a submitted patch."""

    comment_id: int
    body: str
    url: str | None = None


@dataclass(frozen=True, slots=True)
class ReceiptPollResult:
    """Result returned by receipt polling."""

    status: str
    source_comment_id: int
    receipt_comment_id: int | None = None
    body: str | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class BranchValidationRequest:
    """Parsed LOCAL_BRANCH_VALIDATE_V1 request for branch-as-payload validation."""

    metadata: dict[str, str]

    @property
    def repo(self) -> str:
        return self.metadata["repo"]

    @property
    def base_branch(self) -> str:
        return self.metadata["base_branch"]

    @property
    def target_branch(self) -> str:
        return self.metadata["target_branch"]

    @property
    def source_pr(self) -> str | None:
        value = self.metadata.get("source_pr")
        return value if value else None

    @property
    def validation_mode(self) -> str:
        return self.metadata["validation_mode"]

    @property
    def checks_required(self) -> str:
        return self.metadata.get("checks_required", "default")


CommandRunner = Callable[
    [Sequence[str], Path | None, str | None],
    core.subprocess.CompletedProcess[str],
]
SleepFunc = Callable[[float], None]


def install() -> None:
    """Install hardening hooks into the legacy core module."""

    global _INSTALLED
    if _INSTALLED:
        return
    core.parse_ai_patch_body = parse_ai_patch_body  # type: ignore[assignment]
    core.make_ai_patch_comment = make_ai_patch_comment  # type: ignore[assignment]
    core._post_receipt = post_verified_receipt  # type: ignore[attr-defined]
    core._should_process_comment = should_process_comment  # type: ignore[attr-defined]
    core.process_comment = process_comment  # type: ignore[assignment]
    _INSTALLED = True


def parse_ai_patch_body(body: str, runner: CommandRunner | None = None) -> core.AiPatchMessage:
    """Parse inline or GitHub-blob AI_PATCH_V1 payloads."""

    metadata = core._parse_metadata(body)  # type: ignore[attr-defined]
    payload_transport = metadata.get("payload_transport", INLINE_PAYLOAD_TRANSPORT)
    if payload_transport in ("", INLINE_PAYLOAD_TRANSPORT):
        return _CORE_PARSE_AI_PATCH_BODY(body)
    if payload_transport != GITHUB_BLOB_PAYLOAD_TRANSPORT:
        raise core.AiPatchError(f"unsupported payload_transport: {payload_transport!r}")

    _validate_blob_metadata(body, metadata)
    blob_sha = metadata["payload_blob_sha"]
    gzip_bytes = fetch_github_blob_payload(metadata["repo"], blob_sha, runner=runner)
    return _message_from_gzip_bytes(metadata, gzip_bytes)


def make_ai_patch_comment(
    *,
    repo: str,
    base_branch: str,
    target_branch: str,
    scope: str,
    raw_patch: bytes,
    executor: str = core.LOCAL_CODEX_EXECUTOR,
    mode: str = "local_patch_fit_test_commit_push",
    commit_policy: str = "single_commit",
    test_policy: str = "required",
    payload_transport: str = INLINE_PAYLOAD_TRANSPORT,
    payload_blob_sha: str | None = None,
) -> str:
    """Build an AI_PATCH_V1 body for inline or GitHub-blob transport."""

    if payload_transport in ("", INLINE_PAYLOAD_TRANSPORT):
        return _CORE_MAKE_AI_PATCH_COMMENT(
            repo=repo,
            base_branch=base_branch,
            target_branch=target_branch,
            scope=scope,
            raw_patch=raw_patch,
            executor=executor,
            mode=mode,
            commit_policy=commit_policy,
            test_policy=test_policy,
        )
    if payload_transport != GITHUB_BLOB_PAYLOAD_TRANSPORT:
        raise core.AiPatchError(f"unsupported payload_transport: {payload_transport!r}")
    if not payload_blob_sha:
        raise core.AiPatchError("payload_blob_sha is required for github_blob transport")

    metadata = {
        "executor": executor,
        "commit_policy": commit_policy,
        "test_policy": test_policy,
        "target_branch": target_branch,
    }
    core._validate_branch("base_branch", base_branch, required_prefix=None)  # type: ignore[attr-defined]
    core._validate_policy_metadata(metadata)  # type: ignore[attr-defined]
    core._validate_target_branch_for_executor(metadata)  # type: ignore[attr-defined]

    gzip_bytes = gzip.compress(raw_patch, mtime=0)
    return "\n".join(
        [
            core.AI_PATCH_HEADER,
            f"repo: {repo}",
            f"base_branch: {base_branch}",
            f"target_branch: {target_branch}",
            f"scope: {scope}",
            f"executor: {executor}",
            f"mode: {mode}",
            f"commit_policy: {commit_policy}",
            f"test_policy: {test_policy}",
            "",
            "payload_encoding: base64+gzip",
            f"payload_transport: {GITHUB_BLOB_PAYLOAD_TRANSPORT}",
            f"payload_blob_sha: {payload_blob_sha}",
            f"payload_raw_sha256: {hashlib.sha256(raw_patch).hexdigest()}",
            f"payload_gzip_sha256: {hashlib.sha256(gzip_bytes).hexdigest()}",
            f"payload_raw_bytes: {len(raw_patch)}",
            f"payload_gzip_bytes: {len(gzip_bytes)}",
            "",
        ]
    )


def make_branch_validation_comment(
    *,
    repo: str,
    base_branch: str,
    target_branch: str,
    source_pr: int | str | None = None,
    validation_mode: str = BRANCH_VALIDATE_MODE,
    checks_required: str = "default",
) -> str:
    """Build a LOCAL_BRANCH_VALIDATE_V1 control comment for branch-as-payload."""

    core._validate_branch("base_branch", base_branch, required_prefix=None)  # type: ignore[attr-defined]
    core._validate_branch("target_branch", target_branch, required_prefix="work/")  # type: ignore[attr-defined]
    if validation_mode != BRANCH_VALIDATE_MODE:
        raise core.AiPatchError(f"unsupported validation_mode: {validation_mode!r}")
    lines = [
        BRANCH_VALIDATE_HEADER,
        f"repo: {repo}",
        f"base_branch: {base_branch}",
        f"target_branch: {target_branch}",
        f"validation_mode: {validation_mode}",
        f"checks_required: {checks_required}",
    ]
    if source_pr is not None:
        lines.append(f"source_pr: {source_pr}")
    lines.append("")
    return "\n".join(lines)


def parse_branch_validation_body(body: str) -> BranchValidationRequest:
    """Parse and validate a LOCAL_BRANCH_VALIDATE_V1 branch validation request."""

    if not body.startswith(BRANCH_VALIDATE_HEADER):
        raise core.AiPatchError(f"comment does not start with {BRANCH_VALIDATE_HEADER}")
    metadata = core._parse_metadata(body)  # type: ignore[attr-defined]
    required = ["repo", "base_branch", "target_branch", "validation_mode"]
    missing = [key for key in required if not metadata.get(key)]
    if missing:
        raise core.AiPatchError(f"missing required metadata: {', '.join(missing)}")
    core._validate_branch(  # type: ignore[attr-defined]
        "base_branch",
        metadata["base_branch"],
        required_prefix=None,
    )
    core._validate_branch(  # type: ignore[attr-defined]
        "target_branch",
        metadata["target_branch"],
        required_prefix="work/",
    )
    if metadata["validation_mode"] != BRANCH_VALIDATE_MODE:
        raise core.AiPatchError(f"unsupported validation_mode: {metadata['validation_mode']!r}")
    return BranchValidationRequest(metadata=metadata)


def should_process_comment(comment: core.IssueComment, config: core.BridgeConfig) -> bool:
    """Return true when a watcher comment is supported by the hardened bridge."""

    if comment.body.startswith(BRANCH_VALIDATE_HEADER):
        return True
    return _CORE_SHOULD_PROCESS_COMMENT(comment, config)


def process_comment(comment: core.IssueComment, config: core.BridgeConfig) -> None:
    """Dispatch one watcher comment to the matching hardened consumer."""

    if comment.body.startswith(BRANCH_VALIDATE_HEADER):
        process_branch_validation_comment(comment, config)
        return
    _CORE_PROCESS_COMMENT(comment, config)


def process_branch_validation_comment(
    comment: core.IssueComment,
    config: core.BridgeConfig,
) -> None:
    """Validate an existing remote work branch and post a receipt."""

    request = parse_branch_validation_body(comment.body)
    if request.repo != config.repo:
        raise core.AiPatchError(
            f"message repo {request.repo!r} does not match configured repo {config.repo!r}"
        )

    run_dir = config.resolved_runs_dir() / str(comment.comment_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "issue_comment.md").write_text(comment.body, encoding="utf-8")
    (run_dir / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "LOCAL_BRANCH_VALIDATE_RUN_MANIFEST_V1",
                "source_comment_id": comment.comment_id,
                "source_comment_url": comment.url,
                "repo": request.repo,
                "base_branch": request.base_branch,
                "target_branch": request.target_branch,
                "source_pr": request.source_pr,
                "validation_mode": request.validation_mode,
                "checks_required": request.checks_required,
                "local_checks": list(config.local_checks),
                "run_dir": str(run_dir),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    core.run_command(["git", "fetch", "--prune", "origin"], config.repo_root, None)
    status = core.run_command(["git", "status", "--short"], config.repo_root, None).stdout.strip()
    if status and not config.allow_dirty:
        raise core.AiPatchError("working tree is not clean")

    remote_ref = f"origin/{request.target_branch}"
    core.run_command(["git", "rev-parse", "--verify", f"{remote_ref}^{{commit}}"], config.repo_root, None)
    core.run_command(["git", "switch", "--detach", remote_ref], config.repo_root, None)
    head_sha = core.run_command(["git", "rev-parse", "HEAD"], config.repo_root, None).stdout.strip()

    check_result = _run_branch_validation_local_checks(config, comment.comment_id)
    body_lines = [
        f"target_branch: {request.target_branch}",
        f"head_sha: {head_sha}",
        f"checks_run: {json.dumps(list(config.local_checks))}",
        f"check_outcome: {check_result['check_outcome']}",
        f"run_dir: {run_dir}",
    ]
    if check_result["status"] == "stopped":
        body_lines.extend([
            f"failed_check: {check_result['failed_check']}",
            f"log_path: {check_result['log_path']}",
        ])
    core._post_receipt(  # type: ignore[attr-defined]
        config,
        comment.comment_id,
        status=check_result["status"],
        body_lines=body_lines,
    )


def _run_branch_validation_local_checks(
    config: core.BridgeConfig,
    comment_id: int,
) -> dict[str, str]:
    """Run local checks for a branch validation request."""

    log_path = config.resolved_runs_dir() / str(comment_id) / "branch_validation_checks.log"
    log_parts: list[str] = []

    for command in config.local_checks:
        completed = core.subprocess.run(
            command,
            cwd=str(config.repo_root),
            shell=True,
            text=True,
            capture_output=True,
            check=False,
        )
        log_parts.append(
            f"COMMAND: {command}\n"
            f"RETURN_CODE: {completed.returncode}\n\n"
            f"STDOUT:\n{completed.stdout}\n\n"
            f"STDERR:\n{completed.stderr}\n"
        )
        if completed.returncode != 0:
            log_path.write_text("\n---\n".join(log_parts), encoding="utf-8")
            return {
                "status": "stopped",
                "check_outcome": "failed",
                "failed_check": command,
                "log_path": str(log_path),
            }

    log_path.write_text("\n---\n".join(log_parts), encoding="utf-8")
    return {
        "status": "checked",
        "check_outcome": "passed",
        "failed_check": "",
        "log_path": str(log_path),
    }


def submit_branch_validation_and_wait(
    *,
    repo: str,
    issue_number: int,
    base_branch: str,
    target_branch: str,
    source_pr: int | str | None,
    checks_required: str,
    timeout_seconds: int,
    poll_seconds: int,
    runner: CommandRunner | None = None,
    sleep: SleepFunc = time.sleep,
) -> dict[str, Any]:
    """Post a branch-as-payload validation request and poll for its receipt."""

    body = make_branch_validation_comment(
        repo=repo,
        base_branch=base_branch,
        target_branch=target_branch,
        source_pr=source_pr,
        checks_required=checks_required,
    )
    local_request = parse_branch_validation_body(body)
    posted = post_issue_comment(repo, issue_number, body, runner=runner)
    fetched = fetch_comment_by_id(repo, issue_number, posted.comment_id, runner=runner)
    fetched_request = parse_branch_validation_body(fetched.body)
    assert_branch_validation_equivalent(local_request, fetched_request)
    receipt = poll_for_receipt(
        repo,
        issue_number,
        posted.comment_id,
        timeout_seconds=timeout_seconds,
        poll_seconds=poll_seconds,
        runner=runner,
        sleep=sleep,
    )
    return {
        "submitted": True,
        "control_verified": True,
        "control": BRANCH_VALIDATE_HEADER,
        "comment_id": posted.comment_id,
        "target_branch": target_branch,
        "source_pr": str(source_pr) if source_pr is not None else None,
        "receipt_status": receipt.status,
        "receipt_comment_id": receipt.receipt_comment_id,
        "receipt_reason": receipt.reason,
    }


def assert_branch_validation_equivalent(
    expected: BranchValidationRequest,
    observed: BranchValidationRequest,
) -> None:
    """Raise if a fetched branch validation request differs from submitted intent."""

    fields = ("repo", "base_branch", "target_branch", "validation_mode", "checks_required", "source_pr")
    for field in fields:
        if expected.metadata.get(field) != observed.metadata.get(field):
            raise core.AiPatchError(f"fetched branch validation metadata mismatch: {field}")


def build_transport_comment(
    *,
    repo: str,
    base_branch: str,
    target_branch: str,
    scope: str,
    raw_patch: bytes,
    executor: str = core.LOCAL_CODEX_EXECUTOR,
    mode: str = "local_patch_fit_test_commit_push",
    commit_policy: str = "single_commit",
    test_policy: str = "required",
    transport: str = AUTO_PAYLOAD_TRANSPORT,
    inline_gzip_byte_limit: int = DEFAULT_INLINE_GZIP_BYTE_LIMIT,
    runner: CommandRunner | None = None,
) -> tuple[str, str, str | None]:
    """Build a transport-aware patch comment and return body, transport, blob SHA."""

    gzip_bytes = gzip.compress(raw_patch, mtime=0)
    if transport == AUTO_PAYLOAD_TRANSPORT:
        selected_transport = (
            GITHUB_BLOB_PAYLOAD_TRANSPORT
            if len(gzip_bytes) > inline_gzip_byte_limit
            else INLINE_PAYLOAD_TRANSPORT
        )
    else:
        selected_transport = transport

    if selected_transport == INLINE_PAYLOAD_TRANSPORT:
        body = make_ai_patch_comment(
            repo=repo,
            base_branch=base_branch,
            target_branch=target_branch,
            scope=scope,
            raw_patch=raw_patch,
            executor=executor,
            mode=mode,
            commit_policy=commit_policy,
            test_policy=test_policy,
        )
        return body, selected_transport, None

    if selected_transport != GITHUB_BLOB_PAYLOAD_TRANSPORT:
        raise core.AiPatchError(f"unsupported payload_transport: {selected_transport!r}")

    blob_sha = create_github_blob_payload(repo, gzip_bytes, runner=runner)
    body = make_ai_patch_comment(
        repo=repo,
        base_branch=base_branch,
        target_branch=target_branch,
        scope=scope,
        raw_patch=raw_patch,
        executor=executor,
        mode=mode,
        commit_policy=commit_policy,
        test_policy=test_policy,
        payload_transport=GITHUB_BLOB_PAYLOAD_TRANSPORT,
        payload_blob_sha=blob_sha,
    )
    return body, selected_transport, blob_sha


def create_github_blob_payload(
    repo: str,
    gzip_bytes: bytes,
    runner: CommandRunner | None = None,
) -> str:
    """Create a GitHub blob containing gzip bytes and return the blob SHA."""

    run = runner or core.run_command
    request = {
        "content": base64.b64encode(gzip_bytes).decode("ascii"),
        "encoding": "base64",
    }
    completed = run(
        ["gh", "api", f"repos/{repo}/git/blobs", "--method", "POST", "--input", "-"],
        None,
        json.dumps(request),
    )
    payload = json.loads(completed.stdout)
    blob_sha = payload.get("sha")
    if not isinstance(blob_sha, str) or not blob_sha:
        raise core.AiPatchError("GitHub blob creation response did not include sha")
    return blob_sha


def fetch_github_blob_payload(
    repo: str,
    blob_sha: str,
    runner: CommandRunner | None = None,
) -> bytes:
    """Fetch gzip bytes from a GitHub blob SHA."""

    run = runner or core.run_command
    completed = run(["gh", "api", f"repos/{repo}/git/blobs/{blob_sha}"], None, None)
    payload = json.loads(completed.stdout)
    if payload.get("sha") not in (None, blob_sha):
        raise core.AiPatchError("GitHub blob SHA mismatch")
    if payload.get("encoding") != "base64":
        raise core.AiPatchError("GitHub blob encoding must be base64")
    content = payload.get("content")
    if not isinstance(content, str):
        raise core.AiPatchError("GitHub blob content missing")
    try:
        return base64.b64decode("".join(content.split()), validate=True)
    except Exception as exc:  # noqa: BLE001 - base64 decoder raises several variants.
        raise core.AiPatchError("GitHub blob content is not valid base64") from exc


def submit_patch_and_wait(
    *,
    repo: str,
    issue_number: int,
    base_branch: str,
    target_branch: str,
    scope: str,
    patch_file: Path,
    executor: str,
    mode: str,
    commit_policy: str,
    test_policy: str,
    transport: str,
    inline_gzip_byte_limit: int,
    timeout_seconds: int,
    poll_seconds: int,
    runner: CommandRunner | None = None,
    sleep: SleepFunc = time.sleep,
) -> dict[str, Any]:
    """Submit one patch, verify fetched transport, then poll for a matching receipt."""

    raw_patch = patch_file.read_bytes()
    body, selected_transport, blob_sha = build_transport_comment(
        repo=repo,
        base_branch=base_branch,
        target_branch=target_branch,
        scope=scope,
        raw_patch=raw_patch,
        executor=executor,
        mode=mode,
        commit_policy=commit_policy,
        test_policy=test_policy,
        transport=transport,
        inline_gzip_byte_limit=inline_gzip_byte_limit,
        runner=runner,
    )
    local_message = parse_ai_patch_body(body, runner=runner)
    posted = post_issue_comment(repo, issue_number, body, runner=runner)
    fetched = fetch_comment_by_id(repo, issue_number, posted.comment_id, runner=runner)
    fetched_message = parse_ai_patch_body(fetched.body, runner=runner)
    assert_transport_equivalent(local_message, fetched_message)

    receipt = poll_for_receipt(
        repo,
        issue_number,
        posted.comment_id,
        timeout_seconds=timeout_seconds,
        poll_seconds=poll_seconds,
        runner=runner,
        sleep=sleep,
    )
    return {
        "submitted": True,
        "transport_verified": True,
        "transport": selected_transport,
        "payload_blob_sha": blob_sha,
        "comment_id": posted.comment_id,
        "target_branch": target_branch,
        "receipt_status": receipt.status,
        "receipt_comment_id": receipt.receipt_comment_id,
        "receipt_reason": receipt.reason,
    }


def post_issue_comment(
    repo: str,
    issue_number: int,
    body: str,
    runner: CommandRunner | None = None,
) -> PostedComment:
    """Post a GitHub issue comment and return its ID and body."""

    run = runner or core.run_command
    request = {"body": body}
    completed = run(
        ["gh", "api", f"repos/{repo}/issues/{issue_number}/comments", "--method", "POST", "--input", "-"],
        None,
        json.dumps(request),
    )
    payload = json.loads(completed.stdout)
    comment_id = payload.get("id")
    if not isinstance(comment_id, int):
        raise core.AiPatchError("GitHub comment creation response did not include integer id")
    posted_body = str(payload.get("body", body))
    return PostedComment(comment_id=comment_id, body=posted_body, url=payload.get("html_url"))


def fetch_comment_by_id(
    repo: str,
    issue_number: int,
    comment_id: int,
    runner: CommandRunner | None = None,
) -> core.IssueComment:
    """Fetch issue comments and return the comment matching an exact ID."""

    comments = core.fetch_issue_comments(repo, issue_number, runner=runner)
    for comment in comments:
        if comment.comment_id == comment_id:
            return comment
    raise core.AiPatchError(f"submitted comment {comment_id} was not visible after posting")


def assert_transport_equivalent(
    expected: core.AiPatchMessage,
    observed: core.AiPatchMessage,
) -> None:
    """Raise if a fetched comment does not carry the same verified payload."""

    fields = (
        "repo",
        "base_branch",
        "target_branch",
        "scope",
        "payload_raw_sha256",
        "payload_gzip_sha256",
        "payload_raw_bytes",
        "payload_gzip_bytes",
    )
    for field in fields:
        if expected.metadata.get(field) != observed.metadata.get(field):
            raise core.AiPatchError(f"fetched payload metadata mismatch: {field}")
    if expected.raw_patch != observed.raw_patch:
        raise core.AiPatchError("fetched payload raw patch mismatch")


def poll_for_receipt(
    repo: str,
    issue_number: int,
    source_comment_id: int,
    *,
    timeout_seconds: int,
    poll_seconds: int,
    runner: CommandRunner | None = None,
    sleep: SleepFunc = time.sleep,
) -> ReceiptPollResult:
    """Poll GitHub comments for a LOCAL_CODEX_RECEIPT_V1 matching source_comment_id."""

    deadline = time.monotonic() + timeout_seconds
    while True:
        receipt = find_receipt(
            core.fetch_issue_comments(repo, issue_number, runner=runner),
            source_comment_id,
        )
        if receipt is not None:
            return receipt
        if time.monotonic() >= deadline:
            return ReceiptPollResult(
                status="timeout",
                source_comment_id=source_comment_id,
                reason="no matching LOCAL_CODEX_RECEIPT_V1 before timeout",
            )
        sleep(max(0, min(poll_seconds, deadline - time.monotonic())))


def find_receipt(
    comments: Sequence[core.IssueComment],
    source_comment_id: int,
) -> ReceiptPollResult | None:
    """Return the newest matching receipt comment, if present."""

    matches: list[ReceiptPollResult] = []
    for comment in comments:
        body = comment.body
        if not body.startswith(core.RECEIPT_HEADER):
            continue
        metadata = core._parse_metadata(body)  # type: ignore[attr-defined]
        if metadata.get("source_comment_id") != str(source_comment_id):
            continue
        status = metadata.get("status", "failed")
        reason = metadata.get("reason")
        matches.append(
            ReceiptPollResult(
                status=status,
                source_comment_id=source_comment_id,
                receipt_comment_id=comment.comment_id,
                body=body,
                reason=reason,
            )
        )
    return matches[-1] if matches else None


def receipt_timestamp_lines(now_utc: datetime | None = None) -> list[str]:
    """Return machine and Melbourne human timestamp lines for a GitHub receipt."""

    current_utc = now_utc or datetime.now(timezone.utc)
    if current_utc.tzinfo is None:
        current_utc = current_utc.replace(tzinfo=timezone.utc)
    current_utc = current_utc.astimezone(timezone.utc)
    melbourne = current_utc.astimezone(ZoneInfo(MELBOURNE_TIMEZONE))
    offset = melbourne.utcoffset()
    if offset is None:
        raise core.AiPatchError("could not determine Melbourne UTC offset")
    total_minutes = int(offset.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    hours, minutes = divmod(abs(total_minutes), 60)
    offset_text = f"UTC{sign}{hours:02d}"
    if minutes:
        offset_text = f"{offset_text}:{minutes:02d}"
    return [
        f"computer_unix_epoch_s: {int(current_utc.timestamp())}",
        f"computer_utc_minute: {current_utc.strftime('%Y-%m-%dT%H:%MZ')}",
        f"human_melbourne_minute: {melbourne.strftime('%d-%m-%Y %H:%M %Z')}",
        f"human_timezone: {MELBOURNE_TIMEZONE}",
        f"human_utc_offset: {offset_text}",
    ]


def _ensure_receipt_contract_lines(body_lines: Sequence[str]) -> list[str]:
    lines = list(body_lines)
    if not any(line.startswith("checks_run:") for line in lines):
        lines.append("checks_run: unknown")
    if not any(line.startswith("check_outcome:") for line in lines):
        lines.append("check_outcome: unknown")
    return lines


def post_verified_receipt(
    config: core.BridgeConfig,
    comment_id: int,
    *,
    status: str,
    body_lines: Sequence[str],
) -> None:
    """Post a receipt and verify it is visible on GitHub before returning."""

    body = "\n".join(
        [
            core.RECEIPT_HEADER,
            f"source_comment_id: {comment_id}",
            f"status: {status}",
            *receipt_timestamp_lines(),
            *_ensure_receipt_contract_lines(body_lines),
            "",
        ]
    )
    if config.dry_run:
        receipt_path = config.resolved_runs_dir() / str(comment_id) / "github_receipt.md"
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(body, encoding="utf-8")
        print(body)
        return

    last_error: Exception | None = None
    for _attempt in range(RECEIPT_POST_ATTEMPTS):
        try:
            posted = post_issue_comment(config.repo, config.issue_number, body)
            fetched = fetch_comment_by_id(config.repo, config.issue_number, posted.comment_id)
            if fetched.body.startswith(core.RECEIPT_HEADER):
                fetched_metadata = core._parse_metadata(fetched.body)  # type: ignore[attr-defined]
                if (
                    fetched_metadata.get("source_comment_id") == str(comment_id)
                    and fetched_metadata.get("status") == status
                    and fetched_metadata.get("human_timezone") == MELBOURNE_TIMEZONE
                ):
                    return
            last_error = core.AiPatchError("receipt comment was posted but did not verify")
        except Exception as exc:  # noqa: BLE001 - retry preserves distinct failure state.
            last_error = exc
            time.sleep(1)
    raise core.AiPatchError(f"receipt_post_failed: {last_error}")


def _validate_blob_metadata(body: str, metadata: dict[str, str]) -> None:
    if not body.startswith(core.AI_PATCH_HEADER):
        raise core.AiPatchError(f"comment does not start with {core.AI_PATCH_HEADER}")
    core._validate_required_metadata(metadata)  # type: ignore[attr-defined]
    required_blob_keys = ["payload_transport", "payload_blob_sha"]
    missing = [key for key in required_blob_keys if not metadata.get(key)]
    if missing:
        raise core.AiPatchError(f"missing required metadata: {', '.join(missing)}")
    core._validate_branch("base_branch", metadata["base_branch"], required_prefix=None)  # type: ignore[attr-defined]
    core._validate_policy_metadata(metadata)  # type: ignore[attr-defined]
    core._validate_target_branch_for_executor(metadata)  # type: ignore[attr-defined]
    if metadata["payload_encoding"] != "base64+gzip":
        raise core.AiPatchError("payload_encoding must be base64+gzip")


def _message_from_gzip_bytes(metadata: dict[str, str], gzip_bytes: bytes) -> core.AiPatchMessage:
    gzip_sha256 = hashlib.sha256(gzip_bytes).hexdigest()
    if gzip_sha256 != metadata["payload_gzip_sha256"]:
        raise core.AiPatchError("payload_gzip_sha256 mismatch")
    try:
        raw_patch = gzip.decompress(gzip_bytes)
    except Exception as exc:  # noqa: BLE001 - gzip raises several compression exceptions.
        raise core.AiPatchError("payload is not valid gzip") from exc
    raw_sha256 = hashlib.sha256(raw_patch).hexdigest()
    if raw_sha256 != metadata["payload_raw_sha256"]:
        raise core.AiPatchError("payload_raw_sha256 mismatch")
    if metadata.get("payload_gzip_bytes"):
        core._verify_byte_count(  # type: ignore[attr-defined]
            "payload_gzip_bytes",
            metadata["payload_gzip_bytes"],
            len(gzip_bytes),
        )
    if metadata.get("payload_raw_bytes"):
        core._verify_byte_count(  # type: ignore[attr-defined]
            "payload_raw_bytes",
            metadata["payload_raw_bytes"],
            len(raw_patch),
        )
    if b"diff --git " not in raw_patch:
        raise core.AiPatchError("decoded payload does not look like a git diff")
    return core.AiPatchMessage(
        metadata=metadata,
        payload_b64=base64.b64encode(gzip_bytes).decode("ascii"),
        raw_patch=raw_patch,
        gzip_sha256=gzip_sha256,
        raw_sha256=raw_sha256,
    )


def _main_submit_and_wait(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description="Submit one AI_PATCH_V1 patch and wait for its receipt.")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--base-branch", default="main")
    parser.add_argument("--target-branch", required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--patch-file", type=Path, required=True)
    parser.add_argument("--executor", default=core.LOCAL_CODEX_EXECUTOR)
    parser.add_argument("--mode", default="local_patch_fit_test_commit_push")
    parser.add_argument("--commit-policy", default="single_commit")
    parser.add_argument("--test-policy", default="required")
    parser.add_argument(
        "--transport",
        choices=(AUTO_PAYLOAD_TRANSPORT, INLINE_PAYLOAD_TRANSPORT, GITHUB_BLOB_PAYLOAD_TRANSPORT),
        default=AUTO_PAYLOAD_TRANSPORT,
    )
    parser.add_argument("--inline-gzip-byte-limit", type=int, default=DEFAULT_INLINE_GZIP_BYTE_LIMIT)
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(list(argv))

    result = submit_patch_and_wait(
        repo=args.repo,
        issue_number=args.issue_number,
        base_branch=args.base_branch,
        target_branch=args.target_branch,
        scope=args.scope,
        patch_file=args.patch_file,
        executor=args.executor,
        mode=args.mode,
        commit_policy=args.commit_policy,
        test_policy=args.test_policy,
        transport=args.transport,
        inline_gzip_byte_limit=args.inline_gzip_byte_limit,
        timeout_seconds=args.timeout_seconds,
        poll_seconds=args.poll_seconds,
    )
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.out is not None:
        args.out.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0 if result["receipt_status"] != "timeout" else 1


def _main_validate_branch_and_wait(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Submit one LOCAL_BRANCH_VALIDATE_V1 request and wait for its receipt."
    )
    parser.add_argument("--repo", required=True)
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--base-branch", default="main")
    parser.add_argument("--target-branch", required=True)
    parser.add_argument("--source-pr")
    parser.add_argument("--checks-required", default="default")
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(list(argv))

    result = submit_branch_validation_and_wait(
        repo=args.repo,
        issue_number=args.issue_number,
        base_branch=args.base_branch,
        target_branch=args.target_branch,
        source_pr=args.source_pr,
        checks_required=args.checks_required,
        timeout_seconds=args.timeout_seconds,
        poll_seconds=args.poll_seconds,
    )
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.out is not None:
        args.out.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0 if result["receipt_status"] != "timeout" else 1


def main(argv: Sequence[str] | None = None) -> int:
    """Bridge CLI entry point with hardening overlay installed."""

    args = list(sys.argv[1:] if argv is None else argv)
    install()
    if args and args[0] == "submit-and-wait":
        return _main_submit_and_wait(args[1:])
    if args and args[0] == "validate-branch-and-wait":
        return _main_validate_branch_and_wait(args[1:])
    return core.main(args)
