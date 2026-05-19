# FWD-004 read receipt

Read method records the terminal/file-stream method used in this pass. `read in full` means the file was opened as a complete file for this pass; targeted line excerpts were additionally inspected where mutation decisions required exact line references.

| path | line/row count | SHA-256 | read method | read in full | relevance |
|---|---:|---|---|---|---|
| `AGENTS.md` | 184 | `0223600ad6526baf962ef26de4cc3d70e9564928556f6a08f02a7538e154b4da` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `intent_migration/AGENTS.override.md` | 61 | `30594d481f6c1d0d86eb8d45f2959e21ff93dd8955160a63f5933094c208aa82` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `intent_migration/native_intent_implementation/AGENTS.override.md` | 69 | `77a011ce9e736e1db77c63a63869108ec9524baa9cf1af752f1b5e94359472b0` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `intent_migration/native_intent_satisfaction/AGENTS.override.md` | 60 | `7d31a64ff087ad238ba730d10990255286e1466b1659faf6e17ae1baa139e688` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `tests/AGENTS.override.md` | 76 | `8154245cfbb2734545ba86849f925847ffd10cc08e031bd0087413353cafc5e2` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `PLANS.md` | 707 | `5b1e48007c4655e734e7b74a3e1d34406ec27990a8474ec1bfd7007b047e0672` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `ROADMAP_LEDGER.md` | 4078 | `1c335bd0566c25214691f0606eee7b843c1992601009ff010f135e5dfee7c66b` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md` | 84 | `b75eb0dc0e5182de43dc34965978b42e66206d76a1159c445640dcddfc98f8a2` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/01_NORMATIVE_CORE.md` | 117 | `32d26e8b67a5308291e61294cbc511d6bf51dccc5f961c11798714b249d813ee` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/01.1_NORMATIVE_WORKING.md` | 23 | `3298f39f1674831693a1686aa4742a039a4779aafe5c7b0235412a660a707614` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md` | 147 | `dd2afe14ccc7e2dc1083495d619557fc405d19042cff1055014c8c2e3a293f07` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` | 342 | `1cb694a96d0ccb70895d214246771a40b1a4c003bcecbaeb04ae82466965965b` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/08_TESTING_AND_PROMOTION_CORE.md` | 202 | `c3409910fd27d5452304469584179fb0c421ba82ee7903b95f9e0415b395e944` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/08.1_TESTING_AND_PROMOTION_WORKING.md` | 13 | `c9b8c96deef18fc1b2b3c069c935216f1f5ff8bb363da02570710b6b56d691c1` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/09_DMPV3_PROTOCOL_CORE.md` | 187 | `816ecb0b5e2bc76437920982e8eb37b4118f348a4aba8606806c45eb0ddf4abe` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/09.1_DMPV3_PROTOCOL_WORKING.md` | 39 | `d6feb5dda3a582a96eeae567447e3f7c5753f3b9cbaab170d5db541af729c42a` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` | 50 | `2d365d1f7bb7a765731a5234c2e4deb8cad3a2dff2963fbbe942711329192fa8` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` | 33 | `375d2ddb582f28038fe864565ea21ca1a13f2913f8162bda7f94c02813a6113b` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` | 758 | `23329f7b49e048dbd0ed2a9051b8ee519c3d82f6edde7922c5ad94adccb7a12a` | nl/cat terminal inspection + full file stream | yes | authority/control |
| `var/audit/non310_completion_claim_audit_20260519/FINAL_AUDIT_DECISION.md` | 55 | `b4f59a3a7c95d0543bcd69a4c8f3478b444a51c81fd78706d597aa235f888e43` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `var/audit/non310_completion_claim_audit_20260519/FWD004_ROW_AUDIT.csv` | 73 data rows | `058c2690f5f9aaa4ba70b9d272384be41febfe2d68871350784e2103289c88cc` | csv.DictReader + full file stream | yes | FWD-004 audit/test/source evidence |
| `tests/tier_a/packets/test_dmpv3_extension_canonical_leaf_surface.py` | 72 | `45dfe7e719fb31b6b8aae23b28cc0bd82d8cdcec3456f46acf9b48286ecd107d` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `tests/tier_a/packets/test_dmpv3_transform_boundary_surface.py` | 52 | `40acde2f80b7e2d69b3d5c62f65105e48fe1449eec92f2686c67f2b79a76b699` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `tests/tier_a/packets/test_reference_packet_carriage.py` | 154 | `61a55a2caed8bb9e0497a8a980d413cb0790a8a3d1c3fa8afc07eed93b37ca41` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `src/nvda_desk/contracts/packets.py` | 252 | `61b54ba3993f547466be9aca48379bd95dcbdbb535bf1362cdfbb69be9e55b8a` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `src/nvda_desk/packets/dmp_packets.py` | 408 | `029af4c848fd11c2a60ad08a05ac8192f00e92b08afc7bd0f93554d15dc620bf` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `src/nvda_desk/review/packet_service.py` | 175 | `a7e4700bac877a1351572f30b1904deae0bebee854c6ff62aa57f2120d690ecb` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `src/nvda_desk/contracts/review.py` | 104 | `73a2984b03267b72b4ddd9cbb7a7f9dfb3409e36ccab163dc0a9c89c550ad4e0` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `src/nvda_desk/preparation/context_packet.py` | 103 | `5193192666ceb92835d349cdf8804bcd6c7fbbd201c22c9054df9b2595642773` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `src/nvda_desk/contracts/dataset_packets.py` | 41 | `721534bffeb4afe04f2dc47edb88e38cb3588624d677479f55650f0f1294e953` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
| `tests/tier_a/review_runtime/test_fwd018_review_packet_and_slv_replay_contract.py` | 88 | `d5235b34c8b04486442e3327548441a674b42b9108bca3129dbfc08934731215` | nl/cat terminal inspection + full file stream | yes | FWD-004 audit/test/source evidence |
