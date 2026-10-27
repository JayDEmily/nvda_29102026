# L04 reached baseline — public discovery invariant FAILED

Reviewer and sole strict executor `/root/l04_independent_review`, 27 October
2026. Observed clean candidate
`0617c7bf184f89353b78fe90210bc188099561af` before and after the strict run;
immutable generation3 SHA256
`d3b58bfeb1684138b73db35a9a21c4d5bf424aa3b7f9fc856ffe7966ef5dd504`.

Command: `PYTHONPATH=src /workspace/scratch/ad31885d756b/m00-env/bin/python tools/run_product_proof_gate.py --aggregate m00_brief2`.
Full original external output: `/workspace/scratch/ad31885d756b/l04-baseline-red.log`.
Observed **35 passed /1 failed in86.04s**, aggregate exit1. No repository
mutation occurred during execution.

The control case admitted four A4 depth observations, all five separately
identified controls and six counterfacts. Each control's known-ID full typed
readback and absent public R187 projection succeeded. The first required
generic discovery call, supplied only subject/source/request/generation/
exchange/cutoff selectors, failed at `tools/m00_fixture_io.py:356`:
`AttributeError: '_ReadsV1' object has no attribute 'list_raw_observation_history'`.
Thus known-ID persistence does not establish required N08/N09/N15 public
enumerability. Later control assertions were not reached and are not claimed
as baseline passes. All retained native/history cases passed.

**Diagnosis, ISOLATED:** current public facet has known-ID observation reads
and projected R history, with no generic observation enumeration; controls
correctly have no invented R role. Existing owner-private received-between
enumeration establishes an implementation path, but is not a public consumer
substitute. The failed invariant is public ordered control discovery, not
native control admission or malformed source fields. The mechanism differs
from L02's datetime persistence defect and the closed L02/L03 typed-fresh proof
adequacy class; no recurrent runtime mechanism is asserted.

Preserve this original result. Downstream L05 remains dependent on L04. The
owner-commissioned brief permits the bounded additive correction only after
independent approval of its exact compatibility/ownership contract. That
separate approval is recorded in CONTRACT_REVIEW.md. Do not rewrite the proof,
positive fixtures, oracle, old tests or immutable generation to obtain green.
