# Non-310 completion claim audit surface summary

Surface pass/fail rule: a surface fails if any row is `unsupported_worker_claim`.

| surface | total_rows | pass/fail | implemented_in_tests_and_code | already_satisfied_by_existing_tests_and_code | test_only | code_only | evidence_only_not_implemented | deferred_by_authority | rejected_out_of_scope | duplicate_or_subsumed | unsupported_worker_claim |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FWD-004 — DMPV3 packet carriage | 73 | FAIL | 0 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 59 |
| FWD-006 — Raw capture and source temporal law | 108 | FAIL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 108 |
| FWD-009 — Prepared ingress and runtime context preparation | 51 | FAIL | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 49 |
| FWD-011 — Playbook library architecture | 95 | FAIL | 0 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 75 |
| FWD-012 — Serial desk-cognition spine | 139 | FAIL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 139 |
| FWD-014 — Downstream capital deployment authority | 2 | PASS | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| TOTAL | 468 | FAIL | 0 | 38 | 0 | 0 | 0 | 0 | 0 | 0 | 430 |

## Deterministic basis

- Direct active-code rows with unchanged baseline test/source refs were reclassified as `already_satisfied_by_existing_tests_and_code`.
- Grouped, status-group, ordered-replay, and cluster-based duplicate/subsumed claims were not accepted without row-specific canonical-parent proof and row-specific semantic-equivalence rationale.
- The baseline-vs-worker diff shows no native source/test/config/fixture mutation; the package is not an implementation package.
