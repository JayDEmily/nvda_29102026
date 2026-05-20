# FWD-011 reopened rows — test-first receipt

Reopened rows assessed: `75`.

Result: no new test file was required because every reopened row has existing native test evidence with exact file/range references in the implementation-status ledger. Expected pre-source failure is not applicable for rows closed as pre-existing native satisfaction.

Targeted proof command: `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/playbook tests/tier_b/serial_boundaries/test_playbook_eligibility_decontamination.py`

Targeted proof status: `0`.
