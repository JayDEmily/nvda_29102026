PYTHONPATH=src python -c 'import os, pytest; code=pytest.main(["-q", "tests/tier_b"]); os._exit(code)'
