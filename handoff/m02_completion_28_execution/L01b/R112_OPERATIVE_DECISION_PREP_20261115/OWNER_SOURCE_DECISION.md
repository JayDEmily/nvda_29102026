# R112 operative source policy — exact owner decision requested

**Status:** PROPOSAL FOR OWNER DECISION / NOT ADOPTED / NOT SOURCE-ADMITTED.
**Exact upstream independent verdict:** `d6fb895e54ba0a4dae5fffff172fc91014fb51e8` — `ACCEPT_BOUNDARY_PREPARATION_ONLY`.
**Source base:** PR #20 candidate `5be8ee22609e27e765f46437017b1e7cce6c6f2e`; no changes to PR #19's independently accepted documentary source packet.

## Decision to be made

**Recommended bounded decision:** Adopt, solely for the new D091 *controlled synthetic* implementation, the exact R112 source contract in `handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json` (SHA-256 `31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63`), retaining every restrictive field and the independent no-append closed-batch requirement.

This is an **actual new synthetic source/receipt selection policy**, distinct from the five numeric absolute-delta bins already adopted by the installed T01 successor. It must be explicitly approved by the owner and independently reviewed for **operative** admission. A reviewer can inspect that precise decision but cannot invent approval.

For clarity, the decision would adopt **exactly**:

- `R112` only, `t01-controlled-option-delta`, `controlled-option-model-delta/fraction-v1`, model `CONTROLLED_SIGNED_DELTA_V1`, public mapping `t01-controlled-r112-delta` version 1, native `model.delta` with exact `Decimal` `signed_decimal_fraction` unit and identity conversion (no percent-scale guess).
- Exact option identity `contract_id`, `underlying`, `security_type`, `right`, `expiry_date`, `strike`, `currency`, `model_variant`, `scale`, `generation`, `request_id`; specimen synthetic contract `SYNTH-NVDA-OPT-C100-20261120`. This is not an IBKR callback or a real option model.
- `T01-R112-CONTROLLED-FRACTION-1` and `T01-R112-EXACT-RECEIPT-1`: receipt-only, original raw source timestamp absent, exact `received_ts_utc == as_of_utc <= knowledge_cutoff_utc <= calculated_at_utc`, fixed sequence scope `T01-R112-CONTROL/G1`. No fabricated event time or production staleness rule.
- Maximum 64 projected members, page size 8, actual cursor exhaustion and explicit ambiguous-rank refusal. Source batch `T01-R112-CLOSED-BATCH-V1` must be admitted in full **before** selecting and remain exclusively closed against further writes through every page and calculation. The present M00 numeric offset cursor is not a snapshot/seal. No successful selection without an established exclusive control barrier.
- Original raw occurrence readback through M00 public getter to verify true `native_units`, provider/variant, source field, option identity, receipt, sequence, generation and public projection, **not** only mapping-declared units. Raw `NaN` can be transported but not classified; missing/wrong type/nonfinite/out-of-range and metadata/time/history failures refuse.
- The existing five **already-adopted controlled-synthetic** absolute-delta bucket boundaries, with rule-version lineage, remain unchanged. This decision does not create new production bucket policies or another decision about those numbers.

**Not included**: production Greek/model certification, external feed/IBKR access, source timestamp fabrication, modifying frozen GUARDRAILS, admitting a test, changing case budget, making a product-runner compatibility judgement, appointing an independent Tester, implementing D091, merging PR #20/21 or reactivating D145.

## Concrete approval text when the owner chooses to adopt

> I approve operative adoption of the exact controlled-synthetic R112 source policy identified by SHA-256 `31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63`, limited to L01b→L04 D091, including its receipt-only selection and exclusive closed-batch precondition. No product tests, live provider policy or unrelated implementation are released by this approval. Proceed to independent operative source clearance and then the separately gated implementation/proof process.

**No approval has been recorded in this document.** The text above is a proposed, exact scope-bound decision, not a quotation of an existing owner instruction. Once explicit approval exists, bind its actual transcript/source and candidate byte identities in a separate acceptance record. Do not edit the accepted PR #19 packet merely to change a PROPOSED header into ADMITTED.

## Necessary technical follow-through (conditional on approval)

Independently validate source/profile/selection semantics and direct R112 catalogue meaning. Then admit a narrow implementation changed-path/claim/codec contract, prepare exact finite proof mapping, qualify the actual runtime, record sole Tester designation and verify its fresh Git receiver. Only then write bounded product code/unexecuted cases as permitted by installed authority. See accompanying crosswalk/runner documents.

**Authority sources:** root `GUARDRAILS.md`; installed `AGENTS.md`, `EXEC_PLAN.md` §3 L00/L01b/L04 and §4; `handoff/m02_completion_28_execution/L01b/INDEPENDENT_DOCUMENTARY_REVIEW.md`; `handoff/m02_completion_28_execution/L04/D091_INDEPENDENT_REVIEW_20261115/INDEPENDENT_BOUNDARY_VERDICT.md` at review commit; and the exact JSON source contract.
