from pathlib import Path
import os, sys
import pytest
node = 'tests/tier_b/proof_model/test_proof_executor_contract.py::test_proof_executor_exposes_check_mode_in_cli_surface'
out_path = Path('var/audit/active_code_atlas_001/vocabulary_suppression_removal_20260514/reports/tier_b_pytest_os_exit_receipts/proof_executor_nodes/008.stdout')
err_path = Path('var/audit/active_code_atlas_001/vocabulary_suppression_removal_20260514/reports/tier_b_pytest_os_exit_receipts/proof_executor_nodes/008.stderr')
status_path = Path('var/audit/active_code_atlas_001/vocabulary_suppression_removal_20260514/reports/tier_b_pytest_os_exit_receipts/proof_executor_nodes/008.status')
cmd_path = Path('var/audit/active_code_atlas_001/vocabulary_suppression_removal_20260514/reports/tier_b_pytest_os_exit_receipts/proof_executor_nodes/008.cmd')
cmd_path.write_text("PYTHONPATH=src python -m pytest -q " + node + "\n", encoding="utf-8")
with out_path.open("w", encoding="utf-8") as out, err_path.open("w", encoding="utf-8") as err:
    sys.stdout = out
    sys.stderr = err
    code = pytest.main(["-q", node])
    out.flush(); err.flush()
status_path.write_text(str(int(code)) + "\n", encoding="utf-8")
os._exit(int(code))
