"""Core parser, decoder, and dispatcher support for AI_PATCH_V1 comments."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import textwrap
import time
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

AI_PATCH_HEADER = "AI_PATCH_V1"
RECEIPT_HEADER = "LOCAL_CODEX_RECEIPT_V1"
PAYLOAD_BEGIN = "PAYLOAD_BEGIN"
PAYLOAD_END = "PAYLOAD_END"
DEFAULT_STATE_DIR = ".ai_patch_bridge/state"
DEFAULT_RUNS_DIR = ".ai_patch_bridge/runs"
DEFAULT_CODEX_COMMAND = "codex exec --full-auto -"
DEFAULT_LOCAL_CHECKS = ("make test",)
BRANCH_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,180}$")
LOCAL_CODEX_EXECUTOR = "local-codex"
GITHUB_ACTION_EXECUTOR = "github-action"
RESCUE_BRANCH_EXECUTOR = "rescue-branch"
SUPPORTED_EXECUTORS = (LOCAL_CODEX_EXECUTOR, GITHUB_ACTION_EXECUTOR, RESCUE_BRANCH_EXECUTOR)
SUPPORTED_COMMIT_POLICIES = ("single_commit", "patch_series")
SUPPORTED_TEST_POLICIES = ("required", "not_run_allowed", "rescue_unvetted")
PAYLOAD_RE = re.compile(r"(?ms)^PAYLOAD_BEGIN\n(?P<payload>.*?)\nPAYLOAD_END\s*$")
CommandRunner = Callable[[Sequence[str], Path | None, str | None], subprocess.CompletedProcess[str]]


class AiPatchError(RuntimeError):
    """Raised when an AI_PATCH_V1 payload is invalid or cannot be processed."""


@dataclass(frozen=True, slots=True)
class AiPatchMessage:
    """Parsed and verified AI_PATCH_V1 issue comment."""

    metadata: dict[str, str]
    payload_b64: str
    raw_patch: bytes
    gzip_sha256: str
    raw_sha256: str

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
    def scope(self) -> str:
        return self.metadata["scope"]


@dataclass(slots=True)
class BridgeConfig:
    """Runtime configuration for the local bridge."""

    repo: str
    issue_number: int
    repo_root: Path = field(default_factory=lambda: Path.cwd())
    state_dir: Path = field(default_factory=lambda: Path(DEFAULT_STATE_DIR))
    runs_dir: Path = field(default_factory=lambda: Path(DEFAULT_RUNS_DIR))
    codex_command: str = DEFAULT_CODEX_COMMAND
    local_checks: tuple[str, ...] = DEFAULT_LOCAL_CHECKS
    poll_seconds: int = 60
    expected_codex_version: str | None = None
    allow_dirty: bool = False
    dry_run: bool = False
    accepted_executors: tuple[str, ...] = ("local-codex",)

    def resolved_state_dir(self) -> Path:
        return _resolve_under_repo(self.repo_root, self.state_dir)

    def resolved_runs_dir(self) -> Path:
        return _resolve_under_repo(self.repo_root, self.runs_dir)


@dataclass(frozen=True, slots=True)
class IssueComment:
    """One GitHub issue comment from the inbox."""

    comment_id: int
    body: str
    user_login: str | None = None
    url: str | None = None


def parse_ai_patch_body(body: str) -> AiPatchMessage:
    """Parse, decode, and verify an AI_PATCH_V1 body."""

    if not body.startswith(AI_PATCH_HEADER):
        raise AiPatchError(f"comment does not start with {AI_PATCH_HEADER}")

    payload_match = PAYLOAD_RE.search(body)
    if payload_match is None:
        raise AiPatchError("missing PAYLOAD_BEGIN/PAYLOAD_END block")

    metadata = _parse_metadata(body)
    _validate_required_metadata(metadata)
    _validate_branch("base_branch", metadata["base_branch"], required_prefix=None)
    _validate_policy_metadata(metadata)
    _validate_target_branch_for_executor(metadata)

    if metadata["payload_encoding"] != "base64+gzip":
        raise AiPatchError("payload_encoding must be base64+gzip")

    payload_b64 = "".join(payload_match.group("payload").split())
    try:
        gzip_bytes = base64.b64decode(payload_b64, validate=True)
    except Exception as exc:  # noqa: BLE001 - base64 raises binascii.Error or ValueError variants.
        raise AiPatchError("payload is not valid base64") from exc

    gzip_sha256 = hashlib.sha256(gzip_bytes).hexdigest()
    if gzip_sha256 != metadata["payload_gzip_sha256"]:
        raise AiPatchError("payload_gzip_sha256 mismatch")

    try:
        raw_patch = gzip.decompress(gzip_bytes)
    except Exception as exc:  # noqa: BLE001 - gzip raises several compression exceptions.
        raise AiPatchError("payload is not valid gzip") from exc

    raw_sha256 = hashlib.sha256(raw_patch).hexdigest()
    if raw_sha256 != metadata["payload_raw_sha256"]:
        raise AiPatchError("payload_raw_sha256 mismatch")

    if metadata.get("payload_gzip_bytes"):
        _verify_byte_count("payload_gzip_bytes", metadata["payload_gzip_bytes"], len(gzip_bytes))
    if metadata.get("payload_raw_bytes"):
        _verify_byte_count("payload_raw_bytes", metadata["payload_raw_bytes"], len(raw_patch))

    if b"diff --git " not in raw_patch:
        raise AiPatchError("decoded payload does not look like a git diff")

    return AiPatchMessage(
        metadata=metadata,
        payload_b64=payload_b64,
        raw_patch=raw_patch,
        gzip_sha256=gzip_sha256,
        raw_sha256=raw_sha256,
    )


def make_ai_patch_comment(
    *,
    repo: str,
    base_branch: str,
    target_branch: str,
    scope: str,
    raw_patch: bytes,
    executor: str = LOCAL_CODEX_EXECUTOR,
    mode: str = "local_patch_fit_test_commit_push",
    commit_policy: str = "single_commit",
    test_policy: str = "required",
) -> str:
    """Build a deterministic base64+gzip AI_PATCH_V1 issue-comment body."""

    metadata = {
        "executor": executor,
        "commit_policy": commit_policy,
        "test_policy": test_policy,
        "target_branch": target_branch,
    }
    _validate_branch("base_branch", base_branch, required_prefix=None)
    _validate_policy_metadata(metadata)
    _validate_target_branch_for_executor(metadata)
    gzip_bytes = gzip.compress(raw_patch, mtime=0)
    payload_b64 = base64.b64encode(gzip_bytes).decode("ascii")
    wrapped_payload = "\n".join(textwrap.wrap(payload_b64, width=100))
    return "\n".join(
        [
            AI_PATCH_HEADER,
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
            f"payload_raw_sha256: {hashlib.sha256(raw_patch).hexdigest()}",
            f"payload_gzip_sha256: {hashlib.sha256(gzip_bytes).hexdigest()}",
            f"payload_raw_bytes: {len(raw_patch)}",
            f"payload_gzip_bytes: {len(gzip_bytes)}",
            "",
            PAYLOAD_BEGIN,
            wrapped_payload,
            PAYLOAD_END,
            "",
        ]
    )


def fetch_issue_comments(
    repo: str,
    issue_number: int,
    runner: CommandRunner | None = None,
) -> list[IssueComment]:
    """Fetch issue comments with GitHub CLI."""

    run = runner or run_command
    endpoint = f"repos/{repo}/issues/{issue_number}/comments"
    completed = run(
        ["gh", "api", "--paginate", endpoint, "-H", "Accept: application/vnd.github.raw+json"],
        None,
        None,
    )
    payload = _parse_gh_api_json_pages(completed.stdout)
    comments: list[IssueComment] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        user = item.get("user")
        user_login = user.get("login") if isinstance(user, dict) else None
        comments.append(
            IssueComment(
                comment_id=int(item["id"]),
                body=str(item.get("body", "")),
                user_login=user_login,
                url=item.get("html_url"),
            )
        )
    return comments


def run_once(config: BridgeConfig) -> int:
    """Process all unprocessed AI_PATCH_V1 comments once."""

    _ensure_dirs(config)
    processed = _load_processed(config.resolved_state_dir())
    comments = fetch_issue_comments(config.repo, config.issue_number)
    new_patch_comments = [
        comment
        for comment in comments
        if str(comment.comment_id) not in processed and _should_process_comment(comment, config)
    ]
    if not new_patch_comments:
        print("No new AI_PATCH_V1 comments found.")
        return 0

    exit_code = 0
    for comment in new_patch_comments:
        try:
            process_comment(comment, config)
            processed[str(comment.comment_id)] = {"status": "processed", "ts": int(time.time())}
        except Exception as exc:  # noqa: BLE001 - top-level command should receipt and continue.
            exit_code = 1
            processed[str(comment.comment_id)] = {
                "status": "failed",
                "ts": int(time.time()),
                "reason": str(exc),
            }
            _safe_failure_receipt(comment, config, str(exc))
        finally:
            _save_processed(config.resolved_state_dir(), processed)
    return exit_code


def process_comment(comment: IssueComment, config: BridgeConfig) -> None:
    """Decode one comment, invoke Codex, and post a receipt."""

    message = parse_ai_patch_body(comment.body)
    if message.repo != config.repo:
        raise AiPatchError(
            f"message repo {message.repo!r} does not match configured repo {config.repo!r}"
        )

    run_dir = config.resolved_runs_dir() / str(comment.comment_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    patch_path = run_dir / "incoming.patch"
    manifest_path = run_dir / "manifest.json"
    prompt_path = run_dir / "codex_prompt.md"
    comment_path = run_dir / "issue_comment.md"
    comment_path.write_text(comment.body, encoding="utf-8")
    patch_path.write_bytes(message.raw_patch)

    manifest = _build_manifest(comment, message, config, patch_path, run_dir)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    prompt_path.write_text(_build_codex_prompt(manifest_path, manifest), encoding="utf-8")

    if config.dry_run:
        _post_receipt(
            config,
            comment.comment_id,
            status="dry_run_ready",
            body_lines=[
                f"target_branch: {message.target_branch}",
                f"run_dir: {run_dir}",
                (
                    "note: dry run decoded and verified only; "
                    "it did not change git state or invoke Codex"
                ),
            ],
        )
        return

    _prepare_target_branch(message, config)
    _invoke_codex(config, prompt_path)
    receipt = _build_success_or_stop_receipt(
        config, comment.comment_id, message.target_branch, message.raw_patch, message.scope
    )
    _post_receipt(config, comment.comment_id, status=receipt["status"], body_lines=receipt["lines"])


def run_watch(config: BridgeConfig) -> None:
    """Run the bridge in polling mode."""

    while True:
        run_once(config)
        time.sleep(config.poll_seconds)


def run_preflight(config: BridgeConfig) -> int:
    """Run deterministic environment checks without processing patches."""

    checks: list[tuple[str, Sequence[str], Path | None]] = [
        ("python_version", [sys.executable, "--version"], None),
        ("git_version", ["git", "--version"], None),
        ("gh_auth_status", ["gh", "auth", "status"], None),
        ("codex_version", ["codex", "--version"], None),
        ("git_status", ["git", "status", "--short"], config.repo_root),
        ("git_remote_origin", ["git", "remote", "get-url", "origin"], config.repo_root),
        ("git_fetch", ["git", "fetch", "origin"], config.repo_root),
    ]
    results: list[dict[str, Any]] = []
    failed = False
    for name, command, cwd in checks:
        try:
            completed = run_command(command, cwd, None)
            stdout = completed.stdout.strip()
            stderr = completed.stderr.strip()
            results.append({"name": name, "ok": True, "stdout": stdout, "stderr": stderr})
            if name == "git_status" and stdout and not config.allow_dirty:
                failed = True
                results[-1]["ok"] = False
                results[-1]["reason"] = "working tree is not clean"
            if (
                name == "codex_version"
                and config.expected_codex_version
                and config.expected_codex_version not in stdout
            ):
                failed = True
                results[-1]["ok"] = False
                results[-1]["reason"] = (
                    f"expected Codex version containing {config.expected_codex_version!r}"
                )
        except Exception as exc:  # noqa: BLE001 - preflight reports all checks.
            failed = True
            results.append({"name": name, "ok": False, "reason": str(exc)})
    print(json.dumps(results, indent=2))
    return 1 if failed else 0


def run_self_test() -> int:
    """Run a local parser/decoder self-test without GitHub or Codex."""

    patch = (
        b"diff --git a/example.txt b/example.txt\n"
        b"--- a/example.txt\n"
        b"+++ b/example.txt\n"
        b"@@ -1 +1 @@\n"
        b"-old\n"
        b"+new\n"
    )
    body = make_ai_patch_comment(
        repo="owner/repo",
        base_branch="main",
        target_branch="work/self-test",
        scope="self-test patch",
        raw_patch=patch,
    )
    parsed = parse_ai_patch_body(body)
    assert parsed.raw_patch == patch
    assert parsed.repo == "owner/repo"
    print("AI_PATCH_V1 self-test passed.")
    return 0


def run_command(
    command: Sequence[str], cwd: Path | None = None, input_text: str | None = None
) -> subprocess.CompletedProcess[str]:
    """Run a command and raise with stdout/stderr included on failure."""

    completed = subprocess.run(
        list(command),
        cwd=str(cwd) if cwd is not None else None,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AiPatchError(
            f"command failed ({completed.returncode}): {shlex.join(command)}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return completed


def _parse_gh_api_json_pages(stdout: str) -> list[Any]:
    """Parse gh api output, including paginated JSON arrays when gh concatenates pages."""

    text = stdout.strip()
    if not text:
        return []
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        values: list[Any] = []
        index = 0
        while index < len(text):
            while index < len(text) and text[index].isspace():
                index += 1
            if index >= len(text):
                break
            value, index = decoder.raw_decode(text, index)
            values.append(value)
        payload = values
    if isinstance(payload, list) and all(isinstance(page, list) for page in payload):
        return [item for page in payload for item in page]
    if isinstance(payload, list):
        return payload
    raise AiPatchError("gh api comments payload was not a list")


def _should_process_comment(comment: IssueComment, config: BridgeConfig) -> bool:
    """Return true when an inbox comment belongs to this local-Codex bridge."""

    if not comment.body.startswith(AI_PATCH_HEADER):
        return False
    try:
        metadata = _parse_metadata(comment.body)
    except Exception:
        return True
    executor = metadata.get("executor", "")
    return executor in config.accepted_executors


def _parse_metadata(body: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if line == PAYLOAD_BEGIN:
            break
        if not line or line == AI_PATCH_HEADER or line.startswith("-"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata


def _validate_required_metadata(metadata: dict[str, str]) -> None:
    required = [
        "repo",
        "base_branch",
        "target_branch",
        "scope",
        "payload_encoding",
        "payload_raw_sha256",
        "payload_gzip_sha256",
        "executor",
    ]
    missing = [key for key in required if not metadata.get(key)]
    if missing:
        raise AiPatchError(f"missing required metadata: {', '.join(missing)}")


def _validate_branch(branch_key: str, branch: str, *, required_prefix: str | None) -> None:
    if not BRANCH_RE.fullmatch(branch):
        raise AiPatchError(f"invalid {branch_key}: {branch!r}")
    if any(token in branch for token in ("..", "@{", "\\", "//", " ")):
        raise AiPatchError(f"unsafe {branch_key}: {branch!r}")
    if required_prefix is not None and not branch.startswith(required_prefix):
        raise AiPatchError(f"{branch_key} must start with {required_prefix}")


def _validate_policy_metadata(metadata: dict[str, str]) -> None:
    executor = metadata.get("executor", LOCAL_CODEX_EXECUTOR)
    if executor not in SUPPORTED_EXECUTORS:
        raise AiPatchError(f"unsupported executor: {executor!r}")
    commit_policy = metadata.get("commit_policy", "single_commit")
    if commit_policy not in SUPPORTED_COMMIT_POLICIES:
        raise AiPatchError(f"unsupported commit_policy: {commit_policy!r}")
    test_policy = metadata.get("test_policy", "required")
    if test_policy not in SUPPORTED_TEST_POLICIES:
        raise AiPatchError(f"unsupported test_policy: {test_policy!r}")
    if executor == RESCUE_BRANCH_EXECUTOR and test_policy != "rescue_unvetted":
        raise AiPatchError("rescue-branch executor requires test_policy rescue_unvetted")


def _validate_target_branch_for_executor(metadata: dict[str, str]) -> None:
    executor = metadata.get("executor", LOCAL_CODEX_EXECUTOR)
    target_branch = metadata["target_branch"]
    if executor == RESCUE_BRANCH_EXECUTOR:
        _validate_branch("target_branch", target_branch, required_prefix="rescue/")
        return
    _validate_branch("target_branch", target_branch, required_prefix="work/")


def _verify_byte_count(name: str, expected_value: str, actual: int) -> None:
    try:
        expected = int(expected_value)
    except ValueError as exc:
        raise AiPatchError(f"{name} must be an integer") from exc
    if expected != actual:
        raise AiPatchError(f"{name} mismatch")


def _ensure_dirs(config: BridgeConfig) -> None:
    config.resolved_state_dir().mkdir(parents=True, exist_ok=True)
    config.resolved_runs_dir().mkdir(parents=True, exist_ok=True)


def _resolve_under_repo(repo_root: Path, path: Path) -> Path:
    return path if path.is_absolute() else repo_root / path


def _load_processed(state_dir: Path) -> dict[str, Any]:
    ledger_path = state_dir / "processed_comments.json"
    if not ledger_path.exists():
        return {}
    return json.loads(ledger_path.read_text(encoding="utf-8"))


def _save_processed(state_dir: Path, processed: dict[str, Any]) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = state_dir / "processed_comments.json"
    tmp_path = ledger_path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(processed, indent=2, sort_keys=True), encoding="utf-8")
    tmp_path.replace(ledger_path)


def _build_manifest(
    comment: IssueComment,
    message: AiPatchMessage,
    config: BridgeConfig,
    patch_path: Path,
    run_dir: Path,
) -> dict[str, Any]:
    return {
        "schema": "LOCAL_CODEX_RUN_MANIFEST_V1",
        "source_comment_id": comment.comment_id,
        "source_comment_url": comment.url,
        "repo": message.repo,
        "base_branch": message.base_branch,
        "target_branch": message.target_branch,
        "scope": message.scope,
        "executor": message.metadata.get("executor", LOCAL_CODEX_EXECUTOR),
        "commit_policy": message.metadata.get("commit_policy", "single_commit"),
        "test_policy": message.metadata.get("test_policy", "required"),
        "run_dir": str(run_dir),
        "patch_path": str(patch_path),
        "payload_raw_sha256": message.raw_sha256,
        "payload_gzip_sha256": message.gzip_sha256,
        "local_checks": list(config.local_checks),
        "prohibited_paths": [
            ".github/workflows/**",
            ".git/**",
            ".ai_patch_bridge/state/**",
        ],
        "required_outputs": ["codex_receipt.md"],
    }


def _prepare_target_branch(message: AiPatchMessage, config: BridgeConfig) -> None:
    repo_root = config.repo_root

    # Fetch first. This is deliberate: ChatGPT may have already committed directly
    # to GitHub, so the local executor must anchor itself on the latest remote
    # truth before fitting a patch.
    run_command(["git", "fetch", "--prune", "origin"], repo_root, None)

    status = run_command(["git", "status", "--short"], repo_root, None).stdout.strip()
    if status and not config.allow_dirty:
        raise AiPatchError("working tree is not clean")

    existing_branch = subprocess.run(
        ["git", "ls-remote", "--exit-code", "--heads", "origin", message.target_branch],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
        check=False,
    )
    if existing_branch.returncode == 0:
        raise AiPatchError(f"target branch already exists on origin: {message.target_branch}")

    remote_base = f"origin/{message.base_branch}"
    run_command(["git", "rev-parse", "--verify", remote_base], repo_root, None)
    run_command(["git", "switch", "--detach", remote_base], repo_root, None)
    run_command(["git", "switch", "-c", message.target_branch], repo_root, None)


def _build_codex_prompt(manifest_path: Path, manifest: dict[str, Any]) -> str:
    checks = "\n".join(f"- `{command}`" for command in manifest["local_checks"])
    prohibited = "\n".join(f"- `{path}`" for path in manifest["prohibited_paths"])
    return f"""# LOCAL_CODEX_EXECUTOR_TASK_V1

You are the authorised local Codex executor for an AI_PATCH_V1 inbox comment.

Read AGENTS.md before editing. Then read this run manifest:

`{manifest_path}`

## Objective

Apply or fit the decoded patch intent to this repo, run the declared checks,
and write the required Codex receipt. Do not run `git add`, `git commit`, or
`git push`; the outer bridge process owns Git commit and push after Codex exits.

## Execution policy

- Executor: `{manifest["executor"]}`
- Commit policy: `{manifest["commit_policy"]}`
- Test policy: `{manifest["test_policy"]}`

## Branch

- Base branch: `{manifest["base_branch"]}`
- Target branch: `{manifest["target_branch"]}`

The bridge has already fetched `origin` and created the target branch from
`origin/{manifest["base_branch"]}`. Before editing, confirm the worktree and
remote are sane with read-only commands such as `git status --short` and
`git log --oneline -1`. Do not switch branches except for inspection commands
that restore the target branch before editing.

## Patch

Decoded patch path:

`{manifest["patch_path"]}`

If the patch applies cleanly, apply it. If it does not apply cleanly, make the
smallest lawful adjustment that preserves intent.

## Checks to run

{checks}

## Prohibited paths

{prohibited}

## Required finish state

1. Intended file changes exist in the worktree on `{manifest["target_branch"]}`.
2. The declared local checks have been run by Codex.
3. A receipt file exists at `{Path(manifest_path).parent / "codex_receipt.md"}`.
4. Codex has not attempted to commit or push.
5. The outer bridge will re-run checks, stage declared paths, commit, push, and post the final receipt.

Stop and write a receipt if you cannot satisfy these conditions within scope.
"""


def _invoke_codex(config: BridgeConfig, prompt_path: Path) -> None:
    command = shlex.split(os.environ.get("AI_PATCH_BRIDGE_CODEX_COMMAND", config.codex_command))
    prompt = prompt_path.read_text(encoding="utf-8")
    log_path = prompt_path.with_name("codex_stdout_stderr.log")
    completed = subprocess.run(
        command,
        cwd=str(config.repo_root),
        input=prompt,
        text=True,
        capture_output=True,
        check=False,
    )
    log_path.write_text(
        f"COMMAND: {shlex.join(command)}\n"
        f"RETURN_CODE: {completed.returncode}\n\n"
        f"STDOUT:\n{completed.stdout}\n\nSTDERR:\n{completed.stderr}\n",
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise AiPatchError(f"Codex command failed; see {log_path}")


def _build_success_or_stop_receipt(
    config: BridgeConfig,
    comment_id: int,
    target_branch: str,
    raw_patch: bytes | None = None,
    scope: str | None = None,
) -> dict[str, Any]:
    """Build the final receipt after Codex exits.

    Codex may be sandboxed with `.git` mounted read-only. The outer bridge owns
    Git staging, commit, push, and final origin verification.
    """

    repo_root = config.repo_root
    current_branch = run_command(
        ["git", "branch", "--show-current"], repo_root, None
    ).stdout.strip()
    status = run_command(["git", "status", "--short"], repo_root, None).stdout.strip()
    head_sha = run_command(["git", "rev-parse", "HEAD"], repo_root, None).stdout.strip()
    receipt_path = config.resolved_runs_dir() / str(comment_id) / "codex_receipt.md"

    if current_branch != target_branch:
        return {
            "status": "stopped",
            "lines": [
                f"reason: current branch {current_branch!r} does not match target {target_branch!r}",
                f"head_sha: {head_sha}",
            ],
        }

    if not receipt_path.exists():
        return {
            "status": "stopped",
            "lines": [
                "reason: Codex did not write required codex_receipt.md",
                f"head_sha: {head_sha}",
            ],
        }

    if status:
        if raw_patch is None or scope is None:
            return {
                "status": "stopped",
                "lines": [
                    "reason: worktree is not clean after Codex execution",
                    "git_status:",
                    status,
                ],
            }

        commit_result = _commit_and_push_declared_patch_paths(
            config=config,
            raw_patch=raw_patch,
            target_branch=target_branch,
            scope=scope,
            comment_id=comment_id,
        )
        if commit_result is not None:
            return commit_result

        status = run_command(["git", "status", "--short"], repo_root, None).stdout.strip()
        head_sha = run_command(["git", "rev-parse", "HEAD"], repo_root, None).stdout.strip()

        if status:
            return {
                "status": "stopped",
                "lines": [
                    "reason: worktree is not clean after outer bridge commit/push",
                    "git_status:",
                    status,
                ],
            }

    remote_head = _remote_branch_head(repo_root, target_branch)
    if remote_head != head_sha:
        return {
            "status": "stopped",
            "lines": [
                "reason: pushed branch was not verified on origin",
                f"local_head_sha: {head_sha}",
                f"remote_head_sha: {remote_head or 'missing'}",
            ],
        }

    receipt_note = receipt_path.read_text(encoding="utf-8")
    return {
        "status": "pushed",
        "lines": [
            f"target_branch: {target_branch}",
            f"head_sha: {head_sha}",
            f"codex_receipt_path: {receipt_path}",
            "codex_receipt:",
            receipt_note,
        ],
    }


def _commit_and_push_declared_patch_paths(
    *,
    config: BridgeConfig,
    raw_patch: bytes,
    target_branch: str,
    scope: str,
    comment_id: int,
) -> dict[str, Any] | None:
    """Run checks, stage decoded patch paths, commit, and push outside Codex."""

    check_result = _run_outer_local_checks(config, comment_id)
    if check_result is not None:
        return check_result

    changed_paths = _changed_paths_from_patch(raw_patch)
    if not changed_paths:
        return {
            "status": "stopped",
            "lines": ["reason: decoded patch did not declare changed paths"],
        }

    for path in changed_paths:
        run_command(["git", "add", "--", path], config.repo_root, None)

    staged = run_command(
        ["git", "diff", "--cached", "--name-only"], config.repo_root, None
    ).stdout.strip()

    if not staged:
        return {
            "status": "stopped",
            "lines": [
                "reason: no decoded patch paths were staged after Codex execution",
                "declared_paths:",
                *changed_paths,
            ],
        }

    commit_message = f"Apply AI patch: {' '.join(scope.split())[:72]}"
    run_command(["git", "commit", "-m", commit_message], config.repo_root, None)
    run_command(["git", "push", "-u", "origin", target_branch], config.repo_root, None)
    return None


def _run_outer_local_checks(config: BridgeConfig, comment_id: int) -> dict[str, Any] | None:
    """Run declared local checks outside the Codex sandbox before commit."""

    log_path = config.resolved_runs_dir() / str(comment_id) / "outer_local_checks.log"
    log_parts: list[str] = []

    for command in config.local_checks:
        completed = subprocess.run(
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
                "lines": [
                    "reason: outer bridge local check failed after Codex execution",
                    f"failed_check: {command}",
                    f"log_path: {log_path}",
                ],
            }

    log_path.write_text("\n---\n".join(log_parts), encoding="utf-8")
    return None


def _changed_paths_from_patch(raw_patch: bytes) -> list[str]:
    """Return repository paths declared by diff --git headers."""

    paths: list[str] = []
    seen: set[str] = set()

    for line in raw_patch.decode("utf-8", errors="replace").splitlines():
        if not line.startswith("diff --git "):
            continue

        parts = line.split()
        if len(parts) < 4:
            continue

        path = parts[3]
        if path.startswith("b/"):
            path = path[2:]

        if path != "/dev/null" and path not in seen:
            seen.add(path)
            paths.append(path)

    return paths


def _remote_branch_head(repo_root: Path, target_branch: str) -> str | None:
    """Return the remote branch head SHA, or None when the branch is absent."""

    completed = subprocess.run(
        ["git", "ls-remote", "--heads", "origin", target_branch],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        return None
    return completed.stdout.split()[0]


def _post_receipt(
    config: BridgeConfig,
    comment_id: int,
    *,
    status: str,
    body_lines: Iterable[str],
) -> None:
    receipt_path = config.resolved_runs_dir() / str(comment_id) / "github_receipt.md"
    receipt_body = "\n".join(
        [
            RECEIPT_HEADER,
            f"source_comment_id: {comment_id}",
            f"status: {status}",
            *body_lines,
            "",
        ]
    )
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(receipt_body, encoding="utf-8")
    if config.dry_run:
        print(receipt_body)
        return
    run_command(
        [
            "gh",
            "issue",
            "comment",
            str(config.issue_number),
            "--repo",
            config.repo,
            "--body-file",
            str(receipt_path),
        ],
        config.repo_root,
        None,
    )


def _safe_failure_receipt(comment: IssueComment, config: BridgeConfig, reason: str) -> None:
    try:
        _post_receipt(config, comment.comment_id, status="failed", body_lines=[f"reason: {reason}"])
    except Exception as exc:  # noqa: BLE001 - do not mask original failure with receipt failure.
        print(f"Failed to post failure receipt: {exc}", file=sys.stderr)


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(description="Local AI_PATCH_V1 GitHub issue inbox bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--repo", required=True, help="GitHub repo in owner/name form")
        subparser.add_argument(
            "--issue-number",
            type=int,
            required=True,
            help="AI_PATCH_INBOX issue number",
        )
        subparser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Local repo root")
        subparser.add_argument("--state-dir", type=Path, default=Path(DEFAULT_STATE_DIR))
        subparser.add_argument("--runs-dir", type=Path, default=Path(DEFAULT_RUNS_DIR))
        subparser.add_argument("--allow-dirty", action="store_true")
        subparser.add_argument("--dry-run", action="store_true")
        subparser.add_argument(
            "--local-check",
            action="append",
            dest="local_checks",
            help="Local check command; may be supplied more than once",
        )
        subparser.add_argument(
            "--accepted-executor",
            action="append",
            dest="accepted_executors",
            choices=SUPPORTED_EXECUTORS,
            help="Executor kind this bridge may consume; default is local-codex",
        )

    once = subparsers.add_parser("once", help="Process new AI_PATCH_V1 comments once")
    add_common(once)

    watch = subparsers.add_parser("watch", help="Continuously poll the inbox")
    add_common(watch)
    watch.add_argument("--poll-seconds", type=int, default=60)

    preflight = subparsers.add_parser("preflight", help="Run local bridge environment checks")
    add_common(preflight)
    preflight.add_argument("--expected-codex-version")

    decode = subparsers.add_parser(
        "decode",
        help="Decode and verify a local AI_PATCH_V1 comment file",
    )
    decode.add_argument("comment_file", type=Path)
    decode.add_argument("--out", type=Path, default=Path("incoming.patch"))

    make_comment = subparsers.add_parser(
        "make-comment",
        help="Create an AI_PATCH_V1 comment from a patch",
    )
    make_comment.add_argument("--repo", required=True)
    make_comment.add_argument("--base-branch", required=True)
    make_comment.add_argument("--target-branch", required=True)
    make_comment.add_argument("--scope", required=True)
    make_comment.add_argument("--patch-file", type=Path, required=True)
    make_comment.add_argument("--out", type=Path, required=True)
    make_comment.add_argument("--executor", default=LOCAL_CODEX_EXECUTOR, choices=SUPPORTED_EXECUTORS)
    make_comment.add_argument("--commit-policy", default="single_commit", choices=SUPPORTED_COMMIT_POLICIES)
    make_comment.add_argument("--test-policy", default="required", choices=SUPPORTED_TEST_POLICIES)

    subparsers.add_parser("self-test", help="Run parser/decoder self-test")
    return parser


def config_from_args(args: argparse.Namespace) -> BridgeConfig:
    """Create BridgeConfig from argparse namespace."""

    return BridgeConfig(
        repo=args.repo,
        issue_number=args.issue_number,
        repo_root=args.repo_root.resolve(),
        state_dir=args.state_dir,
        runs_dir=args.runs_dir,
        local_checks=tuple(args.local_checks or DEFAULT_LOCAL_CHECKS),
        poll_seconds=getattr(args, "poll_seconds", 60),
        expected_codex_version=getattr(args, "expected_codex_version", None),
        allow_dirty=args.allow_dirty,
        dry_run=args.dry_run,
        accepted_executors=tuple(args.accepted_executors or (LOCAL_CODEX_EXECUTOR,)),
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""

    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if args.command == "self-test":
        return run_self_test()
    if args.command == "decode":
        body = args.comment_file.read_text(encoding="utf-8")
        message = parse_ai_patch_body(body)
        args.out.write_bytes(message.raw_patch)
        print(json.dumps(message.metadata, indent=2, sort_keys=True))
        return 0
    if args.command == "make-comment":
        body = make_ai_patch_comment(
            repo=args.repo,
            base_branch=args.base_branch,
            target_branch=args.target_branch,
            scope=args.scope,
            raw_patch=args.patch_file.read_bytes(),
            executor=args.executor,
            commit_policy=args.commit_policy,
            test_policy=args.test_policy,
        )
        args.out.write_text(body, encoding="utf-8")
        print(args.out)
        return 0

    config = config_from_args(args)
    if args.command == "preflight":
        return run_preflight(config)
    if args.command == "once":
        return run_once(config)
    if args.command == "watch":
        run_watch(config)
        return 0
    raise AssertionError(f"unhandled command {args.command!r}")
