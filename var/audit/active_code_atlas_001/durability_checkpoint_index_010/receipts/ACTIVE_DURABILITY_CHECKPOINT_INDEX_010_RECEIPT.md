# ACTIVE_DURABILITY_CHECKPOINT_INDEX_010_RECEIPT

## Scope

Record the latest smoke-tested durability checkpoint for the continuation-control hardening branch.

## Checkpoint

- Path: `/mnt/data/NVDA10_2_CONTINUATION_CONTROL_HARDENING_2517326_2026-05-12.tar.gz`
- SHA256: `ea33bf52c8c43210be60d6061c48a6c2e7201139a4e6f14d6ae2ca604a88a42e`
- HEAD: `2517326fa13710f16fed1b1c5edf19e15b78a998`
- Branch: `worker/handoff-control-repair-c466`

## Smoke result

Clean unpack, `git status --short` count `0`, `git fsck --connectivity-only` exit `0`, skip-worktree archive count `11`, physical `_archive/*.tar.gz` count `0`, manifest validation `PASS` over ten current manifests with zero stale hashes and zero `full_read=false`.

## Boundaries

No runtime/source/test/refactor/dependency/vocabulary/original Atlas/Bridge/generated-slice mutation was opened.

No `_archive/*.tar.gz` payload was restored or used.

## Proof

- `git diff --check`: PASS, no output.
- `python3 var/audit/active_code_atlas_001/tools/validate_surface_records_and_registry.py`: PASS, `error_count=0`, `warning_count=0`.
- `python3 scripts/run_proof_block.py --check-all`: PASS, `count=46`.
- `python3 var/audit/active_code_atlas_001/tools/validate_full_read_manifest.py` over eleven current manifests: PASS, `stale_hash_mismatch_count=0`, `full_read_false_count=0`.

## Result

PASS. The durability checkpoint is indexed with smoke proof.
