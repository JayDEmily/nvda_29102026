# D014 control-review checkpoint — recovery evidence

This is recovery evidence, not control application, review acceptance or product proof.

Verified candidate: c990f8b936f3b5f1e981024699fcffafc67d2e2d; tree b48cad4ce5b0c6e6ba0c9e322bb541154e232f5c.

NVDA_V2_G61_D014_CONTROL_REVIEW_DELTA_20261020.bundle has SHA256 877b094423e220a43dd46efcb367c43b69fb77b5b986068919f4ae8891c0a322. It requires prerequisite164ddb5a479d7aa4a11ef4e12be1cf95e7c073ac; it is not a standalone full-Git archive. That prerequisite is preserved in NVDA_V2_G61_D014_CONTROL_RED_FULL_GIT_20261020.tar.gz, SHA256 fa4bc978d60a0f987dd4b852df8ce41c9a26ea44e0298ecbba3dc18b1055c1f3,100763463bytes. Both are saved, as are the unchanged unapplied patch and phase ruling.

Actual bundle verification succeeded. A fresh private clone of the recovered base fetched the bundle and checked out its HEAD at d014-delta-recovery-Fjydbd/repository. The first comparison to original working-file bytes failed on handoff/m01_completion/proof/f4_20261009/F4_CLASS_PROOF_RECONCILIATION.csv. Exact commit/tree already matched; no corruption diagnosis was inferred from that mismatch.

Inspection established the scoped cause: repository attributes prescribe LF for CSV, canonical Git blobs are LF, and 21 original historical working CSVs are CRLF. The revised verifier compared every restored tracked file to its actual Git blob, checking executable modes and symlinks, and independently compared original bytes: every differing original file becomes exactly the canonical blob after CRLF-to-LF conversion. All1813 tracked files/modes/links passed; restored git status is clean and git fsck --full exits0. Dangling historical objects are retained, not pruned.

This verifies restoration of the exact Git commit/tree, not a byte-identical reconstruction of the original working checkout. The full base archive preserves original working bytes; the delta carries the subsequent committed changes. No historical CSV, attribute, dependency or active loader was altered to resolve the comparison. The first failed comparison remains disclosed here rather than relabelled successful.

Library save results for the delta, exact patch and ruling each report succeeded and local identity applied. No remote reread was used to manufacture confirmation.

TS: 20-10-26 01:08
