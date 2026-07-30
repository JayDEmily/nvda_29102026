# M04 Authority Worker Record V1

## Assignment

| Field | Value |
|---|---|
| Worker | `Lane 2AW` |
| Tester | `Lane 2AT` |
| Unit | `M04-PROOF-MLC-A-V1` |
| Module | `M04 packet_protocol` |
| Contract | `K07 DmpV3Packet` |
| Leaf | `MLC-A — Authority sufficiency` |
| Result label | `PROPOSED_M04_AUTHORITY_V1_AWAITING_LANE_2AT` |

## Result

`BLOCKED_MISSING_NORMATIVE_AUTHORITY:For every governed DMPV3 packetrole, which execution-context identities (traceid, runid, scenarioid), lineage fields (parentids, dependencyids, derivedfrom, replayref, sourceartifactids, inputfingerprint, reviewtraceid, replaytraceid, decisiontraceid) and validation checks are mandatory, conditionally required, optional or not applicable, and what exact rejection, stand-down, non-admission or diagnostic/degraded outcome applies when each is absent?`

Current numbered authority is sufficient for the common M04 invariants listed below. It is not sufficient for the assignment's complete role-specific contract because it expressly defers the mandatory/optional/conditional/not-applicable lineage matrix and exact per-role validation checks. The missing matrix is material: the retained D-010 evidence records an actual conflict over whether a reference packet may lawfully omit caller-owned runtime context.

This is an authority result only. It does not route or observe tests, specify proof, mutate normative meaning, or open implementation.

## Accepted owner, surface and contract

| Item | Accepted meaning | Locators |
|---|---|---|
| Architecture surface | `5.6 DMPV3 packet carriage`; structural status `Locked`; implementation truth `thin_seam`; deliberate inter-module carriage only | `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-234`; `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:50`; workbook `Surface Map!A7:O7`; JSON selector `.surfaces[] | select(.surface_id=="5.6")` |
| Owner module | `M04 packet_protocol`; no runtime prerequisite; no owned state | `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:150-173,184-202`; `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md:125-145,200-209`; workbook `Target Modules!A6:Q6`; JSON selector `.modules[] | select(.module_id=="M04")` |
| Owned authority | DMPV3 outer-envelope validation and deliberate packet carriage | `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:160`; workbook `Target Modules!E6`; JSON `.modules[] | select(.module_id=="M04") | .owns` |
| Prohibited authority | Raw-ingress carriage, domain decisions, identity fabrication, time fabrication, payload ownership and persistence truth by implication | `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-234`; `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:160`; `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md:133,206-207` |
| Public contract | `K07 DmpV3Packet`: one common outer envelope; role-specific IDs are supplied, not fabricated | workbook `Contracts!A8:E8`; JSON selector `.contracts[] | select(.contract_id=="K07")` |
| Historical obligations | `C-010 → D-010` and `C-016 → D-016` remain traceability obligations, not present implementation authority | `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv:11,17`; `GATE_C2_PROOF_ENVELOPE_REGISTER.tsv:8,11`; `gate_c2_proof_envelopes/D-010.md:1-71`; `gate_c2_proof_envelopes/D-016.md:1-71` |

## Exact numbered authority propositions

### Common envelope and boundary

1. Every live packetised inter-module output uses one canonical DMPV3 outer envelope; the envelope normalises carriage without merging responsibility or meaning (`docs/01_NORMATIVE_CORE.md:81-85`; `docs/04_TECHNICAL_ARCHITECTURE_CORE.md:24-50`; `docs/09_DMPV3_PROTOCOL_CORE.md:19-29`).
2. The canonical shell carries the complete outer field set, including packet role, producer, lineage, validation, summary, typed data and bounded extensions (`docs/09_DMPV3_PROTOCOL_CORE.md:31-58`).
3. DMPV3 begins at deliberate live inter-module boundaries. It is not the universal raw-source, prepared-data or internal-stage carrier and does not replace typed domain contracts (`docs/03.1_DOMAIN_MODEL_WORKING.md:77-87`; `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:74-84`; `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-234`).
4. Readers use `packetrole`, `producer.grammar_role`, `producer.behaviour_class` and `dataschema`; payload shape alone does not establish carriage meaning (`docs/09_DMPV3_PROTOCOL_CORE.md:78-93`; `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:17-41`).

### Identity, lineage and time

5. M04 may create packet-occurrence identity and emission metadata only inside packet-carriage authority. It may not create source, domain, decision, state, policy, receipt, trace, run or scenario authority (`docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:74-84`; `docs/09.1_DMPV3_PROTOCOL_WORKING.md:11-23`).
6. `source + id` identifies a packet occurrence. It does not become an upstream source artefact, domain object, decision, position, execution, state, receipt or preserved-original identity (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:13-23`).
7. `traceid`, `runid` and `scenarioid` are distinct execution-context identities supplied by their owning boundary. A packet builder propagates them and must not derive trace/run from packet ID or silently default a generic scenario such as `live` (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:25-39`).
8. Lineage fields have separate declared meanings; immediate parents, material dependencies, principal domain derivation, replay reference, source artefacts, semantic input fingerprint and review/replay/decision traces are not interchangeable (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:41-59`).
9. Packet `time` is packet emission time, not source observation time. Source temporal truth remains separately carried at its lawful precision (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:63-79`; `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:43-72`).
10. A packet or execution-context identifier must not substitute for an absent source, capture, domain, decision, position, execution or state identifier (`docs/03.1_DOMAIN_MODEL_WORKING.md:41-55`; `docs/05.1_GUARDRAILS_WORKING.md:33-44`).

### Validation, reproduction and side effects

11. Validation records only the checks actually performed for the exact packet role and boundary. A mandatory structural, identity, lineage, semantic or authority failure rejects governed emission, stands down, remains non-admitted, or uses a separately admitted diagnostic/rejection contract (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:81-91`).
12. `degraded` is lawful only when the role contract permits limited non-binding carriage and names the limitation. Model construction, default `schema_validation=true` or an empty violation list is not proof of validity (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:83-91`).
13. The summary is a deterministic human-facing projection and cannot create or override domain authority; extensions cannot hide mandatory fields, lineage or authority (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:93-119`).
14. Preserved-occurrence replay keeps the original envelope unchanged. Newly emitted replay output is a new occurrence. Domain-result equivalence uses the semantic result and material-version fingerprint, excluding regenerated packet identity/time and current wall-clock metadata (`docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:113-127`; `docs/09.1_DMPV3_PROTOCOL_WORKING.md:121-129`; `project_control/normative_authority_top_down_alignment/normative_completion_decisions/N-09_AUTHORITATIVE_REPLAY.md:21-44`).
15. M04 owns no domain state and no persistence side effect. Its bounded side effect is creation/emission of the validated packet occurrence; payload meaning, domain state and authoritative evidence remain with their owners (`docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:17-41`; `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:20-49`; accepted M04 architecture rows cited above).

## Input → validation/carriage → output

| Phase | Governed facts |
|---|---|
| Input | One strongly typed, module-owned payload contract; packet role; producer identity; packet source context; caller/owner-supplied execution context; owner-supplied source/domain/decision/state/dependency identities; exact material lineage; role-specific validation evidence; explicit packet emission metadata or an authorised packet-occurrence metadata source. |
| Validation and carriage | Validate the canonical shell, `source + id` occurrence identity, producer/role/schema declarations, exact role-required execution context, typed payload, lineage semantics, validation status and extension limits. Reject or withhold when a mandatory owner fact is absent. Do not carry pre-DMP raw/prepared inputs as though DMP were their native storage or input grammar. |
| Output | One DMPV3 packet occurrence with canonical envelope and typed payload. The packet carries the producing domain's result; it does not become that result's semantic owner. Domain reproduction compares governed semantic content/fingerprint, not current emission metadata. |

## Identity, lineage, time, state and side effects

| Concern | Owner and rule | M04 limit |
|---|---|---|
| Packet occurrence `source + id` | Packet-carriage authority creates or validates the occurrence identity within its declared source context | Must not reuse it as source/domain/state truth |
| Producer identity | Emitting module truth: module, version, instance, grammar role, behaviour class and narrower stage where one exists | Must not infer it from payload shape |
| `traceid`, `runid`, `scenarioid` | Boundary owning the execution, replay or scenario context | Propagate/validate only; no derivation or generic defaults |
| `parentids` / `dependencyids` | Producing domain and dependency owners identify actually consumed upstream material | Preserve exact causal versus non-parent dependency meaning |
| `derivedfrom` | Owner of the principal upstream domain output | No concatenated plural or invented substitute |
| `sourceartifactids` / `inputfingerprint` | Source/capture/preparation owners | Preserve declared evidence and semantic fingerprint; a hash alone is not retrievable evidence |
| Replay/review/decision trace IDs | Respective replay, review and decision owners | Carry only where their role contract requires them |
| `time` | Packet emission metadata | Never source observation time or deterministic domain-result authority |
| State | None owned by M04 | Packet carriage does not create persistence truth |
| Side effects | Bounded packet creation/emission | No domain decision, source admission, capital, execution, inventory, close, review or persistence mutation |

## N-package and C/D evidence reconciliation

| Evidence | Contribution to M04 | Limit |
|---|---|---|
| `N-03` | Defines mandatory prepared identity, source/capture references, versions, temporal facts, fingerprints, validation/completeness and source artefact lineage (`N-03...md:21-43`; `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:17-89`) | Does not allocate those facts into each DMP packet role |
| `N-05` | Defines immutable common context, narrow stage carriers, reference consistency and deterministic reconstruction inputs (`N-05...md:21-43`; `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:150-217`) | Does not define the K07 per-role mandatory lineage/validation profile |
| `N-09` | Defines preserved occurrence versus semantic re-execution, complete authoritative envelope, isolated/no-side-effect replay and emission-metadata exclusion (`N-09...md:21-44`; `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:145-217`) | Does not decide which K07 lineage fields are mandatory for each packet role |
| `C-010 / D-010` | Requires role-specific IDs, source artefact lineage, deterministic reproduction and pre-DMP separation (`B02_TEST_DESIGN.md:53-73`; `D-010.md:1-71`) | D-010 is closed because a reference-packet test permits missing runtime context while the proposed Gate C test rejects it; the exact exception boundary is unresolved |
| `C-016 / D-016` | Requires source artefact IDs, supplied context IDs, dependency semantics and domain output independent of emission time (`B04_TEST_DESIGN.md:53-73`; `D-016.md:1-71`) | D-016 remains dependent on D-010 and prepared-lineage proof; its historical readiness text does not supply missing normative meaning |

## Contradictions and missing meaning

### M04-AUTH-GAP-001 — role-specific identity and lineage matrix absent

`docs/09.1_DMPV3_PROTOCOL_WORKING.md:61` says every packet role must eventually declare its mandatory, optional, conditionally required and not-applicable lineage subset, and assigns that work to Gate B. `docs/09.1_DMPV3_PROTOCOL_WORKING.md:161` prohibits inference of those checks from defaults. `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:66-80` likewise leaves the exact per-boundary mandatory replay subset to the semantic walk.

This is missing normative meaning, not an implementation detail. Without the role matrix, M04 cannot determine whether an absent field is lawful absence, degradation, diagnostic carriage or a fail-closed error.

### M04-AUTH-GAP-002 — exact validation profile absent

`docs/09.1_DMPV3_PROTOCOL_WORKING.md:83-91` requires the producer to know the checks required for the exact role. No current numbered proposition enumerates those checks for all governed packet roles.

### M04-EVIDENCE-CONFLICT-001 — reference packet exception

`project_control/normative_authority_top_down_alignment/gate_c_test_design/B02_TEST_DESIGN.md:53-73` labels C-010 ready/admitted, but the later D-010 record closes proof authority because `test_reference_packet_builder_emits_canonical_shell_and_degraded_validation_without_runtime_context` permits trace/run defaulting while the proposed C-010 test rejects missing caller-owned context (`GATE_C2_BLOCKED_OR_RETURNED_UNITS.tsv:3`; `gate_c2_proof_envelopes/D-010.md:65-71`).

The current module-local protocol makes those historical statuses evidence rather than present scheduling authority. The conflict still demonstrates why the missing role-specific exception boundary cannot be guessed from old tests.

## Exact normative return question

The routed DMPV3 authority must add one role-by-role matrix covering every governed `packetrole`, including at minimum prepared-context, serial-stage, parallel-risk, financial-calendar/reference, review/explanation, replay and separately admitted diagnostic/rejection roles. For each role it must state:

1. required/conditional/optional/not-applicable execution-context and lineage fields;
2. field owner and lawful generation/propagation rule;
3. exact structural, identity, lineage, semantic and authority checks;
4. lawful absence outcome: reject, stand down, remain non-admitted, or expressly diagnostic/degraded carriage;
5. whether any role may omit caller-owned `traceid`, `runid` or `scenarioid`, and why;
6. the typed payload and source-artifact/replay evidence required for deterministic domain reproduction.

Until that numbered authority exists, `M04-PROOF-MLC-A-V1` is blocked at `MLC-A`.
