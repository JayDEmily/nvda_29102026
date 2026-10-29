PYTHON ?= python

.PHONY: validate architecture-tests promotion-gate validate-implementation-authority typecheck lint

validate:
	$(PYTHON) tools/validate_architecture.py

architecture-tests:
	$(PYTHON) -m pytest tests/architecture tests/bootstrap

promotion-gate:
	$(PYTHON) tools/run_promotion_gate.py --set architecture_kernel

validate-implementation-authority:
	@test -n "$(BINDING)" || (echo "BINDING is required" >&2; exit 2)
	@test -n "$(BRIEF)" || (echo "BRIEF is required" >&2; exit 2)
	$(PYTHON) tools/validate_implementation_authority.py --binding "$(BINDING)" --brief "$(BRIEF)"

typecheck:
	$(PYTHON) -m mypy src

lint:
	ruff check src tests tools
