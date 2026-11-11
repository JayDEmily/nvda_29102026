# R2 G0/L00 — bounded candidate provenance clarification

**Scope:** documentary ledger binding only; no application/source/test/oracle/ExecPlan/governance change. Historical G0/SQLite documents from the reviewer’s 29-file packet were recovered into the working tree because the supplied cumulative Git bundle ended at the earlier G0 commit, not the originally reviewed final G0 candidate.

## Verified source identity and local ancestry

- GitHub R2 source **tree** `b849a781029ce8bafa6884f37f02386d2e8e6bfe` was preserved in the synthetic local source-tree snapshot commit `4559694b0c5bd53e98cd88936b80091adbc3b275`. It is **historical source provenance**, not the current G0 review candidate.
- Git objects directly verify `4559694b0c5bd53e98cd88936b80091adbc3b275` is an ancestor of activation `d4f9c09ebf81c3d4f96bc1fcf3f318323e0b27f3` and local G0/SQLite pin commit `22a2f13189fa3f1a55b2fef265f93a6696c0155f`.
- The prior final external `NVDA_R2_G0_SQLITE_FINAL_CANDIDATE_RECEIPT.json` identifies G0 candidate `f9a6de2400b22f361678ffd545d7e38666b8bae5`, expected tree `e3a8421b9d7df6619f850df3922f5dc1e72c92c2`, and final SQLite qualification. **That original f9a6 commit object and its additive bundle were not supplied or found in the reconstructed local history.** The external receipt is retained as an attributed original reviewer input, not asserted locally verified ancestry.
- The final G0 documentary records that were available in the document-only packet were restored with their original bytes and SHA-256 identities; this new branch is transparently derived from verified `22a2f131...`, not from unverified `f9a6de24...`. No original GitHub 61-commit lineage recovery is claimed.

## Active evidence ledger binding (no self-reference)

- `repository.candidate_commit` now holds the exact **pre-repair verified local G0 commit** `22a2f13189fa3f1a55b2fef265f93a6696c0155f`, no longer the historical R2 snapshot.
- `execution_mode.capability_evidence` explicitly labels old `4559694b...` as source-tree history and names the external prior final candidate receipt. This is a metadata-only qualification within the unchanged accepted ledger schema (no changes to 35 proof obligations or test status).
- The corrected **current** review commit SHA cannot be embedded within its own tracked ledger. An externally generated, post-commit `R2_G0_L00_METADATA_REPAIR_FINAL_RECEIPT.json` uniquely binds the new commit, tree, cumulative Git bundle, verified source/proof identities and fresh restoration. The prior `NVDA_R2_G0_SQLITE_FINAL_CANDIDATE_RECEIPT.json` remains evidence of the original reviewer’s candidate, not the current commit.

## Disposition boundary

This corrects the candidate-origin ambiguity without reclassifying any historical proof, granting G0 acceptance or requiring a product test. Independent reviewer must inspect the new candidate and verified post-commit checkpoint; original f9a6 ancestry remains unverified rather than invented. Existing G1–G4 holds and D145 PAUSED stay untouched.
