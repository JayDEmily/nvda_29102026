timeout 30s env PYTHONPATH=src python -m pytest -q 'tests/tier_b/proof_model/test_proof_executor_contract.py::test_proof_executor_check_validates_manifest_without_running_block'
