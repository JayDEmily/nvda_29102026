# D073 - exact first-stage controlled implementation brief

Status: OWNER_APPROVED_SCOPE; INACTIVE_BINDING_REVIEW_PENDING; NO SOURCE OR TEST EXECUTION.
Owning leaf L01a; proof SUP-D073-HISTORY; candidate base a1fc778673e43eab7b0808afa734e15aa7756e7b.

Owner decision: handoff/m02_completion_28_execution/OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json SHA256 6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41.
Independent policy/finite verdict: 1190b50d43755ffd71629d11ba1846894a113771; ACCEPT_EXACT_ALIGNED_HISTORY_JOINT_FIT_POLICY_AND_FINITE34_FOR_OWNER_DECISION.
The following immutable documents are incorporated in full by reference; they establish the exact controlled source, meaning, clocks, roles, literal facts and independent finite oracles. The new brief does not supersede them.
- handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_JOINT_FIT_CONTRACT_AND_REVIEW_20261126.md SHA256 1485a26d4122e821710631cdae49f1f1a0b37990d432edd3a5c57ab1a57b1cef
- handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_SOURCE_POLICY_PROPOSED_20261126.json SHA256 9ba56098c273007980c893db39931ac86e7a3185bbb665f8c3f1e14f99b72af1
- handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_FINITE_SPECIMENS_PROPOSED_20261126.json SHA256 bb03481de75e1820c7aff61777a4a3aa4f676440ec03e373a05c032a0417c76d
- handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_JOINT_FIT_FINITE_CASES_PROPOSED_20261126.json SHA256 3be150f2998b4187a81720b424c848099edeba7a9f638ae90d9aae95d4c5d5c1

## Exact meaning and public seam

ln(current/reference); return; SMH; exact current and prior close anchors, actual original/projection and legal selected corpus.
Append AlignedHistorySourceV1, AlignedHistoryRequestV1, AlignedHistoryOccurrenceV1, AlignedHistoryReadsV1/OwnerV1, create_aligned_history_source, create_aligned_history_owner and create_aligned_history_reader. Each owner/reader exact distinct M02 own brief SHA, signal/profile; underlying sealed source and no predecessor storage; relative ordered concrete SQLiteReadStorageV1 per parent role and no raw source. Exact request fields signal,subject,slot/asof/cutoff,definition/profile/parameter/selection/context refs,ordered predecessor IDs (empty underlying). Occurrence includes owner/admission, request/definition/policy/profile, actual ordered two original+projection pairs or typed nested relative parents, result/units/shape/window, asof/cutoff/calculated. Separate DTO necessary because old WindowMeasurementOccurrenceV1 only retains projection; append-only new route instead of altering old create_window_owner/reader return ABI or codec. Use same checked semantic law live and durable, reconstruct mapping/projection from actual original and exact policy on reopen. Persist actual versioned frame context (id/version/start/end/history_complete_from), parameter set, input selection policy, raw mappings and unit convention in canonical typed or explicit exact-key mapping envelopes, not just an unverified ref/hash. Pure durable validator rechecks all actual retained metadata and original/projection bindings against same policy. Do not widen old API types.

Profile/definition binding (new temporal/IV version names are implementation naming choices within the approved policy):
~~~json
{
  "profile_ref": {
    "id": "t01-l01a-d073-history",
    "version": 1
  },
  "calculation_definition_version": "T01-D073-ALIGNED-HISTORY-DEF-V1",
  "parameter_ref": {
    "id": "t01-l01a-d073-parameters",
    "version": 1
  },
  "selection_ref": {
    "id": "t01-l01a-d073-selection",
    "version": 1
  },
  "subject": "SMH",
  "members": [
    "SMH"
  ],
  "raw_dependencies": [
    "R037",
    "R042"
  ],
  "derived_dependencies": [],
  "kernel": "K03_CHANGE_RETURN",
  "parameter_profile": "P_WINDOW",
  "equation": "ln(current/reference)",
  "units": "return",
  "result_shape": "scalar_decimal",
  "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D073_IMPLEMENTATION_BRIEF.md",
  "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D073_AUTHORITY_BINDING.yaml"
}
~~~

Require actual public M00 ingress/getter/direct projection and complete history. Preserve all required native facts, typed lineage and clocks; apply the exact common selected-corpus/role validators in the adopted policy. No oracle as input, fixture-label pre-refusal, arbitrary reader, private SQL, or legacy codec modification. Ordinary read-only reopen must reconstruct all relevant semantic predicates and first calculation/replay. Exact constructor spellings and proof interface are fixed during independent authoring review before code.

## Changed paths

- src/nvda_desk/market_measurement_truth/api.py (only bounded additive change; shared API and registry serialised)
- src/nvda_desk/market_measurement_truth/_aligned_history_source.py (only bounded additive change; shared API and registry serialised)
- src/nvda_desk/market_measurement_truth/_aligned_history_returns.py (only bounded additive change; shared API and registry serialised)
- src/nvda_desk/market_measurement_truth/_aligned_history_codec.py (only bounded additive change; shared API and registry serialised)
- tools/product_proof_claims.py (only bounded additive change; shared API and registry serialised)
- tests/product/m02_completion_28/support/d073-history/test_profile.py (inert authored source until reviewed registration)
- handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D073_PROOF_CONTRACT.json
- implementation/authority/T01_ALIGNED_HISTORY_D073_AUTHORITY_BINDING.yaml (only exact independently reviewed candidate installation)
- config/product_proof/m02_aligned_history_d073/ (own exact claim/admission/generation/pointer only)
- Owning handoff receipts, execution register and evidence ledger, only this exact jurisdiction.

## Finite scope

Exact 2 owner-admitted physical cases; execution held. No derived predecessor is required by this first-stage profile. All later consumers remain held pending stable committed parent interfaces and independently accepted parent proof before child release.
- SUP-D073-HISTORY-SUCCESS : tests/product/m02_completion_28/support/d073-history/test_profile.py::test_d073_history_success : COMPLETE_EIGHT_FRAME_HISTORY_AND_DURABLE_REOPEN
- SUP-D073-HISTORY-REACHED_REFUSAL : tests/product/m02_completion_28/support/d073-history/test_profile.py::test_d073_late_current : ROW_KNOWLEDGE_SELECTION

All actual fixture, parent, reached-refusal and exact expected result/reopen oracles remain in the pinned inventory. Share mechanical setup without concealing the critical public sequence. Independently review the actual authored proofs, implementation and registration; separate Tester alone may run specifically released cases. No current execution, no other scope, no historical rerun or changed old claims.
