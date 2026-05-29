# NVDA_2026 — Compact Baseline Validation and Handoff Receipt

## Outcome

A Git-preserving compact baseline branch named `work/NVDA_2026_compact_git_preserving_baseline_20260529` was created from the verified active-clean source repository. The forward working tree retains only current reference-required `var/` artefacts; deleted material remains recoverable from Git parent history and the source-locked original archive.

## Git provenance

| Field | Value |
|---|---|
| Source archive | `NVDA10_MAIN_RECONCILED_CLEAN_HANDOFF_20260520.tar.gz` |
| Source archive SHA-256 | `07a449cf6790745b039d100330e38dcbbe9bf6fa8c346d68fc1732a3afc49b18` |
| Parent commit | `2404734a57406576699cf02b12e31ece73ad0602` |
| Compact-baseline commit | `834a4f11252e6d413383ac32249352edfd07346e` |
| Branch | `work/NVDA_2026_compact_git_preserving_baseline_20260529` |

## Change boundary

| Measure | Result |
|---|---:|
| Removed tracked `var/` files | 8,405 |
| Removed working-tree payload bytes | 151,219,145 |
| Retained tracked `var/` files | 6 |
| Retained payload bytes | 197,703 |
| Remaining working-tree `var/` size on disk | approximately 195 KB |

No source, tests, configuration, numbered normative documents, `AGENTS.md`, `PLANS.md`, or `ROADMAP_LEDGER.md` were changed by the compact-baseline commit.

## Retained artefact basis

The retained `var/` files are required by one or more currently present source/test/config references:

- `var/vocabulary/synonym_candidates.json` — `config/proof_blocks.yaml`; `src/nvda_desk/vocabulary_synonym_audit.py`.
- `var/audit/test_false_positive_resistance_001/tier_a_coverage_reconciliation/tier_a_proof_block_coverage_summary.json` — `config/proof_blocks.yaml`.
- `var/audit/test_false_positive_resistance_001/final_closeout/TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001_TIER_B_COVERAGE_RECONCILIATION_RECEIPT.md` — `config/proof_blocks.yaml`.
- `var/audit/atlas_surface_slices/slices/vocabulary_governance_interface.json` — `config/retained_test_registry.yaml`.
- `var/audit/specimens/parallel_risk_envelope/sequence7_parallel_risk_envelope_expected_packet.json` — `config/retained_test_registry.yaml`; `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py`.
- `var/audit/active_code_atlas_001/vocabulary_candidate_adjudication_evidence_hardening_before_fwd016_20260515/VOCABULARY_CANDIDATE_ADJUDICATION_APPENDIX.json` — `tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py`.

## Validation performed

| Check | Observed result |
|---|---|
| Exact retained-path existence and removed-path absence assertion | PASS: retained `6`, removed `8405` |
| Git index retained `var/` equality assertion | PASS: exactly the six retained files remain tracked |
| `git diff --cached --check` before commit | PASS: no output, exit status 0 |
| `make scaffold-check` | PASS: `repo scaffold present` |
| `python3 scripts/run_proof_block.py --check-all` | PASS: `proof_blocks_check_all=PASS count=51` |
| `PYTHONPATH=src python3 -m pytest -q tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py` | PASS: `5 passed in 0.40s` |
| Full `PYTHONPATH=src python3 -m pytest -q tests/tier_a tests/tier_b` | Inconclusive: exceeded bounded execution time twice after displaying progress beyond 87%, without displayed failures before termination. Not claimed as passed. |
| Post-commit `git status --short --branch` | clean branch state observed immediately after commit |

## Deliberate unresolved control issue

This commit is archive hygiene only. Frozen historical references inside `PLANS.md` and `ROADMAP_LEDGER.md` still describe evidence available in the parent/source-locked state; their retirement or supersession belongs to the later Gate 2 authority-reset work. Gate 1 normative-authority repair identified in `NVDA10_3_GATE1_NORMATIVE_AUTHORITY_INTEGRITY_AUDIT_20260529.md` is not repaired by this baseline commit.

## Packaged artefact

| Field | Value |
|---|---|
| Archive | `NVDA_2026_GIT_PRESERVING_COMPACT_BASELINE_20260529.tar.gz` |
| Archive SHA-256 | `9e7375db3b02e3e012d90782126293f2ac3e164ceaba22b80844ff418f088261` |
| Archive size bytes | `31551387` |
| Extracted top-level repository directory | `NVDA_2026/` |
| Extracted Git HEAD | `834a4f11252e6d413383ac32249352edfd07346e` |
| Extracted branch | `work/NVDA_2026_compact_git_preserving_baseline_20260529` |
| Extracted Git status | clean branch state: `## work/NVDA_2026_compact_git_preserving_baseline_20260529` |
