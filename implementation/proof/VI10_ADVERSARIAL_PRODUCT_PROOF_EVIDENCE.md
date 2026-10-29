# VI-10 Adversarial Physical Product-Proof Evidence

## Status

**WORKER 003 CANDIDATE EVIDENCE — physical proof authored before implementation; product-proof PASS is not claimed.**

VI-10 admits six physical Raw Signal Occurrence Truth product-proof families derived from the exact accepted BICP/IRB/IWO authority. The suite is intentionally expected-red because production behaviour has not yet been implemented and the real PostgreSQL proof DSN is not configured in this Worker execution.

## Worker baseline and authority

Worker branch source:

- branch: `work/vi10-product-proof-author`
- PM design/handoff commit: `a2a3578aee21f2b3ab5412e2244284ba59c895f6`
- PM design/handoff tree: `061534297b1879477200e8215b1ce04b6e31de21`

Task/proof authority:

- BICP: `BICP-CANDIDATE-005`
- BICP JSON SHA-256: `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`
- accepted IRB SHA-256: `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`
- METHOD-006 baseline: `7c76b1dc87a9773e92841cae47e34b3b50190614`
- accepted IWO: `VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001`
- implementation target: active `M00`, package `nvda_desk.raw_signal_occurrence_truth`
- product obligations: exactly 13 current obligations, including repaired `IA22R01-PROD-009`
- predecessor `IA17-PROD-009`: lineage only, not admitted
- product tier treatment: `NOT_CLASSIFIED`
- architecture proof axis: separate `architecture_kernel`

Before authoring, the Worker inherited the PM's completed full authority/method read, then reread current `GUARDRAILS.md`, root `AGENTS.md`, accepted `EXEC_PLAN.md`, applicable current normatives, `tests/AGENTS.override.md`, BICP/IRB/IWO and the VI-10 PM design.

## Physical families admitted

| Family | Physical path | Current product obligations |
|---|---|---|
| `rsot_u01_contract_owner` | `tests/product/raw_signal/test_u01_contract_owner_boundary.py` | `IA17-PROD-001`, `IA17-PROD-011`, `IA17-PROD-012` |
| `rsot_u02_capture_schedule` | `tests/product/raw_signal/test_u02_capture_schedule.py` | `IA17-PROD-002`, `IA17-PROD-008` |
| `rsot_u03_observation_native_temporal` | `tests/product/raw_signal/test_u03_observation_native_temporal.py` | `IA17-PROD-003`, `IA17-PROD-004`, `IA17-PROD-005`, `IA17-PROD-008` |
| `rsot_u04_receipt_assessment` | `tests/product/raw_signal/test_u04_receipt_assessment.py` | `IA17-PROD-006`, `IA17-PROD-007`, `IA17-PROD-008` |
| `rsot_u05_postgresql_durability` | `tests/product/raw_signal/test_u05_postgresql_durability.py` | `IA22R01-PROD-009`, `IA17-PROD-010`, `IA17-PROD-007`, `IA17-PROD-008` |
| `rsot_u06_a00_composition` | `tests/product/raw_signal/test_u06_a00_composition.py` | `IA17-PROD-011`, `IA17-PROD-013` |

The product-proof aggregate is now `READY_FOR_PROOF` because those six physical families cover exactly all 13 current product obligations. `READY_FOR_PROOF` is a control-state label, not a semantic PASS.

## Adversarial proof surface

The authored suite contains 58 collected tests. It includes, where applicable:

- lawful positive cases;
- prohibited/false-positive cases;
- missing-mandatory-authority cases;
- lawful optional-absence cases;
- identity/retry conflicts and retransmission distinctions;
- exact `:00`/`:30` and half-open schedule boundaries;
- second-identity challenge against the stable `(policy, slot)` key;
- native-record preservation and no repository-created field splitting;
- `true_instant`, `date_only` and `receipt_only` preservation plus contradictory temporal discriminants;
- no-scope observation and no-relation states;
- ineligible and out-of-slot relation cases;
- all three assessment outcomes, append-only supersession, same-ID conflict, self/broken/non-immediate predecessor rejection;
- real-PostgreSQL version/DSN boundary, fresh-owner durable readback, append-only durable assessment history, failed-write non-fabrication and restart missing-slot `unknown_not_established` proof;
- A00 -> M00 public-seam/composition boundary checks without P01/K01/downstream expansion.

The suite contains no skip for missing implementation, missing DSN or missing required dependency. Missing mandatory proof boundaries fail explicitly.

## Structural control validation

Command:

```text
python tools/validate_product_proof.py
```

Observed:

```text
PASS: product-proof control configuration is structurally and semantically bound
BICP: BICP-CANDIDATE-005 sha256=5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed
implementation target: M00
required product obligations: 13
admitted physical product families: 6
covered product obligations: 13/13
aggregate: raw_signal_occurrence_truth_product state=READY_FOR_PROOF
separate architecture proof axis: architecture_kernel
```

Collection:

```text
python -m pytest --collect-only -q tests/product/raw_signal
58 tests collected
```

## Expected-red pre-implementation execution

Per-family execution from the authored Worker tree:

```text
test_u01_contract_owner_boundary.py        rc=1  6 failed, 1 passed
test_u02_capture_schedule.py               rc=1  11 failed
test_u03_observation_native_temporal.py    rc=1  16 failed
test_u04_receipt_assessment.py             rc=1  13 failed
test_u05_postgresql_durability.py          rc=1  7 failed
test_u06_a00_composition.py                rc=1  2 failed, 2 passed
```

Failures are attributable to the intended pre-implementation boundary:

- M00 v1 public contract symbols are not yet implemented;
- `_build_test_owner` is not yet implemented;
- A00 `_build_test_application` is not yet implemented;
- mandatory `NVDA_TEST_POSTGRES_DSN` is not configured for the real PostgreSQL 17.9 proof boundary.

Psycopg 3.3.4 was installed from the preserved project attachment for this Worker validation. The suite did not substitute an in-memory/mock database for the absent real PostgreSQL DSN.

## Clean candidate aggregate execution

Candidate Git identity:

- commit: `33e16c3e877b1cb696bbb17be37f795f7ee83dd8`
- tree: `63c48de78c2061c77c0345a57c584f407feb66f5`
- pre-check worktree: clean

From that exact clean candidate:

```text
python tools/validate_product_proof.py
rc 0 — six admitted families; 13/13 coverage; READY_FOR_PROOF

python tools/run_product_proof_gate.py --aggregate raw_signal_occurrence_truth_product
rc 1 — resolved exactly the six admitted family paths; 58 tests executed; 55 failed, 3 passed

python tools/run_promotion_gate.py --set architecture_kernel
rc 0 — 11 admitted architecture/bootstrap paths; 74 passed

python -m mypy src
rc 0 — Success: no issues found in 15 source files

ruff check src tests tools
rc 0 — All checks passed

git diff --check
rc 0

git status --porcelain=v1
clean
```

The non-zero product aggregate is the required VI-10 pre-implementation disposition. It is not a VI-10 failure because the aggregate is physically complete and its red state is attributable to absent implementation / mandatory proof environment rather than malformed control or collection.

## Authoring corrections encountered

Two bounded execution issues were encountered and corrected without changing product meaning:

1. the previously created virtual-environment path was absent in the volatile runtime; the Python 3.13.5 proof environment was rebuilt from the preserved offline dependency artefacts;
2. the first Ruff pass found formatting/import-order issues and one intentionally broad failed-write exception assertion. Only test-code formatting/imports were repaired; the broad exception catch was retained with a documented Ruff suppression because the exact technical exception type is not normative product authority.

A separate verification command initially referenced non-existent file names for dependency/public-seam checks. The correct repository-installed CLI entry points were then used; both passed.

## Change boundary

VI-10 changes only:

- `config/product_proof/families.yaml`
- `config/product_proof/aggregates.yaml`
- `tests/product/raw_signal/_support.py`
- six `tests/product/raw_signal/test_u0*.py` physical family files
- this evidence record

No `src/**` production behaviour and no `config/proof/**` architecture-proof configuration was changed.

## Claim boundary

This evidence establishes only that VI-10 physical product proof has been authored, admitted, collected and shown expected-red before implementation while the existing architecture proof axis remains green.

It does **not** establish product-proof PASS, implementation correctness, VI-11 proof-adequacy acceptance, VI-12R implementation start, production fitness or semantic acceptance.
