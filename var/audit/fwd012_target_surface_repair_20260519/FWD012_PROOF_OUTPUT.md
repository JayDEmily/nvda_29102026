# FWD-012 proof output

## Row proof

Command:
```bash
env PYTHONPATH=src python3 -m pytest tests/tier_a/runtime/test_fwd012_reopened_row_serial_cognition_spine_proof.py -q
```

Exit status: `0`

Output:
```text
........................................................................ [ 51%]
...................................................................      [100%]
139 passed in 3.67s
```

## Targeted FWD-012 proof

Command:
```bash
env PYTHONPATH=src python3 -m pytest tests/tier_a/runtime/test_serial_stage_packet_emission_surface.py tests/tier_a/serial_recommendation tests/tier_b/serial_boundaries tests/tier_a/runtime/test_fwd012_reopened_row_serial_cognition_spine_proof.py -q
```

Exit status: `0`

Output:
```text
........................................................................ [ 43%]
........................................................................ [ 87%]
....................                                                     [100%]
164 passed in 4.17s
```

## git diff --check

Exit status: `0`
```text
```

## make scaffold-check

Exit status: `0`
```text
repo scaffold present
```

## proof block

Command:
```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/run_proof_block.py --check-all
```

Exit status: `0`
```text
proof_blocks_check_all=PASS count=51
```
