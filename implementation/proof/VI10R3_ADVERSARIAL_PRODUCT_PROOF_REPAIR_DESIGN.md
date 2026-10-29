# VI-10R3 — Adversarial Product Proof Repair Design

## Status

`AUTHORISED SUCCESSOR PROOF REPAIR — PRE-IMPLEMENTATION`

This successor repairs all eleven findings returned by VI-11R2 Tester Iteration 005. The failed VI-10R2 physical candidate and review wrapper remain preserved in Git history.

## Bound predecessor and unchanged authority

- failed VI-10R2 physical proof: `56ea445d4bb5055b9fc39114bcd3c529b7f0bae5` / tree `b925e086a734492457dd9633a04743aa0c3c0471`
- reviewed wrapper: `c164facaf011f2dc2da7ebcb2d90790b755c8782` / tree `e2062af6d64e29eaaf27340c929ee0d6b70f9d35`
- Tester Iteration 005 archive SHA-256: `e4dd373e1a4a54039a3dbee58f5777844a731df80ba6e57dee856e30b91c84c6`
- Tester Iteration 005 response SHA-256: `c6d675d86660c1f082b022676f9a13dc2bb9b811ad05ba6fdfa324c25b988cbf`
- exact accepted IRB/BICP/IWO and routed METHOD-006 normatives remain unchanged.

## Repair law

Each reviewer-described wrong implementation must fail physically. Registry prose may not substitute for a discriminator.

### R1 — PostgreSQL is the semantic durable source (`T005-F001`)

U05 must create high-entropy authoritative facts whose content is independent of their query identities. Writer and reader processes receive separate ephemeral local filesystems and stripped process environments; the reader receives only the PostgreSQL DSN plus domain query identity. Complete canonical semantic facts must be recovered by the fresh reader and equal the parent-held pre-write expectation. A proof control must show the reader cannot reconstruct those high-entropy facts from identity/token conventions alone. No alternate durable path may be configured or reachable through proof inputs.

### R2 — commit is true when the command reports success (`T005-F002`)

U05 adds a hold-open writer protocol. The writer executes one public semantic command, emits its successful result while remaining alive, then blocks. A distinct reader process must observe the fact before the parent permits writer shutdown. Multi-fact paths must expose an explicit barrier between relation persistence and assessment persistence so the relation is independently visible before the assessment command executes; reconciliation must likewise expose capture visibility before the unknown assessment is appended.

### R3 — independent pre-write durable oracle (`T005-F003`)

The parent constructs and canonicalises authoritative policy/capture/observation/assessment expectations before writer execution. Fresh-process readback is compared to those pre-write expectations, never to writer-returned representations. Material lineage, schedule, provenance, temporal and optional fields are included.

### R4 — strict v1 compatibility and UTC (`T005-F004`)

U01 treats the accepted five-contract field set as closed for `.v1`: any unrecognised field is incompatible absent separate accepted semantic authority. Every `_utc` field is parameterised with aware non-UTC offsets and must reject them; UTC means zero offset, not merely timezone-aware.

### R5 — per-scope monotonic state survives interleaving (`T005-F005`)

U03 exercises `A:10, B:1, A:9` (reject) followed by `A:11` (accept), proving independent high-water state is retained per typed ingestion scope.

### R6 — semantic-free default persistence boundary (`T005-F006`)

U04/U05 inspect the complete production owner package AST, not filename-selected candidates. Semantic-decision literals/helpers may exist only in owner/domain modules, never in the technical persistence implementation. The actual default PostgreSQL construction path is instrumented through a technical persistence protocol whose calls accept already-decided semantic records and expose no eligibility/outcome decision capability; the injected proof port and default port must satisfy the same protocol shape.

### R7 — A00 uses registered policy result (`T005-F007`)

U06 gives the register-policy sentinel a distinct typed effective policy reference. Capture realisation must consume that exact returned reference. A deliberately mismatched caller-supplied reference is included so using the caller value instead of the registration result fails.

### R8 — policy temporal validity and version boundary (`T005-F008`)

U02 rejects unaligned activation/deactivation timestamps and deactivation at/before activation. It proves v1 owns the last slot before v2 activation, v2 owns the slot beginning exactly at its activation boundary, and neither version can claim the other's boundary slot.

### R9 — complete half-open relation and typed missing authority (`T005-F009`)

U04 adds a receipt immediately before slot start and requires no relation. Missing-capture proof uses a valid typed `capture_occurrence_id` that does not exist, so the failure exercises referential authority rather than type validation.

### R10 — assessment depends only on eligible committed receipt evidence (`T005-F010`)

U04 admits ineligible and out-of-slot observations, then appends assessments and requires `zero_received`. Only an eligible in-slot committed relation may produce `one_or_more_received`.

### R11 — exact reconciliation facts (`T005-F011`)

U05 fresh-process reconciliation returns the complete recovered capture and unknown assessment. The parent independently derives expected capture ID, exact effective policy ref, slot start/end and contract facts before execution, and compares the readback to that expectation. The assessment must reference that exact recovered capture.

## Mutation jurisdiction

Allowed:

- `config/product_proof/families.yaml` only to truthfully describe stronger physical proof;
- `tests/product/raw_signal/_support.py`;
- `tests/product/raw_signal/_process_probe.py`;
- the six `tests/product/raw_signal/test_u0*_*.py` families;
- VI-10R3 evidence/control/handoff records.

Prohibited:

- `src/nvda_desk/**` production behaviour;
- architecture registries/proof configuration;
- IRB/BICP/IWO/METHOD-006 meaning;
- obligation deletion, tier reclassification or aggregate weakening;
- hard-coded PostgreSQL physical schema/table names as product law.

## Acceptance before fresh re-review

The successor must retain six families and all thirteen obligations, collect without harness errors, remain pre-implementation red only for attributable missing production/PostgreSQL capability, keep architecture/static gates green, contain no production mutation, map every `T005-F001..F011` to a physical discriminator, and be frozen for fresh independent VI-11R3 review before VI-12R.
