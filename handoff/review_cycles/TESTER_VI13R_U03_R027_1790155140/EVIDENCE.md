# Tester evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 027 / TESTER
- authorised scope: repaired IWO-U03 only; U04 not assessed
- source transport SHA-256: `1dc60018abc1b525abd6d1e4cbe012bafdba62dca768825b53d9935ae60c57ba`
- exact source transport filename: `NVDA_G03_WORKER_VI12R_U03_R026_REPAIR_R027_HANDOFF_FULL_GIT_20260923.tar(1).gz`
- transported repository HEAD before review: `df78e9ef1031a5742d2163e7162e453d4db58191`
- accepted/promoted U02 forward `main`: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- rejected prior repaired U03 candidate: `6316735eb22bdbe243b02637f09376bf1200e43d`
- Reviewer-026 disposition commit: `f58aa8b9cd21f1ebd9b01b80a71213bd5d16c63b`
- repaired frozen U03 candidate: `758060930b015c23bf63a5de4d71c4d318760393`
- repaired candidate tree: `b819ffa1795e97e40374a59cedd42834233d2225`
- repair paths: `src/nvda_desk/raw_signal_occurrence_truth/api.py` and `tests/product/raw_signal/test_u03_observation_native_temporal.py`
- repair binary diff SHA-256: `357742537ccb3d13d80d2beb5c31fdff892e45cd743602b6cee405c1f3014504`
- candidate-to-transport material diff over `src tests config tools pyproject.toml`: none

## Governing material inspected

Read in full before substantive review: root `README.md`, `GUARDRAILS.md`, root `AGENTS.md`, complete
current `EXEC_PLAN.md`, `tests/AGENTS.override.md`, `handoff/control/CURRENT_STATE.md`, active
Reviewer-027 `REQUEST.md`, accepted IRB, BICP Markdown and complete IWO. Also inspected Reviewer-025
and Reviewer-026 dispositions/evidence, Worker Reviewer-026 repair request/evidence/commands/result,
the exact repair diff, complete repaired `api.py`, complete U03 proof and the public test support used
only to construct calls through the realised owner seam. Relevant accepted clauses are BC-005,
BC-006, BC-009 and BC-010. U04 implementation acceptance was not assessed.

Role consistency was established before review: `CURRENT_STATE.md`, active-cycle prefix and active
`REQUEST.md` all route to TESTER Reviewer 027 on repaired U03 only.

## Git / ancestry / transport verification

- received TAR SHA-256 independently read back as
  `1dc60018abc1b525abd6d1e4cbe012bafdba62dca768825b53d9935ae60c57ba`;
- candidate commit/tree independently read back exactly as requested;
- accepted U02 `main` is an ancestor of the repaired candidate;
- rejected candidate `6316735...` -> Reviewer-026 disposition `f58aa8b...` -> repaired candidate
  `7580609...` continuity is preserved;
- changes from repaired candidate to transported handoff HEAD are governance/handoff only; no
  candidate `src/**`, `tests/**`, `config/**`, `tools/**` or `pyproject.toml` bytes changed.

Validation ran in a detached worktree at exact candidate
`758060930b015c23bf63a5de4d71c4d318760393` / tree
`b819ffa1795e97e40374a59cedd42834233d2225`.

## Exact review toolchain

The base sandbox supplied Python 3.13.5 but not the project-pinned pytest/mypy/Ruff combination.
Preserved project wheel artefacts were inspected and the exact pinned review environment was
provisioned outside the repository. Final versions:

- Python 3.13.5
- pytest 9.0.3
- mypy 1.20.1 (compiled)
- Ruff 0.15.11

No tool package was installed into or committed to the repository.

## Reviewer-026 closure

The exact active-request closure checks pass through the production public seam:

1. separately reconstructed same-ID `float("nan")` -> idempotent;
2. separately reconstructed same-ID `Decimal("NaN")` -> idempotent;
3. same-ID `complex(-0.0, 0.0)` -> `complex(0.0, 0.0)` -> rejected;
4. rejected complex conflict leaves the original record unchanged;
5. prior same-ID `int(1)` -> `float(1.0)` and `Decimal("1.0")` -> `Decimal("1.00")` conflicts
   remain rejected under the complete 371-test U01+U02+U03 proof;
6. `_observations_exactly_equal` compares all non-native fields with their existing ordinary
   equality semantics before applying native-specific comparison.

Focused Reviewer-026 regressions: **3 passed / 40 deselected**.

## Exact candidate validation

Observed on the frozen candidate with the pinned environment:

- focused Reviewer-026 regressions: **3 passed**;
- complete U01+U02+U03 pytest: **371 passed**;
- source mypy: **Success: no issues found in 15 source files**;
- Ruff `src tests tools`: **All checks passed**;
- product-proof control: **PASS**, six families / 13 of 13 obligations;
- structural architecture validation: **PASS**, zero dependency/public-seam violations;
- dependency validation: **PASS**;
- public-seam validation: **PASS**;
- architecture/bootstrap: **74 passed**;
- `architecture_kernel` promotion: **74 passed**;
- `git diff HEAD^ HEAD --check`: **pass**;
- `git fsck --full --strict`: **pass**;
- exact detached candidate worktree: **clean**.

These green controls close the requested concrete repair checks but are evidence, not semantic
authority; the bounded challenge below remains dispositive.

## R027-U03-F001 — admitted native content still collapses under generic equality

**Status:** `OPEN` / material implementation defect / Critical.

Two minimal public-seam canaries independently demonstrate one comparator defect.

### Witness A — bytes versus bytearray

1. admit one observation with `native_record={"Native": b"abc"}`;
2. retry the same observation identity with
   `native_record={"Native": bytearray(b"abc")}`;
3. required result under exact-content retry law: conflicting content is rejected;
4. observed result: retry is accepted as idempotent; no exception is raised;
5. readback remains the first admitted `bytes` value.

At candidate `api.py:182-219`, `_native_values_exactly_equal` applies exact type/representation
handling only to selected numeric branches and list/tuple shape. Its generic fallback at line 219 is
ordinary `left == right`. Python regards `b"abc" == bytearray(b"abc")` as true, so distinct admitted
runtime representations collapse.

### Witness B — nested mapping key type

1. admit `native_record={"Native": {1: "x"}}`;
2. retry the same identity with `native_record={"Native": {1.0: "x"}}`;
3. required result: reject changed native content;
4. observed result: retry is accepted as idempotent; original nested `int` key remains stored.

The mapping branch at candidate `api.py:201-209` compares key sets and performs ordinary mapping
lookup. Python mapping/set key equality collapses `1` and `1.0`, so the nested key representation
change is not seen. `_NativeRecordSnapshot` at `api.py:156-173` requires only top-level native field
names to be exact strings; nested mappings remain admitted values.

The standalone canary contains only these two U03 retry propositions and returns **2 failed** because
both `pytest.raises` guards observe no rejection. This canary is external review evidence; it was not
added to the candidate repository.

### Authority impact

The realised public contract types `native_record` as `Mapping[str, object]`; both witnesses are
successfully admitted before retry comparison. No accepted provider-validity rule excludes them,
and BC-009 explicitly leaves provider bad-tick/duplicate/quarantine validity undefined. The review
therefore cannot close the escape by inventing a provider restriction.

The defect defeats:

- BC-005: preservation of provider-native field values without semantic collapse;
- BC-009: conflicting content under an existing occurrence identity must be rejected without
  replacing the admitted record;
- BC-010: same-occurrence retry is idempotent only for identical content;
- IWO-U03 native-fidelity and same-occurrence retry law.

**Owning layer:** U03 M-owner native retry comparator plus bounded implementation-coupled U03 proof.

**Smallest repair:** make native equality exact/runtime-type-sensitive across all values admitted by
the current U03 surface, including mapping keys at every nested level, while retaining the existing
special exact float/complex/Decimal handling and preserving current non-native field equality
semantics. Add focused regressions for `bytes` vs `bytearray` and nested `int` vs `float` mapping-key
change. Do not invent provider validity, duplicate/retransmission equivalence, U04 behaviour,
persistence/replay or downstream capability.

## Disposition

**`FAIL / RETURN_TO_WORKER`**.

`R026-U03-F001` and `R026-U03-F002` are **CLOSED**, but new `R027-U03-F001` is open. U03 must not be
promoted. U04 remains prohibited pending the smallest bounded comparator repair and a fresh
independent U03 re-review.
