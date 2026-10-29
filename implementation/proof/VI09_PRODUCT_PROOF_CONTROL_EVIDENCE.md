# VI-09 Product-Proof Admission/Control Evidence

## Status

**WORKER 002 CANDIDATE EVIDENCE — product-proof control only; no product-proof PASS claimed.**

VI-09 establishes a separate N15/N19 product-proof control surface for the admitted Raw Signal Occurrence Truth implementation target. It intentionally admits zero physical product test families. The product aggregate is therefore required to remain incomplete and non-successful until VI-10 authors and admits adequate physical proof.

## Source authority and Worker baseline

Worker branch source:

- branch: `work/vi09-product-proof-control`
- PM handoff commit: `c5430957b4316a4d8ab5b903f79008f860bd3dfb`
- PM handoff tree: `4bf31f154be32b6eee400c121ab5b93c8a08752a`

Task/proof authority:

- BICP: `BICP-CANDIDATE-005`
- BICP JSON SHA-256: `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`
- accepted IRB SHA-256: `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`
- implementation target: active `M00`, package `nvda_desk.raw_signal_occurrence_truth`, public seam `nvda_desk.raw_signal_occurrence_truth.api`
- separate architecture proof axis: `architecture_kernel`
- exact current product-proof obligations: thirteen, using `IA22R01-PROD-009`; predecessor `IA17-PROD-009` remains forbidden lineage only
- product tier treatment: `NOT_CLASSIFIED`

The Worker reread current repository governance, the accepted ExecPlan, applicable current architecture normatives, the exact six METHOD-006 routed normatives at commit `7c76b1dc87a9773e92841cae47e34b3b50190614`, `tests/AGENTS.override.md`, current architecture/bootstrap proof mechanics, and the preserved Tier A/B/C testing-method evidence before implementing this surface.

## Changed surface

VI-09 changes only:

- `config/product_proof/authority.yaml`
- `config/product_proof/families.yaml`
- `config/product_proof/aggregates.yaml`
- `schemas/product_proof_authority.schema.json`
- `schemas/product_proof_family.schema.json`
- `schemas/product_proof_aggregate.schema.json`
- `tools/validate_product_proof.py`
- `tools/run_product_proof_gate.py`
- `implementation/proof/VI09_PRODUCT_PROOF_CONTROL_EVIDENCE.md`

No `tests/product/**` file and no production-source file is created or changed by VI-09.

## Valid control-state validation

Command:

```text
/mnt/data/nvda_recovery_venv/bin/python tools/validate_product_proof.py
```

Observed:

```text
PASS: product-proof control configuration is structurally and semantically bound
BICP: BICP-CANDIDATE-005 sha256=5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed
implementation target: M00
required product obligations: 13
admitted physical product families: 0
covered product obligations: 0/13
aggregate: raw_signal_occurrence_truth_product state=INCOMPLETE_NO_PHYSICAL_FAMILIES
separate architecture proof axis: architecture_kernel
```

This is control validation only. It is deliberately not product semantic proof.

## Adversarial control matrix

An external temporary probe harness copied the Worker tree into isolated temporary directories, corrupted one governed condition at a time, and invoked the repository validator against each isolated copy. The harness itself is not a repository artefact and did not mutate the Worker tree.

Harness sanity control: one synthetically admitted physical family covering only `IA17-PROD-001` was accepted as `INCOMPLETE_COVERAGE`, proving the harness could create a structurally valid non-empty control state.

Required adversarial dispositions:

| Probe | Expected disposition | Observed |
|---|---|---|
| wrong BICP hash | reject | rc 1 — `BICP hash mismatch` |
| missing current product obligation | reject | rc 1 — product obligation set/order mismatch |
| predecessor `IA17-PROD-009` substituted for `IA22R01-PROD-009` | reject | rc 1 — product obligation set/order mismatch |
| architecture obligation inserted into product family | reject | rc 1 — schema rejects non-product obligation ID |
| Tier A/B/C classification introduced | reject | rc 1 — schema requires `NOT_CLASSIFIED` |
| unadmitted physical product test path | reject | rc 1 — product-test admission mismatch |
| required N15 case dimension omitted | reject | rc 1 — schema reports missing `lawful_optional_absence` |
| proposition outside routed/current authority | reject | rc 1 — unbound proposition rejected |
| duplicate family identity/path admission | reject | rc 1 — duplicate family ID rejected |
| aggregate marked ready with incomplete coverage | reject | rc 1 — aggregate state mismatch |
| empty physical-family aggregate reported as proof success | reject | rc 4 — explicitly `not a product-proof PASS` |

Summary: **12/12 probe dispositions satisfied**, comprising one valid harness sanity control plus all eleven required adversarial checks.

For the empty-family runner probe, the exact current control files were copied into a clean temporary Git repository before execution so the runner's clean-worktree invariant was also exercised. The runner returned code `4` and reported:

```text
FAIL: product-proof aggregate is not ready; state=INCOMPLETE_NO_PHYSICAL_FAMILIES (this is not a product-proof PASS)
```

## Repository regression checks before candidate commit

After a first verification attempt identified eight Ruff `E501` formatting violations in the new validator, execution stopped at that first failed invariant. Only line wrapping within the authorised validator path was repaired. The complete required sequence was then rerun from the start.

Observed rerun:

```text
python tools/validate_product_proof.py
PASS — exact 13-obligation control; 0 admitted families; incomplete aggregate

python tools/validate_architecture.py
PASS — 5 architecture objects; 1 active runtime module; 1 allocation; 11 admitted architecture test families; 0 dependency/public-seam violations

python -m pytest tests/architecture tests/bootstrap -q
74 passed

python -m mypy src
Success: no issues found in 15 source files

ruff check src tests tools
All checks passed

git diff --check
PASS (no output)
```

Physical-product-test inspection returned no `tests/product/**/test_*.py` path. `git diff -- src` returned no production-source change.

## Clean committed-state checks

Candidate Git identity:

- commit: `6d7eede672ede38ea0a9afe5acee4157b8b9bf72`
- tree: `879c609a995ffdba14db761577dbdf0c4000e29f`
- pre-check worktree: clean

Commands/results from that exact clean committed state:

```text
python tools/validate_product_proof.py
PASS — exact authority/control binding; 13 required obligations; 0 physical families; aggregate INCOMPLETE_NO_PHYSICAL_FAMILIES

python tools/run_product_proof_gate.py --aggregate raw_signal_occurrence_truth_product
rc 4 — FAIL: product-proof aggregate is not ready; state=INCOMPLETE_NO_PHYSICAL_FAMILIES (this is not a product-proof PASS)

python tools/run_promotion_gate.py --set architecture_kernel
PASS — resolved all 11 admitted architecture/bootstrap paths; 74 passed

python -m pytest tests/architecture tests/bootstrap -q
74 passed

python -m mypy src
Success: no issues found in 15 source files

ruff check src tests tools
All checks passed

git diff --check
PASS (no output)

git status --porcelain=v1
clean before and after execution
```

The product runner's non-zero result is the required VI-09 outcome: the control state is valid, while product proof remains unavailable until physical families are authored and admitted. The separate architecture aggregate remains green and unchanged in membership.

## Claim boundary

This evidence establishes only the VI-09 product-proof **control** proposition. It does not establish Raw Signal product behaviour, physical product proof, product-proof PASS, VI-10 completion or production implementation.
