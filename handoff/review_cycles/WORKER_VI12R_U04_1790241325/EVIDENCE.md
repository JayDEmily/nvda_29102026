# Worker cycle evidence

**Status:** `COMPLETE`

## Source and promotion binding

- received source TAR SHA-256: `3ee46b932bb45528eb1732abd97914534399e0fedc5f1ed211cee62b735d6d50`;
- received filename: `NVDA_G03_TESTER_VI13R_U03_R030_PASS_U04_HANDOFF_FULL_GIT_20260924.tar(1).gz`;
- received repository Reviewer-030 handoff HEAD: `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec`;
- accepted U03 candidate: `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf`;
- U03 authority clarification: `c4caa78a2d13c5dc115c83fedcdf44648efe6d78`;
- Reviewer-030 PASS: `dc40971d24ee773ee133d07622f92d709a7cec11`;
- forward `main` before promotion: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`;
- forward `main` after preserved-ancestry fast-forward: `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec` / tree `ecf42b1a7fc0d9d1e55444844142149612caeba2`;
- accepted candidate, clarification and Reviewer-030 PASS all verified as ancestors of promoted
  `main`;
- strict Git integrity exited 0 before U04 branch creation, with five dangling-blob diagnostics;
- fresh U04 branch: `work/vi12r-u04-receipt-assessment`.

## Frozen U04 candidate

- commit: `e7eb44119bdf7fb22abacae8291788619792c96a`;
- tree: `ea104900fcaf8e2db4177df3909956f464d6a918`;
- parent/promoted main: `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec`;
- changed path: `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
- candidate diff SHA-256: `6f0bb829cc752636958293068e2e0a4bbf4309ea7295b896edb98db255497e33`.

The owner state now carries capture-local receipt-evidence relations and append-only assessment
identity/order state. Relation derivation requires admitted observation and realised capture,
requires the supplied scope-policy reference to equal the capture's effective stored policy, applies
exact `[start,end)` receipt timing, and calls only the injected eligibility authority with the exact
stored observation/policy. Ineligible and out-of-slot observations lawfully preserve no relation.
Created relations use only `evidences_receipt_presence_only`.

Assessment append derives its own outcome from capture-local relation evidence visible at the
provided UTC system-knowledge as-of value. The U04 live append path yields zero or one-or-more; the
contract still admits the exact three discriminants and leaves restart-created unknown to U05 as
already declared by the accepted proof. New assessment identity is append-only, later records must
name the immediate predecessor, identical same-ID retry is idempotent, and conflicting reuse fails
closed. Referential assessment reads return the preserved chain without overwriting predecessors.

The optional persistence protocol exposes only `append_assessment(value)` and receives the already
constructed assessment. It cannot select eligibility or assessment outcome through the owner seam.
No U05 persistence/restart design, provider eligibility rules, exact count, membership, finality or
health semantics were added.

## Exact committed-candidate validation

Toolchain: Python 3.13.5; pytest 9.0.3; mypy 1.20.1 (compiled); Ruff 0.15.11. The pinned tools were
restored offline from the preserved project wheel evidence in the supplied historical IA archive;
network package retrieval was unavailable and was not relied upon.

On `e7eb44119bdf7fb22abacae8291788619792c96a` / `ea104900fcaf8e2db4177df3909956f464d6a918`:

- U04 proof: **29 passed**;
- U01+U02+U03+U04: **413 passed**;
- source mypy: success, 15 source files;
- strict/disallow-Any mypy on modified `api.py`: success;
- Ruff `src tests tools`: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- architecture validation: PASS, zero dependency/public-seam violations;
- dependency/public-seam checks: PASS;
- architecture/bootstrap: **74 passed**;
- architecture promotion: **74 passed**;
- `git diff HEAD^ HEAD --check`: pass;
- `git fsck --full --strict`: exit 0; dangling blobs
  `d9e05bce55672517b98b3b92de90379e30ec1be2`,
  `7293b42e4c2104678c5e61262e4b870f5056635e`,
  `895775b2d27b6006f3f245b6742d5d021fed089b`,
  `8b2975c927849b624b0d55b9118974975c91bada`, and
  `5f2b966adcbd83a68e901e79de258e620f15c8cc`;
- candidate status after validation: clean.

The bounded accepted U04 proof exposed no additional realised material escape requiring a new Worker
proof case before independent review. That is a Worker observation, not Reviewer acceptance.

U04 remains unaccepted pending fresh Reviewer 031. U05 and later remain prohibited.
