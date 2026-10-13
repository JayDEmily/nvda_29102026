# Independent F4 whole-branch review return — bounded at four proved failures

Disposition: **RETURN_TO_WORKER / RECURRENT_CLASS. No Stage-1 acceptance.**

Reviewed production: base `3fe9f792b10c1eb9d2797eccc2f81d623620f69c` to `95ae8c3f8078fdf492db7831a53efe749f424a5d`. Root was concurrently reconciling tests/evidence; observed worktree modifications in those files are not reviewer edits and are not a frozen new candidate. All line references below refer to this production HEAD. No production/test files or Git objects were changed by this reviewer. Report and executable witnesses are outside Git as requested.

I inspected root GUARDRAILS, AGENTS, accepted EXEC_PLAN, test supplement, authority index, owner approval and both exact approved proposal records, relevant accepted brief rules, branch production diffs, the full new financial-policy module, related public projection/context/history/materialisation code and live-Greek producers, and all five newly approved test files. This is a whole-branch review return bounded by the first established class failures, not an assertion of exhaustive semantic acceptance of every pre-existing Stage-1 row. Green worker test totals were not used as correctness premises.

## Important 1 — actual live risk sources do not establish the labelled units or scoped quantities

**RECURRENT_CLASS.** Locations: `api.py:1606–1618`; `_financial_policy.py:477–491`; `_stage1.py:1896–1914`.

The projection stamps `canonical_risk_unit` solely from D identity. It does not derive that claim from the actual raw canonical unit/conversion. D189 accepts it alongside a source-ID set and the presence of a LivePositionContext reference. That context can have been supplied to the original request without being used to validate quantities, multipliers, contracts or currency by the live-Greek producer.

Independent sequence in `f4_independent_witness.py` uses explicit M00 admission, projection mappings, unit conventions, owner construction, and public `materialise` calls for all four Greek rows; it does not call the worker public-position fixture. Real typed persisted outputs are projected into the D189 own-kernel consumer. Controlled D174/D162 remain explicit Stage-2 predecessor values, not Stage-2 production.

Two independently varied executions:

- `unit_only`: native source R212 quantity 2 agrees with live/candidate/membership quantity 2. R116 canonical unit is explicitly `currency_per_volatility_fraction`, affine scale 1. Public D183 is 240. Its persisted raw lineage still records that unit, but projection labels it `currency_per_volatility_point`; D189 emits using 240 in the point-scaled envelope.
- `quantity_only`: R116 is explicitly point-scaled. Actual native R212 is 2, while candidate/live/membership claim 20 against the same source ID. Public D181–184 produce `(100,8,240,-40)` from quantity 2, and D189 nevertheless emits a nonzero hedge for the quantity-20 scope.

The output logs preserve both observations separately. The approved D175 clarification §3 requires explicit canonical vega/theta scaling; §6C and the earlier approved §5 require exact full live quantities and source scope. IDs alone are insufficient.

Lineage inspected: F1 RC16 census/proof matrix explicitly names exact position, signed quantities, multiplier and convention; production `389c8dd9dc1cdb6a31f50ddaa412fd3ac7306fdb` repaired native-leg completeness by equal input-ID sets; proof `69d56f5a428c4576f819835cfc951b0c50acb2a5` and repair `95ae8c3` introduced retained unit/source metadata. The common unfinished invariant is that actual selected source evidence must establish the complete exact scoped exposure, rather than a co-supplied label or matching ID set.

Class-level closure: every consumed live exposure must be demonstrably for the exact source contracts, signed quantities, multipliers, named currency and explicit canonical scaling of the approved scope; missing/incompatible evidence must refuse. No new risk measure or implicit factor 100 is authorised.

## Important 2 — independent signed-component rounding rejects a valid joint hedge

**ISOLATED numerical representation mechanism** within the new clipping implementation. Locations: `_financial_policy.py:217–218,526–534`.

Authority floors the shared lambda to 28 fractional places, then uses one common `lambda*h`, with conservative inequality readback. Production additionally floors each signed component through `packed_vector`. Flooring a negative component increases its magnitude; several such changes can exceed the exact joint ceiling and lose common scaling.

Independent arithmetic witness: current vector `(.3,0,.7,0)`, all four target bands `[0,0]`, shocks S=V=T=1, K=10000, tail fraction `.0001`, CVaR=3, stress inactive. D175 correctly gives exact B=1/3. The safe shared rounded lambda is `.3333333333333333333333333333`. Its exact finite-Decimal products with `-.3` and `-.7` are safe. Independent component floors instead sum to `.3333333333333333333333333334`, above 1/3. Observed D189 is `None`; direct policy call reports `ValueError: persisted clipping failed readback`.

This uses worker fixture composition only for uncontroversial context setup; the numerical input and expected rational inequality were independently chosen. It does not depend on operation ordering. The earlier approved risk repair `076342c` introduced the implementation; no inspected earlier finding addressed this component-rounding mechanism. A safe refusal prevents an oversized persisted hedge, but does not implement the required valid-input result.

Required proposition: persisted permitted components preserve the same conservative shared lambda and exact inequalities for finite-Decimal inputs; rounding must not change vector direction independently or erase a lawful result.

## Important 3 — D175 ignores the actual retained predecessor identity evidence

**RECURRENT_CLASS retained-provenance/correspondence failure.** Locations: `_financial_policy.py:327–358`; `api.py:1638–1644` exposes the evidence but the consumer does not validate it.

Construct actual typed `DerivedSignalOccurrenceV1` D174 and D162 values with the accepted-shaped named payloads but empty actual `parameter_context_refs`, `convention_refs` and `predecessor_occurrence_ids`; project them through the production owner `_occurrence_kernel_value`. The named payload claims candidate/model/scenario/option-convention identities, D174's D168 ID and D162's D174 ID. Actual metadata contains none of these proven relationships. Observed D175 still returns maximum `(1000,1)`.

The exact approved D175 proposal §6D explicitly calls for actual predecessor/context/version evidence and validating correspondence, not merely retaining those refs in persistence. Checking agreement between two embedded labels cannot establish agreement with the actual producers. This is a controlled typed-predecessor own-kernel failure; current Stage-2 public graph emission is not claimed.

The relevant repair lineage is the mandatory-predecessor presence repair `1b64bd4`, the approved clarification expressly identifying insufficient `_occurrence_kernel_value` metadata, and `69d56f5`→`95ae8c3` adding metadata projection. The shared class invariant is actual producer/reference correspondence, not a further list of self-asserted strings.

Required proposition: the approved consumers validate all materially required embedded reference claims against actual admitted producer/context/convention/predecessor metadata. Merely making metadata available does not discharge that obligation. This witness establishes D175; it does not claim an exhaustive executed D178 mismatch matrix.

## Important 4 — D192 rejects canonical numeric D187 occurrences

**RECURRENT_CLASS producer/consumer carrier incoherence.** Location: `_financial_policy.py:579–585`, especially lines 581–582; compare `_stage1.py:374–385` and `api.py:3026–3029`.

The authoritative D187 catalogue unit is `score/boolean`. Both the kernel result and public persisted occurrence take the catalogue unit verbatim. Projection retains it as `units`. D192 requires `metadata.units == params.invalidation_domain == 'score'`. Therefore a canonical numeric D187 is incompatible with the consumer, even when it is the lawful K07 score.

Independent witness replaces only the worker action fixture's D187 with an actual typed persisted numeric `.2` occurrence using the exact catalogue unit and production projection. The otherwise valid D192 result changes from `hold` to `None`. The worker fixture's manual `units='score'` hides the discrepancy. The witness is controlled own-kernel composition; it is not a claim that the deferred entire D187 graph currently materialises publicly.

This belongs to the same recently repaired real-predecessor versus worker-label mismatch class as the D190/D191 domain and D181–184 metadata work in `95ae8c3`. Closure must establish compatibility for actual canonical numeric K07 score carriers while retaining bool refusal and the explicit threshold/domain; changing the accepted catalogue to accommodate a fixture is not justified.

## Verification and evidence boundaries

Executed with `/workspace/scratch/5eb867831d92/stage1_proof_env/venv/bin/python`, `PYTHONPATH=src:.`, from the repository directory:

- `f4_independent_witness.py unit_only` → wrong unit admitted, D189 emitted.
- `f4_independent_witness.py quantity_only` → wrong scoped quantity admitted, D189 emitted.
- `f4_independent_financial_witnesses.py` → rounding refusal; D175 emission with absent actual predecessor refs; canonical D187 causes D192 refusal.

Scripts and logs are at `/workspace/scratch/5eb867831d92/` beside this report. Initial witness authoring hit the normal nonempty-P_BASIC constructor validation; that scratch script was corrected with an explicit subject parameter before the successful executions. No failed prerequisite was bypassed.

Static observations: the branch's catalogue diff changes only the approved D175/D189 context conjunctions; the Stage-1 dispatcher still has no K09–K15 production branches; RiskScope fields remain immutable references. These observations are narrower than acceptance of all graph and persistence semantics. No Critical or separate Minor finding was established in this bounded pass.

Declined to judge / not established:

- Stage-1 acceptance, exhaustive mathematical correctness of all 174 rows, full public reachability of all 144 closed rows, or all 30 cross-stage contracts. The four failures prevent a positive whole-Stage disposition, and the reviewer did not rerun the whole test suite.
- PostgreSQL role isolation, durability and structured replay in this host. Root reports and the inspected progress ledger records a UID/GID-mapping blocker; this reviewer did not independently execute PostgreSQL or bypass its nonroot requirements. No database PASS is inferred.
- Stage-2 producer correctness or full public D175/D178/D189/D192 graph execution: Stage 2 is absent/unauthorised; the financial own-kernel witnesses explicitly use controlled deferred predecessors.
- Root's concurrent evidence/test adjustments and any subsequent repairs. This report describes the production state at the stated HEAD and is not acceptance of a later candidate.

The root's proposed repair direction—validate live scope against actual sources when supplied, derive risk-unit evidence from actual canonical lineage, preserve exact finite-Decimal products of the one rounded lambda, require actual retained reference correspondence, and reconcile numeric canonical D187—is consistent with the inspected approval. This is a scope observation, not approval of unreviewed code or Stage-1 acceptance.
