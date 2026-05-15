# Vocabulary Governance Remediation Command Log

## added_vocabulary_parity_pytest

```bash
env PYTHONPATH=src python -m pytest -q tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py
```

Exit/status: `0`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/added_vocabulary_parity_pytest.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/added_vocabulary_parity_pytest.stderr`

Summary: ...                                                                      [100%] | 3 passed in 0.20s

## git_diff_check

```bash
git diff --check
```

Exit/status: `0`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/git_diff_check.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/git_diff_check.stderr`

Summary: 

## git_diff_check_final

```bash
git diff --check
```

Exit/status: `0`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/git_diff_check_final.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/git_diff_check_final.stderr`

Summary: 

## git_status_short

```bash
git status --short
```

Exit/status: `0`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/git_status_short.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/git_status_short.stderr`

Summary:  M tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py |  M var/vocabulary/synonym_candidates.json | ?? var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/

## proof_block_vocabulary_governance_conformance_candidate

```bash
env PYTHONPATH=src python scripts/run_proof_block.py --block vocabulary_governance_conformance_candidate
```

Exit/status: `tool_timeout_no_exit_status_no_pass_claimed`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/proof_block_vocabulary_governance_conformance_candidate.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/proof_block_vocabulary_governance_conformance_candidate.stderr`

Summary: ........                                                                 [ 57%] | tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py . [ 58%] | ............

## proof_block_vocabulary_governance_conformance_candidate_rerun

```bash
env PYTHONPATH=src python scripts/run_proof_block.py --block vocabulary_governance_conformance_candidate
```

Exit/status: `0`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/proof_block_vocabulary_governance_conformance_candidate_rerun.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/proof_block_vocabulary_governance_conformance_candidate_rerun.stderr`

Summary: ............                                                             [ 98%] | tests/tier_a/vocabulary/test_vocabulary_workflow_surface.py .            [100%] | ============================= 89 passed in 23.22s ==============================

## proof_block_vocabulary_synonym_audit_clean_check

```bash
env PYTHONPATH=src python scripts/run_proof_block.py --block vocabulary_synonym_audit_clean_check
```

Exit/status: `tool_timeout_no_exit_status_no_pass_claimed`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/proof_block_vocabulary_synonym_audit_clean_check.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/proof_block_vocabulary_synonym_audit_clean_check.stderr`

Summary: 

## proof_block_vocabulary_synonym_audit_clean_check_rerun

```bash
env PYTHONPATH=src python scripts/run_proof_block.py --block vocabulary_synonym_audit_clean_check
```

Exit/status: `0`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/proof_block_vocabulary_synonym_audit_clean_check_rerun.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/proof_block_vocabulary_synonym_audit_clean_check_rerun.stderr`

Summary: proof_block_id=vocabulary_synonym_audit_clean_check | command=python scripts/vocabulary_synonym_audit.py --check-clean | vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False

## proof_blocks_check_all

```bash
env PYTHONPATH=src python scripts/run_proof_block.py --check-all
```

Exit/status: `0`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/proof_blocks_check_all.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/proof_blocks_check_all.stderr`

Summary: proof_blocks_check_all=PASS count=46

## vocabulary_suppression_scan

```bash
grep -RIn "FWD001_GOVERNANCE\|_is_fwd001\|selected_fragments\|GOVERNANCE_CANDIDATE\|path-bound\|suppress\|suppression\|ignore_candidate\|skip_candidate\|filter_candidate\|candidate_filter" src tests scripts docs config || true
```

Exit/status: `0`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/vocabulary_suppression_scan.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/vocabulary_suppression_scan.stderr`

Summary: docs/vocabulary/CONSOLIDATION_WORKFLOW.md:206:The stdin input mode is a transport convenience only. It must preserve the same validation, summary, receipt, and clean-check semantics as file-backed candidate payloads; it must not admit terms, suppress blocked candidates, or mutate canonical vocabulary data. | config/coefficient_authority.v1.yaml:59:    transform_family: suppression_veto | config/coefficient_authority.v1.yaml:80:        transform_family: suppression_veto

## vocabulary_synonym_audit_check_clean

```bash
env PYTHONPATH=src python scripts/vocabulary_synonym_audit.py --check-clean
```

Exit/status: `0`

stdout: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/vocabulary_synonym_audit_check_clean.stdout`
stderr: `var/audit/active_code_atlas_001/vocabulary_governance_remediation_before_fwd016_20260515/reports/vocabulary_synonym_audit_check_clean.stderr`

Summary: vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False

