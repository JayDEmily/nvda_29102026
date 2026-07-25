# Semantic receipt — `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_emission_surface.py`

## File evidence

- Sequence `092`, unit `PM-014`; test SHA-256 `7f5c189cb84c4a7df5270aebd2dc2d967cb2b221c58716ec0ea348fbfd56974c`.
- Full reads: test `1-86`; complete harness `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py`; directly exercised DMP and observation contracts/store; workbook authority `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:26-34,75-86`; test-fixture identity/temporal law `docs/09.1_DMPV3_PROTOCOL_WORKING.md:25-37,41-79`; Parallel Risk observation ownership `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:163-170`.
- Raw test result: `2 passed in 0.20s`.

## G1 — `test_module_8_workbook_specimen_emits_packet_pair_and_observation_record`

- Test locator: `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_emission_surface.py:21-53`; assertions cover dataschemas, workbook derivation/source artefact lineage, packet IDs, append receipt, explicit manual-promotion marker, reserved stages and date-only source fields.
- Authority locator: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:26-34,75-86` and `docs/09.1_DMPV3_PROTOCOL_WORKING.md:25-79`.
- Authority match: a bounded test-owned workbook specimen may preserve provenance and source-time precision, but the workbook is not direct runtime authority and manual promotion is explicitly non-live.
- Behaviour proved: the harness emits a deterministic packet pair and in-process observation record with the asserted workbook lineage, date-only temporal fields and test marker.
- Limitation: cell truth/promotion authority, prepared identity completeness, persistent observation durability and live runtime equivalence are unproved.
- Adversarial challenge: map the wrong workbook cells or lose the observation on restart while retaining the asserted IDs/strings.
- Exact-surface falsifier: alter one asserted dataschema/lineage/packet ID/date field so an assertion at lines `24-53` fails.
- Assertion that must fail and why: at test lines `24-53`, returning the wrong specimen type, schema, lineage reference, packet ID list, append flag, manual-promotion flag, Stage B reservation token, source-time null or source date breaks a direct assertion. The test does not independently reconcile the cited workbook cells or prove that the in-memory append survives restart.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; retain as a deterministic non-live provenance specimen pending authoritative promotion and durable-state proof.

## G2 — `test_module_8_workbook_specimen_artifacts_are_written_under_bounded_home`

- Test locator: `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_emission_surface.py:56-86`; assertions verify five files and selected JSON/receipt contents.
- Authority locator: `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:13-26,75-82` and `docs/09.1_DMPV3_PROTOCOL_WORKING.md:37,69-79`.
- Authority match: deterministic test artefacts and truthful date-level provenance are legitimate shadow evidence; receipt phrases do not prove semantic correctness.
- Behaviour proved: the writer creates the asserted files under the supplied temporary directory and serialises the asserted specimen values/text.
- Limitation: file existence/text does not prove source-cell accuracy, replayability, fingerprint verification or isolation from all live paths.
- Adversarial challenge: write internally inconsistent artefacts with the expected phrases and selected values.
- Exact-surface falsifier: omit an asserted file or change one asserted JSON/receipt value so an assertion at lines `64-86` fails.
- Assertion that must fail and why: at test lines `64-86`, failing to create any of the five paths, changing the selected temporal/VIX/spot/lineage values, or removing any required receipt phrase breaks an existence, equality, absence or substring assertion. Internally inconsistent unasserted fields and incorrect cell interpretation can remain green.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; return to Tier A only with authoritative source reconciliation and executable replay/consistency proof.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `ADMIT_TIER_B_SHADOW`.
- Retain as a bounded workbook-derived, test-owned provenance specimen; it is not live runtime authority or durable persistence proof.
