# M01 F4 worker internal checkpoint — authorised D134/D135 dependency correction

Date: 09-10-2026. This is **not** an F4 or Stage-1 acceptance candidate.
Authority: Programme-Owner D134/D135 R187 amendment (09-10-2026) overrides only the prohibition on the two specific normative edge changes and their necessary mechanical synchronisation. The accepted calculation mathematics, M00 ownership, GUARDRAILS, AGENTS, and Stage-2 prohibition remain unchanged.

## Proof-first sequence

- Base Git commit: `12e6598`. Historical three-field public-interface failing witness at `450b7e6` (preserved in immutable Git ancestry).
- New discriminating tests committed first at `b0faa71` before the production reconstruction repair. Original red results: `F4_POSITIONAL_CLASS_PROOF_FIRST_RED.log`.
- Subsequent production repair uses a single row-shifting mutation helper for the shared reconstruction and book final-state paths, plus D142's applicable positional state handling; insertion shifts higher rows, deletion shifts them down, and update targets an existing row; invalid required predecessor state is refused.
- D134/D135 authoritative and runtime catalogues now declare `R185;R187;R188;R190`; SHA256 `8045c8c0c4a62fbc3b88759a65b415efb1f0d549764ddbdcae2c5c911cd8a64a`. Units, definitions, kernel IDs and other normative fields remain unchanged.
- The retained D134/D135 witness keeps the original expected values, now supplies explicit `R187=insert` for its positive case. Its earlier three-field red state remains in Git ancestry and the new tests separately prove a missing operation fails closed.
- F1 corrected census: **174 Stage-1 rows**, **144 Stage-1-closed**, **30 cross-stage**, **490 declared edges** (two newly authorised R187 dependencies), plus D007 zero-edge sentinel. Historical 488/489 counts and original catalogue SHA are superseded *as current-state assertions* but retained in prior evidence.
- F4 ledger reconciles historical F2/F3 proof identities to the current 490-edge census, adds precisely D134/R187 and D135/R187, provisionally records bounded F4 proofs and leaves **309 Stage-1-closed edges** requiring additional evidence plus 107 Stage-2-deferred edges. Edge-level evidence is **not** identical to full public proof for every row.

## Exact environmental and verification boundary

- Restored offline Python 3.13 proof virtualenv and PostgreSQL 17.9 portable runtime from provided project archives, with separate M00 and M01 role/schema DSNs, not embedded M00 table reads from M01. Verified command transcripts/logs are in this folder.
- `PYTHONPATH=.:src python -m pytest -q tests/product tests/architecture tests/bootstrap tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py`: **743 passed**. See `F4_REPAIR_POSTGRESQL_COMBINED_743_PASS.log`.
- `PYTHONPATH=.:src python -m pytest -q tests/product/derived_signal/test_m01_f4_positional_book_class.py tests/product/derived_signal/test_m01_f4_depth_snapshot_authority.py`: **9 passed**.
- `PYTHONPATH=.:src python tools/validate_architecture.py`: **PASS**, zero dependency/public-seam violations.
- `python -m ruff check src tests tools`: **All checks passed**.
- `python -m mypy src`: **NOT PASS**, five pre-existing missing `types-PyYAML` stub errors, not observed type errors in modified source. `python -m mypy src --disable-error-code=import-untyped` yields **no issues in 21 source files**, but does not substitute for unmodified full typecheck.
- F1 readback and F4 ledger readback: exited 0 with new digest and counts.
- Separate `tests/product/raw_signal/test_u05_postgresql_durability.py`: one attempted invocation **interrupted by 140-second command timeout**; no fresh pass is claimed. F3 historical M00 durability evidence retained.

## Outstanding obligations and no-admission boundary

- Public end-to-end proof for all 144 Stage-1-closed rows, own-kernel plus lawful fail-closed public proof for all 30 cross-stage rows, and edge-class reconciliation of the remaining 309 Stage-1-closed edges are not completed.
- RC12 unresolved public rows recorded as D131, D137, D138, D141, D142 in current F4 readback. No implication of proven defects from these outstanding proof gaps.
- The repair used controlled positional provider operations consistent with the admitted semantics; it does not claim real native broker message trace conformance without provider-specific input authority evidence.
- Do not request routine independent review of this checkpoint; continue F4 under the existing ExecPlan. F4 and Stage 1 remain unaccepted; Stage 2 unauthorised.
