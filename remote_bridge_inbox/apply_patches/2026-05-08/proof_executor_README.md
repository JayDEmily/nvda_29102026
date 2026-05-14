# Remote bridge patch inbox — proof executor

Patch payload from `NVDA10_PM_WORKER_OUTPUT_VOCAB_PROOF_EXECUTOR_GREEN_2026-05-08.tar.gz`.

Source package:

```text
size_bytes: 49633
sha256: 4293da84cc1ba13f89ea4ccdd26dc712bf2d31712baea3de8d9daf8dbbe5d24c
```

Patch:

```text
PATCHES/001_manifest_proof_block_executor.patch
patch_size_bytes: 8365
patch_lines: 212
changed_files: 4
insertions: 126
deletions: 16
```

Expected workflow:

```text
GitHub Actions Apply Remote Bridge Patch
→ git apply --check
→ git apply
→ config control assertions
→ remove consumed patch file
→ commit resulting proof executor changes and receipt to main
```

Worker package recorded:

```text
proof_executor_contract_after_edit: 4 passed
make proof-block BLOCK=vocabulary_governance_conformance: 51 passed
py_compile_executor: status 0
diff checks: status 0
```
