# Unit 7 — M00 bounded Gate D implementation

**Date:** 2026-08-01
**Branch:** `work/m00-testing-guardrail-repair-v1`
**Authority:** `M00-FINAL-COMPOSITION-V1`, propositions `M00-COMP-001` through `M00-COMP-009`
**Outcome:** PASS — source, module-local and Tier B validation; clean installed aggregate remains Unit 8.

## Implemented surface

The canonical package `nvda_desk.m00_application_shell` now exports exactly:

- `ApplicationCommand`;
- `ApplicationQuery`;
- `ApplicationRunReceipt`;
- `RunCoordinator`.

`RunCoordinator` is constructor-injected and stateless between runs. The prepared paper path is M03 prepared authority → M04 prepared packet → independent M05/M06 evaluation → exact M05/M06 packets → M09 packet-only final-risk/capital authority → fresh injected paper scope → M10 paper execution → M11 reconciliation. The separate query path delegates only to M12.

The command carries caller-owned execution identity, packet identities, policies and timestamps. The query must explicitly declare isolated execution, an empty live-side-effect set and no runtime-authority promotion. The aggregate receipt is immutable, content-addressed and cannot claim replay, live execution or durable-state authority.

## Integration roadblock repaired

A direct import of `nvda_desk.packets.dmp_packets` failed through an eager `nvda_desk.contracts.__init__` cycle involving `contracts.parallel_risk`. The package initializer now loads named contract submodules lazily. The direct packet-builder import passes independently, and all admitted M01–M13 module blocks remain green.

M00 consumes the canonical M04 `K07_COMMON_CHECKS` and `K07_ROLE_CHECKS` definitions rather than duplicating packet-owner validation vocabulary.

## Proof results

```text
M00 targeted proof: 16 passed
All 14 admitted Tier A proof blocks: 754 passed; zero block failures
Tier B shadow: 83 passed
Vocabulary builder parity: 4 passed
proof_authority=PASS families=196 tests=198 blocks=67
Black: 473 files unchanged
Ruff: zero findings
compileall: PASS
git diff --check: PASS
```

Per-block Tier A counts:

```text
M13 152
M04 271
M01 18
M07 20
M08 23
M02 33
M03 29
M05 44
M06 33
M09 42
M10 28
M11 23
M12 22
M00 16
TOTAL 754
```

## Guardrails established

- no production module imports M00;
- the legacy runtime orchestrator and mutable API dependency routes are not imported or exported by M00;
- no wall-clock call exists in the M00 package;
- blocked/no-trade capital outcomes terminate before paper-scope creation;
- serial terminal outcomes retain the independent M06 evaluation but create no owner packets or downstream authority;
- a reused coordinator receives a fresh paper execution/portfolio scope for each run;
- M12 comparison-only results remain query projections and cannot become runtime authority;
- current promotion authority resolves 14 families through 14 blocks and 16 admitted paths.

## Unit 8 gate

Reinstall the project non-editably from the accepted offline wheelhouses at the clean Unit 7 commit, then run installed-package smoke, the repository-owned aggregate promotion gate, receipt verification and the complete Tier B shadow. No clean installed-package or aggregate completion claim is made in this Unit 7 record.
