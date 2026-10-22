# Independent D015 documentary design review

Disposition: **RETURN_FOR_BOUNDED_SPECIFICATION_REPAIR**. No owner/domain BLOCK is established. This is independent design judgement, not admission, proof adequacy approval or implementation acceptance.

Candidate inspected: `51e148d4ec3f7c5a45b81ab170ddd0325d6d8a37` on `work/v2-d015-d020-plan-20261022`.

Exact inspected SHA256:

- `handoff/foundation_implementation/authority/D015_IMPLEMENTATION_BRIEF.md`: `95c02a42dc1d01abdd9d3c537d9139c7c5af90de55731f3e9b14290fddde2325`.
- `handoff/foundation_implementation/authority/D015_PROOF_CONTRACT.json`: `f78f3f42743cbf6be002d69fc97960fffa52e6a0c173170719a85df9e8f3203b`.
- `EXEC_PLAN.md`: `2c78f8a7653413eb79d678741473ff88d6b8a18d1887ceb09c28ba242c848e01`.

## Scope and evidence

Read frozen GUARDRAILS, root AGENTS, full current ExecPlan, test-local override, complete proposed D015 brief/contract, existing M02 public records/protocols, original selection/canonical codecs, predecessor capture/validation and existing isolated ratio SQLite mechanism. Reused this reviewer's earlier direct examination of preserved D011 authority, F03, original K08/catalogue, and M01 F2a source/test evidence. The latter supplies historical evidence, not new authority. Inspected D015 Git lineage: the sole new design commit is 51e148d; the earlier preflight found the mapping distinction to be an authorised design task, not a blocker. No earlier D015 design RETURN/repair cycle was found in that inspected lineage. Findings below are ISOLATED initial-design specification omissions, not a classified recurrence.

Commands were read-only source/document/Git/hash inspection. No product test, source import, implementation, binding/admission change or repository edit was performed. This report is the only file created by this reviewer. Parent-reported schema/environment checks are not claimed as independently executed here.

## What is sufficient in principle

The proposed separate synthetic R126/R127 correspondence preserves existing D011 mappings and does not assert native cross-stream equivalence (brief lines 9–13). Actual public predecessor capture, matching trade-time as-of, unchanged receipt cutoff, no local midpoint replacement, distinct IDs and exact Decimal representation matching are appropriate. Current authority commissions those controlled choices (root sections 2.1, 2.3, 5.1); it does not require another owner instruction merely because R IDs differ.

The additive typed request/occurrence/reader/factory shape is compatible in principle with existing public types. Exact-int signs can use the existing canonical primitive-int representation without broadening the original Decimal occurrence. A separate owner-local SQLite profile and additive narrow codec preserve old stores/codecs. The six literal cases, actual M00/D011 setup, immediate equal-price decoy and full successful readback are an appropriate reduced baseline; no old mutation matrix or universal positive/negative quota is requested.

## Findings requiring repair before exact-byte admission

### F001 — Pin the actual predecessor admission supported by the reused validator

Brief lines 11–13 and 38 say “old owner admission” and reuse existing complete predecessor validation, but do not identify the predecessor admission digest. The unchanged `_rational.py:28–30,155–223` validator is concretely pinned to M02 admission `a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393` (accepted D012 brief); it reconstructs the original logical identity using that digest before validating. It does not indiscriminately accept every historical D011 admission.

Consequence: a fixture can lawfully materialise original D011 under another historical accepted digest and nevertheless fail the declared reused validation before reaching D015 semantics. Specify the exact accepted predecessor admission and supported D011 definition/configuration versions, including that D011 must be produced under that existing accepted admission when this validator is reused unchanged. This is a compatibility clarification, not a request to change old D011 or the validator.

### F002 — Finish the exact fixed configuration in the existing representable types

Brief line 19 does not supply `CalculationDefinitionV1.equation` or exact `authority_refs`. Its rule parameter “includes quote-first/last-different/unknown-zero” without specifying a representable constructor payload. The existing `CalculationParameterSetV1` has only `context_id`, `version`, `profile`, `subject_instrument`, and `members` (`api.py:152–158`); it has no rule-options field. The fixed-law meaning itself is clear, but the canonical configuration/identity bytes are not fixed.

Consequence: two workers can choose different parameter members or equation strings and produce distinct supposedly identical version-1 configuration/occurrence identities. Provide all exact constructor fields, representing the fixed rule through the declared immutable definition/profile rather than inventing new fields on the existing type. Identify the exact existing authority references (paths/digests). No new generic parameter model is needed.

### F003 — State the new quote selector's trade-time anchor, and the prior-history eligibility exception

Brief lines 13 and 21 impose a trade-time correspondence result and specify current-trade selection at request as-of, but do not explicitly state the R126/R127 enumeration/selection request anchor. The existing `_selection.select` forwards `request.as_of_utc` to the M00 event cutoff and ranks the resulting eligible facts (`_selection.py:85–161`). Selecting the new quote at parent request time, then rejecting it for not matching the trade-time D011, can falsely refuse when an older compatible quote exists but a newer post-trade quote is visible.

Specify that R126/R127 are independently selected with event/as-of anchor equal to the selected trade event and the unchanged D015 receipt cutoff, using the inherited eligibility/rank/freshness/skew law; a visible later quote is excluded, not allowed to displace the older eligible match. Keep a visible later-quote decoy in an existing successful case to distinguish this from the sixth post-trade-only refusal. This does not require another parameterised case.

Also make explicit which eligibility check is deliberately omitted for prior R120 history. Line 21 says no fixed rolling window, whereas unchanged `_selection.eligible` applies the 60-second freshness bound (`_selection.py:45–81`). State that the last-different scan retains source/type/unit/subject, true-instant, event/receipt/cutoff, duplicate/rank and completeness checks, but does not apply that current-trade freshness bound to earlier prices. Otherwise reuse of “eligible” can accidentally truncate the admitted complete history. The last-different rule and immediately preceding equal-price bypass themselves are sufficient.

### F004 — Own the new store's first-fact retry proof once

Brief lines 40–42 require retry to return the original complete fact/time, but lines 52–54 and contract lines 26–31 identify only successful new-shape roundtrip/readback as the new store evidence. The store is a new implementation/table/profile, not an unchanged previously proved persistence path. A store that serializes and reads correctly yet overwrites or changes calculation time on a repeated materialisation could satisfy the six currently stated outputs and first successful reopen.

Bind one bounded public repeated-request sequence to an existing successful case (later injected calculation clock, same occurrence/content/original time, reopen through the public reader), or explicitly identify an unchanged reused implementation path whose admitted proof covers that exact new-store mechanism. This is one attributable new-store compatibility proposition under root section 3.1, not a request for generic fault, column, hash, or mutation matrices. Clarify that the table's payload stores the full typed occurrence including original calculation time, while ID derivation omits only its own ID and calculation time; this resolves the otherwise loose use of `logical_payload` for complete durable facts.

## Closure boundary

These four bounded corrections can be made within the already commissioned controlled D015 design task. Re-review exact successor bytes and their contract digest before any delegated admission. The unresolved issue is specification exactness and evidence ownership, not provider certification, runtime availability, a new numeric convention or a demand to widen D011. No code/proof result or admission follows from this report.
