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

## Unit 5 offline wheelhouse recovery route

**Outcome:** PASS_CONTROL; **BLOCKED_INPUT** pending the two accepted archive bytes.

Implementation commit: `6f8c0ce0851d7a2a3b59974460e8fad74be45256`. The committed-tree targeted validation ran with a clean Git state.

Historical Git evidence recovered the exact external wheelhouse identities used by a prior successful Python 3.13.5 bootstrap:

- runtime: `498ecf4d0a8f895642a017ba8b2bd208271a0d824b7bd007b25980f9a00125d1`, 64,236,501 bytes;
- dev/build: `d71a1f5f22aaaa588a59012833c8d797258ea1505feec37e77d7948c818cc249`, 15,199,214 bytes.

A test-first `make install-offline` route now verifies those identities, safely extracts the archives and executes frozen, offline, no-index, no-cache, non-editable `uv sync` against both wheelhouses. It retains the ordinary installed-package smoke and promotion gates.

```text
test-first: 5 passed, 2 intended failures
post-implementation environment contract: 9 passed
targeted proof-model aggregate: 33 passed
proof_authority=PASS families=195 tests=197 blocks=66
promotion-check=PASS blocks=13 families=13 tests=15
bootstrap missing-input check: exit 2
compileall: PASS
git diff --check: PASS
```

The wheelhouse ZIP bytes are not present in the current checkout or `/mnt/data`; Git history retains evidence but not payloads, and File Library retrieval returned a service error. Therefore no offline installation, installed-package smoke, Black/Ruff, authoritative aggregate or Tier B `.venv` PASS is claimed yet. Exact evidence and continuation commands are in `evidence/UNIT5_OFFLINE_WHEELHOUSE_RECOVERY.md`.


A complete Tier B run on the ambient diagnostic interpreter was also attempted.
It emitted 57 progress markers but did not terminate. An isolated verbose probe
located the stall during subprocess-based proof-executor testing and showed an
ambient `artifact_tool` startup warmup failure before child pytest collection.
No assertion failure was observed. This is diagnostic-environment evidence, not
a Tier B PASS; the complete shadow remains required from the clean `.venv`.


## Unit 5 — Authoritative offline promotion baseline

**Outcome:** PASS

Clean commit: `f66578aa90eb98c6cf0ca2fddd789ac8a014a2df`.

Known true:

- Runtime/support V6 archive SHA-256 `6e4459f4e5508303bdb2e03bcca7701ee72e640f36a716c20b3cd6b0c09b0b42`, 64,398,120 bytes.
- Dev/build V4 archive SHA-256 `d71a1f5f22aaaa588a59012833c8d797258ea1505feec37e77d7948c818cc249`, 15,199,214 bytes.
- Frozen current-lock export installed 38 compatible distributions into a fresh CPython 3.13.5 `.venv`.
- `nvda_desk` imported from `.venv/site-packages`; `uv pip check` passed.
- Aggregate promotion passed 13/13 blocks, 738 tests and zero skips. Evidence hash: `3f029c959915ce29f7ec2626308f34ea3367da4bf742b9197c6950874699d3f6`.
- Complete Tier B shadow passed 82 tests.
- Black passes all 468 scoped files; Ruff reports zero findings.
- Proof authority passes at 195 families / 197 tests / 66 blocks.
- The standalone proof executor now binds env-prefixed Python commands to the current interpreter; all 13 standalone blocks passed under `.venv` pytest 9.0.3.

Exact evidence: `evidence/UNIT5_AUTHORITATIVE_OFFLINE_BASELINE.md`.

## Open next gate

Unit 6: admit M00 C-NORM and the smallest expected-red C-PROOF family. M00 production code remains unstarted.

## Unit 6 — M00 C-NORM and expected-red C-PROOF

**Outcome:** PASS

Known true:

- `M00-FINAL-COMPOSITION-V1` admits nine exact final-composition propositions, `M00-COMP-001` through `M00-COMP-009`.
- Namespace `m00` admits exactly four public-contract terms: `ApplicationCommand`, `ApplicationQuery`, `ApplicationRunReceipt` and `RunCoordinator`.
- The admitted expected-red family contains eight tests: seven reference/ordering/fail-closed/query/mutant checks pass; one production import fails because `nvda_desk.m00_application_shell` is intentionally absent.
- Proof authority reconciles 196 families, 198 tests and 67 blocks.
- Canonical vocabulary builder parity passes 4 tests; proof-authority contract passes 11 tests.
- Changed Python surfaces pass Black and Ruff; `git diff --check` passes.
- No M00 production package or other `src/` file was changed in Unit 6.

Exact evidence: `evidence/UNIT6_M00_C_NORM_EXPECTED_RED.md`.

## Open next gate

Unit 7: implement the bounded M00 Gate D public seam against the admitted expected-red proof without reopening accepted M01–M13 semantics or selecting the quarantined legacy orchestrator.


## Unit 7 — M00 bounded Gate D implementation

**Outcome:** PASS_SOURCE_AND_MODULE_PROOF

Known true:

- The canonical `nvda_desk.m00_application_shell` package exports exactly `ApplicationCommand`, `ApplicationQuery`, `ApplicationRunReceipt` and `RunCoordinator`.
- The M00 coordinator is constructor-injected, stateless between runs and follows the admitted M03→M04→M05/M06→M09→M10→M11 paper path; the separate query path delegates only to M12.
- A contract-package eager-import cycle that prevented order-independent packet-builder import was repaired through lazy named-submodule loading.
- The M00 family is current blocking and the stable promotion set now resolves 14 blocks / 14 families / 16 paths.
- All 14 admitted Tier A blocks pass independently: 754 tests, including 16 M00 tests.
- Complete Tier B passes 83 tests.
- Vocabulary parity passes 4 tests; proof authority passes at 196 families / 198 tests / 67 blocks.
- Black passes 473 scoped files; Ruff reports zero findings; compileall and `git diff --check` pass.

Exact evidence: `evidence/UNIT7_M00_GATE_D_IMPLEMENTATION.md`.

## Open next gate

Unit 8: commit Unit 7, recreate the non-editable installed environment from the accepted wheelhouses, run installed-package smoke, execute and verify the aggregate promotion receipt, rerun Tier B from that environment, reconcile the canonical plan/roadmap and create the final clean checkpoint.
