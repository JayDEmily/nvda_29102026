# FWD-007 lineage acceptance audit

Status: `accepted_for_merge`

Input tarball: `NVDA10_2026-05-14_WORKER_FWD007_ORDERED_REPLAY_CLOSED_e0a39aa.tar.gz`

Starting branch: `worker/fwd007-ordered-replay-20260514`
Starting HEAD: `e0a39aa`

## Gate evidence

- Required root files were present.
- Git branch before Phase A: `worker/fwd007-ordered-replay-20260514`.
- Current pointer in `ROADMAP_LEDGER.md` records FWD-007 as `bounded_closed_current` and FWD-008 as the next ordered gate pending replay.
- FWD-007 selected raw-signal-family Atlas IDs covered: `123/123`.
- FWD-007 unresolved selected IDs: `0`.
- FWD-007 direct native Atlas links: `0`.
- FWD-007 grouped overlay coverage: `123`.
- Comparison status counts: `{'transform_required': 68, 'partially_satisfied': 55}`.
- Bridge-native satisfaction status counts: `{'transform_required': 68, 'missing': 22, 'partially_satisfied': 33}`.
- Status count separation check: `True`.

## Phase A command results

| Command | Exit | Evidence files |
|---|---:|---|
| `git status --short` | `0` | `reports/git_status_short.*` |
| `git diff --check` | `0` | `reports/git_diff_check.*` |
| `PYTHONPATH=src python scripts/vocabulary_synonym_audit.py --check-clean` | `0` | `reports/vocabulary_synonym_audit_clean.*` |
| `PYTHONPATH=src python -m pytest -q tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py` | `0` | `reports/vocabulary_synonym_candidate_pytest.*` |
| `python scripts/run_proof_block.py --check-all` | `0` | `reports/proof_blocks_check_all.*` |

## Vocabulary suppression acceptance check

`vocabulary_suppression_grep` matched only the retained Tier A guard test that asserts forbidden source tokens are absent from `src/nvda_desk/vocabulary_synonym_audit.py`; it did not match source-code suppression tokens in `src/`.

`score = 0` remains only in generic scoring reset/filter paths for protocol identifier fragments and Python function declaration identifier fragments.

## Merge decision

The worker lineage through FWD-007 is accepted for merge to `main`.

