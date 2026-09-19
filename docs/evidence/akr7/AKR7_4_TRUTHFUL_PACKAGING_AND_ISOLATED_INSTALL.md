# AKR-7.4 truthful packaging and isolated-install evidence

## Scope

AKR-7.4 establishes that the current committed repository builds into truthful wheel/sdist artefacts under its declared packaging authority and that the installed `nvda_desk` package plus declared architecture console scripts resolve from an isolated CPython 3.13.5 environment outside the repository without source-tree path leakage. It does not establish the semantic exclusion/behaviour-neutrality proposition reserved for AKR-7.5.

## Branch and predecessor

- branch: `work/akr-7.4-truthful-packaging`
- predecessor AKR-7.3 commit: `7dc1ee11e7a6336774cc76a9392e1d66c93849b8`

The branch was created directly from the accepted AKR-7.3 committed state.

## Human-read packaging authority

Before interpreting build/install output, the following active surfaces were read:

- `pyproject.toml`
- `src/nvda_desk/__init__.py`
- `src/nvda_desk/architecture/cli.py`
- the current tracked Python source inventory under `src/nvda_desk/`
- the AKR-7.4 acceptance condition in `EXEC_PLAN.md`.

Current packaging authority declares:

- build backend: `hatchling==1.29.0`;
- project: `nvda-architecture-kernel==0.1.0`;
- Python: exactly `3.13.5`;
- sole production dependency: `PyYAML==6.0.3`;
- wheel package root: `src/nvda_desk`;
- five architecture-kernel console scripts;
- an explicit sdist include set covering source, architecture/bootstrap tests, tools, config, schemas, templates, architecture/history documents and root control/metadata files.

## Offline build

The build was executed from a clean committed repository using the admitted local build/dependency surface:

```text
UV_OFFLINE=1 UV_PYTHON_DOWNLOADS=never \
  uv build --offline --out-dir /mnt/data/akr7_4_dist
```

Observed artefacts:

```text
nvda_architecture_kernel-0.1.0-py3-none-any.whl
sha256 5bc7e5ad6fa7da1fdcc1cb171cbcb85e6ebb761ca25d21d2a14b77139f65d074

nvda_architecture_kernel-0.1.0.tar.gz
sha256 2d9596841554a592f575c02bdff523aee6e897fa8e07ca4218bcd7690ebaea30
```

The sdist hash differs from an earlier volatile execution because the current rehydrated branch carries a different, newly committed AKR-7.3 progress/evidence record in `EXEC_PLAN.md`; the wheel source payload is unchanged and retains the same hash.

## Wheel inspection

The wheel contains 18 files total. Its package payload is exactly 13 Python files:

```text
nvda_desk/__init__.py
nvda_desk/architecture/__init__.py
nvda_desk/architecture/allocation.py
nvda_desk/architecture/cli.py
nvda_desk/architecture/dependencies.py
nvda_desk/architecture/identifiers.py
nvda_desk/architecture/implementation_authority.py
nvda_desk/architecture/promotion.py
nvda_desk/architecture/proof.py
nvda_desk/architecture/registry.py
nvda_desk/architecture/schema.py
nvda_desk/architecture/validation.py
nvda_desk/composition/__init__.py
```

The remaining five entries are package metadata/licence/record files. Direct byte comparison established:

```text
wheel_python_files 13
wheel_python_inventory_matches_source True
wheel_source_byte_mismatches []
```

The wheel metadata states:

```text
Requires-Python: ==3.13.5
Requires-Dist: pyyaml==6.0.3
```

Development-only requirements are emitted only under the `dev` extra. `entry_points.txt` contains exactly the five declared architecture-kernel commands:

```text
nvda-check-dependencies
nvda-check-public-seams
nvda-promotion-gate
nvda-validate-architecture
nvda-validate-implementation-authority
```

## Sdist inspection

The sdist contains 89 files. Every member whose relative path corresponds to a tracked repository file was compared byte-for-byte with the current repository:

```text
sdist_files 89
sdist_repository_byte_mismatches []
sdist_nonrepository_files ['PKG-INFO']
```

`PKG-INFO` is the sole generated/non-repository file and reports the same Python/runtime dependency metadata as the wheel. The complete inventory was inspected before isolated installation.

## Isolated installation

A new environment was created outside the repository with the declared interpreter:

```text
/opt/pyvenv/bin/python3.13 -m venv /mnt/data/akr7_4_install_env
/mnt/data/akr7_4_install_env/bin/python -m pip install \
  --no-index \
  --find-links=/mnt/data/nvda_akr7_rehydrated/vendor/wheels \
  /mnt/data/akr7_4_dist/nvda_architecture_kernel-0.1.0-py3-none-any.whl
```

Only the wheel and admitted local `PyYAML==6.0.3` dependency were installed.

From `/mnt/data/akr7_4_outside`, with `PYTHONPATH` removed, `sys.path` did not contain the source repository. All 13 package modules imported from:

```text
/mnt/data/akr7_4_install_env/lib/python3.13/site-packages/nvda_desk/...
```

No imported package module resolved from the repository checkout.

Each declared console script existed under `/mnt/data/akr7_4_install_env/bin/` and independently resolved its installed command surface with `--help` while `PYTHONPATH` was unset.

## Semantic acceptance boundary

The built wheel is an exact representation of the current 13-file `nvda_desk` Python source payload plus standard packaging metadata. The sdist is an exact representation of the declared included repository surfaces plus generated `PKG-INFO`. The wheel installs into an external environment and all retained package modules and declared architecture command entry points resolve without source-tree path injection.

This establishes AKR-7.4 packaging/installability only. AKR-7.5 must still determine whether the retained active tree and these built artefacts are semantically behaviour-neutral and free of prohibited programme/domain machinery.
