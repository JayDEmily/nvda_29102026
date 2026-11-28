# D001/D095 inert registration preparation and independent review commission

Worker disposition: INERT_REGISTRATION_PREPARED_INDEPENDENT_REVIEW_REQUIRED_EXECUTION_HELD, separately for D001 SUP-D001-OPTION (4) at L07b and D095 M02-C28-D095 (7) at L10a/L11 (one jurisdiction). Both remain IMPLEMENTED_UNTESTED. No product acceptance or execution.

- Received exact H: a1ff344c97c54a822bce9341d5aa38fdb9a139c8; verified clean fresh Ubuntu clone.
- Inert preparation candidate C: 7df86afeac63af59105786a2410734da12b7460c; direct parent H; tree 86a827fc9c84170e72985a29fe3a7397251dce0a; 4555 tracked entries; recursive listing SHA256 96f3072bc4b5d9f7e287b6886a6da919a066cc391d0b2796bd376d4030f75667 (git ls-tree -r -z --full-tree C).
- The review handoff is direct child of C, changing only this commission and the execution register. Fetch exactly and stop on mismatch.
- Exact independently cleared source candidate f0cf010f62719e3e9c21fddb2d45474295afcf6e tree 1ac70938abfb661bdb0c9bcb510a4e1057c16fc1; implementation review at 61b14032a56fec9dee4309e8bd3ccc01260bfbb9 tree 68b934a891a20e4b437da60e5d6255b2e636a945 ref refs/heads/review/trial-cac-nvidia-d001-d095-implementation-20261128 report SHA256 7f3d981d5ae87c73465a834b38a6b2b10535c4a0e57c9659faa68863ad6e2910. Separate ACCEPT_DOCUMENTARY_IMPLEMENTATION for both. Authoring verdict 51e4e2bc0693a65987c8264a53d50d3ce2f5303c, tree 8efb8cfd5fa5423b5410fc41b486729ed5bc0875, report SHA256 c183df146ae5afd2423b26b186ddc0cd0234a315b146ed63387c929779b60c5f, separate ACCEPT_DOCUMENTARY_AUTHORING.
- Exact prior implementation review commission: handoff/m02_completion_28_execution/CAC_TRIAL_D001_D095_IMPLEMENTATION_REVIEW_COMMISSION_20261128.md SHA256 3af85601942c4f392b189170d3201d799cadf55003fb39bf1f864dd64d2696ad. Rechecked all 20 path/hash pins against source candidate and current bytes. All family authoritative input pins checked; claim, proof source and contract unchanged. Shared path-only remap accepted at 5da8986e88d777975edae36fc65eaf8a229e29e4 tree 059362c14f0d62a99baf07b429e4dbf779e6b3f8, report SHA256 0aab07086e35fe266bcf20f3dfba2934164c39188c641d6dc14318ebc72900e7. Original grant SHA256 6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41; remap SHA256 11d90adf234d5195d3bd31a6b42df9b046c4ad53690cb279ef071d52b3049aa7. No semantic or case change.
- Exact ledger unchanged SHA256 5d1ac21a0cf62fe98efe5d4bd5c510094d139e6ae6bd3fc85d10924d67189c89. Verified all 17 allocations, nonfungible ceilings, 64 ordered case IDs and remapped nodes, execution_release false and per-case execution_authorised false. No active physical test root, claim descriptor, generation or admission pointer for either D001 or D095. No product source, ledger, schedule, governance or other scope change.

## Exact candidate packages

### D001 ? SUP-D001-OPTION ? 4 cases

Claim: neutral_market_measurement_truth_l07b_d001_option_time; target M02. Generation 1, previous_generation null, exact family only, no support files.

- handoff/m02_completion_28_execution/L07a/D001_TEST_SOURCE.py -> tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py | SHA256 6bedaf2e25bc06c1c3a8f116f9f852fbaa0e94e4a916bdd80defee2519cbd867 | Git blob a83eaf71ed6fbb2521f54d3389b3d6d0d834a204 | 18106 bytes. Future destination is NOT installed.
- handoff/m02_completion_28_execution/L07a/D001_CLAIM_CANDIDATE.json -> config/product_proof/m02_option_time_d001/claim.json | SHA256 84d7116b41d01fe59877f7841c9e376cd2d517fe7bf7c010a4c33ad6fb014e81 | Git blob e5863963dba0e0b8f0a9a504f5477ed69a0b20d2 | 535 bytes. Future destination is NOT installed.
- handoff/m02_completion_28_execution/L07a/D001_GENERATION_0001_CANDIDATE.json -> config/product_proof/m02_option_time_d001/generations/0001.json | SHA256 ab50355f7d0d3625b062a665809fc80192fc92ec842b1444a7e51d0bb1add5b9 | Git blob 00726c45a4f64d883967a58073d89e0be64af5cf | 1526 bytes. Future destination is NOT installed.
- handoff/m02_completion_28_execution/L07a/D001_ADMISSION_CANDIDATE.json -> config/product_proof/m02_option_time_d001/admission.json | SHA256 32fcf9d05a45daf9e669b4861d8173341d206acc27f20d6c195a074a0d9858c1 | Git blob 4c2492d5b24069b7ea729cde1ea08c2b13e12eac | 221 bytes. Future destination is NOT installed.

Ordered cases and remapped nodes:
- SUP-D001-OPTION-SUCCESS: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_success
- SUP-D001-OPTION-REACHED_REFUSAL: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_date_only
- SUP-D001-OPTION-RECEIPT-ONLY: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_receipt_only
- SUP-D001-OPTION-OFFSET-MISMATCH: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_offset_mismatch

### D095 ? M02-C28-D095 ? 7 cases

Claim: neutral_market_measurement_truth_d095; target M02. Generation 1, previous_generation null, exact family only, no support files.

- handoff/m02_completion_28_execution/L10a/D095_TEST_SOURCE.py -> tests/product/m02_completion_28_prospective/d095/test_signal.py | SHA256 50173aa60e71fae8fe969e631f15b92eb8521ef174b845dcfcb2ab3ff0e7b6a8 | Git blob 31d381c70b6f2391070ecbcbc3dca344208971b8 | 23044 bytes. Future destination is NOT installed.
- handoff/m02_completion_28_execution/L10a/D095_CLAIM_CANDIDATE.json -> config/product_proof/m02_option_iv_prior_session_d095/claim.json | SHA256 0eb917d707fe6045d621319b397d9808968393a02cf62510c3a272d38f388bda | Git blob d801faa3308691c0446975f94a54ac9192e5bb81 | 520 bytes. Future destination is NOT installed.
- handoff/m02_completion_28_execution/L10a/D095_GENERATION_0001_CANDIDATE.json -> config/product_proof/m02_option_iv_prior_session_d095/generations/0001.json | SHA256 dc4e6af18629757ec51886626a76ff19a1c78b8c920954fd3a67b90c358fcba4 | Git blob 34db9a6a531533a85301b3fa0c1267d3a4005a1a | 1493 bytes. Future destination is NOT installed.
- handoff/m02_completion_28_execution/L10a/D095_ADMISSION_CANDIDATE.json -> config/product_proof/m02_option_iv_prior_session_d095/admission.json | SHA256 2484747464c02a4b6e5dc114ed43a64c768704eb0b8d2c32d2d5e8f28b56134e | Git blob ca18680716db7fffca3066b1851df9a2df5c04d5 | 233 bytes. Future destination is NOT installed.

Ordered cases and remapped nodes:
- D095-CONTROLLED-SUCCESS: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_success
- D095-CONTROLLED-REACHED_REFUSAL: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_session
- D095-CONTROLLED-LATE-REFERENCE: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_late_reference
- D095-CONTROLLED-WRONG-CONTRACT: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_contract
- D095-CONTROLLED-WRONG-MODEL: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_model
- D095-CONTROLLED-WRONG-UNITS: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_units
- D095-CONTROLLED-DUPLICATE-VINTAGE: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_duplicate_vintage


## Mechanical documentary validation and limitations

- In a separate disposable detached Git worktree at received H, staged both exact prospective package byte sets only for validation. Existing G01 tools/product_proof_claims.py load_product_proof_claim ran for each with both packages present, including existing catalogue, exact descriptor routes, authority/schema, generation history/membership, and whole physical partition checks. Both reported READY_FOR_PROOF, target M02, exact expected generation SHA256 and exact ordered family nodes (4 and 7), no support files. This is a hypothetical static registration compatibility result ONLY; actual branch remains inert, no proof release.
- Used existing /home/jds/nvda_uv3135_20261112/.venv/bin/python -B; first invocation omitted tools directory on sys.path and failed ModuleNotFoundError validate_product_proof (no product execution); corrected import path and re-ran static validation exit 0, not a product test. Confirmed no nvda_desk.market_measurement_truth or nvda_desk.raw_signal modules imported. No product import, collection, execution, runtime qualification or independent product acceptance. AST inspection verified precisely reviewed function names, no collection. An earlier combined terminal call was refused by shell command parsing (unexpected token); no operation ran; used ordinary direct worktree command.
- Remote heads/tags fetched to private audit namespace (358 refs), trial input exact. All 170 historical object tips available (123 commits, 26 blobs, 20 trees, 1 tag) against 2281 contextual rows and 797 literal name/tip pairs, including 66 original names/tips. Full git fsck --full --no-reflogs passed. All 21 vendored wheel hashes and byte lengths match recorded actual values. Historical non-Git asset dispositions 66 VERIFIED, 5 BLOCKED, 1 UNKNOWN retained; no claim of newly restored historical binaries or full independent Tester restoration.
- G01 R2 not adopted, D145 paused, five earlier accepted proof allocations retained. Sole designated strict Tester unchanged; candidate-specific intake and precall release remain required.

## Commission: fresh distinct independent registration-preparation reviewer

Read AGENTS.md, GUARDRAILS.md, EXEC_PLAN.md, tests/AGENTS.override.md and execution register at exact received handoff. Verify C/tree/listing and parent, scoped delta, both exact independent implementation and authoring dispositions, owner grant, remap acceptance, source/claim/contract/brief/binding/policy bytes, generation and admission candidates, correct future destinations, exact physical family hashes, support membership, no predecessor, and all 11 ordered cases as the exact separately held allocations. Independently validate existing G01 schema, generation and whole physical partition compatibility in a separate disposable non-active validation tree, with both prospective packages present; no product import, collection, execution or changes to active physical roots or claim/admission metadata. Verify all 64 remain held, exact ledger unchanged, D145 PAUSED, G01 R2 unadopted; no new allocations or other-scope changes. Issue separate ACCEPT_DOCUMENTARY_REGISTRATION_PREPARATION / RETURN / BLOCKED dispositions for D001 and D095, counted once. Documentary preparation acceptance does not install registration, release execution or prove product. Publish a separate verdict as direct child of received handoff on refs/heads/review/trial-cac-nvidia-d001-d095-registration-preparation-20261128 at handoff/m02_completion_28_execution/INDEPENDENT_CAC_TRIAL_D001_D095_REGISTRATION_PREPARATION_VERDICT_20261128.md; verify commit/tree/readback, reconcile dispositions on trial and commission eligible distinct-role succession once under owner-adopted CAC MVP. On ACCEPT only separately commissioned Worker exact byte installation followed by independent installation clearance may proceed; on RETURN route bounded repair; on BLOCKED preserve holds. Preserve sole designated strict Tester and separate candidate-specific intake/precall release. No product execution or activation by reviewer, no main/original work edits or promotion.
