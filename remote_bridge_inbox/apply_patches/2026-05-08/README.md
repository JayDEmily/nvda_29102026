# Remote bridge patch inbox — 2026-05-08

Patch payload from `NVDA10_PM_WORKER_OUTPUT_VOCAB_PROOF_CONTROLS_GREEN_2026-05-08.tar.gz`.

Source package:

```text
size_bytes: 73363
sha256: 9983dfc3632fef20129db7f27e0761d855655ec2b7435b2c43d7e84ea527e790
```

Patch:

```text
PATCHES/001_vocabulary_retained_proof_controls.patch
patch_size_bytes: 7265
patch_lines: 111
changed_files: 2
```

Expected workflow:

```text
GitHub Actions Apply Remote Bridge Patch
→ git apply --check
→ git apply
→ YAML/control assertions
→ remove consumed patch file
→ commit resulting config changes and receipt to main
```
