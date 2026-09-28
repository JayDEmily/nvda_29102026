# VI-18-L1 Worker evidence summary

- accepted predecessor close-out: `88499cc58767e25919a09c03ff0fdf9f5ea14e5e`;
- routed baseline/main: `4df802c3ebe67409125c58655534814f24b9ae2b` / tree `4a15cb1ba7877ee765a395c1d6cd1a986a72cb48`;
- branch: `work/vi18-l1-final-freeze-recovery`;
- accepted package candidate: `332c1f95da032f841e8779ef21fe3c1fceb698a2` / tree `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`;
- distribution: `nvda-architecture-kernel==1.0.0`;
- wheel SHA-256: `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- sdist SHA-256: `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`;
- product aggregate accepted result: VI-15-L2 Tester `eed5c5f6fa9eeda02886ed8fda0d6205177823e5`, 479/479 and 13/13;
- architecture aggregate accepted result: VI-15-L2 Tester `eed5c5f6fa9eeda02886ed8fda0d6205177823e5`, 74/74;
- whole-BICP re-challenge: VI-16 Tester `9f5f7e90b463365fb39c361f2e346d9e67c6d915`, re-observed 479/479 and 74/74;
- no substantive `src/**`, `tests/**`, `config/**`, `pyproject.toml` drift from accepted package/VI-16/VI-17 candidates to routed baseline;
- baseline `git diff --check`: PASS;
- baseline `git fsck --full --no-dangling`: PASS;
- recovery artefact: `NVDA_G03_VI18_L1_TERMINAL_RECOVERY_FULL_GIT_AND_PACKAGE_20260929.tar.gz`;
- recovery SHA-256: `156c0e720e69e1a31a307d8751582616f9187c6a3ee6947dfa22c413e840b251`;
- recovery bytes: `5965855`;
- fresh readback HEAD/tree/main equal routed baseline; clean status; diff-check/fsck/package manifest PASS;
- source/readback ref-set SHA-256: `2ea2adac6e8183ab8ee028c502741a8b28330787c321b75e4bdb7cd0cefd20a2`;
- first recovery archive was rejected before freeze for a manifest-only wrong ref digest and replaced by the recovery identity above;
- PyYAML 6.0.3 prior overlay binary/archive digest remains UNKNOWN as accepted in VI-17-L2;
- terminal VI-18 Tester acceptance remains UNPROVED.

Full semantic/boundedness evidence: `implementation/proof/VI18_L1_FINAL_FREEZE_RECOVERY_CANDIDATE_EVIDENCE.md`.
