# L00/runtime/Tester readiness — evidence and outstanding binding

**Scope:** Read-only evidence collection for the next D091 admission decision, NOT runner qualification or a new checkpoint transport strategy. Candidate Git base: 07f8140fd9306e51b05f241b02341a2b14579bc2; independently reviewed design 05f6b4b707c6231dc9b4d54a4a6cb626711808de.

## Directly observed current Ubuntu candidate

Ubuntu host: DESKTOP-I188O30, WSL distribution Ubuntu. On 16 November 2026 read-only Python/SQLite metadata inventory at /home/jds/nvda_d091_proof_admission_20261116 and /home/jds/nvda_uv3135_20261112/.venv/bin/python:

- CPython 3.13.5, binary resolved to /home/jds/nvda_uv3135_20261112/.uvpython/cpython-3.13.5-linux-x86_64-gnu/bin/python3.13; SHA-256 0eba26d5f04a3673ee264ca406ef286d5025da098c1a24987a8118c23d69153c.
- Python sqlite3 version **3.49.1**, source ID `2025-02-18 13:38:58 873d4e274b4988d260ba8354a9718324a1c26187a4ab4c1cc0227c03d0f10e70`. This environment has **not** been identified as loading the historical `libsqlite3.so.0` 3.54.1. The earlier isolated nine-mechanism probe in the separate previous handoff is explicitly **non-product**.
- Relevant package metadata in this interpreter: pytest 9.0.3, Ruff 0.15.11, mypy 1.20.1, PyYAML 6.0.3, psycopg 3.3.4. This package-list probe did not import NVIDIA product code. Hatchling not found as an installed distribution in the selected interpreter; that is not evidence that the project build requires installing it or that a product runtime must fail.
- Repository lock/config SHA-256 at candidate: `uv.lock` 65800a98bc9f14fd7df23aac7206fe90d9d3c73c9b221bfbe7e90a4092c3290d; `pyproject.toml` c62bb0b0cbc96707de3444037a2e628c95cac75ebf8b44ebb0a5ebc9e5296225; `.python-version` e72b03ed5b70312f2782f2b05055c55b24670e126d50e24c4f2c559bf288f810.
- Git show-ref lines 289 at this local checkout; this is **not** an independent 66-name/tip historical receiver proof, nor complete restoration of non-Git archives. No product tests run.

The non-product metadata is also retained as RUNTIME_METADATA_OBSERVATION.json with full compile options. A separate historical `handoff/astra_adr_continuation_20261115/SQLITE_3541_BUILD_AND_PROBE.json` reports 3.54.1 from an unrelated /workspace executable/library SHA-256 c53706980906943301153b630aeddba1b4aab6fe5eeda5752d8293952707db4e. Do **not** claim 3.49.1 equals 3.54.1 or that a standalone mechanism check qualifies D091.

## L00 transfers and actual necessary assets

Existing `handoff/astra_adr_continuation_20261115/OUTSTANDING_ASSETS_CURRENT.json` records historical missing or byte-mismatched archives and a separate historical CPython3.12.14 toolchain gap. Their exact applicability to the selected **D091** candidate and finally adopted transport must be **independently established** before diagnosing an active product blocker. The prospective pinned GitHub checkpoint plan calls for verifying exact original 66 names/tips, candidate tree, expected other historical refs, full Git closure, required non-Git asset hashes and a distinct Tester receiver; the main/Worker local worktree count is not that verification.

Current blocker to **product entry** is the *absent independent exact D091 candidate receiver acceptance and scope-specific necessary-assets disposition*, not an unverified assertion that every older mismatched archive is required. There is no new owner-adopted special checkpoint method in this packet. A reviewer should identify the exact required file/ref, not copy over all historical gaps indiscriminately.

## Claim/generation and role

The directly inspected active `TEST_EVIDENCE_LEDGER.json` M02-C28-D091 row retains source `UNRESOLVED_BIND_AT_L04`, `test_allocation.authorised_case_count=0`, `hard_ceiling=0`, `execution.runs=[]` and `SEPARATE_INDEPENDENT_TESTER_NOT_YET_DESIGNATED`; original `PROOF_ALLOCATION_PROPOSED.json` names only two cases, historical proposed hard ceiling six.

No new D091 claim/generation file exists in the inspected `config/` tree at candidate. The existing `tools/product_proof_claims.py`, versioned proof controls and typed category record require specific future accepted generation/pointer bindings; choose the exact path only after independent review of the currently installed claim schema. Do **not** create a speculative new config claim or silently modify an accepted historical one.

Select and qualify the actual **independent strict Tester** with fresh receiver. An available ChatGPT Worker/Reviewer cannot self-designate as that Tester. No test execution schedule is released by this packet, including G1_AFTER_L06. Independent design review and green CI prove neither a product-qualified SQLite runner nor product test approval.
