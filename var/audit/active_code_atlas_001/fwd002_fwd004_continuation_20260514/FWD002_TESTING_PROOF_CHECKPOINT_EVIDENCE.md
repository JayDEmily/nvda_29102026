# FWD-002 — Testing, proof, and checkpoint surfaces evidence

row id: FWD-002
surface name: 5.17 Testing, proof, and checkpoint surfaces
row state after this pass: bounded repair recorded; not closed because the current pass did not complete the closure-grade full authority read required by ROADMAP_LEDGER.md section 14.4 before mutation.

## authority files read

- `AGENTS.md`: full terminal read, lines 1-184.
- `ROADMAP_LEDGER.md`: current pointer and FWD-002 authority sections read by terminal output: lines 1-120 and 621-820.
- `PLANS.md`: substantial terminal read, but not closure-grade full read because tool output ellipsised middle historical/progress sections.
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`: FWD-002-adjacent section read by terminal output lines 407-423 within the 220-423 chunk.
- `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md`: row 5.17 read by terminal output around lines 158-169.
- `docs/08_TESTING_AND_PROMOTION_CORE.md`: proof law was inspected, but not closure-grade full read because the combined terminal output was ellipsised.
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`: terminal read lines 1-13.

## Atlas and Bridge evidence read

Not closure-grade. The pass identified required existing 5.17 receipt directories and ledger rows, but did not fully read all Atlas/Bridge records for this surface.

## source files read

- `scripts/run_proof_block.py`: full terminal read, lines 1-217.
- `src/nvda_desk/downstream/checkpoints.py`: full terminal read, lines 1-58.

## test files read

- `tests/tier_b/proof_model/test_proof_executor_contract.py`: full terminal read before mutation, lines 1-431.
- `tests/tier_b/proof_model/test_checkpoint_receipt_contract.py`: full terminal read, lines 1-65.

## config and fixture files read

- `config/proof_blocks.yaml`: relevant proof-block entries were parsed/inspected for proof/checkpoint/persistence/DMPV3 blocks; file was not displayed in full.
- `config/retained_test_registry.yaml`: not full-read in this pass.
- `tests/AGENTS.override.md`: line count confirmed only; not full-read.

## current behaviour observed

Before repair, a manifest block run with redirected/captured output emitted child process output before the proof block header, because `scripts/run_proof_block.py` printed the block header without flushing before `subprocess.run`.

Pre-repair regression command:

```bash
PYTHONPATH=src python -m pytest -q tests/tier_b/proof_model/test_proof_executor_contract.py::test_proof_executor_emits_block_header_before_child_output
```

Recorded output: `reports/fwd002_proof_executor_ordering_pre_repair_pytest.stdout`; status file records `1`. The failure diff showed actual output order `child-output`, then `proof_block_id=ordered_output_block`, then `command=...`.

## intended behaviour

Proof transcript headers should be emitted before child command output so receipts/transcripts are chronologically coherent and human/audit consumers do not see proof output before the block identity.

## gaps found

- Proof executor output ordering was incoherent under captured/redirected output.
- Closure-grade FWD-002 authority reading was not completed before mutation; this blocks row closure.

## tests added or repaired

Added regression test:

- `tests/tier_b/proof_model/test_proof_executor_contract.py::test_proof_executor_emits_block_header_before_child_output`

## source/config/data changes made

Changed `scripts/run_proof_block.py` to flush the proof block header and command lines before invoking `subprocess.run`.

## commands run

```bash
PYTHONPATH=src python -m pytest -q tests/tier_b/proof_model/test_proof_executor_contract.py::test_proof_executor_emits_block_header_before_child_output
PYTHONPATH=src python -m pytest -q tests/tier_b/proof_model/test_proof_executor_contract.py
python scripts/run_proof_block.py --block proof_executor_contract
python scripts/run_proof_block.py --check-all
git diff --check
PYTHONPATH=src python -m pytest -q tests/tier_b
PYTHONPATH=src python -m pytest -q tests/tier_a
PYTHONPATH=src pytest -q tests/tier_a tests/tier_b
```

## proof outputs

- Pre-repair targeted test: `1 failed` in `reports/fwd002_proof_executor_ordering_pre_repair_pytest.stdout`.
- Post-repair targeted test: `1 passed in 4.47s` in `reports/fwd002_proof_executor_ordering_post_repair_pytest.stdout`.
- Proof executor contract suite: `21 passed in 37.09s` in `reports/fwd002_proof_executor_contract_pytest.stdout`.
- Proof executor block: `21 passed in 37.16s` in `reports/fwd002_proof_executor_contract_proof_block.stdout`.
- Final proof block manifest check: `proof_blocks_check_all=PASS count=46` in `reports/final_proof_blocks_check_all.stdout`.
- Final Tier B: `49 passed in 36.71s` in `reports/final_tier_b.stdout`.
- Final Tier A: `590 passed in 32.60s` in `reports/final_tier_a.stdout`.
- Final combined Tier A+B: `639 passed in 72.10s` in `reports/final_combined_tier_a_tier_b.stdout`.

## remaining blockers

- Closure-grade full read for the full numbered normative stack and row-specific 5.17 Atlas/Bridge/receipt/material set remains incomplete.
- Current manifest was created after mutation, so it records current state but does not prove the required pre-mutation manifest gate.

## Known true / Ruled out / Next gate

Known true: proof transcript ordering had a reproducible failure before repair and targeted proof passed after the flush repair.

Ruled out: no `config/proof_blocks.yaml` ownership-path failure was observed by `python scripts/run_proof_block.py --check-all`.

Next gate: complete closure-grade FWD-002 full authority intake and decide whether any further proof/checkpoint repairs are required before row close.
