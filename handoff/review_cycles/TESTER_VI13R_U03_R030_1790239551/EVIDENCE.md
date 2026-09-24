# Tester evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 030 / TESTER
- authorised scope: U03 NativeValueV1 class-level closure only
- received source TAR SHA-256: `88e54bf699fe53c9e23f4ab4da9a0abed0bae6a46924c88fbe1002d47ca6b9f8`
- received filename: `NVDA_G03_WORKER_VI12R_U03_NATIVE_DOMAIN_CLOSURE_R030_HANDOFF_FULL_GIT_20260924.tar(1).gz`
- transported repository HEAD before review: `c6da5aa31d1b2dd999261b0b1433e93e1427abe1`
- exact candidate: `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf`
- candidate tree: `81ef8edc93c9b322b29cdec6b9ab76b731d8e9a5`
- accepted/promoted U02 forward main before U03 promotion: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- candidate-to-transport `src/**`, `tests/**`, `pyproject.toml` changes: none
- U04 production change: none

## Governing material inspected

Read before disposition: root `GUARDRAILS.md`, root `AGENTS.md`, complete current `EXEC_PLAN.md`, `tests/AGENTS.override.md`, `CURRENT_STATE.md`, active Reviewer-030 request, current U03 NativeValueV1 authority, IRB BC-005/006/009/010/012, IWO-U03/U04 boundary, candidate implementation/proof, Worker closure evidence/commands, and Reviewer-025..029 finding/repair lineage.

Reviewer 030 also inspected the official Python Typing Specification nominal-subtyping/assignability rule because the review exposed a static/runtime representability inconsistency in the Tester-authored authority. That authority issue is resolved in `implementation/authority/VI13R_U03_NATIVE_VALUE_STATIC_TYPING_CLARIFICATION.md` at authority commit `c4caa78a2d13c5dc115c83fedcdf44648efe6d78` without changing runtime carrier semantics.

## Independent candidate evidence

Environment preflight:

- Python 3.13.5 available;
- pytest available;
- `python -m mypy` unavailable (`No module named mypy`).

Exact candidate detached worktree results:

- U01+U02+U03 with only the three mypy-invoking test bodies deselected: **381 passed, 3 deselected**;
- independent NativeValueV1 runtime challenge: **PASS**;
  - exact float NaN payload/sign representation retained and conflicting bit patterns rejected;
  - exact Decimal representation retained and scale change rejected;
  - `int`/`float`/`str`/`bytes`/`Decimal` subclasses fail closed at runtime;
- independent public alias structure inspection: **PASS**;
  - `RawObservationOccurrenceV1.native_record` resolves to `Mapping[str, NativeValueV1]`;
  - recursive alias traversal contains no `Any` or `object` escape;
- `tools/validate_product_proof.py`: **PASS**, 6 families / 13 of 13 obligations;
- `tools/validate_architecture.py`: **PASS**;
- `tools/check_dependencies.py`: **PASS**;
- `tools/check_public_seams.py`: **PASS**;
- candidate `git diff --check`: **PASS**;
- candidate `git fsck --full --strict`: exit 0; diagnostic only for existing dangling blob `895775b2d27b6006f3f245b6742d5d021fed089b`.

The first aggregate invocation had two U01 mypy-invoking tests still selected due incorrect deselect names; both failed solely with `/opt/pyvenv/bin/python: No module named mypy`. The corrected invocation deselected exactly those two plus the U03 mypy-invoking static specimen and produced 381/381 on all remaining tests. No candidate mutation was made.

## Worker evidence retained separately

Worker exact-pinned evidence on the same candidate records:

- Python 3.13.5, pytest 9.0.3, mypy 1.20.1, Ruff 0.15.11;
- U03 56/56;
- U01+U02+U03 384/384;
- source mypy and strict modified-API mypy green;
- Ruff green;
- product/architecture/dependency/public-seam controls green;
- architecture/bootstrap 74/74;
- architecture promotion 74/74.

These are not claimed as independently re-executed Reviewer results.

## Reviewer-030 conclusion

No material defect was established inside the authorised NativeValueV1 carrier. The previous witness-by-witness equality mechanism has been replaced by a closed runtime carrier/exactness mechanism, and the static/runtime representability wording has been corrected at its owning authority layer rather than routed as an impossible Worker patch.

**Disposition: PASS.**
