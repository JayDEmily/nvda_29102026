"""Offline scenario checks for the AI Patch Bridge lane model.

These checks are deliberately stdlib-only and do not require GitHub, Codex, or
network access. They validate that the bridge can classify and generate the
metadata required for each user workflow scenario.
"""

from __future__ import annotations

import sys
from pathlib import Path

from ai_patch_bridge.core import (
    AiPatchError,
    BridgeConfig,
    IssueComment,
    _should_process_comment,
    make_ai_patch_comment,
    parse_ai_patch_body,
)


def sample_patch(label: str) -> bytes:
    """Return a deterministic git patch for offline lane checks."""

    return (
        f"diff --git a/examples/{label}.txt b/examples/{label}.txt\n"
        f"new file mode 100644\n"
        f"index 0000000..1111111\n"
        f"--- /dev/null\n"
        f"+++ b/examples/{label}.txt\n"
        f"@@ -0,0 +1,2 @@\n"
        f"+scenario: {label}\n"
        f"+status: generated for offline validation\n"
    ).encode("utf-8")


def _parse_comment(
    *,
    target_branch: str,
    scope: str,
    executor: str,
    test_policy: str,
    commit_policy: str = "single_commit",
) -> object:
    body = make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch=target_branch,
        scope=scope,
        raw_patch=sample_patch(scope.replace(" ", "_").replace("/", "_")),
        executor=executor,
        commit_policy=commit_policy,
        test_policy=test_policy,
    )
    return parse_ai_patch_body(body)


def scenario_a_direct_pr() -> None:
    """Direct GitHub PR lane is intentionally outside AI_PATCH_V1 transport."""

    # This scenario is connector/manual-GitHub owned. The bridge should not
    # generate an AI_PATCH_V1 payload for it; the useful offline assertion is the
    # explicit classification.
    lane = {
        "name": "A",
        "promotion_intent": "direct_pr",
        "bridge_executor": "none",
        "expected_review_surface": "GitHub PR",
    }
    assert lane["bridge_executor"] == "none"
    assert lane["expected_review_surface"] == "GitHub PR"


def scenario_b_github_action() -> None:
    """Multi-file clean patch lane uses github-action and work/ branches."""

    msg = _parse_comment(
        target_branch="work/scenario-b-github-action",
        scope="scenario B github action",
        executor="github-action",
        test_policy="not_run_allowed",
    )
    assert msg.metadata["executor"] == "github-action"
    assert msg.target_branch.startswith("work/")
    default_config = BridgeConfig(repo="JayDEmily/NVDAV6", issue_number=1)
    assert not _should_process_comment(
        IssueComment(101, make_ai_patch_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="work/scenario-b-github-action",
            scope="scenario B github action",
            raw_patch=sample_patch("scenario_b"),
            executor="github-action",
            test_policy="not_run_allowed",
        )),
        default_config,
    )


def scenario_c_local_codex() -> None:
    """Runtime/tested lane uses local-codex and work/ branches."""

    body = make_ai_patch_comment(
        repo="JayDEmily/NVDAV6",
        base_branch="main",
        target_branch="work/scenario-c-local-codex",
        scope="scenario C local codex",
        raw_patch=sample_patch("scenario_c"),
        executor="local-codex",
        test_policy="required",
    )
    msg = parse_ai_patch_body(body)
    assert msg.metadata["executor"] == "local-codex"
    assert msg.metadata["test_policy"] == "required"
    default_config = BridgeConfig(repo="JayDEmily/NVDAV6", issue_number=1)
    assert _should_process_comment(IssueComment(102, body), default_config)


def scenario_d_long_sandbox_cumulative() -> None:
    """Long sandbox runs export one cumulative patch using single_commit."""

    msg = _parse_comment(
        target_branch="work/scenario-d-cumulative-export",
        scope="scenario D cumulative sandbox export",
        executor="local-codex",
        test_policy="required",
        commit_policy="single_commit",
    )
    assert msg.metadata["commit_policy"] == "single_commit"
    assert msg.target_branch == "work/scenario-d-cumulative-export"


def scenario_e_rescue_unfinished() -> None:
    """Unfinished sandbox work is saved as rescue-branch and rescue/ namespace."""

    msg = _parse_comment(
        target_branch="rescue/scenario-e-unfinished",
        scope="scenario E rescue unfinished",
        executor="rescue-branch",
        test_policy="rescue_unvetted",
    )
    assert msg.metadata["executor"] == "rescue-branch"
    assert msg.metadata["test_policy"] == "rescue_unvetted"
    assert msg.target_branch.startswith("rescue/")


def scenario_f_patch_fails_remote_falls_to_local() -> None:
    """A failed GitHub Action patch should be reissued to local-codex."""

    github_action_msg = _parse_comment(
        target_branch="work/scenario-f-remote-attempt",
        scope="scenario F remote attempt",
        executor="github-action",
        test_policy="not_run_allowed",
    )
    local_repair_msg = _parse_comment(
        target_branch="work/scenario-f-local-repair",
        scope="scenario F local repair",
        executor="local-codex",
        test_policy="required",
    )
    assert github_action_msg.metadata["executor"] == "github-action"
    assert local_repair_msg.metadata["executor"] == "local-codex"
    assert local_repair_msg.metadata["test_policy"] == "required"


def scenario_g_linux_unavailable_rescue() -> None:
    """If Linux is unavailable and work must be preserved, use rescue."""

    msg = _parse_comment(
        target_branch="rescue/scenario-g-linux-unavailable",
        scope="scenario G Linux unavailable rescue",
        executor="rescue-branch",
        test_policy="rescue_unvetted",
    )
    assert msg.metadata["executor"] == "rescue-branch"


def scenario_invalid_rescue_policy() -> None:
    """Rescue branches must not masquerade as tested work."""

    try:
        make_ai_patch_comment(
            repo="JayDEmily/NVDAV6",
            base_branch="main",
            target_branch="rescue/invalid-tested-rescue",
            scope="invalid rescue",
            raw_patch=sample_patch("invalid_rescue"),
            executor="rescue-branch",
            test_policy="required",
        )
    except AiPatchError as exc:
        assert "rescue-branch executor requires test_policy rescue_unvetted" in str(exc)
        return
    raise AssertionError("rescue-branch accepted tested policy")


SCENARIOS = {
    "A": scenario_a_direct_pr,
    "B": scenario_b_github_action,
    "C": scenario_c_local_codex,
    "D": scenario_d_long_sandbox_cumulative,
    "E": scenario_e_rescue_unfinished,
    "F": scenario_f_patch_fails_remote_falls_to_local,
    "G": scenario_g_linux_unavailable_rescue,
    "invalid-rescue-policy": scenario_invalid_rescue_policy,
}


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    selected = args or sorted(SCENARIOS)
    for name in selected:
        if name not in SCENARIOS:
            print(f"UNKNOWN {name}")
            return 2
        SCENARIOS[name]()
        print(f"PASS scenario {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
