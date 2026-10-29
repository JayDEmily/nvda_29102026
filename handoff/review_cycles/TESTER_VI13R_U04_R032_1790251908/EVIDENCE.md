# Tester evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 032 / TESTER
- authorised scope: repaired IWO-U04 only
- received source TAR SHA-256: `1ee90b744042b9f1f51d42dfbc0fa33885955217c5052544192287e4e9f82a38`
- received filename: `NVDA_G03_WORKER_VI12R_U04_R031_REPAIR_R032_HANDOFF_FULL_GIT_20260924.tar(1).gz`
- transported repository HEAD before Tester governance carry-forward: `7037306cc4e4962d88cc21f94e67d490b5fb79ae`
- Tester fixture-independence governance carry-forward commit: `6d90d86200a2139ed2a2d47511630d0c58edad6d`
- exact repaired candidate: `dc3b448191a2b2d3528ffb576b1ebc2c56839991`
- candidate tree: `3c7a42eb215d708a0f8d8db37727133ecc234275`
- rejected U04 predecessor: `e7eb44119bdf7fb22abacae8291788619792c96a`
- promoted U03 forward main before U04 promotion: `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec`
- candidate-to-review-governance `src/**`, `tests/**`, `config/**`, `tools/**`, `pyproject.toml` changes: none
- U05 production change: none

## Governing material inspected

Read before disposition: root `README.md`, full root `GUARDRAILS.md`, root `AGENTS.md`,
`tests/AGENTS.override.md`, complete current `EXEC_PLAN.md`, `CURRENT_STATE.md`, active Reviewer-032
request, Reviewer-031 response/evidence/result and disposition, predecessor Worker repair
response/evidence, accepted IRB BC-007/BC-008/BC-009/BC-010, IWO-U04, admitted U04 proof family and
physical U04 proof, exact repaired implementation/diff, and the relevant U04 failure/repair lineage.

The already-authorised fixture-independence Tester rule was carried into this lineage before
Reviewer-032 disposition because the Worker correctly worked from the earlier packet that predated
that governance-only commit. The candidate bytes remained frozen.

## R031-U04-F001 closure

Verified from exact candidate implementation and independent direct public-seam execution:

- assessment derivation does not read optional receipt-relation materialisation state;
- eligible in-slot admitted evidence produces `one_or_more_received` when the optional relation
  command is omitted;
- missing eligibility authority for admitted in-slot evidence raises `ValueError` rather than
  manufacturing semantic zero;
- `received_ts_utc` is not compared with `evidence_as_of_ts_utc` as a visibility surrogate;
- lawful no-evidence, ineligible and out-of-slot cases remain `zero_received`;
- same-ID retry preserves the previously appended assessment;
- later eligible evidence may append a new `one_or_more_received` assessment that supersedes the
  immediate predecessor while the earlier zero fact remains unchanged; and
- invalid non-immediate predecessor supersession is rejected.

A separate probe supplied an `evidence_as_of_ts_utc` earlier than the observation receipt time and
observed `one_or_more_received`. This is recorded as an observation, not a defect: current U04 law
defines the as-of field as system-knowledge time but does not provide a separate historical-query or
commit-clock mechanism, while Reviewer-031 specifically prohibited using receipt time as that proxy.
No new semantic rule was invented by Reviewer 032.

## Independent executable evidence

Environment:

- Python 3.13.5;
- pytest 9.0.2;
- `python -m mypy` unavailable (`No module named mypy`);
- Ruff executable/module unavailable in this Tester sandbox.

Exact candidate / frozen source results:

- U04 bounded proof: **32 passed**;
- U01-U04 aggregate with exactly the three mypy-invoking test bodies deselected: **413 passed, 3 deselected**;
- direct fixture-independent public-seam R031 closure sequence: **PASS**;
- expanded direct sequence matrix covering zero, positive-without-relation, missing authority,
  ineligible, out-of-slot, same-ID retry, later-evidence supersession and invalid predecessor:
  **PASS**;
- architecture/bootstrap with exactly the two mypy-invoking tests deselected: **72 passed, 2 deselected**;
- `tools/validate_product_proof.py`: **PASS**, six families / 13 of 13 obligations;
- `tools/validate_architecture.py`: **PASS**;
- `tools/check_dependencies.py`: **PASS**;
- `tools/check_public_seams.py`: **PASS**;
- candidate/review-governance diff check: **PASS**;
- strict Git integrity: exit 0, with five existing unreachable dangling blobs reported diagnostically.

The first aggregate executions that retained mypy-invoking tests failed only because this sandbox
has no mypy module. Those environmental failures were isolated rather than relabelled as candidate
failures.

## Worker evidence retained separately

Worker exact-pinned evidence on the same repaired candidate records:

- U04 32/32;
- U01-U04 416/416;
- mypy source and strict modified-API checks green;
- Ruff green;
- product/architecture/dependency/public-seam controls green;
- architecture/bootstrap and clean-state promotion 74/74.

These are Worker evidence and are not claimed as independently re-executed Reviewer results.

## Reviewer-032 conclusion

`R031-U04-F001` is closed. No new material U04 defect was established and no recurrence class is
opened by Reviewer 032.

**Disposition: PASS.**
