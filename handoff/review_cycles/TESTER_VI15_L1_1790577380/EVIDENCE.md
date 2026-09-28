# Tester evidence

**Status:** `COMPLETE`

## Binding

- cycle: `TESTER_VI15_L1_1790577380`
- role: fresh independent `TESTER`
- leaf: `VI-15-L1 — final distribution/version authority closure`
- received handoff SHA-256: `9536d3f5d5d08defe20caa208da680dab73f78ac858a509addcbacefe9f527a8`
- received filename: `NVDA_G03_VI15_L1_METADATA_CANDIDATE_TESTER_HANDOFF_FULL_GIT_20260928.tar(1).gz`
- transported branch tip: `f64167eba9dba3d289f94bd2e1af37f662b7fcd5`
- exact candidate: `466055a1cd5fe678a40049a00f0dc88158951d74`
- candidate tree: `350568be5d5f790d71121fbac383349b9284d649`

## Authority and candidate scope

The Programme Owner instruction retained distribution name `nvda-architecture-kernel`, selected final
version `1.0.0`, and then instructed the Worker to proceed. The candidate matches that authority exactly.

The candidate commit changes only:

1. the VI-15-L1 authority record;
2. `[project].version` in `pyproject.toml` from `0.1.0` to `1.0.0`;
3. `nvda_desk.__version__` from `0.1.0` to `1.0.0`;
4. the corresponding bootstrap version assertion.

No dependency, module-topology, Raw Signal semantic, owner/public-seam or PostgreSQL configuration change is
present in the candidate diff.

## Independent proof environment

Fresh preserved environment verified as Python 3.13.5, pytest 9.0.3, mypy 1.20.1, Ruff 0.15.11,
Psycopg 3.3.4 and PostgreSQL 17.9 / UTF8 / fsync=on / synchronous_commit=on / full_page_writes=on /
Unix-domain-socket transport. PyYAML 6.0.3 from the already-present Python 3.13 installation was exposed
only as the bootstrap's missing runtime dependency.

## Independent execution

Against the exact detached candidate:

- direct metadata/runtime identity: `nvda-architecture-kernel==1.0.0`, runtime `__version__ == "1.0.0"`;
- VI-14 integrated proposition-bearing regression: **66/66 passed**;
- architecture/bootstrap: **74/74 passed**;
- product-proof control: **PASS**, six admitted families / **13/13** obligations;
- structural architecture validation: **PASS**;
- dependency direction/cycle validation: **PASS**;
- public-seam validation: **PASS**;
- mypy: **success, 16 source files**;
- Ruff: **PASS**;
- candidate diff check: **PASS**;
- exact candidate worktree remained clean;
- Git integrity: `git fsck --full` exit `0`; dangling blobs only, no integrity failure.

## Scope boundary

No VI-15-L2 package/build/install proposition was tested or claimed. Wheel/sdist construction, archive
inventory, isolated installation and package hashes remain the next leaf after lawful VI-15-L1 promotion.

## Disposition

`PASS`. No material VI-15-L1 finding was established. The exact candidate is accepted for lawful
preserved-ancestry VI-15-L1 promotion/close-out only.
