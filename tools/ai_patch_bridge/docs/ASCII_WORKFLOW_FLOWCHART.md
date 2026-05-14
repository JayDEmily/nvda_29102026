# AI Patch Bridge ASCII workflow flowchart

## Purpose

This is the operational decision tree for ChatGPT, GitHub, GitHub mobile, local Ubuntu/WSL, Codex, and the AI Patch Bridge.

The user should only need to state availability and intent. ChatGPT must choose the lane.

Typical user statements:

```text
computer off
computer on
phone only
repo dirty
apply this patch
this needs tests
preserve this work
merge it
```

## Core principle

Choose the lowest-risk lane that preserves the work and matches the proof required.

```text
GitHub-only lanes preserve and review work.
GitHub mobile checkpoints approve or merge reviewable work.
Local Codex/watcher lanes repair and prove work that needs local execution.
Blob/repo-file payload lanes prevent sandbox work from being lost.
```

## Full decision flow

```text
START
  |
  v
+-------------------------------------------------------------+
| What did the user provide or request?                       |
+-------------------------------------------------------------+
  |
  +--> A. Patch / diff / generated sandbox work
  |       |
  |       v
  |   +---------------------------------------------------------+
  |   | Is the work valuable but not yet safely applied?         |
  |   +---------------------------------------------------------+
  |       |
  |       +--> YES
  |       |     |
  |       |     v
  |       | +---------------------------------------------------+
  |       | | Is the computer ON, repo CLEAN, and local proof     |
  |       | | or Codex repair required now?                      |
  |       | +---------------------------------------------------+
  |       |     |
  |       |     +--> YES
  |       |     |     |
  |       |     |     v
  |       |     | +-----------------------------------------------+
  |       |     | | LOCAL CODEX / WATCHER LANE                    |
  |       |     | | - start only from clean repo                   |
  |       |     | | - apply/repair patch locally                   |
  |       |     | | - run required checks                          |
  |       |     | | - push branch                                  |
  |       |     | | - post LOCAL_CODEX_RECEIPT_V1                  |
  |       |     | +-----------------------------------------------+
  |       |     |
  |       |     +--> NO
  |       |           |
  |       |           v
  |       |     +-----------------------------------------------+
  |       |     | PRESERVE-FIRST LANE                            |
  |       |     | - create GitHub blob or repo-file payload       |
  |       |     | - or create patch-queue branch/PR               |
  |       |     | - record intended target + proof limitation     |
  |       |     | - do not lose sandbox work                      |
  |       |     +-----------------------------------------------+
  |       |           |
  |       |           v
  |       |     Later when local clean/proof available:
  |       |           |
  |       |           v
  |       |     LOCAL CODEX / WATCHER LANE or DIRECT APPLY LANE
  |       |
  |       +--> NO, try applying now
  |             |
  |             v
  |       +---------------------------------------------------+
  |       | Can ChatGPT apply it safely on a NEW branch from     |
  |       | current main or declared base?                       |
  |       +---------------------------------------------------+
  |             |
  |             +--> YES
  |             |     |
  |             |     v
  |             | +-----------------------------------------------+
  |             | | GITHUB-ONLY APPLY LANE                         |
  |             | | - create non-orphan work branch                 |
  |             | | - apply patch there                             |
  |             | | - open draft PR                                 |
  |             | | - label proof as GitHub-only                    |
  |             | +-----------------------------------------------+
  |             |     |
  |             |     v
  |             | +-----------------------------------------------+
  |             | | Does user explicitly say merge / accept?        |
  |             | +-----------------------------------------------+
  |             |     |
  |             |     +--> YES --> if GitHub mergeable: MERGE
  |             |     |          else: report blocker / use phone gate
  |             |     |
  |             |     +--> NO  --> leave draft PR open
  |             |
  |             +--> NO
  |                   |
  |                   v
  |             +-----------------------------------------------+
  |             | PATCH QUEUE LANE                                |
  |             | - store patch under queue/payload artefact       |
  |             | - open draft PR or issue comment receipt         |
  |             | - do not claim applied                           |
  |             | - route later to Codex/local repair              |
  |             +-----------------------------------------------+
  |
  +--> B. Existing GitHub branch / PR needs proof
  |       |
  |       v
  |   +---------------------------------------------------------+
  |   | Is local computer ON and repo CLEAN?                     |
  |   +---------------------------------------------------------+
  |       |
  |       +--> YES
  |       |     |
  |       |     v
  |       | +---------------------------------------------------+
  |       | | BRANCH-AS-PAYLOAD VALIDATION LANE                |
  |       | | - branch is the payload                           |
  |       | | - post LOCAL_BRANCH_VALIDATE_V1                   |
  |       | | - watcher fetches and validates branch            |
  |       | | - receipt status should be checked/pushed/failed  |
  |       | +---------------------------------------------------+
  |       |
  |       +--> NO
  |             |
  |             v
  |       +---------------------------------------------------+
  |       | QUEUED VALIDATION LANE                            |
  |       | - post or prepare LOCAL_BRANCH_VALIDATE_V1         |
  |       | - leave watcher OFF if repo dirty/unavailable      |
  |       | - wait for clean local gate before execution       |
  |       +---------------------------------------------------+
  |
  +--> C. Small docs / governance / planning edit
  |       |
  |       v
  |   +---------------------------------------------------------+
  |   | Does this require runtime/dependency proof?              |
  |   +---------------------------------------------------------+
  |       |
  |       +--> NO
  |       |     |
  |       |     v
  |       | +---------------------------------------------------+
  |       | | GITHUB-ONLY DOCS LANE                            |
  |       | | - create branch                                  |
  |       | | - edit docs/governance files                      |
  |       | | - open PR or merge if explicitly approved         |
  |       | | - proof = GitHub accepted scoped diff             |
  |       | +---------------------------------------------------+
  |       |
  |       +--> YES
  |             |
  |             v
  |       +---------------------------------------------------+
  |       | LOCAL PROOF LANE                                  |
  |       | - use Codex/local tests/checks                     |
  |       | - require receipt or command output                |
  |       +---------------------------------------------------+
  |
  +--> D. Runtime code / tests / dependency behaviour
  |       |
  |       v
  |   +---------------------------------------------------------+
  |   | Is local computer ON and repo CLEAN?                     |
  |   +---------------------------------------------------------+
  |       |
  |       +--> YES
  |       |     |
  |       |     v
  |       | +---------------------------------------------------+
  |       | | LOCAL CODEX / TEST LANE                          |
  |       | | - use local environment                           |
  |       | | - run dependency-aware tests                      |
  |       | | - Codex repairs if needed                         |
  |       | | - push/receipt when done                          |
  |       | +---------------------------------------------------+
  |       |
  |       +--> NO
  |             |
  |             v
  |       +---------------------------------------------------+
  |       | PRESERVE / DRAFT ONLY                             |
  |       | - create draft branch/PR if safe                   |
  |       | - or queue blob/repo-file payload                  |
  |       | - do not claim tested                              |
  |       | - wait for local proof                             |
  |       +---------------------------------------------------+
  |
  +--> E. User says merge
          |
          v
      +---------------------------------------------------------+
      | What is the proof level of the PR?                      |
      +---------------------------------------------------------+
          |
          +--> GitHub-only docs/governance PR
          |       |
          |       v
          |   +-----------------------------------------------+
          |   | If user explicitly accepts GitHub-only proof    |
          |   | and GitHub says mergeable: merge.               |
          |   +-----------------------------------------------+
          |
          +--> Runtime / bridge / local-proof PR
          |       |
          |       v
          |   +-----------------------------------------------+
          |   | Require local gates and/or LOCAL_CODEX_RECEIPT  |
          |   | unless user explicitly overrides.               |
          |   +-----------------------------------------------+
          |
          +--> Draft PR
                  |
                  v
              +-----------------------------------------------+
              | Ready-for-review required before merge.         |
              | User can do this in GitHub mobile, or           |
              | ChatGPT can try if tool supports it.             |
              +-----------------------------------------------+
```

## Proof ladder

```text
LOWEST PROOF
  |
  +-- queued patch/blob/repo-file artefact
  |     proves: work was preserved
  |     does not prove: patch applies
  |
  +-- GitHub branch + draft PR
  |     proves: GitHub accepted scoped changes
  |     does not prove: local tests or runtime behaviour
  |
  +-- GitHub mobile Ready/Merge
  |     proves: user accepted GitHub review level and advanced PR state
  |     does not prove: local tests unless separately shown
  |
  +-- local command output
  |     proves: named commands ran in local environment
  |     does not prove: watcher receipt unless receipt exists
  |
  +-- LOCAL_CODEX_RECEIPT_V1
        proves: local bridge/Codex lane outcome stated in receipt
        strongest bridge proof surface
HIGHEST PROOF
```

## Lane selection table

| Situation | Default action | Merge allowed? |
|---|---|---|
| Computer off, docs patch | GitHub-only apply PR | Yes, if user explicitly accepts GitHub-only proof |
| Computer off, runtime patch | Draft PR or payload queue only | No, unless user explicitly overrides missing local proof |
| Computer off, sandbox work at risk | Blob/repo-file payload or queue PR | No; preserve first |
| Computer on, repo clean, docs patch | GitHub-only or local check if cheap | Yes after scoped review |
| Computer on, repo clean, runtime patch | Codex/local tests/receipt | Yes after required proof |
| Computer on, repo dirty | Stop watcher, preserve elsewhere | No local automation merge decision |
| Patch applies cleanly on GitHub branch | Open PR, record proof limitation | Depends on work type |
| Patch does not apply cleanly | Queue artefact and failure receipt | No |
| Existing branch needs validation | Queue or run branch-as-payload validation | After receipt if proof required |
| Connector write fails | Retry smaller or queue payload | No until state is clear |

## Mandatory labels in responses

When reporting a result, ChatGPT must use one of these labels:

```text
APPLIED_TO_BRANCH
QUEUED_AS_PAYLOAD
MERGED_TO_MAIN
LOCAL_PROOF_PENDING
LOCAL_PROOF_OBSERVED
BLOCKED_DIRTY_WORKTREE
BLOCKED_CONNECTOR_FAILURE
BLOCKED_DRAFT_PR
BLOCKED_MERGE_CONFLICT
```

## Non-negotiable safety rules

```text
Never apply a patch directly to main first.
Never mix bridge PR work with unrelated governance/runtime work.
Never say tests passed unless command output or receipt proves it.
Never say applied when only queued.
Never use inline base64 issue comments for serious patch payloads.
Never leave watcher running against a dirty mixed-scope repo.
Never ask the user to be the terminal operator when GitHub-only or queued lanes are adequate.
```

## Practical default

```text
When unsure:
  preserve the work first,
  create a branch or payload artefact,
  open a draft PR,
  record proof limitations,
  only escalate to local Codex/watcher when proof or repair actually requires it.
```
