# Independent G0/L00 documentary review request — NVDA R2 CHAT_MANUAL

**Review type:** `INDEPENDENT_DOCUMENTARY_ONLY`, before any G1–G4 product implementation or L32 product tests. This request is deliberately **document-only**, not a source archive, wheelhouse, Git bundle, or permission to execute tests or mutate repository.

## Scope and sought decision

Judge whether the Worker has correctly prepared and documented **G0/L00**: owner-approved local R2 governance, full 126-identity coverage, historical proof preservation, 39-leaf/35-obligation accounting, immutable reference tips, exact bundled checkpoint and the pinned CPython 3.13.5 / SQLite 3.54.1 runtime. Decide `ACCEPT_DOCUMENTARY`, `RETURN_FOR_BOUNDED_REPAIR` with one evidenced discrepancy, or `BLOCKED` with missing decisive evidence. Do not treat successful transport or smoke checks as product acceptance. Do not test 27 M02 D-signal implementations; that is reserved for L32.

## Primary authority and documents in this packet

- `GUARDRAILS.md` — read in full, frozen; authoritative precedence and acceptance rules
- `AGENTS.md` and `tests/AGENTS.override.md` — read in full, local owner-approved chat manual; only local Git bundles
- `EXEC_PLAN.md` — read in full, 463 lines, G0 at L00, 39 leaves and L32-only independent product tester
- `pyproject.toml` — CPython exact `==3.13.5` and `[tool.nvda.runtime].sqlite3_version = "3.54.1"`; the SQLite pin is *not a pip dependency*
- `handoff/m02_completion_28_execution/EXECUTION_REGISTER.json` and `TEST_EVIDENCE_LEDGER.json` — no new product-test execution or cases released
- `handoff/m02_completion_28_execution/L00/R2_LOCAL_G0_RECONCILIATION.json` — exact 126/98/28, holds, inventory and ref accounting
- `handoff/m02_completion_28_execution/L00/R2_G0_DOCUMENTARY_STATUS.md` — current Worker-only status
- `handoff/m02_completion_28_execution/L00/R2_SQLITE_RUNTIME_DECISION.md` — source-led SQLite feature decision, earlier mismatch and updated qualification
- `handoff/m02_completion_28_execution/L00/R2_SQLITE_3541_RUNTIME_VERIFIED.json` — official source archive SHA3, exact compiled shared-object SHA-256, compile command, loaded engine/source ID and exact preflight + nine non-product feature results
- `handoff/m02_completion_28_execution/L00/R2_SQLITE_3461_FEATURE_PROBE.json` — preserved preceding 3.46.1 non-product feature result
- `handoff/m02_completion_28_execution/L00/REVIEW.md` and `L00_FINAL_INDEPENDENT_RESTORE_RECEIPT.json` — original **R1** reviewer evidence, attributable to R1 only
- `handoff/m02_remaining_readiness/{COMPLETION_REGISTER.json,UNRESOLVED_REGISTER.json,EXTERNAL_HOLDS.json,EVIDENCE_REUSE.json}` — historical and held identity authority
- `handoff/planning/m02_foundation_completion_20261030/{SIGNAL_COVERAGE_REGISTER.json,LEAF_REGISTER.json,PROOF_ALLOCATION_PROPOSED.json}` — retained full finite scope/case allocations
- `NVDA_R2_G0_SQLITE_FINAL_CANDIDATE_RECEIPT.json` — **external generated review-attachment** after final Git commit, including exact candidate/checkpoint hashes, fresh restore results and file-list manifest. This receipt is *not* part of the commit it fingerprints.

## Runtime and history distinctions

1. Source SHA3-256 must match SQLite's official [release download](https://www.sqlite.org/download.html) and [3.54.1 release notes](https://www.sqlite.org/changes.html), and Python `sqlite_source_id()` must show the 16 October 2026 3.54.1 identity. Compilation uses a separately inventoried, non-Git shared library loaded by `NVDA_SQLITE_LIBDIR` and the tracked `tools/with_pinned_sqlite.sh`. Environment qualification is reproducible from that exact source file and flags; no PostgreSQL requirement.
2. Non-product `sqlite3` feature probe covers the nine explicitly listed storage features; it is **not** a general across-all-data equivalence or an M02 product test. Non-product probe code and logs are not rewritten as accepted product proofs.
3. Original GitHub R2 **tree**, not the missing original GitHub 61-commit lineage, is reconstructed in local Git. The original 66 historical refs remain; exact local additive checkpoint is verified by a fresh baseline-plus-bundle receiver, not GitHub.
4. G1–G4 source/provider/calculation holds remain under downstream leaves; no new domain decisions, case allocations, D145 implementation or policy is being approved by this G0 review.

## Reviewer instructions

Read the included governing files and evidence documents in full; check the numbers, identities, provenance, runtime pin, observed results and fresh transfer receipt against the precise G0 contractual requirements. Do not fabricate code inspection or re-execution from the document-only packet. If a fact fundamentally requires inaccessible source-level evidence, state `UNKNOWN` and request only that evidence, not a broad product test. Return an evidence-bound independent determination for **this exact local candidate**.
