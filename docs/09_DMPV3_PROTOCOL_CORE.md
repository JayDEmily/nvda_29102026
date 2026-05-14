# 09_DMPV3_PROTOCOL_CORE

All repo paths in the numbered control stack are repo-root-relative.


## Scope of this document

This document owns:

- the canonical DMPV3 outer envelope
- packet-carriage field law
- producer identity law
- packet role and behaviour-class law
- lineage law
- validation and summary carriage law
- bounded DMP extension law
- the rule that all live packetised outputs use the canonical DMPV3 outer shell

## Core rule

The repo uses one canonical DMPV3 outer envelope for live inter-module packet carriage.

That outer envelope normalises carriage.

It does not merge module responsibility, runtime ownership, or downstream meaning.

If a runtime output is packetised, it must use the canonical DMPV3 shell.

A live module does not keep an alternative outer packet grammar.

## Canonical outer envelope

The live DMPV3 outer envelope is the `DmpV3Envelope` surface in `src/nvda_desk/contracts/packets.py`.

A live DMPV3 packet must carry these outer-envelope fields:

- `specversion`
- `dmpversion`
- `id`
- `source`
- `type`
- `time`
- `datacontenttype`
- `dataschema`
- `traceid`
- `runid`
- `scenarioid`
- `packetrole`
- `producer`
- `lineage`
- `validation`
- `summary`
- `data`
- `dmpextensions`

The repo-facing typed packet helper surface is `src/nvda_desk/contracts/packets.py` via `DmpV3Packet` and `DeskModulePacketV3`.

Compatibility wrappers under `src/nvda_desk/schemas/dmp_envelope.py` and `src/nvda_desk/schemas/dmp.py` do not own the live truth.

## Producer identity law

Every live DMPV3 packet must declare a bounded producer identity.

The producer surface must carry:

- `module_id`
- `module_version`
- `module_instance_id`
- `grammar_role`
- `behaviour_class`

`stage_name` must be omitted only when no narrower stage label exists.

Producer identity must describe the emitting module truthfully.

Producer identity must not be backfilled from payload shape alone.

## Packet role and behaviour-class law

Packet interpretation must use the declared outer carriage surfaces.

A packet reader must use:

- `packetrole`
- `producer.grammar_role`
- `producer.behaviour_class`
- `dataschema`

A packet reader must not infer carriage meaning from payload structure alone.

A shared outer envelope does not make two packetised outputs interchangeable.

Runtime ownership remains governed by `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`.

## Lineage law

Every live DMPV3 packet must carry bounded lineage.

Where relevant, lineage must state:

- `parentids`
- `dependencyids`
- `derivedfrom`
- `replayref`
- `sourceartifactids`
- `inputfingerprint`
- `reviewtraceid`
- `replaytraceid`
- `decisiontraceid`

If an emitted packet depends on upstream packets, those upstream packet identities must be declared in lineage rather than left implicit.

If a packet is derived from authoritative source artefacts, those artefact identities must be declared in lineage.

## Validation law

Every live DMPV3 packet must carry a validation record.

A packet with no declared violations is `valid`.

A packet with declared carriage violations is `degraded`.

Validation carriage must not be omitted merely because the payload model validated.

## Summary law

Every live DMPV3 packet must carry a human-facing summary.

The summary must include:

- `headline`
- `keyflags`
- `humanstate`

The summary must describe the emitted packet truthfully.

The summary is an aid for inspection.

It does not replace the payload contract.

## Extension law

`dmpextensions` carries bounded compatibility metadata only.

`dmpextensions` must not be used to replace or weaken the canonical outer-envelope fields.

The repo-owned `nvda` extension block is reserved for bounded compatibility metadata including:

- execution context
- schema identifiers
- semantic dependency annotations

A custom extension must merge without erasing the canonical repo-owned `nvda` compatibility leaves.

## Canonical builder law

Live packet builders must emit the canonical shell through the repo-owned builders:

- `src/nvda_desk/contracts/packets.py`
- `src/nvda_desk/packets/dmp_packets.py`
- explicit compatibility wrappers only where needed, such as `src/nvda_desk/schemas/dmp_envelope.py` and `src/nvda_desk/schemas/dmp.py`

A module-specific packet-specialised wrapper is lawful for a module's own dataschema and module identity.

It still emits the canonical DMPV3 shell.

## Emitter coverage law

The canonical DMPV3 shell applies to live packetised outputs including:

- serial stage packets
- imported-module packets
- financial-calendar reference packets
- the independent parallel risk lane packet
- review packet carriage where runtime outputs are packetised

A module that emits a live packetised output does not keep or reintroduce an alternative outer protocol.

## Native Architecture Blueprint boundary

Within native code-structure architecture scope, this document must be read with `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

`docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` owns target package placement, component form, seams, ownership, persistence, test-family mapping, reservations, module allocation, and traceability for native code-structure architecture.

It does not override the authority hierarchy defined by `docs/01_NORMATIVE_CORE.md`.

All durable terms used by live control documents must be governed by `docs/vocabulary/vocabulary_registry.md` or lawfully admitted by the vocabulary process before they become canonical language.
