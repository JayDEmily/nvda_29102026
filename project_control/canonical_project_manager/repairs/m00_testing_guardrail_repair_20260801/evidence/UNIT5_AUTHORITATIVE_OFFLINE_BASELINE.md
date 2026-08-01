# Unit 5 Authoritative Offline Baseline

**Outcome:** PASS
**Clean commit:** `f66578aa90eb98c6cf0ca2fddd789ac8a014a2df`
**Branch:** `work/m00-testing-guardrail-repair-v1`

## Accepted environment inputs

- Runtime/support wheelhouse V6: SHA-256 `6e4459f4e5508303bdb2e03bcca7701ee72e640f36a716c20b3cd6b0c09b0b42`, 64,398,120 bytes.
- Dev/build wheelhouse V4: SHA-256 `d71a1f5f22aaaa588a59012833c8d797258ea1505feec37e77d7948c818cc249`, 15,199,214 bytes.
- Python: CPython 3.13.5.
- `uv.lock`: SHA-256 `ec501a74c614777a8cc4da3495cc89b92bb311bfcae03ebd3e4416c6bbd31845`.

The uploaded May archives were authentic. The runtime V5 archive was incomplete for the current lock. V6 retains the accepted V5 payload, removes superseded `greenlet==3.2.5`, and adds `greenlet==3.5.0`, `openpyxl==3.1.5`, and `et-xmlfile==2.0.0`. The exact V6 archive identity is pinned by the repository bootstrap.

## Installation proof

`scripts/bootstrap_offline_environment.py` now:

1. verifies the two outer ZIP hashes and byte sizes;
2. rejects unsafe ZIP paths;
3. exports exact environment pins from the frozen current `uv.lock`;
4. creates a fresh CPython 3.13.5 `.venv`;
5. installs dependencies offline with no index or cache from the accepted wheelhouses;
6. installs exact build support;
7. installs the repository non-editably without dependency re-resolution;
8. runs `uv pip check`; and
9. writes a receipt containing Git, lock, archive and command identity.

Observed result: 38 compatible installed distributions. `nvda_desk` imported from `.venv/lib/python3.13/site-packages`, not the source tree. The clean environment receipt records commit `f66578a`, branch identity and `dirty: false`.

## Promotion and shadow proof

- Aggregate promotion: 13/13 blocks passed.
- Tier A tests through the admitted set: 738 passed, zero skipped.
- Promotion evidence hash: `3f029c959915ce29f7ec2626308f34ea3367da4bf742b9197c6950874699d3f6`.
- Tier B shadow: 82 passed.
- Proof authority: 195 families, 197 tests, 66 blocks.
- Installed-package smoke: PASS.

## Style and executor guardrails

The first authoritative tool run revealed a permanently red style baseline: 145 Black files and 135 Ruff findings. A separate mechanical unit established a clean baseline across 468 scoped Python files. Remaining Ruff issues were reviewed individually; no blanket suppression was added.

The standalone proof executor also failed to replace `python` when it followed an `env KEY=value` prefix, allowing ambient interpreter leakage. A test-first repair now binds `python`, `python3`, or `python3.13` to `sys.executable` in both direct and env-prefixed commands. All 13 standalone blocks then passed under pytest 9.0.3 from `.venv`.

## Classification

Unit 5 is authoritative PASS. The package-source and wheelhouse roadblocks are closed. M00 production code remains unstarted. Unit 6 may now admit M00 C-NORM and expected-red C-PROOF.
