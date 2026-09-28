# VI-15-L1 — Independent Tester disposition

**Date:** 2026-09-28  
**Role:** fresh independent `TESTER`  
**Reviewed candidate:** `466055a1cd5fe678a40049a00f0dc88158951d74`  
**Candidate tree:** `350568be5d5f790d71121fbac383349b9284d649`  
**Disposition:** `PASS`

## 1. Exact review boundary

The Tester reviewed the exact VI-15-L1 Worker candidate in a detached worktree, not the later handoff
branch tip. The candidate changes exactly four paths:

- adds `implementation/authority/VI15_L1_FINAL_DISTRIBUTION_AUTHORITY.md`;
- changes `[project].version` in `pyproject.toml` from `0.1.0` to `1.0.0`;
- changes `src/nvda_desk/__init__.py` runtime `__version__` from `0.1.0` to `1.0.0`;
- changes the matching bootstrap assertion in `tests/bootstrap/test_minimal_imports.py`.

The later handoff/routing commits do not alter the candidate bytes under review.

## 2. Programme Owner authority

The mandatory VI-15-L1 authority checkpoint is satisfied. The Programme Owner explicitly directed that
final distribution name remain `nvda-architecture-kernel`, that the final version be bumped to `1.0.0`,
and then instructed the Worker to proceed.

The repository authority record accurately captures that decision and limits it to distribution/version
metadata. No authority was supplied to reopen owner identity, module admission, dependencies, Raw Signal
semantics, PostgreSQL mechanism or VI-15-L2 package proof.

## 3. Candidate conformance

Direct inspection establishes:

- `[project].name == "nvda-architecture-kernel"`;
- `[project].version == "1.0.0"`;
- `nvda_desk.__version__ == "1.0.0"`;
- the bootstrap assertion expects exactly `1.0.0`;
- dependency declarations are unchanged;
- package/module topology is unchanged;
- M-owner/public-seam identity is unchanged;
- no Raw Signal semantic source or PostgreSQL configuration is changed by the candidate.

The candidate therefore applies the authorised metadata exactly and only its necessary version-binding
consequences.

## 4. Independent proof environment

A fresh proof environment was reconstructed from the preserved offline bootstrap and PostgreSQL runtime:

- CPython `3.13.5`;
- pytest `9.0.3`;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4` / psycopg-binary `3.3.4`;
- PostgreSQL `17.9`, UTF8;
- `fsync=on`;
- `synchronous_commit=on`;
- `full_page_writes=on`;
- Unix-domain-socket transport only.

The preserved bootstrap omits PyYAML; the already-present PyYAML `6.0.3` installation was exposed only as
that missing runtime dependency.

## 5. Independent executable evidence

Observed against the exact detached candidate:

- direct distribution/runtime metadata check: **PASS**;
- VI-14 integrated proposition-bearing set: **66/66 passed**;
- architecture/bootstrap: **74/74 passed**;
- product-proof control: **PASS**, six admitted physical product families, **13/13** obligations;
- architecture structural validation: **PASS**;
- dependency direction/cycle validation: **PASS**;
- public-seam validation: **PASS**;
- mypy: **success, 16 source files**;
- Ruff: **PASS**;
- candidate diff check: **PASS**;
- exact candidate worktree remained clean;
- `git fsck --full`: exit `0`; dangling blobs only, no integrity failure.

The VI-14 regression emitted one Python multiprocessing/fork deprecation warning and no assertion failure,
skip, xfail or degraded substitute.

## 6. Leaf boundary

VI-15-L1 does not establish wheel/sdist build correctness, package inventory, isolated installation,
installed-distribution behaviour or package hashes. Those propositions belong to VI-15-L2 and were not
claimed here.

## 7. Disposition

`PASS`.

No material VI-15-L1 defect was established. No recurrence classification is opened because there is no
Tester finding to return.

The exact candidate `466055a1cd5fe678a40049a00f0dc88158951d74` / tree
`350568be5d5f790d71121fbac383349b9284d649` is independently accepted for preserved-ancestry
VI-15-L1 promotion/close-out only. VI-15-L2 remains prohibited until that promotion/close-out succeeds
and current-state routing explicitly advances.
