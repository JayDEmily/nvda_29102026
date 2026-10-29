# D117 — owner-approved exact-contract baseline profile

**Decision:** ACCEPT `D117-BASELINE-EXACT-CONTRACT-20SESSION-RECEIPT-20261016-01`, clauses P1–P6.

**Date:** 16 October 2026 — Australia/Melbourne.

## 1. Authority and exact reviewed object

The assistant asked: “Do you accept the proposed baseline, clauses P1–P6?” The programme owner answered: “Yes, I do proceed.” This records the owner's bounded decision, not worker self-acceptance.

- Reviewed commit: `ee82fa7460a8a253c16d2704a8d9cc2aae7bfdcc`.
- Reviewed tree: `480c99fd2de8a42d54f64ba50de4c7185ef7149c`.
- Reviewed proposal: `handoff/workbook_v2/gates_01_02/G2_D117_POST_APPROVAL_BASELINE_PROFILE_PROPOSED_20261016.md`.
- Whole-proposal SHA-256: `2c5fa7baa17f663fd0617475e9e3847f834fbced68a6b0c0d59b7583f935ba55`.
- Receiving branch: `work/v2-g2-d117-baseline-accepted-source-review-20261016`.

The reviewed proposal remains byte-unchanged as the pre-acceptance snapshot. This record supersedes its PROPOSED/NOT ACCEPTED labels and future-tense approval wording only for activation of P1–P6. In the verbatim clauses below, conditional wording refers to the original proposal; that condition is now satisfied by this decision. The profile is an accepted planning definition; it is not an implemented runtime configuration.

## 2. Exact accepted clauses

### P1 — Definition, identity and permitted inputs

Define a first D117 exact-contract measurement version with profile label `P_BASELINE_D117_EXACT_CONTRACT_20SESSION_RECEIPT_V1`. The label is proposed planning vocabulary only; existing P_BASELINE remains the owning parameter-profile family. Use only current and historical R041 volume facts under the already-approved dependency amendment.

All samples must identify the same underlying, provider/source variant, option contract identifier, expiry date, strike and option right, with the same compatible native-volume meaning and canonical contract-count unit. The acquisition request/observation lineage must justify those identities. No cross-contract average, nearest strike, delta-bucket proxy, provider average R075, open interest, forecast or strategy/position/order context enters the calculation.

The exact-contract mode fixes contract and expiry identity. It does not assert matching remaining days-to-expiry or delta across different sessions, and does not claim cross-contract expiry/delta normalisation. The owner would expressly restrict this first version to exact-contract mode; broader bucket versions are not accepted by this proposal.

### P2 — Calendar and comparison coordinate

Use the applicable option contract's authoritative regular-session calendar with an immutable identity/version and its specified IANA timezone. The concrete calendar binding must be established before any valid output; this proposal does not invent a calendar ID, holidays or exchange hours. A different calendar or comparison-coordinate rule requires a new measurement version.

Evaluation is at complete one-minute boundaries of the selected regular session. Let `T_0(k)` be the end of minute `k >= 1` counted from that session's scheduled regular opening. An occurrence outside a valid regular-session minute is inapplicable under this version. Use the same elapsed minute `k` in each prior session; do not substitute UTC clock time across daylight-saving changes.

Take **exactly the twenty immediately preceding completed regular trading sessions**, excluding the current session. Their calendar identities are fixed before data selection. Each must contain minute `k`; if an early close or other session structure makes that coordinate unavailable, refuse rather than skipping that session, rescaling its time, or substituting an older one. No claim of market hours is made without the calendar binding.

### P3 — Native volume and receipt-time selection

R041 is interpreted as the provider's reported cumulative traded volume for the identified contract/session. Its exact source mapping/unit/counter-period contract must be established; a callback value is not presumed to be per-minute volume. Do not add cumulative counter values together or silently convert them to one-minute traded volume.

For each cutoff `T_j(k)` (current session and twenty prior sessions), select the last eligible observation whose authoritative receipt time `r` satisfies:

`T_j(k) - 60 seconds < r <= T_j(k)`.

Select by receipt time and, for equal receipt time within a selected stream/generation, the preserved strictly ordered ingestion sequence. Ambiguous/incomparable scopes or unproved ordering refuse; an occurrence-ID lexical sort is not a semantic tie-break. An admissible selected stream/generation must be explicitly identified from source/session lineage; do not choose one by arbitrary request-ID or generation-name ordering.

Every selected observation must be visible by the current calculation knowledge cutoff and eligible at its own historical receipt cutoff. Later-arriving values cannot backfill the historical sample under this version. Preserve any actual source temporal kind and timestamp separately; using receipt cutoffs does not create an exchange event timestamp.

All selected observations must be certified as belonging to the intended session and volume counter, from the selected real-time source mode. A received frozen/delayed/previous-session value cannot masquerade as current-session real-time volume. The required evidence may be native fields or preserved request/status lineage whose meaning is established; this document does not claim that the existing collector or raw callback supplies it.

### P4 — Sample sufficiency, equation and refusal

Use one selected non-negative finite cumulative volume value for the current cutoff, `x_0`, and one for each of the twenty distinct required historical sessions, `x_1...x_20`. A genuine observed zero volume is allowed; missing volume is not zero. No duplicate session, shortened horizon, imputation, interpolation, forward fill or adaptive extension to older sessions is allowed.

`mean = (Σ x_i) / 20`, for historical `i=1...20`.

`s = sqrt(Σ (x_i - mean)^2 / 19)`.

`D117 = (x_0 - mean) / s`.

Require all twenty historical samples and the current sample, compatible units/identity/source-period meaning, admitted receipt/session/calendar selection and `s > 0`. Otherwise produce no valid D117 occurrence and preserve the applicable refusal reason. Negative z-scores are valid; no clipping or trade/action threshold is introduced. K04 arithmetic is unchanged; the chosen historical sample is now explicitly proposed.

### P5 — Configuration independence, lineage and versions

The twenty-session horizon, regular-session minute coordinate, receipt-time basis and sixty-second freshness rule are immutable parts of this measurement version. A strategy cannot vary them under the same definition/profile version. Any later twenty-to-sixty-session version or bucket normalisation requires its own explicit definition/profile and comparable-source law; data availability cannot select the version implicitly.

Persist/reference every selected R041 occurrence and its actual provider/request/contract/session, receipt and ingestion-order identity; raw mapping/unit version; definition/profile; calendar/timezone version; twenty session identities and minute cutoffs; current as-of and knowledge cutoff. Those are required future result-lineage properties, not claims that storage/proof already implements them.

### P6 — Approval effect and remaining admission boundary

If accepted, the owner authorises only this exact-contract first-version planning convention and its explicit restriction. It does not authorise a bucket implementation, runtime catalogue/profile changes, source integration, live capability or Gate 2 acceptance. Catalogue/workbook/runtime synchronisation and authority-derived proof belong to later separately authorised work.

Planning reassessment must still establish that the required R041 source/session/counter/identity contract and calendar binding can supply this meaning, applying accepted A1/A2. Operational capture/conformity may be deferred only when those semantic questions are supported. Profile acceptance alone does not automatically make D117 eligible or reduce the unresolved count.


## 3. Effect and retained boundaries

This supplements `D117-RAW-VOLUME-HISTORY-20261016-01`: R041-only current and historical inputs remain effective; the first version now uses the exact-contract twenty-session receipt-based law above. K04 sample-standard-deviation arithmetic remains unchanged. Broader cross-contract delta/expiry normalisation is not delivered or authorised by this restricted version. Missing required history, including short-lived/new contracts, yields no valid occurrence.

The root ExecPlan, guardrails, agent instructions, both catalogue copies, workbooks, source, tests, module registry and main remain unchanged. The catalogue byte digest remains `67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549`; its historical R041/R075 declaration is not runtime adoption of this overlay. D116 and the D138/D145 approvals are unaffected.

Source/calendar feasibility and classification are separate propositions. See `handoff/workbook_v2/gates_01_02/G2_D117_ACCEPTED_PROFILE_SOURCE_REASSESSMENT_20261016.md`. This decision is not Gate 2 acceptance, source admission, an M02 allocation, authority to connect to IBKR, or authority to implement/integrate the profile. Later C–E work requires its own accepted plan and execution authority.
