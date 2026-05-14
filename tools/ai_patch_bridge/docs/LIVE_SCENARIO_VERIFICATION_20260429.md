# Live scenario verification — 2026-04-29

## Scope

This report records live verification of the repo-local AI Patch Bridge in `JayDEmily/NVIDIA9_remotetest`.

The live tests used GitHub issue `#1` as the `AI_PATCH_INBOX` and the local WSL checkout as the executor.

## Proven execution model

```text
ChatGPT posts AI_PATCH_V1 comment
→ local bridge reads GitHub issue inbox
→ bridge verifies payload hashes
→ bridge creates target branch from origin/<base_branch>
→ Codex applies/fits patch and runs declared checks
→ Codex writes codex_receipt.md
→ outer bridge re-runs declared checks
→ outer bridge stages decoded patch paths
→ outer bridge creates the commit and publishes the branch
→ outer bridge verifies the remote branch head
→ outer bridge posts LOCAL_CODEX_RECEIPT_V1
```

Codex does not own final source-control publication. Live testing showed Codex could apply and check a patch but `.git` was mounted read-only inside the Codex sandbox. PR `#3` moved publication to the outer bridge.

## Live probes

| Probe | Source comment | Expected lane | Result |
|---|---:|---|---|
| Malformed dry-run payload | `4340856891` | reject bad input | Passed: bridge rejected hash mismatch |
| Valid dry-run payload | `4340874176` | decode/verify only | Passed: `dry_run_ready` |
| Scenario B watcher skip | `4341134224` | `github-action` skipped by local bridge | Passed: no branch created |
| Scenario C V1 | `4340896762` | local Codex | Failed usefully: Codex CLI too old for GPT-5.5 |
| Scenario C V2 | `4340932492` | local Codex | Stopped usefully: Codex applied/check passed but `.git` was read-only |
| Scenario C V3 | `4341102020` | repaired local Codex plus outer bridge publication | Passed: branch published with receipt |
| Scenario D | `4341156597` | cumulative export | Passed: one payload produced one commit with two files |
| Scenario E | `4341149888` | rescue skipped by default | Passed: default bridge did not consume rescue payload |
| Scenario F | `4341168424` | local fallback | Passed: branch published with receipt |
| Scenario G | `4341182954` | explicit rescue preservation | Passed: rescue branch published with receipt |

## Evidence branches

These branches are evidence branches and are not intended to be merged as product work:

```text
work/scenario-c-v3-20260429
work/scenario-d-cumulative-export-20260429
work/scenario-f-local-fallback-20260429
rescue/scenario-g-rescue-preservation-20260429
```

Scenario B and Scenario E skip tests intentionally created no branch in their default-skip mode.

## Scenario notes

- Scenario B posted a `github-action` payload. The local bridge skipped it by default and the target branch remained absent.
- Scenario C V3 posted a `local-codex` payload. The bridge created the branch, Codex applied the patch and ran `make scaffold-check`, then the outer bridge published the branch and posted `status: pushed`.
- Scenario D posted a cumulative payload that produced two files in one commit.
- Scenario E posted a `rescue-branch` payload. The default bridge skipped it and the target branch remained absent.
- Scenario F proved the local fallback lane.
- Scenario G proved explicit rescue acceptance with `--accepted-executor rescue-branch`.

## Remaining close-out gate

After this documentation branch is pulled locally, run:

```bash
make -C tools/ai_patch_bridge test
make -C tools/ai_patch_bridge lint
make -C tools/ai_patch_bridge ai-bridge-scenarios
make -C tools/ai_patch_bridge ai-bridge-preflight
```

Do not merge this close-out documentation branch until those local gates pass.
