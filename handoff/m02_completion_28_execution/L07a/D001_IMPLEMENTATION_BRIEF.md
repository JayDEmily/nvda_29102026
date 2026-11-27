# D001 - exact first-stage controlled implementation brief

Status: OWNER_APPROVED_SCOPE; INACTIVE_BINDING_REVIEW_PENDING; NO SOURCE OR TEST EXECUTION.
Owning leaf L07b; proof SUP-D001-OPTION; candidate base a1fc778673e43eab7b0808afa734e15aa7756e7b.

Owner decision: handoff/m02_completion_28_execution/OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json SHA256 6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41.
Independent policy/finite verdict: 72d3ac7de64c574f8f707bf318825545d2ccd633; ACCEPT_EXACT_OPTION_TIME_POLICY_AND_FINITE23_FOR_OWNER_DECISION.
The following immutable documents are incorporated in full by reference; they establish the exact controlled source, meaning, clocks, roles, literal facts and independent finite oracles. The new brief does not supersede them.
- handoff/m02_completion_28_execution/L07a/OPTION_TIME_CONTRACT_AND_REVIEW_20261127.md SHA256 48d0a8f9533c8781a11b678a440e0874f6bfac76f49f028a1050e39f4ba3b133
- handoff/m02_completion_28_execution/L07a/OPTION_TIME_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json SHA256 14a3ba2308f519d90d11eb450ac484a2c922507b7e04041c740297527a1d847a
- handoff/m02_completion_28_execution/L07a/OPTION_TIME_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json SHA256 14a3ba2308f519d90d11eb450ac484a2c922507b7e04041c740297527a1d847a
- handoff/m02_completion_28_execution/L07a/OPTION_TIME_FINITE_CASES_PROPOSED_20261127.json SHA256 638f8703e75c15b10c2e3772ef7a8ceb0a105a6845140d0e409d50c9a1f01c7f

## Exact meaning and public seam

Actual R002 and R003 true-instant agreement, exact UTC conversion retaining microseconds. Date-only, receipt-only and inconsistent offset refuse after actual source readback.
Narrow new option-time owner/reader and typed source/request/occurrence in public M02 API; explicit frame, contract, policy and profile. No legacy temporal API or codec alteration.

Profile/definition binding (new temporal/IV version names are implementation naming choices within the approved policy):
~~~json
{
  "profile": "t01-option-time-d001/1",
  "definition": "T01-D001-OPTION-TIME-DEF-V1",
  "raw_dependencies": [
    "R002",
    "R003"
  ],
  "derived_dependencies": [],
  "result_type": "aware UTC datetime"
}
~~~

Require actual public M00 ingress/getter/direct projection and complete history. Preserve all required native facts, typed lineage and clocks; apply the exact common selected-corpus/role validators in the adopted policy. No oracle as input, fixture-label pre-refusal, arbitrary reader, private SQL, or legacy codec modification. Ordinary read-only reopen must reconstruct all relevant semantic predicates and first calculation/replay. Exact constructor spellings and proof interface are fixed during independent authoring review before code.

## Changed paths

- src/nvda_desk/market_measurement_truth/api.py (only bounded additive change; shared API and registry serialised)
- src/nvda_desk/market_measurement_truth/_option_time_source.py (only bounded additive change; shared API and registry serialised)
- src/nvda_desk/market_measurement_truth/_option_time.py (only bounded additive change; shared API and registry serialised)
- src/nvda_desk/market_measurement_truth/_option_time_codec.py (only bounded additive change; shared API and registry serialised)
- tools/product_proof_claims.py (only bounded additive change; shared API and registry serialised)
- tests/product/m02_completion_28/support/d001-option/test_profile.py (inert authored source until reviewed registration)
- handoff/m02_completion_28_execution/L07a/D001_PROOF_CONTRACT.json
- implementation/authority/T01_D001_OPTION_TIME_AUTHORITY_BINDING.yaml (only exact independently reviewed candidate installation)
- config/product_proof/m02_option_time_d001/ (own exact claim/admission/generation/pointer only)
- Owning handoff receipts, execution register and evidence ledger, only this exact jurisdiction.

## Finite scope

Exact 4 owner-admitted physical cases; execution held. No derived predecessor is required by this first-stage profile. All later consumers remain held pending stable committed parent interfaces and independently accepted parent proof before child release.
- SUP-D001-OPTION-SUCCESS : tests/product/m02_completion_28/support/d001-option/test_profile.py::test_d001_success : TRUE_INSTANT_UTC_AND_DURABLE_REOPEN
- SUP-D001-OPTION-REACHED_REFUSAL : tests/product/m02_completion_28/support/d001-option/test_profile.py::test_d001_date_only : ACTUAL_R002_TEMPORAL_KIND
- SUP-D001-OPTION-RECEIPT-ONLY : tests/product/m02_completion_28/support/d001-option/test_profile.py::test_d001_receipt_only : ACTUAL_R002_TEMPORAL_KIND
- SUP-D001-OPTION-OFFSET-MISMATCH : tests/product/m02_completion_28/support/d001-option/test_profile.py::test_d001_offset_mismatch : ACTUAL_R002_R003_OFFSET_AGREEMENT

All actual fixture, parent, reached-refusal and exact expected result/reopen oracles remain in the pinned inventory. Share mechanical setup without concealing the critical public sequence. Independently review the actual authored proofs, implementation and registration; separate Tester alone may run specifically released cases. No current execution, no other scope, no historical rerun or changed old claims.
