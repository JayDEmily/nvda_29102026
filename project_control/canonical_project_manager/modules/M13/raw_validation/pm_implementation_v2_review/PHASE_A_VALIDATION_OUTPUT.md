# Phase A validation output

Source checkpoint: `616fade4123def7870b7950bb3e644ffcc0ccc5a`

## Required tests

Command: `python -m pytest tests/tier_a/persistence/test_m13_state_kernel_contract.py -q`

Output: `152 passed in 0.49s`

Command: `python -m pytest tests/tier_a/persistence -q`

Output: `188 passed in 1.48s`

Command: `python scripts/run_proof_block.py --check-all`

Output: `proof_blocks_check_all=PASS count=52`

Command: `python -m pytest tests/tier_b/proof_model/test_proof_executor_contract.py -q`

Output: `21 passed in 2.94s`

Command: `python -m pytest tests/tier_b/proof_model/test_checkpoint_receipt_contract.py -q`

Output: `2 passed in 0.35s`

## Required checks

| Check | Exact result |
|---|---|
| M13 architecture-boundary validator | `architecture_boundary=PASS`; outgoing dependencies 0; M13 cycle membership 0 |
| Vocabulary exact parity | `1 passed in 0.14s` |
| YAML parsing | `yaml_files=10`; `yaml_parse=PASS` |
| Python compilation | `python_compile=PASS` |
| Ruff | `All checks passed!` |
| Black | `15 files would be left unchanged.` |
| `git diff --check` | exit 0 |
| `git fsck --full` | exit 0; no diagnostic output |
