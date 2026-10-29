# Review evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 024 / TESTER
- authorised scope: repaired IWO-U02 only; U03 not assessed
- source transport SHA-256: `75bd2c5aaacd96c792f65f27e4e6f42cf111a0ad5154da7f2fd72343f2bfb874`
- exact source transport filename: `NVDA_G03_TESTER_VI13R_U02_R024_1790131803_FULL_GIT_20260923.tar(1).gz`
- transported repository HEAD before review: `549ed340c45daaf60366fb7d102b982a6b81c2a2` / tree `c05e0ae6ab45b011f9d55b46b3653838f62faf49`
- rejected U02 candidate: `a77dc596b7cbc3f248097df94d8dd0bef4491bec`
- repaired U02 candidate: `5c62ec5147da718297b251b5a287405ebf3b4755`
- repaired candidate tree: `dc1293d2c3d7e234e53a8d663f25eac51f7086ab`
- accepted/promoted U01 forward `main` before U02 promotion: `b806447eb440a016826728af075e714beee23d31`
- candidate-to-transport `src/**` / `tests/**` changes: none
- rejected-to-repaired candidate `src/**` / `tests/**` diff SHA-256: `dc0ed8cbd9df3d6ce79ee77315eff80f43558842af811320e49642812329c651`
- repaired source/proof paths: `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u02_capture_schedule.py`

## Governing material inspected

Read in full before substantive review: root `README.md`, `GUARDRAILS.md`, root `AGENTS.md`, complete
current `EXEC_PLAN.md`, `tests/AGENTS.override.md`, `handoff/control/CURRENT_STATE.md` and the active
Reviewer-024 `REQUEST.md`. For semantic disposition the review also read the relevant accepted IWO
U02/U03 boundary, IRB BC-003/BC-004, BICP U02 proof obligations and private-state seam law,
Reviewer-023 disposition/commands, Worker repair request/evidence, complete repaired `api.py`, and
complete U02 product proof. U03 implementation acceptance was not assessed.

## Exact candidate validation

Validation ran in a detached worktree at the exact repaired candidate. Exact project-pinned tooling
was provisioned outside the repository from preserved project artefacts; candidate bytes were not
changed:

- Python 3.13.5
- pytest 9.0.3
- mypy 1.20.1 (compiled)
- Ruff 0.15.11

Results:

- focused U01+U02 pytest: **328 passed**
- concrete Reviewer-023 bypass regressions: **2 passed**
- strict positive mypy public-seam specimen: **rc 0**
- strict negative mypy public-seam specimen: **rc 1 as intended**, exactly 15 diagnostics at lines
  15, 18, 21, 23, 28, 34, 43, 48, 53, 59, 64, 67, 70, 73 and 76
- `python -m mypy src --show-error-codes`: **success; 15 source files**
- Ruff over `src tests tools`: **pass**
- product-proof structural validation: **pass; 6 families, 13/13 obligations**
- architecture validation: **pass; 0 dependency/public-seam violations**
- dependency validation: **pass**
- public-seam validation: **pass**
- `tests/architecture tests/bootstrap`: **74 passed**
- `architecture_kernel` promotion: **74 passed**
- candidate `git diff --check`: **rc 0**
- candidate `git fsck --full --strict`: **rc 0**
- exact candidate detached worktree after review validation: **clean**

The first direct strict-mypy specimen invocation omitted `MYPYPATH=src` and therefore produced only
an environment-level import-not-found result. It was corrected without repository mutation; the
corrected pinned positive/negative results above are the disposition-bearing evidence.

## R023-U02-F001 — CLOSED

The rejected implementation placed the same mutable `_U02State` object directly on both public
facets as `_state`; Reviewer 023 used ordinary attribute access to insert an overlapping policy and
erase policy truth outside the M-owned command seam. In the repaired candidate, `_CommandsV1` and
`_ReadsV1` store only private command/read callables. Ordinary access to `_state` raises
`AttributeError` on both facets. Bounded traversal of ordinary instance dictionaries and slots,
without descending through callables, surfaces no `dict`, `list`, `set` or mutable U02 state object.
This closes the exact bypass rather than renaming the same directly reachable capability.

The independent challenge then confirmed that public overlap registration still rejects the second
active policy and that the rejected policy is absent on referential read. This review deliberately
does not claim resistance to arbitrary function-closure introspection, monkey-patching,
`eval`/`exec` or unrestricted Python metaprogramming because the active Reviewer-024 request
explicitly places those outside the required bounded proof.

## Bounded U02 rechallenge

Independent runtime challenge plus the committed U02 proof established the requested concrete
contract points: immutable policy payload meaning; exact UTC `:00`/`:30` boundaries; non-overlap
with adjacent half-open policy transition accepted; exactly 30-second `[start,end)` slots; no slot
before activation or at/after deactivation; stable policy-ref/slot retry identity distinct from the
opaque capture ID; same-identity idempotency; conflicting slot or capture-ID reuse failure; and
referential policy/capture reads. Accepted U01 typed/public-seam controls remained green.

## Disposition

**PASS**.

The repaired U02 candidate may be lawfully promoted. U03 becomes authorised only after the accepted
candidate and this Reviewer-024 PASS/evidence are promoted to forward `main` with preserved ancestry.
