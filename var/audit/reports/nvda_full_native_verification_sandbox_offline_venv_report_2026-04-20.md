# NVDA Full Native Verification Report (Sandbox, Offline VENV)
Date: 2026-04-20

## Repo identity

- branch: `work/final-benchmark-reconciliation-promotion-closeout-tranche-v1-20260420`
- HEAD: `b8bb4c72c8d3a08d23f0c70e7d41d78a1b326e3f`

## Mandatory read set completed

Read in full before execution:

- `pyproject.toml`
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
- `docs/05_GUARDRAILS_CORE.md`
- `docs/05.1_GUARDRAILS_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
- `AGENTS.md`
- `migration_prebuild/AGENTS.override.md`
- `tests/AGENTS.override.md`
- `legacy_import/tests/AGENTS.override.md`
- `tests/README.md`
- `tests/tier_a/README.md`
- `tests/tier_b/README.md`
- `tests/tier_c/README.md`
- `config/retained_test_registry.yaml`
- `config/proof_blocks.yaml`
- `/mnt/data/NVDA_two_zip_offline_venv_method_2026-04-17.md`

## Fresh `.venv` creation status

- `.venv` creation: **successful**
- runtime helper acceptance check: **passed** (`runtime install ok`)
- dev supplement acceptance check: **passed** (`dev supplement install ok`)

## Exact environment creation commands

```bash
cd /tmp/nvda_verify/repo/work_api_dto
/tmp/nvda_verify/runtime_bundle/runtime_bundle/bootstrap_runtime_venv.sh /tmp/nvda_verify/repo/work_api_dto
/tmp/nvda_verify/dev_bundle/dev_bundle/bootstrap_dev_supplement.sh /tmp/nvda_verify/repo/work_api_dto
```

Helper-script contents used:

```bash
# runtime
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-index --find-links "$BUNDLE_DIR/wheelhouse" .

# dev supplement
source .venv/bin/activate
python -m pip install --no-index --find-links "$BUNDLE_DIR/wheelhouse" -r "$BUNDLE_DIR/requirements.dev.supplement.lock.txt"
```

## Exact install commands observed

Runtime install:

```bash
python -m pip install --upgrade pip
python -m pip install --no-index --find-links /tmp/nvda_verify/runtime_bundle/runtime_bundle/wheelhouse .
python - <<'PY'
import ibapi, pydantic, sqlalchemy, asyncpg, psycopg, polars, orjson, openai, fastapi, nvda_desk
print('runtime install ok')
PY
```

Dev supplement install:

```bash
python -m pip install --no-index --find-links /tmp/nvda_verify/dev_bundle/dev_bundle/wheelhouse -r /tmp/nvda_verify/dev_bundle/dev_bundle/requirements.dev.supplement.lock.txt
python - <<'PY'
import black, hypothesis, mypy, pytest, ruff
print('dev supplement install ok')
PY
```

## Python version

```text
Python 3.13.5
```

## Package install summary

Observed `pip` inside `.venv` after runtime bootstrap:

```text
pip 26.0.1 from /tmp/nvda_verify/repo/work_api_dto/.venv/lib/python3.13/site-packages/pip (python 3.13)
```

Exact installed package set (`pip freeze`):

```text
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.12.1
asyncpg==0.31.0
black==26.3.1
certifi==2026.2.25
click==8.3.2
coverage==7.13.5
distro==1.9.0
fastapi==0.135.1
greenlet==3.3.2
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
hypothesis==6.152.1
ibapi==9.81.1.post1
idna==3.11
iniconfig==2.3.0
jiter==0.13.0
librt==0.9.0
mypy==1.20.1
mypy_extensions==1.1.0
nvda-desk @ file:///tmp/nvda_verify/repo/work_api_dto
openai==2.29.0
orjson==3.11.7
packaging==26.1
pathspec==1.0.4
platformdirs==4.9.6
pluggy==1.6.0
polars==1.39.2
polars-runtime-32==1.39.2
psycopg==3.3.3
psycopg-binary==3.3.3
pydantic==2.12.5
pydantic_core==2.41.5
Pygments==2.20.0
pytest==8.4.2
pytest-asyncio==1.3.0
pytest-cov==6.3.0
pytokens==0.4.1
PyYAML==6.0.3
ruff==0.15.11
sniffio==1.3.1
sortedcontainers==2.4.0
SQLAlchemy==2.0.48
starlette==0.52.1
tqdm==4.67.3
typing-inspection==0.4.2
typing_extensions==4.15.0
```

## Native test-surface inventory

On-disk pytest-style repo surfaces:

- `tests/tier_a/`: 60 native pytest files on disk
- `tests/tier_b/`: 10 native pytest files on disk
- `tests/tier_c/`: 0 native pytest files on disk
- `legacy_import/tests/`: 221 legacy/source-evidence pytest files on disk

Collected native surfaces under the governed floor (`PYTHONPATH=src pytest -q --collect-only tests/tier_a tests/tier_b`):

- `tests/tier_a/adapters_egress/` — 2 collected tests
- `tests/tier_a/analysis/` — 2 collected tests
- `tests/tier_a/api/` — 4 collected tests
- `tests/tier_a/calendar_operational/` — 2 collected tests
- `tests/tier_a/calendar_reference/` — 3 collected tests
- `tests/tier_a/capital_deployment/` — 5 collected tests
- `tests/tier_a/config/` — 2 collected tests
- `tests/tier_a/downstream_runtime/` — 5 collected tests
- `tests/tier_a/entry/` — 2 collected tests
- `tests/tier_a/ingress/` — 2 collected tests
- `tests/tier_a/legacy_imported/` — 2 collected tests
- `tests/tier_a/migrations/` — 2 collected tests
- `tests/tier_a/modifiers/` — 2 collected tests
- `tests/tier_a/observability/` — 2 collected tests
- `tests/tier_a/options_flow_history/` — 7 collected tests
- `tests/tier_a/packets/` — 2 collected tests
- `tests/tier_a/parallel_risk/` — 5 collected tests
- `tests/tier_a/persistence/` — 5 collected tests
- `tests/tier_a/reference_data/` — 3 collected tests
- `tests/tier_a/review_runtime/` — 3 collected tests
- `tests/tier_a/runtime/` — 1 collected tests
- `tests/tier_a/seam_boundaries/` — 1 collected tests
- `tests/tier_a/serial_recommendation/` — 4 collected tests
- `tests/tier_a/testing_harnesses/` — 2 collected tests
- `tests/tier_a/upstream_cognition/` — 5 collected tests
- `tests/tier_a/vocabulary/` — 7 collected tests
- `tests/tier_b/options_flow_support/` — 2 collected tests
- `tests/tier_b/proof_model/` — 2 collected tests
- `tests/tier_b/review_lineage/` — 9 collected tests
- `tests/tier_b/serial_boundaries/` — 7 collected tests
- `tests/tier_b/upstream_support/` — 2 collected tests

Total collected tests: **104**

## Exact commands run

```bash
cd /tmp/nvda_verify/repo/work_api_dto
source .venv/bin/activate
python --version
python -m pip freeze
PYTHONPATH=src pytest -q --collect-only tests/tier_a tests/tier_b
PYTHONPATH=src pytest -q tests/tier_a tests/tier_b
python3 -m compileall src tests/tier_a tests/tier_b
```

## Exact pass/fail results

Governed floor:

```text
104 passed in 1.57s
```

Collection:

```text
104 tests collected in 0.89s
```

Compileall:

- `python3 -m compileall src tests/tier_a tests/tier_b`
- result: **clean**
- observed outcome: no compile errors emitted

## Skipped or excluded test surfaces

Excluded:

- `legacy_import/tests/` — excluded from native execution because `tests/AGENTS.override.md` says legacy tests under `legacy_import/tests/` are source evidence only, not native authority.
- `tests/tier_c/` — no pytest files present on disk, so there was no runnable native Tier C surface.

Not run separately:

- no additional native pytest-discoverable repo tests were found outside `tests/tier_a/` and `tests/tier_b/` once `.venv/` and `legacy_import/tests/` were excluded from repo-native execution scope.

## Governance / provenance mismatches observed

### 1. Strict offline provenance is not supportable from the provided helper path

The provided offline instruction note and helper runtime script both include:

```bash
python -m pip install --upgrade pip
```

In this sandbox that command reached the configured package index and downloaded `pip-26.0.1` before the wheelhouse-only install began. The runtime log contains:

- `Looking in indexes: https://.../pypi-public/simple`
- `Downloading .../pip-26.0.1-py3-none-any.whl`

That means the runtime bootstrap did **not** remain purely offline end-to-end, even though the repo dependency install itself used `--no-index` and the runtime/dev acceptance imports both passed.

### 2. Test-admission control surfaces disagree about current native proof state

Observed mismatches:

- `tests/README.md`, `tests/tier_a/README.md`, and `tests/tier_b/README.md` still say that no native or no active tests are admitted, but the repo now contains and runs active native Tier A and Tier B pytest files.
- `config/retained_test_registry.yaml` is declared as the single admission authority, but the on-disk/test-collected state does not reconcile cleanly against it.

Tier A files present on disk but **not** in `retained_seed_tier_a`:
- `tests/tier_a/analysis/test_replay_evaluation_surface.py`
- `tests/tier_a/legacy_imported/test_imported_module_containment_surface.py`
- `tests/tier_a/observability/test_observability_reservation_surface.py`
- `tests/tier_a/persistence/test_research_logs_owner_surface.py`
- `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py`
- `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py`

Tier A file(s) present on disk and collected by the governed floor but **absent from the registry entirely**:
- `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py`

Tier A file paths recorded under `tier_b_dispositions` instead of the Tier A admission section:
- `tests/tier_a/analysis/test_replay_evaluation_surface.py`
- `tests/tier_a/capital_deployment/test_capital_deployment_authority_contract.py`
- `tests/tier_a/legacy_imported/test_imported_module_containment_surface.py`
- `tests/tier_a/observability/test_observability_reservation_surface.py`
- `tests/tier_a/options_flow_history/test_options_flow_history_record_contract.py`
- `tests/tier_a/options_flow_history/test_options_flow_history_runtime_replay.py`
- `tests/tier_a/persistence/test_research_logs_owner_surface.py`
- `tests/tier_a/serial_recommendation/test_serial_recommendation_boundary.py`
- `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py`

These disagreements do not change the empirical test result (`104 passed`) but they are still control-surface mismatches that matter for truthful proof admission and receipt law.

## Final judgement

**verification fail**

Reason for fail:

1. the fresh `.venv` was created and the repo dependency surface installed successfully, and the governed proof run itself was green;
2. however, the provided “offline” helper path performed a network-index `pip` upgrade before the wheelhouse-only repo install, so strict offline provenance cannot be claimed from this run;
3. the native test-admission surfaces are not fully reconciled with the actually collected Tier A test tree.

## Bottom line

The runtime/dev installs succeeded, `104` native tests passed, and `compileall` was clean, but the run cannot be truthfully called a fully offline governed verification pass because the helper path upgraded `pip` from an index and the native test-admission surfaces are not fully reconciled.
