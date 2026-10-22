# Independent D015 implementation review

Disposition: **RETURN** for one bounded public-factory contract defect. This is independent judgement, not admission or permission to change admitted proof bytes. No D016 work is authorised by this report.

Exact candidate `cde2c853abe3fafc5e4a6f01879003d1062b7b7a`, tree `1aad0ebd2e6c1fd325af786781c76c77b5d92a80`. Fresh private `git clone --no-hardlinks` at `/tmp/d015-implementation-review-g91a2oam/repo`; all execution below uses the candidate's own source. No active source edit or reviewer repair.

## F001 — ISOLATED: factory admits objects without the declared public reader facets

Authority: exact D015 brief section3 fixes `raw_projection_reader:RawProjectionReaderV1` and `predecessor_reader:MeasurementReadsV1` and expressly requires wrong public types to raise TypeError. Lawful data absence is a different case returning None; a structurally absent reader is not lawful missing data.

Location: `src/nvda_desk/market_measurement_truth/_trade_direction.py:481–500` (`build_owner`, called by the public `create_trade_direction_owner`). It checks admission, clock and storage, but does not establish either reader's callable public operations before returning an owner. Existing retained D014 `_raw_rational.build_owner` checks callable `list_projected_raw_history`; D013 `_rational.build_owner` checks all six complete predecessor-read operations. The new factory omits both kinds of structural contract validation rather than inheriting them through the reused calculation helpers.

Actual helper-independent discriminator, fresh private candidate, no Worker test/helper or private calculation function called:

```python
f.create_trade_direction_owner(
    admission=f.OwnerAdmissionV1("M02", EXACT_D015_BRIEF),
    raw_projection_reader=object(),
    predecessor_reader=object(),
    storage=f.MemoryStorageV1(),
    utc_now=valid_utc_clock,
)
```

Observed: the public factory returned `_Owner`, rather than raising TypeError. The probe's required-invariant assertion then failed, process1. Complete command/output is preserved in `03_factory_first_failure.log`; exact executable probe is `factory_probe.py`. The parent independently noticed this omission during its self-review and asked this reviewer to evaluate it; the observation above is this reviewer's own reproduction and judgement, not an unattributed parent result.

Required bounded closure proposition: **the new public owner factory rejects structurally invalid raw/predecessor reader facets with TypeError at its constructor boundary, while retaining valid public readers and the admitted six-case calculation behaviour.** Check the operations the new service actually requires, including complete predecessor evidence capture; type annotations alone do not enforce structural protocols. This is a public factory boundary obligation, not a request for a generic malformed-input matrix, new parameterised cases, rewritten contract or changed immutable product generation. A small attributable direct boundary discriminator is sufficient. No specific implementation patch is prescribed.

Classification is **ISOLATED**: this is the first D015 implementation-review boundary omission. The inspected earlier F001–F004 design corrections concern exact predecessor admission/configuration/causal selection/new-store proof specification. Authored-proof P001 concerned incomplete payload oracles and was closed before generation admission. Neither is the current structural factory-reader omission. The precommit mypy fixes added exact native-value/event guards and a typed version tuple; they were static narrowing repairs, not an earlier failed independent factory contract review. No second successive materially related unresolved finding was established.

At this first proved required failure, dependent acceptance work stopped. A prepared helper-independent valid-stream transition script `direct_public.py` was **not executed**; it is not evidence of calculation, transition or persistence success. No further negative probes, domain reruns or downstream repair were attempted. Possible later AttributeError or SQLite creation before rejection is source-level risk, not an independently executed result claimed here.

## Verified evidence before stop

- Read frozen GUARDRAILS/root AGENTS/current root EXEC_PLAN/test override; exact admitted D015 brief, contract, binding, generation; preserved initial/v2 design and authored-proof RETURN/closure; semantic first RED lineage; new API/service/store and admitted physical test; reused public constructor literals, eligibility/selection, canonical decoding, predecessor capture/validation and existing store-path policy.
- Exact brief SHA256 `84baa16665db5f8543eba3b1770dafcfb36cc5e8064b2f1837beb924713acb0d`; contract `e4d481ca99dbb55e2ad4b753dc33b8ba244873eac50e541a8352a6f5384a73c5`; generation `d495a09f834349b7817a28911a58afa372b635ed0d1d211efd4fc8a4f822e543`; physical test `95de43d4538ee3b302430c7c6455edef0373e6bb09ee2f2cb111bfc54178f2fc` independently verified.
- Fresh complete strict command: `/workspace/scratch/83dd7c79f14f/d015-runtime-GUbvor/dev/bin/python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d015`, cwd private exact candidate. Observed six passed0.38s; READY_FOR_PROOF; exact brief/generation/candidate above; aggregateexit0/process0. Complete output in `02_strict.log`. This establishes the admitted six cases, not the missing factory-error boundary.
- Preserved first semantic RED log identifies clean `7b141bd71cc0f2a948df35e50b0ca1fb2963ffe3`: six missing-seam assertion failures after real raw/D011 prerequisites, aggregateexit1. Current physical proof/generation are unchanged since that checkpoint. No imported scalar predecessor or test weakening is introduced by implementation.
- Preservation audit compares all2094 tracked files private versus active: identical bytes with distinct tracked working-file inodes. Private status is clean. Original API is an exact byte prefix of the appended API. Diff from admitted RED checkpoint includes only two new D015 modules, appended API, plan progress and preserved RED log. Therefore old M00/M02 modules, old proof, contracts and generations are unchanged. `04_preservation_audit.json` records candidate/tree/hashes/diff.
- Static source inspection supports the intended fixed configuration/equation, trade-time quote selection, complete prior history beyond freshness, distinct controlled quote correspondence, predecessor evidence validation, exact-int result, canonical logical identity and separate SQLite profile/table/triggers/full typed payload/hash/readback. These are review observations, not acceptance of unexecuted conditions beyond the admitted proof. The first-failure finding above prevents a whole-unit PASS.

## Reused and unfinished evidence

Parent's exact-candidate source/four-control-tool/positive-consumer mypy log was inspected: Success41files with two existing untyped-body notes. Its changed-path Ruff log says all checks passed. These are parent-run results, not independently rerun commands here. Main's architecture promotion was still running when the factory defect was confirmed; no promotion PASS is claimed by this report. The previously reviewed unchanged full149 shared-control result was not needlessly duplicated; current loader/test bytes are outside this implementation diff.

No full old-domain aggregate, new generic mutation matrix or D016 test was run. No runtime environment reinstall, provider certification, full-tranche completion, final product acceptance or new owner/domain authority is inferred. The review is bounded by the first reached failure, with exact successor review needed after lawful repair. Main retains the concrete disposition and determines affected validation for the repaired candidate under the current plan.

All commands and complete runtime outputs are in this directory. `run_review.py` records cloning/checkpoint/strict execution and stops on failure; `run_probe.py` records the direct first failure; `audit.py` performs read-only preservation checks after the stop. The audit does not resume downstream semantic acceptance.
