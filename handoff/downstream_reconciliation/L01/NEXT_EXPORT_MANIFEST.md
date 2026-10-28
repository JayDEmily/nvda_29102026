# L01 next cumulative additive export manifest

Status: documentary AUTHORITY_READY; product/runtime/static proof NOT_RUN. This committed manifest describes the next export without a self-referential bundle hash or commit SHA.

- Fixed baseline: `97f944d51ab9e403250fe76910e2754b50425c73`.
- Baseline archive SHA256: `4d02c82894513bff8d07af7a2af6a151cd3f5f14ece581ac0bf0d87ea9ed0430`.
- Producer work ref: `refs/heads/work/reconciliation-resumed`; export this current tip after committing L01, plus HEAD. Include the complete post-baseline closure. All original baseline refs are preserved locally under `refs/restored_baseline/*`; original names/tips and archive source are in TRANSFER_BASELINE.md. They are baseline prerequisites, not newly created post-baseline independent history.
- Expected filename: `NVDA_DOWNSTREAM_RECONCILIATION_L01_20261028_ADDITIVE_FROM_97f944d51ab9.bundle`.
- Export shape: `git bundle create <output.bundle> refs/heads/work/reconciliation-resumed HEAD ^97f944d51ab9e403250fe76910e2754b50425c73`.
- Restore: first restore/verify the identical original full-history L00 bundle and all its refs; then `git fetch <latest-additive.bundle> refs/heads/work/reconciliation-resumed:refs/heads/work/reconciliation-resumed`; `git checkout work/reconciliation-resumed`. Intermediate additive bundles are unnecessary.
- Controller must perform fresh baseline+additive restore, required ref/tip/tree comparisons, ancestry and `git fsck --full`, SHA256, save and expose the downloadable bundle. Record actual resulting HEAD/tree/ref inventory/hash externally; do not claim product correctness from these mechanical checks.
- Independent receiver baseline possession and L14 environment remain pending. D145 implementation, PostgreSQL runtime and live source capability remain outside scope.
