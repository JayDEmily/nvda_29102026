# FWD-011 test-first receipt

- New row-level proof test: `tests/tier_a/playbook/test_fwd011_reopened_row_playbook_library_authority_proof.py`.
- First run before final branch completion exposed one missing behaviour branch: `service_identity`; output recorded in `fwd011_row_proof_initial.out` with `2 failed, 73 passed`.
- The test was repaired by adding the missing service-identity behavioural assertion branch.
- Final row proof: `75 passed in 1.94s`.
- Targeted surface proof: `145 passed in 1.82s`.
- No production/runtime source, config, fixture, vocabulary, original Atlas/Bridge JSON, or generated surface-slice files were changed.
