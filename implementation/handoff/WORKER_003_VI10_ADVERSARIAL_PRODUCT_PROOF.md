# Worker 003 — VI-10 Adversarial Physical Product Proof

## Assignment

Execute **VI-10 only** from the current PM source state.

Read and obey in order:

1. current `GUARDRAILS.md`;
2. root `AGENTS.md`;
3. accepted root `EXEC_PLAN.md`;
4. the exact routed current architecture/product normative authorities required by VI-10;
5. `tests/AGENTS.override.md`;
6. the complete current admitted architecture/bootstrap proof corpus and the preserved Tier A/B/C testing-method evidence;
7. exact BICP, IRB and accepted IWO;
8. `implementation/proof/VI10_ADVERSARIAL_PRODUCT_PROOF_DESIGN.md`.

The PM design is bounded implementation instruction and cannot override higher authority.

## Objective

Author and admit the six VI-10 physical product-proof families before any product implementation exists. The physical proof must cover exactly all 13 current product obligations and must remain separate from architecture proof.

## Authorised paths

- `tests/product/raw_signal/**`
- `config/product_proof/families.yaml`
- `config/product_proof/aggregates.yaml`
- `implementation/proof/VI10_ADVERSARIAL_PRODUCT_PROOF_EVIDENCE.md`

No production source path is authorised. No `config/proof/**` architecture-proof path is authorised.

## Hard boundaries

- no production code;
- no test skip for missing implementation, DSN, driver or real PostgreSQL proof boundary;
- no predecessor `IA17-PROD-009`;
- product tier treatment remains `NOT_CLASSIFIED`;
- real PostgreSQL durability/restart proof may not be replaced by an in-memory/mock/same-process substitute;
- tests may use proof-only input fixtures, controlled opaque-ID sources and eligibility decisions, but those fixtures cannot invent product semantics;
- the private test construction symbols fixed by the PM design may construct/wire only; they are not semantic-authority escape hatches.

## Required validation

1. `python tools/validate_product_proof.py` passes with six admitted families and 13/13 coverage.
2. Each physical test file collects successfully; missing product implementation appears as explicit test failure, not collection corruption or skip.
3. Product aggregate resolves exactly the six family paths and returns non-zero pre-implementation; record exact failures as expected-red evidence.
4. Existing architecture validation and `architecture_kernel` aggregate remain green.
5. mypy/Ruff and `git diff --check` remain green for the repository/test changes.
6. Final diff confirms no production source behavior and no architecture proof mutation.

## Return

Return final Worker commit/tree, exact changed paths, proof-control validation, per-family collection/execution result, expected-red aggregate result, architecture regression results, limitations, and explicit confirmation that no product implementation was written.

Do not claim product-proof PASS or VI-11 acceptance.
