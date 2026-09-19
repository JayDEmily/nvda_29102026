# Worker 002 — VI-09 Product-Proof Admission/Control

## Assignment

Execute **VI-09 only** from PM source commit `8c4d7374f479c249bb1de5d202a5a8d5fbd2a94b` / tree `eab8e12d60ea46e70afb8db51581433d63eeb6a5`.

Read and obey, in order:

1. current `GUARDRAILS.md`;
2. root `AGENTS.md`;
3. accepted root `EXEC_PLAN.md`;
4. exact routed current architecture/product normatives required by VI-09;
5. `tests/AGENTS.override.md` before relying on or touching test surfaces;
6. complete current admitted architecture/bootstrap proof corpus plus the preserved Tier A/B/C method evidence identified by the PM design;
7. `implementation/proof/VI09_PRODUCT_PROOF_CONTROL_DESIGN.md`.

The PM design is bounded implementation instruction. It cannot override higher authority.

## Exact objective

Create the minimum separate N15/N19 product-proof control surface described in `implementation/proof/VI09_PRODUCT_PROOF_CONTROL_DESIGN.md`.

The truthful end state has **zero physical product test families** and therefore **no successful product aggregate**. VI-09 creates the authority/registry/schema/runner controls needed for VI-10 to admit those families later.

## Authorised changed paths

Only these paths are authorised for Worker 002 unless a required invariant proves a bounded additional path is necessary; in that case stop and return the first unmet invariant rather than broadening scope:

- `config/product_proof/authority.yaml`
- `config/product_proof/families.yaml`
- `config/product_proof/aggregates.yaml`
- `schemas/product_proof_authority.schema.json`
- `schemas/product_proof_family.schema.json`
- `schemas/product_proof_aggregate.schema.json`
- `tools/validate_product_proof.py`
- `tools/run_product_proof_gate.py`
- `implementation/proof/VI09_PRODUCT_PROOF_CONTROL_EVIDENCE.md`

No `tests/product/**` path is authorised in VI-09.

## Hard boundaries

- BICP JSON must remain exact SHA-256 `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`.
- IRB must remain exact SHA-256 `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`.
- Product obligation set is exactly thirteen and uses `IA22R01-PROD-009`; `IA17-PROD-009` is forbidden predecessor lineage.
- Product `tier_treatment` remains `NOT_CLASSIFIED`; do not map product proof onto Tier A/B/C.
- Architecture axis remains the separate existing `architecture_kernel` control/proof surface and must not be mutated.
- No physical product test and no production code.

## Required validation

At minimum:

- valid product-proof control validation;
- all eleven adversarial checks in the PM design;
- product aggregate runner proves the empty/incomplete state cannot return success;
- existing `architecture_kernel` aggregate from clean committed state;
- current architecture/bootstrap tests;
- mypy and Ruff;
- `git diff --check` and final changed-path/diff inspection.

Stop at the first failed required invariant. Do not weaken a schema, validator or acceptance criterion merely to obtain green.

## Return

Return exact final Worker commit/tree, changed paths, validation commands/results, limitations, and the statement that no physical product test or product implementation was created. Do not claim VI-10 or product-proof PASS.
