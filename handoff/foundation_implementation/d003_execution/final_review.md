# D003 independent final judgement

Reviewer `/root/d003_final_acceptance` examined full governing plan/authority, the exact public M00 R002/R003/R004 and actual D001 sequence, source, codec and the two physical cases. First clean candidate `5a041a8a32ae2e69b10ce9e27240e212d08c9251` returned `RETURN_TO_WORKER`: strict aggregate collected two, success failed on local datetime durable readback, refusal passed, exit 1. Complete first output is `strict_original_failure.log`, SHA256 `412da3be364c2a8e965df7c9c6dfd39faf8537ef5a09673659cbfc1a67bd6773`. The exact observed defect and bounded offset-preserving repair are in `strict_repair.md`; this is an isolated D003 codec defect. No other product proof ran.

On clean repaired candidate `f7aebc77ebe886fbd83516b761f96fc9bfc86b81` the same independent sole executor reviewed the material repair, verified retained original failure and read-only ingress, then invoked the same strict aggregate once under root §5's documented repair exception:

`PYTHONPATH=src NVDA_PROOF_PYTHON=/workspace/scratch/17246e12ecdd/nvda-runtime/bin/python /workspace/scratch/17246e12ecdd/nvda-runtime/bin/python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d003`

The complete copied output is `final_green.log`: exit 0, exactly two collected/two passed, no skips; candidate and authority generation matched. **ACCEPT** controlled D003: exact R004 Australia/Melbourne selects actual same-instant D001 UTC result, retains `ZoneInfo` on ordinary public SQLite read-only reopen; visible unknown R004 refuses without result/history. This does not certify a native exchange IANA source.
