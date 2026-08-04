# Protocols, Packet Carriage and Stage Identity

## Authority propositions

`P-PROTO-001`, `P-PROTO-002`, `P-PROTO-003`, `P-PROTO-005`, `P-PROTO-006`, `P-ARCH-003`.

Exact lineage is retained in [`../propositions/A05.md`](../propositions/A05.md), [`../propositions/A07.md`](../propositions/A07.md), [`../propositions/A13.md`](../propositions/A13.md), [`../propositions/B04.md`](../propositions/B04.md), [`../propositions/B09.md`](../propositions/B09.md) and [`../propositions/B10.md`](../propositions/B10.md).

## 1. Stable typed stage carriage

Widened temporal and playbook inputs remain inside a stable typed stage-carriage contract around `TemporalContextOutput`. Posture, execution and review consume typed stage outputs rather than raw broker data. A protocol evolution may change the outer packet version, but it cannot silently rename a stage's payload identity or move business ownership into the envelope.

## 2. Protocol authority chain

The historical authority chain is:

1. DMP v1 was temporarily the live producer for a bounded workflow-modification tranche, with v2 secondary.
2. DMP v2 then explicitly replaced v1 as the sole live producer; v1 became archived history only.
3. DMPV3 later explicitly replaced DMP v2 at one named boundary: the serial runtime's downstream packet-carriage product.

The third step is partial supersession, not a claim that every internal carrier is DMPV3. Raw ingress, raw-to-prepared transfer, prepared-to-cognition transfer and serial stage-to-stage flow remain native typed carriers.

## 3. DMPV3 boundary

The first deliberate DMPV3 boundary is downstream of the serial runtime. The serial runtime emits one canonical bounded set of admitted packets. That set is operational handoff authority, not merely an after-the-fact trace dump.

A stage packet may be emitted only from an already-lawful typed stage output that owns the fields. Packet completeness is subordinate to truthful ownership. Where packetisation would require invented fields, an interim convenience contract, widened parallel-risk stages or expanded downstream consumers, the packet remains conditional or reserved.

DMPV3 packetisation preserves:

- serial order and declared dependencies;
- producer identity;
- explicit stage/packet role and behaviour-class interpretation;
- trace, run and scenario identity;
- lineage;
- validation state;
- a human-readable summary;
- bounded extension data.

## 4. One envelope and one builder path

Live DMPV3 carriage uses one canonical outer-envelope grammar and one deterministic repository-owned builder path. The envelope owns transport grammar, not stage business meaning.

A compatibility wrapper may survive only when necessary, must be labelled as compatibility and must delegate to the canonical builder. It cannot establish a competing packet truth.

The complete mandatory field schema, detailed field validation rules and permitted `dmpextensions` contents are referenced by the successor corpus but not fully restated. They remain unresolved external protocol detail.

## 5. Review stage versus packet-emitting stages

The review-stage sequence includes the terminal final-risk join. Stage-packet identifiers, however, represent only packet-emitting runtime stages plus review. These are intentionally different views. A review stage appearing in the explanatory sequence does not imply that every preserved intermediate surface emits a protocol packet.
