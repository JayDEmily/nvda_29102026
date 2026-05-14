"""Receipt failure hardening overlay for the AI Patch Bridge.

This module wraps the existing transport hardening entrypoint without replacing
that larger module. It makes receipt posting failures durable locally and makes
the watcher ledger distinguish receipt-post failures from ordinary processed
comments.
"""

from __future__ import annotations

import json
import time
from collections.abc import Sequence

from ai_patch_bridge import core
from ai_patch_bridge import transport_hardening as transport

_BASE_INSTALL = transport.install
_BASE_MAIN = transport.main


def _run_dir(config: core.BridgeConfig, comment_id: int):
    """Return the local run directory for one source comment."""

    path = config.resolved_runs_dir() / str(comment_id)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _write_receipt_state(
    config: core.BridgeConfig,
    comment_id: int,
    *,
    status: str,
    ledger_status: str,
    attempted_receipt_path: str,
    receipt_comment_id: int | None = None,
    reason: str | None = None,
) -> None:
    """Write durable local receipt-post state for later diagnostics."""

    state = {
        "schema": "LOCAL_RECEIPT_POST_STATE_V1",
        "source_comment_id": comment_id,
        "status": status,
        "ledger_status": ledger_status,
        "attempted_receipt_path": attempted_receipt_path,
        "receipt_comment_id": receipt_comment_id,
        "reason": reason,
        "ts": int(time.time()),
    }
    (_run_dir(config, comment_id) / "receipt_post_state.json").write_text(
        json.dumps(state, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _read_receipt_ledger_status(config: core.BridgeConfig, comment_id: int) -> str | None:
    """Read the receipt-derived ledger status for a processed comment."""

    state_path = _run_dir(config, comment_id) / "receipt_post_state.json"
    if not state_path.exists():
        return None
    state = json.loads(state_path.read_text(encoding="utf-8"))
    value = state.get("ledger_status")
    return value if isinstance(value, str) else None


def post_verified_receipt(
    config: core.BridgeConfig,
    comment_id: int,
    *,
    status: str,
    body_lines: Sequence[str],
) -> None:
    """Post a receipt, cache the attempted receipt, and record post outcome.

    The previous overlay only wrote ``github_receipt.md`` in dry-run mode. A live
    receipt-post failure could therefore leave useful local validation artefacts
    but no durable attempted receipt. This wrapper always writes the attempted
    receipt body before GitHub posting and records whether GitHub verification
    succeeded.
    """

    body = "\n".join(
        [
            core.RECEIPT_HEADER,
            f"source_comment_id: {comment_id}",
            f"status: {status}",
            *transport.receipt_timestamp_lines(),
            *transport._ensure_receipt_contract_lines(body_lines),  # type: ignore[attr-defined]
            "",
        ]
    )
    run_dir = _run_dir(config, comment_id)
    receipt_path = run_dir / "github_receipt.md"
    receipt_path.write_text(body, encoding="utf-8")

    if config.dry_run:
        _write_receipt_state(
            config,
            comment_id,
            status="dry_run_written",
            ledger_status="processed_receipt_local_only",
            attempted_receipt_path=str(receipt_path),
        )
        print(body)
        return

    last_error: Exception | None = None
    for _attempt in range(transport.RECEIPT_POST_ATTEMPTS):
        try:
            posted = transport.post_issue_comment(config.repo, config.issue_number, body)
            fetched = transport.fetch_comment_by_id(config.repo, config.issue_number, posted.comment_id)
            if fetched.body.startswith(core.RECEIPT_HEADER):
                fetched_metadata = core._parse_metadata(fetched.body)  # type: ignore[attr-defined]
                if (
                    fetched_metadata.get("source_comment_id") == str(comment_id)
                    and fetched_metadata.get("status") == status
                    and fetched_metadata.get("human_timezone") == transport.MELBOURNE_TIMEZONE
                ):
                    _write_receipt_state(
                        config,
                        comment_id,
                        status="posted_verified",
                        ledger_status="processed_receipt_posted",
                        attempted_receipt_path=str(receipt_path),
                        receipt_comment_id=posted.comment_id,
                    )
                    return
            last_error = core.AiPatchError("receipt comment was posted but did not verify")
        except Exception as exc:  # noqa: BLE001 - receipt failures must be durable.
            last_error = exc
            time.sleep(1)

    reason = f"receipt_post_failed: {last_error}"
    _write_receipt_state(
        config,
        comment_id,
        status="receipt_post_failed",
        ledger_status="processed_receipt_post_failed",
        attempted_receipt_path=str(receipt_path),
        reason=reason,
    )
    raise core.AiPatchError(reason)


def _should_process(comment: core.IssueComment, config: core.BridgeConfig) -> bool:
    """Return true when one comment is eligible for local processing."""

    if str(comment.comment_id) in core._load_processed(config.resolved_state_dir()):  # type: ignore[attr-defined]
        return False
    return core._should_process_comment(comment, config)  # type: ignore[attr-defined]


def run_once(config: core.BridgeConfig) -> int:
    """Process supported comments once with receipt-aware ledger states."""

    core._ensure_dirs(config)  # type: ignore[attr-defined]
    processed = core._load_processed(config.resolved_state_dir())  # type: ignore[attr-defined]
    comments = core.fetch_issue_comments(config.repo, config.issue_number)
    new_comments = [comment for comment in comments if _should_process(comment, config)]
    if not new_comments:
        print("No new AI_PATCH_V1 or LOCAL_BRANCH_VALIDATE_V1 comments found.")
        return 0

    exit_code = 0
    for comment in new_comments:
        try:
            core.process_comment(comment, config)
            ledger_status = _read_receipt_ledger_status(config, comment.comment_id) or "processed"
            processed[str(comment.comment_id)] = {"status": ledger_status, "ts": int(time.time())}
        except Exception as exc:  # noqa: BLE001 - preserve failure in the ledger.
            reason = str(exc)
            exit_code = 1
            ledger_status = "processed_receipt_post_failed" if "receipt_post_failed" in reason else "failed"
            processed[str(comment.comment_id)] = {
                "status": ledger_status,
                "ts": int(time.time()),
                "reason": reason,
            }
            if ledger_status != "processed_receipt_post_failed":
                core._safe_failure_receipt(comment, config, reason)  # type: ignore[attr-defined]
        finally:
            core._save_processed(config.resolved_state_dir(), processed)  # type: ignore[attr-defined]
    return exit_code


def install() -> None:
    """Install transport hardening plus receipt-failure hardening hooks."""

    transport.post_verified_receipt = post_verified_receipt  # type: ignore[assignment]
    _BASE_INSTALL()
    core._post_receipt = post_verified_receipt  # type: ignore[attr-defined]
    core.run_once = run_once  # type: ignore[assignment]
    transport.post_verified_receipt = post_verified_receipt  # type: ignore[assignment]


def main(argv: Sequence[str] | None = None) -> int:
    """Run the transport-hardened CLI with receipt-failure hardening installed."""

    transport.install = install  # type: ignore[assignment]
    install()
    return _BASE_MAIN(argv)
