# VI12R U06 Stage 2 — governed typed delegation and semantic dataflow evidence

## Status

**WORKER STAGE 2 COMPLETE — STAGE 3 NOT STARTED.**

This record is Worker evidence for U06 Stage 2 only. It is not U06 acceptance, Tester review,
or promotion.

## Governing boundary

- Active U06 ExecPlan on `main`: `c3ae566ff8367d83dc783289d9b553faa9a51325`.
- Stage 1 boundary predecessor: `674621f7c4c548f382b709c6ba0a7aa13a4dfc0c`.
- Stage 2 implementation/proof commit: `af3bc77349ccaff943f3eabbcce2e25612a42e3b`.
- Stage 2 implementation/proof tree: `d1adad06919c6b31f054dab8ba4d81b144f2cf99`.
- Work branch: `work/u06-a00-composition`.

## Changed production surface

Stage 2 changes only:

- `src/nvda_desk/composition/__init__.py`

No file under `src/nvda_desk/raw_signal_occurrence_truth/**` changed.

## VERIFIED Stage 2 proposition

The committed Stage 2 tree establishes the bounded A00 orchestration path required by IWO-U06:

1. `Application.run_raw_signal_proof_sequence(...)` delegates the authorised sequence through the
   M00 `commands` and `reads` facets only.
2. Policy registration occurs before any capture operation.
3. The caller-supplied scope-policy reference is checked against the identity/version of the
   policy submitted to and accepted by M00; mismatch fails before capture realisation.
4. Capture realisation receives the authoritative slot input, caller capture identity and checked
   policy reference.
5. Relation derivation receives the exact observation identity returned by M00, the exact capture
   identity returned by M00 and the effective policy reference returned on that capture.
6. Assessment append receives the exact capture identity returned by M00 plus the authoritative
   assessment identity, evidence-as-of timestamp and supersession input.
7. Referential readback uses the exact observation identity returned by M00.
8. A00 returns the exact M00 policy/capture/observation/relation/assessment/readback objects in a
   typed A00 orchestration result. It does not recreate Raw Signal semantic records.
9. A00 contains no Raw Signal outcome selection. In particular it does not choose
   `zero_received`, `one_or_more_received`, `unknown_not_established`, relation eligibility or
   supersession meaning.

## Validation against exact Stage 2 implementation commit

### Accepted U06 delegation/dataflow family

Command:

`pytest -q tests/product/raw_signal/test_u06_a00_composition.py`

Result: **7 passed**.

The two sequence cases that were deliberately red at Stage 1 are now green. The accepted spy proof
checks method order, exact material arguments, exact returned-object identity and pre-capture
policy-reference mismatch failure.

### Accepted U01-U04 predecessor regression

Result: **416 passed** across the four accepted U01-U04 product families.

### U05 fresh-owner/restart predecessor slice

Result: **27 passed** across:

- `test_u05_stage2_restart_foundation.py`;
- `test_u05_stage3_observation_restart.py`;
- `test_u05_stage4_assessment_restart.py`;
- `test_u05_stage5_whole_restart.py`.

### Architecture/bootstrap and static checks

- architecture/bootstrap: **74 passed**;
- mypy over `src`: **Success: no issues found in 16 source files**;
- Ruff over `src tests tools`: **All checks passed**;
- `git diff --check`: **PASS**.

## Deliberately UNPROVED at Stage 2

Stage 2 does not establish that the production-default A00 factory composes the real
PostgreSQL-backed M00 path end-to-end. Its sequence proof uses the already-accepted opaque spy
owner/factory solely to discriminate typed delegation and identity/dataflow.

Accordingly Stage 2 does not yet claim:

- real PostgreSQL-backed A00 sequential execution;
- durable public readback through a newly constructed production application;
- production composition independence from unadmitted network/provider/downstream capabilities;
- whole-U06 candidate closure, independent Tester acceptance or promotion.

Those are Stage 3 and later obligations.

## Stage 2 exit

Stage 2 is cleanly committed at
`af3bc77349ccaff943f3eabbcce2e25612a42e3b` / tree
`d1adad06919c6b31f054dab8ba4d81b144f2cf99`.

Stage 3 has not begun at this evidence boundary.
