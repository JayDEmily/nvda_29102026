# ACTIVE_DURABILITY_CHECKPOINT_INDEX_012 receipt

Date: 2026-05-12

## Scope

Indexed smoke-tested durability checkpoint for commit `f8b94f1e8f535f66a351e1065d4437d9eb4755f7`.

## Checkpoint

- Path: `/mnt/data/NVDA10_2_CONTINUATION_CONTROL_SCAN_011_f8b94f1_2026-05-12.tar.gz`
- SHA256: `461c1863d068f5b649dec50a3aaf7963b2d84271a2428b97f11531d738c63de5`
- Size bytes: `59812957`
- Sidecar: `/mnt/data/NVDA10_2_CONTINUATION_CONTROL_SCAN_011_f8b94f1_2026-05-12.tar.gz.sha256`

## Smoke result

```text
HEAD=f8b94f1e8f535f66a351e1065d4437d9eb4755f7
branch=worker/handoff-control-repair-c466
status_count=0
fsck_bytes=0
physical_archive_count=0
skip_archive_count=11
manifest=PASS manifests=12 stale=0 full_read_false=0
```

## Boundaries

- No runtime/source/test/refactor/dependency/vocabulary/original Atlas/Bridge/generated-slice mutation was opened.
- No `_archive/*.tar.gz` payload was restored or used.

## Proof

Pre-final proof command output recorded:

- `git diff --check`: PASS/no output.
- surface-record/registry validator: PASS, errors 0, warnings 0.
- proof-block check-all: PASS count 46.
- selected current manifest validation before proof/report hash refresh: expected stale entry only for this leaf's proof file after writing proof output.

Final selected-manifest validation was rerun and superseded by later current-chain manifest validation: see `ACTIVE_DURABILITY_CHECKPOINT_INDEX_012_REPORT.json`, `ACTIVE_PROOF_PLACEHOLDER_CLOSURE_013_REPORT.json`, and later current manifest validators. The stale pre-final rerun instruction is closed as historical point-in-time wording.
