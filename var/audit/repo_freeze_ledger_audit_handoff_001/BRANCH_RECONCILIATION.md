# Branch Reconciliation

| Branch | Exists? | HEAD commit | Status | Evidence present | Safe to use? | Notes |
|---|---|---|---|---|---|---|
| work/prl-minute-risk-profile-plan | yes | e91be6c031fc040a7bef232509013f644e5009d9 | superseded | git rev-parse | fallback_only | earlier accepted branch in chain; superseded by later branches |
| work/prl-minute-profile-contracts | yes | 7eb107f6527ef5dc37e584a88deecd4a5390d1e5 | superseded | git rev-parse | fallback_only | earlier accepted branch in chain; superseded by later branches |
| work/prl-minute-risk-profile-master-roadmap | yes | 3c5b1db57704c56445bc382c83faa536c1586a6b | superseded | git rev-parse | fallback_only | earlier accepted branch in chain; superseded by later branches |
| work/prl-minute-risk-profile-architecture-decisions | yes | a122379199c1f613c482d76e49016509cd5475d3 | verified_present | git rev-parse | fallback | verified architecture/planning baseline; superseded by candidate execution branch if freeze audit passes |
| work/prl-minute-risk-profile-execution-batch-001 | yes | c477e6a360cbb01a0652b40117922ae591a2ff45 | verified_present | git rev-parse | yes_after_freeze_audit | contains PRL execution batch commits and audit logs; selected as candidate next baseline subject to freeze commit |
| work/repo-freeze-ledger-audit-handoff | yes | c477e6a360cbb01a0652b40117922ae591a2ff45 | present_but_unverified | git rev-parse | use_as_freeze_branch | active freeze audit branch created from execution batch candidate |
