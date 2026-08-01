SHELL := /usr/bin/env bash

VENV ?= .venv
BOOTSTRAP_PYTHON ?= python3.13
UV ?= uv
PYTHON_VERSION := $(strip $(shell cat .python-version))
PYTHON ?= $(VENV)/bin/python
PYTEST ?= $(PYTHON) -m pytest
PYTHON_PATHS ?= src scripts tests alembic
BLACK ?= $(PYTHON) -m black
RUFF ?= $(PYTHON) -m ruff
INSTALL_STAMP := $(VENV)/.install.stamp
INSTALL_INPUTS := pyproject.toml uv.lock .python-version
PROMOTION_SET ?= alpha_current
PROMOTION_RECEIPT ?= var/proof_receipts/$(PROMOTION_SET).json
RUNTIME_WHEELHOUSE_ZIP ?=
DEV_WHEELHOUSE_ZIP ?=

.PHONY: help
help:
	@printf '%s\n' \
		"venv             create/update .venv using Python 3.13.5" \
		"install          install repo into .venv" \
		"install-offline  install from the accepted offline wheelhouse ZIPs" \
		"compile          compile src and tests without writing bytecode" \
		"installed-package-smoke import the non-editable installed wheel outside the repo" \
		"pr-preflight     install and run PR preflight gates" \
		"test             run pytest suite via .venv" \
		"test-targeted    run TESTS=\"...\" via .venv" \
		"format-check     run Black check without modifying files" \
		"format           run Ruff safe fixes then Black formatting" \
		"lint             run Ruff lint without modifying files" \
		"lint-fix         run Ruff lint fixes" \
		"scaffold-check   verify required repo scaffold exists" \
		"bridge-blueprint-check verify remote bridge blueprint/control doctrine" \
		"proof-executor-check verify manifest proof-block runner surfaces" \
		"persistence-ledger-check verify 5.16 persistence/ledger receipt surfaces" \
			"support-spine-check verify prepared/DMP/review support-spine surfaces" \
		"serial-spine-check verify serial desk-cognition spine surfaces" \
			"capital-deployment-check verify 5.11 downstream capital deployment surfaces" \
		"parallel-risk-check verify 5.8 parallel risk lane surfaces" \
			"financial-calendar-check verify 5.4 financial/event calendar surfaces" \
			"coefficient-modifier-check verify 5.9 coefficient/modifier surfaces" \
			"opening-placement-check verify 5.12 opening/placement readiness surfaces" \
		"proof-block      run scripts/run_proof_block.py with BLOCK=<name>" \
		"promotion-check  validate exact aggregate promotion membership" \
		"promotion-gate   execute PROMOTION_SET and write PROMOTION_RECEIPT" \
		"bridge-on        start AI patch bridge watcher" \
		"bridge-off       stop AI patch bridge watcher" \
		"bridge-status    show AI patch bridge watcher status" \
		"bridge-dashboard live AI patch bridge watcher dashboard" \
		"clean-caches     remove Python/test cache directories"

.PHONY: scaffold-check
scaffold-check:
	@test -f AGENTS.md
	@test -f PLANS.md
	@test -f pyproject.toml
	@test -f .python-version
	@test -d docs
	@test -d src/nvda_desk
	@test -d tests
	@test -f scripts/run_proof_block.py
	@echo "repo scaffold present"

.PHONY: bridge-blueprint-check
bridge-blueprint-check:
	@test -f project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
	@grep -Fq "GitHub is the shared work surface" project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
	@grep -Fq 'Successful automated worker jobs push to `main` by default.' project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
	@grep -Fq "Patch/base mismatch rule" project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
	@grep -Fq "GitHub Actions tarball extraction" project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
	@grep -Fq "GitHub chunked base64 payload transport" project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
	@grep -Fq "Manifest-driven proof-block execution" project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
	@grep -Fq "make proof-block BLOCK=vocabulary_governance_conformance_candidate" project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
	@grep -Fq "make proof-block BLOCK=proof_executor_contract" project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
	@echo "remote bridge blueprint present and key doctrine tokens found"

.PHONY: proof-executor-check
proof-executor-check:
	@test -f scripts/run_proof_block.py
	@test -f config/proof_blocks.yaml
	@test -f tests/tier_b/proof_model/test_proof_executor_contract.py
	@grep -Fq "def _find_block" scripts/run_proof_block.py
	@grep -Fq "def _validate_all_blocks" scripts/run_proof_block.py
	@grep -Fq -- "--check-all" scripts/run_proof_block.py
	@grep -Fq "shlex.split" scripts/run_proof_block.py
	@grep -Fq "subprocess.run" scripts/run_proof_block.py
	@grep -Fq "vocabulary_governance_conformance_candidate" config/proof_blocks.yaml
	@grep -Fq "proof_executor_contract" config/proof_blocks.yaml
	@grep -Fq "test_proof_executor_check_all_validates_manifest_without_running_blocks" tests/tier_b/proof_model/test_proof_executor_contract.py
	@grep -Fq "test_proof_executor_contract_block_is_manifest_owned" tests/tier_b/proof_model/test_proof_executor_contract.py
	@echo "proof-block executor present and manifest contract tokens found"

.PHONY: assert-python
assert-python:
	@$(BOOTSTRAP_PYTHON) -c 'import sys; expected=(3, 13, 5); actual=sys.version_info[:3]; sys.exit(f"Expected Python {expected}, got {actual}: {sys.executable}") if actual != expected else print(f"Python OK: {sys.version.split()[0]} ({sys.executable})")'

.PHONY: venv
venv: $(INSTALL_STAMP)

$(INSTALL_STAMP): $(INSTALL_INPUTS) | assert-python
	$(UV) sync --frozen --extra dev --no-editable --python $(PYTHON_VERSION)
	$(PYTHON) --version
	@touch $@

.PHONY: install
install: $(INSTALL_STAMP)

.PHONY: install-offline
install-offline:
	@test -n "$(RUNTIME_WHEELHOUSE_ZIP)" || (echo "RUNTIME_WHEELHOUSE_ZIP is required" >&2; exit 2)
	@test -n "$(DEV_WHEELHOUSE_ZIP)" || (echo "DEV_WHEELHOUSE_ZIP is required" >&2; exit 2)
	$(BOOTSTRAP_PYTHON) scripts/bootstrap_offline_environment.py \
		--repo-root . \
		--uv "$(UV)" \
		--runtime-zip "$(RUNTIME_WHEELHOUSE_ZIP)" \
		--dev-zip "$(DEV_WHEELHOUSE_ZIP)" \
		--replace-venv


.PHONY: installed-package-smoke
installed-package-smoke: $(INSTALL_STAMP)
	@tmp_dir="$$(mktemp -d)"; \
	trap 'rm -rf "$$tmp_dir"' EXIT; \
	cd "$$tmp_dir"; \
	"$(abspath $(PYTHON))" -I -c 'from pathlib import Path; import sysconfig; import nvda_desk; module=Path(nvda_desk.__file__).resolve(); purelib=Path(sysconfig.get_paths()["purelib"]).resolve(); assert module.is_relative_to(purelib), (module, purelib); print(f"installed-package-smoke=PASS {module}")'

.PHONY: pr-preflight
pr-preflight: install scaffold-check installed-package-smoke format-check lint bridge-blueprint-check proof-executor-check promotion-check

.PHONY: compile
compile: $(INSTALL_STAMP)
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m compileall -q src tests

.PHONY: test
test: $(INSTALL_STAMP)
	$(PYTEST) tests

.PHONY: test-targeted
test-targeted: $(INSTALL_STAMP)
	@test -n "$(strip $(TESTS))" || (echo "Usage: make test-targeted TESTS=\"path/to/test_a.py path/to/test_b.py\"" >&2; exit 2)
	$(PYTEST) $(TESTS)

.PHONY: format-check
format-check: $(INSTALL_STAMP)
	$(BLACK) --check $(PYTHON_PATHS)

.PHONY: format
format: $(INSTALL_STAMP)
	$(RUFF) check --fix $(PYTHON_PATHS)
	$(BLACK) $(PYTHON_PATHS)

.PHONY: lint
lint: $(INSTALL_STAMP)
	$(RUFF) check $(PYTHON_PATHS)

.PHONY: lint-fix
lint-fix: $(INSTALL_STAMP)
	$(RUFF) check --fix $(PYTHON_PATHS)

.PHONY: persistence-ledger-check
persistence-ledger-check:
	@test -f src/nvda_desk/persistence/receipt_ledger.py
	@test -f tests/tier_a/persistence/test_receipt_ledger_surface.py
	@grep -Fq "duplicate receipt_id" src/nvda_desk/persistence/receipt_ledger.py
	@grep -Fq "receipt payload must be JSON-serialisable" src/nvda_desk/persistence/receipt_ledger.py
	@grep -Fq "duplicate position_id" src/nvda_desk/repositories/position_repository.py
	@grep -Fq "duplicate snapshot_id" src/nvda_desk/repositories/capital_state_repository.py
	@grep -Fq "duplicate packet_id" src/nvda_desk/repositories/review_repository.py
	@grep -Fq "persistence_ledgers_receipts_surface" config/proof_blocks.yaml
	@grep -Fq "receipt_ledger_surface" config/retained_test_registry.yaml
	@echo "persistence ledger and receipt surfaces present"

.PHONY: support-spine-check
support-spine-check:
	@test -f src/nvda_desk/contracts/prepared_context.py
	@test -f src/nvda_desk/preparation/context_packet.py
	@test -f tests/tier_a/upstream_cognition/test_prepared_context_packet_surface.py
	@grep -Fq "PREPARED_CONTEXT_DATASCHEMA" src/nvda_desk/contracts/prepared_context.py
	@grep -Fq "fingerprint_prepared_context_payload" src/nvda_desk/preparation/context_packet.py
	@grep -Fq "build_prepared_context_packet" src/nvda_desk/packets/dmp_packets.py
	@grep -Fq "build_review_explanation_packet" src/nvda_desk/packets/dmp_packets.py
	@grep -Fq "missing_review_material" src/nvda_desk/services/review_explanation_service.py
	@grep -Fq "support_spine_prepared_packet_review_surface" config/proof_blocks.yaml
	@echo "prepared ingress / DMP / review support spine surfaces present"

.PHONY: serial-spine-check
serial-spine-check:
	@test -f src/nvda_desk/contracts/serial_spine.py
	@test -f tests/tier_a/serial_recommendation/test_serial_spine_contract_surface.py
	@grep -Fq "SERIAL_SPINE_STAGE_ORDER" src/nvda_desk/contracts/serial_spine.py
	@grep -Fq "validate_serial_stage_order" src/nvda_desk/contracts/serial_spine.py
	@grep -Fq "validate_serial_stage_dependencies" src/nvda_desk/contracts/serial_spine.py
	@grep -Fq "serial_spine_contract" src/nvda_desk/runtime/orchestrator.py
	@grep -Fq "serial_desk_cognition_spine_surface" config/proof_blocks.yaml
	@grep -Fq "serial_spine_contract_surface" config/retained_test_registry.yaml
	@echo "serial desk-cognition spine surfaces present"

.PHONY: external-ingress-check
external-ingress-check:
	@test -f src/nvda_desk/contracts/external_source.py
	@test -f tests/tier_a/adapters_ingress/test_external_source_interface_boundary.py
	@grep -Fq "ExternalSourceInterfaceSpec" src/nvda_desk/contracts/external_source.py
	@grep -Fq "external_network_clients_not_admitted" src/nvda_desk/contracts/external_source.py
	@grep -Fq "forbidden_external_payload_keys" src/nvda_desk/contracts/external_source.py
	@grep -Fq "roadmap_external_source_api_ingress_authority_surface" config/proof_blocks.yaml
	@grep -Fq "external_source_interface_boundary" config/retained_test_registry.yaml
	@echo "external source/API ingress authority-readiness surfaces present"

.PHONY: live-inventory-check
live-inventory-check:
	@test -f src/nvda_desk/contracts/downstream.py
	@test -f src/nvda_desk/downstream/live_inventory.py
	@test -f tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py
	@grep -Fq "LivePositionState" src/nvda_desk/contracts/downstream.py
	@grep -Fq "LiveCapitalState" src/nvda_desk/contracts/downstream.py
	@grep -Fq "InventoryExposureState" src/nvda_desk/contracts/downstream.py
	@grep -Fq "InventoryStateReceipt" src/nvda_desk/contracts/downstream.py
	@grep -Fq "declared_exposure_by_symbol" src/nvda_desk/downstream/live_inventory.py
	@grep -Fq "append_receipt" src/nvda_desk/downstream/live_inventory.py
	@grep -Fq "list_position_records" src/nvda_desk/repositories/position_repository.py
	@grep -Fq "list_snapshot_records" src/nvda_desk/repositories/capital_state_repository.py
	@grep -Fq "live_position_inventory_architecture_surface" config/proof_blocks.yaml
	@echo "live position/inventory architecture surfaces present"

.PHONY: capital-deployment-check
capital-deployment-check:
	@test -f src/nvda_desk/contracts/capital.py
	@test -f src/nvda_desk/capital/authority.py
	@test -f src/nvda_desk/services/capital_deployment_service.py
	@test -f tests/tier_a/capital_deployment/test_capital_contract_models.py
	@grep -Fq "CapitalDeploymentInputTrace" src/nvda_desk/contracts/capital.py
	@grep -Fq "CapitalDeploymentReceipt" src/nvda_desk/contracts/capital.py
	@grep -Fq "downstream_pre_deployment_allowed" src/nvda_desk/contracts/capital.py
	@grep -Fq "build_capital_deployment_receipt" src/nvda_desk/capital/authority.py
	@grep -Fq "evaluate_with_receipt" src/nvda_desk/services/capital_deployment_service.py
	@grep -Fq "downstream_capital_deployment_authority_surface" config/proof_blocks.yaml
	@grep -Fq "capital_deployment_traceability_hardening" config/retained_test_registry.yaml
	@echo "downstream capital deployment authority surfaces present"

.PHONY: parallel-risk-check
parallel-risk-check:
	@test -f src/nvda_desk/contracts/parallel_risk.py
	@test -f src/nvda_desk/risk/parallel/evaluate.py
	@test -f src/nvda_desk/services/parallel_risk_lane_service.py
	@test -f tests/tier_a/parallel_risk/test_parallel_risk_evaluation_surface.py
	@grep -Fq "ParallelRiskInputTrace" src/nvda_desk/contracts/parallel_risk.py
	@grep -Fq "PARALLEL_RISK_FORBIDDEN_AUTHORITY_KEYS" src/nvda_desk/contracts/parallel_risk.py
	@grep -Fq "parallel_risk_hidden_authority_key_rejected" src/nvda_desk/risk/parallel/evaluate.py
	@grep -Fq "parallel_risk_forbidden_authority_consumed" src/nvda_desk/contracts/parallel_risk.py
	@grep -Fq "duplicate observation_id" src/nvda_desk/persistence/parallel_risk_observations.py
	@grep -Fq "parallel_risk_lane_authority_surface" config/proof_blocks.yaml
	@grep -Fq "parallel_risk_lane_authority_hardening" config/retained_test_registry.yaml
	@echo "parallel risk lane authority surfaces present"


.PHONY: financial-calendar-check
financial-calendar-check:
	@test -f src/nvda_desk/contracts/reference_data.py
	@test -f src/nvda_desk/calendar/reference/importer.py
	@test -f src/nvda_desk/calendar/reference/projection.py
	@test -f tests/tier_a/financial_calendar/test_financial_calendar_authority_surface.py
	@grep -Fq "CalendarAuthorityProjectionTrace" src/nvda_desk/contracts/reference_data.py
	@grep -Fq "reference artifact_id" src/nvda_desk/calendar/reference/importer.py
	@grep -Fq "forbidden runtime authority keys" src/nvda_desk/calendar/reference/projection.py
	@grep -Fq "financial_event_calendar_authority_surface" config/proof_blocks.yaml
	@grep -Fq "financial_event_calendar_authority_hardening" config/retained_test_registry.yaml
	@echo "financial/event calendar authority surfaces present"

.PHONY: coefficient-modifier-check
coefficient-modifier-check:
	@test -f src/nvda_desk/contracts/modifiers.py
	@test -f src/nvda_desk/config/coefficient_authority.py
	@test -f tests/tier_a/config/test_coefficient_modifier_replay_surface.py
	@grep -Fq "ModifierReplayReceipt" src/nvda_desk/contracts/modifiers.py
	@grep -Fq "build_replay_receipt" src/nvda_desk/config/coefficient_authority.py
	@grep -Fq "replay_fingerprint" tests/tier_a/config/test_coefficient_modifier_replay_surface.py
	@grep -Fq "dynamic_coefficient_modifier_authority_surface" config/proof_blocks.yaml
	@grep -Fq "dynamic_coefficient_modifier_authority_hardening" config/retained_test_registry.yaml
	@echo "dynamic coefficient/modifier authority surfaces present"

.PHONY: opening-placement-check
opening-placement-check:
	@test -f src/nvda_desk/contracts/downstream.py
	@test -f src/nvda_desk/downstream/opening.py
	@test -f tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py
	@grep -Fq "PlacementReadinessInputTrace" src/nvda_desk/contracts/downstream.py
	@grep -Fq "PlacementHandoffMaterial" src/nvda_desk/contracts/downstream.py
	@grep -Fq "evaluate_placement_readiness" src/nvda_desk/downstream/opening.py
	@grep -Fq "protocol_only" tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py
	@grep -Fq "opening_placement_readiness_surface" config/proof_blocks.yaml
	@grep -Fq "opening_placement_readiness_hardening" config/retained_test_registry.yaml
	@echo "opening/placement readiness surfaces present"


.PHONY: playbook-library-check
playbook-library-check:
	@test -f src/nvda_desk/contracts/playbook.py
	@test -f src/nvda_desk/config/playbook_registry.py
	@test -f src/nvda_desk/playbooks/library.py
	@test -f tests/tier_a/playbook/test_playbook_library_architecture_surface.py
	@grep -Fq "PlaybookDefinition" src/nvda_desk/contracts/playbook.py
	@grep -Fq "PlaybookMetadataReceipt" src/nvda_desk/contracts/playbook.py
	@grep -Fq "hidden playbook authority key rejected" src/nvda_desk/contracts/playbook.py
	@grep -Fq "duplicate YAML key" src/nvda_desk/config/playbook_registry.py
	@grep -Fq "playbook_metadata_receipts" src/nvda_desk/contracts/eligibility.py
	@grep -Fq "playbook_library_architecture_surface" config/proof_blocks.yaml
	@grep -Fq "playbook_library_architecture_surface" config/retained_test_registry.yaml
	@echo "playbook library architecture surfaces present"

.PHONY: exit-close-check
exit-close-check:
	@test -f src/nvda_desk/contracts/exit_close.py
	@test -f src/nvda_desk/downstream/exit_close.py
	@test -f src/nvda_desk/services/exit_close_service.py
	@test -f tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py
	@grep -Fq "ExitCloseInputTrace" src/nvda_desk/contracts/exit_close.py
	@grep -Fq "EXIT_CLOSE_FORBIDDEN_AUTHORITY_KEYS" src/nvda_desk/contracts/exit_close.py
	@grep -Fq "fingerprint_exit_close_replay" src/nvda_desk/contracts/exit_close.py
	@grep -Fq "build_close_handoff" src/nvda_desk/downstream/exit_close.py
	@grep -Fq "replay_exit_close_receipt" src/nvda_desk/downstream/exit_close.py
	@grep -Fq "exit_close_architecture_surface" config/proof_blocks.yaml
	@grep -Fq "exit_close_architecture_surface" config/retained_test_registry.yaml
	@echo "exit/close architecture surfaces present"

.PHONY: proof-block
proof-block:
	@test -n "$(BLOCK)" || (echo "Usage: make proof-block BLOCK=<name>" >&2; exit 2)
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 $(BOOTSTRAP_PYTHON) scripts/run_proof_block.py --block $(BLOCK)

.PHONY: bridge-on bridge-off bridge-status bridge-dashboard watch-status watch-dashboard
bridge-on:
	$(MAKE) -C tools/ai_patch_bridge ai-bridge-watch-on

bridge-off:
	$(MAKE) -C tools/ai_patch_bridge ai-bridge-watch-off

bridge-status:
	$(MAKE) -C tools/ai_patch_bridge ai-bridge-watch-status

bridge-dashboard:
	$(MAKE) -C tools/ai_patch_bridge ai-bridge-watch-dashboard

watch-status: bridge-status

watch-dashboard: bridge-dashboard

.PHONY: bridge watch on off status dashboard
bridge:
	@case "$(word 2,$(MAKECMDGOALS))" in \
		on) $(MAKE) bridge-on ;; \
		off) $(MAKE) bridge-off ;; \
		status) $(MAKE) bridge-status ;; \
		dashboard) $(MAKE) bridge-dashboard ;; \
		*) echo "Usage: make bridge {on|off|status|dashboard}" >&2; exit 2 ;; \
	esac

watch:
	@case "$(word 2,$(MAKECMDGOALS))" in \
		status) $(MAKE) bridge-status ;; \
		dashboard) $(MAKE) bridge-dashboard ;; \
		*) echo "Usage: make watch {status|dashboard}" >&2; exit 2 ;; \
	esac

on off status dashboard:
	@:

.PHONY: clean-caches
clean-caches:
	find . \( -path './.git' -o -path './$(VENV)' -o -path './_archive' \) -prune -o -type d \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.mypy_cache' -o -name '.ruff_cache' \) -prune -exec rm -rf {} +
	find . \( -path './.git' -o -path './$(VENV)' -o -path './_archive' \) -prune -o -type f \( -name '*.pyc' -o -name '*.pyo' \) -exec rm -f {} +

.PHONY: promotion-check
promotion-check:
	$(BOOTSTRAP_PYTHON) scripts/run_promotion_gate.py --set $(PROMOTION_SET) --check-only

.PHONY: promotion-gate
promotion-gate: $(INSTALL_STAMP)
	$(PYTHON) scripts/run_promotion_gate.py --set $(PROMOTION_SET) --receipt $(PROMOTION_RECEIPT)
