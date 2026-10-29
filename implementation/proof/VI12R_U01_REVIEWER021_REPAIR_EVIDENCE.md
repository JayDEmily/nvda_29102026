# VI-12R U01 Reviewer 021 bounded repair evidence

## Status

Worker repair candidate frozen for fresh independent VI-13R re-review. U02 remains prohibited.

- Reviewer 021 disposition: `FAIL / RETURN_TO_WORKER` at
  `1637f39980aa3ca476429d85e267a9cb0e575fe5`.
- repaired U01 candidate: `e8b659d7849d2f95b64ba32bed8090a8290358d4` / tree `62b074c0e94215a75fb64c5eb934af55be1ded3a`.
- predecessor production candidate: `d14190cdfe845fdd60629ca9b1eed8d1d2704d44`.
- repair diff SHA-256 from Reviewer 021 disposition commit: `542b3e3a907193774154f2a73bab1a3ebb9af488221e0393e77e6780369b8f6e`.
- repaired paths: `src/nvda_desk/raw_signal_occurrence_truth/api.py`,
  `tests/product/raw_signal/test_u01_contract_owner_boundary.py`, and
  `tests/product/raw_signal/typecheck/public_seam_positive.py` only.

## Bounded repairs

### W-U01-F001 — coherent receipt-only proof construction

The generic finite-discriminant constructor now clears `source_timestamp_raw` when constructing
its lawful `receipt_only` positive specimen. The production law is unchanged: receipt-only with
a provider timestamp remains rejected.

### W-U01-F002 — mypy diagnostic-path normalisation

The negative static-proof parser now resolves relative mypy paths against repository root before
comparing them with the target specimen. The proof still requires all 15 `STATIC_NEGATIVE` sites
to be diagnosed.

### R021-U01-F003 — alias-safe read-only native record

`RawObservationOccurrenceV1.native_record` is now typed as `Mapping[str, object]` and is replaced
at construction by a private alias-safe read-only snapshot. The snapshot deep-copies caller input
and returns copies of stored values, so mutation of the caller container, nested caller values,
values obtained through the payload, or direct mapping assignment cannot alter the constructed
occurrence. Provider-logical names, values and native null values remain represented unchanged.

The focused U01 proof now exercises top-level alias mutation, nested alias mutation, mutation of a
value returned through the payload, and direct mapping assignment.

### R021-U01-F004 — lawful public identity construction

The public seam now exports typed factory functions for each required non-catalogue U01 identity
layer: concept, contract, scope-policy ID/ref, eligibility-policy ref, capture occurrence,
observation occurrence, assessment occurrence, provider, delivery artefact and ingestion-sequence
scope. These factories return the existing runtime-distinct identity types; no universal identity
was introduced.

The positive static specimen now constructs all five U01 payload contracts using only declared
public API symbols before exercising the command/read seam. No underscore/private identity access
or annotation introspection is required by that specimen.

## Worker validation on exact committed candidate

Environment actually available:

- Python: `3.13.5` — exact repository pin;
- mypy: `1.20.1` — exact repository pin, restored offline from the preserved AKR5 wheelhouse;
- pytest: `9.0.2` — environment version differs from repository dev pin `9.0.3`;
- Ruff `0.15.11`: not available in this fresh Worker sandbox, therefore Worker-Ruff execution is
  `UNPROVED` and must be rerun by the fresh reviewer where available.

Observed commands/results on `e8b659d7849d2f95b64ba32bed8090a8290358d4`:

- `python -m pytest -q tests/product/raw_signal/test_u01_contract_owner_boundary.py` ->
  **297 passed**;
- positive public-seam mypy specimen with strict/disallow-any -> return code 0;
- negative public-seam mypy specimen -> return code 1 with exactly **15** intended diagnostics;
- `python -m mypy src --show-error-codes` -> success, no issues in 15 source files;
- `python tools/validate_product_proof.py` -> PASS, 13/13 product obligations structurally bound;
- `python tools/validate_architecture.py` -> PASS;
- `python tools/check_dependencies.py` -> PASS;
- `python tools/check_public_seams.py` -> PASS;
- `python tools/run_promotion_gate.py --set architecture_kernel` -> **74 passed**;
- `git diff --check` -> pass;
- `git fsck --full --strict` -> pass.

The promotion-gate run was made on the clean committed repair candidate. PostgreSQL, namespace and
U05 real-boundary execution were not run because they are outside U01 and are not required by this
repair leaf.

## Claim boundary

This evidence is a Worker claim only. It does not accept or promote U01. Fresh independent VI-13R
re-review must inspect the concrete repaired implementation/proof and disposition all four
Reviewer-021 findings. U02 remains prohibited until that review returns PASS and U01 is lawfully
promoted.
