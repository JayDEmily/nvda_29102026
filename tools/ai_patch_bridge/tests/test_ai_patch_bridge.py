from __future__ import annotations

import contextlib
import io
import json
import re
import tempfile
from collections.abc import Callable
from pathlib import Path

from ai_patch_bridge import core
from ai_patch_bridge.core import (
    AiPatchError,
    BridgeConfig,
    IssueComment,
    _parse_gh_api_json_pages,
    _prepare_target_branch,
    _should_process_comment,
    main as bridge_main,
    make_ai_patch_comment,
    parse_ai_patch_body,
)
from ai_patch_bridge.scenario_tests import main as scenario_main


def sample_patch() -> bytes:
    return (
        b"diff --git a/mock_target.py b/mock_target.py\n"
        b"--- a/mock_target.py\n"
        b"+++ b/mock_target.py\n"
        b"@@ -1,4 +1,4 @@\n"
        b" def value() -> str:\n"
        b"-    return 'old'\n"
        b"+    return 'new'\n"
    )


def assert_raises_regex(
    exc_type: type[BaseException],
    pattern: str,
    func: Callable[[], object],
) -> None:
    try:
        func()
    except exc_type as exc:
        if not re.search(pattern, str(exc)):
            raise AssertionError(f"expected {pattern!r} in {exc!r}") from exc
        return
    raise AssertionError(f"expected {exc_type.__name__}")


def test_make_and_parse_ai_patch_comment_round_trip() -> None:
    body = make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/round-trip-test",
        scope="round trip parser test",
        raw_patch=sample_patch(),
    )

    parsed = parse_ai_patch_body(body)

    assert parsed.repo == "JayDEmily/NVDAV6"
    assert parsed.base_branch == "main"
    assert parsed.target_branch == "work/round-trip-test"
    assert parsed.scope == "round trip parser test"
    assert parsed.raw_patch == sample_patch()
    assert parsed.metadata["payload_raw_bytes"] == str(len(sample_patch()))


def test_rejects_target_branch_outside_work_namespace() -> None:
    assert_raises_regex(
        AiPatchError,
        "target_branch must start with work/",
        lambda: make_ai_patch_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="main",
            scope="bad branch",
            raw_patch=sample_patch(),
        ),
    )


def test_rejects_hash_mismatch() -> None:
    body = make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/hash-test",
        scope="hash mismatch test",
        raw_patch=sample_patch(),
    )
    tampered = body.replace("payload_raw_sha256: ", "payload_raw_sha256: 0000")

    assert_raises_regex(
        AiPatchError,
        "payload_raw_sha256 mismatch",
        lambda: parse_ai_patch_body(tampered),
    )


def test_cli_make_comment_and_decode() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        patch_path = tmp_dir / "incoming.patch"
        comment_path = tmp_dir / "comment.md"
        decoded_path = tmp_dir / "decoded.patch"
        patch_path.write_bytes(sample_patch())

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            make_rc = bridge_main(
                [
                    "make-comment",
                    "--repo",
                    "JayDEmily/NVDAV6",
                    "--base-branch",
                    "main",
                    "--target-branch",
                    "work/cli-test",
                    "--scope",
                    "CLI test",
                    "--patch-file",
                    str(patch_path),
                    "--out",
                    str(comment_path),
                ]
            )
        assert make_rc == 0
        assert comment_path.exists()

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            decode_rc = bridge_main(
                ["decode", str(comment_path), "--out", str(decoded_path)]
            )
        assert decode_rc == 0
        assert decoded_path.read_bytes() == sample_patch()


def test_parse_gh_api_concatenated_paginated_arrays() -> None:
    payload = '[{"id": 1, "body": "a"}] [{"id": 2, "body": "b"}]'

    assert _parse_gh_api_json_pages(payload) == [
        {"id": 1, "body": "a"},
        {"id": 2, "body": "b"},
    ]


def test_local_bridge_skips_github_action_executor_comments() -> None:
    body = make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/local-only-test",
        scope="executor filter test",
        raw_patch=sample_patch(),
    )
    action_body = body.replace("executor: local-codex", "executor: github-action")
    config = BridgeConfig(repo="JayDEmily/NVDAV6", issue_number=1)

    assert _should_process_comment(IssueComment(1, body, user_login="JayDEmily"), config)
    assert not _should_process_comment(
        IssueComment(2, action_body, user_login="JayDEmily"), config
    )


def test_rescue_branch_mode_uses_rescue_namespace_and_unvetted_policy() -> None:
    body = make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="rescue/20260428-sandbox-save",
        scope="preserve unvetted sandbox work",
        raw_patch=sample_patch(),
        executor="rescue-branch",
        test_policy="rescue_unvetted",
    )

    parsed = parse_ai_patch_body(body)

    assert parsed.target_branch == "rescue/20260428-sandbox-save"
    assert parsed.metadata["executor"] == "rescue-branch"
    assert parsed.metadata["test_policy"] == "rescue_unvetted"


def test_rescue_branch_mode_rejects_work_namespace() -> None:
    assert_raises_regex(
        AiPatchError,
        "target_branch must start with rescue/",
        lambda: make_ai_patch_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="work/not-a-rescue-branch",
            scope="bad rescue branch",
            raw_patch=sample_patch(),
            executor="rescue-branch",
            test_policy="rescue_unvetted",
        ),
    )


def test_rescue_branch_mode_requires_unvetted_policy() -> None:
    assert_raises_regex(
        AiPatchError,
        "rescue-branch executor requires test_policy rescue_unvetted",
        lambda: make_ai_patch_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="rescue/missing-unvetted-policy",
            scope="bad rescue policy",
            raw_patch=sample_patch(),
            executor="rescue-branch",
        ),
    )


def test_local_bridge_can_be_configured_to_accept_rescue_executor() -> None:
    body = make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="rescue/configured-rescue",
        scope="configured rescue executor filter",
        raw_patch=sample_patch(),
        executor="rescue-branch",
        test_policy="rescue_unvetted",
    )
    default_config = BridgeConfig(repo="JayDEmily/NVDAV6", issue_number=1)
    rescue_config = BridgeConfig(
        repo="JayDEmily/NVDAV6",
        issue_number=1,
        accepted_executors=("local-codex", "rescue-branch"),
    )

    assert not _should_process_comment(IssueComment(3, body, user_login="JayDEmily"), default_config)
    assert _should_process_comment(IssueComment(4, body, user_login="JayDEmily"), rescue_config)


def test_prepare_target_branch_fetches_latest_origin_before_branch_creation() -> None:
    body = make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/fetch-first",
        scope="fetch first target branch prep",
        raw_patch=sample_patch(),
    )
    message = parse_ai_patch_body(body)
    commands: list[list[str]] = []

    def fake_run_command(command: list[str], cwd: Path | None = None, input_text: str | None = None):
        commands.append(list(command))
        stdout = ""
        if command == ["git", "status", "--short"]:
            stdout = ""
        return core.subprocess.CompletedProcess(command, 0, stdout, "")

    def fake_subprocess_run(command, cwd=None, text=None, capture_output=None, check=None, input=None):
        commands.append(list(command))
        return core.subprocess.CompletedProcess(command, 2, "", "")

    old_run_command = core.run_command
    old_subprocess_run = core.subprocess.run
    try:
        core.run_command = fake_run_command  # type: ignore[assignment]
        core.subprocess.run = fake_subprocess_run  # type: ignore[assignment]
        _prepare_target_branch(message, BridgeConfig(repo="JayDEmily/NVDAV6", issue_number=1, repo_root=Path(".")))
    finally:
        core.run_command = old_run_command  # type: ignore[assignment]
        core.subprocess.run = old_subprocess_run  # type: ignore[assignment]

    assert commands[0] == ["git", "fetch", "--prune", "origin"]
    assert ["git", "switch", "--detach", "origin/main"] in commands
    assert commands[-1] == ["git", "switch", "-c", "work/fetch-first"]



def test_changed_paths_from_patch_lists_declared_targets() -> None:
    patch = (
        b"diff --git a/alpha.txt b/alpha.txt\n"
        b"--- a/alpha.txt\n"
        b"+++ b/alpha.txt\n"
        b"@@ -1 +1 @@\n"
        b"-old\n"
        b"+new\n"
        b"diff --git a/docs/probe.md b/docs/probe.md\n"
        b"new file mode 100644\n"
        b"--- /dev/null\n"
        b"+++ b/docs/probe.md\n"
        b"@@ -0,0 +1 @@\n"
        b"+probe\n"
    )

    assert core._changed_paths_from_patch(patch) == ["alpha.txt", "docs/probe.md"]


def test_codex_prompt_assigns_commit_and_push_to_outer_bridge() -> None:
    manifest_path = Path("/tmp/run/manifest.json")
    manifest = {
        "target_branch": "work/outer-git-owner",
        "base_branch": "main",
        "executor": "local-codex",
        "commit_policy": "single_commit",
        "test_policy": "required",
        "local_checks": ["make scaffold-check"],
        "prohibited_paths": [".git/**"],
        "patch_path": "/tmp/run/incoming.patch",
    }

    prompt = core._build_codex_prompt(manifest_path, manifest)

    assert "outer bridge process owns Git commit and push" in prompt
    assert "Codex has not attempted to commit or push" in prompt


def test_all_offline_scenario_checks_pass() -> None:
    assert scenario_main([]) == 0
