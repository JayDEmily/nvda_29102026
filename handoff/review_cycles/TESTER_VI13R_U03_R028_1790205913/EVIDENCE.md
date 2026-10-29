# Tester evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 028 / TESTER
- authorised scope: repaired IWO-U03 only; U04 not assessed
- source transport SHA-256: `5faa4e3b798e5dc1f893b4f7e3105f914f21516fb38fbf6d09442ba4cca1e7d5`
- exact source transport filename: `NVDA_G03_WORKER_VI12R_U03_R027_REPAIR_R028_HANDOFF_FULL_GIT_20260924.tar(1).gz`
- transported repository HEAD before review: `8ea8a3af3572d6a84859e00db91d15640ef6c0d6`
- accepted/promoted U02 forward `main`: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- rejected prior repaired U03 candidate: `758060930b015c23bf63a5de4d71c4d318760393`
- Reviewer-027 disposition commit: `31b76489b1ec32fa38921bd3f5e97e40f544e23e`
- repaired frozen U03 candidate: `06735b3682d79387ebaa4da70002e6685d52740a`
- repaired candidate tree: `b73b6ba4486eba9ae3aa4c1facc626579c8b8ee5`
- repair paths: `src/nvda_desk/raw_signal_occurrence_truth/api.py` and `tests/product/raw_signal/test_u03_observation_native_temporal.py`
- repair binary diff SHA-256: `e1dbcf371f893f75decea7701bc43415a4cdd2488fefa74221531ad1fb5c6c4d`
- candidate-to-transport material diff over `src tests config tools pyproject.toml`: none

## Governing material inspected

Read in full before substantive review: root `README.md`, `GUARDRAILS.md`, root `AGENTS.md`, complete
current `EXEC_PLAN.md`, `tests/AGENTS.override.md`, `handoff/control/CURRENT_STATE.md`, active
Reviewer-028 `REQUEST.md`, accepted IRB and complete IWO. Also inspected Reviewer-027 disposition,
Worker Reviewer-027 repair request/evidence/commands/result, the exact repair diff, repaired
`api.py`, complete U03 proof and public proof support used to construct calls through the realised
owner seam. Relevant accepted clauses are BC-005, BC-006, BC-009 and BC-010. U04 implementation
acceptance was not assessed.

Role consistency was established before review: `CURRENT_STATE.md`, active-cycle prefix and active
`REQUEST.md` all route to TESTER Reviewer 028 on repaired U03 only.

## Git / ancestry / transport verification

- received TAR SHA-256 independently read back as
  `5faa4e3b798e5dc1f893b4f7e3105f914f21516fb38fbf6d09442ba4cca1e7d5`;
- candidate commit/tree independently read back exactly as requested;
- accepted U02 `main` is an ancestor of the repaired candidate;
- rejected candidate `7580609...` -> Reviewer-027 disposition `31b7648...` -> repaired candidate
  `06735b3...` continuity is preserved;
- changes from repaired candidate to transported handoff HEAD are governance/handoff only; no
  candidate `src/**`, `tests/**`, `config/**`, `tools/**` or `pyproject.toml` bytes changed;
- `git fsck --full --strict` passed.

Validation ran in a detached worktree at exact candidate
`06735b3682d79387ebaa4da70002e6685d52740a` / tree
`b73b6ba4486eba9ae3aa4c1facc626579c8b8ee5`.

## Exact review toolchain

The base sandbox supplied Python 3.13.5 but only pytest 9.0.2 and no mypy. Preserved project wheel
artefacts were inspected and the exact pinned review environment was provisioned outside the
repository. Final versions:

- Python 3.13.5
- pytest 9.0.3
- mypy 1.20.1 (compiled)
- Ruff 0.15.11

No tool package was installed into or committed to the repository.

## Reviewer-027 closure assessment

The two concrete Reviewer-027 witnesses now pass through the production public seam:

1. same-ID native `bytes(b"abc")` -> `bytearray(b"abc")` -> rejected;
2. same-ID nested native mapping key `int(1)` -> `float(1.0)` -> rejected;
3. each rejected retry leaves the first admitted record unchanged;
4. earlier same-ID int/float and Decimal-scale conflicts remain rejected;
5. separately reconstructed same-ID native NaN values remain idempotent;
6. complex signed-zero native content changes remain rejected;
7. non-native observation fields retain their existing ordinary equality semantics.

Focused Reviewer-027 regressions: **2 passed**.

The active Reviewer-028 request, however, makes closure broader than those two concrete examples: it
requires exact/runtime-type-sensitive native retry equality through admitted nested mapping
keys/values and **standard nested sequence/set values rather than falling back to Python equality
where it collapses representation**. The candidate does not yet establish that proposition.
`R027-U03-F001` is therefore **not fully closed**.

## Exact candidate validation

Observed on the frozen candidate with the pinned environment:

- focused Reviewer-027 regressions: **2 passed**;
- complete U01+U02+U03 pytest: **373 passed**;
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

These controls establish the worker's explicit repairs and surrounding regression state. They do not
establish the broader native exact-content proposition required by the active review request.

## R028-U03-F001 — same-type standard sequence representation still collapses under generic equality

**Status:** `OPEN` / material implementation defect / Critical.

Candidate `_native_values_exactly_equal` first requires exact runtime-type equality and contains
special exact branches for Decimal, float and complex. It recursively handles mappings, only
`list`/`tuple` sequences, and `set`/`frozenset`. At `api.py:236` all other admitted values still
return ordinary `left == right`.

Two minimal external public-seam canaries independently demonstrate the same root defect. Both
witness classes are standard-library `collections.abc.Sequence` instances, both are admitted by the
current public U03 `native_record` surface, and both retain the same runtime type across the retry.

### Witness A — `array.array` typecode change

1. admit `native_record={"Native": array('b', [1])}`;
2. retry the same observation identity with `array('B', [1])`;
3. required result: reject changed native content;
4. observed result: no `TypeError`/`ValueError`; retry is accepted as idempotent;
5. readback remains the first admitted `array('b', [1])` record.

Python reports the two arrays equal even though the representation-bearing `typecode` changes from
signed byte (`b`) to unsigned byte (`B`). The candidate's type check does not distinguish them
because both values have runtime type `array.array`; the generic ordinary-equality fallback therefore
collapses the change.

### Witness B — `range` bounds change

1. admit `native_record={"Native": range(0, 3, 2)}`;
2. retry the same identity with `range(0, 4, 2)`;
3. required result: reject changed native content;
4. observed result: no `TypeError`/`ValueError`; retry is accepted as idempotent;
5. readback remains the first admitted `range(0, 3, 2)` record.

Both ranges yield the same sequence `[0, 2]`, so ordinary Python range equality returns true even
though the native `stop` bound differs. The same generic fallback collapses that representation.

An external two-test canary using only the realised public owner seam returns **2 failed** because
both `pytest.raises` guards observe no conflicting-content rejection. This canary was not added to
the candidate repository.

### Authority impact

The realised public contract continues to type `native_record` as `Mapping[str, object]`; both
witnesses are successfully admitted before retry comparison. No accepted provider-validity rule
excludes them, and BC-009 leaves provider validity semantics undefined, so this review cannot close
the escape by inventing a provider restriction.

The defect defeats:

- BC-005: provider-native values must preserve exact native content rather than collapse changed
  representation;
- BC-009: conflicting content under an existing observation identity must be rejected without
  replacing the admitted record;
- BC-010: same-occurrence retry is idempotent only for identical content;
- IWO-U03 native-fidelity and same-occurrence retry law;
- the active Reviewer-028 request's explicit standard-sequence exactness condition.

**Owning layer:** U03 M-owner native retry comparator plus bounded implementation-coupled U03 proof.

**Smallest repair:** remove the remaining ordinary-equality collapse for admitted standard sequence
values. Preserve exact representation-bearing state for the two verified witnesses (`array.array`
`typecode`; `range` start/stop/step), retain all already-closed Decimal/float/complex/mapping/list/
tuple/set/frozenset behaviour and preserve existing non-native field equality semantics. Add focused
U03 regressions for the two Reviewer-028 witnesses. Do not invent provider validity,
duplicate/retransmission equivalence, U04 behaviour, persistence/replay or downstream capability.

No broader redesign is required or authorised by this finding.

## Disposition

**`FAIL / RETURN_TO_WORKER`**.

The two explicit Reviewer-027 example escapes are closed, but `R027-U03-F001` is **not fully closed**
and successor finding `R028-U03-F001` is open. U03 must not be promoted. U04 remains prohibited
pending the smallest bounded comparator repair and a fresh independent U03 re-review.
