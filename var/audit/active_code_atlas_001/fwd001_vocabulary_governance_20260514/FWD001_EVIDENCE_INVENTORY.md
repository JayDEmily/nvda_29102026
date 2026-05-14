# FWD-001 Evidence Inventory

Date: 2026-05-14
Branch: `worker/fwd-001-vocabulary-governance-blocker-resolution`

Read-status caveat: `sectional_current_evidence` means the listed sections were used as current evidence; it is not a full-file-read claim.

| path | line count | SHA256 | read status | influence |
|---|---:|---|---|---|
| `/mnt/data/NVDA10_WORKER_BRIEF_FWD001_DEEP_VOCAB_BLOCKER_RESOLUTION_2026-05-14.md` | 522 | `691925d2695a1d823036c397015961b0a6cb1e2203a518f566f4ad3b40c45e9e` | full | FWD-001 scope, artefact requirements, decision labels, validation/package requirements. |
| `/mnt/data/PROJECT_EXECUTION_METHOD.md` | 473 | `2f14b48155e4fe69c6e969b82c98e41976f888f512a58975680771cbbf0da160` | full | Repo execution method and evidence discipline. |
| `AGENTS.md` | 184 | `0223600ad6526baf962ef26de4cc3d70e9564928556f6a08f02a7538e154b4da` | full | Root execution/governance protocol. |
| `PLANS.md` | 707 | `5b1e48007c4655e734e7b74a3e1d34406ec27990a8474ec1bfd7007b047e0672` | sectional_current_evidence | Standing authority, intake, proof, closeout sections used; not asserted as full-file read in this pass. |
| `ROADMAP_LEDGER.md` | 1655 | `c3ee4467693dcb683b0dea7d1a35a7238ab4aed4b146bbe2924b66ef48004705` | sectional_current_evidence | Current pointer and FWD-001/FWD-state rule sections used; row mutated. |
| `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md` | 84 | `b75eb0dc0e5182de43dc34965978b42e66206d76a1159c445640dcddfc98f8a2` | full | Vocabulary governance route. |
| `docs/01_NORMATIVE_CORE.md` | 117 | `32d26e8b67a5308291e61294cbc511d6bf51dccc5f961c11798714b249d813ee` | full | Normative invariants and vocabulary/blueprint authority. |
| `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` | 50 | `2d365d1f7bb7a765731a5234c2e4deb8cad3a2dff2963fbbe942711329192fa8` | full | Canonical vocabulary law: one durable term/meaning, explicit aliases only. |
| `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` | 33 | `375d2ddb582f28038fe864565ea21ca1a13f2913f8162bda7f94c02813a6113b` | full | Working vocabulary admissions and alias discipline. |
| `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` | 758 | `23329f7b49e048dbd0ed2a9051b8ee519c3d82f6edde7922c5ad94adccb7a12a` | sectional_current_evidence | Row 5.18 vocabulary governance interface and proof expectations. |
| `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md` | 195 | `abccce77e4b3e7847582b9521f47c2e3cf78918221f0bd4e002878de270932e6` | sectional_current_evidence | Current-state row 5.18 context. |
| `docs/vocabulary/README.md` | 23 | `e76cc9c284641d194283f0a3194d0b81d2a603fd5f5c01b042f3b0fbe0e74439` | full | Vocabulary artefact routing. |
| `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` | 213 | `0cce16eb35b95f03684c035da751f4344b10e8ca6f1e671b1cf697e2f9a56f56` | sectional_current_evidence | Candidate escalation and no-hand-editing workflow sections. |
| `docs/vocabulary/vocabulary_registry.md` | 79 | `765496d0603adbf2ad467fdc818cdb5a206fe7f680ee0ef2cceeb343ab1920c1` | full | Current vocabulary registry entries for candidate nearest slugs. |
| `data/vocabulary/canonical_vocabulary.json` | 763 | `0c874e338ea743c977dd0f6c617e990255af8c7672b9752f1b0eb4c55e862d89` | machine_read_for_terms | Nearest slug/label source for audit report and tests. |
| `config/proof_blocks.yaml` | 807 | `b9e22dd47238543e1fe1bfe72112d531245cad9fff0ec6f23f2a9b44150f6995` | sectional_current_evidence | Vocabulary proof block commands and candidate source records. |
| `config/retained_test_registry.yaml` | 3561 | `87cc5eb5b05f2c724c1626ea3201bda5d17e6517fc63ca923b5144f85173bf25` | sectional_current_evidence | Retained test-family records containing several candidate fragments. |
| `tests/AGENTS.override.md` | 76 | `8154245cfbb2734545ba86849f925847ffd10cc08e031bd0087413353cafc5e2` | full | Test mutation authority. |
| `pyproject.toml` | 71 | `e78bb32ac088a884379130b03450fc01d77a6a994281145b6d6c9a14b30df2e6` | full | Pytest path ordering repaired so exact `PYTHONPATH=src pytest ...` resolves root scripts before src/scripts. |
| `scripts/vocabulary_synonym_audit.py` | 26 | `218cd7d6ee854cd04d92a80e4d3eaf0e81f12bad107bc7a371bdd55c182231b2` | full | Exact proof command wrapper repaired to bootstrap repo src path. |
| `src/nvda_desk/vocabulary_synonym_audit.py` | 1212 | `ea823cdf9afc8ce7ac4afbb8b4621b823166f9cdc97bfe09afded52aaa4964de` | full | Audit implementation changed with path-bounded FWD-001 candidate fragment handling. |
| `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py` | 2193 | `556037ba4da8010033220cc5068987dbdd428ea9688ac7df5de403c5c6e7623d` | full | Targeted regression/false-positive-resistance tests added. |
| `var/audit/active_code_atlas_001/full_read_manifests/FWD001_VOCABULARY_GOVERNANCE_FULL_READ_MANIFEST.json` | 163 | `f4ea8d60dcbe713969d9aa028096c9d062918c62500f3ae8f7648be61e104fad` | generated_manifest | Read-status manifest generated for FWD-001. |
| `var/audit/active_code_atlas_001/fwd001_vocabulary_governance_20260514/reports/exact_vocabulary_synonym_audit_clean_check.stdout` | 2 | `86c76bf3cfe497f3d85672007a6d7d947b7238c95391fbd718e917a4032d7cd8` | generated_report | Exact current audit output. |
| `var/audit/active_code_atlas_001/fwd001_vocabulary_governance_20260514/reports/targeted_synonym_candidate_audit_pytest.stdout` | 3 | `b013eff76edef5f02108404d64e3c6723aaab0333f10065e28d5a5f77aa77a89` | generated_report | Targeted synonym-audit pytest output. |
| `var/audit/active_code_atlas_001/fwd001_vocabulary_governance_20260514/reports/vocabulary_synonym_audit_clean_check.stdout` | 4 | `4367a5a344046e6ac22860f4ee9ca8547f683a5d268d2137dd0f61ac3b703278` | generated_report | Named proof block output. |
| `var/audit/active_code_atlas_001/fwd001_vocabulary_governance_20260514/reports/vocabulary_governance_conformance_candidate.stdout` | 33 | `819999bb1955ee212ad6cd75c2e45ba7e6a6d9e1cec8ef1cdd02462df8f80bc2` | generated_report | Vocabulary governance conformance proof block output. |
| `var/audit/active_code_atlas_001/fwd001_vocabulary_governance_20260514/reports/proof_block_check_all.stdout` | 2 | `b9c22ef766419096f167f09059e7ae44510a9c1cb521ef4e704eed6a6f609556` | generated_report | Proof-block manifest validation output. |
| `var/audit/active_code_atlas_001/fwd001_vocabulary_governance_20260514/reports/tier_a_pytest_q.stdout` | 11 | `4f592fa127c7cf2d5274a47151093286e98c612ce70a672b85d884d1300e8e46` | generated_report | Tier A pytest output. |
| `var/audit/active_code_atlas_001/fwd001_vocabulary_governance_20260514/reports/tier_b_pytest_q.stdout` | 3 | `71a194051848ec2355a7ba7f292f28e0c89b86a1c1cbee67ec8fdb1bf9274608` | generated_report | Tier B pytest output. |
| `var/audit/active_code_atlas_001/fwd001_vocabulary_governance_20260514/reports/tier_a_tier_b_pytest_q.stdout` | 11 | `d72134a7714c9fbb9df77308bd9e38e21fea9e3cf4002c75570d22aa7fa57c4a` | generated_report | Combined Tier A/Tier B exact broad proof output. |
| `var/audit/active_code_atlas_001/fwd001_vocabulary_governance_20260514/reports/git_diff_check.stdout` | 1 | `194ff5bca66278888f0f00be5c7ca523d15098ece958b14952533811089f6106` | generated_report | Whitespace/diff hygiene output. |

## Validation summary

| Command | Result | Evidence file |
|---|---|---|
| `python scripts/vocabulary_synonym_audit.py --check-clean` | `EXIT:0`, `candidates=0` | `reports/exact_vocabulary_synonym_audit_clean_check.stdout` |
| `PYTHONPATH=src python -m pytest tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py -q` | `47 passed`, `EXIT:0` | `reports/targeted_synonym_candidate_audit_pytest.stdout` |
| `PYTHONPATH=src python scripts/run_proof_block.py --block vocabulary_synonym_audit_clean_check` | `EXIT:0` | `reports/vocabulary_synonym_audit_clean_check.stdout` |
| `PYTHONPATH=src python scripts/run_proof_block.py --block vocabulary_governance_conformance_candidate` | `117 passed`, `EXIT:0` | `reports/vocabulary_governance_conformance_candidate.stdout` |
| `python scripts/run_proof_block.py --check-all` | `proof_blocks_check_all=PASS count=46`, `EXIT:0` | `reports/proof_block_check_all.stdout` |
| `PYTHONPATH=src python -m pytest -q tests/tier_a` | `590 passed`, `EXIT:0` | `reports/tier_a_pytest_q.stdout` |
| `PYTHONPATH=src python -m pytest -q tests/tier_b` | `48 passed`, `EXIT:0` | `reports/tier_b_pytest_q.stdout` |
| `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` | `638 passed`, `EXIT:0` | `reports/tier_a_tier_b_pytest_q.stdout` |
| `git diff --check` | `EXIT:0` | `reports/git_diff_check.stdout` |

## Changes made

- Added exact FWD-001 path/raw-phrase/nearest-slug fragment handling in `src/nvda_desk/vocabulary_synonym_audit.py`.
- Added tests proving those fragments are path-bounded and do not globally hide the same synonym-like phrases.
- Added CLI wrapper path bootstrap for the exact proof-block command.
- Added pytest `pythonpath = [".", "src"]` so the exact broad `PYTHONPATH=src pytest ...` command resolves root `scripts` before `src/scripts`.
- Recorded candidate adjudication, evidence inventory, read-status manifest, receipt, and validation logs.
