# F4 RC03 environment diagnostic (non-normative)

An initial `python -m pytest -q tests/product tests/architecture
tests/bootstrap tests/implementation/derived_signal` under the isolated
offline Python 3.13.5 environment aborted during collection (11 import errors)
because the bootstrap's exact U05 `requirements.lock` did not itself include
the project runtime dependency PyYAML. The error was
`ModuleNotFoundError: No module named 'yaml'`.

PyYAML 6.0.3, matching the root `pyproject.toml`, was restored by copying
the `yaml`, `_yaml` and `pyyaml-6.0.3.dist-info` local installed package
directories from `/opt/pyvenv/lib/python3.13/site-packages` into the isolated
venv (no network and no project mutation). The pinned import then reported
`6.0.3`; a subsequent full test run executed 867 cases.

That subsequent run had 866 pass and one fail solely because inherited
`FORCE_COLOR=1`/`CLICOLOR_FORCE=1` made mypy emit ANSI formatting in a
test that checks its exact diagnostic substring. The *unchanged test*
`tests/architecture/test_static_typecheck.py::test_incompatible_python_visible_public_seam_use_is_rejected`
then passed in the full 867-test rerun after clearing forced colour in the
test environment (`NO_COLOR=1`). The complete 866-pass/1-fail run is in
`F4_RC03_FULL_POSTGRESQL_COMBINED_REGRESSION.log`, and the full successful
run is in `F4_RC03_867_POSTGRESQL_COMBINED_REGRESSION.log`.

Neither observed environment failure was classified as a production defect
or counted as a passing run. No test or production code was changed to
suppress either failure.

PostgreSQL 17.9 was bootstrapped with `fsync`,
`synchronous_commit` and `full_page_writes` enabled, Unix socket transport,
and separate `f4_m00_role` and `f4_m01_role` roles/schema. The suite also
received an administrator DSN for privilege-boundary evidence.

These notes document only execution-environment facts, not programme
acceptance or reproducibility on a different host.
