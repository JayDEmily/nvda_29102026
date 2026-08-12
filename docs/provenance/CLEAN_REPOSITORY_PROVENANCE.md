# Clean repository provenance

This repository has a new Git history. It was not cloned from the R2 forensic repository and does not import that repository's `.git`, branches, reflogs, recovery worktree, or autonomous rollback state.

## Source identities

- full-history forensic archive SHA-256: `18ec9e5bdce4d1ec53ca8a8a1071c968be6d7876af4982b3da2a4f952d9538d8`
- byte source for accepted semantic/kernel baseline: Git commit `c0bfa6d`
- runtime-reference evidence only: Git commit `79cbbb9db4427ff574ffc87dab45036496d99e21`
- user-accepted Step-5 decision SHA-256: `8eedd78cf1d488ae0dac1842ca119e080b009ae17de9efd56672f67930abf354`
- Step-6 port authority SHA-256: `3acfe267c2697eef2100fb844bcc1b7b15f5d7339c44edaf75d8cf4a9b483bcd`

## New root baseline

- commit: `e137677e8c0f116ba21dadc2e951281820e09916`
- tree: `4f625f20f8882f3cdb249ac2b38046e28200d769`

The root baseline contains only `EXACT_PORT` destinations from the Step-6 manifest. Exact-port bytes are required to match the source SHA-256 even where historical formatting is imperfect.

## Construction

- branch: `restart/codex-control-v1`
- final candidate/accepted commit: deliberately not self-recorded in the candidate; the independent audit binds the exact candidate `HEAD` externally
- accepted `main`: remains at the root baseline until independent audit accepts the complete candidate

`docs/provenance/RESTART_PORT_MANIFEST.tsv` is the repository-local file disposition/provenance ledger. For exact ports, source and destination hashes must be identical. Rewritten/new destinations receive their final SHA-256 once their unit is committed. The manifest deliberately does not claim its own containing-commit hash.
