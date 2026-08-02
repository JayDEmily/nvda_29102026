# NVDA Divergent Worker Branch Comparative Audit

**Audit date:** 2026-08-02  
**Decision:** retain `work/post-alpha-comprehensive-debt-retirement-v1` at `617127f6cb35` as the continuation base. Treat `work/pre-m00-novel-assurance-redo-v3` at `fffb4e31c03a` as an assurance donor.  
**Current gate:** the continuation branch is materially more advanced, but its claim that repository-resolvable debt is retired is **not supported by the complete physical test estate**.

## 1. Direct answer

The **post-alpha comprehensive-debt-retirement branch is more advanced**. It has passed M00 final composition and added later application composition, transport, upstream workflow, durable-state, operational-boundary and Tier C work that does not exist on the assurance branch. Its branch history changes 74 source files (+4,179/-748) after the common ancestor, compared with 17 source files (+289/-134) on the assurance branch.

The **pre-M00 novel-assurance branch is stronger as an assurance and defect-discovery path**. It deliberately stops before M00, but its complete test estate is reconciled and it found several defects still present in the advanced branch.

Therefore:

1. **Do not switch bases and do not merge the assurance branch wholesale.** That would discard or destabilise valid later delivery.
2. **Reopen the advanced branch’s closeout status.** Its selected `alpha_current` gate is green, but the complete physical Tier A estate is red.
3. **Port the donor’s assurance repairs and methods into the advanced branch one semantic unit at a time.** One donor unit has already been port-checked successfully in a disposable copy.

## 2. Scope and method

Inspected both full-history repositories, including root instructions, `PROJECT_EXECUTION_METHOD.md`, `PLANS.md`, live roadmaps, canonical ExecPlans, branch histories, divergent diffs, relevant normative documents, affected source/tests and worker evidence. No original repository was mutated.

Repository authority requires material claims to be backed by paths, lines, command output or artefacts and states that passing tests alone is not correctness proof (`AGENTS.md:97-102`, `127-148`). It also places normative intent above tests and implementation (`AGENTS.md:141-148`). This audit therefore compared behaviour, authority, test completeness and branch history rather than commit count alone.

## 3. Common baseline and divergence

| Item | Advanced implementation path | Assurance path |
|---|---|---|
| Branch | `work/post-alpha-comprehensive-debt-retirement-v1` | `work/pre-m00-novel-assurance-redo-v3` |
| HEAD | `617127f6cb354591a875985788552360e72fd392` | `fffb4e31c03a3bc031f28eba89f9a59562484a8f` |
| Latest common ancestor | `258470526c36da61b3ff4162f1d5ad9e512a8b54` | `258470526c36da61b3ff4162f1d5ad9e512a8b54` |
| Unique commits after ancestor | 40 | 26 |
| Changed entries | 241 | 338 |
| Source change | 74 files; +4,179/-748 | 17 files; +289/-134 |
| Test change | 108 files | 32 direct `tests/` entries, plus rename entries |
| Control/evidence emphasis | 37 `project_control/` files | 279 `project_control/` files |

### Advanced path taken

The advanced worker first repaired promotion/test controls, then implemented M00, final alpha consolidation, transport routing and broad post-alpha debt work. Its own live roadmap declares comprehensive debt retirement and no active slice (`A:ROADMAP_LEDGER_V2.md:5-14`). The canonical plan records M00 final composition and a 754-test aggregate at that earlier point (`A:project_control/canonical_project_manager/EXEC_PLAN.md:237-242`), followed by final alpha consolidation (`:346-360`). The later debt summary records raw-source-to-M03 composition, M06 owner facts, SQLite restart, operational boundaries, Tier C and vocabulary adjudication (`A:.../post_alpha_comprehensive_debt_retirement_20260802/VALIDATION_SUMMARY.md:23-89`).

### Assurance path taken

The assurance worker deliberately did not begin M00. It repaired and reran the pre-M00 estate, then left M00 as the next unit (`B:project_control/canonical_project_manager/EXEC_PLAN.md:323-333`). It reproduced process-wide policy mutability, proof-admission gaps, projection-header self-observation and unresolved vocabulary occurrences (`B:.../NOVEL_ASSURANCE_FINAL_RESULTS.md:7-26`), then executed isolated physical, order, import, graph, replay, boundary, state and proof-control checks (`:28-59`).

## 4. Comparative result

### 4.1 Delivery advancement

**Winner: advanced implementation path.**

This is not close. The assurance branch explicitly says M00 has not started (`B:.../EXEC_PLAN.md:331-333`), while the advanced branch contains M00 and several post-alpha implementation slices. Commit/line volume is not acceptance proof, but here the actual source surfaces and accepted sequencing establish genuine later delivery.

### 4.2 Current assurance state

| Validation | Advanced path | Assurance path |
|---|---:|---:|
| Curated current promotion | **PASS** — 19/19 blocks, 802 tests | Not applicable to later M00 state |
| Complete physical Tier A | **1,713 passed; 247 failed; 1,960 total** | **1,910 passed; 0 failed** |
| Physical Tier B | **90/90 passed** | **51/51 passed** |
| Failing Tier A partitions | 8 of 44 | 0 of 42 |
| Independent proof-control join | 32 unadmitted physical files | 0 unadmitted physical files |
| Exact module graph | 261 modules; 417 edges; 0 implementation cycles/unresolved imports | 250 modules; 394 edges; 0 implementation cycles/unresolved imports |
| Fresh imports | 258/258 forward and reverse | 247/247 forward and reverse |
| Boundary mutation | lawful control accepted; 17 forged mutations rejected | same result class |
| Replay/serialization | 13 models; no recorded failures | 13 models; no failures |

The advanced branch’s curated gate genuinely passes; this audit independently reran it. The problem is scope. Its authority checker reports 201 families, 203 paths and 73 blocks as internally consistent, while the broader physical-file/registry/proof join finds 32 physical test files outside admission. The selected gate cannot support a repository-wide debt-retirement claim.

The 247 failures are concentrated rather than random:

| Partition | Failed | Passed | Dominant failure signal |
|---|---:|---:|---|
| runtime | 143 | 6 | caller-owned `scenarioid` missing from older FWD012 routes |
| packets | 52 | 290 | caller-owned scenario/trace/module identity and stale FWD004 carriage |
| normative_authority | 22 | 31 | absent/stale contract surfaces and persistence transaction expectations |
| parallel_risk | 19 | 84 | forbidden legacy `parallel_risk_bootstrap_input` role and scenario identity |
| testing_harnesses | 4 | 7 | same parallel-risk role/identity drift |
| persistence | 3 | 195 | caller-owned scenario identity |
| upstream_cognition | 3 | 67 | prepared-context module/scenario identity |
| capital_deployment | 1 | 25 | unadmitted `capital_deployment_decision` packet role |

This pattern means the advanced branch is not generally broken. It has unresolved authority/test reconciliation after later identity and packet-law changes.

## 5. Donor lessons still applicable to the advanced branch

### 5.1 Confirmed defects or unresolved conflicts

1. **Nineteen caller-mutable governed policy constants.** The donor expected-red test fails 19/19 against the advanced branch. The test enumerates the exact constants and mutation probes (`B:tests/tier_a/normative_authority/test_governed_module_policy_constants_are_immutable.py:8-57`). The donor repair froze these without changing governed values (`B:.../STATE_POLICY_IMMUTABILITY_REPAIR.md:5-15`).

2. **Vocabulary projection self-observation.** The advanced scanner excludes only `Projection metadata` and `Projection document notes` (`A:src/nvda_desk/vocabulary_synonym_audit.py:171-205`). The donor excludes schema-version, registry-version and namespace-scope machine headers as well (`B:src/nvda_desk/vocabulary_synonym_audit.py:179-213`). The donor expected-red test fails on the advanced branch. Consequently, the advanced branch’s zero-candidate result is not sufficient until the scanner is repaired and current dispositions are rechecked. The number of current dispositions that would become unnecessary is **Unknown**.

3. **Forbidden M12→M10 runtime dependency.** The advanced branch imports `semantic_fingerprint` from M10 in both M12 contracts and service (`A:src/nvda_desk/m12_evidence_replay/contracts.py:11`; `A:src/nvda_desk/m12_evidence_replay/service.py:9`). The donor localises deterministic fingerprint ownership inside M12 (`B:src/nvda_desk/m12_evidence_replay/contracts.py:27-40` onward).

4. **API/default identity authority conflict.** The advanced API still manufactures inventory, placement, capital, risk, decision, evaluation and replay IDs and stores veto/risk events in process memory (`A:src/nvda_desk/api/app.py:278-304`, `325`, `351`, `376-390`). It also exposes those event routes (`:441-444`) and retains `walk_forward_authority_default` (`A:src/nvda_desk/analysis/replay/walk_forward.py:256-269`). Current M00 authority forbids hidden defaults and mutable domain state (`A:docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:517-526`). This requires semantic adaptation to the later M00 transport design, not blind cherry-picking.

5. **Generic M01 `typed_payload`.** The advanced contract admits `dict[str, Any]` (`A:src/nvda_desk/m01_source_admission/contracts.py:163-181`); the donor requires a concrete Pydantic model (`B:.../contracts.py:170-188`). The donor principle remains sound, but the advanced M01 service, M00 tests and Tier C currently pass dictionaries, so this is a multi-surface redesign rather than a one-line port.

6. **Prepared-context owner identity.** The advanced builder lacks module version, module instance, derivation and owner validators (`A:src/nvda_desk/preparation/context_packet.py:73-123`). The donor unit adds them (`B:.../context_packet.py:73-150`). The full donor source+test unit applied cleanly in a disposable copy and changed the entire advanced `upstream_cognition` partition to **71/71 passed**.

7. **Proof admission completeness.** The donor’s method found and closed 29 gaps at its state (`B:.../PROOF_CONTROL_ADMISSION_REVIEW.md:5-12`). Applied to the advanced tree, the same join finds 32 current gaps. The old registry rows must not be imported; each current file must be read and admitted, superseded or retired against current authority.

### 5.2 Reusable assurance methods

The donor’s physical partition runner, order-invariance runner, exact AST graph, fresh-import, replay, boundary-mutation, state and proof-control join instruments are reusable. They already ran successfully against the advanced branch, except that the physical and proof-completeness checks exposed the red estate. The generic state census did not detect the 19 uppercase mutable policy tables; retain the donor’s targeted mutation test alongside it.

## 6. Integration recommendation

Use the advanced branch as the base and open one bounded **post-divergence assurance-reconciliation unit**. Recommended order:

1. **Correct the status boundary.** Do not call repository debt retired while complete physical Tier A and proof admission are red. Preserve the valid M00/post-alpha implementation claims separately.
2. **Port prepared-context identity first.** It is the only donor repair already proven to apply cleanly and restore a complete failing partition. Reapply source+tests without importing historical audit evidence.
3. **Repair policy immutability.** Add the donor expected-red test, freeze all 19 containers, and run every affected owner suite plus vocabulary.
4. **Repair vocabulary instrumentation before touching dispositions.** Port line-wise traversal and all five governed projection-header exclusions; rerun the current global and namespace scans; adjudicate only surviving current candidates.
5. **Remove M12→M10 ownership leakage.** Localise fingerprinting in M12 and rerun M10/M12, graph, replay and serialization checks.
6. **Resolve API and walk-forward fabricated/default identity.** Adapt the donor decision to current M00 transport contracts; do not restore legacy service-locator or mutable event authority.
7. **Decide and execute the typed-ingress migration atomically.** Update M01 contract, service, M00 upstream composition, fixtures and Tier C together.
8. **Reconcile the remaining physical failures by authority family.** Packet roles and caller-owned identity first, then normative legacy surfaces. Do not weaken current identity law merely to turn old tests green.
9. **Read and adjudicate all 32 unadmitted physical files.** Update proof authority only after semantic review.
10. **Close only when both gates pass:** curated `alpha_current` and the complete isolated physical Tier A/B estate, with zero unadmitted physical files and clean graph/import/replay/boundary/state/vocabulary checks.

The detailed item-by-item treatment is in `salvage_inventory.csv`. Patch applicability is recorded in `evidence/patch_applicability.tsv`; clean application does not equal semantic acceptance.

## 7. Git and mutation state

- Original advanced repository: clean at `617127f6cb354591a875985788552360e72fd392` on `work/post-alpha-comprehensive-debt-retirement-v1`.
- Original assurance repository: clean at `fffb4e31c03a3bc031f28eba89f9a59562484a8f` on `work/pre-m00-novel-assurance-redo-v3`.
- No merge, cherry-pick, commit or working-tree mutation was made to either original repository.
- Disposable copies were used for independent testing and port checks.
- The prepared-context donor port check changed only a disposable copy.

## 8. Open Unknowns

- Which of the advanced branch’s 247 failures represent tests that should be updated versus absent implementation must be decided family-by-family from current normative authority. Failure clustering strongly indicates substantial stale-fixture/route work, but not every failure is thereby dismissed.
- The exact number of the advanced branch’s 593 vocabulary dispositions made unnecessary by projection-header self-observation is unknown until the scanner is repaired and the current tree is rerun.
- The API authority repair needs a current M00-aware semantic design review; the donor’s earlier code cannot be assumed to be the final shape.
- Full current order-invariance of all 1,960 advanced Tier A tests was not run because the physical estate is already red; run it after reconciliation.

## 9. Evidence files

- `validation_summary.json` — machine-readable branch and validation summary.
- `progress_quality_matrix.csv` — side-by-side decision matrix.
- `salvage_inventory.csv` — donor item classification and recommended use.
- `advanced_branch_physical_tier_a.tsv` — all 44 advanced Tier A partition results.
- `advanced_branch_unadmitted_physical_tests.txt` — exact 32-file gap list.
- `evidence/` — selected independent command outputs and JSON instruments.
- `donor_patches/` — audit-only patch exports used for applicability checks; not an authorised integration.
