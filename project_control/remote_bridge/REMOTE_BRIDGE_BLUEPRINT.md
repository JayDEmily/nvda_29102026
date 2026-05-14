# NVDA10 Remote Bridge Blueprint

Status: active working blueprint
Repository: `JayDEmily/nvda10`
Default branch: `main`
Last updated: 2026-05-09

## Purpose

This blueprint defines the practical work loop for moving useful work between ChatGPT, GitHub, the local Ubuntu/WSL environment, and Codex CLI.

The goal is not to maximise ceremony. The goal is to reduce the user's manual workload while keeping enough evidence to recover from mistakes.

## Plain-English model

ChatGPT is the planner and operator.

GitHub is the shared work surface: command lane, payload lane, history, and proof wall.

Ubuntu/WSL is the local execution supervisor.

Codex CLI is the local code worker invoked by the WSL bridge when repo-aware repair or implementation is needed.

`main` is the default successful destination.

Receipts are evidence after work, not permission slips before work.

## Current NVDA10 bridge inbox

The active local watcher inbox for NVDA10 is:

```text
repo: JayDEmily/nvda10
issue: 2
title: NVDA10 AI Patch Bridge Inbox
default base: main
```

Historical remote-test inboxes are provenance only and are not active watcher defaults.

## Default successful loop

```text
ChatGPT creates or receives work
→ GitHub carries the work
→ WSL watcher pulls the work when online
→ WSL prepares the current repo state
→ Codex CLI applies, repairs, or implements when required
→ targeted proof runs
→ result is committed and pushed to main
→ receipt is written to GitHub
→ ChatGPT/user inspect the receipt if needed
```

Human diff reading is not the normal gate. The recovery model is Git history, receipts, and backups.

## Current proven lanes

### Lane A: direct small GitHub write

Use when ChatGPT can safely write the complete change as text through the GitHub connector.

Examples:

- documentation updates;
- small source/test edits;
- receipts;
- control files;
- simple manifests.

Observed proof in this repo family:

- PR #1 in `JayDEmily/nvda10` merged Codex branch work into `main` at `49d3c60f6024d8ce425c3096a1aadf3edeec7a50`.
- ChatGPT applied `NVDA10_PM_WORKER_OUTPUT_VOCAB_JSON_HELPERS_GREEN_2026-05-08.tar.gz` final file state to `main` at `87395587bb73abc8e3d713445a3125941ea2a481` with a receipt.

### Lane B: GitHub Actions tarball extraction

Use when a tarball already exists in a GitHub repo and GitHub servers can unpack it.

Workflow pattern:

```text
repo contains .tar.gz/.tgz
→ GitHub Actions manual dispatch
→ validate tar members
→ extract
→ strip nested .git directories
→ remove gitlink/submodule-style index entries
→ commit extracted normal files to main
→ write receipt
```

This lane was tested in `JayDEmily/nvda10_april_v1`. The first run extracted and committed successfully, but a nested `.git` directory caused GitHub to treat an inner repo as a gitlink/submodule-style entry. The workflow was then updated to flatten nested Git repositories before commit.

### Lane C: sandbox tarball / stale patch reconciliation

Use when another ChatGPT sandbox produces a downloadable tarball containing patches, receipts, or final files.

This lane is important because sandbox outputs may be based on a branch or commit that is no longer current.

Required worker behaviour:

```text
inspect package
identify source/base commit and worker intent
identify changed files
compare against current GitHub main
if patch base is current, apply patch normally
if patch base is stale, do not blindly apply patch
recover final intended file state where coherent
run targeted proof
commit to main
write receipt explaining the base mismatch and chosen apply mode
```

The patch is not the authority. The worker intent, final file state, current `main`, and proof result together define the action.

Observed proof:

- package `NVDA10_PM_WORKER_OUTPUT_VOCAB_JSON_HELPERS_GREEN_2026-05-08.tar.gz` was built on a pre-merge Codex branch state;
- current `main` had moved after PR #1;
- the uploaded second-layer patch was not blindly applied;
- final intended files were applied instead;
- targeted sandbox merge probe reported `7 passed in 0.23s`;
- commit landed on `main` as `87395587bb73abc8e3d713445a3125941ea2a481`.

### Lane D: GitHub chunked base64 payload transport

Use when a larger generated artefact must move through GitHub without relying on Gmail, Drive, or direct sandbox network upload.

Pattern:

```text
tar.gz payload
→ base64 encode
→ split into ordered text chunks
→ write manifest + chunks as one Git tree/commit
→ WSL reconstructs
→ verify size and SHA256
→ extract safely
→ execute job
→ commit result and receipt to main
```

Small proof exists in `JayDEmily/NVIDIA9_remotetest`: ChatGPT wrote chunked base64 payload files to `main`, read them back, reconstructed the tarball, verified SHA256, and wrote a receipt.

This is a proven small transport spine, not yet a full large-payload WSL acceptance proof.

### Lane E: Manifest-driven proof-block execution

Use when a bounded set of repo tests has been admitted as a named proof block in `config/proof_blocks.yaml`.

Pattern:

```text
config/proof_blocks.yaml declares block_id + command
→ scripts/run_proof_block.py resolves the named block
→ command is tokenised without shell evaluation
→ leading python/python3 is routed to the current interpreter
→ deterministic proof environment is set
→ Makefile exposes the block as make proof-block BLOCK=<block_id>
```

Current admitted proof-block examples:

```bash
make proof-block BLOCK=vocabulary_governance_conformance_candidate
make proof-block BLOCK=proof_executor_contract
```

This lane is not a substitute for Codex. It is a named executable proof gate for bounded checks that have already been admitted into the manifest.

Observed proof:

- package `NVDA10_PM_WORKER_OUTPUT_VOCAB_PROOF_EXECUTOR_GREEN_2026-05-08.tar.gz` implemented the proof-block executor;
- worker package recorded the vocabulary proof-block family as passing;
- GitHub patch lane applied the executor update to `main` at `f55fe5c0cb5413c46aaa2a5e47e9880146d9342d`;
- `scripts/run_proof_block.py`, `Makefile`, `config/proof_blocks.yaml`, and `tests/tier_b/proof_model/test_proof_executor_contract.py` now define and test the runner surface.

## Retired or rejected lanes

Do not use these as active bridge primitives:

- Gmail `.tar.gz` attachment egress from ChatGPT;
- Google Drive arbitrary binary egress from ChatGPT;
- AWS/S3 upload from ChatGPT sandbox via `curl`;
- ChatGPT GitHub single large binary blob;
- browser-extension export tools as bridge infrastructure;
- PR review as the normal successful path.

Reason: these are undocumented, connector-limited, approval-heavy, or unstable for this workflow.

## WSL/Codex worker responsibilities

When the local machine is online, the WSL bridge should own:

1. polling GitHub for bridge jobs or payload commits;
2. fetching latest `main` before work;
3. creating/using a clean local working state;
4. generating a context pack before Codex invocation;
5. inspecting incoming package metadata, patch base, changed files, and final file state;
6. applying clean patches directly when safe;
7. invoking Codex CLI when the patch is stale, conflicted, or requires repo-aware judgement;
8. running targeted proof required by the job;
9. preferring an admitted proof block when the job is bounded to that block;
10. committing and pushing to `main` on success;
11. writing a receipt under `var/audit/remote_bridge_receipts/`;
12. stopping with a failure receipt when it cannot safely reconcile the job.

## Context packer requirement

Before Codex is invoked, the WSL bridge should build a deterministic context pack containing:

- current branch and HEAD;
- git status;
- recent commits;
- relevant authority/control files;
- target files;
- incoming patch/job intent;
- selected proof logs or prior receipts;
- file sizes and SHA256 values.

The context packer exists in the test bridge repo as `src/nvda_desk/remote_bridge/context_packer.py` and should be treated as a reusable design brick for the WSL worker.

## Mainline doctrine

Successful automated worker jobs push to `main` by default.

A worker should not create a PR or require human diff review unless the job explicitly asks for it or the worker cannot produce a safe automated result.

A failed or uncertain job should not silently mutate `main`. It should write a failure receipt with the exact blocker.

## Receipt doctrine

Every bridge action that mutates GitHub should write a receipt.

Minimum receipt fields:

```text
status
repository
target branch
starting main SHA
result commit SHA
source package or job id
source package SHA256 if available
changed files
apply mode: direct patch / final file state / GitHub Actions extraction / chunk reconstruction / manifest proof-block execution
proof commands run
observed proof result
known non-claims
```

Receipts are part of the bridge's memory. They prevent the next worker from guessing.

## Patch/base mismatch rule

When incoming work was created on an older base, the worker must not treat the patch file as sacred.

Use this order:

1. preserve package metadata and receipt evidence;
2. identify final intended files;
3. compare current `main` state;
4. prefer final intended file state only if coherent and bounded;
5. run targeted proof;
6. commit to `main` with a receipt that records the mismatch.

If final file state cannot be trusted or the change is not bounded, invoke Codex CLI locally to reconcile intent.

## Manifest proof-block rule

When a proof block exists for a bounded test family, use the named block instead of repeating a long pytest command.

Current canonical command:

```bash
make proof-block BLOCK=vocabulary_governance_conformance_candidate
make proof-block BLOCK=proof_executor_contract
```

These commands resolve named blocks from `config/proof_blocks.yaml` and run each manifest command through `scripts/run_proof_block.py`.

A proof-block pass proves only that named block. It does not prove the full repository unless the block explicitly owns the full repository proof.

## Controlled checks

The repo root Makefile owns cheap static control gates:

```bash
make bridge-blueprint-check
make proof-executor-check
```

The bridge-local Makefile delegates to the same gates:

```bash
make -C tools/ai_patch_bridge ai-bridge-blueprint-check
make -C tools/ai_patch_bridge ai-bridge-proof-executor-check
```

These checks do not prove WSL execution. They prove the current repo contains the main bridge blueprint, proof-block executor surface, and key doctrine tokens needed by future workers.

## Current state summary

Known true:

- `JayDEmily/nvda10` is private and uses `main` as the default branch.
- PR #1 merged `codex/update-pyproject-metadata` into `main`.
- ChatGPT can commit direct text changes to `main` via the GitHub connector.
- ChatGPT can inspect a sandbox tarball, detect base mismatch, apply bounded final files, and commit to `main` with receipt.
- GitHub Actions can run from phone-triggered `workflow_dispatch` and commit extracted contents.
- GitHub chunked base64 payload transport has a small successful proof in the remote-test repo.
- GitHub patch-apply lane can apply bounded patches and write receipts.
- The repo now contains a manifest-driven proof-block executor with named blocks for vocabulary governance and proof-executor contract checks.

Not yet proven:

- WSL watcher ingestion of the new GitHub-only job format;
- Codex CLI consuming the deterministic context pack;
- full large-payload chunk transport through WSL reconstruction;
- full end-to-end loop from ChatGPT job to WSL/Codex to `main` receipt without manual intervention;
- GitHub Actions running the full `make proof-block BLOCK=vocabulary_governance_conformance` proof on its own VM after this documentation update.

## Next recommended implementation step

Implement the WSL bridge worker around the proven behaviours above:

```text
GitHub job/payload detection
→ current-main fetch
→ context pack generation
→ patch/base inspection
→ direct apply or Codex reconciliation
→ admitted proof block or targeted proof
→ push to main
→ receipt
```

Do not reopen Gmail/Drive transport. Do not make PR review the default. Keep the bridge boring, git-native, proof-block-aware, and receipt-heavy.
