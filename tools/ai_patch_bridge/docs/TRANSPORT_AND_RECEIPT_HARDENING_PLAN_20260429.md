# AI Patch Bridge transport and receipt hardening plan — 2026-04-29

## Purpose

This plan records the next bridge repair required before more large real patches are sent through the watcher.

The first real patch attempt exposed two defects:

1. large `base64+gzip` payloads in GitHub issue comments can arrive in a form the local watcher rejects as invalid base64;
2. the user had to manually inspect local `.ai_patch_bridge` state to learn whether a run failed.

Both defects are bridge defects, not user-operation problems.

## Current evidence

Observed local receipt:

```text
LOCAL_CODEX_RECEIPT_V1
source_comment_id: 4343724234
status: failed
reason: payload is not valid base64
```

The failure occurred before Codex. No fitting, local check, branch publication, or remote-head verification happened.

The current parser removes whitespace before strict base64 decode:

```python
payload_b64 = "".join(payload_match.group("payload").split())
gzip_bytes = base64.b64decode(payload_b64, validate=True)
```

Therefore ordinary line wrapping should not cause this failure. A post/fetch validation loop is required before the watcher is allowed to consume a submitted patch.

## Non-negotiable outcome

The user should not manually run `grep`, `cat`, or inspect local receipt files to learn whether a watcher run succeeded.

The normal flow must become:

```text
build payload
→ validate locally
→ submit
→ fetch submitted object back
→ validate fetched object
→ wait for watcher receipt
→ verify receipt is visible on GitHub
→ report final status
```

## Gate 1 — Submission self-verification

### Objective

Prevent invalid transport from reaching the watcher.

### Required behaviour

After creating an `AI_PATCH` payload and before considering it submitted:

1. parse the locally built payload with the same parser used by the watcher;
2. post or store the payload;
3. fetch the submitted object back from GitHub;
4. parse the fetched object with the same parser;
5. compare metadata, raw hash, gzip hash, raw byte count, gzip byte count, and target branch;
6. stop immediately if the fetched object is not equivalent.

### Required output

A submission result object:

```json
{
  "submitted": true,
  "comment_id": 123,
  "transport_verified": true,
  "target_branch": "work/example"
}
```

or:

```json
{
  "submitted": false,
  "transport_verified": false,
  "reason": "fetched payload failed parser validation"
}
```

## Gate 2 — Large payload transport

### Objective

Stop relying on large issue-comment bodies as the only payload carrier.

### Required design

Add an external payload transport for larger patches.

Preferred metadata:

```text
AI_PATCH_V1
repo: JayDEmily/NVIDIA9_remotetest
base_branch: main
target_branch: work/example
scope: example
executor: local-codex
mode: local_patch_fit_test_commit_push
commit_policy: single_commit
test_policy: required

payload_encoding: base64+gzip
payload_transport: github_blob
payload_blob_sha: <blob_sha>
payload_raw_sha256: <sha256>
payload_gzip_sha256: <sha256>
payload_raw_bytes: <int>
payload_gzip_bytes: <int>
```

For small patches, inline `PAYLOAD_BEGIN/PAYLOAD_END` may remain supported.

For large patches, the watcher must fetch the GitHub blob content by SHA, decode/verify it, and then continue through the existing `AiPatchMessage` path.

### Required threshold

Use blob transport by default above a conservative inline-size threshold. The threshold must be documented and tested.

## Gate 3 — Receipt sync and polling

### Objective

Make run status visible without terminal inspection.

### Required behaviour

After submitting a patch, the operator side should poll GitHub issue comments for:

```text
LOCAL_CODEX_RECEIPT_V1
source_comment_id: <submitted_comment_id>
```

The polling result must classify:

```text
pushed
checked
failed
stopped
timeout
receipt_post_failed
```

`checked` means an existing remote branch was fetched/inspected, required local checks passed, and no additional patch payload was applied.

If the local watcher writes a local `github_receipt.md`, the watcher must verify that the corresponding GitHub issue comment exists. If posting fails, it must retry and expose a distinct failure state rather than silently leaving the receipt local-only.

## Gate 4 — Tests

Add tests covering at least:

1. inline payload still parses;
2. intentionally corrupted inline payload fails before Codex;
3. fetched-comment mismatch is detected;
4. blob transport payload parses to the same raw patch as inline transport;
5. receipt matching by `source_comment_id` works;
6. receipt timeout is reported distinctly;
7. receipt-post failure is not recorded as successful processing.

## Gate 5 — Documentation

Update:

```text
tools/ai_patch_bridge/README.md
tools/ai_patch_bridge/docs/INSTALL_AI_PATCH_BRIDGE.md
tools/ai_patch_bridge/docs/WATCHER_OPERATIONS.md
tools/ai_patch_bridge/docs/EDGE_CASES_AND_BRANCH_LANES.md
```

Required documentation changes:

1. small patch inline transport;
2. large patch blob transport;
3. submission self-verification;
4. automatic receipt polling;
5. exact status meanings;
6. operator no longer manually reads local receipts during normal operation.

## Stop conditions

Stop and report if:

1. GitHub blob fetch cannot be implemented with available tools;
2. receipt comments cannot be reliably correlated to source comment IDs;
3. implementing blob transport would require changing branch lane semantics;
4. tests cannot run in the available local environment;
5. any repair would silently mark a failed transport as processed.

## Immediate operating rule

Until this hardening exists, do not send large real patches through inline issue-comment payloads.

For large patches, use one direct PR branch with truthful PR notes, or wait for blob transport support.

## Required PR body when implemented

```text
Summary
Transport behaviour before/after
Receipt behaviour before/after
Tests run
Manual verification removed
Known limitations
```
