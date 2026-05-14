# Vocabulary governance native surface inventory — 2026-05-01

## Result
This inventory records native surfaces visible to the selected vocabulary governance candidate. It is read-only planning evidence, not a source/test/config/schema mutation package.

## Accepted native inventory
| Path | Lines | Size bytes | SHA256 | Planning role |
|---|---:|---:|---|---|
| `docs/vocabulary/README.md` | 23 | 962 | `e76cc9c284641d194283f0a3194d0b81d2a603fd5f5c01b042f3b0fbe0e74439` | Vocabulary governance orientation surface. |
| `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` | 51 | 1723 | `1e2643dcd604c193b7e019b23e39d64a966c58d8facf93fd41229246636fd24a` | Vocabulary consolidation/admission workflow surface. |
| `docs/vocabulary/vocabulary_registry.md` | 60 | 1280 | `776c1e390edfb95adefe03cf67b438b345b0bb676f0367578e3aeef7521ad14c` | Human-readable vocabulary registry surface. |
| `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` | 50 | 1944 | `2d365d1f7bb7a765731a5234c2e4deb8cad3a2dff2963fbbe942711329192fa8` | Core vocabulary/term governance authority. |
| `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` | 27 | 1936 | `10c041af1c8a9c916d5db51b0cf9cf35f3bb0caf08adc371cf913893aefbef3b` | Working vocabulary/term governance authority. |
| `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` | 758 | 40431 | `8f3de1fe9cac41c4b36c35c78a1acadb4d60b39e2f82a56f8ad134ed3c94f563` | Architecture owner/seam authority for §5.18. |
| `data/vocabulary/README.md` | 12 | 339 | `4090dfc27f029948d97a438d89938d1f779e01dd89c7fc296d365810586bbe1b` | Canonical vocabulary data directory note. |
| `data/vocabulary/canonical_vocabulary.json` | 699 | 23839 | `446ddd24be8da05aa25ec0bc4b0b618a905ccc6529873731e9d46cc8ef2f06f6` | Canonical vocabulary JSON data surface. |
| `data/vocabulary/feeder/README.md` | 5 | 176 | `9e8db2b8629f337e00709367945b599e99b3053e21a7423d5ec4a39e9953355e` | Feeder-area note. |
| `src/nvda_desk/schemas/vocabulary.py` | 185 | 8434 | `0ac278d3407227efa456bfe41078653c522ec09e309321346a9cb601090c47e8` | Native schema/model surface visible to selected slice. |
| `src/nvda_desk/vocabulary_builder.py` | 554 | 21232 | `736717abfba3c635c98946c1b2da75a560788c6d69654bf193339b076578a82c` | Native canonical vocabulary builder surface visible to selected slice. |
| `src/nvda_desk/vocabulary_synonym_audit.py` | 166 | 5307 | `fe1680a7132abed231ab3da4d77eb663687528b16a442c8fdb6ade8d08cca862` | Native synonym-audit surface visible to selected slice. |
| `scripts/build_canonical_vocabulary.py` | 28 | 641 | `e241a7c444dfb0e00464b1c3ec6924758dddcf66cce8c03c0407bfe126d1899e` | CLI wrapper for canonical vocabulary builder. |
| `scripts/vocabulary_synonym_audit.py` | 17 | 428 | `b51e77faf97ee616fe466c8031db96f842a0ec5374e3a3f6d20c774c7315394b` | CLI wrapper for vocabulary synonym audit. |
| `tests/tier_a/vocabulary/test_vocabulary_schema_contract.py` | 112 | 3643 | `22c49eb8d700639e0f2b9a9886964b240a9fdd40cfd15152b94aa1605bd2edd8` | Existing Tier A vocabulary schema contract test surface. |
| `tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py` | 38 | 1352 | `49cc02a6db86d72b0068575810cb4b37cf4092679060004cd56b06c5750fbc88` | Existing Tier A canonical builder parity test surface. |
| `tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py` | 140 | 4948 | `9c1cbc73cbe009c157323b52e2041719c13404cf0f3e391e3f18808c3f0c9fc7` | Existing Tier A baseline-term test surface. |
| `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py` | 24 | 774 | `2057a4e5013f71337c36959c6c6c0a76fb775a36f8eeaeb054bd5034e2e5a0d7` | Existing Tier A synonym-candidate audit test surface. |
| `tests/tier_a/vocabulary/test_vocabulary_workflow_surface.py` | 20 | 674 | `a7e0dc25de13fac9d29c8d0f46d6a5f17083fdc6c669331a37cee4a3237df1cb` | Existing Tier A vocabulary workflow surface test. |
| `tests/tier_a/vocabulary/test_dmp_v3_vocabulary_terms.py` | 36 | 1376 | `48e171e51b6b03bd8fd2239817d12f3ae1d2d7f147a082b8393eef7b50999c89` | Existing Tier A vocabulary term-presence test surface. |
| `tests/tier_a/vocabulary/test_financial_calendar_vocabulary_terms.py` | 26 | 885 | `abbc3017171310962acc053ff0d9aaa9c2eff5607b9268a81e5d2fd5c53097b7` | Existing Tier A vocabulary term-presence test surface. |
| `tests/tier_a/vocabulary/test_parallel_risk_lane_vocabulary_terms.py` | 25 | 991 | `5dda589d5486f82146f4ed4eaf25ff9421a48e0b1d8995f8bd88449bc0280797` | Existing Tier A vocabulary term-presence test surface. |
| `tests/tier_b/options_flow_support/test_options_flow_history_lane_vocabulary.py` | 41 | 1693 | `75b90bde361e07fbbde57a1ae3cba0da9f7a8b2a05f6dea81a07cf51af5318e1` | Existing Tier B vocabulary-related support test surface. |
| `config/retained_test_registry.yaml` | 2338 | 135837 | `48d7ab8c566c015a76a00a27a54ca7f3718e8073397b5b33301a8e165888ae42` | Proof/test registry surface cited by vocabulary proof posture. |
| `config/proof_blocks.yaml` | 5 | 196 | `5afb6c44800baf89cf87eafdd91ba7faee3365bd7a992a325876dee04e1ff9af` | Proof block registry surface. |
| `var/vocabulary/synonym_candidates.json` | 872 | 30449 | `6de442adbb6475561cd63af8299716b37cfa855116f35de512d310556cf6c4d3` | Vocabulary synonym candidate data surface. |

## Prohibited surfaces for this package
The inventory above is read-only. This package does not edit source code, tests, config, schemas, vocabulary data, generated slices, original Atlas/Bridge JSON, or planning-compiler code.
