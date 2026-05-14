# 07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE

All repo paths in the numbered control stack are repo-root-relative.


## Core rule

Each runtime output must have:

- one bounded owner
- one bounded meaning

If two runtime outputs answer different questions, they remain separate.

A later step in the system does not treat two different outputs as interchangeable merely because one is easier to read or easier to carry forward.

## Packet-carriage rule

When a runtime output is carried in a DMPV3 packet, the common outer envelope does not change ownership of the carried output.

A later step in the system still interprets the carried output according to its bounded owner and bounded meaning.

A later step in the system uses the declared packet contract and packet role.

It does not infer ownership or meaning from payload shape alone.

A common outer envelope is not used as a reason to treat:

- runtime preparation output
- financial-calendar reference output
- serial desk-cognition output
- serial stage outputs inside the desk-cognition spine
- the independent parallel risk lane
- the downstream pre-deployment gate
- capital deployment authority
- downstream opening-architecture outputs
- downstream live-inventory architecture outputs
- downstream state-reader outputs
- review-layer outputs

as interchangeable.

## Runtime outputs that must stay separate

The runtime preserves separate outputs for:

- runtime preparation
- financial-calendar reference and projection
- the serial desk-cognition spine
- serial stage outputs inside the desk-cognition spine
- the independent parallel risk lane
- the downstream pre-deployment gate
- capital deployment authority
- downstream opening-architecture outputs
- downstream live-inventory architecture outputs
- downstream state-reader outputs
- review-layer outputs that state what those parts concluded

Those outputs are related in runtime.

They do not collapse into one blended answer.

## Runtime-preparation output

The runtime-preparation path owns the output that admits source truth and prepares runtime-ready truth.

That output answers the question:

- what runtime-ready truth was admitted and prepared for later governed steps

A later step in the system does not treat that output as candidate formation, the independent parallel risk reading, or capital deployment authority.

## Financial-calendar reference output

The financial-calendar reference and projection path owns the output that preserves calendar truth and projected calendar context.

That output answers the question:

- what financial-calendar truth and projected calendar context were preserved for later governed steps

A later step in the system does not treat that output as candidate formation, the independent parallel risk reading, or capital deployment authority.

## Serial desk-cognition output

The serial desk-cognition spine owns the output that forms the candidate.

That output answers the question:

- what candidate did the serial desk-cognition spine form

A later step in the system does not treat that output as if it came from the independent parallel risk lane or from capital deployment authority.

## Serial stage outputs inside the desk-cognition spine

Where serial stage outputs exist inside the desk-cognition spine, including posture-and-risk permission outputs, those outputs remain serial-path outputs.

Those outputs answer bounded stage questions inside the serial desk-cognition path.

They do not answer the same question as:

- the independent parallel risk lane
- capital deployment authority

A later step in the system does not treat a serial stage output as if it were the independent environmental assessment or the fresh-capital decision.

## Independent parallel risk output

The independent parallel risk lane owns the output that assesses the present environment in parallel with the serial desk-cognition spine.

That output answers the question:

- what did the independent parallel risk lane conclude about the present environment

It does not answer the question:

- what candidate was formed

A later step in the system does not treat the independent parallel risk output as candidate formation.

## Downstream pre-deployment output

The downstream pre-deployment gate owns the output that blocks or allows incomplete, disallowed, or unusable candidate material before capital deployment authority acts.

That output answers the question:

- what candidate material was blocked or allowed before fresh-capital deployment judgement

It does not answer the question:

- what candidate was formed
- what the independent parallel risk lane concluded about the environment
- what fresh-capital decision was made against the candidate

A later step in the system does not treat the downstream pre-deployment output as candidate formation, environmental assessment, or capital deployment authority.

## Capital deployment output

Capital deployment authority owns the output that decides whether fresh capital is deployed against the formed candidate, and in what bounded way.

That output answers the question:

- what fresh-capital decision was made against the candidate

It does not answer the question:

- what candidate was formed
- what the independent parallel risk lane concluded about the environment
- what candidate material was blocked or allowed before the fresh-capital decision

A later step in the system does not treat the capital deployment output as candidate formation or as the environmental assessment.

## Downstream opening-architecture outputs

The downstream opening architecture owns shell outputs. Those shell outputs answer these questions and no others:

- what post-serial opening homes exist
- what those homes read from preserved seam truth and repo-native state
- what remains deferred because behavioural policy is not yet installed

Those outputs do not replace:

- serial candidate formation
- the independent parallel risk lane
- the downstream pre-deployment gate
- capital deployment authority

A later step in the system does not treat an opening-architecture receipt as if it were the fresh-capital decision itself.

## Downstream live-inventory architecture outputs

The downstream live-inventory architecture owns shell outputs. Those shell outputs answer these questions and no others:

- what live-position monitoring, management, rotation, exit, and close homes exist
- which repo-native inventory and receipt readers those homes are permitted to consume
- which behavioural rules remain deferred

Those outputs do not answer the question:

- what fresh-capital decision was made against the opening candidate

A later step in the system does not treat live-inventory architecture receipts as if they were opening-authority outputs.

## Downstream repo-native state reader outputs

The downstream state-reader layer owns explicit outputs. Those outputs answer these questions and no others:

- which repo-native capital, position, and receipt surfaces were read
- whether those reads came from execution-record truth or from a truthful placeholder
- where recommendation-history and every-pass receipt concerns are reserved without policy

Those outputs do not answer the question:

- whether to open, add, rotate, exit, or close a position

A later step in the system does not treat a downstream state-read result as if it were a behavioural decision packet.

## Downstream recommendation-history reservation outputs

The downstream bootstrap owns a reservation output. That reservation output answers these questions and no others:

- the existing receipt tables that anchor later same-pass and recent-pass checks
- the future home where recommendation-history reading will live
- that no duplicate-policy or recent-open formula is installed yet

A later step in the system does not treat that reservation as if the duplicate-policy itself already exists.

## Downstream review and receipt outputs

The downstream review layer owns review outputs that state what downstream architecture receipts read, deferred, and preserved.

Those review outputs do not own the operating decisions of those shells.

A later step in the system does not treat a downstream review receipt as if the review layer itself owned opening, management, rotation, exit, or close behaviour.

## Later-step usage law

A later step in the system uses the runtime output that directly answers the question being asked.

A later step in the system does not prefer a less truthful output merely because it is easier to consume.

If a runtime output exists only for compatibility, that output does not replace the clearer live output underneath it.

If a packet reader has both common-envelope metadata and a clearer preserved runtime surface, the clearer preserved runtime surface still owns the answer to the question it was designed to answer.

Compatibility handling is lawful.

Compatibility handling does not erase the more truthful runtime output.

## Review law

The runtime preserves enough separation that the review layer states, in plain language:

- what runtime truth was admitted and prepared
- what financial-calendar truth was preserved
- what candidate was formed
- what serial stage outputs inside the desk-cognition spine concluded
- what the independent parallel risk lane concluded
- what the downstream pre-deployment gate blocked or allowed
- what capital deployment authority decided
- what downstream opening, execution, inventory, and close surfaces preserved

If a reviewer cannot tell which bounded part of the system produced which result, the runtime output model is wrong.

## Ownership conflict law

A runtime output is in conflict if it appears to answer a question outside its bounded role.

That conflict is resolved by one of these actions:

- narrow the output back to its bounded meaning
- preserve a separate output for the different question
- revise the live control documents explicitly and lawfully

The conflict is not hidden by vague wording or blended review output.

## Native Architecture Blueprint boundary

Within native code-structure architecture scope, this document must be read with `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

`docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` owns target package placement, component form, seams, ownership, persistence, test-family mapping, reservations, module allocation, and traceability for native code-structure architecture.

It does not override the authority hierarchy defined by `docs/01_NORMATIVE_CORE.md`.

All durable terms used by live control documents must be governed by `docs/vocabulary/vocabulary_registry.md` or lawfully admitted by the vocabulary process before they become canonical language.
