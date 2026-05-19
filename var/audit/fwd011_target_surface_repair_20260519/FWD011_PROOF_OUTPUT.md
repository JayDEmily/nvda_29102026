# FWD-011 proof output

## Row-level reopened-row proof

- Command: `env PYTHONPATH=src python3 -m pytest tests/tier_a/playbook/test_fwd011_reopened_row_playbook_library_authority_proof.py -q`
- Exit status: `0`

```text
........................................................................ [ 96%]
...                                                                      [100%]
75 passed in 1.94s

```

## Targeted FWD-011 surface proof

- Command: `env PYTHONPATH=src python3 -m pytest tests/tier_a/playbook tests/tier_b/serial_boundaries/test_playbook_eligibility_decontamination.py -q`
- Exit status: `0`

```text
........................................................................ [ 49%]
........................................................................ [ 99%]
.                                                                        [100%]
145 passed in 1.82s

```

## git diff --check

- Command: `git diff --check`
- Exit status: `0`

```text

```

## make scaffold-check

- Command: `make scaffold-check`
- Exit status: `0`

```text
repo scaffold present

```

## proof block check all

- Command: `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/run_proof_block.py --check-all`
- Exit status: `0`

```text
proof_blocks_check_all=PASS count=51

```

