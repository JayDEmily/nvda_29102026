# M00 Testing Guardrail Repair — Validation Summary

## Unit 1 — Admission authority

**Outcome:** PASS

Known true:

- `config/retained_test_registry.yaml` parses as schema `v4`.
- Its canonical admission model covers all 195 physical `test_*.py` files under Tier A/B/C exactly once.
- Lifecycle totals are 13 current-blocking families, 38 current-nonblocking families, 6 next-gate expected-red families, 63 superseded-compatibility families and 73 historical families.
- The 13 current-blocking module families resolve to exactly 15 physical tests.
- `config/proof_blocks.yaml` parses as schema `v2`; `pre_m00_current` selects those 13 families through 13 proof blocks, with no duplicate family or path membership.
- Every selected block has an exact accepted normative proposition identifier or locator.
- The authority validator rejects duplicate paths, invalid tiers, invalid lifecycles, unknown family references, command/registry membership disagreement and missing proposition locators.

Validation evidence:

```text
python scripts/proof_authority.py --check
proof_authority=PASS families=193 tests=195 blocks=64

python -m pytest tests/tier_b/proof_model/test_proof_authority_contract.py -q
8 passed

python scripts/run_proof_block.py --check-all
proof_blocks_check_all=PASS count=64

python -m pytest tests/tier_b/proof_model/test_proof_executor_contract.py::test_proof_executor_emits_block_header_before_child_output tests/tier_b/proof_model/test_proof_executor_contract.py::test_proof_executor_runs_manifest_commands_without_shell_evaluation tests/tier_b/proof_model/test_checkpoint_receipt_contract.py -q
4 passed

git diff --check
PASS (no output)
```

The complete legacy proof-executor contract was also exercised through 19 of 21 cases in one run before the external 300-second command limit; the final two cases were rerun explicitly and passed. This is recorded as segmented proof rather than represented as one uninterrupted suite result.

## Open next gate

Unit 2: reconcile the single active control state and make the current/legacy API test lifecycles explicit and non-conflicting.

## Unit 2 — Current control and API authority reconciliation

**Outcome:** PASS

Known true:

- Canonical ExecPlan, live roadmap and process overlay identify one active control pack: `PRE-M00-TESTING-GUARDRAIL-REPAIR-V1`.
- The stale M12 active-pack declaration is now retained only as historical programme evidence; it no longer claims current control.
- `tests/tier_a/api/test_fwd005_api_exposure_contract.py` is explicitly `superseded_compatibility` because it requires API-owned mutable CRUD and authority-event state.
- `tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py` is explicitly `next_gate_expected_red` and excluded from the current green claim until its gate opens.
- The registry contains an exclusive `api_state_ownership` claim group. Validation fails if both contradictory families are activated.

Validation evidence:

```text
python -m pytest tests/tier_b/proof_model/test_proof_authority_contract.py -q
11 passed

python scripts/proof_authority.py --check
proof_authority=PASS families=193 tests=195 blocks=64

git diff --check
PASS (no output)
```

## Open next gate

Unit 3: implement the aggregate promotion executor and sufficient tamper-evident receipts.

## Unit 3 — Aggregate promotion gate and receipts

**Outcome:** PASS for the gate implementation and control proof. The first clean full execution remains Unit 5.

Known true:

- `scripts/run_promotion_gate.py` resolves a named promotion set through the reconciled registry/manifest model and executes commands without shell evaluation.
- It refuses dirty pre-run Git state, stops on the first non-PASS block, rejects non-zero exit, zero-pass output, skips and timeouts, and checks post-run Git identity/state.
- Successful or executed-failure receipts include branch/commit, pre/post state, interpreter/platform, `pyproject.toml`/`uv.lock`/`.python-version` hashes, authority-file hashes, exact block/family/test membership, commands, per-block outcomes/counts/durations/output hashes, totals and a deterministic evidence hash.
- Receipt verification detects content tampering.
- `make promotion-check` is non-executing membership validation; `make promotion-gate` is the distinct executing route and writes ignored local evidence under `var/proof_receipts/`.
- The live check resolves 13 blocks, 13 families and 15 tests.

Validation evidence:

```text
python -m pytest tests/tier_b/proof_model/test_proof_authority_contract.py tests/tier_b/proof_model/test_promotion_gate_contract.py -q
22 passed

python scripts/proof_authority.py --check
proof_authority=PASS families=194 tests=196 blocks=65

python scripts/run_promotion_gate.py --set pre_m00_current --check-only
13 proof blocks; 13 test families; 15 test paths

python -m compileall -q scripts/proof_authority.py scripts/run_promotion_gate.py tests/tier_b/proof_model/test_proof_authority_contract.py tests/tier_b/proof_model/test_promotion_gate_contract.py
PASS

git diff --check
PASS (no output)
```

The available diagnostic interpreter does not contain Black, so formatting-tool execution is deferred to the declared-environment repair in Unit 4; no formatting PASS is claimed here.

## Open next gate

Unit 4: make the canonical installation consume `uv.lock`, add an installed-package smoke route, and remove duplicated stale CI schema/count logic.


## Unit 4 — CI and environment authority

**Outcome:** PASS for repository control; local locked installation and installed-package smoke are **BLOCKED_EXTERNAL**.

Known true:

- `make install` now consumes `.python-version`, `pyproject.toml` and `uv.lock` through `uv sync --frozen --extra dev --no-editable`.
- `uv.lock` no longer embeds the private worker package mirror; dependency versions and hashes were retained while registry/file origins were normalised to canonical PyPI hosts.
- `make installed-package-smoke` imports with isolated mode from a temporary directory and proves the imported package resides under the environment's `purelib`, preventing source-tree masking.
- PR CI installs pinned `uv`, uses the locked route, runs the installed-package smoke, repository-owned preflight controls and the aggregate promotion gate. It no longer runs the uncontrolled unsplit suite.
- Remote-patch CI no longer embeds the retired proof schema or hard-coded Tier A count. It runs `make promotion-check`, commits, runs `make promotion-gate` on the clean committed tree and only then pushes.
- The environment-control family is admitted once in the canonical registry and linked to `TP-ENV-001` and `TP-PROMOTION-001`.

Validation evidence:

```text
python -m pytest tests/tier_b/proof_model/test_environment_control_contract.py -q
5 passed

python -m pytest tests/tier_b/proof_model/test_proof_authority_contract.py tests/tier_b/proof_model/test_promotion_gate_contract.py tests/tier_b/proof_model/test_environment_control_contract.py -q
27 passed

python scripts/proof_authority.py --check
proof_authority=PASS families=195 tests=197 blocks=66

YAML parse: both workflows, proof manifest and retained-test registry parsed successfully.
python -m compileall -q scripts tests/tier_b/proof_model/test_environment_control_contract.py
PASS

git diff --check
PASS (no output)
```

Unavailable in the worker environment:

```text
make install
BLOCKED_EXTERNAL_INDEX: configured internal mirror returned HTTP 404 for polars==1.39.3.

UV_INDEX_URL=https://pypi.org/simple uv sync --frozen --extra dev --no-editable --python 3.13.5
BLOCKED_EXTERNAL_DNS: files.pythonhosted.org name resolution failed.
```

No installed-package smoke PASS, Black PASS or Ruff PASS is claimed. Exact sanitised evidence is retained in `evidence/UNIT4_LOCKED_INSTALL_ENVIRONMENT_FAILURE.md`.

## Open next gate

Unit 5: execute the aggregate baseline diagnostically on the available interpreter, while preserving the authoritative locked-environment run as an explicit external roadblock. Do not admit M00 C-NORM until the Unit 5 state is classified.


## Unit 5 — Current pre-M00 promotion baseline

**Outcome:** PASS_DIAGNOSTIC; **BLOCKED_AUTHORITATIVE** by unavailable package sources.

Known true:

- On clean commit `1d657e7c7e5c9f007f22f1c37e5b5c77725630be`, the exact `pre_m00_current` set executed all 13 admitted proof blocks.
- The diagnostic receipt reports 13 passed blocks, 738 passed tests, zero skipped tests, zero failed blocks, unchanged branch/commit and clean pre/post Git state.
- Receipt evidence hash: `54d658bc011a0bf4cb3c488e03c7539c2d358ea383dbc8671584ca76b3c12f2a`.
- Receipt verification passed.
- The complete Tier B shadow passed 78 tests.
- Unit 5 exposed and repaired four aggregate-runner defects: pipe capture, shared process sessions, ambient pytest-plugin admission and unmanaged residual process groups.
- Final targeted control proof passed 29 tests.

Validation evidence:

```text
promotion_gate=PASS set=pre_m00_current blocks=13/13 tests=738
promotion_receipt=PASS var/proof_receipts/pre_m00_current-diagnostic.json
pre/post Git status: clean
pre/post commit: 1d657e7c7e5c9f007f22f1c37e5b5c77725630be
skipped tests: 0

PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/pyvenv/bin/python -m pytest -q tests/tier_b
78 passed in 43.85s

python -m pytest tests/tier_b/proof_model/test_promotion_gate_contract.py tests/tier_b/proof_model/test_proof_authority_contract.py tests/tier_b/proof_model/test_environment_control_contract.py -q
29 passed
```

Limitation:

- The diagnostic receipt identifies `/opt/pyvenv/bin/python`. That interpreter does not match the locked dependency set and therefore cannot establish authoritative environment reproducibility.
- `make install` remains externally blocked as recorded in Unit 4. No substitution is accepted.

Exact evidence is retained in `evidence/UNIT5_DIAGNOSTIC_BASELINE.md`.

## Open next gate

Blocked. Obtain package-source access sufficient for `make install`, then execute `make installed-package-smoke`, `make promotion-gate` and Tier B from `.venv`. Only after those pass may Unit 6 admit M00 C-NORM and expected-red proof.
