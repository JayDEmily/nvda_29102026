SHELL := /bin/bash
PYTHON ?= python3
AI_PATCH_REPO ?= JayDEmily/nvda10
AI_PATCH_ISSUE ?= 2
AI_PATCH_BASE ?= main
AI_PATCH_REPO_ROOT ?= ../..
AI_PATCH_RUNS_DIR ?= .ai_patch_bridge/runs
AI_PATCH_STATE_DIR ?= .ai_patch_bridge/state
AI_PATCH_POLL_SECONDS ?= 60
AI_PATCH_EXPECTED_CODEX_VERSION ?=
AI_PATCH_LOCAL_CHECK ?= make scaffold-check
AI_PATCH_TARGET_BRANCH ?=
AI_PATCH_SCOPE ?=
AI_PATCH_FILE ?=
AI_PATCH_TRANSPORT ?= auto
AI_PATCH_INLINE_GZIP_BYTE_LIMIT ?= 4096
AI_PATCH_RECEIPT_TIMEOUT_SECONDS ?= 3600
AI_PATCH_RECEIPT_POLL_SECONDS ?= 30
INSTALL ?= $(PYTHON) -m pip install

.PHONY: help install bridge-test test lint format ai-bridge-blueprint-check ai-bridge-proof-executor-check ai-bridge-preflight ai-bridge-self-test ai-bridge-once ai-bridge-watch ai-bridge-watch-on ai-bridge-watch-off ai-bridge-watch-start ai-bridge-watch-stop ai-bridge-watch-status ai-bridge-watch-dashboard ai-bridge-watch-tail ai-bridge-make-example-comment ai-bridge-make-rescue-example-comment ai-bridge-submit-and-wait ai-bridge-scenarios ai-bridge-scenario-a ai-bridge-scenario-b ai-bridge-scenario-c ai-bridge-scenario-d ai-bridge-scenario-e ai-bridge-scenario-f ai-bridge-scenario-g clean

help:
	@echo "Targets:"
	@echo "  make install                  Install package in editable mode with dev deps"
	@echo "  make test                     Run bridge Python tests"
	@echo "  make lint                     Run stdlib compile and bridge hygiene checks"
	@echo "  make format                   Normalise bridge-owned text files"
	@echo "  make bridge-test              Alias for make test"
	@echo "  make ai-bridge-blueprint-check Verify repo-level bridge blueprint doctrine"
	@echo "  make ai-bridge-proof-executor-check Verify manifest proof-block executor doctrine"
	@echo "  make ai-bridge-preflight      Check Python/git/gh/codex/repo readiness"
	@echo "  make ai-bridge-self-test      Run stdlib-only AI_PATCH_V1 encode/decode self-test"
	@echo "  make ai-bridge-once           Process new AI_PATCH_V1 comments once"
	@echo "  make ai-bridge-watch          Poll AI_PATCH_INBOX continuously with raw Python watcher"
	@echo "  make ai-bridge-watch-on       Start resilient logged watcher in background"
	@echo "  make ai-bridge-watch-off      Stop resilient logged watcher"
	@echo "  make ai-bridge-watch-status   Show watcher state, repo state, and recent log"
	@echo "  make ai-bridge-watch-dashboard Refresh watcher status every 5 seconds"
	@echo "  make ai-bridge-watch-tail     Tail watcher log"
	@echo "  make ai-bridge-make-example-comment Build local-codex AI_PATCH_V1 comment example"
	@echo "  make ai-bridge-make-rescue-example-comment Build rescue-branch AI_PATCH_V1 comment example"
	@echo "  make ai-bridge-submit-and-wait Submit one patch, verify transport, then poll receipt"
	@echo "  make ai-bridge-scenarios     Run offline checks for scenarios A-G"
	@echo "  make ai-bridge-scenario-a    Direct GitHub PR lane classification"
	@echo "  make ai-bridge-scenario-b    GitHub Action clean multi-file patch lane"
	@echo "  make ai-bridge-scenario-c    Local Codex tested execution lane"
	@echo "  make ai-bridge-scenario-d    Long sandbox cumulative export lane"
	@echo "  make ai-bridge-scenario-e    Unfinished rescue branch lane"
	@echo "  make ai-bridge-scenario-f    Remote patch-fail to local Codex fallback lane"
	@echo "  make ai-bridge-scenario-g    Linux unavailable rescue branch lane"

install:
	$(INSTALL) -e ".[dev]"

test:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.test_runner

bridge-test: test

lint:
	PYTHONPATH=src $(PYTHON) -m compileall -q src scripts tests
	$(PYTHON) scripts/check_bridge_hygiene.py
	bash -n scripts/watch_control.sh

format:
	$(PYTHON) scripts/format_bridge_text.py

ai-bridge-blueprint-check:
	$(MAKE) -C "$(AI_PATCH_REPO_ROOT)" bridge-blueprint-check

ai-bridge-proof-executor-check:
	$(MAKE) -C "$(AI_PATCH_REPO_ROOT)" proof-executor-check

ai-bridge-self-test:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.cli self-test

ai-bridge-preflight:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.cli preflight \
		--repo "$(AI_PATCH_REPO)" \
		--issue-number "$(AI_PATCH_ISSUE)" \
		--repo-root "$(AI_PATCH_REPO_ROOT)" \
		--state-dir "$(AI_PATCH_STATE_DIR)" \
		--runs-dir "$(AI_PATCH_RUNS_DIR)" \
		$(if $(AI_PATCH_EXPECTED_CODEX_VERSION),--expected-codex-version "$(AI_PATCH_EXPECTED_CODEX_VERSION)",)

ai-bridge-once:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.cli once \
		--repo "$(AI_PATCH_REPO)" \
		--issue-number "$(AI_PATCH_ISSUE)" \
		--repo-root "$(AI_PATCH_REPO_ROOT)" \
		--state-dir "$(AI_PATCH_STATE_DIR)" \
		--runs-dir "$(AI_PATCH_RUNS_DIR)" \
		--local-check "$(AI_PATCH_LOCAL_CHECK)"

ai-bridge-watch:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.cli watch \
		--repo "$(AI_PATCH_REPO)" \
		--issue-number "$(AI_PATCH_ISSUE)" \
		--repo-root "$(AI_PATCH_REPO_ROOT)" \
		--state-dir "$(AI_PATCH_STATE_DIR)" \
		--runs-dir "$(AI_PATCH_RUNS_DIR)" \
		--poll-seconds "$(AI_PATCH_POLL_SECONDS)" \
		--local-check "$(AI_PATCH_LOCAL_CHECK)"

ai-bridge-watch-on:
	AI_PATCH_REPO="$(AI_PATCH_REPO)" \
	AI_PATCH_ISSUE="$(AI_PATCH_ISSUE)" \
	AI_PATCH_REPO_ROOT="$(AI_PATCH_REPO_ROOT)" \
	AI_PATCH_RUNS_DIR="$(AI_PATCH_RUNS_DIR)" \
	AI_PATCH_STATE_DIR="$(AI_PATCH_STATE_DIR)" \
	AI_PATCH_LOCAL_CHECK="$(AI_PATCH_LOCAL_CHECK)" \
	AI_PATCH_POLL_SECONDS="$(AI_PATCH_POLL_SECONDS)" \
	bash scripts/watch_control.sh on

ai-bridge-watch-off:
	AI_PATCH_REPO_ROOT="$(AI_PATCH_REPO_ROOT)" bash scripts/watch_control.sh off

ai-bridge-watch-status:
	AI_PATCH_REPO_ROOT="$(AI_PATCH_REPO_ROOT)" bash scripts/watch_control.sh status

ai-bridge-watch-dashboard:
	AI_PATCH_REPO_ROOT="$(AI_PATCH_REPO_ROOT)" bash scripts/watch_control.sh dashboard

ai-bridge-watch-tail:
	AI_PATCH_REPO_ROOT="$(AI_PATCH_REPO_ROOT)" bash scripts/watch_control.sh tail

ai-bridge-watch-start: ai-bridge-watch-on

ai-bridge-watch-stop: ai-bridge-watch-off

ai-bridge-make-example-comment:
	mkdir -p examples/generated
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.cli make-comment \
		--repo "$(AI_PATCH_REPO)" \
		--base-branch "$(AI_PATCH_BASE)" \
		--target-branch "work/example-ai-patch-bridge" \
		--scope "example AI_PATCH_V1 bridge comment" \
		--patch-file examples/sample_patch.diff \
		--out examples/generated/example_ai_patch_comment.md

ai-bridge-make-rescue-example-comment:
	mkdir -p examples/generated
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.cli make-comment \
		--repo "$(AI_PATCH_REPO)" \
		--base-branch "$(AI_PATCH_BASE)" \
		--target-branch "rescue/example-ai-patch-bridge" \
		--scope "example unvetted sandbox rescue branch comment" \
		--patch-file examples/sample_patch.diff \
		--executor rescue-branch \
		--test-policy rescue_unvetted \
		--out examples/generated/example_rescue_ai_patch_comment.md

ai-bridge-submit-and-wait:
	@test -n "$(AI_PATCH_TARGET_BRANCH)" || (echo "AI_PATCH_TARGET_BRANCH is required" >&2; exit 2)
	@test -n "$(AI_PATCH_SCOPE)" || (echo "AI_PATCH_SCOPE is required" >&2; exit 2)
	@test -n "$(AI_PATCH_FILE)" || (echo "AI_PATCH_FILE is required" >&2; exit 2)
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.cli submit-and-wait \
		--repo "$(AI_PATCH_REPO)" \
		--issue-number "$(AI_PATCH_ISSUE)" \
		--base-branch "$(AI_PATCH_BASE)" \
		--target-branch "$(AI_PATCH_TARGET_BRANCH)" \
		--scope "$(AI_PATCH_SCOPE)" \
		--patch-file "$(AI_PATCH_FILE)" \
		--transport "$(AI_PATCH_TRANSPORT)" \
		--inline-gzip-byte-limit "$(AI_PATCH_INLINE_GZIP_BYTE_LIMIT)" \
		--timeout-seconds "$(AI_PATCH_RECEIPT_TIMEOUT_SECONDS)" \
		--poll-seconds "$(AI_PATCH_RECEIPT_POLL_SECONDS)"

ai-bridge-scenarios:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.scenario_tests

ai-bridge-scenario-a:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.scenario_tests A

ai-bridge-scenario-b:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.scenario_tests B

ai-bridge-scenario-c:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.scenario_tests C

ai-bridge-scenario-d:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.scenario_tests D

ai-bridge-scenario-e:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.scenario_tests E

ai-bridge-scenario-f:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.scenario_tests F

ai-bridge-scenario-g:
	PYTHONPATH=src $(PYTHON) -m ai_patch_bridge.scenario_tests G

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
