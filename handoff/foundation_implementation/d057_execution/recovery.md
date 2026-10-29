# D057 strict invocation recovery — output-capture repair

Initial strict invocation returned exit2 before collection: `FAIL: worktree is not clean before product-proof aggregate`. Complete original output is initial_failure.log. Zero cases executed; no semantic/runtime outcome was obtained.

Observed cause: the command's shell redirection created an untracked in-repository output file before the runner checked its required clean-worktree invariant. The runner correctly stopped. This is a capture-path defect, not a product failure; no shared runner changes are authorised or made.

Relevant material repair: preserve/commit original failure and this record, then capture the same aggregate's stdout/stderr to an absolute path OUTSIDE the repository and copy the complete output into the execution evidence directory only after the process exits. Confirm clean status immediately before invocation. Source, proof, generation and runner bytes remain unchanged. The same independent reviewer remains sole executor. This is failed-check recovery following a documented material repair under root §8; it is not a rerun of successful evidence. Subsequent signals use this repaired capture path from their first invocation.
