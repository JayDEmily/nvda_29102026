# D001 independent final acceptance review

Disposition: **accepted for this D001 controlled implementation checkpoint**, conditional on the parent recording and verifying the cumulative full-history checkpoint. No native or provider certification is claimed.

I reviewed the applicable guardrails, repository and test-local instructions, complete accepted execution plan, D001 brief, profile, contract, binding, source and two-case test, together with K01 and the M00 public raw projection. Candidate `efe610c9d70062b719cac33524ef0271ab4ee5d0` passed semantic preflight without a material finding. The implementation consumes the projected R002 timestamp and R003 zone from the M00 public boundary, converts the controlled +11:00 source instant to aware UTC `2026-10-09T13:59:50Z`, retains selected raw lineage and governing versions, and persists an occurrence that the independent read-only SQLite reader returns identically. The reached date-only R002 with R003 refuses materialisation and leaves history empty. The two physical cases assert these distinct branches and durable readback.

The first strict invocation exited 2 at the clean-tree preflight before product collection because the output file was created inside the worktree by redirection. The exact original failure is in `final_initial_failure.log`. `review_round1.md` documents the isolated output-placement repair; no product, proof, test or authority bytes changed. With that failure committed and the worktree clean at `a2b1c6dd24e8219f6059b36634de8a10ea49e8ec`, I reran the **same sole strict aggregate**, directing output outside the worktree until the runner completed. Exact command:

```sh
PYTHONPATH=src NVDA_PROOF_PYTHON=/workspace/scratch/17246e12ecdd/nvda-runtime/bin/python /workspace/scratch/17246e12ecdd/nvda-runtime/bin/python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d001
```

The full, unmodified output is retained in `final_green.log`: exit 0; Python 3.12.14; pytest 9.0.3; precisely 2 collected and 2 passed; aggregate `neutral_market_measurement_truth_d001` in `READY_FOR_PROOF`; authority SHA-256 `bd023e56cbf27f4e2979587fb9e4deb288be329901fd46c7a78897f9b8b4139d`; generation SHA-256 `3c299cc2573ed59bc321021747e042642dec0e85f7d2a463bc0a6064efc4a4c0`; candidate `a2b1c6dd24e8219f6059b36634de8a10ea49e8ec`. No other product tests were run by this reviewer.

This disposition covers the controlled D001 evidence in the accepted plan, including its scoped input and refusal. It does not establish other D signals or native live-market behavior.
