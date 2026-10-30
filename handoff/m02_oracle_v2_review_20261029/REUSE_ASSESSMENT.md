# V2 synthetic oracle attachment — reuse assessment

29 October 2026. Review base: `9bd59acba13ead7252e52e32e1b5d862adecd99a`. Supplied candidate: `46fc04a20312d5687a36cdbf308e9c1070bdb2ef`, tree `d80c95be7493325e8ac0d5ddda452326aed98560`. This is a review of candidate planning material, not a successor ExecPlan, implementation commission, product proof or production-policy approval.

## Decision

**PARTIAL_REUSE_FOR_PLANNING.** The attachment supplies useful concrete example data and expected arithmetic for D079–D081, dependent D078, D091, D142 and D144. Preserve those examples as provenance-labelled inputs to the next plan. They do not establish public-source compatibility, complete proof coverage, executable negative cases or implementation readiness. Seven D identities are illustrated; none is newly accepted by this review.

The supplied branch shares ancestor `10a37c8b81c200b0f048e36a3585cdbaf2eeed08` with the accepted review branch. Its seven V2 additions are separate from the later accepted G4 review and profile clarifications. Do not replace the current root plan or canonical/embedded profiles with the older packet versions. Original bytes and candidate ancestry remain retained as evidence, without merging the candidate into the active tree.

## What saves work

| Material | Reuse in next plan | Remaining work before proof execution |
|---|---|---|
| Existing 64-row K06 CSV and new held-out CSV | Concrete full-rank shared-fit example, expected intercept .0002 and betas 1.50/.40/.70; held-out prediction .0208 and residual 0 | Lawful public training-history ingress, aligned sample/cutoff metadata, shared fit/intercept lineage, numerical output representation; build a real coefficient-mismatch refusal with individual occurrences |
| D091 boundary CSV | Explicit absolute-delta labels at selected edges, an interior point, missing and out-of-range examples | Bind R112 scale/variant/source; specify any extra boundary/nonfinite witnesses within authorised physical case allocation; CSV has no explicit +1 row despite handoff prose mentioning it |
| D142 timeline CSV | A depth-only state at t=3 followed by first joint recovery at t=7; shock t=1 gives elapsed **6 seconds** | Construct admitted ordered book/quote input and completeness/reset lineage; make refusal-window origin and closing event explicit |
| D144 four-pair CSV | All four signed SMART-minus-direct price/size differences in a declared stock example | Reconstruct both books through actual input seams; explicit source receipt times/contract/generation/unit identities; construct reached skew/missing-level refusals |
| V2 case JSON | Candidate success/refusal ideas and lineage requirements | Convert prose descriptions into independently executable, reached cases; agree exact physical case budget and independent execution schedule |
| V2 readback JSON | Historical author calculation record | Use independent review/calculation evidence; do not treat author's PASSED label as runtime proof |
| V2 handoff MD | Scope warnings and bounded seven-ID frontier | Replace stale gate status and inherited ambiguous policies in a new derived plan; preserve original handoff unchanged as evidence |

## Required corrections and exclusions

1. **Inherited authority drift — DO_NOT_CARRY_FORWARD into current authority.** The packet predates current G4 acceptance and the 6aaeacc/9974df6 clarifications. Its old canonical and embedded profiles reopen K06 ownership solely because coefficients vary, omit D142's continued-search rule, and omit D144's explicit quote-unit/multiplier refusal. Those older bytes are historical, not a rollback request. Use the accepted branch's clarified profiles and G4 report.
2. **D142 refusal is underspecified.** The positive example is mathematically sound. The negative description stays unrecovered “through t=30” after shock t=1; this alone does not establish exhaustion of a 30-second shock-relative window. The next plan must declare the observation-window origin, endpoint inclusion and a closing observation/watermark. Under shock-relative 30 seconds, reach t=31 or later as the admitted closure rule requires. Do not infer no future joint recovery from an unfinished trace.
3. **Examples are not source replay.** Aggregate D142 states and already matched D144 pairs do not demonstrate position/operation reconstruction, temporal joins or public M00/M02 ingress. K06 slot IDs alone do not demonstrate real training-history publication. D078's one fit_id column does not itself instantiate three individually tagged coefficient occurrences with one mismatch.
4. **Data coverage is narrower than prose.** D091 CSV has nine rows, selected signed boundaries, one interior point and two refusals; it omits an explicit positive +1 and nonfinite row. This is a coverage limitation, not evidence that all boundary logic is wrong. D144 uses STK shares only and supplies no option/multiplier scenario. No extra physical tests are authorised by adding rows to a CSV or listing candidate refusals.
5. **Transport qualification.** All 42 manifest members match their declared sizes/hashes. Fresh baseline-plus-additive Git restoration preserves all 66 original refs and produces 69 refs with exact candidate tree/blob listing and successful bundle verification/fsck. One loose file, COVERAGE_MATRIX.csv, differs from its Git blob solely by 29 CRLF-versus-LF endings (8783 versus 8754 bytes). Its parsed content agrees; blanket loose/Git byte equality is false. The seven V2 additions match their committed blobs exactly.

The accepted V1 D142 example records elapsed 7 without explicit timeline offsets. V2's explicit t=1 to t=7 example has elapsed 6. Treat these as separately identified examples; the V2 timeline does not prove the V1 elapsed value erroneous.

The independent reviewer also identifies a proof-discrimination limitation: because all three K06 factors are orthogonal, separate univariate fits yield the same slopes as the required joint fit on this sample. A zero-residual example is also weak in isolation. Retain the valid numbers as examples, but select future authorised proof data that distinguish the required computation; do not increase the physical case budget implicitly.

## Implications for the next ExecPlan

Use a prerequisite gate to bind the accepted synthetic policies to concrete lawful public input/output contracts and an explicit proof allocation. Then dependency-order the shared D079–D081 fit before D078, with separate D091, D142 and D144 obligations. Promote a unit only after its own prerequisites are established; the seven-ID list is a candidate frontier, not seven automatically executable coding leaves. Preserve the 21 other unresolved identities and all seven external holds. Even these seven retain their existing production/source holds unless separately satisfied; no subtraction from the current 28 holds is justified here.

Independent sub-agent review is available and used for this assessment. Future test timing must be written explicitly in the proposed plan and follow the owner's then-current direction. Maintain module-local scope; do not invent an M00-to-M02 end-to-end suite or rerun the 98 historical controlled acceptances and 11 L14 claims merely because a plan is new. Keep checkpoint-after-each-leaf requirements.

## Evidence and limits

See `INDEPENDENT_REVIEW.md`, `TRANSFER_AND_LINEAGE_CHECK.json`, `LOOSE_VS_GIT_MISMATCH.json`, `INTAKE.json`, and the byte-preserved seven additions under `untrusted_v2_original/`. Normative meaning comes from the current K02 D144, K06 D078–D081 and K08 D091/D142 provisions in `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`, together with the accepted canonical profiles and current G4 report. The author's supplied receipt is a claim inspected against restored Git evidence, not independent semantic acceptance.

No product tests, imports, static analyser, runtime probe, provider call, installation, proof admission or product/config/test modification was performed. Root EXEC_PLAN.md, GUARDRAILS.md, AGENTS.md, accepted profile files and historical completion/evidence registers remain unchanged. Only review documents and provenance-labelled original V2 additions are added in this pass.
