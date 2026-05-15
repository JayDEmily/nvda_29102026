# NVDA10 Current State Architecture Map

Status: `RECONSTRUCTED_REPLACEMENT_REFRESHED_AFTER_FWD015`
Created: 2026-05-08
Last refreshed: 2026-05-15 FWD-016 ordered replay
Authoritative purpose: planning support only
Requested output path: `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md`

## 1. Reconstruction receipt

This file replaces the missing root-level `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md` expected by `PLANS.md`.

It is not the original missing artefact declared by the active `PLANS.md` lock. The original expected file was not present at the repo root in the sandbox checkout and was not present at the root of GitHub repo `JayDEmily/nvda10` on `main`, `codex/update-pyproject-metadata`, or commit `0c5b599633afaa0be28e1f00e96fac7b245d9366` when checked through the GitHub connector.

```text
expected_by_PLANS_file=NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md
expected_by_PLANS_size_bytes=26137
expected_by_PLANS_line_count=122
expected_by_PLANS_sha256=684379e8bd439936876e50064eb217dadf86798fa670b07622ba22ba2eae4a5d
replacement_status=RECONSTRUCTED_REPLACEMENT
replacement_not_original=true
```

## 2. Baseline lock

```text
source_tar=/mnt/data/nvda10-git-history-20260508.tar.gz
source_tar_size_bytes=123358934
source_tar_sha256=fab634480a65382eaa1ab9d75376d2eaccba3864f02669f7c3f78d8d8478c312
repo_root=/mnt/data/nvda10_git_history_review/nvda10
reconstruction_started_branch=pm/reconstruct-current-state-architecture-map-20260508
reconstruction_started_head=0c5b599633afaa0be28e1f00e96fac7b245d9366
final_reconciled_branch=main
```

Pre-existing working-tree status before this file was authored:

```text
 M assembly_reports/ARCHIVED_ASSET_PLACEMENT.tsv
 M assembly_reports/INPUT_ARCHIVE_READABILITY.tsv
 M assembly_reports/INPUT_ASSET_LOCKS.tsv
 M assembly_reports/ROOT_LAYOUT_VERIFICATION.tsv
 M var/audit/ledgers/sequence10_consolidated_read_ledger.tsv
 M var/audit/ledgers/sequence9_consolidated_read_ledger_hold_repair.tsv
```

The modified `assembly_reports/*` and `var/audit/ledgers/*` files listed above pre-existed this architecture-map repair branch and are not part of this reconstruction.

## 3. What this file is

This file is a whole-repo architecture ledger. It maps the current NVDA10 repo to the eighteen sequential native architecture surfaces defined in `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

For each row it records:

- the blueprint row ID and surface name;
- the blueprint owner and status values;
- observed native repo evidence paths;
- observed proof/test surfaces;
- the current blocker or gap;
- the next lawful action.

It is used by the PM and future worker briefs to prevent Atlas/donor candidates from being routed into vague or convenient code locations.

## 4. What this file is not

This file is not:

- an implementation plan;
- a proof result;
- an Atlas-readiness claim;
- permission to edit source, tests, vocabulary, dependencies, or generated Atlas material;
- a replacement for `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`;
- a second `PLANS.md`.

If this map conflicts with user instruction, `AGENTS.md`, `PLANS.md`, or governing normative docs, the higher authority wins and this map must be marked stale or rebuilt.

## 5. Governing evidence

Key governing evidence read in full for this reconstruction:

| File | Lines | SHA256 |
|---|---:|---|
| `AGENTS.md` | 152 | `39baab3ca05f21f7259440e1057dd742535cbc1118d20b2e852f5cc9b071e317` |
| `PLANS.md` | 468 | `6d16f3d068f5845cbc7bb59c902dd18a80210bce4da53804f91c57cfed7d1a96` |
| `README.md` | 25 | `b2f4096d82419630c0173eae7b221962d7fd3d6b99059c2c05672ad2cf8179f6` |
| `CURRENT_PROJECT_STATE.md` | 23 | `91a603921e260464087e07885c84fe419c86d188f6d54a6d51a660e66e690188` |
| `PROJECT_STRUCTURE.md` | 19 | `e4d594a14191fb63d2a9c15a401ac2af14cbecadfdbff7bb40020f22528a94e4` |
| `pyproject.toml` | 71 | `5cad081faececb68712b30b00b0caf572e36939135baa4f80d4f57fd965f4184` |
| `Makefile` | 143 | `b1024fd5398ef15f870c1f2272804312d3a9d8d705adfa463e321414733d13e2` |
| `.python-version` | 2 | `e72b03ed5b70312f2782f2b05055c55b24670e126d50e24c4f2c559bf288f810` |
| `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md` | 85 | `b75eb0dc0e5182de43dc34965978b42e66206d76a1159c445640dcddfc98f8a2` |
| `docs/01_NORMATIVE_CORE.md` | 118 | `32d26e8b67a5308291e61294cbc511d6bf51dccc5f961c11798714b249d813ee` |
| `docs/01.1_NORMATIVE_WORKING.md` | 24 | `3298f39f1674831693a1686aa4742a039a4779aafe5c7b0235412a660a707614` |
| `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md` | 143 | `d7c1d29948572eaaa7b2215568d2f539ca50bba7673203dc8c5395ce6e9139ae` |
| `docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md` | 14 | `2e790290a57cbb2f843f25e1ed8c233c95f44f022711e26d5847c517dddc0bc8` |
| `docs/03_DOMAIN_MODEL_CORE.md` | 160 | `b0c39d85c3157b6bc432f98e638b4fd1f9b4c8012350ef93653c25c312e0bc2d` |
| `docs/03.1_DOMAIN_MODEL_WORKING.md` | 14 | `c9c81dd0837da899c8733e634f1d7330a4501d231f41d179e1dd799c1535f0ed` |
| `docs/04_TECHNICAL_ARCHITECTURE_CORE.md` | 187 | `eb36ba355604ef193be809c54b1b8375bb89f1b7f057ead6f5c8122d654a3540` |
| `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md` | 44 | `a8cdd25a7870a1b738791e6da536940fea513a2d690d6b0fe4362a91cbfad3b8` |
| `docs/05_GUARDRAILS_CORE.md` | 82 | `7411eb660512161340d9c12819955476f5df523297204e949915412c2b44be9c` |
| `docs/05.1_GUARDRAILS_WORKING.md` | 22 | `214a8fc6ca9f2472a805c0eef26d4c161228220c6655915a6e52f47006b6bd1d` |
| `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md` | 148 | `dd2afe14ccc7e2dc1083495d619557fc405d19042cff1055014c8c2e3a293f07` |
| `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` | 48 | `d1c622a65b6ef082a1f1b9df3dc7dadb90c03ba8768a9c53976cd78b21dae6e3` |
| `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md` | 265 | `b84fc68df93dfaba6c578c04e103365c8fe372175fb351e99f523bb7bfdf1045` |
| `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` | 14 | `0136e6e262eefeeeee4828723efe06429379912015fc64e253c644ce311c380a` |
| `docs/08_TESTING_AND_PROMOTION_CORE.md` | 203 | `c3409910fd27d5452304469584179fb0c421ba82ee7903b95f9e0415b395e944` |
| `docs/08.1_TESTING_AND_PROMOTION_WORKING.md` | 14 | `c9b8c96deef18fc1b2b3c069c935216f1f5ff8bb363da02570710b6b56d691c1` |
| `docs/09_DMPV3_PROTOCOL_CORE.md` | 188 | `816ecb0b5e2bc76437920982e8eb37b4118f348a4aba8606806c45eb0ddf4abe` |
| `docs/09.1_DMPV3_PROTOCOL_WORKING.md` | 32 | `8e1c4e69cd799b860c5e0747f4f053c62106e8149340fdc050ec7f5b019a69f0` |
| `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` | 51 | `2d365d1f7bb7a765731a5234c2e4deb8cad3a2dff2963fbbe942711329192fa8` |
| `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` | 34 | `375d2ddb582f28038fe864565ea21ca1a13f2913f8162bda7f94c02813a6113b` |
| `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` | 759 | `23329f7b49e048dbd0ed2a9051b8ee519c3d82f6edde7922c5ad94adccb7a12a` |
| `docs/vocabulary/README.md` | 24 | `e76cc9c284641d194283f0a3194d0b81d2a603fd5f5c01b042f3b0fbe0e74439` |
| `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` | 52 | `25b04d2c45302de18d7d0652af2d53ff09c49fbafb20f522971550acac206b13` |
| `docs/vocabulary/vocabulary_registry.md` | 80 | `765496d0603adbf2ad467fdc818cdb5a206fe7f680ee0ef2cceeb343ab1920c1` |
| `data/vocabulary/README.md` | 13 | `4090dfc27f029948d97a438d89938d1f779e01dd89c7fc296d365810586bbe1b` |
| `data/vocabulary/canonical_vocabulary.json` | 764 | `0c874e338ea743c977dd0f6c617e990255af8c7672b9752f1b0eb4c55e862d89` |
| `src/README.md` | 6 | `175a254865113b8a1252abaa494256fb19033664bc80a5a191e8aae9c058ddf3` |
| `tests/AGENTS.override.md` | 77 | `8154245cfbb2734545ba86849f925847ffd10cc08e031bd0087413353cafc5e2` |
| `tests/README.md` | 12 | `c85d58cece621a044186f8aa88ad01a0ad2c90b7f54085f116520e16970522af` |
| `tests/tier_a/README.md` | 8 | `e32a0e2677131dc0f330093f14fd3c588c5d85f4067f2bb74a8651f9f7eb2ca1` |
| `tests/tier_b/README.md` | 8 | `d30e54959d88a7309081f70243e5376983fff2217e5b13230825b7aae13cf2fa` |
| `tests/tier_c/README.md` | 8 | `4d1a32dc7d7bd159f06867a22b17d20edc49eda39effce494e4e5fb51f718477` |
| `config/README.md` | 19 | `4b5f0bf9194374fc375dc7ca7d103477c3289bdc063796fd36c9d5ac91c234df` |
| `config/proof_blocks.yaml` | 6 | `4c4185cd1d3a314aa76a17e3d89547949922e521ea5b74b1cd732b74b7770f44` |
| `config/retained_test_registry.yaml` | 2488 | `05dbd9d8d8771631127acb07e9ca42fd77ef690b3f85596de81b6c64b7a40371` |
| `intent_migration/AGENTS.override.md` | 62 | `30594d481f6c1d0d86eb8d45f2959e21ff93dd8955160a63f5933094c208aa82` |
| `intent_migration/atlas_tranche_roadmap/AGENTS.override.md` | 73 | `b4c82dfa60dc2dad620156a9464703efd6c63ef0b4df48eaf61de7a596bdae47` |
| `intent_migration/testing_governance_reconciliation/AGENTS.override.md` | 60 | `b7b2c25b77dde5d8d5b9e34d264bb98abffd7234fd45d865c1e1f90c097e9d5c` |
| `assembly_reports/ASSEMBLY_REPORT.md` | 31 | `e3575ddd172d3aa91f276b5b2c7a6a98531303c628df3bd1d07ed0cf9f403c74` |
| `assembly_reports/NVDA10_CLEAN_BASELINE_STATUS.md` | 43 | `b4f427fcced77aa85729e7184386ad06606e52026d507cadcb180da8a003644b` |
| `assembly_reports/GAP006_REPAIR_PROMOTION_REPORT.md` | 94 | `cdd38c2b6b416b90d19912f5fa6ecb8fdda264e4b7dc80cfee0ebc01bc8205ac` |
| `assembly_reports/GAP006_REPAIR_PROMOTED_FILES.tsv` | 15 | `f10aa6812e7a8b05eabe803ad4ffd13704fbc5bf13b7e084ae0b9d049baf7bf5` |
| `evidence_index/atlas/README.md` | 4 | `ea02ca9edfe95b8fd94f9a7eacd7a669acca7e190c8404ed13393a24410e8871` |
| `evidence_index/gap006/README.md` | 4 | `988569c3c528403e6d88bed5676faf1e49da5ef4e93764a9044b7e644185205a` |
| `evidence_index/historical_sources/README.md` | 4 | `9164614a0ced30b67acd3cc610100ef0f5665e9bd8ee1151c234f356e574703d` |
| `evidence_index/stage1e/README.md` | 6 | `a7dcff9c5c81f35d54fd900d0aae55575b6f36070bedfd5bcaae5c746ff98add` |
| `project_control/atlas_provenance/README.md` | 4 | `d76c6802fa887561c18831bfa35a76b9c6c87745419ee80cbad199f0e8d40509` |
| `project_control/bridge_consolidation/README.md` | 4 | `d8de792d08595e145e80e624b7bca969da6aa431d42c343de7a37aacb3f64658` |
| `project_control/project_universe/PROJECT_UNIVERSE_INDEX.md` | 11 | `ec8b9b10cd889858634bc749abe8e7f6d9cf05da337be6228de121f9165b9a90` |
| `project_control/six_gap_status/README.md` | 4 | `fa2345b916d74ea138166a42f7763979fe6bf532e18ee3768e8c438af5329a28` |
| `var/audit/atlas_vocab_governance/2026-05-01_VOCAB_GOVERNANCE_NATIVE_ARCHITECTURE_MAP.md` | 36 | `612791cf93623aa3193e3b082f86beade16749450a06798697786d8ec9054238` |

## 6. Status rules used

The blueprint requires each target capability to map to a target package, module form, owner, seam, persistence owner where applicable, test family, traceability path, and honest structural and implementation-truth statuses. It defines implementation-truth values as `implemented`, `thin_seam`, `placeholder`, `reserved`, `future_only`, `legacy_only`, or `rejected` in `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:81-99`.

This replacement is conservative: no row is upgraded to `implemented` merely because code or tests exist. A row remains at its blueprint implementation-truth status unless an acceptance ledger or bounded proof evidence justifies a narrower claim. Where a proof report exists, this map records it as bounded evidence only.

## 7. Whole-repo architecture map

Current state after programme closeout reconciliation: all eighteen forward architecture surfaces have current ledger closure evidence or accepted bounded closure-remediation evidence. This map is an evidence index, not permission to reopen runtime/source/test/vocabulary/Atlas/generated-slice boundaries.

| Row ID | Architecture surface | Forward row | Ledger status | Current bounded semantic status | Primary evidence pointer | Next lawful action |
|---|---|---|---|---|---|---|
| 5.1 | External source interfaces and API ingress | `FWD-005` | `bounded_closed_current` | external-source/API ingress seam; no live network/client authority opened | FWD005_EXTERNAL_SOURCE_API_INGRESS_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.2 | Raw capture and source temporal law | `FWD-006` | `bounded_closed_current` | raw capture/source-temporal seam; source-time truth bounded by ordered replay | FWD006_RAW_CAPTURE_SOURCE_TEMPORAL_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.3 | Raw signal families | `FWD-007` | `bounded_closed_current` | raw/minimally-derived signal-family seam; grouped overlay coverage recorded | FWD007_RAW_SIGNAL_FAMILIES_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.4 | Financial and event calendar architecture | `FWD-008` | `bounded_closed_current` | financial/event calendar seam; projection/CRUD/reference-data boundaries recorded | FWD008_FINANCIAL_EVENT_CALENDAR_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.5 | Prepared ingress and runtime context preparation | `FWD-009` | `bounded_closed_current` | prepared ingress/runtime context seam; does not make runtime decisions | FWD009_PREPARED_INGRESS_CONTEXT_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.6 | DMPV3 packet carriage | `FWD-004` | `bounded_closed_current` | DMPV3 packet carriage seam; Tier A/B batch proof recorded | FWD004_PROOF_SUMMARY.json | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.7 | Serial desk-cognition spine | `FWD-012` | `bounded_closed_current` | serial candidate/cognition seam; no downstream capital/risk/placement authority opened | FWD012_SERIAL_DESK_COGNITION_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.8 | Parallel risk lane | `FWD-013` | `bounded_closed_current` | parallel risk reading seam; no serial candidate formation/capital sizing opened | FWD013_PARALLEL_RISK_LANE_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.9 | Dynamic coefficient and modifier authority | `FWD-010` | `bounded_closed_current` | bounded coefficient/modifier authority; no live self-tuning opened | FWD010_DYNAMIC_COEFFICIENT_MODIFIER_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.10 | Playbook library architecture | `FWD-011` | `bounded_closed_current` | playbook library/eligibility seam; blueprint remains provisional/reserved | FWD011_PLAYBOOK_LIBRARY_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.11 | Downstream capital deployment authority | `FWD-014` | `bounded_closed_current` | downstream capital deployment seam; no broker/order execution opened | FWD014_DOWNSTREAM_CAPITAL_DEPLOYMENT_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.12 | Opening architecture and placement readiness | `FWD-015` | `bounded_closed_current` | opening/placement-readiness seam; no live order placement opened | FWD015_OPENING_PLACEMENT_READINESS_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.13 | Live position and inventory architecture | `FWD-016` | `bounded_closed_current` | live position/inventory state seam; no exit/close authority opened by FWD-016 | FWD016_LIVE_POSITION_INVENTORY_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.14 | Exit and close architecture | `FWD-017` | `bounded_closed_current` | exit/close seam; batched broad proof hardened; no review/explanation opened by FWD-017 | FWD017_EXIT_CLOSE_ORDERED_REPLAY_CLOSURE_RECEIPT.md; FWD017_BATCHED_BROAD_PROOF_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.15 | Review and explanation layer | `FWD-018` | `bounded_closed_current` | post-runtime review/explanation/replay seam; no live trading decisions or programme completion claimed | FWD018_REVIEW_EXPLANATION_ORDERED_REPLAY_CLOSURE_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.16 | Persistence, ledgers, and receipts | `FWD-003` | `bounded_closed_current` | persistence/ledger/receipt seam and linkage remediation evidence recorded | FWD003_LINKAGE_REMEDIATION_PROOF_SUMMARY.json; FWD003_PERSISTENCE_LEDGER_RECEIPT_CLOSURE_EVIDENCE.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.17 | Testing, proof, and checkpoint surfaces | `FWD-002` | `closed_bounded_closure_remediation_accepted` | testing/proof/checkpoint closure remediation accepted; broad proof remains current through closeout | FWD002_CLOSURE_GRADE_READ_MANIFEST.json and FWD002_FWD004 receipts | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |
| 5.18 | Vocabulary governance interface | `FWD-001` | `bounded_closed_current` | vocabulary governance closed on suppression-removal plus pre-FWD-016 remediation/evidence-hardening | FWD001_BOUNDARY_RECEIPT.md; VOCABULARY_GOVERNANCE_REMEDIATION_RECEIPT.md; VOCABULARY_CANDIDATE_EVIDENCE_HARDENING_RECEIPT.md | No automatic feature row remains; future work requires explicit PM/user authority or a recorded defect. |

Programme closeout reconciliation artefacts are recorded under `var/audit/active_code_atlas_001/programme_closeout_reconciliation_20260515/`.

## 8. Closeout implication

The forward architecture-surface ordered replay programme through `FWD-018` has been reconciled in `var/audit/active_code_atlas_001/programme_closeout_reconciliation_20260515/`. This map does not approve live trading, broker execution, production deployment, external credentials, original Atlas/Bridge mutation, generated-slice rebuild, or new runtime feature work. It records only the current bounded evidence state.

## 9. Material considered

Material considered by the programme closeout reconciliation includes `ROADMAP_LEDGER.md`, all current row receipts/manifests/proof summaries/comparison reports selected in `PROGRAMME_CLOSEOUT_READ_MANIFEST.json`, current proof-block registry state, vocabulary governance remediation and evidence-hardening artefacts, and the batched Tier A/Tier B closeout proof logs under `var/audit/active_code_atlas_001/programme_closeout_reconciliation_20260515/reports/`.

## 10. Open items / Unknowns

- Unknown: whether future PM/user authority will open production-readiness, live broker/API credentials, generated-slice rebuild, or additional proof-hardening beyond the bounded closeout evidence recorded here.
- Known caveat: several blueprint rows remain `placeholder`, `reserved`, or `provisional`; row closure is bounded-current evidence, not a claim of final product maturity.
- Known caveat: FWD-002 has `closed_bounded_closure_remediation_accepted` rather than the later `bounded_closed_current` wording, retained to preserve its specific accepted remediation state.

## 11. Next PM action

No automatic FWD feature row remains after `FWD-018`. Future work requires explicit PM/user authority selecting a new defect, hardening, production-readiness, generated-slice, Atlas/Bridge, or deployment tranche.
