# VI-16-L1 — Whole-BICP semantic review candidate evidence

## Status

**WORKER TRACE COMPLETE / CANDIDATE PREPARATION — INDEPENDENT TESTER REQUIRED.**

This is the VI-16-L1 Worker review packet required by section 8 of the accepted ExecPlan. It binds the
accepted semantic authority, realised implementation/proof state and accepted package artefacts into one
review surface. It does **not** award VI-16 semantic acceptance. Only the fresh VI-16 Tester may dispose
the frozen candidate as `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`.

## 1. Exact governing and semantic authority

Verified current byte identities:

| Authority | Path | SHA-256 |
| --- | --- | --- |
| BICP narrative | `handoff/authority/BICP_CANDIDATE_005.md` | `6b2906b92e11bf09fd7f8b188e8ed6555a0a5ae61636909f676f84827601d21f` |
| BICP machine packet | `handoff/authority/BICP_CANDIDATE_005.json` | `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed` |
| accepted IRB | `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md` | `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342` |
| accepted IWO narrative | `implementation/work_order/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md` | `b23fec7e83eace6353272f92b983160c2ab768043640d15d7ee1fb88f270ca0e` |
| accepted IWO machine packet | `implementation/work_order/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.json` | `a673ff05bc58870fdfca49167482aabe4647889d7750fd1b49805c7064ef7eed` |

Supplementing current programme authority:

- `implementation/authority/VI04_AUTHORITY_CLOSURE.md` fixes owner package
  `nvda_desk.raw_signal_occurrence_truth`, public seam `nvda_desk.raw_signal_occurrence_truth.api`,
  `psycopg[binary]==3.3.4`, PostgreSQL 17.9 as proof environment only, and bounded delegation for the
  smallest correctness-only PostgreSQL layout/types/direct repository-adapter form required by BC-011.
  PostgreSQL/schema/driver/repository remain non-owning mechanisms.
- `implementation/authority/VI15_L1_FINAL_DISTRIBUTION_AUTHORITY.md` fixes final distribution metadata
  exactly to `nvda-architecture-kernel==1.0.0` and closes no other Remaining Unknown.

## 2. Accepted implementation lineage rebound

The following accepted unit identities are all verified ancestors of the current VI-16 Worker state:

| Unit | Accepted implementation candidate | Independent acceptance | Promotion / accepted-forward identity |
| --- | --- | --- | --- |
| U01 | `e8b659d7849d2f95b64ba32bed8090a8290358d4` | Reviewer-022 `4db58e9091083500a2505023a302f36447185029` | `b806447eb440a016826728af075e714beee23d31` |
| U02 | `5c62ec5147da718297b251b5a287405ebf3b4755` | Reviewer-024 `df45c5e93e7c4c19cb1cca75de5cd1c64b15537c` | `a78ae7b5515c2e482a2656cebeebae3fa5a6d584` |
| U03 | `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf` | clarification `c4caa78a2d13c5dc115c83fedcdf44648efe6d78`; Reviewer-030 `dc40971d24ee773ee133d07622f92d709a7cec11` | `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec` |
| U04 | `dc3b448191a2b2d3528ffb576b1ebc2c56839991` | Reviewer-032 `dd42d645b59a62f88cfbc7fba47a75e415b7296f` | accepted recovery baseline carried forward into U05 |
| U05 | `2bdbedff62307ecfaf6186f9c12814fb662c11a7` | Tester `9f35df4c1915de78847dfc4a23ce886dfa3b5fd8` | `9f35df4c1915de78847dfc4a23ce886dfa3b5fd8` |
| U06 | `8462630277b04d431ad393e2b73039cacb5d6247` | Tester `562767529235cedff77d3e740a259fab9d88716e` | Tester/promoted lineage `562767529235cedff77d3e740a259fab9d88716e`; close-out `ed94f745effd65050f03d921ad0ae30769877206` |

This table records lineage; it does not substitute those earlier reviews for the fresh VI-16 whole-system review.

## 3. Final realised implementation and architecture paths

The final product-visible/runtime paths bound into the accepted package candidate are:

- M00 public semantic owner: `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
- M00 package export: `src/nvda_desk/raw_signal_occurrence_truth/__init__.py`;
- private non-owning PostgreSQL mechanism: `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py`;
- A00 construction/orchestration: `src/nvda_desk/composition/__init__.py`;
- architecture owner/form/dependency/allocation authority: `config/architecture/modules.yaml`,
  `application_shells.yaml`, `dependency_rules.yaml`, `implementation_allocations.yaml`, `protocols.yaml`,
  `kernels.yaml`, and `surfaces.yaml`;
- product proof-control authority: `config/product_proof/authority.yaml`, `families.yaml`, `aggregates.yaml`;
- architecture/bootstrap proof-control authority: `config/proof/test_families.yaml`, `proof_blocks.yaml`,
  `promotion_sets.yaml`;
- final distribution/dependency metadata: `pyproject.toml`.

Current architecture records allocate runtime implementation only to M00, declare the runtime owner edge exactly
`A00 -> M00`, keep P01 and K01 as placeholders, and expose no architecture surface. The only private technical
composition exception is A00's import of `create_postgres_persistence`; Raw Signal decisions remain in M00.

## 4. Twelve named Raw Signal propositions — whole-system binding

`TRACE BOUND` below means the Worker found an authority -> proof -> realised source/package path and no obvious
contradiction in that path. It is not a VI-16 PASS.

| Proposition | Accepted meaning | Current product proof | Realised implementation/package trace | Worker trace |
| --- | --- | --- | --- | --- |
| `M16-RSOT-001` | Bounded ownership | `IA17-PROD-001`; U01 family, supported again by U06 composition | M00 `api.py` owns commands/outcomes/persistence semantics; A00 composes; `_postgres.py` stores owner-decided facts; `modules.yaml` records M00 ownership | TRACE BOUND |
| `M16-RSOT-002` | Configured schedule truth | `IA17-PROD-002`; U02 family | immutable policy registration and exact 30-second slot realisation in `api.py`; no scheduler-wake substitution | TRACE BOUND |
| `M16-RSOT-003` | Occurrence admission | `IA17-PROD-003`; U03 family | `RawObservationOccurrenceV1` and owner admission preserve one actually received provider-logical record per observation and independent capture/observation validity | TRACE BOUND |
| `M16-RSOT-004` | Native fidelity | `IA17-PROD-004`; U03 family | finite `NativeValueV1`, alias-safe snapshot and exact native equality in `api.py`; PostgreSQL native codec round-trips the admitted carrier | TRACE BOUND |
| `M16-RSOT-005` | Temporal-kind law | `IA17-PROD-005`; U03 family | exact `true_instant|date_only|receipt_only` contract law; UTC receipt separated from provider timestamp/timezone; no raw `event_ts_utc` field | TRACE BOUND |
| `M16-RSOT-006` | Receipt-evidence law | `IA17-PROD-006`; U04 family | `derive_capture_receipt_evidence_relation` requires in-slot receipt plus separately supplied eligibility decision and emits only `evidences_receipt_presence_only` | TRACE BOUND |
| `M16-RSOT-007` | Assessment law | `IA17-PROD-007`; U04/U05 families | owner computes exactly three outcomes, enforces append-only immediate-predecessor supersession; PostgreSQL inserts owner-decided assessment without re-derivation | TRACE BOUND |
| `M16-RSOT-008` | Identity and retry law | `IA17-PROD-008`; U02/U03/U04/U05 coverage | distinct opaque identity classes; exact same-ID content comparison; stable schedule retry ref distinct from occurrence ID; no equal-value/provider-ID dedup | TRACE BOUND |
| `M16-RSOT-009` | Persistence/failure law | successor `IA22R01-PROD-009`; U05 family | direct Psycopg mechanism behind M-owned port, per-operation transactions, commit/rollback, durable restart reconciliation; missing owed slot creates `unknown_not_established`, never inferred zero | TRACE BOUND |
| `M16-RSOT-010` | Referential replay law | `IA17-PROD-010`; U05 family | referential reads return original facts by domain identity; no authoritative replay execution/runtime package is present | TRACE BOUND |
| `M16-RSOT-011` | Public governance law | `IA17-PROD-011`; U01/U06 families | exact v1 typed M00 command/read facets; A00 sole authorised caller; one declared private technical PostgreSQL constructor exception only | TRACE BOUND |
| `M16-RSOT-012` | Compatibility law | `IA17-PROD-012`; U01 family | exact v1 contracts/requiredness/discriminants/types remain bound; no successor schema or silent weakening is introduced | TRACE BOUND |

## 5. BC-001 composition trace

BC-001 requires M00/M16 to own the five accepted meanings plus semantic persistence/transaction-outcome truth;
A00 may construct/translate/orchestrate but may not own Raw Signal meaning; PostgreSQL is a technical translator;
P01/K01 remain inactive and no downstream consumer is admitted.

The final realised path is:

```text
A00 create_application
  -> private technical create_postgres_persistence(postgres_dsn)
  -> public M00 create_owner(durability_port=...)
  -> M00 commands / reads
  -> M00-owned semantic decisions
  -> M00 persistence port
  -> private PostgreSQL transaction adapter
```

`Application.run_raw_signal_proof_sequence` delegates policy -> capture -> observation -> relation -> assessment ->
referential read through M00 commands/reads. It validates that the caller's effective policy reference matches the
policy accepted by M00, but it does not calculate assessment outcome, fabricate semantic result objects, write SQL,
or access M00 private state. `_postgres.py` accepts/stores/reconstructs typed owner facts and provides transaction
commit/rollback; semantic assessment selection remains in `api.py`.

Current dependency/configuration authority declares `A00 -> M00` only. No `M00 -> A00` production dependency was
identified by Worker source trace. P01/K01 have no runtime package allocation.

## 6. Nineteen current proof obligations

### Product obligations — 13/13 current required IDs

| Obligation | Authority / proposition | Registered physical family | Final-state accepted evidence |
| --- | --- | --- | --- |
| `IA17-PROD-001` | BC-001/013; RSOT-001 | `rsot_u01_contract_owner` | VI-15-L2 aggregate included current family; 479/479 aggregate, 13/13 obligations |
| `IA17-PROD-002` | BC-003/004; RSOT-002 | `rsot_u02_capture_schedule` | same accepted aggregate |
| `IA17-PROD-003` | BC-005/006; RSOT-003 | `rsot_u03_observation_native_temporal` | same accepted aggregate |
| `IA17-PROD-004` | BC-002/005/006/009; RSOT-004 | `rsot_u03_observation_native_temporal` | same accepted aggregate |
| `IA17-PROD-005` | BC-005/009; RSOT-005 | `rsot_u03_observation_native_temporal` | same accepted aggregate |
| `IA17-PROD-006` | BC-007; RSOT-006 | `rsot_u04_receipt_assessment` | same accepted aggregate |
| `IA17-PROD-007` | BC-008/009; RSOT-007 | U04 plus `rsot_u05_postgresql_durability` for durable state | same accepted aggregate |
| `IA17-PROD-008` | BC-002/004/010; RSOT-008 | U02/U03/U04 plus U05 durable retry coverage | same accepted aggregate |
| `IA22R01-PROD-009` | BC-011/015; RSOT-009 | `rsot_u05_postgresql_durability` | real PostgreSQL family in accepted aggregate; predecessor `IA17-PROD-009` remains forbidden lineage-only |
| `IA17-PROD-010` | BC-011/016; RSOT-010 | `rsot_u05_postgresql_durability` | same accepted aggregate |
| `IA17-PROD-011` | BC-001/002/013; RSOT-011 | U01 and `rsot_u06_a00_composition` | same accepted aggregate |
| `IA17-PROD-012` | BC-012; RSOT-012 | `rsot_u01_contract_owner` | same accepted aggregate |
| `IA17-PROD-013` | BC-001/014/015 | `rsot_u06_a00_composition` | same accepted aggregate; final A00->M00 sequential composition |

Current `config/product_proof/authority.yaml` binds the exact BICP/IRB hashes above, requires exactly these 13 IDs,
forbids predecessor `IA17-PROD-009`, and leaves product tier `NOT_CLASSIFIED`. The six current product families remain
separately registered in `config/product_proof/families.yaml`.

### Architecture obligations — 6/6 BICP obligations bound to the current architecture kernel

| Obligation | BICP authority | Current architecture proof population bearing on it |
| --- | --- | --- |
| `IA17-ARCH-001` | implementation-authority ingress | `implementation_authority_ingress` (`AK-INGRESS-001..005`) |
| `IA17-ARCH-002` | taxonomy / identity / lifecycle / registry | `registry_schema`, `identifier_taxonomy`, `object_lifecycle`, `activation_readiness` |
| `IA17-ARCH-003` | owner / form / state boundary | `activation_readiness` (`AK-OWN-001`, `AK-FORM-001`, `AK-STATE-001`) plus registry law |
| `IA17-ARCH-004` | dependency direction | `dependency_direction` plus `activation_readiness` (`AK-DEP-001/002`) |
| `IA17-ARCH-005` | public seam | `public_seam_law`, `typed_public_seam`, `activation_readiness` |
| `IA17-ARCH-006` | composition / proof / package law | `object_lifecycle`, `proof_control`, `minimal_imports`, `legacy_exclusion`, `activation_readiness` |

The accepted VI-15-L2 architecture/bootstrap axis was 74/74 across the 11 current-blocking families and remained
separate from the product aggregate.

## 7. Final package identity and byte binding

Accepted VI-15-L2 package candidate:

- commit `332c1f95da032f841e8779ef21fe3c1fceb698a2`;
- tree `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`;
- distribution `nvda-architecture-kernel==1.0.0`;
- wheel `nvda_architecture_kernel-1.0.0-py3-none-any.whl`, 37,378 bytes,
  SHA-256 `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- sdist `nvda_architecture_kernel-1.0.0.tar.gz`, 161,445 bytes,
  SHA-256 `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`.

VI-16 Worker readback established:

- `SHA256SUMS` verifies both supplied artefacts;
- the wheel contains 21 files total and 16 Python files;
- all 16 wheel Python files are byte-identical to the corresponding `src/nvda_desk/**` blobs at exact package
  candidate `332c1f95...`;
- installed/runtime top-level package roots represented in the wheel are exactly `architecture`, `composition`, and
  `raw_signal_occurrence_truth` under `nvda_desk`;
- selected semantic/config/source files in the 117-member sdist are byte-identical to exact candidate `332c1f95...`;
- wheel metadata is exactly `nvda-architecture-kernel==1.0.0`, `Requires-Python: ==3.13.5`,
  `psycopg[binary]==3.3.4`, and `pyyaml==6.0.3`.

The current VI-16 branch is intentionally later than the package candidate because accepted Tester/promotion/review
records were added afterwards. There is **no** `src/**`, `tests/**`, `config/**` or `pyproject.toml` drift from
`332c1f95...` to the VI-16 routed Worker baseline. The accepted wheel/sdist therefore remain bound to the exact final
implementation/proof/config/package-metadata bytes under review. This packet does not claim that rebuilding the sdist
from the later VI-16 evidence/routing tree would be byte-identical, because the sdist includes repository evidence/
governance files that legitimately advanced after the package candidate.

## 8. Accepted VI-14 and VI-15 evidence

- VI-14 exact candidate `076f1e979474babbb8985dc87d3b2d4d62ec0b4c` / tree
  `45aec5c01ae8a35fa8879fab978c6fb0f0082140`; independent Tester PASS
  `79b1d9d1d9da1b921c8d8197d154937dd1a699e5`. Integrated material set: 66/66, product control 13/13,
  architecture/bootstrap 74/74, plus fixture-independent production A00->PostgreSQL-backed M00 challenge.
- VI-15-L1 exact candidate `466055a1cd5fe678a40049a00f0dc88158951d74`; independent Tester PASS
  `226c5cdebdfa33d5b3d8f43d3eb67b0ae6b8b355`; close-out `abccadf20d10daa29e739c6ba54a970fcff41614`.
  This leaf applied only the Programme Owner's `nvda-architecture-kernel==1.0.0` metadata authority.
- VI-15-L2 exact candidate/package identities are those in section 7; independent Tester PASS
  `eed5c5f6fa9eeda02886ed8fda0d6205177823e5`; promotion close-out
  `93c1212f113e6cc4f14aca7fb7a2e560f691c38f`. The independent Tester rebuilt byte-identical artefacts,
  re-ran the complete product and architecture populations, installed outside the source tree, and directly challenged
  the installed A00->M00 PostgreSQL public path.

VI-16 does not relabel those results as newly rerun evidence; it uses them as accepted exact-final-byte predecessor
evidence and independently checks that the bytes to which they apply have not drifted.

## 9. Remaining Unknowns and current dispositions

### Closed only by later explicit/bounded authority

| Former Remaining Unknown | Current disposition | Authority boundary |
| --- | --- | --- |
| owner package / public seam | RESOLVED | VI-04: exactly `nvda_desk.raw_signal_occurrence_truth` / `.api` |
| PostgreSQL Python driver | RESOLVED | VI-04: exactly `psycopg[binary]==3.3.4` |
| smallest correctness-only physical PostgreSQL relation layout / SQL types / direct repository-adapter form needed for BC-011 | RESOLVED BY BOUNDED DELEGATION | VI-04; mechanism only, no semantic ownership; no partitioning/pooling/performance-policy authority |
| final distribution naming/version metadata | RESOLVED | VI-15-L1: exactly `nvda-architecture-kernel==1.0.0` |

### Preserved unresolved / outside the admitted slice

The following IWO/BC-016 items remain unresolved and are not selected by the realised implementation:

- concrete provider eligibility/scope/mapping contents;
- provider revision/retransmission equivalence;
- clock accuracy/drift/leap/smear/wake latency;
- finality/watermarks/exact counts/member queries;
- provider duplicate equivalence/exactly-once;
- pre-commit raw loss/bounded recovery;
- availability/latency/throughput/RTO/RPO;
- production opaque-ID generation/collision handling/cross-process recovery;
- PostgreSQL partitioning;
- PostgreSQL pooling;
- performance/SLA index policy;
- retention/deletion/deterministic recomputation/P01;
- real provider adapters/networking;
- validation/quarantine;
- D001+;
- downstream consumers/behaviour;
- historical-M re-establishment detail;
- provider/collector-specific ingestion-sequence scope/overflow.

BC-016's broader physical-PostgreSQL unknown was narrowed only by VI-04. Correctness constraints intrinsic to the
bounded selected layout are permitted; separately designed performance indexes, partitioning and pooling remain
unresolved. PostgreSQL 17.9 remains proof-environment authority only, not a production-version claim.

Worker source trace found no path that converts any preserved item above into an operational/default semantic claim.
Where eligibility is required for in-slot receipt evidence, absence of an admitted `eligibility_resolver` fails closed
with an error rather than defaulting eligible/ineligible. Production opaque IDs remain supplied/injected to the owner;
the code does not claim a production generator.

## 10. Inactive capabilities that must remain inactive

The following are outside this BICP and must not be activated by VI-16 or the accepted package:

- P01 / DMPV3 packet/carrier implementation;
- K01 selection/activation;
- authoritative replay/re-execution or equivalence machinery;
- live provider/API/network adapters;
- live external side effects or account authority;
- validation/quarantine semantics;
- D001+ event-time/downstream derivation semantics;
- downstream signal/model/trading/risk/portfolio/business consumers;
- retention/deletion/deterministic recomputation capability beyond referential non-deletion reads;
- exact membership/count/finality/watermark capability;
- SLA/performance/RTO/RPO/bounded-recovery capability.

Current architecture records keep P01 and K01 as placeholders and allocate only M00. Worker inspection of production
`src/nvda_desk/**` found no P01, K01, DMPV3, authoritative-replay, provider-network or downstream runtime implementation
reference, and the exact wheel contains no corresponding runtime package root.

## 11. Worker whole-system obvious-gap trace

The Worker traced authority -> IWO -> accepted unit lineage -> current proof controls -> realised M00/A00/PostgreSQL
source -> exact accepted package artefacts.

**VERIFIED observations:**

1. Current BICP/IRB/IWO hashes match their recorded accepted identities.
2. Every accepted U01-U06 candidate/review identity listed above is an ancestor of the current VI-16 Worker lineage.
3. Exact VI-15-L2 package candidate `332c1f95...` is an ancestor of the current VI-16 state.
4. There is no post-package-candidate drift in `src/**`, `tests/**`, `config/**` or `pyproject.toml`.
5. Product proof-control still requires exactly 13 current obligations, uses repaired successor
   `IA22R01-PROD-009`, and explicitly forbids predecessor `IA17-PROD-009`.
6. Architecture proof-control still contains 11 current-blocking families in the `architecture_kernel` promotion set.
7. M00 source owns semantic decisions; A00 composes/orchestrates; PostgreSQL stores/reconstructs owner facts and commits
   transactions without an observed semantic decision branch of its own.
8. Receipt eligibility does not acquire a hidden default: an in-slot observation requiring eligibility fails closed when
   no admitted resolver is supplied.
9. Restart reconciliation creates `unknown_not_established` for an owed slot lacking an assessment; it does not infer
   `zero_received`.
10. Exact wheel Python runtime bytes match candidate source and expose only the admitted framework/A00/M00 roots.
11. Exact sdist semantic/config/source members sampled for this trace match candidate blobs, and the supplied package
    hashes remain intact.
12. No substantive VI-16 repair was identified by this Worker trace, so no return to an owning implementation layer was
    triggered.

**WORKER CONCLUSION:** `NO_OBVIOUS_GAP_IDENTIFIED_BY_WORKER_TRACE`.

That conclusion is deliberately narrower than semantic acceptance. The fresh VI-16 Tester must independently challenge
all twelve propositions, BC-001, all nineteen obligations, hidden-default/additional-meaning risk, inactive capability
closure, mechanism ownership, product-visible boundedness and proof relevance to the exact final package bytes.

## 12. VI-16 Worker validation performed

Commands/checks used in this leaf included:

- direct SHA-256 calculation of BICP/IRB/IWO files;
- `git merge-base --is-ancestor` for accepted U01-U06, VI-14 and VI-15 identities;
- exact scoped diff `332c1f95... .. current VI-16 baseline -- src tests config pyproject.toml`;
- `sha256sum -c PACKAGE_ARTIFACTS/SHA256SUMS`;
- wheel inventory and byte comparison of all 16 Python runtime files against `git show 332c1f95:<source>`;
- sdist inventory and exact candidate-byte comparison for final package metadata, product-proof control,
  architecture owner/dependency/allocation records, M00 public owner, PostgreSQL mechanism and A00 composition;
- direct source trace of M00 commands/reads, PostgreSQL transaction adapter and A00 sequence;
- targeted production-source scan for inactive/forbidden capability terms and current architecture/config references.

The VI-15-L2 479/479 product and 74/74 architecture/bootstrap aggregates were **not rerun by this VI-16 Worker**.
They remain the independently accepted exact-package-candidate evidence. The VI-16 Worker's job is semantic review
packet preparation and obvious-gap tracing, not manufacturing duplicate aggregate evidence after verifying no relevant
byte drift.

## 13. Non-claims / handoff boundary

This Worker packet does not claim:

- VI-16 `PASS` or semantic acceptance;
- operational fitness or production commissioning;
- provider integration or downstream NVDA capability;
- product Tier A/B/C classification;
- any preserved Remaining Unknown;
- any inactive capability;
- package reproducibility from later evidence/routing commits rather than exact package candidate `332c1f95...`.

The next lawful action after exact candidate freeze is a **fresh independent VI-16 Tester review**. VI-17 must not begin
unless that Tester accepts the exact candidate and the accepted lineage is subsequently promoted to `main`.
