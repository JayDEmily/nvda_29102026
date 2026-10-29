# AKR-3 architecture-authority reconciliation evidence

## Scope

AKR-3 reconciles the post-AKR-2 behaviour-neutral kernel authority. Current user instruction for this leaf additionally requires the mature Native Architecture Blueprint to be used as mandatory challenge evidence without first amending the ExecPlan.

Historical evidence does not reactivate former product semantics or the `M00–M15` allocation.

## Primary current authority read

Read in full for this leaf:

- `GUARDRAILS.md`;
- `AGENTS.md`;
- accepted `EXEC_PLAN.md` AKR-3 scope;
- current `ARCHITECTURE_KERNEL.md`;
- `ARCHITECTURAL_OBJECT_TAXONOMY.md`;
- `DEPENDENCY_LAWS.md`;
- `PUBLIC_SEAM_LAW.md`;
- `TEST_AND_PROMOTION_KERNEL.md`;
- `EXTENSION_AND_RETIREMENT_RULES.md`;
- `ARCHITECTURE_KERNEL_RESET_BRIEF.md`;
- `ADR_20260902_ARCHITECTURE_KERNEL_CONFORMANCE_HARDENING.md`.

## Historical challenge evidence

Read/inspected at historical commit `d24f9626a23b526384668b3cb26ee811b235eb5c`:

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`;
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`;
- `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`;
- the ownership/writer/reader/substitution sections of `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`;
- `docs/09_DMPV3_PROTOCOL_CORE.md`;
- `CURRENT_PROJECT_STATE.md` and `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md` as historical state/planning evidence only.

## Generic historical problems retained in current law

The current steady-state authority now explicitly retains these behaviour-neutral structural invariants:

1. architecture surface, semantic module and physical package are different concepts;
2. a carrier/protocol does not acquire the meaning it transports;
3. a technical state/transaction mechanism does not acquire consumer-domain meaning;
4. semantic owner, writer, reader, coordinator and reviewer are distinct roles;
5. adapters, contracts, schemas/models, services, repositories/stores, orchestrators, configuration and tests have bounded component forms;
6. runtime dependency, state/transaction participation, governance/promotion and build/test dependencies are distinct planes;
7. a public seam is an owned contract, not merely an import path;
8. architecture/config/test presence does not prove semantic or implementation truth.

The historical eighteen product surfaces and the old `M00–M15` allocation are not current kernel law.

## September conformance disposition

| Concern | AKR-3 disposition | Current authority owner / follow-up |
|---|---|---|
| real dependency-edge representation | `RETAIN_AS_KERNEL_LAW` | `DEPENDENCY_LAWS.md`; current mapping-shaped config/schema retained; real-path activation proof remains AKR-5 |
| category/dependency direction incl. lawful M→P/K | `RETAIN_AS_KERNEL_LAW` | `ARCHITECTURAL_OBJECT_TAXONOMY.md` + `DEPENDENCY_LAWS.md` |
| representable P/K activation without category conflation | `RETAIN_AS_KERNEL_LAW` | taxonomy/extension law; current schemas retain package/seam representation; category-complete activation proof remains AKR-5 |
| active-module semantic/ownership obligations | `REWRITE_AS_KERNEL_LAW` | `OWNERSHIP_AND_COMPONENT_LAW.md` + `EXTENSION_AND_RETIREMENT_RULES.md`; current validator/schema end-to-end proof remains AKR-5 |
| dynamic-import and import-form coverage | `RETAIN_AS_KERNEL_LAW` | `PUBLIC_SEAM_LAW.md`; known `from nvda_desk import m02` blind spot remains an implementation repair for AKR-5 |
| proof-scope accuracy | `REWRITE_AS_KERNEL_LAW` | `TEST_AND_PROMOTION_KERNEL.md`; recursive discovery and exact real-path proof remain AKR-5 |
| lifecycle/permanent-identity lineage | `RETAIN_AS_KERNEL_LAW` | taxonomy + extension/retirement law; current historical lineage remains representable without reactivation |
| public-seam exception law | `RETAIN_AS_KERNEL_LAW` | `PUBLIC_SEAM_LAW.md`; schema-complete exception shape already exists |
| typed-seam checker | `RETAIN_AS_KERNEL_LAW` | `PUBLIC_SEAM_LAW.md`; accepted mechanical implementation remains AKR-5 |
| CPython 3.14.7 / UUIDv7 intentions | `DO_NOT_CARRY_FORWARD_WITH_EVIDENCE` as current kernel requirement | retained only in historical ADR; current platform remains separately governed by toolchain files |

## Authority-manifest disposition

`authority/AUTHORITY_MANIFEST.md` is absent after AKR-2 and remains `DO_NOT_CARRY_FORWARD`. No current kernel invariant requires a second static hash manifest to legislate architecture authority. Git object identity, current accepted documents, schemas/registries and repository proof have separate jurisdictions; this leaf does not recreate the removed Raw Signal manifest.

## Steady-state authority correction

The former `ARCHITECTURE_KERNEL.md` duplicated detailed laws and embedded reset-time initial registry state as if it were permanent law. AKR-3 changes it to an authority router plus cross-cutting registry/composition/package propositions. Detailed proposition IDs now live in their owning law documents.

The current state itself remains in `config/architecture/*.yaml`; future lawful admission therefore does not require rewriting a normative "empty registry" proposition.

## Explicit implementation gaps left to AKR-5

AKR-3 is authority reconciliation, not implementation repair. The following known mechanical gaps remain open and must not be represented as proved merely because the law is now clear:

- `validation.py` still rejects every active runtime module using reset-only logic;
- `dependencies.py` still has the reproduced `ImportFrom` owner/seam blind spot;
- `proof.py` still discovers only top-level `test_*.py` paths in the two proof jurisdictions;
- a pinned static type checker is not yet part of the proof surface;
- category-complete first activation still requires real committed configuration-path proof.

These are AKR-5 obligations under the accepted ExecPlan.

The new `AK-OWN-001`, `AK-FORM-001` and `AK-STATE-001` propositions are current normative requirements after this reconciliation but have no dedicated admitted proof family in AKR-3. No mechanical proof claim is made for them here; proof design/admission belongs to AKR-5 before capability admission.
