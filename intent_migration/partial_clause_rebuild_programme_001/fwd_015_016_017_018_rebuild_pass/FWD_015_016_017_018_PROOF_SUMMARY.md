# FWD-015/016/017/018 proof summary

| Proof | Result |
|---|---|
| Test-first failure | Collection failed before source mutation because required native seams were absent; see `proof/test_first_failure.txt`. |
| Targeted FWD tests | `14 passed`. |
| Adjacent downstream/review/API tests | `153 passed`. |
| Full Tier A suite | `600 passed`. |
| Proof block `fwd015_016_017_018_rebuild_surface` | `14 passed`. |
| `scripts/run_proof_block.py --check-all` | `proof_blocks_check_all=PASS count=51`. |
| Vocabulary synonym audit | `PASS candidates=0 vocabulary_touched=False`. |
| Vocabulary candidate review | `PASS blocked_candidates=0`. |
| Changed-file Black | clean. |
| Changed-file Ruff | clean. |
