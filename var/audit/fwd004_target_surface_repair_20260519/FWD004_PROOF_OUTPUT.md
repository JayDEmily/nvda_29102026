# FWD-004 proof output

| proof | command file | status file | observed result |
|---|---|---|---|
| baseline targeted packets | `reports/baseline_targeted_pytest.command` | `reports/baseline_targeted_pytest.status` | `12 passed`; status `0` |
| row-specific reopened proof | `reports/test_first_reopened_rows.command` | `reports/test_first_reopened_rows.status` | `59 passed`; status `0` |
| targeted FWD-004 packets | `reports/targeted_fwd004_packets.command` | `reports/targeted_fwd004_packets.status` | `71 passed`; status `0` |
| diff whitespace check | `reports/git_diff_check.command` | `reports/git_diff_check.status` | status `0` |
| scaffold check | `reports/scaffold_check.command` | `reports/scaffold_check.status` | `repo scaffold present`; status `0` |
| proof block check-all | `reports/proof_blocks_check_all.command` | `reports/proof_blocks_check_all.status` | `proof_blocks_check_all=PASS count=51`; status `0` |

No proof command was silently downgraded.

## Final reruns after closeout hygiene correction

| proof | command file | status file | observed result |
|---|---|---|---|
| final diff whitespace check | `reports/final_git_diff_check.command` | `reports/final_git_diff_check.status` | status `0` |
| final targeted FWD-004 packets | `reports/final_targeted_fwd004_packets.command` | `reports/final_targeted_fwd004_packets.status` | `71 passed`; status `0` |
| final proof block check-all | `reports/final_proof_blocks_check_all.command` | `reports/final_proof_blocks_check_all.status` | `proof_blocks_check_all=PASS count=51`; status `0` |
