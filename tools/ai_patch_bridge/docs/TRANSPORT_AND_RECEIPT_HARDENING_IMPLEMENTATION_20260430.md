# AI Patch Bridge transport and receipt hardening implementation — 2026-04-30

## Scope

This document records the implemented branch surface for transport and receipt hardening.

Branch:

```text
work/bridge-transport-and-receipt-hardening-20260430
```

This work does not change NVDA trading runtime code. It changes only the repo-local bridge pack.

## Active control surface

The active static-review plan for this branch is recorded in:

```text
tools/ai_patch_bridge/PLANS.md
```

The plan classifies this work as GitHub-only `direct_pr` static hardening while the user's local computer is unavailable. It explicitly forbids merge, live `AI_PATCH_V1` runs, watcher-readiness claims, and Codex/local-gate claims until local proof exists.

## Implemented surfaces

### Transport overlay

File:

```text
tools/ai_patch_bridge/src/ai_patch_bridge/transport_hardening.py
```

The overlay adds:

1. inline payload compatibility;
2. GitHub blob payload support;
3. automatic transport selection;
4. post-submit fetch-back validation;
5. receipt polling by `source_comment_id`;
6. verified receipt posting with retry;
7. a `submit-and-wait` CLI path.

### CLI routing

File:

```text
tools/ai_patch_bridge/src/ai_patch_bridge/cli.py
```

The console entrypoint now routes through the hardening overlay. Existing commands still delegate to the legacy core command parser. The new command is:

```bash
PYTHONPATH=src python3 -m ai_patch_bridge.cli submit-and-wait \
  --repo JayDEmily/nvda10 \
  --issue-number 2 \
  --base-branch main \
  --target-branch work/example \
  --scope "example scope" \
  --patch-file /path/to/change.patch
```

### Makefile target

File:

```text
tools/ai_patch_bridge/Makefile
```

New target:

```bash
make -C tools/ai_patch_bridge ai-bridge-submit-and-wait \
  AI_PATCH_TARGET_BRANCH=work/example \
  AI_PATCH_SCOPE="example scope" \
  AI_PATCH_FILE=/path/to/change.patch
```

Default knobs:

```text
AI_PATCH_TRANSPORT=auto
AI_PATCH_INLINE_GZIP_BYTE_LIMIT=4096
AI_PATCH_RECEIPT_TIMEOUT_SECONDS=3600
AI_PATCH_RECEIPT_POLL_SECONDS=30
```

## Transport behaviour

### Inline transport

Small payloads continue to use:

```text
payload_encoding: base64+gzip
PAYLOAD_BEGIN
...
PAYLOAD_END
```

Inline payloads still run through the existing strict parser path.

### Blob transport

Large payloads use:

```text
payload_encoding: base64+gzip
payload_transport: github_blob
payload_blob_sha: <sha>
payload_raw_sha256: <sha256>
payload_gzip_sha256: <sha256>
payload_raw_bytes: <int>
payload_gzip_bytes: <int>
```

The watcher fetches the GitHub blob by SHA, validates the gzip hash, decompresses the patch, validates the raw hash and byte counts, then continues through the same `AiPatchMessage` shape used by the old inline path.

## Submission verification

`submit-and-wait` performs:

```text
build payload
→ validate local payload
→ post issue comment
→ fetch the posted comment back
→ validate fetched payload
→ compare metadata and raw patch bytes
→ poll for matching LOCAL_CODEX_RECEIPT_V1
```

If the fetched comment does not match the locally built payload, submission fails before the watcher result is trusted.

## Receipt verification

The overlay replaces the legacy receipt poster with a verified poster.

Required behaviour:

1. post the receipt comment;
2. fetch the comment back by ID;
3. confirm `source_comment_id` and `status` match;
4. retry on failure;
5. raise `receipt_post_failed` if the GitHub-visible receipt cannot be verified.

## Tests added

File:

```text
tools/ai_patch_bridge/tests/test_transport_hardening.py
```

Coverage added:

1. inline payload remains on the legacy parser path;
2. automatic transport keeps small payloads inline below threshold;
3. GitHub blob payload round trip;
4. automatic blob selection above threshold;
5. blob payload hash mismatch rejection;
6. direct fetched-comment metadata mismatch detection;
7. `submit-and-wait` fetched-comment mismatch detection;
8. receipt matching by `source_comment_id`;
9. receipt timeout classification;
10. verified receipt posting success path;
11. verified receipt posting mismatch failure path.

## Static review results

GitHub-only static review checked the active plan gates against the implementation candidate.

Observed from direct file read:

1. branch lane semantics remain unchanged;
2. inline transport remains supported;
3. blob transport metadata includes blob SHA, raw hash, gzip hash, raw bytes, and gzip bytes;
4. fetched-comment validation compares submitted and fetched metadata plus raw patch bytes;
5. receipt polling matches `LOCAL_CODEX_RECEIPT_V1` by `source_comment_id`;
6. receipt posting verifies the fetched GitHub comment before returning;
7. Makefile target fails when required `AI_PATCH_TARGET_BRANCH`, `AI_PATCH_SCOPE`, or `AI_PATCH_FILE` is missing;
8. test coverage now includes inline compatibility, blob round trip, fetched mismatch, receipt match, receipt timeout, and receipt-post verification;
9. local proof remains absent because the user's computer is off.

## Gates

Sandbox checks performed before the first GitHub write:

```text
python compile of transport_hardening.py: passed
python compile of test_transport_hardening.py: passed
```

No later local or sandbox test execution is claimed here.

Local repo gates not run because the user's computer is off:

```bash
make -C tools/ai_patch_bridge test
make -C tools/ai_patch_bridge lint
make -C tools/ai_patch_bridge ai-bridge-scenarios
make -C tools/ai_patch_bridge ai-bridge-preflight
make bridge-status
```

## Required local close-out when computer is on

Run from repo root:

```bash
make bridge-status
make -C tools/ai_patch_bridge test
make -C tools/ai_patch_bridge lint
make -C tools/ai_patch_bridge ai-bridge-scenarios
make -C tools/ai_patch_bridge ai-bridge-preflight
```

Do not merge until these gates pass locally.

## Required live probes when computer is on

Run only after the local gates pass:

```text
forced inline submit-and-wait probe
forced blob submit-and-wait probe
matching receipts visible on GitHub issue #1
local repo returned to main with clean worktree
```

## Known limitations

1. This branch has not been exercised by the live watcher.
2. No local Codex execution was performed.
3. The implementation depends on `gh api` access to GitHub blob and issue-comment endpoints.
4. The conservative inline limit is configured, not empirically derived from a live GitHub mutation study.
5. The overlay patches `core.parse_ai_patch_body`, `core.make_ai_patch_comment`, and `core._post_receipt` at CLI startup; this compatibility strategy requires local bridge tests before merge.
