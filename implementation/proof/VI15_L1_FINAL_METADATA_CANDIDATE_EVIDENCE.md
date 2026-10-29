# VI-15-L1 — Final distribution metadata candidate evidence

## Status

**WORKER CANDIDATE FROZEN — FRESH INDEPENDENT TESTER REQUIRED.**

## Exact candidate

- branch: `work/vi15-l1-final-distribution-authority`;
- candidate commit: `466055a1cd5fe678a40049a00f0dc88158951d74`;
- candidate tree: `350568be5d5f790d71121fbac383349b9284d649`;
- accepted predecessor `main` at Worker start: `1e4e649115f4eac87d58bfa6ad6c1bbc9912b767`;
- pre-authority inspection commit: `bc01ebb5963525618e011b5aa3c11068e79fd66f`.

## Programme Owner authority

The Programme Owner explicitly selected the final distribution identity:

- name: `nvda-architecture-kernel`;
- version: `1.0.0`;

and then instructed the Worker to proceed.

The binding repository authority record is
`implementation/authority/VI15_L1_FINAL_DISTRIBUTION_AUTHORITY.md`.

## Candidate mutation

The candidate commit changes exactly four paths:

1. `pyproject.toml` — project version `0.1.0 -> 1.0.0`;
2. `src/nvda_desk/__init__.py` — `__version__` `0.1.0 -> 1.0.0`;
3. `tests/bootstrap/test_minimal_imports.py` — bootstrap assertion bound to `1.0.0`;
4. `implementation/authority/VI15_L1_FINAL_DISTRIBUTION_AUTHORITY.md` — records the exact Programme Owner decision and its bounded scope.

The distribution name remains `nvda-architecture-kernel`. No owner identity, import/module topology,
runtime dependency, Raw Signal semantic implementation, PostgreSQL mechanism or proof meaning is
changed by the candidate.

Historical evidence containing `0.1.0` is intentionally retained as historical evidence rather
than rewritten.

## Proof environment

Fresh preserved proof environment reconstructed from the accepted offline bootstrap assets:

- Python 3.13.5;
- pytest 9.0.3;
- mypy 1.20.1;
- Ruff 0.15.11;
- Psycopg 3.3.4;
- PostgreSQL 17.9;
- PyYAML 6.0.3 exposed from the already-present host installation because the preserved U05 proof
  bootstrap deliberately omits PyYAML;
- PostgreSQL settings verified: UTF8, `fsync=on`, `synchronous_commit=on`,
  `full_page_writes=on`, Unix-domain socket only.

## Post-freeze validation on exact candidate

Verified against exact commit `466055a1cd5fe678a40049a00f0dc88158951d74`:

- `nvda_desk.__version__ == "1.0.0"` — PASS;
- `tests/bootstrap/test_minimal_imports.py` — **2/2 passed**;
- VI-14 proposition-bearing integrated set:
  - U05 PostgreSQL durability family — **55/55 passed**;
  - U06 composition + whole-restart/real-PG integration remainder — **11/11 passed**;
  - combined VI-14 integrated boundary set — **66/66 passed**;
- `tests/architecture tests/bootstrap` — **74/74 passed**;
- product-proof structural validator — PASS, six admitted product families, 13/13 obligations;
- architecture structural validator — PASS;
- dependency direction/cycle validator — PASS;
- public-seam validator — PASS;
- mypy over `src` — success, 16 source files;
- Ruff over `src tests tools` — PASS;
- `git diff HEAD^..HEAD --check` — PASS.

The U05 durability family is execution-heavy. Two grouped invocations reached the command-wrapper
limit after emitting successful cases. No failure was inferred from those timeouts; the same exact
cases were split into bounded runs, and all 55 cases received explicit PASS results on the candidate.

## Scope boundary / nonclaim

VI-15-L1 establishes only exact Programme Owner authority and bounded application of final
name/version metadata. It does **not** claim VI-15-L2 package/build/install closure. In particular,
this Worker evidence does not substitute for the separate VI-15-L2 complete product/architecture
aggregate, wheel/sdist inventory, isolated installation or package-hash propositions.

## Worker disposition

**VERIFIED:** candidate `466055a1cd5fe678a40049a00f0dc88158951d74` applies exactly
`nvda-architecture-kernel==1.0.0` as authorised, with only the previously identified necessary
version-binding consequences, and the governed regression/static surfaces above remain green.

**UNPROVED:** fresh independent VI-15-L1 Tester acceptance. The Worker does not self-award PASS.

**NEXT LAWFUL ACTION:** fresh independent Tester review of exactly `466055a1cd5fe678a40049a00f0dc88158951d74` / tree
`350568be5d5f790d71121fbac383349b9284d649`. VI-15-L2 remains blocked until Tester PASS and promotion of the accepted VI-15-L1
lineage to `main`.
