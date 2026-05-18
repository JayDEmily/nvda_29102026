# Command log — PRL minute profile contracts 001

```sh
rm -rf /mnt/data/prl_contracts_work
mkdir -p /mnt/data/prl_contracts_work
tar -xzf /mnt/data/prl-minute-risk-profile-plan-branch.tar.gz -C /mnt/data/prl_contracts_work
cd /mnt/data/prl_contracts_work/MVD-A10_1704_V1
git status --short --branch
git branch --show-current
git log --oneline -5
git checkout -B work/prl-minute-profile-contracts work/prl-minute-risk-profile-plan
wc -l AGENTS.md PLANS.md ROADMAP_LEDGER.md docs/planning/PRL_MINUTE_RISK_PROFILE_IMPLEMENTATION_PLAN.md
python - <<'PY'
# read required governance files fully and write FULL_READ_MANIFEST
PY
grep -RInE "vocabulary|dictionary|lexicon|glossary|normative wording|controlled language|plain English|review language|explanation language" docs src tests config schemas project_control evidence_index > var/audit/prl_minute_profile_contracts_001/vocabulary_search.txt
find docs data config -iname '*.xlsx' -o -iname '*.xlsm' -o -iname '*.xls'
python - <<'PY'
# inspect signal workbook names and sheets using openpyxl without editing workbook
PY
```

## Gate 2 test-first command

```sh
cat > tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py <<'PY'
# new contract tests for PRL-MRP-001/002
PY
pytest tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py -q || true
```

Observed pre-implementation result: collection error because `AuthorityFlags` is not yet exported from `nvda_desk.contracts.parallel_risk`; this is the expected new-contract failure before implementation.
## Gate 3 implementation command
```sh
python - <<PY
# inserted contract-only models/enums into src/nvda_desk/contracts/parallel_risk.py
PY
python -m pytest tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py -q
```

Observed implementation result: `14 passed` for new contract tests after contract-only model additions.
