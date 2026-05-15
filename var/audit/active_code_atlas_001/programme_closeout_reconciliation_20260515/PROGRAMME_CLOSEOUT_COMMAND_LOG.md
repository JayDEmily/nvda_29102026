# PROGRAMME_CLOSEOUT_COMMAND_LOG

## git_diff_check

Command: `git diff --check`
Exit code: `0`
Duration seconds: `0.154`

Stdout tail:
```text

```

## git_diff_check_final

Command: `git diff --check`
Exit code: `0`
Duration seconds: `0.161`

Stdout tail:
```text

```

## proof_blocks_check_all

Command: `python scripts/run_proof_block.py --check-all`
Exit code: `0`
Duration seconds: `1.904`

Stdout tail:
```text
proof_blocks_check_all=PASS count=46

```

## proof_blocks_check_all_final

Command: `python scripts/run_proof_block.py --check-all`
Exit code: `0`
Duration seconds: `2.095`

Stdout tail:
```text
proof_blocks_check_all=PASS count=46

```

## vocabulary_synonym_audit_clean

Command: `python scripts/vocabulary_synonym_audit.py --check-clean`
Exit code: `0`
Duration seconds: `10.767`

Stdout tail:
```text
vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False

```

## vocabulary_synonym_audit_clean_final

Command: `python scripts/vocabulary_synonym_audit.py --check-clean`
Exit code: `0`
Duration seconds: `7.269`

Stdout tail:
```text
vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False

```

## Batched pytest

Counted batches: `53`
Nonzero: `0`
Tier A passed: `563`
Tier B passed: `49`
No-status attempts not counted: `tests_tier_a_31_vocabulary, tests_tier_b_03_proof_model, tests_tier_b_03_proof_model_rerun`

