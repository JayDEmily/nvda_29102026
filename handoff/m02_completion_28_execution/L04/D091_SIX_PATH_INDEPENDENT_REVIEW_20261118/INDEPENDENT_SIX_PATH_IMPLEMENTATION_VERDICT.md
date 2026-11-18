# Independent D091/L01b six-path implementation review — 18 November 2026

**Verdict: RETURN.** This is a bounded source-implementation review, **not** product-test execution, claim admission, proof generation, product acceptance, PR merge or D145 reactivation.

## Exact scope and evidence

- Repository: `JayDEmily/nvda_29102026`; independently commissioned at `2f42405d64c24b73227fa8515df9c3430542864c` in `handoff/m02_completion_28_execution/L04/D091_SIX_PATH_IMPLEMENTATION_20261118/INDEPENDENT_SIX_PATH_IMPLEMENTATION_COMMISSION_20261118.md`.
- Reviewed candidate commit: `e8557095c8b7e555e6bfdc0df215aaa7036674d5`; **independently verified Git tree** `ecf4a0a8f9e229c5d26ae2ec993ff0e1af580bbf` (`git show -s --format=%H:%T:%P` in a separately cloned, detached worktree). Preceding candidate: `f2e8e3ef9fa112805a3f53155266d9db612046df`. `git diff --check` across that interval returned no diagnostics. No changes were made to the Worker branch.
- Read the root `GUARDRAILS.md`, `AGENTS.md`, active `EXEC_PLAN.md` in full, applicable `tests/AGENTS.override.md`, the pinned commission and Worker handover; inspected the owner-adopted R112 source contract, the A–E negative-only owner decision, the separately admitted 18 D091 / 15 L01b case inventory, the repaired pre-edit technical binding and preceding independent authoring verdict. The 18+15 case approval **does not** release execution.
- The six reviewed paths, independently byte-identified at the candidate, are:
  1. `src/nvda_desk/market_measurement_truth/api.py` — SHA256 `144d3de0c3c59d9a503fd86351c9305f893b02d66b84bfd17e7dbd910f1307e2`;
  2. `src/nvda_desk/market_measurement_truth/_controlled_r112.py` — SHA256 `0fcec581bd040e6c1e8cfb6adde080a789659e8314a4ddeecbf8981a7eb0b1ee`;
  3. `src/nvda_desk/market_measurement_truth/_native_codec.py` — SHA256 `b3d247b4396073d5059e674b9392c03e1b9ce3e418b9a9f1df56417255847759`;
  4. `src/nvda_desk/market_measurement_truth/_native_d091.py` — SHA256 `171846acf03486e7f7b074ef2d8c43b5af540ef903003e1a6fe247ca50ae9e96`;
  5. `src/nvda_desk/market_measurement_truth/_record_store.py` — SHA256 `882a61238b74ba5aa2ffacf95d0587633392722d2336a3954681c6ac0a86f0ef`;
  6. `tools/product_proof_claims.py` — SHA256 `59b9a6037142f7d553aa731f7b1926b81dadd6fcca23bf0a267121dfa94a5bae`.
- The unchanged test-authoring files were read without import, execution or collection: D091 SHA256 `d1eab7802786344ecf9ab4d4e2f46b802aba6d2fea0c72d14ad149492504b86f`; L01b SHA256 `1f648998ca4c64829a3655057598e5ae5687b6568bb7e9eebf7ca2f17caa56f5`. Their earlier `ACCEPT_REVISED_TEST_AUTHORING_ONLY` is not an implementation verdict.

## F01 — RETURN: the sealed private M00 write boundary is not enforced by the returned coordinator

**Accepted requirement.** `handoff/m02_completion_28_execution/L04/D091_PREEDIT_IMPLEMENTATION_BINDING_20261117/IMPLEMENTATION_BRIEF.md` §2 and `handoff/m02_completion_28_execution/L04/D091_FINITE_ADEQUACY_REVISION_20261117/COHORT_AND_FIELD_REACHABILITY.md` RETURN-01 require genuine exclusive closed-batch admission, no caller-accessible M00 command or writable alias, a one-way seal and no unlisted M00 admissions. The owner-adopted `L01b/R112_SOURCE_CONTRACT_PROPOSED.json`, `selection.closed_batch_precondition`, requires excluding all further admissions throughout selection/pagination. This is a source-invariant requirement, not a demand for adversarial product testing.

**Observed code.** The factory `create_controlled_coordinator()` returns a `_Coordinator` instance (`_controlled_r112.py:264-268`). This same returned object has a slotted `_writer` attribute (`:202`), assigned directly from the genuine `owner.commands.admit_raw_observation_occurrence` (`:204-208`). Only `checked_admit()` (`:217-234`) checks preseal state, exact source fields, expected roster and the coordinator admission set before invoking `self._writer` (`:229`). The underlying M00 command itself checks generic identity and sequence high-water, not the coordinator's seal (`src/nvda_desk/raw_signal_occurrence_truth/api.py:1395-1465`).

Consequently, a holder of the factory's returned coordinator has a direct bound write-method alias at `coordinator._writer`; invoking it does not traverse `checked_admit`, its lock, its roster or its postseal refusal. This conclusion is a **static code-path derivation**, not a claimed executed product stimulus. The underscore naming convention and `__slots__` do not prevent direct attribute access in Python. The independent source capability restriction is therefore weaker than the explicit no-writer-alias requirement.

The seal checks `_state["admitted"] == set(_roster)` and reads back only the expected roster (`_controlled_r112.py:236-248`); it does **not** enumerate the complete actual M00 owner membership to establish that no unlisted raw observation was admitted. A call through that retained write alias would not update the coordinator's `_state["admitted"]`. Thus the seal cannot independently certify full M00 closure if the alias is used, and the accepted successful-source exclusivity premise is not mechanically guaranteed.

**Impact and disposition.** The reviewed source does not establish the required writer isolation / genuine closed-batch invariant; therefore a source-level implementation preparation acceptance would be premature. The older design's RETURN-01 concerns genuine independently sealed source ownership; this implementation problem belongs to that **source-closure mechanism class**, not to SQLite or the separate L01b negative field tests. Return only this bounded source-interface/isolation proposition for Worker correction and a fresh independent review. Do not infer authorisation for new physical case IDs, product runs, a replacement successful R112 population or claim admission.

## Other five paths — static observations, not runtime proof

- `api.py`: exact D091 category/request/occurrence and output-only five-field observer types are separately represented; H02 relative clock ordering is deferred to `materialise` while individual instant types remain validated. This aligns with the preceding F01 authoring revision.
- `_native_codec.py`: D091 DTO classes are specifically allowlisted; the canonical codec preserves native signed Decimal tuples without float coercion.
- `_native_d091.py`: Stage A clock/seal, actual private original readback B, cursor-page collection/tie/bound C, selector-only getter comparison D, exact-as-of source target E, target-only Decimal domain F and typed SQLite G are present. D03's second invocation uses a coherent alternate 0.498 candidate while retaining the first logical identity; the independently inspected test source checks the real `RecordState._existing` traceback. None of these observations repairs F01.
- `_record_store.py`: D01 raises after actual INSERT before COMMIT (transaction rollback); D02 callback raises after actual COMMIT (uncertain acknowledgement); D03 relies on existing canonical immutable conflict detection. These placements were inspected but **not executed or proved**.
- `tools/product_proof_claims.py`: the two precisely SHA-pinned unadmitted test files are staged without an unconditional claim; future D091 registration is conditional on an exact descriptor, correct 18/15 jurisdictions, validated authority and immutable generation. No pointer or generation was created by this review. Prospective runner/registration correctness remains unexecuted.

The Worker-authored 22/22 static check receipt was inspected as **attributed static evidence**, not substituted for independent semantic correctness or a strict product run.

## Restricted close-out

**RETURN** for F01; no other source defect is asserted as verified by this review. No product test was run, imported, collected or fabricated, no negative source stimulus was invoked, no live/production policy was admitted and no proof generation, claim, ledger, Worker branch, PR or main state was changed. The 18 D091 and 15 L01b physical cases remain separately admitted **without execution release**; strict independent Tester, exact runtime/L00 prerequisites and future claim/generation admission remain held. D145 stays PAUSED.

Reviewer action: commit only this verdict on `review/d091-l01b-pr27-six-path-implementation-independent-20261118-gpt6`; verify committed SHA, tree, single review-file delta and remote readback. This independent review **does not authorise the Worker branch to be changed by the reviewer**.
