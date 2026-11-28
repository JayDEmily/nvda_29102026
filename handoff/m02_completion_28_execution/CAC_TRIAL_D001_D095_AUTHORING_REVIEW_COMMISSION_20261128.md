# D001/D095 first-stage authoring candidate and independent review commission

Status: two exact bindings installed; eleven admitted cases authored inert; independent authoring review required. No product or test execution, source implementation, active registration, case release, or acceptance.

Received trial checkpoint: 6ae23d4c9f5a80fa62de1b296ecfa99da0c3e957; tree df3743722d52a3fddd391bc096004bc08acb3368.
Prior separate binding acceptance: a29290c672420b3bf7b149c89828e5c8d43a9d9f, parent a090eaf255925ba1afd11a0928d1171118d5a447; report SHA256 ebff2ba39bbd9860995498e4660788ece24e61ebc3acd8198189266bb4c98952.
Both active YAML copies are byte-identical to accepted inactive originals, validated against the existing binding schema and exact own brief; M02 active, G01 framework, ordered modify targets M02 then G01.
Original immutable source policies, reviewed inventories, owner grant, path-only mapping and evidence ledger remain unchanged; ledger SHA256 5d1ac21a0cf62fe98efe5d4bd5c510094d139e6ae6bd3fc85d10924d67189c89.
Static documentary validation only: JSON schema, exact hashes, literal specimen digest, ordered admitted IDs/nodes/stages/oracles and AST inspection; no import, collection, execution or claim activation.

## D001 - SUP-D001-OPTION

Exact 4 cases; physical destination (not installed): tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py.
Prospective descriptor root (not created): config/product_proof/m02_option_time_d001.

- handoff/m02_completion_28_execution/L07a/D001_TEST_SOURCE.py SHA256 6bedaf2e25bc06c1c3a8f116f9f852fbaa0e94e4a916bdd80defee2519cbd867
- handoff/m02_completion_28_execution/L07a/D001_PROOF_CONTRACT.json SHA256 a18704f720dce0bd77a2c16f098846fe02b7e4027ec2715cdb7c0663b6e43ad5
- handoff/m02_completion_28_execution/L07a/D001_CLAIM_CANDIDATE.json SHA256 84d7116b41d01fe59877f7841c9e376cd2d517fe7bf7c010a4c33ad6fb014e81
- implementation/authority/T01_D001_OPTION_TIME_AUTHORITY_BINDING.yaml SHA256 ff80ea7dd3aa7674723b758dda9173356bda75119ba996ece5bf4c1a9ff2cf35

- SUP-D001-OPTION-SUCCESS: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_success
- SUP-D001-OPTION-REACHED_REFUSAL: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_date_only
- SUP-D001-OPTION-RECEIPT-ONLY: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_receipt_only
- SUP-D001-OPTION-OFFSET-MISMATCH: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py::test_d001_offset_mismatch

## D095 - M02-C28-D095

Exact 7 cases; physical destination (not installed): tests/product/m02_completion_28_prospective/d095/test_signal.py.
Prospective descriptor root (not created): config/product_proof/m02_option_iv_prior_session_d095.

- handoff/m02_completion_28_execution/L10a/D095_TEST_SOURCE.py SHA256 50173aa60e71fae8fe969e631f15b92eb8521ef174b845dcfcb2ab3ff0e7b6a8
- handoff/m02_completion_28_execution/L10a/D095_PROOF_CONTRACT.json SHA256 651c9cea0db295b16eafccfb3f8a9f042e7893cc3430b28ca29d9defcbb454aa
- handoff/m02_completion_28_execution/L10a/D095_CLAIM_CANDIDATE.json SHA256 0eb917d707fe6045d621319b397d9808968393a02cf62510c3a272d38f388bda
- implementation/authority/T01_D095_PRIOR_SESSION_IV_AUTHORITY_BINDING.yaml SHA256 2a4530490537b2552b320db240ac09eb24508ccc9d9347316e517463c4548f32

- D095-CONTROLLED-SUCCESS: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_success
- D095-CONTROLLED-REACHED_REFUSAL: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_session
- D095-CONTROLLED-LATE-REFERENCE: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_late_reference
- D095-CONTROLLED-WRONG-CONTRACT: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_contract
- D095-CONTROLLED-WRONG-MODEL: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_model
- D095-CONTROLLED-WRONG-UNITS: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_wrong_units
- D095-CONTROLLED-DUPLICATE-VINTAGE: tests/product/m02_completion_28_prospective/d095/test_signal.py::test_d095_duplicate_vintage

## Proposed public seam (naming and field choices for review, not implementation)

D001: OptionTimeSourceV1, OptionTimeRequestV1, OptionTimeOccurrenceV1; create_option_time_source(admission, specimen_id), create_option_time_owner(admission, source, storage, utc_now), create_option_time_reader(admission, storage). Request binds exact frame, profile, contract, definition and UTC clocks; occurrence binds exact CalculationDefinitionV1, policy digest, profile, ordered R002/R003 mapping and original/projection lineage, UTC result, effective/knowledge/first calculation clocks. Full public source corpus readback (all seven roles) does not change D001 dependency R002/R003. No legacy D001 codec change.
D095: OptionIVPriorSessionSourceV1, OptionIVPriorSessionRequestV1, OptionIVPriorSessionOccurrenceV1; create_option_iv_prior_session_source(admission, specimen_id), create_option_iv_prior_session_owner(admission, source, storage, utc_now), create_option_iv_prior_session_reader(admission, storage). Request binds exact profile/contract/calendar/definition and UTC clocks; occurrence binds exact CalculationDefinitionV1, policy digest, profile/calendar identity, full ordered visible originals/projections, selected current/reference IDs, prior trading date and configured close, exact ratio and first calculation clocks. No D001/D004 predecessor.
Both sealed source objects must internally admit actual literal facts through M00 public commands; then expose getter/direct projection/bounded history and identity only, not writer commands. No expected oracle or case label used by materialisation. Owner materialise(request) and owner.reads/get_derived_occurrence/list_derived_history plus ordinary SQLiteReadStorageV1 reopen are explicit. The inert tests specify exact field shapes/types and calls; reviewers must assess these before implementation, including immutable selected-corpus/role validators, durable decode/revalidation and independent oracle. Reader must not need a source producer. Negative cases reach actual target after confirming facts and check no target rows, including after reopen. Source label must never itself cause refusal.

## Next commission - fresh distinct independent documentary authoring reviewer

Fetch and require the exact published candidate HEAD; review against its parent 6ae23d4c9f5a80fa62de1b296ecfa99da0c3e957 and exact previous binding verdict. Verify the bounded delta, both installed bindings, proof contracts, prospective descriptors, actual authored source and public API naming/field choices. Review each case's admitted literal fixture, reached semantic invariant, independently derived result or refusal, complete native lineage, replay and ordinary durable reopen; check mapping, role, unit, clock, candidate roster, absence and selection invariants against pinned policies, not just Worker helper descriptions. Inspect the existing public M00 and M02 seams by source only; no imports or collection. Verify exact ordered 4 and 7 case sets, no substitution, duplicate, hidden test or change to old claims/ledger. Check scope and isolation. Separate ACCEPT_DOCUMENTARY_AUTHORING or bounded RETURN/BLOCKED dispositions for D001 and D095. Publish exact reviewed candidate/tree/delta/report on a separate review ref and reconcile the trial register per established pattern; only independently cleared jurisdiction(s) may advance to a fresh distinct implementation Worker. Serialise shared api.py/G01 edits; registration remains a separate clearance. Continue eligible distinct-role succession once via AGENTS.md CAC MVP. No new source implementation in reviewer, no product or test execution, no G01 R2 adoption, no release, no Tester appointment, no main merge or original-work edits. Preserve 64 held cases, ten L01a NOT_ATTEMPTED, 67 historical accepted, twelve mapping-only, D145 PAUSED; D003/D004/D086 and all dependent release predicates remain held. Sole designated strict Tester retains candidate-specific intake and precall release.

Checkpoint scope: exact trial commit/tree and reviewed delta; receiver must verify historical/evidence refs and applicable non-Git asset prerequisites under existing PINNED_REMOTE_CHECKPOINT. Existing historical asset/runtime holds are neither repaired nor waived by this documentary candidate. No independent receiver restoration or Tester qualification is claimed by Worker.

Worker checkpoint coverage: fetched all advertised heads and tags into a separate local audit ref namespace, verified exact received trial ref and independent binding review ref, and verified reachability of all 170 distinct historical tips across the retained 2,281 contextual rows / 797 literal pairs (including the original 66-name manifest) from those remote-fetched refs. All four retained ref/asset manifest byte identities match the received tree. This is remote-fetched object coverage, not a fresh independent recreation of every contextual literal name or external asset restore. The five older BLOCKED asset rows and one UNKNOWN historical runtime row remain intact.
