# PRL Tranche Final Audit Mainline Command Log

## Initial state commands
```bash
git status --short
?? var/audit/prl_tranche_final_audit_mainline_001/
git branch --show-current
work/prl-blocked-leaves-completion
git log --oneline --decorate -n 40
e58a624 (HEAD -> work/prl-blocked-leaves-completion) PRL-MRP-013: reconcile PRL VIX thresholds through governed config
47857ca PRL-MRP-020: handle unavailable PRL signals from typed inventory
4c78d40 PRL-MRP-009: promote PRL signal inventory to typed runtime config
f2aa50e PRL-MRP-007: create governed signal inventory workbook tab
a7962ee (work/repo-freeze-ledger-audit-handoff) Close repo freeze ledger audit handoff
878c1cc Freeze repo state and audit roadmap ledger for handoff
c477e6a (work/prl-minute-risk-profile-execution-batch-001) PRL execution batch 001: closeout artefacts
10fac49 PRL-MRP-027: document deferred rich signal-family intake
caa54b5 PRL-MRP-026: update PRL roadmap and current-state docs
79a6896 PRL-MRP-025: add deterministic PRL description renderer
abefc5d PRL-MRP-024: add deterministic description contract
c4f0af0 PRL-MRP-023: document vocabulary-governed description constraints
737fba4 PRL-MRP-022: harden enriched authority regression tests
d912a27 PRL-MRP-021: complete minute profile lineage
0c8a4a4 PRL-MRP-020: mark inventory-backed unavailable signals blocked
0de59b7 PRL-MRP-019: add optional minute profile service path
6800fff PRL-MRP-018: add minute profile assembly
d3af38d PRL-MRP-017: add risk family aggregation
9d1add2 PRL-MRP-016: harden atom no-play authority tests
bcbdce1 PRL-MRP-015: add supported risk atom skeleton
2d10c3f PRL-MRP-014: preserve options DTE repricing caution
e17860c PRL-MRP-013: mark VIX reconciliation blocked
9dcce10 PRL-MRP-012: preserve VIX threshold compatibility
cb94296 PRL-MRP-011: preserve scheduled event caution
4d662dc PRL-MRP-010: add event proximity register
64ba82b PRL-MRP-009: mark runtime inventory promotion blocked
ff6a50f PRL-MRP-008: plan signal inventory typed promotion
a395841 PRL-MRP-007: mark workbook tab creation blocked
bd8e197 PRL-MRP-006: document signal inventory workbook tab
e773aad PRL-MRP-005: add unavailable signal handling foundation
00ee669 PRL-MRP-004: add missing signal register helpers
08511fc PRL-MRP-003: add freshness register calculation
a122379 (work/prl-minute-risk-profile-architecture-decisions) Plan PRL architecture decisions
3c5b1db (work/prl-minute-risk-profile-master-roadmap) Plan PRL minute risk profile master roadmap
528af6c Add PRL minute risk profile master roadmap ledger entry
7eb107f (work/prl-minute-profile-contracts) Record PRL contracts archive command
59b1202 Close out PRL minute profile contract leaf
e66ea53 Implement PRL minute profile contract models
656d1fd Add PRL minute profile contract tests
a1d27a2 Record PRL minute profile contract leaf governance
git branch --list
  main
* work/prl-blocked-leaves-completion
  work/prl-minute-profile-contracts
  work/prl-minute-risk-profile-architecture-decisions
  work/prl-minute-risk-profile-execution-batch-001
  work/prl-minute-risk-profile-master-roadmap
  work/prl-minute-risk-profile-plan
  work/repo-freeze-ledger-audit-handoff
  worker/fwd-003-through-fwd-009-closure-continuation
  worker/fwd006-fwd008-closure-20260514
  worker/fwd006-fwd008-forensic-audit-20260514
  worker/fwd006-ordered-replay-20260514
  worker/vocabulary-suppression-removal-20260514
```
## premerge_git_diff_check
```bash
git diff --check
```
- premerge_git_diff_check exit_code=0
## premerge_scaffold_check
```bash
make scaffold-check
```
- premerge_scaffold_check exit_code=0
## premerge_parallel_risk_pytest
```bash
env PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/parallel_risk -q
```
- premerge_parallel_risk_pytest exit_code=0
## premerge_proof_parallel_risk_lane_authority_surface
```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/run_proof_block.py --block parallel_risk_lane_authority_surface
```
- premerge_proof_parallel_risk_lane_authority_surface exit_code=0
## premerge_targeted_prl_inventory_vix
```bash
env PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_governance.py tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py tests/tier_a/vocabulary/test_parallel_risk_description_vocabulary_constraints.py -q
```
- premerge_targeted_prl_inventory_vix exit_code=0
## Gate summaries
- Gate 1 PRL-MRP reconciliation: PASS; see LEAF_RECONCILIATION.md.
- Gate 2 formerly blocked leaves deep audit: PASS; see LEAF_RECONCILIATION.md and deep_audit_probe.log.
- Gate 3 pre-merge validation: PASS; see VALIDATION_SUMMARY.md.
- Gate 4 branch hygiene: PASS pending audit commit; see BRANCH_HYGIENE.md.
- Gate 5 ledger finalisation: PRL_TRANCHE_READY_FOR_MAINLINE recorded in ROADMAP_LEDGER.md.
## Gate 6 merge to main
```bash
$ git status --short
 M var/audit/prl_tranche_final_audit_mainline_001/COMMAND_LOG.md
$ git checkout main
$ git status --short
 M var/audit/prl_tranche_final_audit_mainline_001/COMMAND_LOG.md
?? var/audit/prl_tranche_final_audit_mainline_001/merge_to_main.log
$ git log --oneline --decorate -n 20
3068c50 (HEAD -> work/prl-blocked-leaves-completion) Audit PRL tranche completion before mainline integration
e58a624 PRL-MRP-013: reconcile PRL VIX thresholds through governed config
47857ca PRL-MRP-020: handle unavailable PRL signals from typed inventory
4c78d40 PRL-MRP-009: promote PRL signal inventory to typed runtime config
f2aa50e PRL-MRP-007: create governed signal inventory workbook tab
a7962ee (work/repo-freeze-ledger-audit-handoff) Close repo freeze ledger audit handoff
878c1cc Freeze repo state and audit roadmap ledger for handoff
c477e6a (work/prl-minute-risk-profile-execution-batch-001) PRL execution batch 001: closeout artefacts
10fac49 PRL-MRP-027: document deferred rich signal-family intake
caa54b5 PRL-MRP-026: update PRL roadmap and current-state docs
79a6896 PRL-MRP-025: add deterministic PRL description renderer
abefc5d PRL-MRP-024: add deterministic description contract
c4f0af0 PRL-MRP-023: document vocabulary-governed description constraints
737fba4 PRL-MRP-022: harden enriched authority regression tests
d912a27 PRL-MRP-021: complete minute profile lineage
0c8a4a4 PRL-MRP-020: mark inventory-backed unavailable signals blocked
0de59b7 PRL-MRP-019: add optional minute profile service path
6800fff PRL-MRP-018: add minute profile assembly
d3af38d PRL-MRP-017: add risk family aggregation
9d1add2 PRL-MRP-016: harden atom no-play authority tests
```
- checkout exit code: 1
- merge exit code: 99
## Gate 6 retry preparation
- Initial checkout failed because command-log mutation after the audit commit made the branch dirty; this was retained as audit evidence and the audit commit was amended before retry.
## Gate 6 merge to main retry result
## Gate 6 merge to main retry
$ git status --short
$ git checkout main
Switched to branch 'main'
checkout_exit_code=0
$ git merge --no-ff work/prl-blocked-leaves-completion -m "Merge PRL tranche completion"
Merge made by the 'ort' strategy.
 NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md           |    2 +-
 ROADMAP_LEDGER.md                                  | 1166 ++++++++
 config/parallel_risk_lane_profile.v1.yaml          |   21 +
 config/parallel_risk_signal_inventory.v1.yaml      |  460 ++++
 data/parallel_risk/description_templates.v1.json   |   13 +
 ...VDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx |  Bin 112232 -> 116946 bytes
 data/vocabulary/canonical_vocabulary.json          |   33 +-
 data/vocabulary/vocabulary_touch_stamp.json        |    2 +-
 .../PRL_DEFERRED_RICH_SIGNAL_FAMILY_INTAKE_PLAN.md |   30 +
 ...L_MINUTE_RISK_PROFILE_ARCHITECTURE_DECISIONS.md |  353 +++
 .../PRL_MINUTE_RISK_PROFILE_IMPLEMENTATION_PLAN.md |  252 ++
 .../PRL_MINUTE_RISK_PROFILE_MASTER_ROADMAP.md      |  324 +++
 .../PRL_RISK_DESCRIPTION_VOCABULARY_CONSTRAINTS.md |   31 +
 .../PRL_SIGNAL_INVENTORY_PROMOTION_PLAN.md         |   45 +
 .../PRL_SIGNAL_INVENTORY_WORKBOOK_TAB_SPEC.md      |   60 +
 src/nvda_desk/config/parallel_risk_lane_profile.py |   30 +
 .../config/parallel_risk_signal_inventory.py       |   43 +
 src/nvda_desk/contracts/parallel_risk.py           |  426 +++
 .../parallel_risk/deterministic_description.py     |   87 +
 .../domain/parallel_risk/environment_assessment.py |   35 +-
 .../domain/parallel_risk/event_proximity.py        |   33 +
 .../domain/parallel_risk/family_aggregation.py     |   53 +
 src/nvda_desk/domain/parallel_risk/freshness.py    |   77 +
 .../parallel_risk/minute_profile_assembly.py       |  158 ++
 .../domain/parallel_risk/missing_signals.py        |   74 +
 src/nvda_desk/domain/parallel_risk/risk_atoms.py   |  123 +
 .../domain/parallel_risk/unavailable_signals.py    |  219 ++
 .../services/parallel_risk_lane_service.py         |   20 +-
 src/nvda_desk/vocabulary_builder.py                |   25 +-
 .../test_parallel_risk_atom_authority_semantics.py |   72 +
 .../test_parallel_risk_description_contract.py     |   48 +
 .../test_parallel_risk_description_templates.py    |   92 +
 ..._parallel_risk_enriched_authority_regression.py |   68 +
 .../test_parallel_risk_event_proximity_register.py |   71 +
 .../test_parallel_risk_family_aggregation.py       |   37 +
 .../test_parallel_risk_freshness_register.py       |   59 +
 ...el_risk_inventory_backed_unavailable_signals.py |  108 +
 .../test_parallel_risk_lineage_completeness.py     |   91 +
 .../test_parallel_risk_minute_profile_assembly.py  |   83 +
 .../test_parallel_risk_minute_profile_contracts.py |  224 ++
 ...llel_risk_minute_profile_service_integration.py |   50 +
 .../test_parallel_risk_missing_signal_register.py  |   70 +
 .../test_parallel_risk_options_dte_preservation.py |   33 +
 ...t_parallel_risk_scheduled_event_preservation.py |   37 +
 ...est_parallel_risk_signal_inventory_promotion.py |  119 +
 ...test_parallel_risk_signal_inventory_workbook.py |  130 +
 .../test_parallel_risk_supported_risk_atoms.py     |   93 +
 .../test_parallel_risk_unavailable_signals.py      |   39 +
 .../test_parallel_risk_vix_threshold_governance.py |  105 +
 ...est_parallel_risk_vix_threshold_preservation.py |   40 +
 ...llel_risk_description_vocabulary_constraints.py |   29 +
 .../ARTIFACT_MANIFEST.md                           |   26 +
 .../prl_architecture_decisions_001/COMMAND_LOG.md  |   61 +
 .../FULL_READ_MANIFEST.md                          |  137 +
 .../git_diff_check.txt                             |    0
 .../prl-architecture-decisions.patch               |  773 ++++++
 .../scaffold_check.txt                             |    1 +
 .../ARTIFACT_MANIFEST.md                           |   27 +
 .../COMMAND_LOG.md                                 |   78 +
 .../FULL_READ_MANIFEST.md                          |   65 +
 .../final_broad_pytest.log                         |    5 +
 .../final_diff_check.log                           |    2 +
 .../final_financial_calendar_pytest.log            |    4 +
 .../final_parallel_risk_pytest.log                 |    5 +
 .../final_scaffold_check.log                       |    3 +
 .../final_temporal_pytest.log                      |    4 +
 .../final_testing_harnesses_pytest.log             |    4 +
 .../final_upstream_cognition_pytest.log            |    4 +
 .../final_upstream_signal_pytest.log               |    4 +
 .../final_vocabulary_pytest.log                    |    4 +
 .../final_vocabulary_pytest_after_admission.log    |    4 +
 ...nal_vocabulary_test_dmp_v3_vocabulary_terms.log |    4 +
 ...ry_test_financial_calendar_vocabulary_terms.log |    4 +
 ...lel_risk_description_vocabulary_constraints.log |    4 +
 ...ry_test_parallel_risk_lane_vocabulary_terms.log |    4 +
 ...cabulary_candidate_admission_plan_contracts.log |    2 +
 ...ry_candidate_admission_plan_contracts_retry.log |    5 +
 ...bulary_candidate_admission_review_contracts.log |    4 +
 ...cabulary_candidate_classification_contracts.log |    4 +
 ...test_vocabulary_candidate_payload_contracts.log |    4 +
 ...t_vocabulary_candidate_review_cli_contracts.log |    3 +
 ..._candidate_review_cli_contracts_final_retry.log |    5 +
 ...bulary_candidate_review_cli_contracts_retry.log |    3 +
 ..._test_vocabulary_candidate_schema_contracts.log |    4 +
 ...ry_test_vocabulary_canonical_builder_parity.log |    4 +
 ...ulary_test_vocabulary_document_json_helpers.log |    4 +
 ...ulary_test_vocabulary_json_helper_contracts.log |    4 +
 ...ary_test_vocabulary_required_baseline_terms.log |    2 +
 ...st_vocabulary_required_baseline_terms_retry.log |    5 +
 ...ulary_test_vocabulary_schema_contract_retry.log |    5 +
 ...ary_synonym_candidate_audit_after_admission.log |    5 +
 ...vocabulary_workflow_surface_after_admission.log |    5 +
 ...lary_test_vocabulary_workflow_surface_retry.log |    2 +
 .../patch_sha256.log                               |    1 +
 .../prl-blocked-leaves-completion.patch            | 2662 ++++++++++++++++++
 .../prl_mrp_007_diff_check.log                     |    0
 .../prl_mrp_007_pytest.log                         |    4 +
 .../prl_mrp_009_diff_check.log                     |    0
 .../prl_mrp_009_pytest.log                         |    4 +
 .../prl_mrp_013_diff_check.log                     |    0
 .../prl_mrp_013_pytest.log                         |    4 +
 .../prl_mrp_020_diff_check.log                     |    0
 .../prl_mrp_020_pytest.log                         |    4 +
 ..._block_parallel_risk_lane_authority_surface.log |   79 +
 ...vocabulary_governance_conformance_candidate.log |   26 +
 .../vocabulary_synonym_audit_final.log             |    3 +
 .../prl_execution_batch_001/ARTIFACT_MANIFEST.md   |   26 +
 var/audit/prl_execution_batch_001/COMMAND_LOG.md   |   12 +
 .../prl_execution_batch_001/FULL_READ_MANIFEST.md  |   45 +
 .../git_diff_check_final.txt                       |    0
 .../git_diff_check_prl_mrp_003.txt                 |    0
 .../git_diff_check_prl_mrp_004.txt                 |    0
 .../git_diff_check_prl_mrp_005.txt                 |    0
 .../git_diff_check_prl_mrp_006.txt                 |    0
 .../git_diff_check_prl_mrp_007_blocked.txt         |    0
 .../git_diff_check_prl_mrp_008.txt                 |    0
 .../git_diff_check_prl_mrp_009_blocked.txt         |    0
 .../git_diff_check_prl_mrp_010.txt                 |    0
 .../git_diff_check_prl_mrp_011.txt                 |    0
 .../git_diff_check_prl_mrp_012.txt                 |    0
 .../git_diff_check_prl_mrp_013_blocked.txt         |    0
 .../git_diff_check_prl_mrp_014.txt                 |    0
 .../git_diff_check_prl_mrp_015.txt                 |    0
 .../git_diff_check_prl_mrp_016.txt                 |    0
 .../git_diff_check_prl_mrp_017.txt                 |    0
 .../git_diff_check_prl_mrp_018.txt                 |    0
 .../git_diff_check_prl_mrp_019.txt                 |    0
 .../git_diff_check_prl_mrp_020_blocked.txt         |    0
 .../git_diff_check_prl_mrp_021.txt                 |    0
 .../git_diff_check_prl_mrp_022.txt                 |    0
 .../git_diff_check_prl_mrp_023.txt                 |    0
 .../git_diff_check_prl_mrp_024.txt                 |    0
 .../git_diff_check_prl_mrp_025.txt                 |    0
 .../git_diff_check_prl_mrp_025_rerun.txt           |    0
 .../git_diff_check_prl_mrp_026.txt                 |    0
 .../git_diff_check_prl_mrp_027.txt                 |    0
 .../prl-execution-batch-001.patch                  | 2860 ++++++++++++++++++++
 .../prl_execution_batch_001/pytest_prl_mrp_003.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_004.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_005.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_006.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_010.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_011.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_012.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_014.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_015.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_016.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_017.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_018.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_019.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_021.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_022.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_023.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_024.txt |    2 +
 .../prl_execution_batch_001/pytest_prl_mrp_025.txt |   62 +
 .../pytest_prl_mrp_025_rerun.txt                   |    2 +
 .../pytest_relevant_final.txt                      |    3 +
 .../scaffold_check_final.txt                       |    1 +
 .../scaffold_check_prl_mrp_006.txt                 |    1 +
 .../scaffold_check_prl_mrp_008.txt                 |    1 +
 .../scaffold_check_prl_mrp_026.txt                 |    1 +
 .../scaffold_check_prl_mrp_027.txt                 |    1 +
 .../prl_master_roadmap_001/ARTIFACT_MANIFEST.md    |   32 +
 var/audit/prl_master_roadmap_001/COMMAND_LOG.md    |   43 +
 .../prl_master_roadmap_001/FULL_READ_MANIFEST.md   |   94 +
 .../prl_master_roadmap_001/git_diff_check.txt      |    0
 .../git_diff_check_final.txt                       |    0
 .../prl-master-roadmap.patch                       |  304 +++
 .../prl_master_roadmap_001/scaffold_check.txt      |    1 +
 .../ARTIFACT_MANIFEST.md                           |   31 +
 .../COMMAND_LOG.md                                 |   76 +
 .../FULL_READ_MANIFEST.md                          |   10 +
 .../git_diff_check.txt                             |    0
 .../git_diff_check_closeout.txt                    |    0
 .../prl-minute-profile-contracts.patch             |  998 +++++++
 .../pytest_parallel_risk_contracts.txt             |    2 +
 .../vocabulary_search.txt                          |  202 ++
 .../ARTIFACT_MANIFEST.md                           |   31 +
 .../COMMAND_LOG.md                                 |   44 +
 .../FULL_READ_MANIFEST.md                          |   56 +
 .../prl-minute-risk-profile-plan.patch             |  234 ++
 .../ARTIFACT_MANIFEST.md                           |   18 +
 .../BRANCH_HYGIENE.md                              |   12 +
 .../COMMAND_LOG.md                                 |  129 +
 .../FULL_READ_MANIFEST.md                          |  151 ++
 .../LEAF_RECONCILIATION.md                         |   46 +
 .../VALIDATION_SUMMARY.md                          |   16 +
 .../branch_hygiene_raw.log                         |  102 +
 .../deep_audit_probe.log                           |   24 +
 .../merge_to_main.log                              |    7 +
 .../premerge_git_diff_check.log                    |    1 +
 .../premerge_parallel_risk_pytest.log              |    4 +
 ..._proof_parallel_risk_lane_authority_surface.log |   77 +
 .../premerge_scaffold_check.log                    |    2 +
 .../premerge_targeted_prl_inventory_vix.log        |    3 +
 .../ARCHIVE_RECONCILIATION.md                      |   12 +
 .../ARTIFACT_MANIFEST.md                           |   27 +
 .../BRANCH_RECONCILIATION.md                       |   10 +
 .../COMMAND_LOG.md                                 |  180 ++
 .../FULL_READ_MANIFEST.md                          |  130 +
 .../LEDGER_AUDIT_SUMMARY.md                        |   55 +
 .../branches_initial.txt                           |   12 +
 .../current_branch_initial.txt                     |    1 +
 .../full_read_manifest_wc.txt                      |    1 +
 .../git_diff_check.txt                             |    0
 .../git_diff_stat_post_first_commit.txt            |    0
 .../git_log_all_initial.txt                        |   80 +
 .../git_status_initial.txt                         |    1 +
 .../git_status_post_first_commit.txt               |    1 +
 .../mnt_data_files_initial.txt                     |   21 +
 .../repo-freeze-ledger-audit-handoff.patch         |  673 +++++
 .../scaffold_check.txt                             |    1 +
 .../tags_initial.txt                               |    0
 var/vocabulary/synonym_candidates.json             |    4 +-
 214 files changed, 16959 insertions(+), 26 deletions(-)
 create mode 100644 config/parallel_risk_lane_profile.v1.yaml
 create mode 100644 config/parallel_risk_signal_inventory.v1.yaml
 create mode 100644 data/parallel_risk/description_templates.v1.json
 create mode 100644 docs/planning/PRL_DEFERRED_RICH_SIGNAL_FAMILY_INTAKE_PLAN.md
 create mode 100644 docs/planning/PRL_MINUTE_RISK_PROFILE_ARCHITECTURE_DECISIONS.md
 create mode 100644 docs/planning/PRL_MINUTE_RISK_PROFILE_IMPLEMENTATION_PLAN.md
 create mode 100644 docs/planning/PRL_MINUTE_RISK_PROFILE_MASTER_ROADMAP.md
 create mode 100644 docs/planning/PRL_RISK_DESCRIPTION_VOCABULARY_CONSTRAINTS.md
 create mode 100644 docs/planning/PRL_SIGNAL_INVENTORY_PROMOTION_PLAN.md
 create mode 100644 docs/planning/PRL_SIGNAL_INVENTORY_WORKBOOK_TAB_SPEC.md
 create mode 100644 src/nvda_desk/config/parallel_risk_lane_profile.py
 create mode 100644 src/nvda_desk/config/parallel_risk_signal_inventory.py
 create mode 100644 src/nvda_desk/domain/parallel_risk/deterministic_description.py
 create mode 100644 src/nvda_desk/domain/parallel_risk/event_proximity.py
 create mode 100644 src/nvda_desk/domain/parallel_risk/family_aggregation.py
 create mode 100644 src/nvda_desk/domain/parallel_risk/freshness.py
 create mode 100644 src/nvda_desk/domain/parallel_risk/minute_profile_assembly.py
 create mode 100644 src/nvda_desk/domain/parallel_risk/missing_signals.py
 create mode 100644 src/nvda_desk/domain/parallel_risk/risk_atoms.py
 create mode 100644 src/nvda_desk/domain/parallel_risk/unavailable_signals.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_atom_authority_semantics.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_description_contract.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_description_templates.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_enriched_authority_regression.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_event_proximity_register.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_family_aggregation.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_assembly.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_service_integration.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_options_dte_preservation.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_scheduled_event_preservation.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_supported_risk_atoms.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_unavailable_signals.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_governance.py
 create mode 100644 tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py
 create mode 100644 tests/tier_a/vocabulary/test_parallel_risk_description_vocabulary_constraints.py
 create mode 100644 var/audit/prl_architecture_decisions_001/ARTIFACT_MANIFEST.md
 create mode 100644 var/audit/prl_architecture_decisions_001/COMMAND_LOG.md
 create mode 100644 var/audit/prl_architecture_decisions_001/FULL_READ_MANIFEST.md
 create mode 100644 var/audit/prl_architecture_decisions_001/git_diff_check.txt
 create mode 100644 var/audit/prl_architecture_decisions_001/prl-architecture-decisions.patch
 create mode 100644 var/audit/prl_architecture_decisions_001/scaffold_check.txt
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/ARTIFACT_MANIFEST.md
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/COMMAND_LOG.md
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/FULL_READ_MANIFEST.md
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_broad_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_diff_check.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_financial_calendar_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_parallel_risk_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_scaffold_check.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_temporal_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_testing_harnesses_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_upstream_cognition_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_upstream_signal_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_pytest_after_admission.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_dmp_v3_vocabulary_terms.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_financial_calendar_vocabulary_terms.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_parallel_risk_description_vocabulary_constraints.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_parallel_risk_lane_vocabulary_terms.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_candidate_admission_plan_contracts.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_candidate_admission_plan_contracts_retry.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_candidate_admission_review_contracts.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_candidate_classification_contracts.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_candidate_payload_contracts.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_candidate_review_cli_contracts.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_candidate_review_cli_contracts_final_retry.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_candidate_review_cli_contracts_retry.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_candidate_schema_contracts.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_canonical_builder_parity.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_document_json_helpers.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_json_helper_contracts.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_required_baseline_terms.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_required_baseline_terms_retry.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_schema_contract_retry.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_synonym_candidate_audit_after_admission.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_workflow_surface_after_admission.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/final_vocabulary_test_vocabulary_workflow_surface_retry.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/patch_sha256.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/prl-blocked-leaves-completion.patch
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/prl_mrp_007_diff_check.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/prl_mrp_007_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/prl_mrp_009_diff_check.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/prl_mrp_009_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/prl_mrp_013_diff_check.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/prl_mrp_013_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/prl_mrp_020_diff_check.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/prl_mrp_020_pytest.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/proof_block_parallel_risk_lane_authority_surface.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/proof_block_vocabulary_governance_conformance_candidate.log
 create mode 100644 var/audit/prl_blocked_leaves_completion_001/vocabulary_synonym_audit_final.log
 create mode 100644 var/audit/prl_execution_batch_001/ARTIFACT_MANIFEST.md
 create mode 100644 var/audit/prl_execution_batch_001/COMMAND_LOG.md
 create mode 100644 var/audit/prl_execution_batch_001/FULL_READ_MANIFEST.md
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_final.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_003.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_004.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_005.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_006.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_007_blocked.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_008.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_009_blocked.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_010.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_011.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_012.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_013_blocked.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_014.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_015.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_016.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_017.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_018.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_019.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_020_blocked.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_021.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_022.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_023.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_024.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_025.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_025_rerun.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_026.txt
 create mode 100644 var/audit/prl_execution_batch_001/git_diff_check_prl_mrp_027.txt
 create mode 100644 var/audit/prl_execution_batch_001/prl-execution-batch-001.patch
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_003.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_004.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_005.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_006.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_010.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_011.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_012.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_014.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_015.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_016.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_017.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_018.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_019.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_021.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_022.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_023.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_024.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_025.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_prl_mrp_025_rerun.txt
 create mode 100644 var/audit/prl_execution_batch_001/pytest_relevant_final.txt
 create mode 100644 var/audit/prl_execution_batch_001/scaffold_check_final.txt
 create mode 100644 var/audit/prl_execution_batch_001/scaffold_check_prl_mrp_006.txt
 create mode 100644 var/audit/prl_execution_batch_001/scaffold_check_prl_mrp_008.txt
 create mode 100644 var/audit/prl_execution_batch_001/scaffold_check_prl_mrp_026.txt
 create mode 100644 var/audit/prl_execution_batch_001/scaffold_check_prl_mrp_027.txt
 create mode 100644 var/audit/prl_master_roadmap_001/ARTIFACT_MANIFEST.md
 create mode 100644 var/audit/prl_master_roadmap_001/COMMAND_LOG.md
 create mode 100644 var/audit/prl_master_roadmap_001/FULL_READ_MANIFEST.md
 create mode 100644 var/audit/prl_master_roadmap_001/git_diff_check.txt
 create mode 100644 var/audit/prl_master_roadmap_001/git_diff_check_final.txt
 create mode 100644 var/audit/prl_master_roadmap_001/prl-master-roadmap.patch
 create mode 100644 var/audit/prl_master_roadmap_001/scaffold_check.txt
 create mode 100644 var/audit/prl_minute_profile_contracts_001/ARTIFACT_MANIFEST.md
 create mode 100644 var/audit/prl_minute_profile_contracts_001/COMMAND_LOG.md
 create mode 100644 var/audit/prl_minute_profile_contracts_001/FULL_READ_MANIFEST.md
 create mode 100644 var/audit/prl_minute_profile_contracts_001/git_diff_check.txt
 create mode 100644 var/audit/prl_minute_profile_contracts_001/git_diff_check_closeout.txt
 create mode 100644 var/audit/prl_minute_profile_contracts_001/prl-minute-profile-contracts.patch
 create mode 100644 var/audit/prl_minute_profile_contracts_001/pytest_parallel_risk_contracts.txt
 create mode 100644 var/audit/prl_minute_profile_contracts_001/vocabulary_search.txt
 create mode 100644 var/audit/prl_minute_risk_profile_plan_001/ARTIFACT_MANIFEST.md
 create mode 100644 var/audit/prl_minute_risk_profile_plan_001/COMMAND_LOG.md
 create mode 100644 var/audit/prl_minute_risk_profile_plan_001/FULL_READ_MANIFEST.md
 create mode 100644 var/audit/prl_minute_risk_profile_plan_001/prl-minute-risk-profile-plan.patch
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/ARTIFACT_MANIFEST.md
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/BRANCH_HYGIENE.md
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/COMMAND_LOG.md
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/FULL_READ_MANIFEST.md
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/LEAF_RECONCILIATION.md
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/VALIDATION_SUMMARY.md
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/branch_hygiene_raw.log
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/deep_audit_probe.log
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/merge_to_main.log
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/premerge_git_diff_check.log
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/premerge_parallel_risk_pytest.log
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/premerge_proof_parallel_risk_lane_authority_surface.log
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/premerge_scaffold_check.log
 create mode 100644 var/audit/prl_tranche_final_audit_mainline_001/premerge_targeted_prl_inventory_vix.log
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/ARCHIVE_RECONCILIATION.md
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/ARTIFACT_MANIFEST.md
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/BRANCH_RECONCILIATION.md
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/COMMAND_LOG.md
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/FULL_READ_MANIFEST.md
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/LEDGER_AUDIT_SUMMARY.md
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/branches_initial.txt
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/current_branch_initial.txt
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/full_read_manifest_wc.txt
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/git_diff_check.txt
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/git_diff_stat_post_first_commit.txt
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/git_log_all_initial.txt
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/git_status_initial.txt
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/git_status_post_first_commit.txt
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/mnt_data_files_initial.txt
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/repo-freeze-ledger-audit-handoff.patch
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/scaffold_check.txt
 create mode 100644 var/audit/repo_freeze_ledger_audit_handoff_001/tags_initial.txt
merge_exit_code=0
$ git status --short
$ git log --oneline --decorate -n 20
78cbf3c (HEAD -> main) Merge PRL tranche completion
c2c2f5f (work/prl-blocked-leaves-completion) Audit PRL tranche completion before mainline integration
e58a624 PRL-MRP-013: reconcile PRL VIX thresholds through governed config
47857ca PRL-MRP-020: handle unavailable PRL signals from typed inventory
4c78d40 PRL-MRP-009: promote PRL signal inventory to typed runtime config
f2aa50e PRL-MRP-007: create governed signal inventory workbook tab
a7962ee (work/repo-freeze-ledger-audit-handoff) Close repo freeze ledger audit handoff
878c1cc Freeze repo state and audit roadmap ledger for handoff
c477e6a (work/prl-minute-risk-profile-execution-batch-001) PRL execution batch 001: closeout artefacts
10fac49 PRL-MRP-027: document deferred rich signal-family intake
caa54b5 PRL-MRP-026: update PRL roadmap and current-state docs
79a6896 PRL-MRP-025: add deterministic PRL description renderer
abefc5d PRL-MRP-024: add deterministic description contract
c4f0af0 PRL-MRP-023: document vocabulary-governed description constraints
737fba4 PRL-MRP-022: harden enriched authority regression tests
d912a27 PRL-MRP-021: complete minute profile lineage
0c8a4a4 PRL-MRP-020: mark inventory-backed unavailable signals blocked
0de59b7 PRL-MRP-019: add optional minute profile service path
6800fff PRL-MRP-018: add minute profile assembly
d3af38d PRL-MRP-017: add risk family aggregation
## postmerge_git_diff_check
```bash
git diff --check
```
- postmerge_git_diff_check exit_code=2
## postmerge_scaffold_check
```bash
make scaffold-check
```
- postmerge_scaffold_check exit_code=0
## postmerge_parallel_risk_pytest
```bash
env PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/parallel_risk -q
```
- postmerge_parallel_risk_pytest exit_code=0
## postmerge_proof_parallel_risk_lane_authority_surface
```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/run_proof_block.py --block parallel_risk_lane_authority_surface
```
- postmerge_proof_parallel_risk_lane_authority_surface exit_code=0
## postmerge_targeted_prl_inventory_vix
```bash
env PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_governance.py tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py tests/tier_a/vocabulary/test_parallel_risk_description_vocabulary_constraints.py -q
```
- postmerge_targeted_prl_inventory_vix exit_code=0
## postmerge_git_diff_check_after_log_trim
```bash
git diff --check
```
- postmerge_git_diff_check_after_log_trim exit_code=0
