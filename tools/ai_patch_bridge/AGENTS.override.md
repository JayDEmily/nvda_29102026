# AGENTS.override.md

## Scope

This file applies to the bridge tooling tree rooted at `tools/ai_patch_bridge/`.

This file and `PLANS.md` are bridge-local control surfaces only. They do not define NVDA trading-system doctrine.

The repo-level bridge blueprint is:

```text
project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
```

Read that blueprint before changing bridge publication rules, payload routing, receipt behaviour, proof-block execution, or Codex handoff behaviour.

## Bridge operating law

- Treat bridge-local `pyproject.toml` as the bridge Python environment authority.
- Treat bridge-local `Makefile` as the bridge executable gate authority.
- Treat this `AGENTS.override.md` as the Codex behavioural authority for bridge tooling work.
- Treat `project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md` as the repo-level bridge workflow doctrine when it conflicts with older bridge-local PR/review assumptions.
- Treat `config/proof_blocks.yaml` plus `scripts/run_proof_block.py` as the manifest-driven proof-block execution surface.
- Do not widen scope beyond the explicit task, patch, or run manifest.
- Keep the worktree clean after local execution.
- Do not amend existing commits unless the user explicitly instructs it.

## Scenario routing law

Before executing bridge work, read `PLANS.md` and classify the task as exactly one promotion intent:

```text
direct_pr
local_codex_execute
rescue_only
```

For local Codex execution, use `executor: local-codex`, `target_branch: work/...`, and `test_policy: required` unless the current repo-level bridge blueprint or explicit user instruction routes the task to the mainline automation lane.

For unvetted preservation, use `executor: rescue-branch`, `target_branch: rescue/...`, and `test_policy: rescue_unvetted`.

Do not treat a rescue branch as tested or merge-ready.

## Current mainline automation amendment

The active NVDA10 bridge doctrine uses `main` as the default successful destination after automated proof and receipt.

This means a future WSL/Codex bridge worker may commit and push directly to `main` when all of these are true:

1. the task is routed by the user or repo-level bridge blueprint to mainline automation;
2. latest remote `main` has been fetched;
3. the incoming payload or package has been inspected;
4. the patch base or final-file-state strategy has been chosen explicitly;
5. required targeted proof has run;
6. a GitHub-visible receipt is written.

This amendment does not permit direct `main` publication for rescue-only or unvetted work.

## Manifest proof-block execution law

A retained proof block is an admitted named proof command declared in:

```text
config/proof_blocks.yaml
```

The executable runner is:

```text
scripts/run_proof_block.py
```

The canonical user-facing command shape is:

```bash
make proof-block BLOCK=<block_id>
```

For the current vocabulary control gate, the admitted block is:

```bash
make proof-block BLOCK=vocabulary_governance_conformance
```

Rules:

1. Proof-block commands must be declared in `config/proof_blocks.yaml`.
2. `scripts/run_proof_block.py` must resolve the named block and run the manifest command without shell evaluation.
3. Workers may use a proof block as the targeted proof for a bounded change only when the block owns the relevant files/tests or the job explicitly declares it.
4. A proof-block pass is evidence for the owned block, not proof of the full repository.
5. Changes to proof-block routing, ownership, or execution must update the blueprint and run `make proof-executor-check`.
6. Do not add ad hoc long pytest commands to receipts when an admitted proof block already exists; cite the block command instead.

## Remote freshness law

Before applying, fitting, testing, or publishing work, ensure the local repository has fetched latest remote state from GitHub.

The bridge prepares the target work from `origin/<base_branch>` or directly from latest `origin/main` when mainline automation is routed. Codex must not assume a stale local `main` branch is current.

If remote freshness cannot be established, stop and write a receipt instead of publishing.

## AI_PATCH_V1 local executor law

When Codex CLI is invoked by the local AI patch bridge:

1. Read the run manifest first.
2. Read the decoded patch file named in the manifest.
3. Read the repo-level bridge blueprint when the run touches publication, payload, receipt behaviour, proof-block execution, or Codex handoff behaviour.
4. Work only on the declared `target_branch`, except when the run is explicitly routed to the mainline automation lane.
5. Preserve the patch intent.
6. If the patch applies cleanly, apply it.
7. If the patch does not apply cleanly, make the smallest lawful adjustment that preserves intent.
8. If the patch base is stale but final intended files are present, reconcile against current `main` rather than blindly applying the stale patch.
9. Run the declared local checks exactly as listed in the manifest.
10. Prefer admitted proof blocks for bounded targeted proof when the relevant block exists.
11. Do not touch prohibited paths.
12. Do not create extra files outside the declared scope unless required for the patch to work and documented in the receipt.
13. Write a local receipt file to the run directory named `codex_receipt.md`.
14. Stop and write a receipt if the patch intent conflicts with current repo truth or if the checks cannot pass within scope.

## Default local checks

Unless the run manifest overrides them, use:

```bash
make test
```

For bridge development itself, run:

```bash
make bridge-test
```

For blueprint/control doctrine checks, run:

```bash
make bridge-blueprint-check
make proof-executor-check
make -C tools/ai_patch_bridge ai-bridge-blueprint-check
make -C tools/ai_patch_bridge ai-bridge-proof-executor-check
```

For the admitted vocabulary proof block, run:

```bash
make proof-block BLOCK=vocabulary_governance_conformance
```

## Default watcher inbox

The bridge watcher defaults to the NVDA10 repository inbox:

```text
AI_PATCH_REPO=JayDEmily/nvda10
AI_PATCH_ISSUE=2
AI_PATCH_BASE=main
```

Do not point active watcher defaults, service templates, or installer-generated units at historical remote-test inboxes.

## Git discipline

- Use one work branch per patch comment for legacy AI_PATCH_V1 work-branch lanes.
- Use direct `main` only for explicitly routed mainline automation jobs after proof and receipt.
- Do not commit directly to `main` for rescue-only, unvetted, or legacy PR-validation lanes.
- Do not leave untracked temporary files in the repo root.
- Runtime scratch files belong under `.ai_patch_bridge/runs/<comment_id>/`.
- Persistent bridge state belongs under `.ai_patch_bridge/state/`.
- Codex local runtime state belongs under `.codex` and is ignored by Git.

## Receipt discipline

A receipt must state:

- source comment ID, package ID, or job ID;
- target branch or `main`;
- starting `main` SHA;
- resulting commit SHA, if pushed;
- checks run;
- pass/fail outcome;
- files intentionally changed;
- apply mode, such as direct patch, final file state, chunk reconstruction, GitHub Actions extraction, or manifest proof-block execution;
- reason for stop, if stopped.

## Bridge-local planning route

For AI patch bridge work, read `PLANS.md` in this directory before changing bridge code, scripts, docs, tests, or Makefile targets.

Also run the blueprint and proof-executor checks when bridge work changes publication, payload, receipt, proof-block, or Codex handoff doctrine:

```bash
make -C tools/ai_patch_bridge ai-bridge-blueprint-check
make -C tools/ai_patch_bridge ai-bridge-proof-executor-check
```
