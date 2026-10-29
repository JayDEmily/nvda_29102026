# Independent M00 Brief 2 documentary plan review

Disposition: **APPROVED_DOCUMENTARY**. Reviewer: independent worker `/root/independent_m00_plan_review`, 27 October 2026. Review unit: replacement M00-only plan, not implementation, runtime proof or programme admission.

Source anchor: `17d7553cf3ad92700f849f696134de67b64b0dfa` (observed HEAD during initial review). Initial exact reviewed root `EXEC_PLAN.md` SHA-256: `e835b4662968762fa11fa2a73e26c3998260781f4cf907f5f7dafa59e6f64bc6`.

Brief SHA-256 independently observed: `0d5ee211c1285b31834062ab2d871670ed2f318cbb955e7df95f80067d562007`. Preserved paused-plan SHA-256 independently observed: `2d95d7c5e425ed1dd231f4685100f7c1db9c85ee1369fea54f91580aab6caa5a`; the original anchor's `EXEC_PLAN.md` hashes identically. Final status-only plan recheck is recorded below.

## Decision and coverage

No blocking documentary defect was identified in this bounded review. The plan can be committed and delivered as the requested planning checkpoint. This disposition is independent planning clearance only; it cannot supply human implementation acceptance, proof admission, M00 completion, a baseline freeze certificate or product correctness.

The plan covers only Brief 2 and pauses D145 without discarding prior holds, tests, proofs or history. Its L00–L06 are meaningful acceptance boundaries: exact authority/baseline/admission, immutable inputs/oracle, native projection proof, history/isolation/reopen, control discovery, deterministic actual export, and final independent disposition. The current turn stops before those leaves execute. Documentary clearance and future product acceptance are explicitly separated.

I checked the ten table contributions against the original brief: A1 1/4, A2 4/4, A3 4/4, A4 4/20, A5 3/15, A6 2/10, B 7/35, C1 3/15, C2 4/24 and C3 4/24 observations/projections; totals are 36/155. Controls, optional R001 proof and any contract-required direct PUT supplement remain outside those base totals. The original literal tables remain authoritative rather than silently replaced by arithmetic.

All N01–N18 have explicit owning leaves. L02 owns N01/02/03/06/07/11/12/14/17/18; L03 owns N04/05/10/13/16; L04 owns N08/09/15. L01 provides isolated immutable negative fixtures and L06 requires assertion/evidence mapping. Native side, operation and position law, four asynchronous option callbacks, provider timestamp absence, MPID versus requested exchange, synthetic namespace and fixture-family separation are preserved. No downstream midpoint, book standing-state, concentration or production skew decision is assigned to M00.

The actual public seam supports the plan's baseline experiment: observation admission/read, field-path projection and R-specific history exist. The code rejects receipt-only fabricated source timestamps, permits equal ingestion sequence while rejecting decreases, requires exactly one matching provider/variant/R mapping, and sorts history by receipt/scope/sequence/ID. The plan explicitly addresses shared-variant mapping ambiguity, receipt/event cutoff distinction, retained tied facts and absence of invented causal ordering. These are static observations; I did not execute these behaviours.

L04 correctly treats known-ID control retrieval as insufficient. Inspection of the public read facade did not reveal a generic control-history enumeration method. The plan requires a direct discovery witness, an exact compatible additive read contract and independent contract/ownership clearance before correcting this interface. It does not disguise error 316/317 as R187 operations or enumerate private SQLite as consumer proof. The narrow read-model approach is consistent with AK-OWN-001 and AK-STATE-001 while preserving v1 shapes; its actual contract remains future work.

L02/L03/L05 require genuine SQLite persistence and fresh public readback, including a fresh process and ordinary read transactions. The adapter currently opens read transactions with URI mode=ro and query_only; `create_sqlite_persistence(create=False)` itself also performs a writable connection validation. Thus this review does not claim the entire constructor is a filesystem permission boundary. L03's requirement to inspect actual read-only transaction mode is necessary and retained. The plan correctly excludes PostgreSQL runtime and live-feed certification while retaining static adapter impact assessment.

The current raw SQLite proof contract names four physical families and generation0003 binds exact historical brief/binding/contract bytes. The proposed three new physical families cannot simply be placed under that old admission and run as accepted proof. L00 explicitly requires an exact new binding, lawful proof-path ownership, independently reviewed scoped admission/control diff and stopping if authority is missing. It does not authorize automatic resealing of generation0003 or relax the runner. This is an execution prerequisite, not a resolved planning claim.

L05 requires actual public M00 output, independent oracle comparison including type/Decimal representation/absence, a second clean-checkout fresh-SQLite reproducibility experiment, hashes and precise manifest statuses. A failed mandatory criterion cannot become accepted completion through partial output delivery. L06 requires impact assessment and reacceptance if later changes invalidate an earlier leaf. Each accepted leaf must be committed and its cumulative full-history checkpoint verified, saved and exposed before continuation. The planning checkpoint has its own explicit stop boundary.

## Lineage and recurrence assessment

I inspected relevant actual Git history, not merely author summaries: the plan history leading to the anchor, source history for M00, and the `ce21f6e10845f17436e1f83520b38c668feb18e5` diff correcting R193 versus R197 and introducing the typed positional path. I also read the retained M00 SQLite proof review's original/second/final static review and generation2/3 repair records. That record identifies earlier recurrent proof-correspondence/static-signature defects and later isolated integer fidelity repair. The current candidate does not reopen those tests or infer native admission from their accepted labels.

No RETURN_TO_WORKER finding is raised, so no new isolated/recurrent failure is asserted. Prior repeated mechanisms remain relevant future review risks: apparently green proof that misses exact source/typed semantics, helper composition that pre-satisfies an invariant, and binding/generation provenance substituted for current authority. The plan contains class-level guards for these mechanisms: independent literal oracle, direct reviewer sequences, exact admission before execution, first-witness preservation and no claim inflation. This is documentary risk coverage, not proof that future authored tests close those classes.

## Inspection record and limits

Read in full:

- Current `GUARDRAILS.md`, `AGENTS.md`, `tests/AGENTS.override.md`, root `EXEC_PLAN.md`, original Brief 2 and preserved paused plan.
- Planning `OWNER_REQUEST.md` and `PLANNING_EVIDENCE.md`; the latter's packaging/environment claims were treated as author evidence rather than independently rerun product proof.
- `docs/architecture/IMPLEMENTATION_AUTHORITY_INGRESS.md`, `docs/architecture/OWNERSHIP_AND_COMPONENT_LAW.md`, and `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md` (BC-001–016).
- SQLite proof-admission addendum, M00 SQLite proof contract, raw SQLite admission pointer and generation0003, and `M00_SQLITE_PROOF_REVIEW_20261019.md`.
- Repository `README.md`, `Makefile`, `pyproject.toml`, and the observed documentary diff of the root/test-local agent maps.

Partial primary inspection:

- `src/nvda_desk/raw_signal_occurrence_truth/api.py`: observation/selection/mapping/projection records, read facade, admission/idempotency/high-water, projection and history implementations.
- `_sqlite.py`: connection mode/settings, observation enumeration/append, transaction lifecycle and persistence factory. This was not an exhaustive schema/codec audit.
- `tests/product/raw_signal/test_u03_observation_native_temporal.py`: temporal/native/identity/sequence assertions (read the returned file text); `tests/product/raw_signal_sqlite/test_contract_native.py`: record fields, native fidelity and conflict cases; `_support.py`: actual owner construction and fresh-process transport. Relevant test reads are not runtime evidence.
- Relevant Git object/log/diff lineage described above; not a whole-repository historical audit.

Not independently inspected in full: every incorporated PA-02 authority object, original complete M00 freeze/admission chain, full SQLite implementation brief, complete affected source/test closure, PostgreSQL adapter, external live provider environment or all historical attached archives. Those limits are compatible with documentary clearance because L00 explicitly owns authority/baseline/full affected inspection closure and blocks dependent execution on any missing invariant. They do not certify future execution readiness as already achieved.

No product tests, collection/import proof, static product checks, runtime installation, provider query or product/config/test mutation was performed. This worker writes only this review. Documentary hash/Git/source reads are the verification obtained. Packaging integrity remains the authoring worker's separate checkpoint task.

## Final hash-specific recheck

Final reviewed root `EXEC_PLAN.md` SHA-256: **`48855924ced49fb5b0b28e681b79cdd0e29032efb1441cd3071c1d961f731366`**. Disposition remains **APPROVED_DOCUMENTARY**. Independently hashed the current root plan and reconstructed the initial reviewed bytes by reversing exactly three status/progress replacements; the resulting SHA-256 equals the initial reviewed hash above. Thus the final delta is exactly the documentary status, independent-review checkbox/reference and external packaging-progress location, with no semantic plan change. Full guardrails were reread before this final response. The implementation leaves remain NOT_ATTEMPTED; checkpoint packaging is separate from this review.
