# Gate 2 — D117 post-approval baseline investigation and proposed first profile

**Date:** 16 October 2026 — Australia/Melbourne.

**Current accepted change:** `D117-RAW-VOLUME-HISTORY-20261016-01`; see `handoff/m01_completion/authority/D117_OWNER_APPROVED_RAW_VOLUME_HISTORY_AMENDMENT_20261016.md`. D117 now requires R041 only. The R075 dependency question is answered; the remaining comparison-history convention is a different proposition.

**New proposal:** `D117-BASELINE-EXACT-CONTRACT-20SESSION-RECEIPT-20261016-01` — **PROPOSED, NOT ACCEPTED OR IMPLEMENTED**. This is a proposed measurement profile and definition-version restriction, not a second active plan, new canonical D identity or new runtime module. Its receipt-time, regular-session, twenty-session and freshness choices are new proposed conventions; the preceding dependency approval did not select them.

## 1. Investigation and established baseline

Inspected the accepted D117 correction and its exact proposal, original brief §5 K04, §§6–9/11 and Appendix A, effective catalogue row D117, applicable authority index/current clarifications and their D117/P_BASELINE lineage. Inspected `api.py` option-selection constants, `_selection_policy_satisfies_row_authority`, `CalculationParameterSetV1` and `InputSelectionPolicyVersionV1`, plus `_stage1.py` K04 and its history selection. The original workbook D117/R041/R075 source cells and RC14 test/source history were inspected in the immediately preceding D117 reassessment; their bytes remain unchanged here.

The accepted source establishes a parameterised 20–60-session historical z-score, with matching time-of-day/contract bucket, strict prior history and sample standard deviation. The catalogue permits each-contract/delta-bucket scope. The current public selection code recognises exact-contract or expiry/right/delta-bucket joins, but that source comment/code is evidence of representation, not permission to select either as the new default. The generic selection type permits temporal-basis and freshness fields; it is not an instantiated D117 measurement convention.

The read of the K04 branch shows a history-count operation over selected observations, not a D117-specific guarantee of one same-time observation per distinct prior trading session. A two-sample controlled fixture does not prove a twenty-session matched source history. This is a bounded source inspection, not a full implementation/proof census or a newly executed test.

**First remaining semantic invariant:** which option identity and within-session coordinate define comparable samples, what complete historical horizon is intended, and which temporal/freshness law selects one sample per session. These choices affect the value and must not be inferred from the old fixture or filled by the amount of data available.

## 2. Recommendation and its practical scope

Start with **one exact option contract**, comparing its reported session-cumulative volume at the same regular-session minute over **twenty complete prior sessions**. This uses the existing accepted exact-contract scope and the minimum named session horizon. It does not require inventing cross-contract delta/expiry normalisation or adding unapproved numerical R inputs.

Twenty sessions is a proposed fixed descriptive convention within the accepted 20–60 range, not an empirically established optimum or strategy tuning. A sixty-second freshness bound is a proposed fixed convention aligned with the one-minute evaluation cadence; the cadence does not itself prove that tolerance was previously accepted. Receipt time is proposed explicitly so absent source event times are not fabricated. The resulting measure describes **reported volume available by a receipt cutoff**, not exchange-event-time trading activity.

**Material limit:** a contract without all twenty prior matching sessions produces no result. A new/short-history contract is not rescued by another strike, expiry or delta bucket. This profile therefore does not provide universal coverage of short-lived or sparsely observed option contracts. The historical cross-contract/bucket objective remains explicit receiving design work for a separately specified and accepted version; it is not claimed as delivered by an exact-contract profile.

## 3. Exact proposed profile law

These clauses are the concrete proposal for a separate owner decision. They do not become authority merely because this file is committed.

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

## 4. Why the original control is not silently removed

The programme owner has already removed the mandatory R075 dependency; no further approval is requested for that change. This new proposal addresses the separate exact historical-sample law that the accepted correction deliberately left open. The old two-sample fixture and its R075/open-interest naming remain preserved as historical/current source evidence. They are not rewritten as proof of the new twenty-session receipt-based profile, nor declared equivalent to it.

Comparative check: existing conditional M02 candidates D028–D031 also retain P_BASELINE/source-instance obligations. Their current conditional status is not proof of an accepted D117 session or contract-bucket policy. No inference from those row labels is used to certify D117. The current D117 canonical classification remains UNKNOWN until the material source/selection obligations are actually established.

## 5. Receiving work and close-out boundary

The accepted dependency amendment resolves the obsolete R075-role requirement. The three existing cumulative registers retain 209 canonical rows, 21 root issues and 124 links. The accompanying post-approval fields distinguish the new effective R041 dependency from the historical catalogue and preserve the remaining D117 profile/source question.

Static reconstruction of the complete 209-identity declared D graph, with the accepted D138/D145 overlays applied before the D117 change, finds **zero D117 descendants**. Applying the new D117 overlay changes direct and terminal R reachability only for D117, from R041/R075 to R041. There is no downstream D dependency propagation to claim. This graph check is documentary analysis, not an application test or proof that any source/history exists.

This document is a planning design candidate under the authorised continuation. No code, test, workbook, catalogue, schema, registry, guardrail, active plan or accepted main is changed. No application tests, runtime validators, database or broker operation ran. The proposed profile is not empirically validated or source-admitted. Exact native metadata/session availability remains a required evidence question, not a promised future adapter capability.

**Next owner decision:** ACCEPT or RETURN `D117-BASELINE-EXACT-CONTRACT-20SESSION-RECEIPT-20261016-01`, clauses P1–P6, with its stated short-history/sparse-data limitation and unadmitted bucket extension. This is a new convention decision, separate from the already-approved R041-only dependency.
