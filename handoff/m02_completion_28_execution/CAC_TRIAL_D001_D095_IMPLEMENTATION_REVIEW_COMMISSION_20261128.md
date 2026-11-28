# D001/D095 first-stage implementation checkpoint and independent review commission

Worker disposition: IMPLEMENTED_UNTESTED for D001 and D095 separately. No product acceptance, registration, execution or release. D095 L10a/L11 is one jurisdiction.

Received handoff: 84be5ec50df42cda48b0ee4352311d3e32ed924b
Exact product candidate C: f0cf010f62719e3e9c21fddb2d45474295afcf6e
C tree: 1ac70938abfb661bdb0c9bcb510a4e1057c16fc1
C tracked listing: 4550 entries; SHA256 60b5d59d4ca94e2e27a69858caee0d33b214b7eb8ec3055974c14083ec5da062 (git ls-tree -r -z --full-tree C).
The review handoff H is the direct child of C containing this commission and execution register only. Fetch H exactly; stop on mismatch.

## Authority and immutable reviewed inputs

### D001: SUP-D001-OPTION, 4 cases
Separate authoring verdict: 51e4e2bc0693a65987c8264a53d50d3ce2f5303c / 8efb8cfd5fa5423b5410fc41b486729ed5bc0875; parent 92a6dce2022f5e51994b417fcda30767507413d3; refs/heads/review/trial-cac-nvidia-d001-d095-authoring-20261128; handoff/m02_completion_28_execution/INDEPENDENT_CAC_TRIAL_D001_D095_AUTHORING_VERDICT_20261128.md; SHA256 c183df146ae5afd2423b26b186ddc0cd0234a315b146ed63387c929779b60c5f; blob 8c47b616c2a27fc90dbf17276a8f4078524031f9.
- handoff/m02_completion_28_execution/L07a/D001_IMPLEMENTATION_BRIEF.md: 222d0919c67c05f6436f985b8262ace985ab11dea30fc045333ee13fa10a8d8d
- implementation/authority/T01_D001_OPTION_TIME_AUTHORITY_BINDING.yaml: ff80ea7dd3aa7674723b758dda9173356bda75119ba996ece5bf4c1a9ff2cf35
- handoff/m02_completion_28_execution/L07a/OPTION_TIME_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json: 14a3ba2308f519d90d11eb450ac484a2c922507b7e04041c740297527a1d847a
- handoff/m02_completion_28_execution/OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json: 6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41
- handoff/m02_completion_28_execution/L07a/D001_TEST_SOURCE.py: 6bedaf2e25bc06c1c3a8f116f9f852fbaa0e94e4a916bdd80defee2519cbd867
- handoff/m02_completion_28_execution/L07a/D001_PROOF_CONTRACT.json: a18704f720dce0bd77a2c16f098846fe02b7e4027ec2715cdb7c0663b6e43ad5
- handoff/m02_completion_28_execution/L07a/D001_CLAIM_CANDIDATE.json: 84d7116b41d01fe59877f7841c9e376cd2d517fe7bf7c010a4c33ad6fb014e81
Physical test and descriptor absent. Ordered exact reviewed cases:
- SUP-D001-OPTION-SUCCESS: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_success
- SUP-D001-OPTION-REACHED_REFUSAL: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_date_only
- SUP-D001-OPTION-RECEIPT-ONLY: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_receipt_only
- SUP-D001-OPTION-OFFSET-MISMATCH: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_offset_mismatch

### D095: M02-C28-D095, 7 cases
Separate authoring verdict: 51e4e2bc0693a65987c8264a53d50d3ce2f5303c / 8efb8cfd5fa5423b5410fc41b486729ed5bc0875; parent 92a6dce2022f5e51994b417fcda30767507413d3; refs/heads/review/trial-cac-nvidia-d001-d095-authoring-20261128; handoff/m02_completion_28_execution/INDEPENDENT_CAC_TRIAL_D001_D095_AUTHORING_VERDICT_20261128.md; SHA256 c183df146ae5afd2423b26b186ddc0cd0234a315b146ed63387c929779b60c5f; blob 8c47b616c2a27fc90dbf17276a8f4078524031f9.
- handoff/m02_completion_28_execution/L10a/D095_IMPLEMENTATION_BRIEF.md: 4885ee1efe9f5832f33a8bf0552caf288990f9f992542c26f535bf378bcbc703
- implementation/authority/T01_D095_PRIOR_SESSION_IV_AUTHORITY_BINDING.yaml: 2a4530490537b2552b320db240ac09eb24508ccc9d9347316e517463c4548f32
- handoff/m02_completion_28_execution/L10a/OPTION_IV_PRIOR_SESSION_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json: 050d167a6f15ae210f3a0b7a776957e6ebb00ce8f674ad9d417e7082951b6a39
- handoff/m02_completion_28_execution/OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json: 6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41
- handoff/m02_completion_28_execution/L10a/D095_TEST_SOURCE.py: 50173aa60e71fae8fe969e631f15b92eb8521ef174b845dcfcb2ab3ff0e7b6a8
- handoff/m02_completion_28_execution/L10a/D095_PROOF_CONTRACT.json: 651c9cea0db295b16eafccfb3f8a9f042e7893cc3430b28ca29d9defcbb454aa
- handoff/m02_completion_28_execution/L10a/D095_CLAIM_CANDIDATE.json: 0eb917d707fe6045d621319b397d9808968393a02cf62510c3a272d38f388bda
Physical test and descriptor absent. Ordered exact reviewed cases:
- D095-CONTROLLED-SUCCESS: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_success
- D095-CONTROLLED-REACHED_REFUSAL: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_session
- D095-CONTROLLED-LATE-REFERENCE: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_late_reference
- D095-CONTROLLED-WRONG-CONTRACT: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_contract
- D095-CONTROLLED-WRONG-MODEL: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_model
- D095-CONTROLLED-WRONG-UNITS: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_units
- D095-CONTROLLED-DUPLICATE-VINTAGE: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_duplicate_vintage

## Source delta and serial execution

D001 initial d7017b269619aa63f70aed412ad97a46568ebe06; static format and mode correction 2c6ba7c8bbcdb0b2e2c264ddea5a73b22a8f07d5. D095 initial ac747b7d2076a7b788ceef401e575a35563a64a2. Scoped native-path typing corrections serially D001 dc443098aec90a1323b7209844f3adb57cf33c3f, D095 f0cf010f62719e3e9c21fddb2d45474295afcf6e. Existing API prefix retained, G01 additions only; no legacy/M00 changes.

- src/nvda_desk/market_measurement_truth/_option_iv_prior_session.py: SHA256 f417e612752a4f94fbbae0f7c655c3c39dfef7f2d462807a0128b8cda2b56d09
- src/nvda_desk/market_measurement_truth/_option_time.py: SHA256 ea4f4a931561ac73414def19dffa35894446d8fc3fab50f7df4ec4dbc5c96572
- src/nvda_desk/market_measurement_truth/_option_time_codec.py: SHA256 c989b87df4944b89ad29cbc1f2e5d897ffc490e97078913d386043872e2ebf5c
- src/nvda_desk/market_measurement_truth/_option_time_source.py: SHA256 18b3922caa8c2ae99999f9bcfe8c10eacb48b8d32234b0718f1f595de0a447f8
- src/nvda_desk/market_measurement_truth/api.py: SHA256 d1bcb337ea166d3cdf8a30cc89f7d3d0db822abaebde810cff3ac979eb0f406c
- tools/product_proof_claims.py: SHA256 c77ffc08d586735d056ee9ff347ca5dfe16156e899ebc1839842d98cd2813ba2

D001 uses actual public M00 admission, retrieval and projection plus complete bounded history, native true-instant role and offset comparison, typed public carrier, canonical identity and durable readback validation. D095 uses its own exact synthetic source and public M00 ingress, complete roster and calendar, actual receipt/contract/model/units and unique highest eligible final prior-session reference, exact Fraction arithmetic, typed carrier, canonical identity and durable validation. D095 source logic is independently scoped; both use existing native codec and RecordState without altering those shared mechanisms. G01 fixed per-claim pinned descriptor routes are dormant without the separately cleared descriptor; existing partition and generation machinery is retained. These descriptions are implementation intent, not a reviewer verdict or proof result.

## Static checks and checkpoint limitations

- Final scoped py_compile of the six paths and git diff --check passed. Scoped Ruff 0.15.11: only three identical baseline api.py findings (E402:2594, I001:2666, E501:2727). Scoped mypy 1.20.1, --follow-imports=silent --no-incremental --cache-dir=/dev/null, five M02 paths: only five identical baseline ScalarStraddleSourceV1 attr-defined findings (2873,2877,2881,2886,2896). New native nested-field typing findings were repaired in the two serial correction commits; no baseline edits. Existing local venv used, no installations. No product import, test collection/execution, runtime proof or qualification.
- Exact reviewed proof, contract, claim, brief, policy and installed binding bytes unchanged. No physical tests, active descriptor/claim/admission or release; allocation ledger unchanged (SHA256 5d1ac21a0cf62fe98efe5d4bd5c510094d139e6ae6bd3fc85d10924d67189c89); 17 allocations / 64 cases remain held as governed.
- Fetched remote heads/tags into private refs/audit namespace (357 refs). Exact original trial ref verified. All 170 historical object tips available and exact types matched (123 commits, 26 blobs, 20 trees, 1 tag) against REQUIRED_REF_RESULTS.json (2281 contextual rows, 797 literal name/tip pairs, 66 original name/tips); initial all-commit assumption corrected to actual type check. Full git fsck --full --no-reflogs passed. The 21 vendored wheel hashes matched recorded actual_sha256 (expected_sha256 null for vendor rows) in NON_GIT_ASSET_RESULTS_CURRENT.json. Existing 66 VERIFIED, 5 BLOCKED, 1 UNKNOWN historical non-Git asset dispositions preserved; no assertion of newly restored historical binaries, runtime qualification or independent receiver restoration.

## Commission: fresh distinct independent implementation reviewer

Read AGENTS.md, GUARDRAILS.md, EXEC_PLAN.md, tests/AGENTS.override.md and execution register at exact H. Independently reconstruct candidate C/tree/listing, ancestry, changed paths, historical ref/asset evidence and authority pins. Verify separate exact independent authoring verdict and both actual product slices against their own briefs, accepted policies, reviewed proof source, contracts, claims, case discriminators and installed binding. Trace actual public M00 ingress/get/direct projection/complete bounded history, native roles and semantics, source selection/roster, temporal/calendar/receipt/vintage compatibility, exact identity, durable payload validation and replay. Assess whether actual public construction and durable reopen genuinely meet the reviewed obligations without fixture-only short cuts or prewritten oracle values. Inspect G01 fixed dormant routes and strict generation/partition behaviour; verify no active registration or other-scope edits. Review statically; no product import, collection, execution, activation or release.
Issue separate ACCEPT_DOCUMENTARY_IMPLEMENTATION / RETURN / BLOCKED dispositions for D001 and D095, D095 counted once across L10a/L11. Classify any finding under AGENTS.md and identify exact evidence and bounded corrective scope. Do not accept runtime or product on documentary evidence. Publish a separate verdict as direct child of H on new refs/heads/review/trial-cac-nvidia-d001-d095-implementation-20261128 at handoff/m02_completion_28_execution/INDEPENDENT_CAC_TRIAL_D001_D095_IMPLEMENTATION_VERDICT_20261128.md, verify commit/tree and readback, then reconcile dispositions on the trial branch and commission eligible distinct-role succession once under the owner-adopted CAC MVP. On ACCEPT, next registration preparation/independent registration clearance remains required before activation; on RETURN commission only bounded corrective work; on BLOCKED preserve holds. Sole designated strict Tester unchanged; candidate-specific intake and precall release required. No G01 R2 adoption, main/original-work edits, promotion, new allocations or Tester appointment. No test execution by Worker or Reviewer.
