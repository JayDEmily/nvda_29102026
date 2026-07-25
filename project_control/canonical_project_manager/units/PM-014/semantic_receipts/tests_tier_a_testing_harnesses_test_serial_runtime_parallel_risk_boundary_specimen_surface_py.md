# Semantic receipt — `tests/tier_a/testing_harnesses/test_serial_runtime_parallel_risk_boundary_specimen_surface.py`

## File evidence

- Sequence `094`, unit `PM-014`; test SHA-256 `f67b69999aace0eb663cb0c1793a5e64ec024f9a4aaa60972d110d8260a7ca60`.
- Full reads: test `1-92`; complete harness `src/nvda_desk/testing/harnesses/serial_runtime_parallel_risk_boundary_specimen.py`; bounded Parallel Risk ownership `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:163-170`; DMP identity and lineage law `docs/09.1_DMPV3_PROTOCOL_WORKING.md:13-61`; native serial/DMP/Parallel Risk seams `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-269`.
- Raw test result: `2 passed in 0.21s`.

## G1 — `test_serial_runtime_parallel_risk_boundary_specimen_emits_admitted_boundary_path`

- Test locator: `tests/tier_a/testing_harnesses/test_serial_runtime_parallel_risk_boundary_specimen_surface.py:18-42`; assertions cover the six serial stage keys, temporal-only selection, bootstrap parent/dependency identity, bootstrap source and lane parent/dependency identity.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:163-170`, `docs/09.1_DMPV3_PROTOCOL_WORKING.md:27-61`, and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:237-269`.
- Authority match: the asserted temporal-only serial packet selection and immediate packet parent/dependency chain are lawful bounded clauses at the serial-to-Parallel-Risk seam.
- Behaviour proved: the specimen currently routes the temporal serial packet into a bootstrap packet and then into the Parallel Risk lane packet with the asserted immediate lineage.
- Limitation: the test does not prove complete `ParallelRiskInputTrace`, rejection of non-admitted inputs, non-consumption of hidden state, validation status, observation durability, or lawful ownership of trace/run/scenario identities created by the harness path.
- Adversarial challenge: retain the asserted packet IDs and parent/dependency lists while silently reading capital or broker state, omitting a material dependency from the input trace, or inventing live execution identities.
- Exact-surface falsifier: select a non-temporal stage, change `bootstrap_source`, or break either asserted parent/dependency edge; an assertion at lines `22-42` must fail.
- Assertion that must fail and why: at test lines `22-42`, changing the six stage-key order, selecting anything other than the temporal packet, breaking either bootstrap parent/dependency edge, changing the exact bootstrap-source label, or breaking either lane-to-bootstrap edge fails a direct assertion. Hidden reads and omitted dependencies outside those lists remain unobserved.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; retain the nominal lineage seam in shadow until complete input-trace, hidden-read rejection and execution-identity ownership are proved.

## G2 — `test_serial_runtime_parallel_risk_boundary_specimen_artifacts_are_written_under_bounded_home`

- Test locator: `tests/tier_a/testing_harnesses/test_serial_runtime_parallel_risk_boundary_specimen_surface.py:45-92`; assertions cover six file existences, selected serial/lineage values and finite absence of four legacy seam phrases.
- Authority locator: `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:13-26,75-82`, `docs/09.1_DMPV3_PROTOCOL_WORKING.md:41-61`, and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-269`.
- Authority match: deterministic bounded artefacts can preserve specimen evidence, but file existence and selected-string absence are not proof of complete authority isolation or executable replay.
- Behaviour proved: the writer creates the six asserted artefacts under the supplied directory and serialises the asserted stage order, temporal selection and immediate lineage values without the named legacy phrases.
- Limitation: content consistency across all artefacts, input-trace completeness, durability, replay equivalence, indirect/aliased forbidden seams and hidden side effects are unproved.
- Adversarial challenge: write semantically inconsistent artefacts that retain the asserted fields and avoid the finite forbidden strings.
- Exact-surface falsifier: omit one asserted file, alter one asserted stage/lineage value, or insert one exact forbidden phrase into the receipt; the corresponding assertion at lines `50-92` must fail.
- Assertion that must fail and why: at test lines `50-92`, omitting any written artefact, changing the asserted stage order/selection or immediate lineage values, placing the legacy workbook name in the path/receipt, or inserting any exact forbidden seam phrase breaks an existence, equality or absence assertion. Cross-file inconsistency and aliased authority can still pass.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; return to Tier A only with executable cross-artefact consistency, complete trace and forbidden-authority behaviour checks.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `ADMIT_TIER_B_SHADOW`.
- Preserve the nominal serial-to-Parallel-Risk specimen as shadow evidence; it does not prove complete boundary authority.
