PYTHON ?= python

.PHONY: validate architecture-tests promotion-gate lint

validate:
	$(PYTHON) tools/validate_architecture.py

architecture-tests:
	$(PYTHON) -m pytest tests/architecture tests/bootstrap

promotion-gate:
	$(PYTHON) tools/run_promotion_gate.py --set architecture_kernel

lint:
	ruff check src tests tools
