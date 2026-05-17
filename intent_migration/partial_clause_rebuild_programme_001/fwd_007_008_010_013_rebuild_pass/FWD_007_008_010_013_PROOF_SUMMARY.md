# FWD-007/008/010/013 proof summary

## Targeted proof

| Command | Result artefact | Result |
|---|---|---|
| `env PYTHONPATH=src python -m pytest tests/tier_a/upstream_signal/test_fwd007_raw_signal_family_rebuild_contract.py tests/tier_a/financial_calendar/test_fwd008_runtime_calendar_query_contract.py tests/tier_a/config/test_fwd010_coefficient_calibration_contract.py tests/tier_a/parallel_risk/test_fwd013_parallel_risk_candidate_enrichment_contract.py` | `proof/targeted_fwd007_008_010_013_pass.txt` | `6 passed` |
| `env PYTHONPATH=src python -m pytest tests/tier_a/upstream_signal tests/tier_a/financial_calendar tests/tier_a/config tests/tier_a/modifiers tests/tier_a/parallel_risk tests/tier_a/api` | `proof/adjacent_surface_tests_pass.txt` | `90 passed` |
| `python scripts/run_proof_block.py --block fwd007_008_010_013_rebuild_surface` | `proof/fwd007_008_010_013_proof_block_pass.txt` | `6 passed` |
| `python scripts/run_proof_block.py --check-all` | `proof/proof_blocks_check_all_pass.txt` | `proof_blocks_check_all=PASS count=50` |

## Adjacent proof blocks run

| Proof block | Result artefact | Result |
|---|---|---|
| `raw_signal_contract_copy_boundary_surface` | `proof/raw_signal_contract_copy_boundary_surface_pass.txt` | `2 passed` |
| `raw_signal_transform_boundary_surface` | `proof/raw_signal_transform_boundary_surface_pass.txt` | `2 passed` |
| `financial_event_calendar_authority_surface` | `proof/financial_event_calendar_authority_surface_pass.txt` | `13 passed` |
| `financial_event_calendar_transform_boundary_surface` | `proof/financial_event_calendar_transform_boundary_surface_pass.txt` | `2 passed` |
| `dynamic_coefficient_modifier_authority_surface` | `proof/dynamic_coefficient_modifier_authority_surface_pass.txt` | `18 passed` |
| `modifier_contract_authority_boundaries_surface` | `proof/modifier_contract_authority_boundaries_surface_pass.txt` | `5 passed` |
| `dynamic_modifier_transform_boundary_surface` | `proof/dynamic_modifier_transform_boundary_surface_pass.txt` | `3 passed` |
| `parallel_risk_lane_authority_surface` | `proof/parallel_risk_lane_authority_surface_pass.txt` | `39 passed` |
| `parallel_risk_lane_transform_boundary_surface` | `proof/parallel_risk_lane_transform_boundary_surface_pass.txt` | `3 passed` |
| `fwd005_api_internal_exposure_surface` | `proof/fwd005_api_internal_exposure_surface_pass.txt` | `7 passed` |

## Vocabulary and style gates

| Command | Result artefact | Result |
|---|---|---|
| `env PYTHONPATH=src python scripts/vocabulary_synonym_audit.py --check-clean` | `proof/vocabulary_synonym_audit_clean_check_pass.txt` | `vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False` |
| `env PYTHONPATH=src python scripts/vocabulary_candidate_review.py --candidates var/vocabulary/synonym_candidates.json --summary-only --check-clean` | `proof/vocabulary_candidate_review_clean_check_pass.txt` | `vocabulary_candidate_review=PASS blocked_candidates=0` |
| `python -m black --check <changed-files>` | `proof/black_check_changed_files_pass.txt` | `18 files would be left unchanged` |
| `python -m ruff check <changed-files>` | `proof/ruff_check_changed_files_pass.txt` | `All checks passed` |

## Known limitation

A broad `python -m black --check src tests scripts` invocation aborted in this container with multiprocessing worker failures before completion. Changed-file Black and Ruff checks passed and are the styling proof used for this bounded pass.
