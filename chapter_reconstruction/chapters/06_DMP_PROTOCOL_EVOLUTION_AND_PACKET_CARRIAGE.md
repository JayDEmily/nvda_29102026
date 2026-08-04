# Chapter 6 — DMP Protocol Evolution and Packet Carriage

## Chapter role

This chapter traces the protocol authority chain without turning “later” into “global replacement”. It identifies which carrier is authoritative at each boundary, when DMPV3 actually begins, what a stage may lawfully packetise, and why packet transport cannot absorb stage meaning.

**Primary propositions:** `P-PROTO-001`, `P-PROTO-002`, `P-PROTO-003`, `P-PROTO-005`, `P-PROTO-006`, `P-ARCH-003`.

## 1. Original intention: stable typed stage carriage

The first protocol rule wraps widened temporal and playbook inputs in a stable typed DMP stage carrier around `TemporalContextOutput`. Posture, execution and review consume typed stage outputs rather than raw broker data. A wrapper may evolve, but it cannot silently rename the payload identity or move stage ownership into transport. (`P-PROTO-001`)

This rule survives every later version change. Protocol versions determine how information is carried; they do not authorise raw-broker bypass, opaque mappings or a new owner for temporal, posture, eligibility, execution or risk meaning.

## 2. DMP v1 becomes temporary and is then explicitly retired from live production

The version history is not a simple “v1 then v2” assumption. It contains an explicit bounded reversal and replacement chain. (`P-PROTO-002`)

1. Gate 54 temporarily fixed DMP v1 as the live producer for one workflow-modification tranche, with v2 secondary for migration or inspection.
2. That authority was expressly tranche-bounded.
3. Gate 57 then promoted DMP v2 across live runtime and imported-module emissions and ended v1 canonical-producer status.
4. Gate 58 removed mixed mode: DMP v1 became archived historical context only, and DMP v2 became the sole live packet protocol.

The Gate-54 v1-live state is therefore superseded. DMP v1 may remain in historical evidence, but it cannot be a live producer dependency or a compatibility path that secretly emits live packets.

DMP v2 remains partially authoritative. It is later replaced only at the exact downstream boundary named by DMPV3 authority. The v1 retirement and the unaffected v2 governance rules survive.

## 3. DMPV3 begins only after the serial runtime

The successor boundary alignment explicitly promotes DMPV3 at one named seam: the serial runtime's downstream packet-carriage product. (`P-PROTO-003`)

The following remain native typed carriers:

- raw ingress;
- raw-to-prepared transfer;
- prepared-to-cognition ingress;
- serial stage-to-stage flow.

The first deliberate DMPV3 product is emitted after the serial runtime. The runtime emits one canonical bounded set of admitted packets for downstream carriage, including the parallel-risk handoff. That packet set is operational handoff authority, not merely an after-the-fact trace dump.

This is partial supersession. It is incorrect to read the later protocol name as authority to wrap every internal seam in DMPV3. Earlier packetisation would move protocol concerns into raw, preparation or serial-stage ownership and would contradict the named boundary.

DMPV3's temporal rule is likewise bounded: `packet.time` represents emission time, while source observation remains separately governed by the source-time grammar in Chapter 3. Packet carriage may not manufacture source precision.

## 4. Packet completeness is subordinate to truthful stage ownership

A serial stage may emit a DMPV3 packet only when its lawful typed output already exists and owns every emitted field. Packetisation preserves: (`P-PROTO-005`)

- serial stage order;
- declared dependencies;
- trace identity;
- run identity;
- scenario identity;
- lineage.

A desire for a visually complete packet set is not authority to invent stage outputs. If an emitter would require fabricated fields, a temporary convenience contract, widened parallel-risk Stage B/C logic, or expanded final-risk, capital or downstream consumers, the emitter remains conditional or reserved.

The lawful outputs are therefore:

- a truthful packet built from an admitted stage output; or
- an explicit reservation explaining why the emitter does not yet exist.

There is no third option in which a nominal packet is populated with borrowed or speculative meaning.

## 5. One canonical outer envelope and one builder path

The current DMPV3 carriage model has one canonical outer-envelope grammar and one deterministic repository-owned builder path. (`P-PROTO-006`)

The shell carries, within the admitted bounded design:

- truthful producer identity;
- explicit packet role;
- behaviour-class interpretation;
- bounded lineage;
- validation state;
- a human-facing summary;
- bounded extension data.

The envelope owns transport grammar. It does not own the business meaning of a temporal state, playbook decision, risk result or capital value. Those meanings remain with the stage or authority that produced them.

A compatibility wrapper may survive when necessary, but it must be labelled as compatibility and delegate to the canonical builder. It cannot create a competing envelope grammar or a second builder truth. Deterministic inputs must produce stable builder output, subject to explicitly time-varying emission metadata.

The successor corpus references, but does not fully restate, the complete mandatory field schema, detailed validation rules and permitted `dmpextensions` content. Those protocol details remain unresolved external authority.

## 6. Review stages and packet-emitting stages are different views

The review-stage sequence includes the terminal `final_risk_join` before review. Stage packet identifiers, however, cover only runtime stages that actually emit packets plus review. The two ordered lists are intentionally not identical. (`P-ARCH-003`)

A stage may appear in the explanatory decision chain without owning a packet emitter. Conversely, a packet identifier cannot be invented merely to make the review sequence and packet sequence have equal length. Expectations must follow actual governed emitters.

This resolves an apparent counting temptation in the broader design. Chapter 4 states six serial cognitive stages. The terminal final-risk join occurs downstream of those stages. Review then explains the chain. Packet-emitting stages are a separate subset. The design does not flatten those distinctions into one overloaded stage count.

## 7. Current authoritative position

The lawful protocol chain is:

1. typed stage carriage preserves payload identity and stage ownership;
2. DMP v1 is historical only;
3. DMP v2 remains live outside the exact boundary later replaced;
4. DMPV3 begins at the serial runtime's downstream packet-carriage product;
5. upstream raw, preparation, cognition and serial-internal carriers remain native typed contracts;
6. a stage packet is emitted only from lawful stage-owned output;
7. missing emitters remain conditional or reserved rather than fabricated;
8. live DMPV3 uses one canonical envelope and builder;
9. packet transport never owns stage business meaning;
10. review-stage order and packet-emitter order remain distinct.

## 8. Unresolved matters

The admitted corpus does not fully specify:

- the unaffected DMP v2 schema details;
- the complete canonical DMPV3 emitted packet set;
- the mandatory DMPV3 field schema and validation rules;
- permitted `dmpextensions` contents;
- which optional stage emitters will become lawful after their typed outputs exist;
- the complete packet-emitter list.

These gaps do not authorise early packetisation, competing envelope grammars or invented stage fields.

## Cross-references

- Temporal-state identity and packet emission time: [Chapter 3](03_TEMPORAL_TRUTH_CALENDARS_AND_PROVENANCE.md).
- Six-stage serial ownership: [Chapter 4](04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md).
- Playbook and modifier payload meaning: [Chapter 5](05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md).
- Parallel-risk packet ingress and Stage A: [Chapter 7](07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md).
- Packet-linked persistence: [Chapter 8](08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md).
- Review and workbook packet specimens: [Chapter 9](09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md).
- Compatibility survival and public projection: [Chapter 10](10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md).
