# Tester evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 026 / TESTER
- authorised scope: repaired IWO-U03 only; U04 not assessed
- source transport SHA-256: `8c8ea063fb11de9ca059b77b80e56f857a3f6edcbfebf9fe8350b6b713fc18b7`
- exact source transport filename: `NVDA_G03_TESTER_VI13R_U03_R026_1790143078_FULL_GIT_20260923.tar(1).gz`
- transported repository HEAD before review: `418fb198ab1884e382171346f8868494e928b449`
- accepted/promoted U02 forward `main`: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- rejected original U03 candidate: `7cf8936f854fbed952a468ce06c2f2a0320d9291`
- repaired frozen U03 candidate: `6316735eb22bdbe243b02637f09376bf1200e43d`
- repaired candidate tree: `a9cc881f50b7a6adf021ce80fce52a330e9d203d`
- repaired candidate parent / Reviewer-025 handoff continuity: `8a87fc7ae8a2d55286840159bd9c5fb3610bcf62`
- repair paths: `src/nvda_desk/raw_signal_occurrence_truth/api.py` and `tests/product/raw_signal/test_u03_observation_native_temporal.py`
- repair binary diff SHA-256 over those paths: `5af39d80702380726633d379b719d99093dc8b7af46224ff7de06a40a9134cad`
- candidate-to-transport material diff over `src tests config tools pyproject.toml`: none

## Governing material inspected

Read in full before substantive review: root `README.md`, `GUARDRAILS.md`, root `AGENTS.md`, complete
current `EXEC_PLAN.md`, `tests/AGENTS.override.md`, `handoff/control/CURRENT_STATE.md`, active
Reviewer-026 `REQUEST.md`, accepted IRB, BICP Markdown and complete IWO. Also inspected Reviewer-025
disposition/evidence, Worker Reviewer-025 repair request/evidence/commands/result, the exact repair
diff, complete repaired `api.py`, complete U03 product proof and the public test support used only to
construct calls through the real production owner seam. Relevant accepted clauses are BC-005,
BC-006, BC-009 and BC-010. U04 implementation acceptance was not assessed.

## Exact candidate/tool binding

Validation ran in a detached worktree at exact candidate commit
`6316735eb22bdbe243b02637f09376bf1200e43d` / tree
`a9cc881f50b7a6adf021ce80fce52a330e9d203d`.

Initial environment preflight exposed pytest 9.0.2, no installed mypy module and no Ruff executable.
A search of preserved project artefacts found the exact project-pinned wheels. They were extracted
and installed outside the repository; required mypy dependency wheels were likewise taken from the
preserved AKR5 dependency-ingress artefact. Exact review tooling then reported:

- Python 3.13.5
- pytest 9.0.3
- mypy 1.20.1 (compiled)
- Ruff 0.15.11

No tool package was installed into or committed to the repository.

## Exact candidate validation

Observed results on the frozen candidate:

- focused U01+U02+U03 pytest: **368 passed**
- strict positive public-seam mypy specimen: **pass**
- strict negative public-seam mypy specimen: **expected rc 1**, all 15 intended negative sites diagnosed
- source mypy: **pass across 15 source files**
- Ruff over `src tests tools`: **pass**
- product-proof control: **pass, six families and 13/13 obligations**
- architecture validation: **pass, zero dependency/public-seam violations**
- dependency validation: **pass**
- public-seam validation: **pass**
- architecture/bootstrap: **74 passed**
- `architecture_kernel` promotion command: **74 passed**
- `git diff --check`: **pass**
- `git fsck --full --strict`: **pass**
- exact detached candidate worktree after validation: **clean**

One initial focused-pytest command used guessed historical U01/U02 filenames and returned pytest rc 4
because those paths do not exist in this candidate. The repository listing was then used and the
correct current paths produced 368/368. This command error did not mutate the repository and is not
attributed to the candidate.

## Reviewer-025 closure check

The exact required original conflict cases now behave correctly through the production public seam:

1. same observation ID, native `int(1)` then native `float(1.0)` -> retry rejected with `ValueError`;
   readback remains the first `int(1)`;
2. same observation ID, `Decimal("1.0")` then `Decimal("1.00")` -> retry rejected with
   `ValueError`; readback retains the first Decimal representation/scale;
3. the Worker regression separately reconstructs the first native mapping for each of those cases
   and the focused suite proves those ordinary identical reconstructions remain idempotent.

However, Reviewer-025's required outcome also states that separately reconstructed genuinely
identical native content must remain idempotent. The current implementation does not satisfy that
proposition for all native numeric values it currently admits.

## R026-U03-F001 — identical NaN retry is falsely rejected

**Status:** `OPEN` / material implementation defect.

**Concrete public-seam canaries:**

- first admit `native_record={"Native": float("nan")}`;
- reconstruct the same observation identity and a fresh `float("nan")` native value;
- retry -> `ValueError("observation occurrence identity is already admitted with different content")`;
- original observation remains stored;
- the same failure occurs for separately reconstructed `Decimal("NaN")` values.

The implementation first evaluates ordinary dataclass equality in
`_observations_exactly_equal`. NaN equality is non-reflexive across separately reconstructed values,
so that outer check returns false before `_native_values_exactly_equal` can establish the intended
native comparison. The result is a false conflict for genuinely reconstructed identical content.

**Accepted propositions defeated:** BC-010 idempotency for same opaque identity + identical content;
BC-005 preservation of admitted native value truth; IWO-U03 same-occurrence retry law and the active
Reviewer-026 explicit identical-reconstruction check.

**Owning layer:** U03 M-owner retry comparison plus bounded implementation-coupled U03 proof.

## R026-U03-F002 — complex signed-zero conflict is falsely accepted

**Status:** `OPEN` / material implementation defect.

**Concrete public-seam canary:**

- first admit `native_record={"Native": complex(-0.0, 0.0)}`;
- retry the same observation ID with `native_record={"Native": complex(0.0, 0.0)}`;
- retry -> accepted as the same occurrence rather than rejected;
- readback still exposes the original `(-0+0j)` native value.

The repair explicitly classifies `complex` as a native numeric type but compares it with ordinary
`==`; Python complex equality collapses the signed-zero component. The candidate therefore treats
changed native representation as identical content.

**Accepted propositions defeated:** BC-005 exact admitted native-value fidelity; BC-009 rejection of
conflicting payload under the same occurrence ID; BC-010 idempotency only for identical content; and
IWO-U03 native-fidelity/retry law.

**Owning layer:** U03 M-owner retry comparison plus bounded implementation-coupled U03 proof.

## Why these are in-scope realised inputs

`RawObservationOccurrenceV1.native_record` is currently typed as `Mapping[str, object]` and the
production snapshot checks that native field names are strings but imposes no provider-native value
exclusion covering NaN or complex values. Both challenge families were admitted successfully by the
real public owner command before retry comparison. BC-009 explicitly says not to define provider
bad-tick/duplicate/quarantine validity here, and the active Reviewer-026 request likewise prohibits
adding provider validity semantics. The review therefore cannot erase these observed failures by
assuming an unstated provider restriction.

## Disposition

**`FAIL / RETURN_TO_WORKER`**.

`R025-U03-F001` is not fully closed. U03 must not be promoted. U04 remains prohibited pending the
smallest bounded comparator repair and a fresh independent U03 re-review.
