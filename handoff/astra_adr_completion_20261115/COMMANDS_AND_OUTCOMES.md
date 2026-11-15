# Commands and actual outcomes

All commands run in /workspace/nvda unless a receipt specifies its disposable receiver or connected WSL host. No product suite was run. This is an execution inventory, not permission to replay product work.

## Intake / source inspection

- `git clone https://github.com/JayDEmily/nvda_29102026.git /workspace/nvda`, `gh auth status`, `git rev-parse HEAD`, `git status --short`, `git fetch origin main`, `git ls-remote origin`: successful; base matches 02a19ae02678824908568d8db08f0e1d015cb861. Branch created with `git switch -c work/astra-adr-governance-recovery-20261115`.
- `cat` / consecutive `sed -n` reads of GUARDRAILS, root AGENTS, tests override, root EXEC_PLAN, proposal files, TEST_AND_PROMOTION_KERNEL, runtime manifests/decisions and scoped inventories; `rg --files`, `rg -l`, `rg -n`, `git ls-tree -r --name-only` to locate sources. Historical ADR and independent PR #16 verdict retrieved using `git show` at 67f5a6c... and e4473ce... respectively. Initial root-path lookup of the ADR and current-tree lookup of the independent verdict failed; exact historical paths/objects were then found and read. Initial nonexistent schemas/test_evidence_ledger.schema.json lookup was corrected to the original planning schema.
- `gh api repos/JayDEmily/nvda_29102026/actions/runs/43677126708`, `gh run view 43677126708 --repo JayDEmily/nvda_29102026 --log`: successful; exact main push CI success, 221 architecture/bootstrap tests, primary output extract retained. No new local architecture aggregate rerun was needed for handoff-only changes.
- `gh release list`, `gh api repos/JayDEmily/nvda_29102026/releases`, `gh release download nvda-l00-transfer-successor-40960483921 --repo JayDEmily/nvda_29102026 --dir /workspace/recovery-assets`, and corresponding older `nvda-m02-l00-recovery-20261030` download: successful. Older archive member inspection and hash-based original-asset comparison retained in OLDER_RELEASE_MEMBERS.json.

## Governance authoring / verification

The first authoring script prepared complete proposed replacements, copied all semantic leaf fields, calculated transitive source/parent-proof dependencies and preserved original case objects. A metadata correction removed a non-schema top-level field and updated proposed repository/test-phase labels before schema validation. Later independent review found the installed-location pointer recurrence; commit 1a564b39 corrected it and refreshed hashes/redlines. Historical source files and active root files were not edited.

- Python `jsonschema.validate` against `handoff/planning/m02_foundation_completion_20261030/TEST_EVIDENCE_LEDGER.schema.json`: passed.
- `git diff --no-index <active> <proposed>`: expected exit 1 for each actual redline, retained as five .diff files; independent reviewer reconstructed exact proposed bytes from each patch.
- `python handoff/astra_adr_completion_20261115/procedures/verify_package.py`: exit 0; JSON/schema, 39/35 identities, no released cases/runs, hashes, 2,281 ref rows, bundle/wheel/probe results and protected path equality passed. VALIDATION_RESULT.json retained.
- `git diff --check`: exit 0. `git diff --exit-code <base> HEAD -- <protected paths>`: exit 0. Independent A review accepted repaired exact SHA, with no remaining important finding; its scope excludes B/product/installation acceptance.

## Recovery commands — complete raw records

`procedures/recovery.py` executed each command in RECOVERY_COMMAND_INDEX.json; full stdout/stderr is retained losslessly in RECOVERY_COMMANDS.json.gz (`gzip -dc` to inspect). Commands include all tip `cat-file`, isolated `update-ref`/`rev-parse`, fetch, per-inventory bundle creation/verification/fresh restoration/ref equality, `git fsck --full --no-reflogs` and baseline/integration ancestry checks. All recorded exit codes are zero. An unborn default HEAD notice from a bare receiver is not a missing supplied ref.

`procedures/original_restore.py` executed the documented original baseline + actual published successor additive restore. ORIGINAL_BUNDLE_RESTORE.json contains every command/output, expected/actual release hash, exact target head/tree, all779-ref comparison and tracked-list equality. All commands exit 0; no forced overwrite. Archive files were read as evidence only. `procedures/assets.py`, older_assets.py and asset_addendum.py generated asset/wheel/member observations, then explicit Git/remote recoveries were added; preserve the committed final inventories rather than treating a fresh raw scan as their replacement.

## Non-product runtime

- `uv --version`: 0.13.6. `uv sync --locked --extra dev`: exit 0, exact CPython 3.13.5 and 14 installed packages; lock resolved15. CI uses uv0.10.0, a disclosed difference.
- `.venv/bin/python procedures/runtime_probe.py` (script initially /tmp/runtime_probe.py): exit 0, all nine storage checks true; Python3.13.5, actual SQLite3.46.1. RUNTIME_OBSERVATION.json retains identities/options/linkage and packages. Disposable temporary database only.
- `uv run python tools/sha_bound_ruff_gate.py`: exit 0; exact51 diagnostics and accepted digest, unchanged verifier. LINT_READBACK.log retained.
- Every wheel ZIP CRC and populated RECORD hash checked; no errors. WHEEL_VERIFICATION.json retains identities and counts.

## Connected host recovery alternatives

Remote Desktop Commander read-only processes used Windows PowerShell/WSL. An initial broad F02 filename search returned unrelated extension filenames and was not treated as evidence of absence. A targeted `find /home/jds /mnt/c/Users/james/Downloads -type f` for F02 ZIP, original baseline archive, SQLite source and libsqlite3 located the original ZIP and archive. `sha256sum` of both gave the exact governing hashes. A bounded maxdepth4 SQLite-name search returned repository evidence paths; it establishes no global asset absence. Remote original ZIP verification is explicitly separate from Cloud transfer.

## Publication

Commits use a purpose-specific branch, ordinary push and draft PR; no main mutation or force push. Publication receipt is in the PR body and final handoff, with exact final SHA. File-by-file GitHub readback is compared by Git blob SHA after push. GitHub Actions on this new PR are reported independently of the already successful merged-main run.
