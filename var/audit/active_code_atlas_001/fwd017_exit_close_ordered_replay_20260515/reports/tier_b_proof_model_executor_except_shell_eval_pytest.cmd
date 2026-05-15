PYTHONPATH=src python -m pytest -q tests/tier_b/proof_model/test_proof_executor_contract.py -k "not test_proof_executor_runs_manifest_commands_without_shell_evaluation"
