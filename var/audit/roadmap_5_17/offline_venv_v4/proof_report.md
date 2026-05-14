# Offline VENV proof report

            Status: `PASS`

            ## Inputs

            - Source TAR: `/mnt/data/NVDA10_LATEST_MAIN_AFTER_ATLAS_VOCAB_WORKFLOW_2026-05-09.tar.gz`
            - Runtime wheelhouse: `/mnt/data/nvda55_runtime_wheelhouse_v5_ibapi_polars1393_py3135_2026-05-02 (1).zip`
            - Dev/build wheelhouse: `/mnt/data/nvda55_dev_build_support_wheelhouse_v4_black_ruff_pytest_editables_py3135_2026-05-02 (1).zip`

            ## Result summary

            - Repo root: `/mnt/data/nvda10_2_work/offline_venv_v4/source`
            - VENV Python: `/mnt/data/nvda10_2_work/offline_venv_v4/source/.venv/bin/python`
            - Polars version observed by import smoke: `1.39.3`

            ## pyproject.toml runtime summary

            ```json
            {
  "dependencies": [
    "asyncpg==0.31.0",
    "fastapi==0.135.1",
    "ibapi==9.81.1.post1",
    "orjson==3.11.7",
    "polars==1.39.3",
    "psycopg[binary]==3.3.3",
    "pydantic==2.12.5",
    "PyYAML==6.0.3",
    "SQLAlchemy==2.0.48"
  ],
  "dependency_count": 9,
  "dev_dependency_count": 3,
  "has_readme_key": false,
  "license": "LicenseRef-Proprietary",
  "optional_dependency_groups": [
    "dev"
  ],
  "parse": "PASS",
  "project_name": "nvda10",
  "project_version": "0.1.0",
  "requires_python": "==3.13.5"
}
            ```

            ## Steps

            - input:source_tar: PASS — /mnt/data/NVDA10_LATEST_MAIN_AFTER_ATLAS_VOCAB_WORKFLOW_2026-05-09.tar.gz
- input:runtime_wheelhouse: PASS — /mnt/data/nvda55_runtime_wheelhouse_v5_ibapi_polars1393_py3135_2026-05-02 (1).zip
- input:dev_wheelhouse: PASS — /mnt/data/nvda55_dev_build_support_wheelhouse_v4_black_ruff_pytest_editables_py3135_2026-05-02 (1).zip
- executable:python: PASS — /opt/pyvenv/bin/python3.13
- executable:uv: PASS — /opt/pyvenv/bin/uv
- extract:source_tar: PASS — /mnt/data/nvda10_2_work/offline_venv_v4/source
- extract:runtime_wheelhouse: PASS — /mnt/data/nvda10_2_work/offline_venv_v4/runtime
- extract:dev_wheelhouse: PASS — /mnt/data/nvda10_2_work/offline_venv_v4/dev
- repo_root_candidate: OBSERVED — score=100 path=/mnt/data/nvda10_2_work/offline_venv_v4/source markers=uv.lock,.python-version,AGENTS.md,PLANS.md,src/nvda_desk,tests,docs
- repo_root_candidate: OBSERVED — score=0 path=/mnt/data/nvda10_2_work/offline_venv_v4/source/tools/ai_patch_bridge markers=PLANS.md,tests,docs,penalty:tools_path
- repo_root: PASS — selected=/mnt/data/nvda10_2_work/offline_venv_v4/source score=100 markers=uv.lock,.python-version,AGENTS.md,PLANS.md,src/nvda_desk,tests,docs
- pyproject_parse: PASS — name=nvda10 requires_python===3.13.5
- wheelhouse_dir:runtime: PASS — /mnt/data/nvda10_2_work/offline_venv_v4/runtime/wheelhouse
- wheelhouse_dir:dev: PASS — /mnt/data/nvda10_2_work/offline_venv_v4/dev/wheelhouse
- create_venv: PASS — exit_code=0
- install_build_support: PASS — exit_code=0
- install_editable_dev: PASS — exit_code=0
- uv_pip_check: PASS — exit_code=0
- import_smoke: PASS — exit_code=0
