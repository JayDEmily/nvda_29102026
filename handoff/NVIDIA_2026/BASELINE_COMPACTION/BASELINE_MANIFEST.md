# NVDA_2026 — Git-Preserving Compact Active-Codebase Baseline

## Purpose

This is a compact forward baseline derived from the active-clean repository archive. It retains Git history, native source, tests, configuration and normative/control documents, while removing historical `var/` payload from the forward working tree except for artefacts still directly required by current source, tests or configuration.

This packaging/hygiene commit does **not** repair the Gate 1 normative-authority defects identified in `NVDA10_3_GATE1_NORMATIVE_AUTHORITY_INTEGRITY_AUDIT_20260529.md`, does not accept any Atlas migration output, and does not open source/test/normative/vocabulary feature mutation.

## Source lock

| Field | Value |
|---|---|
| Source archive | `NVDA10_MAIN_RECONCILED_CLEAN_HANDOFF_20260520.tar.gz` |
| Source archive SHA-256 | `07a449cf6790745b039d100330e38dcbbe9bf6fa8c346d68fc1732a3afc49b18` |
| Parent Git HEAD | `2404734a57406576699cf02b12e31ece73ad0602` |
| Baseline branch | `work/NVDA_2026_compact_git_preserving_baseline_20260529` |

## Boundary decision

The prior `var/` payload is retained in Git ancestry and in the source-locked archive above. It is not carried as forward working-tree payload in `NVDA_2026` unless required by an existing executable/config/test reference.

Frozen historical references in `PLANS.md` and `ROADMAP_LEDGER.md` remain provenance references to the parent state; their later retirement or supersession is a separate Gate 2 control-surface task and is not concealed by this hygiene commit.

## Retained `var/` artefacts

| Path | Reason retained |
|---|---|
| `var/vocabulary/synonym_candidates.json` | Owned output path in `config/proof_blocks.yaml` and output path in `src/nvda_desk/vocabulary_synonym_audit.py`. |
| `var/audit/test_false_positive_resistance_001/tier_a_coverage_reconciliation/tier_a_proof_block_coverage_summary.json` | Owned path in `config/proof_blocks.yaml`. |
| `var/audit/test_false_positive_resistance_001/final_closeout/TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001_TIER_B_COVERAGE_RECONCILIATION_RECEIPT.md` | Owned path in `config/proof_blocks.yaml`. |
| `var/audit/atlas_surface_slices/slices/vocabulary_governance_interface.json` | Architecture-basis path retained in `config/retained_test_registry.yaml`. |
| `var/audit/specimens/parallel_risk_envelope/sequence7_parallel_risk_envelope_expected_packet.json` | Required by `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py` and retained-test registry. |
| `var/audit/active_code_atlas_001/vocabulary_candidate_adjudication_evidence_hardening_before_fwd016_20260515/VOCABULARY_CANDIDATE_ADJUDICATION_APPENDIX.json` | Required by `tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py`. |

Exact retained hashes and exact removed-path hashes are recorded in:

- `NVDA_2026_RETAINED_VAR_PATHS_MANIFEST.json`
- `NVDA_2026_REMOVED_VAR_PATHS_MANIFEST.json`

## Known limitations

- `scripts/materialise_atlas_surface_slices.py` remains historical tooling but its old `var/audit/imports` and ledger inputs are no longer carried forward in the compact working tree. It must not be treated as runnable migration authority in this baseline without explicitly restoring/supplying its input package.
- Gate 1 normative-authority repair remains outstanding and must be performed after this compact baseline is accepted as the working substrate.
