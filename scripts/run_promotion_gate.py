"""Execute one manifest-resolved aggregate promotion set and write a receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shlex
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.proof_authority import AuthorityError, load_and_validate_authority


DEFAULT_RECEIPT_DIR = Path("var/proof_receipts")
DEFAULT_TIMEOUT_SECONDS = 300
AUTHORITY_PATHS = (
    Path("config/retained_test_registry.yaml"),
    Path("config/proof_blocks.yaml"),
    Path("docs/08_TESTING_AND_PROMOTION_CORE.md"),
    Path("docs/08.1_TESTING_AND_PROMOTION_WORKING.md"),
    Path("docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md"),
    Path("project_control/canonical_project_manager/EXEC_PLAN.md"),
    Path("ROADMAP_LEDGER_V2.md"),
)
ENVIRONMENT_PATHS = (Path("pyproject.toml"), Path("uv.lock"), Path(".python-version"))


class PromotionError(RuntimeError):
    """Raised when an aggregate promotion claim cannot be established."""


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _canonical_payload(payload: Mapping[str, Any]) -> bytes:
    unsigned = dict(payload)
    unsigned.pop("evidence_hash", None)
    return json.dumps(
        unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sign_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy with a deterministic evidence hash."""

    signed = dict(payload)
    signed["evidence_hash"] = _sha256_bytes(_canonical_payload(signed))
    return signed


def verify_receipt(payload: Mapping[str, Any]) -> None:
    """Fail when a receipt is unsigned or its content has changed."""

    actual = payload.get("evidence_hash")
    if not isinstance(actual, str) or not actual:
        raise PromotionError("receipt has no evidence_hash")
    expected = _sha256_bytes(_canonical_payload(payload))
    if actual != expected:
        raise PromotionError(
            f"receipt evidence_hash mismatch: expected {expected}, got {actual}"
        )


def _git(repo_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise PromotionError(
            f"git {' '.join(args)} failed: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def git_identity(repo_root: Path) -> dict[str, str]:
    return {
        "commit": _git(repo_root, "rev-parse", "HEAD"),
        "branch": _git(repo_root, "branch", "--show-current"),
        "status": _git(
            repo_root, "status", "--porcelain=v1", "--untracked-files=all"
        ),
    }


def require_clean_git(identity: Mapping[str, str], *, stage: str) -> None:
    status = identity.get("status", "")
    if status:
        raise PromotionError(f"{stage} Git state is dirty:\n{status}")


def resolve_command(
    command: str, *, inherited_environment: Mapping[str, str] | None = None
) -> tuple[list[str], dict[str, str]]:
    """Resolve an env-prefixed command without shell evaluation."""

    parts = shlex.split(command)
    if not parts:
        raise PromotionError("proof command is empty")
    environment = dict(inherited_environment or os.environ)
    if parts[0] == "env":
        parts = parts[1:]
        while parts and "=" in parts[0] and not parts[0].startswith("="):
            key, value = parts.pop(0).split("=", 1)
            if not key:
                raise PromotionError("proof command contains an empty environment key")
            environment[key] = value
    if not parts:
        raise PromotionError("proof command has no executable")
    if parts[0] in {"python", "python3", "python3.13"}:
        parts[0] = sys.executable
    return parts, environment


def classify_pytest_result(
    *, exit_code: int | None, stdout: str, stderr: str, timed_out: bool = False
) -> tuple[str, dict[str, int]]:
    """Classify a pytest proof result and reject hidden skips."""

    combined = f"{stdout}\n{stderr}"
    counts = {
        label: sum(int(value) for value in re.findall(rf"(\d+)\s+{label}", combined))
        for label in ("passed", "failed", "skipped", "errors", "error")
    }
    if timed_out:
        return "TIMEOUT", counts
    if exit_code != 0:
        return "FAIL", counts
    if counts["skipped"]:
        return "FAIL_SKIPPED", counts
    if counts["passed"] == 0:
        return "FAIL_NO_PASS_EVIDENCE", counts
    return "PASS", counts


def _run_block(
    block_id: str,
    command: str,
    *,
    repo_root: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    resolved, environment = resolve_command(command)
    started = time.monotonic()
    stdout = ""
    stderr = ""
    exit_code: int | None = None
    timed_out = False
    with (
        tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stdout_file,
        tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stderr_file,
    ):
        try:
            completed = subprocess.run(
                resolved,
                cwd=repo_root,
                env=environment,
                check=False,
                text=True,
                stdout=stdout_file,
                stderr=stderr_file,
                timeout=timeout_seconds,
            )
            exit_code = completed.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
        stdout_file.flush()
        stderr_file.flush()
        stdout_file.seek(0)
        stderr_file.seek(0)
        stdout = stdout_file.read()
        stderr = stderr_file.read()
    duration = round(time.monotonic() - started, 6)
    status, counts = classify_pytest_result(
        exit_code=exit_code, stdout=stdout, stderr=stderr, timed_out=timed_out
    )
    return {
        "proof_block_id": block_id,
        "status": status,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "duration_seconds": duration,
        "command": command,
        "resolved_command": resolved,
        "pytest_counts": counts,
        "stdout_sha256": _sha256_bytes(stdout.encode("utf-8")),
        "stderr_sha256": _sha256_bytes(stderr.encode("utf-8")),
    }


def _environment_identity(repo_root: Path) -> dict[str, Any]:
    return {
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "environment_files": {
            path.as_posix(): _sha256_path(repo_root / path)
            for path in ENVIRONMENT_PATHS
        },
    }


def _authority_identity(repo_root: Path) -> dict[str, str]:
    return {
        path.as_posix(): _sha256_path(repo_root / path) for path in AUTHORITY_PATHS
    }


def build_check_summary(
    promotion_set_id: str, *, repo_root: Path = Path(".")
) -> dict[str, Any]:
    model = load_and_validate_authority(repo_root=repo_root)
    promotion = model.promotion_sets.get(promotion_set_id)
    if promotion is None:
        raise PromotionError(f"unknown promotion set: {promotion_set_id}")
    return {
        "promotion_set_id": promotion_set_id,
        "proof_block_ids": list(promotion.proof_block_ids),
        "test_family_ids": list(promotion.test_family_ids),
        "test_paths": list(promotion.test_paths),
    }


def execute_promotion_set(
    promotion_set_id: str,
    *,
    repo_root: Path = Path("."),
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Validate, execute and receipt one exact promotion set."""

    resolved_root = repo_root.resolve()
    model = load_and_validate_authority(repo_root=resolved_root)
    promotion = model.promotion_sets.get(promotion_set_id)
    if promotion is None:
        raise PromotionError(f"unknown promotion set: {promotion_set_id}")

    pre_git = git_identity(resolved_root)
    require_clean_git(pre_git, stage="pre-run")
    started_at = datetime.now(UTC).isoformat()
    started = time.monotonic()
    results: list[dict[str, Any]] = []
    for block_id in promotion.proof_block_ids:
        block = model.proof_blocks[block_id]
        result = _run_block(
            block_id,
            block.command,
            repo_root=resolved_root,
            timeout_seconds=timeout_seconds,
        )
        results.append(result)
        if result["status"] != "PASS":
            break

    post_git = git_identity(resolved_root)
    total_duration = round(time.monotonic() - started, 6)
    status = "PASS"
    failure_reasons: list[str] = []
    if len(results) != len(promotion.proof_block_ids):
        status = "FAIL"
        failure_reasons.append("not all promotion blocks executed")
    failed = [result["proof_block_id"] for result in results if result["status"] != "PASS"]
    if failed:
        status = "FAIL"
        failure_reasons.append("failed proof blocks: " + ", ".join(failed))
    if post_git["status"]:
        status = "FAIL"
        failure_reasons.append("post-run Git state is dirty")
    if post_git["commit"] != pre_git["commit"] or post_git["branch"] != pre_git["branch"]:
        status = "FAIL"
        failure_reasons.append("Git identity changed during proof")

    receipt = {
        "schema_version": "promotion_receipt_v1",
        "promotion_set_id": promotion_set_id,
        "status": status,
        "failure_reasons": failure_reasons,
        "started_at_utc": started_at,
        "finished_at_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": total_duration,
        "git": {"pre": pre_git, "post": post_git},
        "environment": _environment_identity(resolved_root),
        "authority_sha256": _authority_identity(resolved_root),
        "membership": {
            "proof_block_ids": list(promotion.proof_block_ids),
            "test_family_ids": list(promotion.test_family_ids),
            "test_paths": list(promotion.test_paths),
        },
        "block_results": results,
        "summary": {
            "expected_block_count": len(promotion.proof_block_ids),
            "executed_block_count": len(results),
            "passed_block_count": sum(result["status"] == "PASS" for result in results),
            "failed_block_count": sum(result["status"] != "PASS" for result in results),
            "passed_test_count": sum(
                result["pytest_counts"].get("passed", 0) for result in results
            ),
            "skipped_test_count": sum(
                result["pytest_counts"].get("skipped", 0) for result in results
            ),
        },
    }
    return sign_receipt(receipt)


def _write_receipt(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--set", default="pre_m00_current", dest="promotion_set")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--verify-receipt", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        if args.verify_receipt:
            payload = json.loads(args.verify_receipt.read_text(encoding="utf-8"))
            verify_receipt(payload)
            print(f"promotion_receipt=PASS {args.verify_receipt}")
            return 0
        if args.check_only:
            summary = build_check_summary(args.promotion_set)
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 0
        receipt = execute_promotion_set(
            args.promotion_set, timeout_seconds=args.timeout
        )
    except (AuthorityError, PromotionError, OSError, json.JSONDecodeError) as exc:
        print(f"promotion_gate=FAIL {exc}", file=sys.stderr)
        return 2

    receipt_path = args.receipt or (
        DEFAULT_RECEIPT_DIR / f"{args.promotion_set}.json"
    )
    _write_receipt(receipt_path, receipt)
    print(
        f"promotion_gate={receipt['status']} set={args.promotion_set} "
        f"blocks={receipt['summary']['executed_block_count']}/"
        f"{receipt['summary']['expected_block_count']} "
        f"tests={receipt['summary']['passed_test_count']} "
        f"receipt={receipt_path} hash={receipt['evidence_hash']}"
    )
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
