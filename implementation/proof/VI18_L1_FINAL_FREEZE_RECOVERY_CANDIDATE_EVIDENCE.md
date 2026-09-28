# VI-18-L1 — Final freeze and durable recovery artefact — Worker candidate evidence

## Epistemic status

This is Worker evidence for the VI-18-L1 freeze candidate. It is **not** terminal acceptance.
Independent VI-18 Tester disposition remains **UNPROVED** until a fresh Tester reviews the exact
frozen candidate and recovery artefact.

## Scope and authority

The active ExecPlan defines VI-18-L1 as a closure/freeze leaf only. No implementation meaning,
proof-control meaning, architecture authority, dependency selection or package byte may be changed
by this leaf. The authorised Worker action is limited to exact terminal identity binding, durable
full-Git recovery creation/readback, terminal evidence/current-state records, candidate freeze and
fresh Tester routing.

## Accepted predecessor and routed baseline

**VERIFIED** at the VI-18 routed baseline:

- accepted VI-17-L2 promotion close-out: `88499cc58767e25919a09c03ff0fdf9f5ea14e5e`;
- VI-18 route/current accepted `main`: `4df802c3ebe67409125c58655534814f24b9ae2b`;
- routed baseline tree: `4a15cb1ba7877ee765a395c1d6cd1a986a72cb48`;
- Worker branch: `work/vi18-l1-final-freeze-recovery`;
- worktree clean before VI-18 evidence mutation;
- `git diff --check`: PASS;
- `git fsck --full --no-dangling`: PASS.

The exact frozen VI-18 candidate commit/tree cannot exist until the freeze commit is created. The
Worker cycle routing records must bind that exact identity after freeze. That frozen candidate is the
only state proposed for terminal promotion if, and only if, the independent VI-18 Tester returns
`PASS` and the terminal close-out preserves ancestry.

## Active implementation identity

**VERIFIED:** the accepted final package/implementation candidate remains
`332c1f95da032f841e8779ef21fe3c1fceb698a2` / tree
`3abec93134d128978ad6bcedbd0dfa6cf4334ec6`.

The accepted U01-U06 semantic lineage remains anchored by accepted U06 production candidate
`8462630277b04d431ad393e2b73039cacb5d6247` and U06 Tester `PASS`
`562767529235cedff77d3e740a259fab9d88716e`. VI-14 through VI-17 subsequently proved integrated
interaction, package/aggregate state, whole-BICP semantics, authority/lineage and provenance/integrity.

**VERIFIED:** there is no diff from accepted package candidate `332c1f95...` to the VI-18 routed
baseline in `src/**`, `tests/**`, `config/**` or `pyproject.toml`. The same no-drift check is empty
against accepted VI-16, VI-17-L1 and VI-17-L2 candidates for those paths.

## Final distribution and package identities

**VERIFIED / ACCEPTED predecessor state:**

- distribution: `nvda-architecture-kernel==1.0.0`;
- wheel: `nvda_architecture_kernel-1.0.0-py3-none-any.whl`;
- wheel SHA-256: `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- sdist: `nvda_architecture_kernel-1.0.0.tar.gz`;
- sdist SHA-256: `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`.

`sha256sum -c PACKAGE_ARTIFACTS/SHA256SUMS` passed at the routed baseline and again from the fresh
recovery readback.

## Final aggregate result identities

The final aggregate results are bound to independently reviewed accepted evidence rather than
re-executed by this terminal evidence-only leaf:

- product aggregate result identity: Tester cycle `TESTER_VI15_L2_1790584579`, disposition commit
  `eed5c5f6fa9eeda02886ed8fda0d6205177823e5` — complete admitted product population **479/479
  PASS**, six admitted product families, **13/13** required product obligations;
- architecture aggregate result identity: the same independent Tester disposition
  `eed5c5f6fa9eeda02886ed8fda0d6205177823e5` — architecture/bootstrap blocking set **74/74 PASS**;
- whole-BICP independent semantic re-challenge: Tester cycle `TESTER_VI16_L1_1790592833`,
  disposition `9f5f7e90b463365fb39c361f2e346d9e67c6d915` — independently re-observed product **479/479**,
  six families / **13/13** obligations and architecture/bootstrap **74/74**.

VI-18 makes no new claim that these tests were rerun in the present sandbox.

## Accepted VI-14 through VI-17 review identities

**VERIFIED ancestors of the routed VI-18 baseline:**

| Leaf | Frozen candidate | Independent Tester PASS |
| --- | --- | --- |
| VI-14-L1 | `076f1e979474babbb8985dc87d3b2d4d62ec0b4c` | `79b1d9d1d9da1b921c8d8197d154937dd1a699e5` |
| VI-15-L1 | `466055a1cd5fe678a40049a00f0dc88158951d74` | `226c5cdebdfa33d5b3d8f43d3eb67b0ae6b8b355` |
| VI-15-L2 | `332c1f95da032f841e8779ef21fe3c1fceb698a2` | `eed5c5f6fa9eeda02886ed8fda0d6205177823e5` |
| VI-16-L1 | `9248f3b1788f8e99e59a0482c4cc393c27942715` | `9f5f7e90b463365fb39c361f2e346d9e67c6d915` |
| VI-17-L1 | `c07d5277512f600669b05a88cc2c174af3e3b046` | `5397a90dd2e245e17bd5e0eb526861396dae3082` |
| VI-17-L2 | `57712201296c6da811e4e6838d0f3fb302239df4` | `90fdc6fc5f2fe13e81202dd50f1f9d4c9dfa4634` |

## Remaining Unknowns intentionally unresolved / out of scope

VI-04 closed only the exact owner package/public seam, Psycopg driver, smallest correctness-only
PostgreSQL physical delegation and PostgreSQL 17.9 proof-environment choice. VI-15 closed only final
distribution name/version. The following IWO Remaining Unknowns therefore remain intentionally
unresolved or outside this BICP and must not be converted into terminal claims:

- concrete provider eligibility/scope/mapping contents;
- provider revision/retransmission equivalence;
- clock accuracy/drift/leap/smear/wake latency;
- finality/watermarks/exact counts/member queries;
- provider duplicate equivalence/exactly-once;
- pre-commit raw loss/bounded recovery;
- availability/latency/throughput/RTO/RPO;
- production opaque-ID generation/collision/cross-process recovery;
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

The historical IWO entry for final distribution naming/version is no longer Unknown because VI-15
explicitly resolved it to `nvda-architecture-kernel==1.0.0`.

## Inactive capabilities that remain inactive

**VERIFIED** from current architecture registration and accepted package/install review: only M00
Raw Signal Occurrence Truth is active at the bounded implementation surface. The following remain
inactive/not admitted:

- P01 / DMPV3 packet/carrier capability;
- K01;
- authoritative replay/re-execution/equivalence capability;
- live provider/API/network integration;
- live external side effects or account authority;
- validation/quarantine capability;
- D001+ event-time/downstream derivation semantics;
- downstream signal/model/trading/risk/portfolio/business consumers;
- retention/deletion/deterministic recomputation beyond admitted referential reads;
- exact membership/count/finality/watermark capability;
- SLA/performance/RTO/RPO/bounded-recovery capability.

Current `config/architecture/modules.yaml` registers only M00 as active and explicitly excludes these
classes. Accepted VI-15-L2 installed-distribution review found only `architecture`, `composition` and
`raw_signal_occurrence_truth` runtime packages and no P01, K01, provider/network, downstream,
DMPV3 or replay package.

## Durable full-Git recovery artefact

The Worker created:

- file: `NVDA_G03_VI18_L1_TERMINAL_RECOVERY_FULL_GIT_AND_PACKAGE_20260929.tar.gz`;
- bytes: `5,965,855`;
- SHA-256: `156c0e720e69e1a31a307d8751582616f9187c6a3ee6947dfa22c413e840b251`.

It contains the full active Git repository plus the accepted wheel/sdist at the clean VI-18 routed
baseline, before VI-18 evidence/candidate mutation. This is deliberately a recovery artefact for the
accepted repository history feeding the terminal freeze; it is not itself a VI-18 Tester PASS or
terminal-promotion record.

### Recovery readback

A fresh extraction independently established:

- readback `HEAD`: `4df802c3ebe67409125c58655534814f24b9ae2b`;
- readback tree: `4a15cb1ba7877ee765a395c1d6cd1a986a72cb48`;
- readback `main`: `4df802c3ebe67409125c58655534814f24b9ae2b`;
- branch: `work/vi18-l1-final-freeze-recovery`;
- worktree status count: `0`;
- `git diff --check`: PASS;
- `git fsck --full --no-dangling`: PASS;
- source and readback `git show-ref` SHA-256:
  `2ea2adac6e8183ab8ee028c502741a8b28330787c321b75e4bdb7cd0cefd20a2`;
- wheel/sdist manifest validation: PASS.

The first generated recovery manifest recorded an incorrect `show-ref` digest even though the live
and extracted ref sets were identical. The Worker stopped before candidate freeze, diagnosed the
manifest-only defect, replaced that value with the directly recomputed matching digest, regenerated
the archive, and repeated fresh extraction/readback successfully. The superseded archive identity
`8252286763da8c98b8df0cca589f9785902a3e6021eb1b28ef2dc5c2ac22bacd` is **not** the recovery
identity for VI-18 acceptance.

The active thin-history boundary remains explicit: thin root
`8133432ba8a07e4d04d83b14af5c3c4bd12e6b0e` is present; external predecessor
`d095954c16a9818eadb60d6364148229f2dc4558` is intentionally absent from this active thin object
database and is not claimed as local ancestry.

## Preserved provenance limitation

The VI-17-L2 accepted limitation remains unchanged: the exact binary/archive digest of the prior
accepted PyYAML 6.0.3 proof-environment overlay is **UNKNOWN**. No claim of a fully self-contained,
arbitrary-host reproducible build/proof environment is made.

## Worker conclusion and boundary

**VERIFIED:** no VI-18 terminal-freeze blocker has been established by the Worker evidence trace
after repair and successful readback of the recovery artefact. No `src/**`, `tests/**`, `config/**`
or `pyproject.toml` mutation is authorised or required by this leaf.

**UNPROVED:** VI-18 terminal acceptance. A fresh independent Tester must challenge the exact frozen
candidate, all prerequisite/recovery/package identities, the no-drift proposition, Remaining
Unknown/inactive-capability record, repository integrity and bounded terminal claims. Only that
Tester may return the VI-18 terminal disposition defined by the ExecPlan.
