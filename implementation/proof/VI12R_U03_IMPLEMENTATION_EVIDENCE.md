# VI-12R U03 implementation evidence

## Status

**WORKER CANDIDATE — NOT INDEPENDENTLY ACCEPTED.**

## Promotion and exact lineage

- Reviewer-024 accepted repaired U02 candidate: `5c62ec5147da718297b251b5a287405ebf3b4755`.
- Reviewer-024 PASS commit: `df45c5e93e7c4c19cb1cca75de5cd1c64b15537c`.
- Returned tester/handoff history was fast-forwarded to forward `main` at
  `a78ae7b5515c2e482a2656cebeebae3fa5a6d584` with preserved ancestry.
- Both the accepted U02 candidate and Reviewer-024 PASS are ancestors of that `main`.
- U03 branch: `work/vi12r-u03-observation-fidelity`.
- U03 production candidate: `7cf8936f854fbed952a468ce06c2f2a0320d9291`.
- U03 production tree: `b63aac7fb538ea6a38ce3dea5aab719fc7be0ee0`.
- U03 production parent: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`.
- Production candidate changes exactly one path:
  `src/nvda_desk/raw_signal_occurrence_truth/api.py`.
- Candidate binary diff SHA-256:
  `91f20c62a03884aae9a666c105a91a4477ad66257e1ad00ffc50cba9046fb8ff`.

## Implemented proposition

IWO-U03 only: raw-observation admission, native fidelity and temporal-kind truth.

The candidate implements:

- one admitted `RawObservationOccurrenceV1` per caller-supplied provider logical record;
- no equal-value, native-ID or delivery-reference deduplication across distinct observation IDs;
- same observation occurrence ID is idempotent only for identical payload content;
- exact referential readback by observation occurrence identity;
- local ingestion-sequence non-decrease enforced independently per typed ingestion scope;
- retry of an already admitted identical occurrence remains lawful even after later sequence values;
- preservation of the existing U01 native-record alias-safe snapshot, provider nulls, exact numeric
  runtime types and optional provider/native metadata;
- exact `true_instant|date_only|receipt_only` contract law already fixed by U01 payload validation;
- no provider timestamp/timezone synthesis from receipt time and no raw `event_ts_utc` derivation;
- no capture/relation/assessment semantics, persistence, provider mapping, replay or downstream
  behaviour added.

U04-U05 command/read behaviour remains deliberately `NotImplementedError`.

## Exact validation environment

```text
Python 3.13.5
pytest 9.0.3
mypy 1.20.1 (compiled)
Ruff 0.15.11
```

The pinned pytest/Ruff/mypy wheels were restored from preserved project artefacts outside the
repository. No toolchain files were committed to the candidate.

## Validation on exact committed candidate

With `HEAD=7cf8936f854fbed952a468ce06c2f2a0320d9291` and a clean worktree:

- focused U01+U02+U03 product proof: **366 passed**;
- `mypy src`: **success, 15 source files**;
- Ruff `src`: **pass**;
- product-proof control: **PASS**, six families, 13/13 obligations;
- public-seam validation: **PASS**;
- structural architecture validation: **PASS**, zero dependency/public-seam violations;
- architecture/bootstrap tests: **74 passed**;
- `architecture_kernel` promotion set: **74 passed**;
- `git diff --check`: pass;
- `git fsck --full --strict`: pass;
- committed worktree: clean.

An earlier architecture/bootstrap invocation without `PYTHONPATH=src` produced one environment-level
`ModuleNotFoundError` inside a subprocess. The repository-native invocation with `PYTHONPATH=src`
then passed 74/74; no repository mutation was made to address that environment error.

## Scope and next gate

This Worker evidence does not accept U03. Fresh VI-13R Reviewer 025 must review the realised U03
candidate against IRB BC-005/BC-006/BC-009/BC-010, IWO-U03 and the bounded U03 proof. U04 remains
prohibited until U03 is independently accepted and lawfully promoted to forward `main`.
