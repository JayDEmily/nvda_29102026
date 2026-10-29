# L07 next cumulative additive export manifest

Status: IMPLEMENTED_UNTESTED; product/runtime/static proof NOT_RUN. This committed manifest describes the export before the resulting HEAD and bundle SHA-256 exist.

- Fixed baseline: 97f944d51ab9e403250fe76910e2754b50425c73; original L00 archive SHA-256 4d02c82894513bff8d07af7a2af6a151cd3f5f14ece581ac0bf0d87ea9ed0430. Its starting refs are in handoff/downstream_reconciliation/TRANSFER_BASELINE.md.
- Export current refs/heads/work/reconciliation-resumed and HEAD with all reachable post-baseline objects, excluding unchanged baseline history. Expected file: NVDA_DOWNSTREAM_RECONCILIATION_L07_20261028_ADDITIVE_FROM_97f944d51ab9.bundle.
- Restore identical original L00 full-history archive/bundle and refs first; then git fetch <latest-additive.bundle> refs/heads/work/reconciliation-resumed:refs/heads/work/reconciliation-resumed and git checkout work/reconciliation-resumed. Intermediate L01–L06 additive files are not prerequisites.
- Controller verifies fresh-baseline prerequisites, restored HEAD/ref/tree/object identity, git fsck --full, SHA-256 and clean committed tree, then saves/exposes the newest downloadable bundle. These checks establish transfer integrity, not product correctness.
- Independent receiver possession of identical L00 baseline and L14 semantic/static/runtime review remain pending. D145 implementation, PostgreSQL runtime and live source capability remain excluded.
