# AKR-4 — Implementation-authority ingress investigation and disposition

## Scope

Branch start: `38ea93e482717180959afea9aa6b19659025368b` (`work/akr-3-architecture-authority-reconciliation`).

AKR-4 was executed under direct user instruction to investigate before creating anything: establish whether the clean kernel already contained a generic implementation-ready-brief -> implementation-authority boundary, then retain/adapt/create only what primary evidence showed was missing.

No real product brief or NVIDIA domain capability is admitted by this leaf.

## Current-kernel finding

At the AKR-3 branch start, the current architecture laws referred to "accepted implementation authority" in `ARCHITECTURE_KERNEL.md`, `OWNERSHIP_AND_COMPONENT_LAW.md`, `PUBLIC_SEAM_LAW.md` and `EXTENSION_AND_RETIREMENT_RULES.md`.

However, the active tree contained no:

- implementation-authority binding schema;
- brief-byte hash validator;
- accepted-brief binding record type;
- generic create/modify target projection record;
- implementation-authority ingress CLI/tool.

The current module/protocol/kernel/surface schemas described architecture objects but contained no object representing an accepted implementation-ready brief.

Disposition: the conceptual boundary existed partially in normative wording; the concrete generic ingress mechanism did not.

## Historical admission machinery inspected

The immediately pre-AKR-2 state at `985c9cec866e6690e6268aafa181cc7840602b60` retained the Raw Signal programme governance system, including:

- `schemas/work_order.schema.json`;
- `schemas/attempt_record.schema.json`;
- `schemas/review.schema.json`;
- `schemas/admission_record.schema.json`;
- `schemas/semantic_index.schema.json`;
- `tools/validate_governance.py`.

That machinery contained useful mechanical invariants:

- SHA-256 authority references;
- exact accepted Git-base binding;
- bounded mutation scope;
- mechanically derived candidate Git facts;
- candidate/admission identity consistency.

It was not reused wholesale because its schema and validator are coupled to the superseded Raw Signal construction programme: gates/stages, commissioned agent roles, semantic index, semantic worker/reviewer roles, runtime-identity receipts and semantic-result admission.

The generic invariant carried forward is exact byte identity plus bounded architectural scope. The programme-specific workflow remains historical Git evidence.

## AKR-4 design

The new steady-state owner is `docs/architecture/IMPLEMENTATION_AUTHORITY_INGRESS.md`.

The boundary is intentionally small:

1. raw brief bytes are supplied externally and hashed exactly with SHA-256;
2. a binding record contains that digest;
3. the binding records a non-empty locator/reference to explicit current human/programme acceptance for implementation;
4. the binding records only proposed architecture-object `create` / `modify` targets;
5. the current architecture registry is used to reject impossible target state (`create` existing/reused retired ID; `modify` unknown ID);
6. the binding schema has no brief-text, M10, G1-G7, PMB, semantic-candidate or worker/tester fields.

The binding is not a semantic oracle. Its acceptance field does not prove that a human actually accepted the brief. That legitimacy remains a higher-authority fact the worker must establish before use.

The kernel does not copy or normalise brief text. SHA-256 is computed over the exact supplied bytes.

## Files introduced or changed

Introduced:

- `docs/architecture/IMPLEMENTATION_AUTHORITY_INGRESS.md`;
- `schemas/implementation_authority_binding.schema.json`;
- `src/nvda_desk/architecture/implementation_authority.py`;
- `templates/implementation_authority/binding.yaml.template`;
- `tests/architecture/test_implementation_authority_ingress.py`;
- `tools/validate_implementation_authority.py`.

Updated:

- root architecture authority routing;
- brief-derived runtime-module admission routing;
- architecture proof family/block/promotion configuration;
- repository CLI/Makefile entry points;
- README orientation;
- proof-control expected admitted-family population.

## Mechanical proof obtained before commit

Environment: CPython `3.13.5` through the repository's offline `uv` configuration.

Observed:

- ingress-specific tests: `6 passed`;
- architecture/bootstrap suite after proof-family admission: `44 passed`;
- architecture validator: 5 architecture objects, 0 active runtime modules, 9 admitted test families, 1 promotion set, 0 dependency/public-seam violations;
- Ruff: PASS;
- `git diff --check`: PASS;
- repository console ingress command accepted a synthetic exact brief/binding with targets `create:M100` and `modify:P01`;
- the Makefile ingress entry point accepted the same synthetic binding;
- changing the synthetic brief bytes under the same binding returned exit code 2 with `FAIL: implementation brief bytes do not match the bound SHA-256`.

The first full architecture/bootstrap run after adding the ninth proof family failed because `test_proof_control.py` correctly expected the previously admitted population of eight families. The expected admitted-state assertion was updated to nine after verifying that the new ingress family is intentionally Tier-A/current-blocking and reachable from the `architecture_kernel` promotion set. No proof law or test was weakened.

## Explicit limits

AKR-4 does not establish:

- legitimacy of any future human/programme acceptance merely from a binding file;
- semantic completeness of an arbitrary brief by mechanical inspection;
- a future AI/code-writing methodology;
- changed-path/work-order/reviewer machinery;
- behavioural-test generation;
- implementation or integration of any product capability;
- end-to-end brief -> registry -> proof -> code rehearsal (AKR-6);
- dormant structural repairs such as first-active-module validation, recursive proof discovery, ImportFrom seam enforcement or static type checking (AKR-5).

If semantic meaning is missing or architecture law cannot be satisfied without inventing meaning, the normative disposition is to stop and return the defect upstream.
