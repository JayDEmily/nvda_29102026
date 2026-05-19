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
