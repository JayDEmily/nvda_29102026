# VI-17-L1 — Authority and lineage reconstruction Worker evidence

## Status

`WORKER AUDIT COMPLETE / CANDIDATE FREEZE PENDING / INDEPENDENT TESTER REQUIRED`

This record executes only VI-17-L1 of the current root `EXEC_PLAN.md`. It reconstructs the current
Raw Signal Occurrence Truth authority-to-package lineage and records the Worker's audit findings. It
does not self-award VI-17-L1 acceptance and does not begin VI-17-L2.

## 1. Governing authority rebound

The Worker reread the current root `GUARDRAILS.md`, root `AGENTS.md`, current root `EXEC_PLAN.md`,
`handoff/control/CURRENT_STATE.md`, the active VI-17-L1 request, applicable test-local guidance,
and the current primary authority/proof/implementation evidence required by the leaf.

Exact current fixed authority identities:

| Authority | SHA-256 / identity | Worker finding |
| --- | --- | --- |
| accepted BICP JSON | `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed` | current bytes match |
| accepted BICP Markdown | `6b2906b92e11bf09fd7f8b188e8ed6555a0a5ae61636909f676f84827601d21f` | current bytes match |
| accepted IRB | `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342` | current bytes match |
| VI-04 authority closure | `4909bfb3561f4ad08d21d82005f2aa60ed9c18440067c91180f6ee65c85bc9ca` | current bytes match |
| fixed IWO JSON | `a673ff05bc58870fdfca49167482aabe4647889d7750fd1b49805c7064ef7eed` | handoff/implementation copies match |
| fixed IWO Markdown | `b23fec7e83eace6353272f92b983160c2ab768043640d15d7ee1fb88f270ca0e` | handoff/implementation copies match |
| VI-15 final distribution authority | `59ad4a66bedeacd89947fae974808d435fd94cf9eb1ef7e9bbeec7797780b4c2` | exact `nvda-architecture-kernel==1.0.0` |

The current implementation-authority binding still binds IRB SHA-256
`938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`, acceptance reference
`IA-AUTH-001`, create target `M / raw_signal_occurrence_truth`, and modify target `A00`.

### VI-06 IWO review status preserved exactly

`implementation/review/VI06_IWO_REVIEW_001.md` remains a blocked independent-review record; it is
not relabelled `PASS`. `implementation/authority/VI06_OWNER_DIRECTION.md` records the later explicit
Programme Owner decision to proceed with the fixed VI-05 IWO as the work order for this run while
preserving the blocked review evidence. Therefore the execution authority is the fixed IWO plus the
Programme Owner routing decision, not a fictitious VI-06 reviewer acceptance.

## 2. Explicit later authority additions are separately attributable

The audit found later authority records in ordinary Git history. They are not silent source/test
inventions:

- canonical Raw Signal catalogue carriage:
  `implementation/authority/VI10R6_SIGNAL_CATALOGUE_CARRIAGE.md`, SHA-256
  `eff91fce5738df073fe57b18d97ac594c746c40b81af0873e5e7339a9f64001e`, with canonical workbook
  SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`;
- U03 recurrence/root-cause routing:
  `VI13R_U03_NATIVE_RETRY_ROOT_CAUSE_DIRECTION.md`, SHA-256
  `17e34d411cd94eb58867963a3a752ca2228d4c5d69160d970cb4ad6e85254f41`;
- U03 lineage/blocker correction:
  `VI13R_REVIEW_LINEAGE_AND_U03_BLOCKER_CORRECTION.md`, SHA-256
  `7d4e40b984583c9bb7e83d789d910ffcb385c6b9dbf296f3ba5d7bdc2308b6c5`;
- accepted U03 NativeValueV1 domain authority:
  `VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md`, SHA-256
  `542b06b24c826417e84700a919649da88c26ebb3a25f59c3e4178beb386d02a6`;
- accepted U03 static-envelope clarification:
  `VI13R_U03_NATIVE_VALUE_STATIC_TYPING_CLARIFICATION.md`, SHA-256
  `689c1051ab6f2c03700d1a67e2852995ca9edb6d13d34f336ab039cccc40f6f8`;
- final distribution metadata authority:
  `VI15_L1_FINAL_DISTRIBUTION_AUTHORITY.md`, SHA-256
  `59ad4a66bedeacd89947fae974808d435fd94cf9eb1ef7e9bbeec7797780b4c2`.

The U03 NativeValueV1 domain authority is explicitly marked current human/programme authority and
supersedes the recorded U03 authority blocker; the later static clarification changes only the
representability interpretation, not runtime carrier semantics. The catalogue-carriage authority is
explicitly Programme-authorised and remains provenance-only with respect to provider mapping;
concrete provider mapping remains unresolved.

## 3. Active Git start boundary and external predecessor distinction

The current repository's actual Git root is exactly:

- commit `8133432ba8a07e4d04d83b14af5c3c4bd12e6b0e`;
- tree `2220077c621eb9fef5b9b2cd37377c6926ff148a`;
- subject `Prepare thin Worker 001 VI-08 handoff`.

`git rev-list --max-parents=0 --all` returns that one root. The earlier pre-implementation source
identity recorded by the handoff is:

- commit `d095954c16a9818eadb60d6364148229f2dc4558`;
- tree `7fdb0e5308f3af187134bc3ebf633835748e9475`.

Those earlier objects are **not present in the current object database**. `git cat-file -t` cannot
resolve either object. This is not silently treated as ancestry. Primary VI-08 recovery evidence
states that the supplied Worker transport was intentionally thin and that omitted historical Git
ancestry was not reconstructed; the current run preserves the thin-transport ancestry exactly as
supplied. `GATE_03_WORKER_001_HANDOFF.md` likewise records a visible commit count of one and calls
`d095954...` the genuine external predecessor.

Accordingly the reproducible Git-ancestry claim in this repository begins at `8133432...`. The
external `d095954...` identity remains an exact recorded provenance referent, not a falsely claimed
current Git ancestor. This distinction is part of the VI-17 Tester challenge.

## 4. Architecture admission and durable allocation

Exact accepted VI-08 candidate:

- commit `544624b5e2ede33501335af93be6ee1cafb3d55f`;
- tree `6b870fd8ff2204a603b5619d247ababad578f441`;
- independent Tester Iteration 002: `PASS`, zero findings.

Net VI-08 admission mutation from thin root `8133432...` to the accepted candidate changed the
architecture registries, introduced the M00 package/public seam skeleton, and repaired stale
architecture proof fixtures; it did not implement Raw Signal product decisions.

Current registry/control state was revalidated directly:

- architecture objects: `5`;
- active runtime modules: `1`;
- implementation allocations: `1`;
- admitted architecture/bootstrap test families: `11`;
- promotion sets: `1`;
- dependency/public-seam violations: `0`.

Current durable declarations are:

- active semantic owner: `M00 / raw_signal_occurrence_truth`;
- owner package: `nvda_desk.raw_signal_occurrence_truth`;
- public seam: `nvda_desk.raw_signal_occurrence_truth.api`;
- exactly one implementation allocation: `M00`;
- application shell: `A00 / nvda_desk.composition`;
- declared owner edge: exactly `A00 -> M00`;
- P01 and K01: placeholders, not active runtime allocations;
- PostgreSQL/Psycopg: non-owning technical persistence mechanism;
- one symbol-specific A00 construction exception:
  `nvda_desk.raw_signal_occurrence_truth._postgres.create_postgres_persistence`.

Current structural architecture, dependency-direction and public-seam validators all pass.

## 5. Product and architecture proof lineage

VI-09 accepted control state is commit
`956fab361825acb4a0563803ce03d419997748a1` / tree
`de47a6976be2617f23d17feebeffcbadb13b8ae5`. It established the separate product-proof control
surface before production code.

The final bounded pre-implementation physical-proof candidate reviewed at VI-11 is
`cca84de4ce2e9df52647352237c8a64e52a10db5` / tree
`6b7881fc045345eef357248f4fa8f75f38599923`; Tester Iteration 014 returned `PASS` at continuity
commit `86744106d0c9f868d2c37f24b3d3a155a9d3fe68`, then forward `main` accepted that lineage at
`95c0aeabf3b76316bd32870ffe6c311be8ad1237`.

The current BICP/control surface contains exactly:

- 13 current product obligations: `IA17-PROD-001..008`, repaired successor
  `IA22R01-PROD-009`, and `IA17-PROD-010..013`;
- predecessor `IA17-PROD-009` remains forbidden/non-current;
- six architecture obligations: `IA17-ARCH-001..006`;
- six physical product families, one for each U01-U06 proof boundary;
- 13/13 current product obligations covered;
- 11 separately attributable architecture/bootstrap families in current-blocking
  `architecture_kernel`.

Current product-proof validation passes and reports six families / 13 of 13 obligations /
`READY_FOR_PROOF`. Product and architecture proof remain separate axes.

## 6. U01-U06 accepted implementation/review lineage

All identities below are present and are ancestors of the VI-17 Worker branch:

| Unit | Exact accepted candidate | Independent review | Promotion / accepted forward state |
| --- | --- | --- | --- |
| U01 | `e8b659d7849d2f95b64ba32bed8090a8290358d4` | `4db58e9091083500a2505023a302f36447185029` PASS | `b806447eb440a016826728af075e714beee23d31` |
| U02 | `5c62ec5147da718297b251b5a287405ebf3b4755` | `df45c5e93e7c4c19cb1cca75de5cd1c64b15537c` PASS | `a78ae7b5515c2e482a2656cebeebae3fa5a6d584` |
| U03 | `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf` | `dc40971d24ee773ee133d07622f92d709a7cec11` PASS, after authority clarification `c4caa78...` | `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec` |
| U04 | `dc3b448191a2b2d3528ffb576b1ebc2c56839991` | `dd42d645b59a62f88cfbc7fba47a75e415b7296f` PASS | accepted U04 recovery baseline `50ce8b2d5f84f0e6a0fc4b4c71b6e7b05a2744cb`; U05 plan base `4bf4b4f...` |
| U05 | `2bdbedff62307ecfaf6186f9c12814fb662c11a7` | `9f35df4c1915de78847dfc4a23ce886dfa3b5fd8` PASS | same review identity fast-forwarded to `main` |
| U06 | `8462630277b04d431ad393e2b73039cacb5d6247` | `562767529235cedff77d3e740a259fab9d88716e` PASS | Stage-6 close-out `ed94f745effd65050f03d921ad0ae30769877206` |

The prior abandoned U05/CP line remains historical/`DO_NOT_CARRY_FORWARD`; the active U05 lineage
starts from the accepted U04 recovery baseline under the 2026-09-26 restart plan.

## 7. Changed-path authority audit

The IWO permits VI-12R production mutation under the M owner, bounded A00 construction/composition,
the exact Psycopg dependency, correctness-only PostgreSQL mechanism and evidence/lineage. The
historical execution plans/reviewer routes separately allowed proof-layer repair where an accepted
proof was stale or a reviewer finding required implementation-coupled discrimination.

Net substantive paths from each accepted predecessor to accepted candidate were inspected:

- **U01:** M00 `api.py`; U01 proof and static public-seam specimen only.
- **U02:** M00 `api.py`; U02 proof only.
- **U03:** M00 `api.py`; U03 support/proof/static specimens only, under the later explicit
  NativeValueV1 authority closure.
- **U04:** M00 `api.py`; U04 proof only.
- **U05:** product-proof family record, exact `psycopg[binary]==3.3.4` dependency, private M00
  `_postgres.py`, M00 `api.py`, legacy-dependency bootstrap proof and U05 restart/durability proof.
  The active U05 ExecPlan records the VI-04-bounded PostgreSQL mechanism and restart stages and does
  not reopen U01-U04 meaning.
- **U06:** A00 composition source, the exact A00->M00 technical-constructor dependency exception,
  product-proof family update, relocation of U05 supplemental implementation proofs out of the
  admitted product-family directory, and U06 implementation/product proof. The U06 ExecPlan limits
  production mutation principally to `src/nvda_desk/composition/**` and expressly preserves M00.
- **VI-14:** no `src/**`, `tests/**`, `config/**` or `pyproject.toml` mutation.
- **VI-15-L1:** final metadata consequences only: `pyproject.toml`, package `__version__` and the
  bootstrap version-binding assertion, under explicit Programme Owner metadata authority.
- **VI-15-L2:** no substantive source/test/config/package-metadata mutation relative to its routed
  predecessor.

No accepted candidate introduced P01/K01/DMPV3/provider-network/downstream runtime implementation.

## 8. Authority-mutation audit

For the fixed BICP/IRB/VI-04/IWO/VI-06-owner-direction/implementation-authority-binding paths,
`git log 8133432...HEAD -- <path>` reports zero post-root mutations. The VI-15 distribution authority
has zero changes after its creation in candidate `466055a1...`.

Git history under `implementation/authority` after the thin root was inspected rather than assumed
empty. The material post-root authority additions are the explicitly recorded Programme Owner
catalogue-carriage decision, the U03 recurrence/blocker/domain/static-typing authority sequence, and
the VI-15 distribution metadata decision. No current source/test/config mutation was found that
requires an authority value absent from those records or from the fixed BICP/IRB/VI-04/IWO chain.

**Worker finding:** no unauthorised semantic-authority mutation was identified. This remains subject
to independent Tester reconstruction.

## 9. VI-14 -> VI-16 exact accepted closure lineage

- VI-14 integrated boundary candidate:
  `076f1e979474babbb8985dc87d3b2d4d62ec0b4c` / tree
  `45aec5c01ae8a35fa8879fab978c6fb0f0082140`; Tester PASS
  `79b1d9d1d9da1b921c8d8197d154937dd1a699e5`.
- VI-15-L1 metadata candidate:
  `466055a1cd5fe678a40049a00f0dc88158951d74`; Tester PASS
  `226c5cdebdfa33d5b3d8f43d3eb67b0ae6b8b355`; close-out
  `abccadf20d10daa29e739c6ba54a970fcff41614`.
- VI-15-L2 package candidate:
  `332c1f95da032f841e8779ef21fe3c1fceb698a2` / tree
  `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`; Tester PASS
  `eed5c5f6fa9eeda02886ed8fda0d6205177823e5`; close-out
  `93c1212f113e6cc4f14aca7fb7a2e560f691c38f`.
- VI-16 whole-BICP candidate:
  `9248f3b1788f8e99e59a0482c4cc393c27942715` / tree
  `5560c97ad83a05190603c323eb4fbfa0c21d983d`; Tester PASS
  `9f5f7e90b463365fb39c361f2e346d9e67c6d915`; promotion close-out
  `27d83923dc982b914d898c24a03e10e221c9c2c8`.

Every listed active-history identity from the thin root onward was directly verified as an ancestor
of the current VI-17 Worker branch.

## 10. Code -> package binding

Accepted package artefacts remain:

- wheel `nvda_architecture_kernel-1.0.0-py3-none-any.whl`, 37,378 bytes,
  SHA-256 `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- sdist `nvda_architecture_kernel-1.0.0.tar.gz`, 161,445 bytes,
  SHA-256 `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`.

`SHA256SUMS` was rechecked from the package-artifact directory and both artefacts pass. All 16
tracked Python runtime files under `src/nvda_desk/**/*.py` at exact package candidate `332c1f95...`
were independently compared byte-for-byte with the wheel entries: `16 compared / 0 mismatches`.
The wheel therefore binds the accepted architecture/A00/M00 runtime bytes to the accepted package
candidate. A scoped Git diff from package candidate `332c1f95...` to the VI-17 routed Worker
baseline is empty for `src/**`, `tests/**`, `config/**` and `pyproject.toml`.

## 11. Worker audit conclusion

**VERIFIED observations:**

1. the exact fixed authority hashes currently match their bound identities;
2. the IWO review blocker is preserved truthfully and execution authority is the later Programme
   Owner direction, not an invented PASS;
3. post-IWO semantic authority additions are individually attributable to explicit Programme Owner
   records and are reflected in the proof/implementation lineage;
4. the reproducible active Git history begins at the intentional thin transport root `8133432...`;
5. every active architecture/proof/U01-U06/VI-14/VI-15/VI-16 identity audited from that root is an
   ancestor of the VI-17 Worker state;
6. the current architecture registry/allocation/dependency/seam state matches the admitted M00/A00
   boundary and validators report zero dependency/public-seam violations;
7. current product proof is exactly six families covering 13/13 current obligations, separately
   from six architecture obligations / 11 architecture-bootstrap families;
8. net substantive implementation mutations remain inside the authorised owner/A00/PostgreSQL/
   proof/package jurisdictions identified above;
9. no post-package substantive drift exists in `src/**`, `tests/**`, `config/**` or `pyproject.toml`;
10. the accepted wheel hashes verify and all 16 wheel Python runtime files match the exact package
    candidate source bytes.

**Important provenance boundary:** the recorded external predecessor `d095954...` is not available as
a Git object in this thin active repository and is therefore not claimed as a current ancestor. The
intentional omission is itself recorded by the original VI-08 handoff/recovery evidence. The
independent Tester must decide whether the exact embedded authority plus explicit thin-transport
bridge is sufficient for VI-17-L1 acceptance; the Worker does not conceal or upgrade that boundary.

**WORKER CONCLUSION:** `NO_MATERIAL_AUTHORITY_OR_LINEAGE_GAP_IDENTIFIED_BY_WORKER_AUDIT`.

This is a Worker conclusion only. Fresh independent VI-17-L1 Tester reconstruction is mandatory.
VI-17-L2 must not begin before Tester PASS and preserved-ancestry promotion of the accepted
VI-17-L1 candidate.
