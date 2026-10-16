# D117 — owner-approved raw-volume-history dependency amendment

**Revision:** `D117-RAW-VOLUME-HISTORY-20261016-01`.

**Decision:** APPROVED by the programme owner, 16 October 2026 — Australia/Melbourne.

## 1. Exact decision and reviewed baseline

The assistant presented the six exact proposed clauses in `handoff/workbook_v2/gates_01_02/G2_D117_SOURCE_ROLE_REASSESSMENT_AND_DECISION_20261016.md` §4 and asked: **“Do you approve D117-RAW-VOLUME-HISTORY-20261016-01?”** The programme owner answered in this thread: **“Yes, I do proceed.”** This is approval of that bounded correction and instruction to continue planning, not worker self-acceptance.

- Reviewed commit: `ca11e1aa683e6561150d1c809f7af88162eaca7c`.
- Reviewed tree: `559f8d39f0b673ec736da7964c27d35ad2ffe748`.
- Proposal SHA-256: `112b7e0a83c8a5bd85896855e04be13148042f164968c08cac8694cf18f762fa`.
- Receiving branch: `work/v2-g2-d117-approved-history-contract-20261016`.

The reviewed proposal remains byte-unchanged as a pre-acceptance snapshot. This subsequent owner decision supersedes its proposed/not-accepted status only for its six named clauses.

## 2. Accepted clauses

1. Change D117's effective direct raw dependencies only from `R041;R075` to `R041`; retain no D predecessor. R041 denotes current and required historical volume occurrences, not only a single latest value.
2. Preserve K04's sample-mean/sample-standard-deviation z-score, current-observation exclusion, knowledge cutoff and invalid/missing-history refusal. Preserve P_BASELINE, the catalogue's `20-60 sessions` and its matching time-of-day/contract/delta/expiry requirements. No integer horizon, new bucket rule, selector or coefficient is chosen by this amendment. These still require exact, immutable, non-strategy source/selection specification before unqualified classification.
3. R075 retains its raw meaning and identity and remains available for separately authorised uses. It is not redefined, relabelled as open interest, or replaced with a fabricated raw sample.
4. Supersede **only for D117** the D116 correction's statement retaining its mandatory R075 dependency. Preserve the D116 correction, arithmetic, right-conditional open-interest dependencies and every unrelated D/R rule.
5. Record approval as a semantic overlay if accepted. Leave frozen catalogue/workbook/runtime bytes unchanged during Gate 2. Later authorised C–E work must synchronise the normative/runtime catalogue and its hash binding, adjust lawful materialisation/lineage and test expectations, and independently prove the revised input contract. Do not delete tests to obtain green or claim that the existing fixture certifies the new contract.
6. Acceptance of this proposed revision is not Gate 2 acceptance, D117 implementation acceptance, source admission or final M02 allocation. Reassess D117 after the remaining baseline-selection semantics are established; do not turn the dependency correction alone into an eligibility pass.

## 3. Effective authority, runtime bytes and propagation

The effective D117 raw list is now **R041**. Its kernel remains K04, parameter profile P_BASELINE, declared horizon `20-60 sessions`, no D predecessor and dimensionless z-score output. All other meaning and source/refusal conditions remain applicable. This document overrides only the named D117 raw-dependency field and the D117 retention sentence in the earlier D116 correction.

The source/runtime catalogue bytes remain SHA-256 `67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549`. They still contain the historical D117 `R041;R075` list. Both catalogue copies and their hash-bound loader are intentionally unchanged; semantic authority and current executable incorporation are separate propositions. The original catalogue's other fields and all unrelated rows remain governing, subject to their own accepted overlays.

The separately approved D138/D145 five-R overlays and their source blockers remain unchanged. D117's post-approval direct and terminal R set is R041. Reconstruct the full declared D graph to check descendant exposure rather than assuming it from a prior ledger; any reported propagation result belongs in the accompanying assessment.

The old R075 role question is resolved by removal of that mandatory input from D117. The historical matching/window/source-time contract is not resolved by this correction. Keep its remaining classification question explicit. Runtime synchronisation, tests, public materialisation and source conformity remain later work under separate authority. No main merge, registry change, broker connection or Gate 2 acceptance is authorised.
