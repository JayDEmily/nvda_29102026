# Unit 5 Offline Wheelhouse Recovery Evidence

Date: 2026-08-01
Branch: `work/m00-testing-guardrail-repair-v1`
Implementation commit: `6f8c0ce0851d7a2a3b59974460e8fad74be45256`

## Outcome

`PASS_CONTROL / BLOCKED_INPUT`

A repository-owned, fail-closed offline bootstrap route now exists. The accepted
wheelhouse archives are not present in the current worker filesystem, so the
locked environment has not yet been created and no authoritative promotion PASS
is claimed.

## Recovered accepted archive identity

Historical Git evidence at commit `f26b09f` records the two external archives
that previously created a Python 3.13.5 environment successfully:

| Archive | SHA-256 | Size |
|---|---|---:|
| `nvda55_runtime_wheelhouse_v5_ibapi_polars1393_py3135_2026-05-02.zip` | `498ecf4d0a8f895642a017ba8b2bd208271a0d824b7bd007b25980f9a00125d1` | 64,236,501 bytes |
| `nvda55_dev_build_support_wheelhouse_v4_black_ruff_pytest_editables_py3135_2026-05-02.zip` | `d71a1f5f22aaaa588a59012833c8d797258ea1505feec37e77d7948c818cc249` | 15,199,214 bytes |

Evidence sources:

```text
git show f26b09f:var/audit/roadmap_5_17/logs/wheelhouse_sha256.txt
git show f26b09f:var/audit/reports/sequence10_review_explanation_route_proof.json
git show f26b09f:var/audit/roadmap_5_17/offline_venv_v4/proof_report.json
```

The prior proof reports successful imports at the current direct dependency
versions, including FastAPI 0.135.1, Polars 1.39.3, psycopg 3.3.3, pydantic
2.12.5, SQLAlchemy 2.0.48, Black 26.3.1, pytest 9.0.3 and Ruff 0.15.11.
Whether the archives contain the complete current transitive `uv.lock` closure
remains unproven until the frozen sync executes.

## Current recovery route

New repository command:

```bash
make install-offline \
  RUNTIME_WHEELHOUSE_ZIP=/mnt/data/nvda55_runtime_wheelhouse_v5_ibapi_polars1393_py3135_2026-05-02.zip \
  DEV_WHEELHOUSE_ZIP=/mnt/data/nvda55_dev_build_support_wheelhouse_v4_black_ruff_pytest_editables_py3135_2026-05-02.zip
```

The command delegates to `scripts/bootstrap_offline_environment.py`, which:

1. requires Python 3.13.5;
2. verifies both accepted archive sizes and SHA-256 values before extraction;
3. rejects ZIP members that escape the extraction root;
4. removes only the repository `.venv`, and only with explicit replacement authority;
5. runs `uv sync --frozen --offline --no-index --no-cache --extra dev --no-editable --no-managed-python` with both extracted wheelhouse directories;
6. runs `uv pip check` against the resulting environment;
7. writes `.venv/.install.stamp` only after those checks pass; and
8. writes an ignored environment receipt under `var/proof_receipts/`.

This route preserves the current lock-owned, non-editable installation law. It
does not restore the older editable install or perform an unpinned pip upgrade.

## Test-first evidence

Before implementation:

```text
5 passed, 2 failed
```

The two intended failures were the absent Make target and absent bootstrap
script.

After implementation:

```text
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/pyvenv/bin/python -m pytest -q \
  tests/tier_b/proof_model/test_environment_control_contract.py
9 passed

PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/pyvenv/bin/python -m pytest -q \
  tests/tier_b/proof_model/test_environment_control_contract.py \
  tests/tier_b/proof_model/test_proof_authority_contract.py \
  tests/tier_b/proof_model/test_promotion_gate_contract.py
33 passed

/opt/pyvenv/bin/python scripts/proof_authority.py --check
proof_authority=PASS families=195 tests=197 blocks=66

make install-offline
RUNTIME_WHEELHOUSE_ZIP is required
exit 2
```

The last command confirms fail-closed input validation; it is not an
installation attempt.

## Retrieval investigation

- The accepted ZIPs are absent from the current checkout and `/mnt/data`.
- Historical Git objects retain hashes, sizes and successful proof, but not the ZIP bytes.
- No pull-request workflow run exists for the historical proof commit, so no GitHub Actions artefact was recoverable through that route.
- File Library search returned a retrieval-service error. This does not establish that the archives are absent from the user's File Library.
- The configured internal Python mirror returns HTTP 404 for required package indexes, and public package hosts are unreachable from this worker.

## Next gate

Attach either exact archive filename variant, including copies with ` (1)` in
the filename. Content identity, not filename, is authoritative. Then execute:

```bash
make install-offline RUNTIME_WHEELHOUSE_ZIP=... DEV_WHEELHOUSE_ZIP=...
make installed-package-smoke
make promotion-gate
.venv/bin/python -m pytest -q tests/tier_b
```

Only those results can close Unit 5 and open M00 C-NORM.

## Diagnostic interpreter limitation observed during validation

A complete Tier B diagnostic attempt on `/opt/pyvenv/bin/python` emitted 57 test
progress markers and did not terminate within the bounded run. An isolated
verbose run of `test_proof_executor_contract.py` passed the first eight tests and
then timed out while a subprocess-based receipt test was starting. Child Python
startup emitted an `artifact_tool` spreadsheet-runtime warmup failure before
pytest collection. No assertion failure was observed before termination.

This is retained as further evidence that the ambient worker interpreter is not
a trustworthy substitute for the clean project `.venv`. The targeted changed
proof-model set remains green; the complete Tier B shadow must be rerun only from
the accepted offline environment before Unit 5 can close.
